# 循环增强

## 什么是循环增强
```Java
    for (Integer i : list)
```

## Java中的实现
语法糖将会转化成为iterator的形式，利用迭代器实现

## 迭代器的注意事项
不能在迭代器中调用外部的remove会发生ConcurrentModificationException异常

可以使用iterator本身的remove

 
