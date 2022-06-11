| CISC                                | RISC                                     |
| ----------------------------------- | ---------------------------------------- |
| object code少，一条指令包含多条操作 | object code多，一条指令代表唯一的功能    |
|                                     | 寄存器多，可以保存更多的中间变量         |
|                                     | instruction cache 缓存指令               |
|                                     | 减少CPI（流水线和其他并行的技术）        |
|                                     | 指令集被设计利于流水线的进行和减少stalls |
|                                     | critical path 少，时钟周期快                           |
|                                     |                                          |
l                                    |                                          |

寄存器重命名技术可以消除WAR和WAW冒险
Tomasulo算法中由保留站提供。

2020
1. Give three reasons that a pipeline will achieve a speedup factor which is less than the number of stages (2e)

   * Every clock cycle needs to be longer (by a small safety factor) than the delay on the critical path, to allow for minor variations (for example, tiny manufacturing defects, etc.). That means that if retiming has been used, an extra safety factor has been introduced.
   *  Every instruction needs to go through all stages, not just the relevant ones. The number of stages needs to accomodate the most complex instruction; therefore the simpler instructions (such as RRR) will be less efficient.
   *  Data hazards will occur from time to time, resulting in pipeline stalls.
   *  different stages may have different path depths but all have to be clocked at the speed of the slowest. 
3. 

2019
reservation stations
busy bits                 3合一解释2.  functional unit的理解 （1c）
3.  中断的程序处理 （2a）
4.  组相连的cache （3a）
5.  bypassing的解释 （3b）
6.  WAW的解释以及如何解决（3d）
7.  流水线的执行以及为什么加速小于stage （4a）
8.  Common data bus 的解释。（4b）
9.   Synchronizer circuit 的解释。（4c）
10.   foldr 和 scanf function 解释 （4d）

2016
1. RISC速度快的原因 （1a）
2. sigma16数组和指针的数值访问产生过程 （1b）
3. critical path的解释 ！！！！ （1c）抄！！！
4. retiming  （2b iii）
5. interleveled memory 的理解和解释 （3a）
6. functional unit 的过程和对比AlU（3d）
7. superscalar和pipeline的对比和解释 （4a）
8. metastable的解释  metastable signal （4c）  2014 2c
9. binary add。scan等解释（4d）

2015
1. 寄存器个数k的确认 （1c）
2. carry位放在R15的优点（2c）
3. common data bus (4b)
4. 同步和异步电路的区别。（4c）
5. 用户态和内核态的理解（特权指令相关）。（4d）

2014
1. 布尔值比较的结果存放。（1a）
2. 虚拟机解释 （1d）
3. 乘法在不同部件实现的优点 （1b）
4. GALS。global asynchronous， local synchromc的解释 （4c）
5. circuit parallelism 的理解和应用 （4d）

2013
1. synchronic 电路的理解 （1d）
2. time complexity的理解 （2c）
3. mul 用时序加组合电路实现的优缺点 （2d）
4. associative memory的理解。（3a）   TLB
5. conditional。jump 的过程（3b）
6. reservation station 的理解。（4b）
7. 程序变快的原因 的 5个例子 （4c）
8. 举例子  串行的方式计算x的最大值 （4d）

2012   贼难
1. Explain how a suitable clock speed (1d)

2010
1. 变长指令和固定指令 （1d）
2. never execute a privileged instruction 	（1e）
3. control和datapath   (1) Simplifies design through divide and conquer, as the datapath and control are typically of similar complexity. (2) The control is specified naturally as an algorithm with the structure of an interpreter, so it can be designed similarly to software. (3) There are several different ways to synthesise a control circuit from a control algorithm, so expressing the control as an algorithm keeps the designer’s options open. 
4. synchroniser 的 解释 （2e）
5. RT level (register transfer level),  （3b）
6. Explain how interrupts are implemented by the control algorithm of a processor. （3 d）
7. CDB and interrupt cause problem  （等待CDB和功能单元的清空）

2009
1. The M1 control algorithm increments the pc register immediately on loading an instruction into the ir。 （多了一个周期 RX指令）
2. a three-port register file is able to load a register and read out two registers simultaneously （为什么寄存器可以读2个输出一个）
3. Describe three factors that limit the amount of parallelism that can be exploited on a shared memory parallel system.  （共享内存设计失败的地方  treadeoff）

2008
1. features that might be found in an architecture targeted for high level programming languages  
2. In a RAW hazard, the pipeline would need to stall to prevent the wrong data from being read. However, the new register value may already be in the processor when needed, it just hasn’t yet been loaded into the destination register. Therefore the control detects this by examining the destination and source registers of the consecutive register instructions, and it can effect the bypassing by setting control signals so that the result goes directly from the ALU to the place the data is being read. （bypassing。fowarding技术）
3.   第二大题求解为什么需要同步时许电路

2007
1. A control algorithm specifies the functionality but not the structure of the control circuit. It is written as a piece of software (or firmware). There are many different methods for generating a circuit from the algorithm. Advantages of this separation include: it’s easier to change the algorithm than the circuit; the synthesis method can be chosen for efficiency, taking into account whichever cost model is suitable; optimisations can be performed by software that change the structure of the circuit, and which would change completely if the algorithm is modified even slightly; the algorithm is easier to understand and verify than the circuit.   （control 和 datapath分离设计的优点）
2.  schematic 设计的特点
3.  添加interrupt 需要什么样子的机制

 ** The speed of program execution depends on the clock speed and the average number of cycles per instruction; it does not depend on the number of instructions. **