# Explain 理解

## rows
这个rows就是mysql认为必须要** 逐行去检查和判断的记录的条数。** 
举个例子来说，假如有一个语句 select * from t where column_a = 1 and column_b = 2;
全表假设有100条记录，column_a字段有索引（非联合索引），column_b没有索引。
column_a = 1 的记录有20条， column_a = 1 and column_b = 2 的记录有5条。

！！！预估值