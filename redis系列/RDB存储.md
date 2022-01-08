# RDB存储
## RDB是什么
RDB类似于存储快照，可以将内存中的数据进行快照存储。方便redis的数据进行备份和传输。
## 为什么需要RDB
AOF的存储机制恢复起来太慢了，需要一条条执行AOF中的redis命令。RDB可以快速恢复数据。
RDB体积小

## 开启或者触发RDB
* 手动使用save | bgsave 
其中save会阻塞主进程直到RDB完成，线上禁止使用
bgsave会创建子进程进行save操作，阻塞只会在fork阶段
* 如何触发RDB机制 （ps：由于save会阻塞主进程，不对save进行过多讲述）
	从节点全量复制操作的时候，主节点会执行RDB并发送给从库
	shutdown后没开启AOF，自动执行RDB
## RDB运行过程
![[rdb执行过程.jpg]]
* 如果有AOF或者RDB执行，直接返回

## RDB对系统的影响（坏）
1. 不同版本的RDB不兼容
2. RDB对实时持久化做的没AOF好，毕竟每次需要fork一个子进程
3. 
## RDB内部实现机制