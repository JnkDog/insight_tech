1. 调用close函数，但是socket中仍有数据，reset报文中带ack标志位 ==> 单实例
2. fin_wait2状态调用close，且
3. 

## 分类
1. tcp_v4_send_reset
1.1 套接字不存在

1.2 握手阶段不合法的ack
如果找到了监听套接口，并且其状态为TCP_NEW_SYN_RECV，而且成功创建了子套接口，但是在子套接口处理函数tcp_child_process中返回错误，也将发送reset报文。错误情况稍后在函数tcp_rcv_state_process中介绍。

比较符合这样的情况

1.3 需要进一步对空闲超时的状态进行分析确定符合理论分析的结果


2. tcp_send_active_reset
TCP reset包必须要有ACK以及RST标志


## ref
https://blog.csdn.net/sinat_20184565/article/details/110962869