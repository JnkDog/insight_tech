# ArrayList 理解

## ArrayList 初始化
```Java
// 无参构造
// 本质是Object类型的空数组
private static final Object[]  DEFAULTCAPACITY_EMPTY_ELEMENTDATA = {};

public ArrayList() {
    this.elementData = DEFAULTCAPACITY_EMPTY_ELEMENTDATA;
}

// 带capacity的构造函数
// 直接返回一个initalCap大小的Object数组
public ArrayList(int initialCapacity) {
    if (initialCapacity > 0) {
        this.elementData = new Object[initialCapacity];
    } else if (initialCapacity == 0) {
        // elementData 实际存储位置
        this.elementData = EMPTY_ELEMENTDATA;
    } else {
        throw new IllegalArgumentException("Illegal Capacity: "+
                                            initialCapacity);
    }
}

// 传入一个Collection，调用的是Arrays.copyOf
 public ArrayList(Collection<? extends E> c) {
    elementData = c.toArray();
    if ((size = elementData.length) != 0) {
        // defend against c.toArray (incorrectly) not returning Object[]
        // (see e.g. https://bugs.openjdk.java.net/browse/JDK-6260652)
        if (elementData.getClass() != Object[].class)
            elementData = Arrays.copyOf(elementData, size, Object[].class);
    } else {
        // replace with empty array.
        this.elementData = EMPTY_ELEMENTDATA;
    }
}
```

## ArrayList add操作

## 涉及add的代码
```Java
public boolean add(E e) {
    modCount++; // 涉及iterator的迭代纠错功能，fail-fast机制，后面填坑
    // size 当前list的元素数量
    add(e, elementData, size);
    return true;
}

private void add(E e, Object[] elementData, int s) {
    if (s == elementData.length)
        elementData = grow();
    elementData[s] = e;
    size = s + 1;
}

private Object[] grow() {
    return grow(size + 1);
}

// 需要扩容的最小数组大小
private Object[] grow(int minCapacity) {
    int oldCapacity = elementData.length;
    if (oldCapacity > 0 || elementData != DEFAULTCAPACITY_EMPTY_ELEMENTDATA) {
        int newCapacity = ArraysSupport.newLength(oldCapacity,
                minCapacity - oldCapacity, /* minimum growth 最小增长 */
                oldCapacity >> 1           /* preferred growth 原数组长度/2 */);
        return elementData = Arrays.copyOf(elementData, newCapacity);
    } else {
        return elementData = new Object[Math.max(DEFAULT_CAPACITY, minCapacity)];
    }
}

// ArraysSupport.newLength函数，不在ArrayList中，在ArraysSupport.java中
public static int newLength(int oldLength, int minGrowth, int prefGrowth) {
    // assert oldLength >= 0
    // assert minGrowth > 0
    // 扩容时新数组长度 = 原数组长度 + max（原数组长度/2, 最小增长）---> 单纯的说扩容为1.5倍有点太教条主义
    int newLength = Math.max(minGrowth, prefGrowth) + oldLength;
    if (newLength - MAX_ARRAY_LENGTH <= 0) {
        return newLength;
    }
    // 扩容上限 Integer.MAX_VALUE，如果超过这个值就会overflow
    return hugeLength(oldLength, minGrowth);
}
```

值得注意的一点是，在无参初始化构造后的第一次add
```Java
private static final int DEFAULT_CAPACITY = 10;

private Object[] grow(int minCapacity) {
    // oldCapacity = 0
    int oldCapacity = elementData.length;
    if (oldCapacity > 0 || elementData != DEFAULTCAPACITY_EMPTY_ELEMENTDATA) {
        int newCapacity = ArraysSupport.newLength(oldCapacity,
                minCapacity - oldCapacity, /* minimum growth 最小增长 */
                oldCapacity >> 1           /* preferred growth 原数组长度/2 */);
        return elementData = Arrays.copyOf(elementData, newCapacity);
    } else {
        // 进入这个，minCapacity = 0 + 1 = 1，初始化默认长度为10
        return elementData = new Object[Math.max(DEFAULT_CAPACITY, minCapacity)];
    }
}
```


