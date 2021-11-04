# copy on writer

父进程只有在需要对内存进行修改的时候，才会copy那一页。否则是和子进程共享内存空间。这样在创建子进程的时候速度就快很多，也节省空间。

父进程进行fork后，页被标记为read-only，当某个进程写内存的时候，cpu监测到read-only flag。就会触发（page-fault），陷入kernel的一个中断历程。在其中，kernel把触发的页复制一份，所以父子进程都有独立的一份。

copy on write缺点

如果fork()后，父子进程需要继续进行写操作，那么产生大量的分页错误

