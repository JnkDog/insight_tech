# C的声明阅读
最近在看 Linux 网络部分的代码，发现对C语言的声明读的很艰辛，最近学到一个蛮好的用法，学习下。

## 方法简介
右左规则
1. 首先以标识符为起始点，读成：标识符是...
2. 接着扫描标识符的右边，如果遇到()，你知道这是要声明一个函数，于是读成：xxx是一个函数，返回...；如果遇到[]，那么这是一个数组，读成：xxx是一个数组，元素为...；继续向右扫描，直到右边结束，或是碰到)。
接下来扫描标识符的左边，如果遇到*就读成：xxx是一个指针，指向...，如果遇到类型，就直接说出类型。继续向左扫描，直到左边结束，或是碰到(。
3. 一直重复第2或第3步，直到解析结束。

这里的标识符可以看成是 int x 中的， ...就是一个待后续补充的部分。

## 举例
```C
int *(*f())()
```
1. f是一个标识符，看右边，f是一个函数，返回...
2. 继续右扫描，碰到 ）向左边扫描，f是一个函数返归一个指针，这个指针指向... , 碰到 （ 继续右扫描
3. f是一个函数返归一个指针，这个指针指向一个函数，该函数返回... 左扫描
4. f是一个函数返归一个指针，这个指针指向一个函数，该函数返回一个指针，指针指向一个int

口语话来说，f是一个函数，返回一个输出为int*的函数指针。
这里也可以看出go的精简的人性化右边挂载。
再复杂的指针就别写了，看的人和写的人都会emo

## Ref
1. https://cseweb.ucsd.edu//~ricko/rt_lt.rule.html
2. https://zhuanlan.zhihu.com/p/352036764