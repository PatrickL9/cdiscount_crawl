# -*- coding: UTF-8 -*-
#!/usr/bin/python3

"""
爬虫程序各项配置参数
@Author ：Patrick Lam
@Date ：2023-02-13
"""

import redis
import os
import datetime
from util import logging_util

# 代理API
PROXY_URL = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=460e34f07cf041899a22e79353081288&orderno=YZ2021112078186AsWJy&returnType=1&count=1'
ipPool = []

# 主页链接
main_url = 'https://www.cdiscount.com/'
# 请求头
headers = {
    'Host': 'www.cdiscount.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Cookie': 's_ecid=MCMID|18341238211178450613597517558168624104; app_vi=34041600|; prio7j=prio4; prio30j=prio4; s_cc=true; AMCVS_6A63EE6A54FA13E60A4C98A7@AdobeOrg=1; AMCV_6A63EE6A54FA13E60A4C98A7@AdobeOrg=1585540135|MCIDTS|19402|MCMID|18341238211178450613597517558168624104|MCAID|NONE|MCOPTOUT-1676281687s|NONE|vVersion|4.4.0; tcId=bc84cffc-5831-4c45-a997-ae39f24332ef; ___utmvm=###########; _$dtype=t:d; CookieId=CookieId=230213084820IKEOHGRQ&IsA=0; mssctse=W2dNXeEyrPIEsW5Db5bOJJ3RYQdI1H2i250xOsbJcL6ru5NoZGxIuDepaGyWNzLTchrxR3qH5P7IYOoZjt8H3Q; rxVisitor=1676274503537KHKQR1K6N8EEGPDH8U7AGQ447VR0R5CC; TC_AB=A; UniqueVisitContext=UniqueVisitId__230213084825NDRXSOMA__; _$3custinf=AUT=0&XV1=0; SitePersoCookie=PersoCountryKey____PersoLatitudeKey____PersoLongitudeKey____PersoTownKey____GeolocPriorityKey__0__PersoPostalCodeKey____PersoUrlGeoSCKey____ExpressSellerId____ExpressShopName____ExpressGlobalSellerId____ShowroomVendorId____RetailStoreName____VehicleId__0__AddressId____; dtLatC=5; TCPID=123211548322328687505; dtCookie=v_4_srv_21_sn_1562859F08A1BE4D709D981A3AFF73EC_app-3Ac93cbedcccfc6fbb_0_ol_0_perc_100000_mul_1; el2=0; _cs_c=3; TC_PRIVACY=0@078|2|2|183@4,1,5,3,2,6,10001,10003,10005,10007,10013,10015,10017,10019,10009,10011,13002,13001,10004,10014,10016,10018,10020,10010,10012,10006,10008@@1676274530215,1676274530215,1691826530215@_u_PvZ8a-F4BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACKqOn6gO_u-YujiLKfB6576K-C69kmqC-amoFqaKCY8KqbrzqmOjqi4oYACg7gBoh6oHkMrqIGgKhgIPirmOPvYe4BiK7XmwcYOg6KgLioaiaCYuIDYGIoGOgHgmAungimABgCCACKghiooEGoiQGgiGEoGpAnYCAIiCgiGBKo4oAigqApoCCGCBqaYAKCKg6AgSAYghsKKBgvioeKOAAogOiCom8oWgiIALorCABiKLCGoqiHq4uKi4uzTvgoEKo6sqiuqziquubhurngiq6xqvGZjHqojxqKKrn7uqGqirEo4EpgAQ==; TC_PRIVACY_CENTER=4,1,5,3,2,6,10001,10003,10005,10007,10013,10015,10017,10019,10009,10011,13002,13001,10004,10014,10016,10018,10020,10010,10012,10006,10008; tcIdNe=6c5d2dee-18a7-4b45-9d9e-3bd25e8feff5; _$1okcook=1; _$cst=1; _gcl_au=1.1.1444178624.1676274533; _scid=2d4d4585-66dc-4979-b0ff-9b817f04d3a7; mics_vid=32430846866; mics_lts=1676274535440; _MFB_=fHwxfHx8W118fHw1NC44Nzg1ODg5NDIwMDA1MDV8; msswt=; SiteVersionCookie=1547.1|2038.1|2054.0|2524.1|3027.0|3032.1|3033.1|3040.0|4012.1|4018.1|4019.1|4026.1|4028.1|4033.0|4039.1|4048.1|4050.0|4302.1|4305.1|4308.1|4513.1|4514.1|4517.1|4521.0|4525.1; SiteVersionCookieNoChanges=1370.1|1418.1|1423.1|1426.1|1433.1|1441.1|1458.1|1464.0|1466.1|1467.1|1469.1|1475.1|1482.1|1484.1|1488.1|1491.1|5008.1|5015.1|5016.0|5019.1|5021.1|5023.1|5024.1|5030.1|5033.1|5038.0|5042.0|5043.0|5044.1; dtPC=21$474503536_63h-vLWPPQVFAFCBCGKKOEWRRFNAPSUPTARNN-0; rxvt=1676278170759|1676276370759; svisit=1; visit_baleen_ACM-655d44=XjY0d3Fm9hKJVhNn81NfqFzu7jKFYaMA9fzcb08mmVG_jJNBwVeyJkptPjo_KFlHBKS_F0wYULMY_O8fh6A9_4asTVairEe1WolnE8ffIuiKZ4PNZVD7D-e7RHw5Cyt4mPWuYso7Xho84dbUhnizye_x2ob0roy2HmAsCBkv92QncOd2HK27i3sOr9LIk9JYnIk3ajsw_bRoskUBNpcaFXMVLvtLZI0pWcQTzeeZ3ccnzm_Jc2GRx6bnA2J-xztbEsLp6qAL_um_e_UpiG7leaiQ-h3H4sUn10Ofhzn4EQc; TBMCookie_6223335112164439712=6273160016762775225FkZvATwostGbpa0GRy9cV5rnqc=; _$3ci=; __gads=ID=936c6af265ec852b:T=1676277529:S=ALNI_MY2b-6uwcEvFuWGU0mDKtU8VRgGpg; __gpi=UID=00000bc0d33d87e3:T=1676277529:RT=1676277529:S=ALNI_MZJxHrK9DryhSHHSEUX0qs2ou8_Sg; _cs_cvars={"8":["h_deb_session","16"]}; fpg=1; iadvize-11-vuid=eb97b03f117eaee697a777cb7013cbd463e9f7b3ef786; iadvize-11-consent=true; cache_cdn=; _uetsid=dce9ebd0ab7211ed8a2f859677a7f1e6; _uetvid=dce9e330ab7211ed800961e8b7c9d70a; visit_baleen_ACM-655d43=JmNaL4p84LHEfek6eFD6LVZa66jwFKkom4tn-Rgb4Z5KgN8np3yH7kEkKGe7ph5G4fKmiu8xu8tGLAC37QHonUDTvp7gm4zZ3sKG9M05fBsT0txK2cQc-jhfluYFzh1Dw4VaQ_p7qqRpl-SXoLSqQuY-bgdfs-Xx-w3h6qv1gBc2dnLsHUlvv3eLvxIctAGvahBfFs4UWsc9S_K-6afeq6X9-2O6-EPnZtHldDno_l4QjgAdqF78p4EW4HRE7f5K; msstvt=VuCLfhaWGAqOMmypHvUu_4tZDze0AZIWsm0SD5PMa9O2Z5Ut1sLv7kNc2iStLf9uNtfprgIikPwRY3Jopem3iq8Rmi6JqTfAK1VDkpOWbXF821_j8VWNzoYrpOOr6QQN8LR5kevlK2kdJc1SzkoTAQ; _cs_id=d9ed3693-26e0-adfc-e3ee-6ef4b4fa7927.1676274526.2.1676277959.1676277174.1590586488.1710438526503; _cs_s=3.0.0.1676279759123; cs_heure_session=16; chcook7=direct; s_nr=1676277963852-Repeat; s_pv=Home; ABTastySession=mrasn=&lp=https%3A%2F%2Fwww.cdiscount.com%2Fjuniors%2Fpoupees-poupons%2Fpoussette-double-canne-landau-bebe-pliable-a-4-rou%2Ff-1206404-auc6971664983692.html%3FidOffre%3D342299516%23mpos%3D0%7Cmp%26sw%3D893db8137e96607de37268aef9444fb6e2e002869ae54bc99ca55a6e116b9ffdd40f1f8907a90213944de46b3730bb1debf56eceb45bfedf811146951c84a72c016409590f3142c65dd8a8edc8ba15eaca7c45f9d204bc70cbf2bee4e5602ae7d775b4b852c205c999485ce1fa7eb5c1127809c10105e9e2e8ef13b3d7b2363c; ABTasty=uid=0dectwpjgs44c4yx&fst=1676274533826&pst=1676274533826&cst=1676277526702&ns=2&pvt=5&pvis=4&th=723627.899155.1.1.1.1.1676277964464.1676277964464.1.2_884141.1101374.1.1.1.1.1676274534659.1676274534659.1.1_888659.1106982.3.3.1.1.1676277527559.1676277694420.1.2_908953.1133635.5.4.2.1.1676274534094.1676277964466.1.2_945303.1178112.4.3.2.1.1676274534582.1676277694430.1.2; cto_bundle=FP8WX195TkFIaXRZMmhJRzBEN2FQVlBBaFJwRFBBUUhHWnRhOEhUb2JFOXhUdGdPWWoydWhPS01ybDRnOXFaZW5ob0NjSWMlMkJwdiUyQjg1TEtTMGs2SlhqQm0xNnZkNmF4MG5yTnpodU5meFFrNmVUWHNteXg3WkpXTjElMkZ6OFhNUlZKSUh3RFJJaHdmWWdhbndWWE1yQU43dHQ2V3clM0QlM0Q; tp=12536; s_ppv=Home,8,8,969; VisitContextCookie=O4YBwcpjA9LOIFoJGYtg2cseFSaH88ZhDAIkBPJcfCpUU9Y2VIz5Hg',
}

# 日志级别
LOGGING_LEVEL = 'INFO'
# 日志文件保存路径
logging_dir = os.getcwd() + r'\log'
if not os.path.isdir(logging_dir):
    os.makedirs(logging_dir)
# 日志文件前缀处理
to_day = datetime.datetime.now()
LOGGING_PATH = logging_dir + r'\cd_crawl_{}{:02}{:02}.log'.format(to_day.year, to_day.month, to_day.day)
# 设置日志级别
logging = logging_util.LoggingUtil(LOGGING_LEVEL, LOGGING_PATH).get_logging()

