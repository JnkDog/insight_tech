# SDS 数据结构

## 1.3.6的封装
```c
struct sdshdr {
    long len;
    long free;
    char buf[];
};
```
定义在sds.h中，在计算头大小的时候，sizeof(sdshdr) 长度为16，2个long类型 8+8，char buf[]不计算,为什么呢？
You can only have one flexible array member in a struct, and it must always be the last member of the struct. In other words, in this case you've gone wrong before you call malloc, to the point that there's really no way to call malloc correctly for this struct.

char buf[]长度不知道，所以编译器默认不分配空间，malloc需要自己定义空间长度。而且只能有一个flexiable的成员

在分配buf[]空间的时候，需要注意 +1，例如 "get" 长度为3，计算出后buf的长度为 3 + 1 = 4，末尾加 '\0'
这个结构体分配在堆上面！！！

在得到buf的指针的时候 例如 char *s = buf;
可以推出len的长度

```c
size_t sdslen(const sds s) {
    // 计算sds结构体头部指针
    struct sdshdr *sh = (void*) (s-(sizeof(struct sdshdr)));
    return sh->len;
}
```
以 "get" sds 为例子，在gdb中解析
```shell
(gdb) x/24xb (s - (sizeof(struct sdshdr)))
0x55555555faf8: 0x03    0x00    0x00    0x00    0x00    0x00    0x00    0x00
0x55555555fb00: 0x00    0x00    0x00    0x00    0x00    0x00    0x00    0x00
0x55555555fb08: 0x67    0x65    0x74    0x00    0x00    0x00    0x00    0x00
```
0x55555555faf8 处存放了长度 3 0x0000000000000003 long 类型
0x55555555fb08 存放了3个字符 ascii get，刚好对应

### 关于sds扩容
```c
static sds sdsMakeRoomFor(sds s, size_t addlen) {
    struct sdshdr *sh, *newsh;
    // 剩余可用空间
    size_t free = sdsavail(s);
    size_t len, newlen;

    // 如果还可以使用就直接返回，不用扩容
    if (free >= addlen) return s;
    len = sdslen(s);
    sh = (void*) (s-(sizeof(struct sdshdr)));
    // free空间不够，扩大char buf[] 的容量
    newlen = (len+addlen)*2;
    newsh = zrealloc(sh, sizeof(struct sdshdr)+newlen+1);
#ifdef SDS_ABORT_ON_OOM
    if (newsh == NULL) sdsOomAbort();
#else
    if (newsh == NULL) return NULL;
#endif

    newsh->free = newlen - len;
    return newsh->buf;
}
```