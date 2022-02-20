# TCP理解
## TCP头部
给出比较重要的几个部分
* 序列号 
* 确认应答号
* ACK
* RST
* SYN
* FIN

## 三次握手
终极目的，确保双方的接发送能力
* 三次握⼿才可以阻⽌重复历史连接的初始化（主要原因）
* 三次握⼿才可以同步双⽅的初始序列号
* 三次握⼿才可以避免资源浪费

用Wireshark演示抓包一个HTTP链接。
1. 先用python启动一个http服务器 （python -m http.server ）
2. tcpdump监听 （tcpdump -i any tcp and host 127.0.0.1 and port 8000 -w http.pcap）
3. 利用wireshark 解析http.pcap

握手1
![[握手1.png]]
客户端随机生成一个序列号，flags为SYN

