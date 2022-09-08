#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_wxCompleteInfo.py(完善信息有礼)
Author: HarbourJ
Date: 2022/8/8 19:52
TG: https://t.me/HarbourToulu
TgChat: https://t.me/HarbourSailing
cron: 1 1 1 1 1 1
new Env('完善信息有礼');
ActivityEntry: https://cjhy-isv.isvjcloud.com/wx/completeInfoActivity/view/activity?activityId=f3325e3375a14866xxxxxxxxxxxx&venderId=1000086
               变量 export jd_wxCompleteInfoId="f3325e3375a14866xxxxxxxxxxxx&1000086192"(活动id&venderId)
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

from jd_sign import *
try:
    from jdCookie import get_cookies
    getCk = get_cookies()
except:
    print("请先下载依赖脚本，\n下载链接: https://raw.githubusercontent.com/HarbourJ/HarbourToulu/main/jdCookie.py")
    sys.exit(3)
redis_url = os.environ.get("redis_url") if os.environ.get("redis_url") else "172.17.0.1"
redis_pwd = os.environ.get("redis_pwd") if os.environ.get("redis_pwd") else ""
jd_wxCompleteInfoId = os.environ.get("jd_wxCompleteInfoId") if os.environ.get("jd_wxCompleteInfoId") else ""

if not jd_wxCompleteInfoId or "&" not in jd_wxCompleteInfoId:
    print("⚠️未发现有效活动变量jd_wxCompleteInfoId,退出程序!")
    sys.exit()
activityId = jd_wxCompleteInfoId.split('&')[0]
venderId = jd_wxCompleteInfoId.split('&')[1]

activityUrl = f"https://cjhy-isv.isvjcloud.com/wx/completeInfoActivity/view/activity?activityId={activityId}&venderId={venderId}"
print(f"【🛳活动入口】{activityUrl}")

def redis_conn():
    try:
        try:
            import redis
        except Exception as e:
            print(e)
            if "No module" in str(e):
                os.system("pip install redis")
            import redis
        try:
            pool = redis.ConnectionPool(host=redis_url, port=6379, decode_responses=True, socket_connect_timeout=5, password=redis_pwd)
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
        # redis缓存Token 活动域名+pt_pin
        pt_pin = unquote_plus(re.compile(r'pt_pin=(.*?);').findall(ck)[0])
    except:
        # redis缓存Token 活动域名+ck前7位(获取pin失败)
        pt_pin = ck[:8]

    if r is not None:
        Token = r.get(f'{activityUrl.split("https://")[1].split("-")[0]}_{pt_pin}')
        # print("Token过期时间", r.ttl(f'{activityUrl.split("https://")[1].split("-")[0]}_{pt_pin}'))
        if Token is not None:
            # print(f"♻️获取缓存Token->: {Token}")
            print(f"♻️获取缓存Token")
            return Token
        else:
            print("🈳去设置Token缓存")
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
            sign_txt = sign({"url": f"{host}", "id": ""}, 'isvObfuscator')
            # print(sign_txt)
            f = s.post('https://api.m.jd.com/client.action', verify=False, timeout=30)
            if f.status_code != 200:
                print(f.status_code)
                return
            else:
                if "参数异常" in f.text:
                    return
            Token_new = f.json()['token']
            # print(f"Token->: {Token_new}")
            if r.set(f'{activityUrl.split("https://")[1].split("-")[0]}_{pt_pin}', Token_new, ex=1800):
                print("✅Token缓存设置成功")
            else:
                print("❌Token缓存设置失败")
            return Token_new
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
        sign_txt = sign({"url": f"{host}", "id": ""}, 'isvObfuscator')
        # print(sign_txt)
        f = s.post('https://api.m.jd.com/client.action', verify=False, timeout=30)
        if f.status_code != 200:
            print(f.status_code)
            return
        else:
            if "参数异常" in f.text:
                return
        Token = f.json()['token']
        print(f"Token->: {Token}")
        return Token

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
    url = activityUrl
    headers = {
        'Host': 'cjhy-isv.isvjcloud.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': ua,
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        if response.cookies:
            cookies = response.cookies.get_dict()
            set_cookies = [(set_cookie + "=" + cookies[set_cookie]) for set_cookie in cookies]
            set_cookie = ''.join(sorted([(set_cookie + ";") for set_cookie in set_cookies]))
        return set_cookie
    else:
        print(response.status_code)
        print("⚠️疑似ip黑了")
        sys.exit()

def getOpenStatus():
    url = "https://cjhy-isv.isvjcloud.com/assembleConfig/getOpenStatus"
    payload = f'activityId={activityId}'
    headers = {
        'Host': 'cjhy-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://cjhy-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)

def getSystemConfig():
    url = "https://cjhy-isv.isvjcloud.com/wxCommonInfo/getSystemConfig"
    payload = f'activityId={activityId}&activityType='
    headers = {
        'Host': 'cjhy-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://cjhy-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)

def getSimpleActInfoVo():
    url = "https://cjhy-isv.isvjcloud.com/customer/getSimpleActInfoVo"
    payload = f"activityId={activityId}"
    headers = {
        'Host': 'cjhy-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://cjhy-isv.isvjcloud.com',
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

def getMyPing(venderId):
    url = "https://cjhy-isv.isvjcloud.com/customer/getMyPing"
    payload = f"userId={venderId}&token={token}&fromType=APP&riskType=1"
    headers = {
        'Host': 'cjhy-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://cjhy-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        refresh_cookies(response)
        res = response.json()
        if res['result']:
            return res['data']['nickname'], res['data']['secretPin']
        else:
            print(f"⚠️{res['errorMessage']}")
    else:
        print(response.status_code)
        print("⚠️疑似ip黑了")
        sys.exit()

def _selectById(venderId):
    url = "https://cjhy-isv.isvjcloud.com/completeInfoActivity/selectById"
    body = f"activityId={activityId}&venderId={venderId}"
    headers = {
        'Host': 'cjhy-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://cjhy-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=body)
    res = response.json()
    if res['result']:
        saveInfo = ""
        data = res['data']
        chooseName = data['chooseName']
        choosePhone = data['choosePhone']
        chooseBirth = data['chooseBirth']
        chooseWeixin = data['chooseWeixin']
        chooseAddress = data['chooseAddress']
        chooseQQ = data['chooseQQ']
        chooseEmail = data['chooseEmail']
        chooseGender = data['chooseGender']
        chooseProfessional = data['chooseProfessional']
        customJson = data['customJson']
        phone = get_mobile()
        if chooseName == 'y':
            name = quote_plus(f"{random.choice(['A','B','C','D','E','F','G','H'])}贤笙")
            saveInfo += f"name={name}&"
        if choosePhone == 'y':
            saveInfo += f"phone={phone}&"
        if chooseBirth == 'y':
            birthDay = "2000-01-01"
            saveInfo += f"birthDay={birthDay}&"
        if chooseWeixin == 'y':
            weiXin = phone
            saveInfo += f"weiXin={weiXin}&"
        if chooseEmail == 'y':
            email = quote_plus(f"{phone}@163.com")
            saveInfo += f"email={email}&"
        if chooseGender == 'y':
            gender = quote_plus("男")
            saveInfo += f"gender={gender}&"
        if chooseProfessional == 'y':
            professional = "Engineer"
            saveInfo += f"professional={professional}&"
        if chooseQQ == 'y':
            qq = phone
            saveInfo += f"{qq}&"
        if chooseAddress == 'y':
            province = quote_plus("北京市")
            city = quote_plus("东城区")
            address = quote_plus("北京大学城北门")
            saveInfo += f"province={province}&city={city}&address={address}&"
        if customJson != "[]":
            customContent = "%5B%2222%22%5D"
            saveInfo += f"customContent={customContent}&"
        return saveInfo
    else:
        print(res['errorMessage'])

def getOpenCardInfo(venderId, pin, activityType):
    url = "https://cjhy-isv.isvjcloud.com/mc/new/brandCard/common/shopAndBrand/getOpenCardInfo"
    body = f"venderId={venderId}&buyerPin={pin}&activityType={activityType}"
    headers = {
        'Host': 'cjhy-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://cjhy-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=body)
    res = response.json()
    if res['result']:
        return res['data']
    else:
        print(res['errorMessage'])

def getShopInfoVO(venderId):
    url = "https://cjhy-isv.isvjcloud.com/wxActionCommon/getShopInfoVO"
    payload = f"userId={venderId}"
    headers = {
        'Host': 'cjhy-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://cjhy-isv.isvjcloud.com',
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

def accessLog(venderId, pin, activityType):
    url = "https://cjhy-isv.isvjcloud.com/common/accessLog"
    payload = f"venderId={venderId}&code={activityType}&pin={quote_plus(pin)}&activityId={activityId}&pageUrl={quote_plus(activityUrl)}&subType="
    headers = {
        'Host': 'cjhy-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://cjhy-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    requests.request("POST", url, headers=headers, data=payload)

def listDrawContent(activityType):
    url = "https://cjhy-isv.isvjcloud.com/drawContent/listDrawContent"
    body = f"activityId={activityId}&type={activityType}"
    headers = {
        'Host': 'cjhy-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://cjhy-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=body)
    res = response.json()
    if res['result']:
        return res['data']
    else:
        # print(res['errorMessage'])
        if "暂未填写" in res['errorMessage']:
            print("📝现在去完善信息")

def selectById(pin, venderId):
    url = "https://cjhy-isv.isvjcloud.com/wx/completeInfoActivity/selectById"
    body = f"activityId={activityId}&pin={quote_plus(pin)}&venderId={venderId}"
    headers = {
        'Host': 'cjhy-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://cjhy-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=body)
    refresh_cookies(response)
    res = response.json()
    if res['result']:
        return res['data']
    else:
        # print(res['errorMessage'])
        if "暂未填写" in res['errorMessage']:
            print("📝现在去完善会员信息")

def getInfo():
    url = f"https://cjhy-isv.isvjcloud.com/miniProgramShareInfo/getInfo?activityId={activityId}"
    headers = {
        'Host': 'cjhy-isv.isvjcloud.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Accept': 'application/json',
        'User-Agent': ua,
        'Referer': activityUrl,
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': activityCookie,
    }
    requests.request("GET", url, headers=headers)

def get_mobile():
    mobiles = ['130', '131', '132', '133', '134']
    number = str(int(time.time()))[2:]
    mobile = random.choice(mobiles)+number
    return mobile

def save(saveInfo, venderId, pin, drawInfoId):
    url = "https://cjhy-isv.isvjcloud.com/wx/completeInfoActivity/save"
    body = f"{saveInfo}drawInfoId={drawInfoId}&activityId={activityId}&venderId={venderId}&pin={quote_plus(pin)}&vcode=&token={token}&fromType=APP"
    headers = {
        'Host': 'cjhy-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://cjhy-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=body)
    res = response.json()
    if res['result']:
        return res['data']
    else:
        print(res['errorMessage'])


if __name__ == '__main__':
    r = redis_conn()
    try:
        cks = getCk
        if not cks:
            sys.exit()
    except:
        print("未获取到有效COOKIE,退出程序！")
        sys.exit()
    num = 0
    for cookie in cks[:]:
        num += 1
        if num % 9 == 0:
            print("⏰等待5s,休息一下")
            time.sleep(5)
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
            print(f"⚠️获取Token失败！⏰等待2s")
            time.sleep(2)
            continue
        time.sleep(0.2)
        activityCookie = getActivity()
        time.sleep(0.3)
        getOpenStatus()
        time.sleep(0.1)
        getSimAct = getSimpleActInfoVo()
        venderId = getSimAct['venderId']
        activityType = getSimAct['activityType']
        time.sleep(0.2)
        getPin = getMyPing(venderId)
        if getPin:
            nickname = getPin[0]
            secretPin = getPin[1]
            time.sleep(0.2)
            getOC = getOpenCardInfo(venderId, secretPin, activityType)
            time.sleep(0.1)
            if getOC['openedCard']:
                getShopInfo = getShopInfoVO(venderId)
                shopName = getShopInfo['shopName']
                print(f"✅开启{shopName} 店铺完善会员信息有礼")
                accessLog(venderId, secretPin, activityType)
                time.sleep(0.2)
                saveInfo = _selectById(venderId)
                time.sleep(0.2)
                selectBI = selectById(secretPin, venderId)
                if selectBI:
                    print(f"💨{nickname} 已经完善过店铺信息")
                    continue
                else:
                    time.sleep(0.2)
                    listDraw = listDrawContent(activityType)
                    drawInfoId = listDraw[0]['drawInfoId']
                    time.sleep(0.2)
                    getInfo()
                    time.sleep(0.1)
                    sv = save(saveInfo, venderId, secretPin, drawInfoId)
                    if sv:
                        drawInfo = sv['drawInfo']['name']
                        if drawInfo:
                            print(f"🎉🎉🎉{nickname} 成功领取 {drawInfo}")
                        else:
                            print(f"⛈⛈⛈{nickname} 领取完善有礼奖励失败,请重试~")
                    else:
                        print(f"💨{nickname} 已经领过完善有礼奖励~")
            else:
                print(f"⛈{nickname} 非店铺会员无法完善信息！")
                continue
        time.sleep(2.5)