# HashMap

# HashMap初始化
初始HashMap的时候没有进行哈希表的加载，只有一些基础成员变量的初始化。例如loadFactor，以及threshold --> 切换成2的n次方才行。
** 懒加载。。节省空间，等到真的要put了才进行哈希表的加载 **

# HashMap put和resize过程
```Java
static final int DEFAULT_INITIAL_CAPACITY = 1 << 4; // aka 16 默认hash table大小 
static final float DEFAULT_LOAD_FACTOR = 0.75f;  // 默认负载因子
```
size的上限应该是initalSize * loadFactory

put -> putVal

```Java
// 如果hash table没初始化或者table长度为0就进行扩resize（是可以理解为扩容，但是还是用英文比较好，resize可能会使hash table变小）
if ((tab = table) == null || (n = tab.length) == 0)
    n = (tab = resize()).length;

// 找到需要插入的表的位置，插入
if ((p = tab[i = (n - 1) & hash]) == null)
    tab[i] = newNode(hash, key, value, null);
```

-> 在put插入哈希表成功后，记录哈希表的size自增同时会和threshold进行比较 > initalSize * loadFactory, 进入resize阶段

resize阶段 newCap会变为原来的哈希表的2倍，如原来的(3 + 1 = 4) 4->8，其中的1代表已近插入数据然后的size大小
上限则是使用8 * loadFactory（0.75）= 6
在接着把旧哈希表的数据重新传入到新的哈希表中


