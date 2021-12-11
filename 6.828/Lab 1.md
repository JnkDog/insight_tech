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
47 ～ 16  gdt的内存起始地址          .long      gdt地址    32bits
15 ～ 0  gdt的界限（gdt的总大小）  .word  0x17         16bits