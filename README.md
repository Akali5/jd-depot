# jd-depot
自用脚本
内部互助
拉库
```
ql repo https://github.com/Akali5/jd-depot.git "jd_|jx_|jddj_|gua_|getJDCookie|wskey" "activity|backUp" "^jd[^_]|USER|utils|ZooFaker_Necklace|JDJRValidator_|sign_graphics_validate|jddj_cookie|function|ql|magic|JDJR|sendNotify|depend|h5"
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

