#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_redisTest.py(本地redis连接测试)
Author: HarbourJ
Date: 2023/2/8 21:00
TG: https://t.me/HarbourToulu
cron: 1 1 1 1 1 *
new Env('本地redis连接测试');
Description: 测试redis是否正常连接，运行脚本前请先设置redis_url、redis_port、redis_pwd这三个变量（可选）
"""

import os
from sendNotify import *
from functools import partial
print = partial(print, flush=True)
try:
    import redis
except ImportError as e:
    print(e)
    if "No module" in str(e):
        print("请先安装python依赖redis")
        send("🗣redis连接通知", "请先安装python依赖redis")

redis_url = os.environ.get("redis_url") if os.environ.get("redis_url") else "172.17.0.1"
redis_port = os.environ.get("redis_port") if os.environ.get("redis_port") else "6379"
redis_pwd = os.environ.get("redis_pwd") if os.environ.get("redis_pwd") else ""


def redis_conn():
    try:
        try:
            pool = redis.ConnectionPool(host=redis_url, port=redis_port, decode_responses=True, socket_connect_timeout=30, password=redis_pwd)
            r = redis.Redis(connection_pool=pool)
            r.get('conn_test')
            print('✅redis连接成功\n')
            send(title, "✅redis连接成功")
        except:
            print("⚠️redis连接异常\n")
            send(title, "⚠️redis连接异常")
    except:
        print("⚠️redis连接异常\n")
        send(title, "⚠️redis连接异常")


if __name__ == '__main__':
    print("开始运行redisTest检测\n")
    title = '🗣redis连接通知'
    redis_conn()
