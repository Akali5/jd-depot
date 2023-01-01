#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_poolCaptainAJ.py(安佳组队瓜分)
Author: HarbourJ
Date: 2022/8/1 22:37
TG: https://t.me/HarbourToulu
cron: 1 1 1 1 1 1
new Env('安佳组队瓜分');
活动入口: https://lzkjdz-isv.isvjcloud.com/pool/captain/8001978?activityId=36cc0f18d3eb4e178f2a3632f7af1c14
"""


import time, requests, sys, re, os, json, random
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
from functools import partial
print = partial(print, flush=True)

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
jd_poolCaptainNums = os.environ.get("jd_poolCaptainNums") if os.environ.get("jd_poolCaptainNums") else "80"

activityId = "36cc0f18d3eb4e178f2a3632f7af1c14"
shopId = "1000014486"
print(f"【🛳活动入口】https://lzkjdz-isv.isvjcloud.com/pool/captain/8451632?activityId={activityId}")

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
            # print(f"redis get error: {str(e)}")
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
                # print(f"redis set error: {str(e)}")
                print(f"✅获取实时Token")
            return Token_new
    except Exception as e:
        print(f"Token error: {str(e)}")
        return

def getJdTime():
    url = "http://api.m.jd.com/client.action?functionId=queryMaterialProducts&client=wh5"
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'api.m.jd.com',
        'Proxy-Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    try:
        response = requests.request("GET", url, headers=headers, timeout=2)
        if response.status_code == 200:
            res = response.json()
            jdTime = res['currentTime2']
    except:
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
        activityCookie = ''.join(
            sorted([(set_cookie + ";") for set_cookie in list(set(activityCookieMid + set_cookie))]))
        # print("刷新cookie", activityCookie)

def getActivity():
    url = activityUrl
    headers = {
        'Host': 'lzkjdz-isv.isvjcloud.com',
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
        print(response.status_code)
        print("⚠️疑似ip黑了")
        sys.exit()

def getSystemConfigForNew():
    url = "https://lzkjdz-isv.isvjcloud.com/wxCommonInfo/getSystemConfigForNew"
    payload = f'activityId={activityId}&activityType=46'
    headers = {
        'Host': 'lzkjdz-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzkjdz-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)

def getSimpleActInfoVo():
    url = "https://lzkjdz-isv.isvjcloud.com/customer/getSimpleActInfoVo"
    payload = f"activityId={activityId}"
    headers = {
        'Host': 'lzkjdz-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzkjdz-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)

def getInfo():
    url = f"https://lzkjdz-isv.isvjcloud.com/miniProgramShareInfo/getInfo?activityId={activityId}"
    headers = {
        'Host': 'lzkjdz-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzkjdz-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    requests.request("GET", url, headers=headers)

def getMyPing(index):
    url = "https://lzkjdz-isv.isvjcloud.com/customer/getMyPing"
    payload = f"userId={shopId}&token={token}&fromType=APP"
    headers = {
        'Host': 'lzkjdz-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzkjdz-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)
    res = response.json()
    if res['result']:
        return res['data']['nickname'], res['data']['secretPin']
    else:
        print(f"⚠️{res['errorMessage']}")
        if index == 1:
            print(f"\t⛈车头黑,退出本程序！")
            sys.exit()

def accessLogWithAD(pin):
    url = "https://lzkjdz-isv.isvjcloud.com/common/accessLogWithAD"
    payload = f"venderId={shopId}&code=46&pin={quote_plus(pin)}&activityId={activityId}&pageUrl={quote_plus(activityUrl)}&shopid={shopId}&subType=app&adSource="
    headers = {
        'Host': 'lzkjdz-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzkjdz-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)

def getSystime():
    url = "https://lzkjdz-isv.isvjcloud.com/common/getSystime"
    headers = {
        'Host': 'lzkjdz-isv.isvjcloud.com',
        'Origin': 'https://lzkjdz-isv.isvjcloud.com',
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

def activityContent(pin):
    url = "https://lzkjdz-isv.isvjcloud.com/pool/activityContent"
    payload = f"activityId={activityId}&pin={quote_plus(pin)}&signUuid={signUuid}"
    headers = {
        'Host': 'lzkjdz-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzkjdz-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    # print('activityContent', response.text)
    # refresh_cookies(response)
    res = response.json()
    if res['result']:
        return res['data']
    else:
        print(res['errorMessage'])
        if "活动已结束" in res['errorMessage']:
            sys.exit()

def getUserInfo(pin):
    url = "https://lzkjdz-isv.isvjcloud.com/wxActionCommon/getUserInfo"
    payload = f"pin={quote_plus(pin)}"
    headers = {
        'Host': 'lzkjdz-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzkjdz-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)
    res = response.json()
    # print('getUserInfo', res)
    if res['result']:
        return res['data']['nickname'], res['data']['yunMidImageUrl'], res['data']['pin']
    else:
        print(res['errorMessage'])

def saveCandidate(pin, pinImg, nickname):
    try:
        yunMidImageUrl = quote_plus(pinImg)
    except:
        yunMidImageUrl = quote_plus(
            "https://img10.360buyimg.com/imgzone/jfs/t1/21383/2/6633/3879/5c5138d8E0967ccf2/91da57c5e2166005.jpg")
    url = "https://lzkjdz-isv.isvjcloud.com/pool/saveCandidate"
    payload = f"activityId={activityId}&signUuid={signUuid}&pin={quote_plus(pin)}&pinImg={yunMidImageUrl}&jdNick={quote_plus(nickname)}"
    headers = {
        'Host': 'lzkjdz-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzkjdz-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)

def saveCaptain(pin, pinImg, nickname):
    url = "https://lzkjdz-isv.isvjcloud.com/pool/saveCaptain"
    try:
        yunMidImageUrl = quote_plus(pinImg)
    except:
        yunMidImageUrl = quote_plus(
            "https://img10.360buyimg.com/imgzone/jfs/t1/21383/2/6633/3879/5c5138d8E0967ccf2/91da57c5e2166005.jpg")
    payload = f"activityId={activityId}&pin={quote_plus(pin)}&pinImg={yunMidImageUrl}&jdNick={quote_plus(nickname)}"
    headers = {
        'Host': 'lzkjdz-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzkjdz-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)
    res = response.json()
    if res['result']:
        return res['data']['signUuid']
    else:
        print(res['errorMessage'])

def updateCaptain(uuid):
    url = "https://lzkjdz-isv.isvjcloud.com/pool/updateCaptain"
    payload = f"uuid={uuid}"
    headers = {
        'Host': 'lzkjdz-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzkjdz-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    res = response.json()
    if res['result']:
        return res['data']['captainStatus']
    else:
        print(res['errorMessage'])

def getShopOpenCardInfo(cookie):
    shopcard_url = f"https://shopmember.m.jd.com/shopcard/?venderId={shopId}&channel=7014&returnUrl={quote_plus(activityUrl)}"
    body = {"venderId": str(shopId), "channel": "7014"}
    url = f'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=getShopOpenCardInfo&body={json.dumps(body)}&client=H5&clientVersion=9.2.0&uuid=88888'
    headers = {
        'Host': 'api.m.jd.com',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'User-Agent': ua,
        'Accept-Language': 'zh-cn',
        'Referer': shopcard_url,
        'Accept-Encoding': 'gzip, deflate'
    }
    response = requests.get(url=url, headers=headers, timeout=5).text
    return json.loads(response)

def bindWithVender(cookie):
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
                'venderId': shopId,
                'shopId': shopId,
                'bindByVerifyCodeFlag': 1
            }, separators=(',', ':'))
        }
        res = s.post('https://api.m.jd.com/', verify=False, timeout=30).json()
        if res['success']:
            return res['message']
    except Exception as e:
        print(e)


if __name__ == '__main__':
    r = redis_conn()
    try:
        cks = getCk
        if not cks:
            sys.exit()
    except:
        print("未获取到有效COOKIE,退出程序！")
        sys.exit()
    global signUuid, inviteSuccNum, activityUrl, firstCk
    inviteSuccNum = 0
    try:
        inviterUuid = remote_redis(f"lzkjdz_{activityId}", 1)
        if not inviterUuid:
            inviterUuid = "07ba2355d1c445c49d4f49f23aece5ef"
    except:
        inviterUuid = "07ba2355d1c445c49d4f49f23aece5ef"
    signUuid = inviterUuid
    activityUrl = f"https://lzkjdz-isv.isvjcloud.com/pool/captain/8451632?activityId={activityId}&signUuid={inviterUuid}&sid=&un_area=12_1212_1212_22222"

    updateCaptainReward = False
    num = 0
    for cookie in cks:
        num += 1
        if num == 1:
            firstCk = cookie
        if num % 10 == 0:
            print("⏰等待3s,休息一下")
            time.sleep(5)
        global ua, activityCookie, token
        ua = userAgent()
        try:
            pt_pin = re.compile(r'pt_pin=(.*?);').findall(cookie)[0]
            pt_pin = unquote_plus(pt_pin)
        except IndexError:
            pt_pin = re.compile(r'pin=(.*?);').findall(cookie)[0]
            pt_pin = unquote_plus(pt_pin)
        print(f'\n******开始【京东账号{num}】{pt_pin} *********\n')

        try:
            print(datetime.now())
            token = None
            activityCookie = ''
            token = getToken(cookie, r)
            if token is None:
                if num == 1:
                    print(f"⚠️车头获取Token失败,退出本程序！")
                    sys.exit()
                print(f"⚠️获取Token失败！⏰等待3s")
                time.sleep(3)
                continue
            time.sleep(0.3)
            activityCookie = getActivity()
            time.sleep(0.2)
            getSystemConfigForNew()
            time.sleep(0.3)
            getSimpleActInfoVo()
            time.sleep(0.3)
            getInfo()
            time.sleep(0.3)
            getPin = getMyPing(num)
            if getPin is not None:
                nickname = getPin[0]
                secretPin = getPin[1]
                time.sleep(0.3)
                accessLogWithAD(secretPin)
                time.sleep(0.3)
                actContent = activityContent(secretPin)
                if num == 1:
                    if not actContent['successRetList']:
                        print("🛳CK1已邀请0人")
                    else:
                        memberLists = actContent['successRetList']
                        groupNums = len(memberLists)
                        for memberList in memberLists:
                            inviteSuccNum += len(memberList['memberList']) - 1
                        print(f"🛳CK1已邀请{groupNums}组,共计{inviteSuccNum}人")
                        if inviteSuccNum >= int(jd_poolCaptainNums):
                            print(f"🎉CK1已达到最大邀请人数,现在去瓜分")
                            updateCaptainReward = True
                            time.sleep(0.5)
                            getUserInfo(secretPin)
                            time.sleep(0.5)
                            count = 0
                            success_count = 0
                            for memberList in memberLists:
                                sendStatus = memberList['sendStatus']
                                canSend = memberList['canSend']
                                if canSend:
                                    if not sendStatus:
                                        captainId = memberList['memberList'][0]['captainId']
                                        count += 1
                                        print(f"🎁开始瓜分第{count}队")
                                        if updateCaptain(captainId):
                                            success_count += 1
                                            print(f"\t🎉成功瓜分第{count}队,获得50豆!")
                                        else:
                                            print(f"\t❌瓜分第{count}队失败!")
                                        time.sleep(2)
                            if count > 0:
                                print(f"🎉🎉🎉瓜分完毕,本次共获得{success_count * 50}豆")
                            else:
                                print("😆已全部瓜分完毕,本次无可瓜分队伍！")
                            sys.exit()
                    print(f"CK1准备助力🛳")
                time.sleep(0.3)
                userInfo = getUserInfo(secretPin)
                nickname = userInfo[0]
                yunMidImageUrl = userInfo[1]
                pin = userInfo[2]
                if actContent['canJoin']:
                    print("🎉加入队伍成功,请等待队长瓜分京豆,现在去开卡助力")
                    saveCandidate(pin, yunMidImageUrl, nickname)
                    time.sleep(0.5)
                    if not actContent['openCard']:
                        open_result = bindWithVender(cookie)
                        if open_result is not None:
                            if "火爆" in open_result or "失败" in open_result or "解绑" in open_result:
                                print(f"⛈{open_result} ️助力失败!")
                                if num == 1:
                                    print("‼️车头疑似黑号,退出程序！")
                                    sys.exit()
                                time.sleep(3)
                                continue
                            if "加入店铺会员成功" in open_result:
                                if num == 1:
                                    print(f"CK1成功助力🛳")
                                else:
                                    inviteSuccNum += 1
                                    print(f"🛳🛳🛳助力成功,本次已邀请{inviteSuccNum}人")
                                    if inviteSuccNum >= int(jd_poolCaptainNums):
                                        updateCaptainReward = True
                        time.sleep(1)
                        actContent1 = activityContent(pin)
                        if num == 1:
                            time.sleep(0.5)
                            if actContent1['canCreate']:
                                print("✅CK1成功创建队伍")
                                time.sleep(0.5)
                                signUuid1 = saveCaptain(pin, yunMidImageUrl, nickname)
                            else:
                                print("‼️CK1无法创建队伍,退出程序！")
                                sys.exit()
                else:
                    if not actContent['openCard']:
                        print("⛈已加入其他队伍,但未开卡！")
                        open_result = bindWithVender(cookie)
                        if open_result is not None:
                            if "火爆" in open_result or "失败" in open_result or "解绑" in open_result:
                                print(f"⛈{open_result} ️助力失败！")
                                if num == 1:
                                    print("‼️车头疑似黑号,退出程序！")
                                    sys.exit()
                                time.sleep(1.5)
                                continue
                            if "加入店铺会员成功" in open_result:
                                print("🤖开卡成功,但助力失败！")
                        time.sleep(1)
                        actContent1 = activityContent(pin)
                        time.sleep(0.5)
                        if num == 1:
                            if actContent1['canCreate']:
                                print("✅CK1成功创建队伍")
                                time.sleep(0.5)
                                signUuid1 = saveCaptain(pin, yunMidImageUrl, nickname)
                            else:
                                print("‼️CK1无法创建队伍,退出程序！")
                                sys.exit()
                    else:
                        if num == 1:
                            print("⛈CK1已入会,无法完成助力")
                            if actContent['canCreate']:
                                signUuid1 = saveCaptain(pin, yunMidImageUrl, nickname)
                            else:
                                signUuid1 = actContent['signUuid']
                        else:
                            print("⛈已入会,无法完成助力")

            if num == len(cks) and inviteSuccNum >= 4:
                updateCaptainReward = True
            if updateCaptainReward:
                print(f"🎉CK1已达到最大邀请人数,现在去瓜分")
                ua = userAgent()
                token = getToken(firstCk, r)
                time.sleep(0.3)
                activityCookie = getActivity()
                time.sleep(0.2)
                getSystemConfigForNew()
                time.sleep(0.3)
                getSimpleActInfoVo()
                time.sleep(0.3)
                getInfo()
                time.sleep(0.3)
                getPin = getMyPing(num)
                secretPin = getPin[1]
                time.sleep(0.3)
                accessLogWithAD(secretPin)
                time.sleep(0.3)
                actContent = activityContent(secretPin)
                time.sleep(0.3)
                memberLists = actContent['successRetList']
                time.sleep(0.3)
                getUserInfo(secretPin)
                time.sleep(0.3)
                count = 0
                success_count = 0
                for memberList in memberLists:
                    sendStatus = memberList['sendStatus']
                    canSend = memberList['canSend']
                    if canSend:
                        if not sendStatus:
                            captainId = memberList['memberList'][0]['captainId']
                            count += 1
                            print(f"🎁开始瓜分第{count}队")
                            if updateCaptain(captainId):
                                success_count += 1
                                print(f"\t🎉成功瓜分第{count}队,获得50豆!")
                            else:
                                print(f"\t❌瓜分第{count}队失败!")
                            time.sleep(2)
                if count > 0:
                    print(f"🎉🎉🎉瓜分完毕,本次共获得{success_count * 50}豆")
                else:
                    print("😆已全部瓜分完毕,本次无可瓜分队伍！")
                sys.exit()

            if num == 1:
                signUuid = signUuid1
                activityUrl = f"https://lzkjdz-isv.isvjcloud.com/pool/captain/8451632?activityId={activityId}&signUuid={signUuid}&sid=&un_area=12_1212_1212_22222"
                print(f"🤖后面的号全部助力CK1-->{signUuid}")
        except Exception as e:
            print(str(e))
        time.sleep(3)