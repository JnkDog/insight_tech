# JAVA线程创建

## Java线程创建的方法
### 继承Thread类
* 定义Thread类的子类，并重写该类的run方法，该run方法的方法体就代表了线程要完成的任务。因此把run()方法称为执行体。
* 创建Thread子类的实例，即创建了线程对象。
* 调用线程对象的start()方法来启动该线程。

## 实现Runnable接口创建
* 定义Runnable接口的实现类，并重写该接口的run()方法，该run()方法的方法体同样是该线程的线程执行体。
* 创建Runnable实现类的实例，并以此实例作为Thread的target来创建Thread对象，该Thread对象才是真正的线程对象。
* 调用线程对象的start()方法来启动该线程。

## 实现Callable接口创建
### Callable和Runnable接口的区别
Runnable自 Java 1.0 以来一直存在，但Callable仅在 Java 1.5 中引入,目的就是为了来处理Runnable不支持的用例。Runnable 接口 不会返回结果或抛出检查异常，但是 Callable 接口 可以。所以，如果任务不需要返回结果或抛出异常推荐使用 Runnable 接口 ，这样代码看起来会更加简洁。


