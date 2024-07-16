## Tomcat连接池
### 原生连接池
1. task提交（这里的task指的是什么？映射到业务层次）
2. 小于corePoolSize，直接启动线程开始run
3. 如果大于等于corePoolSize，放入workQueue，线程池corePoolSize的线程周期性拉等待队列中的数据
4. 如果workQueue满了，线程池就会紧急创建新的临时线程来救场，如果总线程池达到了maxNumPoolSize，则执行handler，拒绝策略

### Tomcat扩展版本
1. 前 corePoolSize 个任务时，来一个任务就创建一个新线程。
2. 再来任务的话，就把任务添加到任务队列里让所有的线程去抢，如果队列满了就创建临时线程。
3. **如果总线程数达到 maximumPoolSize，则继续尝试把任务添加到任务队列中去。** ---> 主要不同
4. 如果缓冲队列也满了，插入失败，执行拒绝策略。

### 几个重要的参数
1. acceptCount		
The maximum queue length for incoming connection requests when all possible request processing threads are in use. Any requests received when the queue is full will be refused. The default value is 100.
也就是所有线程都已经在处理中，等待的队列也满了，新来的请求会被拒绝。这里的拒绝？how to do？

### Tomcat线程池的设置
PS：这个和数据库的关系？


### 监控这些Thread