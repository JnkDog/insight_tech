# commit failed exception
## 发生背景
rebalance的时候，原有分区被新的消费实例占用从而造成提交的问题。

## 缩短当条消息的处理时间

## 增大max.poll.interval.ms 或者减少一次性poll拉取的消息


## 最终思路，启用多线程处理消息，但是有弊端