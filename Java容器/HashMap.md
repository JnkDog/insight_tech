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

// 找到需要插入的表的位置，插入，如果hash表中暂时没有值
if ((p = tab[i = (n - 1) & hash]) == null)
    tab[i] = newNode(hash, key, value, null);
else {
    // p != null
    Node<K,V> e; K k;
    if (p.hash == hash &&
        ((k = p.key) == key || (key != null && key.equals(k))))
        // 如果hashtable第一个就满足条件，单纯的比较key
        e = p;
    else if (p instanceof TreeNode)
        // 如果是树类型就转为树插入
        e = ((TreeNode<K,V>)p).putTreeVal(this, tab, hash, key, value);
    else {
        for (int binCount = 0; ; ++binCount) {
            if ((e = p.next) == null) {
                // 拉链法，读取下一个node为null后插入
                p.next = newNode(hash, key, value, null);
                // TREEIFY_THRESHOLD = 8, 这里是因为从第二个node开始所以上限为7
                if (binCount >= TREEIFY_THRESHOLD - 1) // -1 for 1st
                    treeifyBin(tab, hash);
                break;
            }
            if (e.hash == hash &&
                ((k = e.key) == key || (key != null && key.equals(k))))
                break;
            p = e;
        }
    }
    if (e != null) { // existing mapping for key
        V oldValue = e.value;
        if (!onlyIfAbsent || oldValue == null)
            e.value = value;
        afterNodeAccess(e);
        return oldValue;
    }
}
```

-> 在put插入哈希表成功后，记录哈希表的size自增同时会和threshold进行比较 > initalSize * loadFactory, 进入resize阶段

resize阶段 newCap会变为原来的哈希表的2倍，如原来的(3 + 1 = 4) 4->8，其中的1代表已近插入数据然后的size大小
上限则是使用8 * loadFactory（0.75）= 6
在接着把旧哈希表的数据重新传入到新的哈希表中

！！！经过观测可以发现，我们使用的是2次幂的扩展(指长度扩为原来2倍)，所以，元素的位置要么是在原位置，要么是在原位置再移动2次幂的位置

```Java
final Node<K,V>[] resize() {
    Node<K,V>[] oldTab = table;
    int oldCap = (oldTab == null) ? 0 : oldTab.length;
    int oldThr = threshold;
    int newCap, newThr = 0;
    if (oldCap > 0) {
        // 超出最大值，就扩容到  Integer.MAX_VALUE
        if (oldCap >= MAXIMUM_CAPACITY) {
            threshold = Integer.MAX_VALUE;
            return oldTab;
        }
        else if ((newCap = oldCap << 1) < MAXIMUM_CAPACITY &&
                    oldCap >= DEFAULT_INITIAL_CAPACITY)
            // 扩容到原来的2倍
            newThr = oldThr << 1; // double threshold
    }
    // 如果初始化使用 this(int initialCap) oldThr有值，但此时oldCap没有数值的情况, * initialCap赋给threshold的 *
    else if (oldThr > 0) // initial capacity was placed in threshold
        newCap = oldThr;
    else {              // 单 new HashMap（）初始化
        newCap = DEFAULT_INITIAL_CAPACITY;
        newThr = (int)(DEFAULT_LOAD_FACTOR * DEFAULT_INITIAL_CAPACITY);
    }
    // 计算新的上限 如果初始化使用 this(int initialCap) oldThr有值，但此时oldCap没有数值的情况
    if (newThr == 0) {
        float ft = (float)newCap * loadFactor;
        newThr = (newCap < MAXIMUM_CAPACITY && ft < (float)MAXIMUM_CAPACITY ?
                    (int)ft : Integer.MAX_VALUE);
    }
    threshold = newThr;
    @SuppressWarnings({"rawtypes","unchecked"})
    Node<K,V>[] newTab = (Node<K,V>[])new Node[newCap];
    table = newTab;
    if (oldTab != null) {
        for (int j = 0; j < oldCap; ++j) {
            Node<K,V> e;
            if ((e = oldTab[j]) != null) {
                oldTab[j] = null;
                // 单节点直接插
                if (e.next == null)
                    newTab[e.hash & (newCap - 1)] = e;
                else if (e instanceof TreeNode)
                    ((TreeNode<K,V>)e).split(this, newTab, j, oldCap);
                else { // preserve order
                    // 优化插法
                    Node<K,V> loHead = null, loTail = null;
                    Node<K,V> hiHead = null, hiTail = null;
                    Node<K,V> next;
                    do {
                        next = e.next;
                        if ((e.hash & oldCap) == 0) {
                            // 原地不动的node
                            if (loTail == null)
                                loHead = e;
                            else
                                loTail.next = e;
                            loTail = e;
                        }
                        else {
                            // 需要加newCap的node
                            if (hiTail == null)
                                hiHead = e;
                            else
                                hiTail.next = e;
                            hiTail = e;
                        }
                    } while ((e = next) != null);
                    if (loTail != null) {
                        loTail.next = null;
                        newTab[j] = loHead;
                    }
                    if (hiTail != null) {
                        hiTail.next = null;
                        newTab[j + oldCap] = hiHead;
                    }
                }
            }
        }
    }
    return newTab;
}
```



## hash函数
```Java
// 计算hash值
static final int hash(Object key) {
    int h;
    // 允许为 KEY 为 null 成为 0
    return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
}

// 计算哈希表的索引
static int indexFor(int h, int length) {  //jdk1.7的源码，jdk1.8没有这个方法，但是实现原理一样的
     return h & (length-1);  //第三步 取模运算
}
```
在代码中，(h = key.hashCode()) ^ (h >>> 16) 可以保证hash值的高低位都参与运算
计算索引的 h & (length-1); 因为length是2的n次方，减去一以后可以确保取模，加快运算速度


红黑树退化为链表的阈值为 6，它和链表转化为红黑树的阈值 8 不同，原因在于防止某个桶中节点个数在 8 附近震荡，导致频繁地发生转化。

## 和HashTable比较
- 线程是否安全：HashTable 使用 synchronized 关键字修饰操作方法来获得相对线程安全性；
- 对 null 键的支持：HashTable 不支持 null 键；
- 初始容量和扩容：HashTable 默认初始容量为 11，每次扩容，容量都为原来的 2n+1，会直接使用手动传入的容量作为初始容量。