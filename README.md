# 自用，出事概不负责




拉库
```
ql repo https://github.com/Akali5/jd-depot.git "jd_|jx_|jddj_|gua_|getJDCookie|wskey" "activity|backUp" "^jd[^_]|USER|utils|ZooFaker_Necklace|JDJRValidator_|sign_graphics_validate|jddj_cookie|function|ql|magic|JDJR|sendNotify|depend|h5|jdspider"
```

国内🐓
```
ql repo https://hub.xn--gzu630h.xn--kpry57d/Akali5/jd-depot.git "jd_|jx_|jddj_|gua_|getJDCookie|wskey" "activity|backUp" "^jd[^_]|USER|utils|ZooFaker_Necklace|JDJRValidator_|sign_graphics_validate|jddj_cookie|function|ql|magic|JDJR|sendNotify|depend|h5|jdspider"

```


青龙命令2.10.13版本
```
docker run -dit \
  -v /home/ql/config:/ql/config \
  -v /home/ql/db:/ql/db \
  -v /home/ql/scripts:/ql/scripts \
  -v /home/ql/repo:/ql/repo \
  -v /home/ql/backup:/ql/backup \
  -v /home/ql/log:/ql/log \
  -p 5701:5700 \
  --name qinglong \
  --hostname qinglong \
  --restart unless-stopped \
  whyour/qinglong:2.10.13
```
2.12版本以后
```
docker run -dit \
  -v /home/ql/data:/ql/data \
  -p 5701:5700 \
  --name qinglong \
  --hostname qinglong \
  --restart unless-stopped \
  whyour/qinglong:latest
  ```
  
其他脚本
```
58.js(58同城)
jd_txstockex.js(腾讯自选股-全加密)
telecom.py(电信脚本)
```
  
  
  
  ## 加密脚本清单

<details>
<summary>加密脚本清单，已审查， 不放心可禁用</summary>
<pre><code>
jd_fans.js (粉丝互动，全加密)
jd_jxmc.js (京喜牧场，算法加密)
jd_cfd.js (京喜财富岛，算法加密)
jd_cfd_loop.js (京喜财富岛捡贝壳，算法加密)
jd_speed_sign.js (极速版签到，算法加密)
jd_speed_signred.js  (极速版红包，算法加密)
jd_19E_help.js (热爱奇旅互助版-部分加密)
jd_game.js (LZ店铺通用游戏任务-加密)
jd_speed_redpocke.js (京东极速版领红包-加密)
jd_wxSignRed.js(微信签到红包-加密)
jd_cjzdgf.js(CJ组队瓜分京豆-加密)
jd_zdjr.js(LZ组队瓜分京豆-加密)
jd_js_sign.js(极速版签到提现-加密)
jd_drawCenter.js(LZ刮刮乐抽奖通用活动-加密)
jd_jrsign.js(金融签到-加密)
jd_dailysign.js(京东日常签到-加密)
jd_jx_sign.js(京喜双签-加密)
jd_fcwb_help.js(发财挖宝助力-加密)
jd_wxFansInterActionActivity.js(粉丝互动通用活动-加密)
jd_wxUnPackingActivity.js(LZ让福袋飞通用活动)
jd_wxCartKoi.js (购物车锦鲤通用活动)
jd_wxCollectCard.js(集卡抽奖通用活动)
jd_wxCollectionActivity.js(取关商品)
jd_wxSecond.js (读秒拼手速)
jx_one2shopping.js(京喜一元兑好礼)
jx_sign_xd.js(京喜签到-喜豆)
jd_card.js (店铺开卡)
jd_carplay.js(头文字j)
jd_mf_new.js(京东魔方-全加密)
jd_txstockex.js(腾讯自选股-全加密)
jd_washbeans.js(临时京豆续命-加密)

开卡系列全部部分或全部加密 
</code></pre>
</details>

