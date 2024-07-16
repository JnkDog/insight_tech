# nstat指标
## TcpRetransSegs
TcpExtTCPSynRetrans这个重传的情况，代表syn报文和synack报文的重传数量。
实测这个指标是算到TcpRetransSegs这个里面的，但是我拿的ebpf指标是没有的，得找一个可以统计到位的。
换句话说可以从TcpRetransSegs - TcpExtTCPSynRetrans指标看下大头是谁
TcpRetransSegs                 
TcpExtTCPLostRetransmit     --- A SACK points out that a retransmission packet is lost again.    
TcpExtTCPFastRetrans        --- The TCP stack wants to retransmit a packet and the congestion control state is not ‘Loss’.   
TcpExtTCPSlowStartRetrans   --- The TCP stack wants to retransmit a packet and the congestion control state is ‘Loss’.   
TcpExtTCPRetransFail   --- 给下面的协议栈发送但是失败了       
TcpExtTCPSynRetrans    --- syn + syn-ack ?  抓包看是这样的


### ref
https://blog.mygraphql.com/zh/notes/low-tec/trace/tcp-connect-syn-trace/
http://arthurchiao.art/blog/tcp-retransmission-may-be-misleading/

