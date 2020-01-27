# 草记

## green thread 这篇博客说了什么
原文程序是在x86上的一个程序、实现了协程的功能、协程这个翻译说起来可能相对多一些人更熟悉。  
  
我第一次知道协程是在课上学Unity开发游戏时学到的、但其实时C#的功能、Unity使用了C#作为脚本、作为例子说使用Unity做游戏、应用场景很有想象空间、  
## 协程
大致的描述是：  
在 **用户态**的**一个线程**内、完成了**好似**内核中的**多线程**的效果、**感觉上**是在**并行**执行任务。  
  
实际上是在一个用户态线程内、使用了类似内核中资源切换的思想、涉及栈结构、保存与恢复特性、再加上用户态线程的特性、通过迭代器来达到感觉上的并行、
但却可以更方便的控制运行逻辑。
## 事情的核心
1.知道**switch**的作用  
2.知道关键字 **yield**的作用

## switch作用
switch顾名思义、计算机中切换的思想非常核心、这涉及到栈结构、我们可以把栈看作一个范围、好比高数中的定义域，一个活动的全部要在这个范围内进行、
现在有两个活动、那么理论上应该有两个栈结构、为这两个活动提供空间。一般来说一个人只做一件事、思路很顺畅、如果做两件事、就多了一些两件事来回切换的问题、
人们常用的办法就是夹个书签、程序也是这样、这个书签的名字一般叫做**context**的结构、他来保存一些关键的信息、通过switch的动作来进行保存、  
  
原文中、是在x86上进行的、我们以此举例：  
他的context结构  
```
struct ThreadContext {
    rsp: u64,
    r15: u64,
    r14: u64,
    r13: u64,
    r12: u64,
    rbx: u64,
    rbp: u64,
}
```
那么为什么是这些结构呢、作者也说了  
> 正是这些寄存器记录我们程序的上下文：下一个的运行指令、基本指针、栈指针等等。 

那接下来我们来看下switch函数的怎么定义的  
```
unsafe fn switch(old: *mut ThreadContext, new: *const ThreadContext)
```
看上去的意思是接受两个地址参数、那么内容呢？
```
asm!("
        mov     %rsp, 0x00($0)
        mov     %r15, 0x08($0)
        mov     %r14, 0x10($0)
        mov     %r13, 0x18($0)
        mov     %r12, 0x20($0)
        mov     %rbx, 0x28($0)
        mov     %rbp, 0x30($0)

        mov     0x00($1), %rsp
        mov     0x08($1), %r15
        mov     0x10($1), %r14
        mov     0x18($1), %r13
        mov     0x20($1), %r12
        mov     0x28($1), %rbx
        mov     0x30($1), %rbp
        ret
        "
    :
    :"r"(old), "r"(new)
    :
    : "volatile", "alignstack"
    );
```
原来内容是内联汇编、主要含义是、因为寄存器是唯一的、其内容也描述着这一时刻的程序是哪里、所以动作是在重写寄存器、
把当前的寄存器的内容放回书签（context）内、把下个新的内容从书签（context）内拿出、放到寄存器内、这时寄存器内容描述的就是新的正确的位置、
这样就完成了切换、  
  
 大致意思我们知道了、稍后接下来我们将尝试把x86替换为risc-v结构、
 ## yield作用
 yield 更生动一些的说法、像是排队用勺子舀汤、一个人用完勺子、就调用yield、下一个人在等待这个勺子、那么勺子就传到他那里、他开始舀汤、其中包含了切换、  
   
 更具体的细节与含义、还是要参照代码实现、仅说这个博客范围内对yield的细节与含义
 ```
 fn t_yield(&mut self) -> bool {
        let mut pos = self.current;
        while self.threads[pos].state != State::Ready {
            pos += 1;
            if pos == self.threads.len() {
                pos = 0;
            }
            if pos == self.current {
                return false;
            }
        }

        if self.threads[self.current].state != State::Available {
            self.threads[self.current].state = State::Ready;
        }

        self.threads[pos].state = State::Running;
        let old_pos = self.current;
        self.current = pos;

        unsafe {
            switch(&mut self.threads[old_pos].ctx, &self.threads[pos].ctx);
        }
    }
 ```
可能需要花一下时间、细品一下、

## 想的通了
知道了上述的关键点、那么大概就思路上了解了、协程的运作方式、这些点只限于了解大概方式、跑起来还是要参照博客、
  
不知道这样说是否真的描述清了、协程的大概意思、如果没有、um..还请提出宝贵建议、

## switch 在 Risc-V 上应该怎么办
首先由x86-64变为riscv64、那么context内容就不一样了、应该去看riscv是怎么约定这个"书签"的  
在[这里](https://github.com/riscv/riscv-elf-psabi-doc/blob/master/riscv-elf.md#integer-calling-convention)我找到了一些信息

-------------------------------------------------------------------------
Name    | ABI Mnemonic | Meaning                | Preserved across calls?
--------|--------------|------------------------|------------------------
x0      | zero         | Zero                   | -- (Immutable)
x1      | ra           | Return address         | No
x2      | sp           | Stack pointer          | Yes
x3      | gp           | Global pointer         | -- (Unallocatable)
x4      | tp           | Thread pointer         | -- (Unallocatable)
x5-x7   | t0-t2        | Temporary registers    | No
x8-x9   | s0-s1        | Callee-saved registers | Yes
x10-x17 | a0-a7        | Argument registers     | No
x18-x27 | s2-s11       | Callee-saved registers | Yes
x28-x31 | t3-t6        | Temporary registers    | No

因此按照刚才x86的方式操作context看上去理应是这个样子
```
struct Context {
    x2:  u64,
    x8:  u64,
    x9:  u64,
    x18: u64,
    x19: u64,
    x20: u64,
    x21: u64,
    x22: u64,
    x23: u64,
    x24: u64,
    x25: u64,
    x26: u64,
    x27: u64,
}
```
类似switch应该是
```
         sd x2, 0x00($0)
         sd x8, 0x08($0)
         sd x9, 0x10($0)
         sd x18, 0x18($0)
         sd x19, 0x20($0)
         sd x20, 0x28($0)
         sd x21, 0x30($0)
         sd x22, 0x38($0)
         sd x23, 0x40($0)
         sd x24, 0x48($0)
         sd x25, 0x50($0)
         sd x26, 0x58($0)
         sd x27, 0x60($0)
 
         ld x2, 0x00($1)
         ld x8, 0x08($1)
         ld x9, 0x10($1)
         ld x18, 0x18($1)
         ld x19, 0x20($1)
         ld x20, 0x28($1)
         ld x21, 0x30($1)
         ld x22, 0x38($1)
         ld x23, 0x40($1)
         ld x24, 0x48($1)
         ld x25, 0x50($1)
         ld x26, 0x58($1)
         ld x27, 0x60($1)
         
         ret
```
这肯定是有问题的、在找问题之前、我们还需要看下x86的实现
```
unsafe {
            let s_ptr = available.stack.as_mut_ptr().offset(size as isize);
            let s_ptr = (s_ptr as usize & !15) as *mut u8;
            ptr::write(s_ptr.offset(-24) as *mut u64, guard as u64);
            ptr::write(s_ptr.offset(-32) as *mut u64, f as u64);
            available.ctx.rsp = s_ptr.offset(-32) as u64;
        }
```
这段代码表达了一些前提准备的意思  
  
首先
> let s_ptr = available.stack.as_mut_ptr().offset(size as isize);  

是把栈的首地址偏移到栈顶、然后把栈顶地址给到s_ptr
> let s_ptr = (s_ptr as usize & !15) as *mut u8;  

16字节对齐  
> ptr::write(s_ptr.offset(-24) as *mut u64, guard as u64);    

把guard函数地址写入栈顶偏移24字节处
> ptr::write(s_ptr.offset(-32) as *mut u64, f as u64);

把函数f的地址写入栈顶偏移32字节处
> available.ctx.rsp = s_ptr.offset(-32) as u64;

把栈顶偏移32字节处地址给到ctx.rsp、意思把栈顶指针偏移到原先栈-32字节处、也是f函数的地址
  
稍作分析、guard函数地址应该时返回地址、谁的返回地址、当前运行的"线程"运行完后的要去到这个地址、  
  
而f函数、是我们想执行的函数、我们希望运行它、所以应该设置pc为这个地址、  
  
这样我们在目前这个程序里要记录和设置两个地址、
  
所以在riscv64情况下、我们的context、可能会变成这样
```
struct Context {
    x1:  u64,
    x2:  u64,
    x8:  u64,
    x9:  u64,
    x18: u64,
    x19: u64,
    x20: u64,
    x21: u64,
    x22: u64,
    x23: u64,
    x24: u64,
    x25: u64,
    x26: u64,
    x27: u64,
    f  : u64,
}
```
因为在riscv里刚好提供ra寄存器、x1,又多了一个f值、是要存放f函数的地址、好把pc指向到那里来首先运行、

那么switch应该怎样的、还未去深入研究、但这时有人已经做完了、请参考rcore群内、名字叫做<协程.docx>的word文件、

之后很快实现了可以跑的riscv版本程序  
地址:https://github.com/chyyuu/rCore_tutorial/blob/greenthread/usr/rust/src/bin/greenthread.rs

## 想运行一下这个程序在riscv版本上的操作步骤

前提： 在可以运行rCorre_tutorial的环境下、在rCorre_tutorial文件夹下 [github 上可[下载](https://github.com/rcore-os/rCore_tutorial.git)]
1. 进入usr 文件夹
2. make user_img
3. 回到rCorre_tutorial文件夹下 
4. 进入os文件夹
5. make run
6. 成功运行
