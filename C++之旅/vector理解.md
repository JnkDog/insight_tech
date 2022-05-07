# vector理解

## vector初始化细节
```cpp
/*
 * 在调用的时候string的默认初始化不是10
 * 所以大括号初始化不行，得使用小括号默认初始化
 * 初始化10个空字符串
 */
vector<string> v {10}
```