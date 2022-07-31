/*
活动名称：大牌集合通用任务
环境变量：DAPAINEW // 活动ID

抽奖的奖池是单独的，而邀请和任务类共用同一个奖池

作者：===32===
内部脚本，不得外泄！

*/

const $ = new Env("大牌集合通用任务");
const jdCookieNode = $.isNode() ? require('./jdCookie.js') : '';
const notify = $.isNode() ? require('./sendNotify') : '';

//IOS等用户直接用NobyDa的jd cookie
let cookiesArr = [],
  cookie = '';
if ($.isNode()) {
  Object.keys(jdCookieNode).forEach((item) => {
    cookiesArr