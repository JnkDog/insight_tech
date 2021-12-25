## 开机键按钮开启后
首先进入OS后。会进入BIOS，CPU中的寄存器PC(IP) 强制被执行未为 *0xFFF0*, 同时CS(code segment)被设置为*0xF000*。实模式下，cpu取指令的操作为 CS << 4 + PC(IP) = 0xFFFF0。在这个地址中存放的是一条跳转指令（**一跳**），跳转指令后BIOS的大致步骤为检测基本的输入输出设备，最为重要的是，BIOS会把磁盘中第一扇区，512字节的数据载入到内存从*0x7c00* to *0x7dff*中，并将PC(IP)跳转到*0x7c00*处 （**二跳**）。


## 二跳后的执行分析
**总的来说，实现了实模式到保护模式的切换。保护模式的概念：**
二跳以后的代码执行可以观察boot.asm处一一对照。
```x86asm
cli # Disable interrupts  关闭中断，以后会补上
 7c00: fa cli      
cld # String operations increment  
 7c01: fc cld
  
# Set up the important data segment registers (DS, ES, SS). 
# 重要的段寄存器清零的操作
xorw    %ax,%ax             # Segment number zero  
 7c02: 31 c0 xor    %eax,%eax  
movw    %ax,%ds             # -> Data Segment  0  
 7c04: 8e d8                  mov    %eax,%ds  
movw    %ax,%es             # -> Extra Segment 0  
 7c06: 8e c0                  mov    %eax,%es  
movw    %ax,%ss             # -> Stack Segment 0  
 7c08: 8e d0                  mov    %eax,%ss


# Enable A20:  
# For backwards compatibility with the earliest PCs, physical 
# address line 20 is tied low, so that addresses higher than 
# 1MB wrap around to zero by default.  This code undoes this.seta20.1: 
# 打开A20的线，具体参考：
# https://objectkuan.gitbooks.io/ucoredocs/content/lab1/lab1_appendix_a20.html

 inb $0x64,%al               # Wait for not busy  
 7c0a: e4 64 in     $0x64,%al  
  testb $0x2,%al  
    7c0c: a8 02 test   $0x2,%al  
  jnz seta20.1  
    7c0e: 75 fa jne    7c0a <seta20.1>  
  
  movb $0xd1,%al               # 0xd1 -> port 0x64  
 7c10: b0 d1                  mov    $0xd1,%al  
  outb    %al,$0x64  
 7c12: e6 64 out    %al,$0x64
 
```

```x86asm
# Bootstrap GDT 段选择  
.p2align 2 # force 4 byte alignment  
gdt:  
  SEG_NULL                              # null seg  
  SEG(STA_X|STA_R, 0x0, 0xffffffff)     # code seg  
  SEG(STA_W, 0x0, 0xffffffff)           # data seg  
  
gdtdesc:  
  .word   0x17                          # sizeof(gdt) - 1  
  .long gdt                             # address gdt
```

gdtr寄存器的结构
共48bits
47 ～ 16  gdt的内存起始地址          .long      gdt地址    32bits   （0x7c4c）
15 ～ 0  gdt的界限（gdt的总大小）  .word  0x17         16bits
(汇编代码已经写死了位置)

```x86asm
lgdt gdtdesc  
  7c1e: 0f 01 16 lgdtl  (%esi)  
  7c21: 64 7c 0f               fs jl  7c33 <protcseg+0x1>  
movl    %cr0, %eax            # cr0 -> eax  
  7c24: 20 c0 and    %al,%al  
orl $CR0_PE_ON, %eax      # or 操作  
  7c26: 66 83 c8 01 or     $0x1,%ax  
movl    %eax, %cr0  
  7c2a: 0f 22 c0               mov    %eax,%cr0
 ```
 
 $CR0_PE_ON = 0x1,      **or** 0x1, %eax
 再将eax写入cr0中，开启分段和分页
 cr0控制是否开启分页和分段模式     PG｜PE 

**注意在GDT的内容已经在内存中**
可以利用GDB进行打印
```shell
(gdb) x/24xb 0x7c4c
0x7c4c: 0x00    0x00    0x00    0x00    0x00    0x00    0x00    0x00
0x7c54: 0xff    0xff    0x00    0x00    0x00    0x9a    0xcf    0x00
0x7c5c: 0xff    0xff    0x00    0x00    0x00    0x92    0xcf    0x00
```
段描述符的大小为64bits，即8个bytes 
其中0x7c4c是GDT初始的地址，第一段默认全为0
第二段为代码段
第三段为数据段

**Attention**
```
# $protcseg = 跳转地址
# ljmp $section, $offset
ljmp $PROT_MODE_CSEG, $protcseg

```
由于缓存和影子寄存器的存在所以不能直接转到保护模式，有可能还是在实模式下运行。所以需要进行长跳转清空缓存。因为`ljmp`指令可以使处理器清空流水线和指令预读取队列。`PROT_MODE_CSEG`，其值为`0x08`

cs寄存器中存放段选择子，但不是直白的0x1（偏移量是1），而是0x8。因为cs寄存器中记录的不单单是偏移量 ！！！第4位开始才是偏移量。具体见[Ref 1][1]





## Ref
[1] https://www.ics.uci.edu/~aburtsev/143A/2017fall/lectures/lecture07-system-boot/lecture07-system-boot.pdf 
2. 