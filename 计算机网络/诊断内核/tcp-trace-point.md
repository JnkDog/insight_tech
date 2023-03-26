# 使用
```shell
$ cd /sys/kernel/debug/tracing/events/
$ echo 1 > tcp/tcp_retransmit_skb/enable
$ cat trace_pipe
```

## tcpretrans
```shell
$ sudo tcpretrans -p 80
```

