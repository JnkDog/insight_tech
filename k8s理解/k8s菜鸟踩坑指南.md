# 一个虚拟机重启后，kubelet启动有问题的解决方法
## 背景
重启worker node后，kubectl报错显示`The connection to the server localhost:8080 was refused - did you specify the right host or port?`。同时kubelet报错显示 `E0317 16:59:12.813688  126081 server.go:302] "Failed to run kubelet" err="failed to run Kubelet: misconfiguration: kubelet cgroup driver: \"cgroupfs\" is different from docker cgroup driver: \"systemd\""`。
## 解决方法
1. 看报错像是配置异常导致的，一个cgroup用了systemd，另一个用了cgroupfs
```json
// root@worker:/etc/docker# cat daemon.json
// 这里确实是systemd
{
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  },
  "storage-driver": "overlay2"
}
```
2. 尝试修改下配置看下吧

修改完就好了。。。真是稀奇古怪的fix 