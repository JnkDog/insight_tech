# flannel组件通信理解
## 大致流程

## 我遇到的问题
flannel进行vxlan的拆解和封装。但是在eth0口并没有抓到vxlan报文

## 小tips
1. 查看具体网络设备信息：`ip -details link show flannel.1`
```shell
# 看到是vxlan设备，对端端口号是8472
root@master:~/demo# ip -details link show flannel.1
5: flannel.1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UNKNOWN mode DEFAULT group default
    link/ether c2:e1:67:05:ad:32 brd ff:ff:ff:ff:ff:ff promiscuity 0 minmtu 68 maxmtu 65535
    vxlan id 1 local 10.0.3.15 dev enp0s8 srcport 0 0 dstport 8472 nolearning ttl auto ageing 300 udpcsum noudp6zerocsumtx noudp6zerocsumrx addrgenmode eui64 numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535
```



## 参考
https://cloud.tencent.com/developer/article/1819134   