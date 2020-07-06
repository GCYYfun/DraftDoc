# x86_64

## 目录结构
```
x86_64                    // 仓库根目录
    ├── src                 // 代码
    │   ├── asm               // 
    │   ├── instructions      // 
    │   ├── register          //     
    │   ├── structures        //   
    │   │   ├── paging          //  
    │   │   ├── gdt.rs          //  
    │   │   ├── idt.rs          //  
    │   │   ├── mod.rs          //  
    │   │   ├── port.rs         //      
    │   │   └── tss.rs          // 
    │   ├── addr.rs           // 
    │   └── lib.rs            //     
    ├── testing             // 测试
    |···
    └── README.md
    ···
```

## Key Point

### src/registers

#### control.rs

读写控制寄存器的功能

/// 各种控制标志修改了CPU的基本操作  
Cr0、  
/// 当发生页面错误时，CPU将该寄存器设置为访问的地址   
Cr2、  
/// 包含第4级页表的物理地址  
Cr3、  
/// 处于保护模式时，各种控制标志会修改CPU的基本操作  
Cr4

#### rflags.rs

读写标志寄存器  

处理器状态存储在RFLAGS寄存器中  
RFlags、  

### src/strutures

#### port.rs
访问I/O端口的 Traits

端口读
```
/// A helper trait that implements the read port operation.
///
/// On x86, I/O ports operate on either `u8` (via `inb`/`outb`), `u16` (via `inw`/`outw`),
/// or `u32` (via `inl`/`outl`). Therefore this trait is implemented for exactly these types.
pub trait PortRead {
    /// Reads a `Self` value from the given port.
    ///
    /// ## Safety
    ///
    /// This function is unsafe because the I/O port could have side effects that violate memory
    /// safety.
    unsafe fn read_from_port(port: u16) -> Self;
}
```

端口写
```
/// A helper trait that implements the write port operation.
///
/// On x86, I/O ports operate on either `u8` (via `inb`/`outb`), `u16` (via `inw`/`outw`),
/// or `u32` (via `inl`/`outl`). Therefore this trait is implemented for exactly these types.
pub trait PortWrite {
    /// Writes a `Self` value to the given port.
    ///
    /// ## Safety
    ///
    /// This function is unsafe because the I/O port could have side effects that violate memory
    /// safety.
    unsafe fn write_to_port(port: u16, value: Self);
}
```

端口读和写
```
/// A helper trait that implements the read/write port operations.
///
/// On x86, I/O ports operate on either `u8` (via `inb`/`outb`), `u16` (via `inw`/`outw`),
/// or `u32` (via `inl`/`outl`). Therefore this trait is implemented for exactly these types.
pub trait PortReadWrite: PortRead + PortWrite {}
```
