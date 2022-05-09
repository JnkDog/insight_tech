# Redis-cli 1.3.6

## 终端输入字符
```c
int main(int agrc, char **argv) {
    
}
```
argc = 多少个输入，例如./redis-cli -h 127.0.0.1 = 3
argv = 保存具体的输入信息，如argv[0] := "./redis-cli" argv[1] := "-h"

```c
# include <stdio.h>
char *fgets(char *s, int size, FILE *stream);
```
fgets() 功能是从 stream 流中读取 size 个字符存储到字符指针变量 s 所指向的内存空间。它的返回值是一个指针，指向字符串中第一个字符的地址。


## 参数解析
### IP 参数解析
```c
int anetResolve(char *err, char *host, char *ipbuf) 
{
    struct sockaddr_in sa;
    // 设置ipv4
    sa.sin_family = AF_INET;
    // 将host的 ipv4 number-and-dots 格式转换为 二进制 网络字节序列，存储在sin_addr中
    // 如果成功返回非0, 失败返回0
    if (inet_aton(host, &sa.sin_addr) == 0) {
        // 解析失败，进入 如果host是一个域名而不是ip地址的话
        struct hostent *he;
        
        he = gethostbyname(host);
        // 如果根据域名没有找到相应的he，就返回解析错误
        if (he == NULL) {
            anetSetError(err, "can't resolve: %s\n", host);
            return ANET_ERR;
        }
        // 拷贝内存
        memcpy(&sa.sin_addr, he->h_addr, sizeof(struct in_addr));
    }
    // inet_ntoa 网络序（大端）转化为实际ipv4地址
    // 解析的地址拷贝到ipbuf中 拷贝字符
    strcpy(ipbuf, inet_ntoa(sa.sin_addr));
    return ANET_OK;
}
```
PS：关于inet_aton的理解，man指令看到有意思的地方
inet_aton可以支持4种格式的ipv4地址形式 a.b.c.d a.b.c a.b a
a.b.c.d 按照一个位一个字节来划分
a.b.c a和b按照一个字节划分，c就默认成为最右边的16-bits的位数
余下的道理一样
这里的ip解析有一个十分有意思的设定，双重检测机制
* 如果host是ipv4格式，即 a.b.c.d 这种，inet_aton可以直接检测出，但是如果是域名这种，就解析不出来。
* 就需要进入第二步 gethostbyname，根据域名找对应ip，找到了即可，如果he是空代表解析失败，返回错误。
