# 代码目录结构
数据类型：  
- String（t_string.c、sds.c、bitops.c）  
- List（t_list.c、ziplist.c）  
- Hash（t_hash.c、ziplist.c、dict.c）  
- Set（t_set.c、intset.c）  
- Sorted Set（t_zset.c、ziplist.c、dict.c）  
- HyperLogLog（hyperloglog.c）  
- Geo（geo.c、geohash.c、geohash_helper.c）  
- Stream（t_stream.c、rax.c、listpack.c）  
  
全局：  
- Server（server.c、anet.c）  
- Object（object.c）  
- 键值对（db.c）  
- 事件驱动（ae.c、ae_epoll.c、ae_kqueue.c、ae_evport.c、ae_select.c、networking.c）  
- 内存回收（expire.c、lazyfree.c）  
- 数据替换（evict.c）  
- 后台线程（bio.c）  
- 事务（multi.c）  
- PubSub（pubsub.c）  
- 内存分配（zmalloc.c）  
- 双向链表（adlist.c）  
  
高可用&集群：  
- 持久化：RDB（rdb.c、redis-check-rdb.c)、AOF（aof.c、redis-check-aof.c）  
- 主从复制（replication.c）  
- 哨兵（sentinel.c）  
- 集群（cluster.c）  
  
辅助功能：  
- 延迟统计（latency.c）  
- 慢日志（slowlog.c）  
- 通知（notify.c）  
- 基准性能（redis-benchmark.c）

后台任务的代码在 bio.c
