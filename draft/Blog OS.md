# CPU Exceptions

On x86 there are about 20 different CPU exception types

## Key Exception Type

Page Fault
Invalid Opcode
General Protection Fault
Double Fault
Triple Fault

## The Interrupt Descriptor Table

### Descriptor 描述符

## The Interrupt Calling Convention 中断调用协定

### Preserved and Scratch Registers 函数寄存器数据保存协定

### The Interrupt Stack Frame 中断栈帧

## Implementation

1、IDT 的初始化  
2、在IDT 注册错误类型  
3、对应实现注册错误类型的函数实现
4、加载IDT
* idt 应为静态全局变量 期望对于程序的完整运行时有效 并且unsafe 
* 懒加载：第一次引用时宏执行初始化、而不是static在编译时求值 
