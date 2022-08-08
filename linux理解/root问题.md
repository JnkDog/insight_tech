# root问题
## 问题详情
想使用goland连接到parallel中的虚拟机，开了22端口后怎么连都连不上。

## 解决
现在shell中尝试用户切换
```shell
su root
```
结果发现输入进入虚拟机的密码是验证失败。后来发现原来是root密码刚进入是没有的。
需要
```shell
sudo passwd
```
进行密码输入，然后切成su root 就可以进入root模式
但是通过goland还是登陆不成功，需要对 /etc/ssh/sshd_config 配置文件进行修改。
然后进行ssh的重启，就可以成功了！
