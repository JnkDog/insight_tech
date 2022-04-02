# park 和 unpark

LockSupport.park(); 线程进入waiting状态，等待LockSupport.unpark()的唤醒
通过 LockSupport.park() 方法将线程挂起期间，不会抛出中断异常，所以在被唤醒后，需要通过 Thread.interrupted() 方法的返回值来决定是否需要中断当前线程

Thread.interrupted() 返回的是线程是否被中断过，并清除中断状态

https://ppting.me/2022/02/19/2022_02_19_Java_JUC_AQS/