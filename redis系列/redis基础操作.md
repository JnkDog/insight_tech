# 基础操作和坑
## 操作命令
1. dbsize。 返回数据库中的key数目。dbsize时间复杂度是O1（猜测维护了一个变量），反观keys 命令时间复杂度是On   线上环境key多的时候对性能有影响。
2.  setnx  setxx   setnx为键不存在才能设置成功，用于添加，xx想法只有key存在才能设置，用于更新   **setnx可以用来实现分布式锁**
3.  尽量采用批量操作，例如n个set指令，时间大概为n次网络连接+n次redis执行命令。而mset时间为1次网络+n次命令的时间
4.  当redis查询失效后，进入mysql寻找，并回填到redis中，**设置过期时间**
5.  hgetall，如果哈希元素过多会阻塞redis的可能，可以采用**hscan**，渐进式便利操作
6.  ltrim key start end ---- 保留 start 到 end 的数据，其他删除。。 ⚠️ 
7.  list 的阻塞操作 brpop blpop，需要注意的是阻塞后，先执行的brpop的得到的客户端最先得到.  如果有多个key的话，从左到右遍历key，一旦有一个key能弹出元素，客户端立即返回。（brpop, blpop）都一样 都是这个遍历的操作。
8.  srandmember 和 spop都弹出元素 区别在于 spop会弹出 srandmember不真正弹出
9.  set 可以用来整用户喜好的tag
10.  rename的期间，redis会执行del命令，如果旧key值过大，可能会造成阻塞。
11.  set会去掉设置的expire 时间
12.  migrate 数据迁移是原子操作
13.  redis切换数据库后还是单进程的，多数据库会对性能产生影响，多数据库功能使用多个redis实例
14.  redis 慢查询，只会记录执行命令的时间，无慢查询不代表没有客户端超时
15.  redis 事务。multi 开启 exec结束。。。 但在运行的时候，会有2种不同的情况。1. 语法错误，全部不执行。2. 语法对，但是指令错，则需要自己修理
16.  