# 记录下踩过的坑
## shell脚本启动
启动zkServer.sh脚本的时候，3.5版本以后

```Shell
# 不要使用sh启动会报错
sh zkServer.sh start 
# 改用bash或者./
bash zkServer.sh start 
./zkServer.sh
```