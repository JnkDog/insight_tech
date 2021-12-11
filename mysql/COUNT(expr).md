COUNT(*) , COUNT(1) [aka COUNT(常量)] 和 COUNT(列名)
1. COUNT(列名)不会统计此列为NULL的行
2. COUNT(*) 在InnDB和MyISAM中的实现细节是不一样的。具体的在于MyISAM只支持表级的锁，而且不支持事务，只需要一个用来维护表数量的参数即可记录（MyISAM）。而InnDB则是支持行级的锁和事务，所以不能使用MyISAM的方法。但是在InnDB中，COUNT(*)是优化过的。具体的优化过程如下：
  * COUNT(*) 只是统计了表里面的行数，而不是具体的值。因此InnDB会挑选出成本较低的索引项目进行扫描，而不是主键的索引。
 
 PS: 以上都针对的是没有where的情况分析
 *ATTENTION* ：show_table_status 只会给出大概的数据行，是一个估算的值