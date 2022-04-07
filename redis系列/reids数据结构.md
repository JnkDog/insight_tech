# Redis数据类型和底层数据结构的关系

## Redis数据结构流程
![](./pictures/%E6%95%B0%E6%8D%AE%E5%AD%98%E5%82%A8%E4%BE%8B%E5%AD%90.png)

```C
typedef struct redisDb {    
    dict *dict;                 //保持数据的dict    
    dict *expires;              //保持key的过期信息
    dict *blocking_keys;        // 一些同步的keys    
    dict *ready_keys;            
    dict *watched_keys;         // MULTI 的时候监测使用
    int id;                     // Redis默认有16个数据库 数据库编号
    long long avg_ttl;          /* Average TTL, just for stats */
} redisDb;
```
这是一个redis数据库实例的数据结构，主要的结构是dict，里面存放所有的键值对。
dict的结构

```C
/* * 字典 * * 每个字典使用两个哈希表，用于实现渐进式 rehash */
typedef struct dict {    
    // 特定于类型的处理函数 --> hash函数
    dictType *type;    
    // 类型处理函数的私有数据    
    void *privdata;    
    // 哈希表（2 个） --> 渐进式hash   
    dictht ht[2];    
    // 记录 rehash 进度的标志，值为 -1 表示 rehash 未进行    
    int rehashidx;    
    // 当前正在运作的安全迭代器数量    
    int iterators;
} dict;
```
*ht[2]*是一个长度为2的数组，正常情况下回使用ht[0]来存储数据，当进行rehash操作时，redis会使用ht[1]来配合进行渐进式rehash操作。而在平常情况下，只有 ht[0]有效，ht[1]里面没有任何数据。

dictht 就是我们说的 hashTable （dictht 是字典 dict 哈希表的缩写，即 dict hash table）
```C
/* * 哈希表 */
typedef struct dictht {    
    // 哈希表节点指针数组（俗称桶，bucket）    
    dictEntry **table;    
    // 指针数组的大小 它总是 2 的指数次幂。 ---> 一个nice的设计，可以快速取模运算 
    unsigned long size;    
    // 指针数组的长度掩码，用于计算索引值，其实永远都是size-1，hash % size = hash & (sizemask - 1)
    unsigned long sizemask;    
    // 哈希表现有的节点数量    
    unsigned long used;
} dictht;
```

dictht是有dictEntry组成的
```dictEntry
 /* * 哈希表节点 */
typedef struct dictEntry {    
    // 键    
    void *key;    
    // 值    
    union {        
        void *val;       
        uint64_t u64;        
        int64_t s64;    
    } v;   
    // 链往后继节点    
    struct dictEntry *next;
} dictEntry;
```
看上面的图可以知道，value指向的是redisObject对象，这个对象对底层的实际存储进行了封装，就比如string类型的key，value的实现可能有raw，embstr，但是用户层面却使用了一样的api，就是redisObject进行了封装
```C
typedef struct redisObject {    
    // 类型    
    unsigned type:4;    
    // 编码    
    unsigned encoding:4;    
    // 对象最后一次被访问的时间        
    unsigned lru:REDIS_LRU_BITS; 
    // 引用计数    
    int refcount;    
    // 指向实际值的指针    
    void *ptr;
} robj;
```

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