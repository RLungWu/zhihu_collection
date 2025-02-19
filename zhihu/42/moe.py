import torch
import torch.nn as nn
import torch.nn.Functional as F 


# This is an Expert model.
# It's an easy MLP.
class Expert(nn.Module):
    def __init__(self, n_embd):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_embd, 4 * n_embd),
            nn.ReLU(),
            nn.Linear(4 * n_embd, n_embd),
            nn.Dropout(dropout),
        )
    
    def forward(self, x):
        return self.net(x)


# This is MOE router
# We define 4 expert, router will take 2 experts. That is expert = 4, top_k = 2. 
# We define n_embed = 32, num_experts = 4, top_k = 2
class TopkRouter(nn.Module):
    def __init__(self, n_embed, num_experts, top_k):
        super(TopkRouter, self).__init__()
        self.top_k = top_k
        self.linear = nn.Linear(n_embed, num_experts)
    
    
    def forward(self, mh_output):
        logits = self.linear(mh_output) # (2, 4, 32)  --> (2, 4, 4)
        
        top_k_logits, indices = logits.topk(self.top_k, dim = -1)
        
        zeros = torch.full_like(logits, float('-inf')) # (2, 4, 4)
        
        # 按照索引和值填充上述zeros矩阵
        sparse_logits = zeros.scatter(-1, indices, top_k_logits)
        
        router_output = F.softmax(sparse_logits, dim = -1)
        
        return router_output, indices


class NoisyTopkRouter(nn.Module):
    def __init__(self, n_embed, num_experts, top_k):
        super(NoisyTopkRouter, self).__init__()
        self.top_k = top_k
        self.topkroute_linear = nn.Linear(n_embed, num_experts)
        
        # add noise
        self.noise_linear = nn.Linear(n_embed, num_experts)
    
    def forward(self, mh_output):
        #mh_output is the output tensor from multihead self attention block
        logits = self.toprouter_linear(mh_output)
        
        # Noise llgits
        noise_logits = self.noise_linear(mh_output)
        
        # Adding scaled unit gaussian noise to the logits
        noise = torch.randn_like(logits) * F.softplus(noise_logits)
        noisy_logits = logits + noise
        
        top_k_logits, indices = noisy_logits.topk(self.top_k, dim = -1)
        zeros = torch.full_like(noisy_logits, float('-inf'))
        sparse_logits = zeros.scatter(-1, indices, top_k_logits)
        router_output = F.softmax(sparse_logits, dim = -1)
        return router_output, indices


class SparseMoe(nn.Module):
    def __init__(self, n_embed, num_experts, top_k):
        super(SparseMoe, self).__init__()
        self.router = NoisyTopkRouter(n_embed, num_experts, top_k)
        self.experts = nn.ModuleList([Expert(n_embed) for _ in range(num_experts)])
        self.top_k = top_k
    
    def forward(self, x):
        # input router and get 2 output
        gating_output, indices = self.router(x)
        
        # Initialize zero array
        final_output = torch.zeros_like(x)
        
        # flatten,
        flat_x = x.view(-1, x.size(-1))
        flat_gating_output = gating_output.view(-1, gating_output.size(-1))
        
        
        for i, expert in enumerate(self.experts):
            expert_mask = (indices == i).any(dim = -1)
            flat_mask = expert_mask.view(-1)
            
            if flat_mask.any():
                expert_input = flat_x[flat_mask]
                
                expert_output = expert(expert_input)
                
                gating_scores = flat_gating_output[flat_mask, i].unsqueeze(1)
                
                weighted_output = expert_output * gating_scores
                
                final_output = expert_output * gating_scores
                
                final_output[expert_mask] += weighted_output.squeeze(1)
        
        return final_output


class Block(nn.Module):
    '''
    Mixuture of experts transformer block: communication followed by computation( multi-head self attention _ sparseMOE)
    '''
    def __init__(self, n_embed, n_head, num_experts, top_k):
        super().__init__()
        head_size = n_embed //n_head
        self.sa = MultiHeadAttention(n_head, head_size)
        self.smoe = SparseMoe(n_embed, num_experts, top_k)
        self.ln1 = nn.LayerNorm(n_embed)
        self.ln2 = nn.LayerNorm(n_embed)
    
    def forward(self, x):
        x = x + self.sa(self.ln1(x))
        x = x + self.smoe(self.ln2(x))
        
        return x