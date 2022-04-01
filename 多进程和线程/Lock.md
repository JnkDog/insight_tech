# Lock
## Lock 和 synchronized
Lock是一个接口，synchronized是一个关键字
Java中的大部分同步类（Lock、Semaphore、ReentrantLock等）都是基于AbstractQueuedSynchronizer（简称为AQS）实现的。
其中Lock提供的几个api可以避免死锁

```Java
void lock();  // 简单获取锁 如果锁被其他线程获取，则进行等待

boolean tryLock(); // 尝试获取锁，如果获取成功返回true，否则false

boolean tryLock(long time, TimeUnit unit) throws InterruptedException; // 一段时间内没有获取锁，没进入阻塞，返回个错误

// 在锁上等待，直到获取锁，但是会响应中断，这个方法优先考虑响应中断，而不是响应锁的普通获取或重入获取。
void lockInterruptibly() throws InterruptedException;  // 支持中断的api，t1.interrupt();后释放锁
```

![](./pictures/%E9%94%81%E6%AF%94%E8%BE%83.png)


## AQS理解



ReentrantLock的底层就是由AQS来实现的
AQS 框架实际上是模板方法的一种体现，AQS 定义好主流程并实现大部分方法，子类实现特定方法后便可以完成加锁和解锁操作。

AQS中等待队列是核心，等待队列的底层实现是双向队列
![](./pictures/AQS%E9%98%9F%E5%88%97.png)

单个Node的结构
```Java
static final class Node {
    // 每个节点分为独占模式节点和共享模式节点，分别适用于独占和共享锁
    static final Node SHARED = new Node();
    static final Node EXCLUSIVE = null;

    // 唯一一个大于0的状态
    static final int CANCELLED =  1;
    // 后面节点被挂起，不包括本身节点
    static final int SIGNAL    = -1;

    static final int CONDITION = -2;

    static final int PROPAGATE = -3;

    volatile int waitStatus; // 等待状态

    volatile Node prev;

    volatile Node next;

    volatile Thread thread;   // 当前等待线程

    Node nextWaiter;

    /**
        * Returns true if node is waiting in shared mode.
        */
    final boolean isShared() {
        return nextWaiter == SHARED;
    }

    /**
        * Returns previous node, or throws NullPointerException if null.
        * Use when predecessor cannot be null.  The null check could
        * be elided, but is present to help the VM.
        *
        * @return the predecessor of this node
        */
    final Node predecessor() {
        Node p = prev;
        if (p == null)
            throw new NullPointerException();
        else
            return p;
    }

    /** Establishes initial head or SHARED marker. */
    Node() {}

    /** Constructor used by addWaiter. */
    Node(Node nextWaiter) {
        this.nextWaiter = nextWaiter;
        THREAD.set(this, Thread.currentThread());
    }

    /** Constructor used by addConditionWaiter. */
    Node(int waitStatus) {
        WAITSTATUS.set(this, waitStatus);
        THREAD.set(this, Thread.currentThread());
    }

    /** CASes waitStatus field. */
    final boolean compareAndSetWaitStatus(int expect, int update) {
        return WAITSTATUS.compareAndSet(this, expect, update);
    }

    /** CASes next field. */
    final boolean compareAndSetNext(Node expect, Node update) {
        return NEXT.compareAndSet(this, expect, update);
    }

    final void setPrevRelaxed(Node p) {
        PREV.set(this, p);
    }

    // VarHandle mechanics
    private static final VarHandle NEXT;
    private static final VarHandle PREV;
    private static final VarHandle THREAD;
    private static final VarHandle WAITSTATUS;
    static {
        try {
            MethodHandles.Lookup l = MethodHandles.lookup();
            NEXT = l.findVarHandle(Node.class, "next", Node.class);
            PREV = l.findVarHandle(Node.class, "prev", Node.class);
            THREAD = l.findVarHandle(Node.class, "thread", Thread.class);
            WAITSTATUS = l.findVarHandle(Node.class, "waitStatus", int.class);
        } catch (ReflectiveOperationException e) {
            throw new ExceptionInInitializerError(e);
        }
    }
}
```

## 梳理加锁流程
等待状态

![[waitstatus.png]]


这里以公平锁为例子

公平锁的实现是基于抽象类 **Sync** ,这里可以get到一些设计模式的思维方式，核心步骤父类实现，具体实现细节子类实现

```Java
abstract static class Sync extends AbstractQueuedSynchronizer {
    abstract void lock();
    // 。。。
}

// 非公平锁
static final class NonfairSync extends Sync {
    private static final long serialVersionUID = 7316153563782823691L;
    
    final void lock() {
        // 直接进行抢锁操作，成功就返回，不走AQS队列，非公平的体现
        if (compareAndSetState(0, 1))
            setExclusiveOwnerThread(Thread.currentThread());
        else
            acquire(1);
    }

    protected final boolean tryAcquire(int acquires) {
        return nonfairTryAcquire(acquires);
    }
}

// 公平锁
static final class FairSync extends Sync {
    private static final long serialVersionUID = -3000897897090466540L;

    final void lock() {
        acquire(1);
    }
	
    // 尝试加锁
    protected final boolean tryAcquire(int acquires) {
        final Thread current = Thread.currentThread();
        int c = getState();
        if (c == 0) {
            // 多了一个判断，和非公平锁比较
            if (!hasQueuedPredecessors() &&
                compareAndSetState(0, acquires)) {
                setExclusiveOwnerThread(current);
                return true;
            }
        }
        else if (current == getExclusiveOwnerThread()) {
            int nextc = c + acquires;
            if (nextc < 0)
                throw new Error("Maximum lock count exceeded");
            setState(nextc);
            return true;
        }
        return false;
    }
}
```



公平锁加锁的时候，直接调用AQS的方法

```java
public final void acquire(int arg) {
    // tryAcquire(arg) 成功，直接返回 （FairSync实现的）
    // 失败就调用addWaiter，线程加入到等待队列中,并调用acquireQueued方法
    if (!tryAcquire(arg) &&
        acquireQueued(addWaiter(Node.EXCLUSIVE), arg))
        selfInterrupt();
}

 private Node addWaiter(Node mode) {
     Node node = new Node(Thread.currentThread(), mode);
     // Try the fast path of enq; backup to full enq on failure
     Node pred = tail;
     // 先用cas入队
     if (pred != null) {
         node.prev = pred;
         if (compareAndSetTail(pred, node)) {
             pred.next = node;
             return node;
         }
     }
     // 失败用这个，开销大
     enq(node);
     return node;
 }
```

调试的时候需要注意，如果断点类型是all，那么全部线程都卡在那里了，stop the world，修改成thread

为了进一步理解AQS，采用JDK8版本的程序写了一个代码来检测

```java
import java.util.concurrent.locks.ReentrantLock;

public class Main extends Thread {
    final static ReentrantLock lock = new ReentrantLock(true);

    public Main(String name) {
        super(name);
    }

    @Override
    public void run() {
        lock.lock(); // 断点处，注意设置suspend为thread
        try {
            System.out.println(Thread.currentThread().getName());
            sleep(100000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            lock.unlock();
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Main main1 = new Main("thread" + 1);
        Main main2 = new Main("thread" + 2);
        Main main3 = new Main("thread" + 3);

        main1.start();
        main2.start();
        main3.start();
    }
}

```

操作过程中，可以先选择一个thread1先执行到lock方法后面。由于是第一次加锁，不需要初始化AQS队列，又是一种懒加载的方法。

thread2再尝试进行加锁，由于已经被thread1加锁成功，thread2就需要进行AQS初始化。刚开始AQS队列为空，进入enq()方法。

由于是空节点需要进行初始化，再次进入循环进行节点插入尾部。

```java
// 自选状态
private Node enq(final Node node) {
    for (;;) {
        Node t = tail;
        // 第一次初始化
        if (t == null) { // Must initialize
            if (compareAndSetHead(new Node()))
                // 空头节点 
                tail = head;
        } else {
            node.prev = t;
            // CAS操作，更新尾节点为新加入的node
            // compareAndSetTail 只是修改了tailOffest内存中的值为Node引用
            if (compareAndSetTail(t, node)) {
                t.next = node;
                return t;
            }
        }
    }
}


/**
 * CAS tail field. Used only by enq.
 */
private final boolean compareAndSetTail(Node expect, Node update) {
    return unsafe.compareAndSwapObject(this, tailOffset, expect, update);
}
```

在插入成功后，进入acquireQueued（final Node node,  int arg）的函数。进入自旋状态等待拿锁。

```java
final boolean acquireQueued(final Node node, int arg) {
	// 标记是否成功拿到资源
    boolean failed = true;
    try {
	    // 标记是否中断
        boolean interrupted = false;
		// 也是个自旋锁，要么获取到锁，要么中断
        for (;;) {
            // 活得前驱节点
            final Node p = node.predecessor();
            // 前一节点是头节点，头节点是什么都不存的节点。意味着当前节点是逻辑上的首节点
            // 进行一次获取锁操作，这个又是调用到ReentrantLock
            if (p == head && tryAcquire(arg)) {
                setHead(node);   // 操作成功后，直接把当前节点设置成头节点
                p.next = null; // help GC 原始的头节点没有任何意义
                failed = false;
                return interrupted; // 返回程序过程中是否被中断
            }
            
            // 说明P为头节点且当前没有获取到锁，可能是被非公平锁抢占了
            // 或者p不为头节点，要判读当前node是否被阻塞，防止无限循环
            
            // 将当前节点的前驱节点等待设置为SIGNAL，如果失败就开启下一轮循环
            // 直到成功
            if (shouldParkAfterFailedAcquire(p, node) &&
                parkAndCheckInterrupt())
                interrupted = true; // 设置中断状态
        }
    } finally {
        if (failed)
            cancelAcquire(node);
    }
}

// 传入前驱节点和当前节点，靠前驱点判断是不是需要阻塞
private static boolean shouldParkAfterFailedAcquire(Node pred, Node node) {  
    // 获取头节点的状态
    int ws = pred.waitStatus;  
 if (ws == Node.SIGNAL)
    // 如果处于唤醒状态，直接返回  
    return true;  
 if (ws > 0) { 
	 // 如果是取消状态
    do {  
        // 循环向前查找取消节点，把取消节点从列表中删了
	    node.prev = pred = pred.prev;  
	 } while (pred.waitStatus > 0);  
		 pred.next = node;  
 } else { 
	  // 设置前任节点等待状态为SIGNAL
      compareAndSetWaitStatus(pred, ws, Node.SIGNAL);  
 }  
    return false;  
}

private final boolean parkAndCheckInterrupt() {  
    LockSupport.park(this);   // 挂起线程直接进入阻塞状态。
	return Thread.interrupted();  // 被中断返回true
}

```

一个流程图可以用来描述
![[队列中锁获取.png]]
这张图可以看出来出循环的唯一状态是前置节点是头节点，且当前线程获取锁成功。为了防止cpu空转，（自旋锁弊端），会根据前驱节点的状态来决定是否要把线程刮起来。
![[节点挂起.png]]
这里引申出了新的问题，取消节点是怎么生成的。为什么需要把节点waitStatues设置成-1
又是在什么时候释放节点通知被挂起线程

cancel状态是怎么生成的 
