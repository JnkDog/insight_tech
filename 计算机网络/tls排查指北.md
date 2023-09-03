# 有用的命令
## openssl
```shell
openssl s_client -tlsextdebug -showcerts -connect 网站:443
```

## 如何解密
环境变量创建。SSLKEYLOGFILE，映射文件 key.log, wireshark在 pre-master-secret log file中写进去就好了

## 证书以及签发机构
```shell
echo | openssl s_client -showcerts -connect zoom.us:443 -servername zoom.us 2> /dev/null | grep -A1 s:
```

## ref
https://www.kawabangga.com/all-posts