# jd-depot
# 自用脚本，内部互助




拉库
```
ql repo https://github.com/Akali5/jd-depot.git "jd_|jx_|jddj_|gua_|getJDCookie|wskey" "backUp" "^jd[^_]|USER|utils|ZooFaker_Necklace|JDJRValidator_|sign_graphics_validate|jddj_cookie|function|ql|magic|JDJR|sendNotify|depend|h5"
```

国内🐓
```
ql repo https://hub.xn--gzu630h.xn--kpry57d/Akali5/jd-depot.git "jd_|jx_|jddj_|gua_|getJDCookie|wskey" "backUp" "^jd[^_]|USER|utils|ZooFaker_Necklace|JDJRValidator_|sign_graphics_validate|jddj_cookie|function|ql|magic|JDJR|sendNotify|depend|h5"

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
  
  ## 加密脚本清单

<details>
<summary>加密脚本清单，已审查， 不放心可禁用</summary>
<pre><code>
jd_zjd.js (赚京豆，全加密）
jddj_fruit.js（到家果园，全加密）
jd_fans.js （粉丝互动，全加密）
jd_half_redrain.js (半点京豆雨，全加密）
jd_jxmc.js （京喜牧场，算法加密）
jd_cfd.js （京喜财富岛，算法加密）
jd_cfd_loop.js (京喜财富岛捡贝壳，算法加密）
jd_speed_sign.js （极速版签到，算法加密）
jd_speed_signred.js  （极速版红包，算法加密）
开卡系列全部部分或全部加密 
</code></pre>
</details>

