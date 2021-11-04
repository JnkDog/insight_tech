# B+ Tree的危险性

1. 不像append only的database，需要对disk进行覆写，这是一个物理器件上的操作。分为ssd和机械盘

2. 覆盖写带来的危害，如果插入操作造成页满了，则需要进行分割页，高危险操作造成孤页（覆盖页）

   针对这种危害性，需要特殊的操作名为 write-ahead log (**WAL**) aka **redo log**

   这是一个append only的file，对B tree的修改需要现在这里记录 然后再适用到b tree中

   即便数据库奔溃，redo log也能用来恢复

   

