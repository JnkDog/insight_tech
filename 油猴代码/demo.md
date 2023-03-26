```js
// ==UserScript==
// @name         截取 JSON 响应并展示在浮窗中
// @namespace    http://tampermonkey
// @version      1
// @description  截取 JSON 响应并展示在浮窗中
// @match        http://*/*
// @match        https://*/*
// @grant        GM_xmlhttpRequest
// ==/UserScript==

(function() {
  'use strict';

  GM_xmlhttpRequest({
    method: "GET",
    url: "http://example.com/data.json",
    onload: function(response) {
      // 获取响应数据
      var data = JSON.parse(response.responseText);

      // 创建浮窗
      var div = document.createElement("div");
      div.style.position = "fixed";
      div.style.top = "20px";
      div.style.right = "20px";
      div.style.zIndex = 9999;
      div.style.background = "white";
      div.style.padding = "10px";
      div.style.border = "1px solid black";

      // 将响应数据展示在浮窗中
      var pre = document.createElement("pre");
      pre.textContent = JSON.stringify(data, null, 2);
      div.appendChild(pre);
      document.body.appendChild(div);
    }
  });
})();
```

```js
// ==UserScript==
// @name         捕获网页发送的 JSON 数据
// @namespace    http://tampermonkey
// @version      1
// @description  捕获网页发送的 JSON 数据
// @match        http://*/*
// @match        https://*/*
// @grant        GM_xmlhttpRequest
// ==/UserScript==

(function() {
  'use strict';

  // 监听所有的 HTTP 请求
  window.addEventListener("XMLHttpRequest", function(event) {
    // 检查请求的 URL 是否是 JSON 数据的地址
    if (event.url === "http://example.com/data.json") {
      // 检查请求的数据是否是 JSON 格式
      try {
        var data = JSON.parse(event.data);
        // 在这里处理捕获到的 JSON 数据
        console.log("捕获到 JSON 数据：", data);
      } catch (error) {
        // 忽略不是 JSON 格式的请求
      }
    }
  });
})();
```

```js
// 定义要处理的 URL 前缀
const urlPrefix = "https://example.com/api";

// 注册 XMLHttpRequest 事件监听器
window.addEventListener("XMLHttpRequest", function(event) {
  // 获取当前请求的 URL
  const url = event.target.responseURL;

  // 判断当前请求的 URL 是否符合要求
  if (url && url.startsWith(urlPrefix)) {
    // 处理符合要求的请求
    console.log("Processing XMLHttpRequest for URL:", url);
    // ...
  } else {
    // 跳过不符合要求的请求
    console.log("Skipping XMLHttpRequest for URL:", url);
  }
});
```
