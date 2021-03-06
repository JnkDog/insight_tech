# 主从架构

## 主从设置
redis多个实例启动后，可以用replicaof形成主从关系。
例如，现在有实例 1（ip：172.16.19.3）和实例 2（ip：172.16.19.5），我们在实例 2 上执行以下这个命令后，实例 2 就变成了实例 1 的从库，并从实例 1 上复制数据：
```shell
replicaof 172.16.19.3 6379
```

同步的过程主要可以用下图表示
![](./pictures/redis%E4%B8%BB%E4%BB%8E%E7%AC%AC%E4%B8%80%E6%AC%A1%E5%90%8C%E6%AD%A5.png)

**第一阶段是**主从间建立连接，同步协商。主要是为了**全量复制**做准备。从这一步开始，从库和主库建立连接，告诉主库要进行同步，主库确认后，主从库开始同步了。
！！！
这一阶段包括了许多步骤，具体来说:
1. 从库发送psync命令，表示进行同步，主库根据参数进行复制。值得注意的是，pysnc命令包含了主库的runID和复制进度offset参数。

* runID代表每个redis实例启动都会生成一个随机ID，用来唯一标记这个实例。当从库和主库第一次复制，因为不知道主库的ID，所以runID设置为 ？

* offest = -1， 表示第一次复制

2. 主库收到pysnc命令后，会用FULLRESYNC命令后带上2个参数：主库runID和主库的复制进度offset，返回给从库。从库收到命令后，会记录2个参数。

注：这里的offset表示 主库写入偏移量，作为全量复制和增量复制的瞄点。（类似于一个基准点）每个从库也有一个读取偏移量。

这里有个地方需要注意，FULLRESYNC 响应表示第一次复制采用的全量复制，也就是说，主库会把当前所有的数据都复制给从库。（所以为了同步，主库会进行一个RDB快照的生成）


在**第二阶段**，主库将所有数据同步给从库。从库收到数据后，在本地完成数据加载。这个过程依赖于内存快照生成的 RDB 文件。

具体来说，主库执行 bgsave 命令，生成 RDB 文件，接着将文件发给从库。从库接收到 RDB 文件后，会先清空当前数据库，然后加载 RDB 文件。这是因为从库在通过 replicaof 命令开始和主库同步前，可能保存了其他数据。为了避免之前数据的影响，从库需要先把当前数据库清空。很自然的想法。

在主库将数据同步给从库的过程中，主库不会被阻塞，仍然可以正常接收请求。否则，Redis 的服务就被中断了。但是，这些请求中的写操作并没有记录到刚刚生成的 RDB 文件中。为了保证主从库的数据一致性，主库会在内存中用专门的 **replication buffer**，记录 RDB 文件生成后收到的所有写操作。**和单机RDB有什么其他差别吗？**

## 主从架构的弊端
通过分析主从库间第一次数据同步的过程，你可以看到，一次全量复制中，对于主库来说，需要完成两个耗时的操作：生成 RDB 文件和传输 RDB 文件。（这里带来了一个问题，如何传输RDB文件，什么协议，那种方式，会阻塞进程吗？？？）

如果从库数量很多，而且都要和主库进行全量复制的话，就会导致主库忙于 fork 子进程生成 RDB 文件，进行数据全量同步。fork 这个操作会阻塞主线程处理正常请求，从而导致主库响应应用程序的请求速度变慢。每个replicaof操作都是需要主库进行fork操作执行RDB快照，所以会严重拖慢主库的运行速度。  ---> fork会阻塞进程 ---> 怎么理解？

这时候带来 **主 - 从 - 从** 架构

简单来说，我们在部署主从集群的时候，可以手动选择一个从库（比如选择内存资源配置较高的从库），用于级联其他的从库。然后，我们可以再选择一些从库（例如三分之一的从库），在这些从库上执行如下命令，让它们和刚才所选的从库，建立起主从关系。

![](./pictures/%E4%B8%BB%E4%BB%8E%E4%BB%8E%E6%9E%B6%E6%9E%84.png)

那么，一旦主从库完成了全量复制，它们之间就会一直维护一个网络连接，主库会通过这个连接将后续陆续收到的命令操作再同步给从库，这个过程也称为基于**长连接的命令传播**，可以避免频繁建立连接的开销。  (长链接的命令传播是什么鬼？？？)

由于主从库之间是通过网络进行数据传播，那么要如何保证数据的一致性。

## 增量复制
2.8以前的redis会进行全量复制，重新生成RDB。
2.8后采用增量复制。增量复制只会把主从库网络断连期间主库收到的命令，同步给从库。

那么，增量复制时，主从库之间具体是怎么保持同步的呢？这里的奥妙就在于 **repl_backlog_buffer** 这个缓冲区。我们先来看下它是如何用于增量命令的同步的。

当从库断连又重连之后，通过psync命令告诉主库自己的slave_repl_offset，然后主库根据自己的master_repl_offset和slave_repl_offset来判断是需要全量同步还是把两者之间的命令增量同步给从库（同步的方式就是通过主库与每个从库建立连接之后的这个所谓的replication buffer）


1、主从库连接都断开了，哪里来replication buffer呢？(主从库同步中，replication buffer主要是主库用来同步命令给从库的，一旦从库断联，replication buffer也不存在了，但repl_backlog_buffer是存在的) 

2、应该不是“主从库断连后”主库才把写操作写入repl_backlog_buffer，只要有从库存在，这个repl_backlog_buffer就会存在。主库的所有写命令除了传播给从库之外，都会在这个repl_backlog_buffer中记录一份，缓存起来，只有预先缓存了这些命令，当从库断连恢复后，从库重新发送psync $master_runid $offset，主库才能通过$offset在repl_backlog_buffer中找到从库断开的位置，只发送$offset之后的增量数据给从库即可

### repl_backlog_buffer 和 replication buffer 区别

1、repl_backlog_buffer：就是上面我解释到的，它是为了从库断开之后，如何找到主从差异数据而设计的环形缓冲区，从而避免全量同步带来的性能开销。如果从库断开时间太久，repl_backlog_buffer环形缓冲区被主库的写命令覆盖了，那么从库连上主库后只能乖乖地进行一次全量同步，所以repl_backlog_buffer配置尽量大一些，可以降低主从断开后全量同步的概率。而在repl_backlog_buffer中找主从差异的数据后，如何发给从库呢？这就用到了replication buffer。 
2、replication buffer：Redis和客户端通信也好，和从库通信也好，Redis都需要给分配一个 内存buffer进行数据交互，客户端是一个client，从库也是一个client，我们每个client连上Redis后，Redis都会分配一个client buffer，所有数据交互都是通过这个buffer进行的：Redis先把数据写到这个buffer中，然后再把buffer中的数据发到client socket中再通过网络发送出去，这样就完成了数据交互。所以主从在增量同步时，从库作为一个client，也会分配一个buffer，只不过这个buffer专门用来传播用户的写命令到从库，保证主从数据一致，我们通常把它叫做replication buffer。

repl_backlog_buffer 是一个环形缓冲区，主库会记录自己写到的位置，从库则会记录自己已经读到的位置。感觉类似mysql的redo log

在主库接受写命令的时候，随着主库不断接受写操作，他在环形缓冲区中的写位置会偏离起始位置。这种偏移量叫做 **master_repl_offset**

同样，从库在复制完写操作命令后，它在缓冲区中的读位置也开始逐步偏移刚才的起始位置，此时，从库已复制的偏移量 **slave_repl_offset** 也在不断增加。正常情况下，这两个偏移量基本相等。（这里的偏移量是在从库还是主库？？？  是从库的，后面会通过pysnc发送偏移量给主库）


主从库的连接恢复之后，从库首先会给主库发送 psync 命令，并把自己当前的 slave_repl_offset 发给主库，主库会判断自己的 master_repl_offset 和 slave_repl_offset 之间的差距。在网络断连阶段，主库可能会收到新的写操作命令，所以，一般来说，master_repl_offset 会大于 slave_repl_offset。此时，主库只用把 master_repl_offset 和 slave_repl_offset 之间的命令操作同步给从库就行。

![](./pictures/redis%E5%A2%9E%E9%87%8F%E5%A4%8D%E5%88%B6.png)

总结来说， redis主从架构有全量复制、基于长连接的命令传播，以及增量复制。