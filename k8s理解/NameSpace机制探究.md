# NameSpace机制探究
NS机制涉及过多，先从进程模块开始。进程在Linux中的表现形式是一个task结构体。
```C
struct task_struct {
    pid_t pid;    // 全局唯一 
    pid_t tgid;   // 全局唯一
    ......
    /* namespaces */
    struct nsproxy *nsproxy;
    struct pid_link pids[PIDTYPE_MAX]; // 指向不同的pid类型，具体分析见下面
    ......
}
```
保存的是一个nsproxy指针，长这样
```C
struct nsproxy {
	atomic_t count; // 关联该结构体的task_struct数量
	struct uts_namespace *uts_ns; //uts命名空间
	struct ipc_namespace *ipc_ns; //ipc命名空间
	struct mnt_namespace *mnt_ns; //mnt命名空间
	struct pid_namespace *pid_ns; //pid命名空间
	struct net 	     *net_ns; //网络相关的命名空间的数量
}
```
这里需要注意，如果一个命名空间不一致或者新的命名空间产生，nsproxy将会重新copy一份。
PID命名空间是按照层次组织的，当我们在新复制一个进程时，都会设置是否新建一个命名空间的标志位。新建的命名空间中的所有PID对父命名空间都是可见的，但是子命名空间却无法看到父命名空间。为什么会这样呢，原来在建立新的命名空间的时候，新命名空间的所有PID都会在父命名空间建立一个它的映射，有了这个映射，父命名空间就可以看到子命名空间的PID啦。父子命名空间的层次结构图如下：

![](./pictures/pid.png)

这种层级可以看到有2种id，一种全局，一种局部。
全局id就是PID，唯一性。在task_struct中pid，tgid是唯一的。
局部ID：只属于一个命名空间，其局部ID也只有在该命名空间里面有效。
从这里也可以看出这个这个is_global_init()函数判断的是全局id唯一性

```C
// sched.h
static inline int is_global_init(struct task_struct *tsk)
{
	return task_tgid_nr(tsk) == 1;
}

// 这里_nr后缀代表number？ 还是 number reference？
static inline pid_t task_tgid_nr(struct task_struct *tsk)
{
	return tsk->tgid;
}
```

既然直接展示的是pid， tgip，那么在进程在不同命名空间中呈现不同的pid又是怎么样实现的呢？

现在来看看pid_t到底是什么组成的
```C
#ifndef __kernel_daddr_t
typedef int		__kernel_daddr_t;
#endif

typedef __kernel_pid_t		pid_t;
```
本质是个int类的整形

看下linux的解决思路，以下是有关的数据结构
```C
// 一个小技巧，前三个是PID_TYPE，最后代表TYPE的个数，这样根据enum性质推出TYPE个数。
// 以后即使要添加种类也不需要大改代码！ 优雅，真的优雅！！！
// 以下的类型都是namespace下的，别和全局id pid_t 搞混了，pid_t就是个整数类型（具体得从源码确定）
enum pid_type
{
    PIDTYPE_PID,   // PID 
    PIDTYPE_PGID,  // PGID 进程组编号
    PIDTYPE_SID,   // SID  会话组编号
    PIDTYPE_MAX
};

// namespace核心
struct upid {
    int nr;  // 当前pid_namespace的pid编号
    struct pid_namespace *ns; // 指向当前pid_namespace
    struct hlist_node pid_chain; // hash冲突时候的链表法
};

struct pid {
    atomic_t count;
    struct hlist_head tasks[PIDTYPE_MAX];  // 
    struct rcu_head rcu;        // race condition
    unsigned int level;         // 命名空间一共有几层
    struct upid numbers[1];     // 未确定空间大小的upid数组 由于该数组位于结构的末尾，因此
                                // 只要分配更多的内存空间，即可向数组添加附加的项。
};

struct pid_link {
    struct hlist_node node;
    struct pid *pid;      // 指向一个pid结构体的指针
};
```
先来看看hlist_node和hlist_head是什么？一个双向链表
```C
struct hlist_head {
	struct hlist_node *first;
};

struct hlist_node {
	struct hlist_node *next, **pprev;
};
```
![](./pictures/hlist.png)
现在问题是为什么pprev需要设计成为一个指针的指针。
只需要在删除的时候操作指针就可以了，不需要对头节点进行特批，也是一个小技巧。毕竟头节点也只是一个hlist_node的指针

下面看看如何进行具体的查找
![](./pictures/search.png)

其中task_struct中的结构体里的pid_link中的pid指向一个pid结构体
pid结构体中的upid数组存储着不同命名空间下的pid编号，同时指向相应的编号的命名空间
这就完事了！
```C
pid_t pid_nr_ns(struct pid *pid, struct pid_namespace *ns)
{
    struct upid *upid;
    pid_t nr = 0;
    if (pid && ns->level <= pid->level) { // 需要 <= pid->level 
        upid = &pid->numbers[ns->level];
        if (upid->ns == ns)
        nr = upid->nr;
    }
    return nr;
}
```
因为父命名空间可以看到子命名空间中的PID，反过来却不行，内核必须确保当前命名空间的level
小于或等于产生局部PID的命名空间的level。 提一句，如果这个进程没在这个空间创建的意思？估计是这个用处，待确定，需要探究pid->level到底是代表什么？

这是从task_struct角度上寻找，如果从pid反推出task_struct呢？
先吧pid进行hash上查找，找到hlist_node后，挨个遍历比较nr，然后找到对应的hlist_head，进行反查task_struct
