#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import sys
from time import sleep
from log import logger

base_taobao_url = "http://ip.taobao.com/service/getIpInfo.php"
base_sina_url = "http://int.dpool.sina.com.cn/iplookup/iplookup.php" # 新浪库准确率太低，抛弃他

def query_ip(ip):
    payload = {"ip":ip}
    resultL = []
    while True:
        try:
            payload.pop("format", 0)
            result = requests.get(base_taobao_url, params=payload, timeout=5)
            if result.status_code == 200:
                json = result.json()
                resultL.append(json["data"])
                break
            else:
                logger.warn("request ip.taobao error, maybe too many requests, let's wait a while")
                sleep(1)
        except Exception, e:
            logger.error("request taobao exception: " + str(e.message))

    if resultL:
        rjson = reduce(lambda d1,d2: dict(d1.items() + { k:v for k,v in d2.items() if v }.items()), resultL)
    else:
        rjson = reduce(lambda d1,d2: dict(d1.items() + { k:v for k,v in d2.items() if v }.items()), resultL,{})
    if rjson:
        if not rjson.get("province", ""):
            rjson["province"] = rjson.get("region", "")
            rjson["city"] = rjson.get("city", "")
            rjson["isp"] = rjson.get("isp", "")
        #print rjson
        return rjson

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        ip = sys.argv[1]
    else:
        ip = "199.19.226.150"
    print query_ip(ip)
