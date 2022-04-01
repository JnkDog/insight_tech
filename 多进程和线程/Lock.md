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