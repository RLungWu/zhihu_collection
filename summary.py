import requests

link = "https://zhuanlan.zhihu.com/p/713256008?utm_psn=1850877468791164928"

def get_page(url):
    headers = {
        "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language":"zh-TW,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control":"max-age=0",
        "cookie":"__snaker__id=TeSHQqULPEXiKp8C; SESSIONID=Id6y4ytXSMfd1Kkv2YRUgRzoGohgqfN29dbA15rv4Q5; JOID=UFkWBU97pGCb97s_KH-hMwnYQ8AwMeE075zac1kV3Tfbv4xoZwZDz_jyujgvJO4v3_se0lqc-_IMY6WsoKy3bPg=; osd=UFscA0l7pmqd8bs9InmnMwvSRcYwM-sy6ZzYeV8T3TXRuYpoZQxFyfjwsD4pJOwl2f0e0FCa_fIOaaOqoK69av4=; _xsrf=ki1lwb7Xm3AMmkBajKAr4DmOb1n4Nsqx; _zap=301c6030-1c2f-47a1-b3d2-6770b1611c27; d_c0=BDBSuYB85BmPTuDm_NlgL4VVH9YUVQYb-NU=|1737610188; __zse_ck=004_NfHF6R01CxEN5sEN/aBKIPDnABIEoJ6lNRIf1eR/7uVfakWC47NYWcuErgKnTUdSuE739PgRgLhgwSLUmgbnKI7iZ1dqtRsfSW=OYczPKOy82CkxhIQogQQ0aZrKjF2J-9YmYkkyiCGFzSFMygeqkPxhhKP2pJtW59vUFfL3VqGq9pzBxpy6Bwr0MKd3mHLj8UBcgCzCC22pf51vJVR8TmIkh8h58MQkGl9tlUyjMm8AH6jsnGvGp+tOtdp5TV4bL; gdxidpyhxdE=aQiyGD%2Bd4cmn3EgzDwzqZgPMtThgBLf%5Cfv1jVZErTe5a%5CK2%2BgE5cAdMfuGWZo7qmSLEBsHTi2SKsn92%2FOkLLbbub%2FhWoQ3frqlQu665jAo5JIqSbexeCzsXekwiu2GlkS7iMYqtvU75hifaUW0JXr28PvyG6lllHoJsLoiEMtbP5Rhfo%3A1739120948756; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1739120051; HMACCOUNT=2B57A0F9912B23F0; captcha_session_v2=2|1:0|10:1739120053|18:captcha_session_v2|88:MFpHb2ROSFludkpoWnY5WUpsUWQvNUJZNXV6Mktaa0tJRUp0TTBYVTBpcFFoYVFlclRwL1FiOWdLMEZQL2w3dg==|9292fd42599b06b008ab866bdba7173a421b68baa7968cfbfd10eddb06abe95a; tst=r; z_c0=2|1:0|10:1739120723|4:z_c0|92:Mi4xZTRFTE93QUFBQUFFTUZLNWdIemtHU1lBQUFCZ0FsVk54aXVXYUFBNlcyZnhveHY0c05wX0RQOXdXU1I0alVpekJn|4e3737fc3ab6e7d12b4cc642d20da93e25828ab8aa3fe62da0cab5b988e9ba56; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1739120774; BEC=030db281a345ec21f9cf5bbc04693de6",
        "dnt":"1",
        "priority":"u=0, i",
        "sec-ch-ua":"Microsoft Edge",
        "sec-ch-ua-mobile":"?0",
        "sec-ch-ua-platform":"Linux",
        "sec-fetch-dest":"document",
        "sec-fetch-mode":"navigate",
        "sec-fetch-site":"none",
        "sec-fetch-user":"?1",
        "upgrade-insecure-requests":"1",
        "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
    }

    
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    return response.text

url = link

html_content = get_page(url)
print(html_content)