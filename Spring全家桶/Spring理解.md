# Spring理解
## IOC
IOC实现控制反转

## 一些注意事项
1. bean的id和name属性需要唯一
2. beans的产生默认是单例模式，可以使用scope进行调整 prototype

3. beans顺序加载用depends-on，顺序上的关系如先A后B，而不是一种包含，如B中需要A对象

### 依赖注入
XML的方式
有参数构造需要加入property和setXXX函数在类中 （基本类型）
-- 无参数构造
如果不是基本类，而一个Bean需要得在xml中配置ref ref名字要和单独的bean中的name相同或者采用autwired的在xml中，
（需要setXXX类型的函数在Bean中）
byType找bean
byName找setXXX中的xxx
-- 有参数构造
 <constructor-arg/>


## AOP
代理的思想，核心业务无侵入式修改

### 如何spring中使用
加入spring-aspects依赖，同时配置aop:config, ** 动态代理！**（要理解下）

其中比较有意思的是around方法，需要自己手动调用代理中的类的方法。
如果需要返回值得从aop类中获取！！！
