# Redis数据类型和底层数据结构的关系

| Redis数据类型 | 底层数据类型        |
| ------------- | ------------------- |
| String        | 简单动态字符串(SDS) |
| List          | 压缩列表  双向链表   |
| Hash          | 压缩列表  哈希表    |
| Sorted Set    | 压缩列表  跳表      |
| Set           | 哈希表   整数数组   |
	
	
| 数据结构 | 内部编码            |
| -------- | ------------------- |
| string   | raw, int, embstr    |
| hash     | hashtable, ziplist  |
| lish     | linkedlist, ziplist |
| set      | hashtable, intset   |
| zset      |skiplist ziplist                  |

TODO REVIEW source code

String 

```shell
redis> SET msg "hello world"
OK
```

其中key为字符串的“msg”  SDS
value为"hello world"的SDS

## SDS 简单动态字符串和C的字符串的区别
C字符串获取长度需要On的复杂度

SDS的结构为
｜ sdshdr ｜
｜free / alloc (看redis 版本)  4B｜
｜len   4B｜
| Buf   指向具体的字符串数组的指针 |

* C的字符串有缓冲区问题，如果没有分配足够的空间，数据会被意外修改。
* SDS的api在进行字符串拼接的时候需要进行检测空间是否足够，不够则进行扩容

SDS的扩容的空间分配机制

																


## Hash类型 （value当中的哈希）
### ziplist
在配置中hash元素个数小于 hash-max-ziplist-entrise (default 512)
同时 hash-max-ziplist-value (default 64 bytes)  才用ziplist ！！！ 
2者都满足的时候。


## 队列类型