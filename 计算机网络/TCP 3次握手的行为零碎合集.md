# TCP 3次握手的行为零碎合集
假定第一个syn包到了服务端，服务端可能有什么样的行为？
1. 接收到消息，但是不回任何消息，熟视无睹。
2. 明确回复拒绝，这里会有很多不同的策略，需要注意，后面再分析。

第一种情况，因为服务端做了“静默丢包”，也就是虽然收到了 SYN，但是它直接丢弃
了，也不给客户端回复任何消息。这也导致了一个问题，就是客户端无法分清楚这个 SYN
到底是下面哪种情况：
1. 在网络上丢失了，服务端收不到，自然不会有回复；
2. 对端收到了但没回，就是刚才说的“静默丢包”；
3. 对端收到了也回了，但这个回包在网络中丢了。

在对端收到了但没回，就是刚才说的“静默丢包”的情况下，设置iptables规则 
```shell
iptables -I input -p tcp --dport 80 -j DROP
```
这个时候到80端口的tcp包都会被drop掉了。但是tcp包被drop掉，对于tcp协议会尝试重试来恢复连接。在 Linux 中，这个设置是由内核参数 net.ipv4.tcp_syn_retries 控制的，默认值为 6。man tcp可以来看参数。

那么设置另一个iptables的规则：
```shell
Iptables -I INPUT -p tcp --dport 80 -j REJECT
```
这个时候再去telnet后，就不会卡那么久，会直接退出。会显示一些输出：
```shell
xxx Connection refused
xxx Unable to connect to remote host
```
但是这个造成refused出现的原因是不一样的，例如上面的iptables的规则，有可能真实的规则是带–reject-with icmp-port-unreachable，也就是说确实用 ICMP 消息做了回复。但是如果指定 –reject-with tcp-reset 那么服务端就会回RST包的tcp包。

# TCP option字段
TCP扩展字段中有个windows scale，它代表tcp的窗口 * 2的多少次方，从而做到窗口的放大。Window Scale 只出现在 TCP 握手里面，这个是“控制面”的信息，说一次让双方明白就够了。而且是客户端服务端都有这个参数才行！！！