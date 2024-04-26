# flannel组件通信理解
## 大致流程

## 我遇到的问题
在master节点上访问worker节点上的pod 10.10.2.3:80，结果访问异常。
flannel进行vxlan的拆解和封装。但是在eth2口并没有抓到vxlan报文。

## 一步步探究
在eth2口死活没有抓到对应的vxlan报文，最后照着flannel vxlan的封包流程走了一遍。果然发现了异常点。
1. node 上执行 `ip route get 10.10.2.3`，路由走了flannel iface 进入封装
```shell
root@master:/tmp# ip route get 10.10.2.3
10.10.2.3 via 10.10.2.0 dev flannel.1 src 10.10.0.0 uid 0
    cache
```
2. node 上执行 `arp -e | grep 10.10.2.0` 看arp表项，flannel决定要转发给be:1e:10:b1:c3:43 mac地址
```shell
root@master:/tmp# arp | grep 10.10.2.0
10.10.2.0                ether   be:1e:10:b1:c3:43   CM                    flannel.1
```
3. 由于flannel要封装vxlan，那么需要知道对应的mac be:1e:10:b1:c3:43 的地址对应的主机ip 也就是 `bridge fdb show`，看到要送到10.0.3.15这台机子上
```shell
root@master:/tmp# bridge fdb show |grep be:1e:10:b1:c3:43
be:1e:10:b1:c3:43 dev flannel.1 dst 10.0.3.15 self permanent
```

4. 查到了对端的ip 10.0.3.15，那么flannel需要发送vxlan udp 报文这个ip上进行。又得查这个路由表，出问题的点就在这。由于我这台master节点把第二个网卡不知道为什么也配成了这个 10.0.3.15，所以路由表默认走了lo口，导致了异常！！！
```shell
root@master:/tmp# ip route get 10.0.3.15
local 10.0.3.15 dev lo src 10.0.3.15 uid 0
    cache <local>
```

发现最后在flannel出去的路由走了lo口。。。没有预期的走向另一个node。然后看了下各个node的ip，震惊，发现原来重新加入集群的ip不是10网段的而是192网段。 

真是狗血的排查经历。。。。下面得考虑下怎么修这个情况

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


