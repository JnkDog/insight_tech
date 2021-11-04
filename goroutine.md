**主线程退出，附属goroutine中断**

利用 wait group进行同步



如何从通道中拿值

```go
obj, ok := <- channel
// 如果channel关闭，ok为false
// 放进channel
channel <- obj
```

用range 从channel有空间的地方取数，必须要close(ch) 先