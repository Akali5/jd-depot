#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_opencardH1228.py(12.28-1.28 品牌会员年度盛典)
Author: HarbourJ
Date: 2022/12/28 21:00
TG: https://t.me/HarbourToulu
cron: 1 1 1 1 1 1
new Env('12.28-1.28 品牌会员年度盛典');
ActivityEntry: https://lzdz1-isv.isvjcloud.com/m/1000072521/9380848/dzd5d739ab4fa4916380c44baa9c45/?shareUuid=3d246317319f4cefbe8e57a6a52958dc&adsource=null
Description: 开卡5 邀请10
            并发变量: export jd_opencard1228_uuid="你的助力码"
"""

import time
import requests
import sys
import re
import os
from datetime import datetime
import json
import random
from urllib.parse import quote_plus, unquote_plus
from functools import partial
print = partial(print, flush=True)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

try:
    from jd_sign import *
except ImportError as e:
    print(e)
    if "No module" in str(e):
        print("请先运行HarbourJ库依赖一键安装脚本(jd_check_dependent.py)，安装jd_sign.so依赖")
    sys.exit()
try:
    from jdCookie import get_cookies
    getCk = get_cookies()
except:
    print("请先下载依赖脚本，\n下载链接: https://raw.githubusercontent.com/HarbourJ/HarbourToulu/main/jdCookie.py")
    sys.exit(3)

redis_url = os.environ.get("redis_url") if os.environ.get("redis_url") else "172.17.0.1"
redis_port = os.environ.get("redis_port") if os.environ.get("redis_port") else "6379"
redis_pwd = os.environ.get("redis_pwd") if os.environ.get("redis_pwd") else ""
inviterUuid = os.environ.get("jd_opencard1228_uuid") if os.environ.get("jd_opencard1228_uuid") else ""

venderId = "1000072521"
activityId = "dzd5d739ab4fa4916380c44baa9c45"
activity_url = f"https://lzdz1-isv.isvjcloud.com/m/1000072521/9380848/{activityId}/?shareUuid={inviterUuid}&adsource=null"
print(f"【🛳活动入口】https://lzdz1-isv.isvjcloud.com/m/1000072521/9380848/{activityId}")

def redis_conn():
    try:
        import redis
        try:
            pool = redis.ConnectionPool(host=redis_url, port=redis_port, decode_responses=True, socket_connect_timeout=5, password=redis_pwd)
            r = redis.Redis(connection_pool=pool)
            r.get('conn_test')
            print('✅redis连接成功')
            return r
        except:
            print("⚠️redis连接异常")
    except:
        print("⚠️缺少redis依赖，请运行pip3 install redis")
        sys.exit()

def getToken(ck, r=None):
    host = f'{activityUrl.split("com/")[0]}com'
    try:
        pt_pin = unquote_plus(re.compile(r'pt_pin=(.*?);').findall(ck)[0])
    except:
        pt_pin = ck[:15]
    try:
        try:
            Token = r.get(f'{activityUrl.split("https://")[1].split("-")[0]}_{pt_pin}')
        except Exception as e:
            print(f"redis get error: {str(e)}")
            Token = None
        if Token is not None:
            print(f"♻️获取缓存Token")
            return Token
        else:
            s.headers = {
                'Connection': 'keep-alive',
                'Accept-Encoding': 'gzip, deflate, br',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'User-Agent': '',
                'Cookie': ck,
                'Host': 'api.m.jd.com',
                'Referer': '',
                'Accept-Language': 'zh-Hans-CN;q=1 en-CN;q=0.9',
                'Accept': '*/*'
            }
            sign({"url": f"{host}", "id": ""}, 'isvObfuscator')
            f = s.post('https://api.m.jd.com/client.action', verify=False, timeout=30)
            if f.status_code != 200:
                print(f.status_code)
                return
            else:
                if "参数异常" in f.text:
                    print(f.text)
                    return
            Token_new = f.json()['token']
            try:
                if r.set(f'{activityUrl.split("https://")[1].split("-")[0]}_{pt_pin}', Token_new, ex=1800):
                    print("✅Token缓存成功")
                else:
                    print("❌Token缓存失败")
            except Exception as e:
                print(f"redis set error: {str(e)}")
                print(f"✅获取实时Token")
            return Token_new
    except Exception as e:
        print(f"Token error: {str(e)}")
        return

def getJdTime():
    jdTime = int(round(time.time() * 1000))
    return jdTime

def randomString(e, flag=False):
    t = "0123456789abcdef"
    if flag: t = t.upper()
    n = [random.choice(t) for _ in range(e)]
    return ''.join(n)

def refresh_cookies(res):
    if res.cookies:
        cookies = res.cookies.get_dict()
        set_cookie = [(set_cookie + "=" + cookies[set_cookie]) for set_cookie in cookies]
        global activityCookie
        activityCookieMid = [i for i in activityCookie.split(';') if i != '']
        for i in activityCookieMid:
            for x in set_cookie:
                if i.split('=')[0] == x.split('=')[0]:
                    if i.split('=')[1] != x.split('=')[1]:
                        activityCookieMid.remove(i)
        activityCookie = ''.join(sorted([(set_cookie + ";") for set_cookie in list(set(activityCookieMid + set_cookie))]))

def getActivity():
    url = "https://lzdz1-isv.isvjcloud.com/wxCommonInfo/token"
    headers = {
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': ua,
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': activityUrl
    }
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        if response.cookies:
            cookies = response.cookies.get_dict()
            set_cookies = [(set_cookie + "=" + cookies[set_cookie]) for set_cookie in cookies]
            set_cookie = ''.join(sorted([(set_cookie + ";") for set_cookie in set_cookies]))
        return set_cookie
    else:
        print(response.status_code, "⚠️ip疑似黑了,休息一会再来撸~")
        sys.exit()

def getMyCidPing(index, venderId):
    url = "https://lzdz1-isv.isvjcloud.com/customer/getMyCidPing"
    payload = f"userId={venderId}&token={token}&fromType=APP&pin="
    headers = {
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz1-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)
    res = response.json()
    if res['result']:
        return res['data']['nickname'], res['data']['secretPin'], res['data']['cid'] # c3f202cfbc91c3fa90c74b38a1855783
    else:
        print(f"⚠️{res['errorMessage']}")
        if index == 1 and "火爆" in res['errorMessage']:
            print(f"\t⛈车头黑,退出本程序！")
            sys.exit()

def getSystemConfigForNew():
    url = "https://lzdz1-isv.isvjcloud.com/wxCommonInfo/getSystemConfigForNew"
    payload = f'activityId={activityId}&activityType=99&pin='
    headers = {
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz1-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)

def getSimpleActInfoVo():
    url = "https://lzdz1-isv.isvjcloud.com/dz/common/getSimpleActInfoVo"
    payload = f"activityId={activityId}&pin="
    headers = {
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz1-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)
    res = response.json()
    if res['result']:
        return res['data']
    else:
        print(res['errorMessage'])

def init():
    url = "https://lzdz1-isv.isvjcloud.com/dingzhi/taskact/common/init"
    payload = f"activityId={activityId}&pin="
    headers = {
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz1-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)

def accessLogWithAD(venderId, pin):
    url = "https://lzdz1-isv.isvjcloud.com/common/accessLogWithAD"
    payload = f"venderId={venderId}&code=99&pin={quote_plus(pin)}&activityId={activityId}&pageUrl={quote_plus(activityUrl)}&subType=JDApp&adSource=null"
    headers = {
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz1-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)

def getSystime():
    url = "https://lzdz1-isv.isvjcloud.com/common/getSystime"
    headers = {
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Origin': 'https://lzdz1-isv.isvjcloud.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': activityCookie,
        'Content-Length': '0',
        'Connection': 'keep-alive',
        'Accept': 'application/json',
        'User-Agent': ua,
        'Referer': activityUrl,
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'X-Requested-With': 'XMLHttpRequest'
    }
    response = requests.request("POST", url, headers=headers)
    refresh_cookies(response)

def getUserInfo(pin):
    url = "https://lzdz1-isv.isvjcloud.com/wxActionCommon/getUserInfo"
    payload = f"pin={quote_plus(pin)}"
    headers = {
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz1-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)
    res = response.json()
    if res['result']:
        return res['data']['nickname'], res['data']['yunMidImageUrl'], res['data']['pin']
    else:
        print(res['errorMessage'])

def activityContent(pin, pinImg, nickname):
    url = "https://lzdz1-isv.isvjcloud.com/dingzhi/years/brandUnion/activityContent"
    try:
        yunMidImageUrl = quote_plus(pinImg)
    except:
        yunMidImageUrl = quote_plus("https://img10.360buyimg.com/imgzone/jfs/t1/21383/2/6633/3879/5c5138d8E0967ccf2/91da57c5e2166005.jpg")
    payload = f"activityId={activityId}&pin={quote_plus(pin)}&pinImg={yunMidImageUrl}&nick={quote_plus(nickname)}&shareUuid={shareUuid}"
    headers = {
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz1-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': f'IsvToken={token};{activityCookie}'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)
    res = response.json()
    if res['result']:
        return res['data']
    else:
        print(res['errorMessage'])
        if "活动已结束" in res['errorMessage']:
            sys.exit()

def drawContent(pin):
    url = "https://lzdz1-isv.isvjcloud.com/dingzhi/taskact/common/drawContent"
    payload = f"activityId={activityId}&pin={quote_plus(pin)}"
    headers = {
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz1-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    requests.request("POST", url, headers=headers, data=payload)

def getShareRecord(pin, actorUuid):
    url = "https://lzdz1-isv.isvjcloud.com/dingzhi/taskact/common/getShareRecord"
    payload = f"activityId={activityId}&pin={quote_plus(pin)}&actorUuid={actorUuid}"
    headers = {
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz1-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    res = response.json()
    if res['result']:
        return res['data']
    else:
        print(res['errorMessage'])

def initOpenCard(pin, actorUuid, shareUuid):
    url = "https://lzdz1-isv.isvjcloud.com/dingzhi/years/brandUnion/initOpenCard"
    payload = f"activityId={activityId}&pin={quote_plus(pin)}&actorUuid={actorUuid}&shareUuid={shareUuid}"
    headers = {
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz1-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)
    res = response.json()
    if res['result']:
        return res['data']
    else:
        print(res['errorMessage'])

def saveTask(actorUuid, shareUuid, pin, taskType, taskValue):
    url = "https://lzdz1-isv.isvjcloud.com/dingzhi/years/brandUnion/saveTask"
    payload = f"activityId={activityId}&actorUuid={actorUuid}&shareUuid={shareUuid}&pin={quote_plus(pin)}&taskType={taskType}&taskValue={taskValue}"
    headers = {
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz1-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    res = response.json()
    if res['result']:
        data = res['data']
        print(f"saveTask-->{data}")
        return data
        # if data['score'] == 0:
        #     print("\t获得 💨💨💨")
        # else:
        #     print(f"\t🎉获得{data['score']}积分")
    else:
        print(f"\t{res['errorMessage']}")

def bindWithVender(cookie, venderId):
    try:
        s.headers = {
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': ua,
            'Cookie': cookie,
            'Host': 'api.m.jd.com',
            'Referer': 'https://shopmember.m.jd.com/',
            'Accept-Language': 'zh-Hans-CN;q=1 en-CN;q=0.9',
            'Accept': '*/*'
        }
        s.params = {
            'appid': 'jd_shop_member',
            'functionId': 'bindWithVender',
            'body': json.dumps({
                'venderId': venderId,
                'shopId': venderId,
                'bindByVerifyCodeFlag': 1
            }, separators=(',', ':'))
        }
        res = s.post('https://api.m.jd.com/', verify=False, timeout=30).json()
        if res['success']:
            return res['message']
    except Exception as e:
        print(e)

def getShopOpenCardInfo(cookie, venderId):
    try:
        body = {"venderId": str(venderId), "channel": "401"}
        url = f'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=getShopOpenCardInfo&body={json.dumps(body)}&client=H5&clientVersion=9.2.0&uuid=88888'
        headers = {
            'Host': 'api.m.jd.com',
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Cookie': cookie,
            'User-Agent': ua,
            'Accept-Language': 'zh-cn',
            'Referer': 'https://shopmember.m.jd.com/',
            'Accept-Encoding': 'gzip, deflate'
        }
        response = requests.get(url=url, headers=headers, timeout=5).text
        res = json.loads(response)
        if res['success']:
            venderCardName = res['result']['shopMemberCardInfo']['venderCardName']
            return venderCardName
        else:
            return venderId
    except:
        return venderId


if __name__ == '__main__':
    r = redis_conn()
    try:
        cks = getCk
        if not cks:
            sys.exit()
    except:
        print("未获取到有效COOKIE,退出程序！")
        sys.exit()
    global shareUuid, inviteSuccNum, activityUrl, firstCk
    inviteSuccNum = 0
    if len(cks) == 1:
        shareUuid = inviterUuid
        activityUrl = activity_url
    else:
        shareUuid = remote_redis(f"lzdz1_{activityId}", 2)
        activityUrl = f"https://lzdz1-isv.isvjcloud.com/m/1000077335/7722148/{activityId}/?shareUuid={shareUuid}&adsource=null"
    num = 0
    for cookie in cks[:]:
        num += 1
        if num == 1:
            firstCk = cookie
        if num % 8 == 0:
            print("⏰等待10s,休息一下")
            time.sleep(10)
        global ua, activityCookie, token
        ua = userAgent()
        try:
            pt_pin = re.compile(r'pt_pin=(.*?);').findall(cookie)[0]
            pt_pin = unquote_plus(pt_pin)
        except IndexError:
            pt_pin = f'用户{num}'
        print(f'\n******开始【京东账号{num}】{pt_pin} *********\n')
        print(datetime.now())

        token = getToken(cookie, r)
        if token is None:
            if num == 1:
                print(f"⚠️车头获取Token失败,退出本程序！")
                sys.exit()
            print(f"⚠️获取Token失败！⏰等待3s")
            time.sleep(3)
            continue
        time.sleep(0.5)
        activityCookie = getActivity()
        time.sleep(0.5)
        getSystemConfigForNew()
        time.sleep(0.3)
        getSimAct = getSimpleActInfoVo()
        if getSimAct:
            venderId = getSimAct['venderId']
        else:
            venderId = "1000015664"
        time.sleep(0.2)
        getPin = getMyCidPing(num, venderId)
        if getPin is not None:
            nickname = getPin[0]
            secretPin = getPin[1]
            time.sleep(0.5)
            accessLogWithAD(venderId, secretPin)
            time.sleep(0.5)
            userInfo = getUserInfo(secretPin)
            time.sleep(0.8)
            nickname = userInfo[0]
            yunMidImageUrl = userInfo[1]
            pin = userInfo[2]
            actContent = activityContent(pin, yunMidImageUrl, nickname)
            if not actContent:
                if num == 1:
                    print("⚠️无法获取车头邀请码,退出本程序！")
                    sys.exit()
                continue
            hasEnd = actContent['hasEnd']
            if hasEnd:
                print("活动已结束，下次早点来~")
                sys.exit()
            print(f"✅开启【{actContent['activityName']}】活动\n")
            actorUuid = actContent['actorUuid']
            # followShop = actContent['allFollowShop']
            # takeCoupon = actContent['takeCoupon']
            # addSku = actContent['skuAddCart']

            print(f"邀请码->: {actorUuid}")
            print(f"准备助力->: {shareUuid}")
            time.sleep(0.5)
            drawContent(pin)
            time.sleep(0.5)
            initOC = initOpenCard(pin, actorUuid, shareUuid)
            allOpenCard = initOC['allOpenCard']
            isAssist = initOC['openCardAndSendJd']
            assistStatus = initOC['assistStatus']
            openInfo = initOC['openInfo']
            if allOpenCard:
                print("已完成全部开卡任务")
                print(f"助力状态-->{isAssist},{assistStatus}")
                if assistStatus == 0:
                    print("无法助力自己")
                elif assistStatus == 2:
                    print("已经助力过好友")
            else:
                print("现在去开卡")
                unOpenCardLists = [i['venderId'] for i in openInfo if not i['openStatus']]
                for shop in unOpenCardLists:
                    print(f"去开卡 {shop}")
                    venderId = shop
                    venderCardName = getShopOpenCardInfo(cookie, venderId)
                    open_result = bindWithVender(cookie, venderId)
                    if open_result is not None:
                        if "火爆" in open_result or "失败" in open_result or "解绑" in open_result:
                            print(f"⛈{open_result}")
                            print("\t尝试重新入会 第1次")
                            time.sleep(1.5)
                            continue
                        if "加入店铺会员成功" in open_result:
                            print(f"\t🎉🎉{venderCardName} {open_result}")
                    time.sleep(1.5)
                activityContent(pin, yunMidImageUrl, nickname)
                drawContent(pin)
                initOC = initOpenCard(pin, actorUuid, shareUuid)
                allOpenCard = initOC['allOpenCard']
                isAssist = initOC['openCardAndSendJd']
                assistStatus = initOC['assistStatus']
                if allOpenCard:
                    print("已完成全部开卡任务")
                    print(f"助力状态-->{isAssist} {assistStatus}")
                    print("🎉🎉🎉助力成功")
                    inviteSuccNum += 1
                    print(f"\t本次车头已邀请{inviteSuccNum}人")
            time.sleep(0.5)
            getSR = getShareRecord(pin, actorUuid)
            if getSR:
                print(f"🎉🎉🎉已成功邀请{len(getSR)}人")
            if num == 1:
                print(f"后面账号全部助力 {actorUuid}")
                shareUuid = actorUuid
                activityUrl = f"https://lzdz1-isv.isvjcloud.com/m/1000072521/9380848/{activityId}/?shareUuid={shareUuid}&adsource=null"

        time.sleep(3)