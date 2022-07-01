# RAII
## 如何理解
在堆上的资源进行释放，或者其他资源释放如 socket，file handler这种。
平常的进程流 可能会产生 exception，造成最后的资源没释放。
避免使用exception的方式是：
离开作用域调用析构函数，在析构函数中进行资源的释放

## 例子
lock_guard的用法