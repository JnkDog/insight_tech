# poll机制
![](./pictures/poll.png)

可以看出改变的是reevent里面的值，event不变。从而使数据可重用，不像select的bitset机制，每次都需要重置

![](./pictures/poll%E4%BB%A3%E7%A0%81.png)

代码里的reevent会改变，开销比较小
fds是基于pollfd的动态数组，突破上限
但还是存在On查询复杂度和内核，用户态上下文拷贝的问题。

