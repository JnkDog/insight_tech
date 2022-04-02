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


这里synchronized是非公平的锁，如果一个线程释放锁，另一个新来的线程直接进行抢占，有可能会抢走这把锁，而不经过队列。

```Java
import org.junit.Test;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class LockTest {
    private static Lock fairLock = new ReentrantLockMine(true);
    private static Lock unfairLock = new ReentrantLockMine(false);

    @Test
    public void unfair() throws InterruptedException {
        testLock("非公平锁", unfairLock);
    }

    @Test
    public void fair() throws InterruptedException {
        testLock("公平锁", fairLock);
    }

    private void testLock(String type, Lock lock) throws InterruptedException {
        System.out.println(type);
        // 创建5个线程进行操作
        for (int i = 0; i < 5; i++) {
            Thread thread = new Thread(new Job(lock)){
                public String toString() {
                    return getName();
                }
            };
            thread.setName("" + i);
            thread.start();
        }
        Thread.sleep(11000);
    }

    private static class Job implements Runnable{
        private Lock lock;
        public Job(Lock lock) {
            this.lock = lock;
        }

        public void run() {
            // 每个线程加锁放锁2次
            for (int i = 0; i < 2; i++) {
                lock.lock();
                try {
                    Thread.sleep(1000);
                    System.out.println("获取锁的当前线程[" + Thread.currentThread().getName() + "], 同步队列中的线程" + ((ReentrantLockMine)lock).getQueuedThreads() + "");
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } finally {
                    lock.unlock();
                }
            }
        }
    }

    private static class ReentrantLockMine extends ReentrantLock {  //重新实现ReentrantLock类是为了重写getQueuedThreads方法，便于我们试验的观察
        public ReentrantLockMine(boolean fair) {
            super(fair);
        }

        // 公平锁获取的时候会调用这个方法,看看等待队列有没有
        @Override
        protected Collection<Thread> getQueuedThreads() {   //获取同步队列中的线程
            List<Thread> arrayList = new ArrayList<>(super.getQueuedThreads());
            Collections.reverse(arrayList);
            return arrayList;
        }
    }
}
```
输出的结果为
非公平锁
获取锁的当前线程[0], 同步队列中的线程[4, 1, 2, 3]
获取锁的当前线程[0], 同步队列中的线程[4, 1, 2, 3]
获取锁的当前线程[4], 同步队列中的线程[1, 2, 3]
获取锁的当前线程[4], 同步队列中的线程[1, 2, 3]
获取锁的当前线程[1], 同步队列中的线程[2, 3]
获取锁的当前线程[1], 同步队列中的线程[2, 3]
获取锁的当前线程[2], 同步队列中的线程[3]
获取锁的当前线程[2], 同步队列中的线程[3]
获取锁的当前线程[3], 同步队列中的线程[]
获取锁的当前线程[3], 同步队列中的线程[]
// 在第二次获取锁的时候，非公平锁大概率能直接获取，不需要进队列
公平锁
获取锁的当前线程[0], 同步队列中的线程[1, 2, 3, 4]
获取锁的当前线程[1], 同步队列中的线程[2, 3, 4, 0]
获取锁的当前线程[2], 同步队列中的线程[3, 4, 0, 1]
获取锁的当前线程[3], 同步队列中的线程[4, 0, 1, 2]
获取锁的当前线程[4], 同步队列中的线程[0, 1, 2, 3]
获取锁的当前线程[0], 同步队列中的线程[1, 2, 3, 4]
获取锁的当前线程[1], 同步队列中的线程[2, 3, 4]
获取锁的当前线程[2], 同步队列中的线程[3, 4]
获取锁的当前线程[3], 同步队列中的线程[4]
获取锁的当前线程[4], 同步队列中的线程[]
// 第二次尝试获取锁的时候，由于有个队列判断，因此放在对队列后面，公平的体现，无法抢占

Lock api是支持公平和非公平的锁

## AQS理解
AQS属性

```Java
// 头结点，你直接把它当做 当前持有锁的线程 可能是最好理解的  存在疑惑 head是个类似空节点（不存放线程信息）
private transient volatile Node head;

// 阻塞的尾节点，每个新的节点进来，都插入到最后，也就形成了一个链表
private transient volatile Node tail;

// 这个是最重要的，代表当前锁的状态，0代表没有被占用，大于 0 代表有线程持有当前锁
// 这个值可以大于 1，是因为锁可以重入，每次重入都加上 1
private volatile int state;

// 代表当前持有独占锁的线程，举个最重要的使用例子，因为锁可以重入
// reentrantLock.lock()可以嵌套调用多次，所以每次用这个来判断当前线程是否已经拥有了锁
// if (currentThread == getExclusiveOwnerThread()) {state++}
private transient Thread exclusiveOwnerThread; //继承自AbstractOwnableSynchronizer

```


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

    // 唯一一个大于0的状态，代表此线程取消争夺锁
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

这里可以简单说下 waitStatus 中 SIGNAL(-1) 状态的意思，Doug Lea 注释的是：代表后继节点需要被唤醒。也就是说这个 waitStatus 其实代表的不是自己的状态，而是后继节点的状态，我们知道，每个 node 在入队的时候，都会把前驱节点的状态改为 SIGNAL，然后阻塞，等待被前驱唤醒。这里涉及的是两个问题：有线程取消了排队、唤醒操作。其实本质是一样的，读者也可以顺着 “waitStatus代表后继节点的状态” 这种思路去看一遍源码。
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
            // 虽然此时此刻锁是可以用的，但是这是公平锁，既然是公平，就得讲究先来后到，
            // 看看有没有别人在队列中等了半天了
            if (!hasQueuedPredecessors() &&
                compareAndSetState(0, acquires)) {
                setExclusiveOwnerThread(current);
                return true;
            }
        }
        // 可重入设置
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
// CAS设置tail过程中，竞争一次竞争不到，我就多次竞争，总会排到的
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
            
            // 说明P为头节点且当前没有获取到锁，可能是被非公平锁抢占了，没抢过别人
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
// 刚刚说过，会到这里就是没有抢到锁呗，这个方法说的是："当前线程没有抢到锁，是否需要挂起当前线程？"
// 第一个参数是前驱节点，第二个参数才是代表当前线程的节点
private static boolean shouldParkAfterFailedAcquire(Node pred, Node node) {  
    // 获取头节点的状态
    int ws = pred.waitStatus;  
 if (ws == Node.SIGNAL)
    // 如果处于唤醒状态，直接返回  
    return true;  
 if (ws > 0) { 
	// 如果是取消状态
    // 前驱节点 waitStatus大于0 ，之前说过，大于0 说明前驱节点取消了排队。
    // 这里需要知道这点：进入阻塞队列排队的线程会被挂起，而唤醒的操作是由前驱节点完成的。
    // 所以下面这块代码说的是将当前节点的prev指向waitStatus<=0的节点，
    // 简单说，就是为了找个好爹，因为你还得依赖它来唤醒呢，如果前驱节点取消了排队，
    // 找前驱节点的前驱节点做爹，往前遍历总能找到一个好爹的
    do {  
        // 循环向前查找取消节点，把取消节点从列表中删了
	    node.prev = pred = pred.prev;  
	 } while (pred.waitStatus > 0);  
		 pred.next = node;  
 } else { 
        // 设置前任节点等待状态为SIGNAL
        // 仔细想想，如果进入到这个分支意味着什么
        // 前驱节点的waitStatus不等于-1和1，那也就是只可能是0，-2，-3
        // 在我们前面的源码中，都没有看到有设置waitStatus的，所以每个新的node入队时，waitStatu都是0
        // 正常情况下，前驱节点是之前的 tail，那么它的 waitStatus 应该是 0
        // 用CAS将前驱节点的waitStatus设置为Node.SIGNAL(也就是-1)，意外当前节点需要挂起来
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


## 解锁操作
```Java
public void unlock() {
    sync.release(1);
}

public final boolean release(int arg) {
    // 往后看吧
    if (tryRelease(arg)) {
        Node h = head;
        // 为什么需要判断 waitStatus != 0 见下面
        if (h != null && h.waitStatus != 0)
            unparkSuccessor(h);
        return true;
    }
    return false;
}

// 回到ReentrantLock看tryRelease方法
protected final boolean tryRelease(int releases) {
    int c = getState() - releases;
    // 如果释放锁和解锁不是同一个线程，报错
    if (Thread.currentThread() != getExclusiveOwnerThread())
        throw new IllegalMonitorStateException();
    // 是否完全释放锁
    boolean free = false;
    // 其实就是重入的问题，如果c==0，也就是说没有嵌套锁了，可以释放了，否则还不能释放掉
    if (c == 0) {
        free = true;
        setExclusiveOwnerThread(null);
    }
    setState(c);
    return free;
}

/**
 * Wakes up node's successor, if one exists.
 *
 * @param node the node
 */
// 唤醒后继节点
// 从上面调用处知道，参数node是head头结点
private void unparkSuccessor(Node node) {
    /*
     * If status is negative (i.e., possibly needing signal) try
     * to clear in anticipation of signalling.  It is OK if this
     * fails or if status is changed by waiting thread.
     */
    int ws = node.waitStatus;
    // 如果head节点当前waitStatus<0, 将其修改为0
    if (ws < 0)
        compareAndSetWaitStatus(node, ws, 0);
    /*
     * Thread to unpark is held in successor, which is normally
     * just the next node.  But if cancelled or apparently null,
     * traverse backwards from tail to find the actual
     * non-cancelled successor.
     */
    // 下面的代码就是唤醒后继节点，但是有可能后继节点取消了等待（waitStatus==1） 为什么会取消等待？
    // 从队尾往前找，找到waitStatus<=0的所有节点中排在最前面的
    Node s = node.next;
    if (s == null || s.waitStatus > 0) {
        s = null;
        // 从后往前找，仔细看代码，不必担心中间有节点取消(waitStatus==1)的情况
        for (Node t = tail; t != null && t != node; t = t.prev)
            if (t.waitStatus <= 0)
                s = t;
    }
    if (s != null)
        // 唤醒线程
        LockSupport.unpark(s.thread);
}
```
release函数中
这里的判断条件为什么是h != null && h.waitStatus != 0？

* h == null Head还没初始化。初始情况下，head == null，第一个节点入队，Head会被初始化一个虚拟节点。所以说，这里如果还没来得及入队，就会出现head == null 的情况。

* h != null && waitStatus == 0 表明后继节点对应的线程仍在运行中，不需要唤醒。 不理解

* h != null && waitStatus < 0 表明后继节点可能被阻塞了，需要唤醒。