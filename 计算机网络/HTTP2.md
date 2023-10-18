# http2
1. 直观感受HTTP2和 HTTP1.1的区别
https://http2.akamai.com/demo

2. 如果配置的是http2的ngx，不走tls，那么需要加 --http2-prior-knowledge
```shell
curl offers the --http2 command line option to enable use of HTTP/2.

curl offers the --http2-prior-knowledge command line option to enable use of HTTP/2 without HTTP/1.1 Upgrade. (如果升级不支持的情况下)

3. https://imququ.com/post/http2-traffic-in-wireshark.html https 抓

4. nghttp 调试

====

116.63.135.144 ok
114.217.16.130 not ok