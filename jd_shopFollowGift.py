#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_shopFollowGift.py(关注有礼-JK)
Author: tttccz,HarbourJ
Date: 2022/8/8 19:52
TG: https://t.me/HarbourToulu
TgChat: https://t.me/HarbourChat
cron: 1 1 1 1 1 1
new Env('关注有礼-JK');
ActivityEntry: https://shop.m.jd.com/?shopId=12342136
               变量 export jd_shopFollowGiftId="店铺shopId1&店铺shopId2" #变量为店铺🆔,建议一次仅运行2-3个shopId
                   export jd_shopFollowGiftRunNums=xx #变量为需要运行账号数量,默认跑前10个账号
"""

import time, requests, sys, re, os, json, random
from datetime import datetime
from urllib.parse import quote_plus, unquote_plus
from sendNotify import *
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
redis_pwd = os.environ.get("redis_pwd") if os.environ.get("redis_pwd") else ""
jd_shopFollowGiftId = os.environ.get("jd_shopFollowGiftId") if os.environ.get("jd_shopFollowGiftId") else ""
runNums = os.environ.get("jd_shopFollowGiftRunNums") if os.environ.get("jd_shopFollowGiftRunNums") else 10

if not jd_shopFollowGiftId:
    print("⚠️未发现有效活动变量jd_shopFollowGiftId,退出程序!")
    sys.exit()

runNums = int(runNums)
if runNums == 10:
    print('🤖本次关注默认跑前10个账号,设置自定义变量:export jd_shopFollowGiftRunNums="需要运行加购的ck数量"')
else:
    print(f'🤖本次运行前{runNums}个账号')

def getJdTime():
    jdTime = int(round(time.time() * 1000))
    return jdTime

def randomString(e, flag=False):
    t = "0123456789abcdef"
    if flag: t = t.upper()
    n = [random.choice(t) for _ in range(e)]
    return ''.join(n)

def check(ua, ck):
    try:
        url = 'https://me-api.jd.com/user_new/info/GetJDUserInfoUnion'
        header = {
            "Host": "me-api.jd.com",
            "Accept": "*/*",
            "Connection": "keep-alive",
            "Cookie": ck,
            "User-Agent": ua,
            "Accept-Language": "zh-cn",
            "Referer": "https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&",
            "Accept-Encoding": "gzip, deflate",
        }
        result = requests.get(url=url, headers=header, timeout=None).text
        codestate = json.loads(result)
        if codestate['retcode'] == '1001':
            return {'code': 1001, 'data': '⚠️当前ck已失效，请检查'}
        elif codestate['retcode'] == '0' and 'userInfo' in codestate['data']:
            nickName = codestate['data']['userInfo']['baseInfo']['nickname']
            return {'code': 200, 'name': nickName, 'ck': ck}
    except Exception as e:
        return {'code': 0, 'data': e}

def get_venderId(index, shopId):
    url = f'https://api.m.jd.com/client.action?functionId=whx_getMShopOutlineInfo&body=%7B%22shopId%22%3A%22{shopId}%22%2C%22source%22%3A%22m-shop%22%7D&appid=shop_view&clientVersion=11.0.0&client=wh5'
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'origin': 'https://shop.m.jd.com',
        'referer': 'https://shop.m.jd.com/',
        'user-agent': ua,
        'cookie': cookie
    }
    response = requests.request("GET", url, headers=headers)
    res = response.json()
    if res['success']:
        venderId = res['data']['shopInfo']['venderId']
        shopName = res['data']['shopInfo']['shopName'] if res['data']['shopInfo']['shopName'] else ""
        print(f'【店铺{index}】{shopName}')
        return shopName, venderId
    else:
        print(f'获取店铺信息失败！')
        return None, None

def getShopHomeActivityInfo(shopId, venderId, ck):
    global MSG
    body = {
        "shopId": shopId,
        "source": "app-shop",
        "latWs": "0",
        "lngWs": "0",
        "displayWidth": "1170.000000",
        "sourceRpc": "shop_app_home_home",
        "lng": "0",
        "lat": "0",
        "venderId": venderId
    }
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
    sign(body, 'getShopHomeActivityInfo')
    f = s.post('https://api.m.jd.com/client.action', verify=False, timeout=30)
    if f.status_code != 200:
        print(f.status_code)
        MSG += f" ⛈{f.status_code}"
        return
    else:
        if "参数异常" in f.text:
            return
    res = f.json()
    if res['isSuccess'] and res["code"] == '0':
        if res["result"]["followed"]:
            print("\t🤖已关注过店铺")
            return
        else:
            if 'shopGifts' in str(res):
                shopGifts = res['result']['shopGifts']
                for shopGift in shopGifts:
                    redWord = shopGift['redWord']
                    rearWord = shopGift['rearWord']
                    print(f'\t🎁关注有礼奖励：{redWord}{rearWord}')
                    if rearWord.find('京豆') > -1:
                        return res['result']['activityId']
            else:
                print('\t⛈未发现关注有礼活动')
                return
    else:
        print('⛈获取活动信息失败！')
        return

def drawShopGift(shopId, venderId, ck, activityId):
    body = {
        "shopId": shopId,
        "source": "app-shop",
        "latWs": "0",
        "lngWs": "0",
        "displayWidth": "1170.000000",
        "sourceRpc": "shop_app_home_home",
        "lng": "0",
        "lat": "0",
        "venderId": venderId,
        "activityId": activityId
    }
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
    sign_txt = sign(body, 'drawShopGift')
    f = s.post('https://api.m.jd.com/client.action', verify=False, timeout=30)
    if f.status_code != 200:
        print(f.status_code)
        return
    else:
        if "参数异常" in f.text:
            return
    return f.json()

if __name__ == '__main__':
    global MSG
    MSG = ''
    title = "🗣消息提醒：关注有礼-JK"
    shopIds = jd_shopFollowGiftId.split('&')
    print(f"✅成功获取{len(shopIds)}个jd_shopFollowGift🆔变量")
    try:
        cks = getCk
        if not cks:
            sys.exit()
    except:
        print("未获取到有效COOKIE,退出程序！")
        sys.exit()
    num = 0
    for cookie in cks[:runNums]:
        num += 1
        if num % 10 == 0:
            print("⏰等待3s,休息一下")
            time.sleep(3)
        global ua
        ua = userAgent()
        try:
            pt_pin = re.compile(r'pt_pin=(.*?);').findall(cookie)[0]
            pt_pin = unquote_plus(pt_pin)
        except IndexError:
            pt_pin = f'用户{num}'
        print(f'\n******开始【京东账号{num}】{pt_pin} *********\n')
        MSG += f"【账号{num}】{pt_pin}"
        print(datetime.now())

        result = check(ua, cookie)
        if result['code'] != 200:
            print(f"‼️{result['data']}")
            MSG += f" ⚠️当前ck已失效\n"
            time.sleep(1)
            continue

        MSG1 = ''
        for index, shopId in enumerate(shopIds, 1):
            shopInfo = get_venderId(index, shopId)
            shopName = shopInfo[0]
            venderId = shopInfo[1]
            if venderId:
                activityId = getShopHomeActivityInfo(shopId, venderId, cookie)
                time.sleep(0.5)
                if activityId:
                    drawResult = drawShopGift(shopId, venderId, cookie, activityId)
                    if drawResult:
                        if drawResult['isSuccess'] and drawResult['code'] == '0':
                            drawResultDesc = drawResult['result']['followDesc']
                            if '关注成功' in str(drawResultDesc):
                                drawResultTotal = ''
                                drawResultPrizes = drawResult['result']['alreadyReceivedGifts']
                                for drawResultPrize in drawResultPrizes:
                                    drawResultTotal += str(drawResultPrize['redWord']) + drawResultPrize['rearWord'] + ''
                                print(f"\t🎉🎉🎉成功领取 {drawResultTotal}")
                                MSG1 += f"\n    🎉【{shopName}】{drawResultTotal}"
                            else:
                                print('⛈奖励领取失败1！')
                                MSG1 += f"\n    ⛈【{shopName}】奖励领取失败1！"
                        else:
                            print('⛈奖励领取失败2！')
                            MSG1 += f"\n    ⛈【{shopName}】奖励领取失败2！"
                    else:
                        print('⛈奖励领取失败3！')
                        MSG1 += f"\n    ⛈【{shopName}】奖励领取失败3！"
            time.sleep(0.5)

        if not MSG1:
            MSG += " 💨💨💨\n"
        else:
            MSG += MSG1 + "\n"
        time.sleep(1)

    MSG = f"⏰{str(datetime.now())[:19]}\n" + MSG
    send(title, MSG)