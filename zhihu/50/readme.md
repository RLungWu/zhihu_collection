# 目前大模型量化方案有很多，有哪些比较SOTA的量化方案？
大模型的壓縮可以分成三個部份，模型剪枝(Pruning)、知識蒸餾(Knowledge Distillation)與模型量化(Quantization)。
## 簡單說明
模型量化是一個直接減少模型佔用記憶體的大小和計算量的一種方法，透過將模型參數(Weight) 從高精度的數據類型(float32, float14) 轉換成低精度的數據類型(int8, fp8)。　在相同的參數量下，透過減少每個參數佔用的位數來減少模型佔用的記憶體。

## 模型量化的粒度
- Per-tensor(pre-layer) 量化： 每層或每個張量只有一個縮放因子，張量內的所有值都被這個縮放因子量化。
- Per-channel 量化：　卷積核的每個通道都有不同的縮放因子。
- Per-token 量化：　針對激活而言，針對每一行進行量化。　在LLM當中，通常與 Pre-channel 量化搭配使用，讓我們可以針對每一個　Token 量化來激活，針對每一個通道量化權重。
- Per-group/group-wise: 以組為單位。　正如 Q-BERT:Hessian Based Ultra Low Precision Quantization of BERT 所說的那樣，分組量化的一個特殊情況是將每個密集矩陣視為一組，每個矩陣都可以有自己的量化範圍。兒更普遍的情況是將每個密集矩陣按照輸出神經元進行分割，每個連續的ｎ輸出神經元作為一個組。像是GPTQ, AWQ 當中使用128個元素當作一組來量化。有些地方也稱為子通道分組量化，是比 Pre-Channel 更精細的一種量化。

## 模型量化對象
- Weight: 正如前面所說，權重的量化是最常見的對象。而且權重在訓練完成之後舊故訂了，數值範圍與輸入無關，因此我們可以離線完成量化。
- Activation: Activation 其實才佔用了絕大部分的記憶體。因此量化 Activation 不僅可以大大減少記憶體使用，更重要的是，我們可以顯著的提昇模型推理的性能。但 Activation 輸出隨輸入變化，因此更難量化。
- KV Cache: KV Cache 也會消耗不少的記憶體，因此量化　KV Cache 對於提高模型長序列生成的吞吐量至關重要。
- Gradient: 主要是在訓練的時候來訓練，因為反向傳播會比較重要。

## 動態量化與靜態量化
對於 Activation 來說，靜態量化是指採用具有代表性的數據來產生縮放因子和零點，這些參數在整個生命週期當中保持不便。相較於動態量化，靜態量化因為不需要在前項傳播時動態計算，因此效率會比較高。

動態量化則是只在每次前向傳播時計算激活的最大最小值。像是模型的參數可能是　[1,255,35,45]，在前向傳播時會被當成[0.001, 0.32,0.032,0.002]，因此會需要動態計算。

## 線性量化與非線性量化
根據量化數據的範圍是否均勻，我們可以非成線性與非線性。主要是依據是否是使用線性的方式來決定。

## 量化數據類型
LLM 主要有三種類型量化：
- 僅權重量化：只量化每個線性層的權重張量 W
- 權重激活量化：量化每個線性層的輸入 Activation X 和權重張量 W
- kv Cache 量化：量化每個 Attention Blocks 中的張量K和值張量 V

一些典型的方案：
**針對僅權重量化： **
- 對於 W8A16 量化，代表方法有 MinMax 
- 對於 W6A16 量化，代表方法有 FP6-LLM 
- 對於 W4A16 量化，代表方法有 AWQ、GPTQ、SpQR、OmniQuant、QuIP# 
- 對於 W3A16 量化，代表方法有 GPTQ、SpQR、OmniQuant、QuIP#
- 對於 W2A16 量化，代表方法有 OmniQuant、QuIP、QuIP# 
**針對權重激活量化： **
- 對於 W8A8 量化，代表方法有 LLM.int8()、SmoothQuant、ZeroQuant 
- 對於 W6A6 量化，代表方法有 OmniQuant 
- 對於 W4A8 量化，代表方法有 QoQ 
- 對於 W4A4 量化，代表方法有 Atom 、QuaRot、OmniQuant 
**針對 KV Cache量化： **
- KV8：INT8（LMDeploy、TensorRT-LLM）、FP8（TensorRT-LLM、vLLM） 
- KV4：Atom、QuaRot、QoQ 
- KV3：KVQuant 
- KV2：KVQuant、KIVI
