# wireshark字段说明
一些wireshark的字段说明，提高定位速度。

## tcp相关
### RTT
可以理解为往返时间，最为简单的说法是一发送，一syn，一来一回才能确认RTT。

### Bytes in flight
在途数据，这个数据和RTT有大关系。RTT越长，报文就相单于在路途中越久，这个时候在**路途中的数据**被叫做Bytes in flight，可以在 wireshark 中看到 SEQ/ACK analysis 中看到。

与RTT和发送窗口有关


### Bandwidth Delay Product
带宽时延积，可以抽象为这样一个矩形，长为RTT，宽为带宽。 计算公式 = 带宽 * RTT
可以理解为在途中BIF所有的累积值。
+------------------------------+
｜                             ｜
｜                             ｜
｜                             ｜
+------------------------------+
RTT 可以由 TCP 的iRTT看看。

### window 窗口
窗口会涉及到很多种类，来看下具体的。
接受窗口，接收端最多只能接受的数量，tcp的window字段表示，显性的可以看的到的。

拥塞窗口，发送端根据公式算的，不公开，各玩各的。

发送窗口，min(我方的拥塞窗口, 对方接受窗口)，实际的发送大小

calculated window size = window 字段 和 tcp option里面的 window scale 的算出来的值  ----> 接受窗口
不带window scale字段的情况下，TCP的Window是一个16bit位字段，它代表的是窗口的字节容量，
也就是TCP的标准窗口最大为2^16-1=65535个字节。

#### 理解
src-22 ==========> dst-59159 22接受的 window size 64kb

### 速度
send window / RTT ， 发送速度

send window（发送端口） 可以从 Bytes in flight 中看出。

