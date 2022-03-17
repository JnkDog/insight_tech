# ConcurrentHashMap
## 初始化哈希表
```JAVA
// 由Node组成的哈希表
 static class Node<K,V> implements Map.Entry<K,V> {
        final int hash;
        final K key;
        volatile V val;
        volatile Node<K,V> next;
        ...
}

注意：ConcurrentHashMap中间有很多的不同的Node
ForwardingNode表示一个因为扩容而正在移动中的节点；
ReservationNode表示一个空节点，加锁时使用；
TreeNode表示红黑树中普通的节点；
TreeBin表示红黑树的根节点，封装了红黑树中左旋、右旋、新增节点、删除节点等维护红黑树平衡的逻辑

```
JDK1.8中，在第一次put进入哈希表中才会调用初始化
```Java
for (Node<K,V>[] tab = table;;) {
    Node<K,V> f; int n, i, fh; K fk; V fv;
    if (tab == null || (n = tab.length) == 0)
    tab = initTable();
    ...
}
```
这里会有并发问题，当多个线程一起进入initTable()方法，会进行如何操作确保维护并发性质。
```Java
 while ((tab = table) == null || tab.length == 0) {
 			// 已经有进程在init，让出时间片
            if ((sc = sizeCtl) < 0)
                Thread.yield(); // lost initialization race; just spin
            else if (U.compareAndSetInt(this, SIZECTL, sc, -1)) {
            // CAS操作成功的进程进入扩容阶段
                try {
                
                    if ((tab = table) == null || tab.length == 0) {
                    // 哈希表的bin长度为n
                        int n = (sc > 0) ? sc : DEFAULT_CAPACITY;
                        @SuppressWarnings("unchecked")
                        Node<K,V>[] nt = (Node<K,V>[])new Node<?,?>[n];
                        table = tab = nt;
                        // 相当于sc = n * 0.75
                        sc = n - (n >>> 2);
                    }
                } finally {
                    sizeCtl = sc;
                }
                break;
            }
```

## Put操作
```Java
final V putVal(K key, V value, boolean onlyIfAbsent) {
        if (key == null || value == null) throw new NullPointerException();
        int hash = spread(key.hashCode());
        int binCount = 0;
        // 无限循环直到完成put
        for (Node<K,V>[] tab = table;;) {
            Node<K,V> f; int n, i, fh; K fk; V fv;
            // 如果hash table没初始化，先初始化，这里可能会有并发问题，但是在initTable中解决
            if (tab == null || (n = tab.length) == 0)
                tab = initTable();
            // CAS操作获得volatile取出对应的Node对象赋值给f，f是volatile确保多线程的可见性，如果为null代表可以放进去
            else if ((f = tabAt(tab, i = (n - 1) & hash)) == null) {
                // CAS set Node。set成功代表插入成功，set 失败代表，进入下一步
                if (casTabAt(tab, i, null, new Node<K,V>(hash, key, value)))
                    break;                   // no lock when adding to empty bin
            }
            // 进入扩容。。。 后面讲， fh = firstNode.hashCode
            else if ((fh = f.hash) == MOVED)
                tab = helpTransfer(tab, f);
            // 如果哈希表第一个点没有获得锁，则进入，如果put的与第一个node相等直接返回
            else if (onlyIfAbsent // check first node without acquiring lock
                     && fh == hash
                     && ((fk = f.key) == key || (fk != null && key.equals(fk)))
                     && (fv = f.val) != null)
                return fv;
            else {
                V oldVal = null;
                // firstNode加锁
                synchronized (f) {
                    // tab 哈希数组，i 哈希数组的索引
                    if (tabAt(tab, i) == f) {
                        if (fh >= 0) {
                            binCount = 1;
                            // hash冲突后的遍历，插入
                            for (Node<K,V> e = f;; ++binCount) {
                                K ek;
                                // 尾部的hash节点中有相同的直接返回
                                if (e.hash == hash &&
                                    ((ek = e.key) == key ||
                                     (ek != null && key.equals(ek)))) {
                                    oldVal = e.val;
                                    if (!onlyIfAbsent)
                                        e.val = value;
                                    break;
                                }
                                Node<K,V> pred = e;
                                if ((e = e.next) == null) {
                                    pred.next = new Node<K,V>(hash, key, value);
                                    break;
                                }
                            }
                        }
                        // 红黑树的方式插入
                        else if (f instanceof TreeBin) {
                            Node<K,V> p;
                            binCount = 2;
                            if ((p = ((TreeBin<K,V>)f).putTreeVal(hash, key,
                                                           value)) != null) {
                                oldVal = p.val;
                                if (!onlyIfAbsent)
                                    p.val = value;
                            }
                        }
                        else if (f instanceof ReservationNode)
                            throw new IllegalStateException("Recursive update");
                    }
                }
                if (binCount != 0) {
                    // 拉链法转化为红黑树法
                    if (binCount >= TREEIFY_THRESHOLD)
                        treeifyBin(tab, i);
                    if (oldVal != null)
                        return oldVal;
                    break;
                }
            }
        }
        addCount(1L, binCount);
        return null;
    }
```
整体上来说，加锁直接加入到Node数组的第一节点，相比以前的阶段锁，颗粒度更加小。

## Get操作
```Java
 public V get(Object key) {
        Node<K,V>[] tab; Node<K,V> e, p; int n, eh; K ek;
        int h = spread(key.hashCode());
        if ((tab = table) != null && (n = tab.length) > 0 &&
            (e = tabAt(tab, (n - 1) & h)) != null) {
            // 没有扩容的情况下直接查
            if ((eh = e.hash) == h) {
                if ((ek = e.key) == key || (ek != null && key.equals(ek)))
                    return e.val;
            }
            // hash < 0 正在迁移，使用fwd占位Node去看table中的数据
            // ConcurrentHashMap 内部有很多类型的Node
            // eh = -1, ForwardingNode 正在迁移
            // eh=-2，说明该节点是一个TreeBin，此时调用TreeBin的find()方法遍历红黑树，注意：由于红黑树可能正在旋转变色，所以find()方法里会加一个读写锁。
            else if (eh < 0)
                return (p = e.find(h, key)) != null ? p.val : null;
            while ((e = e.next) != null) {
                if (e.hash == h &&
                    ((ek = e.key) == key || (ek != null && key.equals(ek))))
                    return e.val;
            }
        }
        return null;
    }
```