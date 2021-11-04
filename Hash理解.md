Q1. HashMap, Set, java 是否存在HashTable

Q2. 线程的安全性

Q3. 各个之间的差别和联系



# 1 从0开始的Hash理解

```java
# Collection<? extends E> c meaning ？
add(Collection<? extends E> c)
 
```

HashMap的底层是数组加链表加红黑树     

HashSet implements Set<E>  

HashSet的底层是基于HashMap实现的，HashMap的<K, V>中的K是HashSet存放的地方，确保了唯一性。

由于在计算Hash的时候，null被视为0 --- hash值

HashMap是HashTable的轻量级的实现，HashTable不支持null key和 null value 因为没有对null值的特殊判定

HashTable是线程安全的 加入了**synchronize** 修饰方法



# 关键字的理解

```java
// 这些关键字的理解
transient volatile Node[] table;

// final
// 加入final关键字后，属性和方法无法修改
// 用final修饰的类不能被继承，没有子类
```





# synchronize的理解

1. java如何实现synchronize
2. synchronize加锁可使用在哪里 ？ this 非静态。静态 x.class ---> 反射
3. 







# RandomAccess 和 Java 文件操作

seek 设定起点的游标。。。 实现断点传送





# Page 中 tuples的计算

1. Page  =  headers + many tuples   tuple 大小固定
2. 一个Table 里面含多个page， 一个page 含多个tuples



# iterator 究竟这么写

1. hasnext() 和 next()的关系
2. java的 comparator **升序**  （a, b）->    a > b return 1.   a = b return 0.   a < b return -1 **降序** 反过来



# Java notify





The status of the submission is that both circuits in the trafficLights.hs are completed, compile and they both produce the correct output. 

The logic for the circuits appear to be correct and they were both run using the main method given in the trafficLightsRun.hs which also runs and compile with no errors.

 The circuits were tested using input data given in the trafficLightRun.hs. controller1 was tested by giving a list of integers where only the first integer is 1 and all the rest are zero to simulate the required function. 

The circuit was also tested to show what would happen if the reset button was pressed again after the initial press which showed that it reverted back to the initial state of green and from there on, it proceeds with the normal sequence of state changes. 





controller2 was tested the same way as inputs are given as a pairs where the first pair is 1,0 to simulat the reset button press. A couple of pairs in, the second index in the pair is set to one, 0, 1, to simulate a walkrequest and after this the circuit performs the required functionality of going to amber then red for 3 cycles before returning to the initial state of green. 

At the same time this also showed that the walk outputs 1 when the circuit outputs red and wait is 1 when green outputs 1. Finally the test data also includes multiple walkrequest presses to simulate the incrementation of the counter as well as a reset press to reset the counter to 0.     



The approach used to design each circuit is as follows: controller1: this circuit contains 9 different state changes where each new one from the required sequence of states is represented by a new line. Each state change is dictated by a delay flip flop where if the logic for it is true then it takes the new state else it is ignored. The truth logic is dictated by simple and2 and or2 logic gates and no black box circuits such as muxes were used. Since there were different states for the same colour such as red1, 2 and 3, a orw gate is used to represent all of them ie the previously mentioned red state changes will be represented by red.



 controller2: this circuit is similar to the first controller but also contains an counter to count the number of times walkrequest is pressed ie passed in as an input along with a value for reset. The counter is reset to 0 if reset is 1 and the counter is incremented by 1 if the walkrequest is 1. The circuit also includes walk and wait outputs that are linked to the traffic light colours as well where if red is 1 then walk is also 1 and if green or amber are 1 then wait is 1.   

