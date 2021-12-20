# zCore Porting

## 入口

/zCore/src/platform/riscv/entry.rs

rust_main()

再此 之前 linker64.ld 和 entry64.asm 

## 添加 unmatched.asm

在 /zCore/src/platform/riscv/boot 目录下

创建 boot_unmatched.asm

内容为

```asm

.equ PHY_MEM_OFS, 0xffffffff00000000

	.section .data
	.align 12 #12位对齐
boot_page_table_sv39:
	#1G的一个大页: 0x00000000_80000000 --> 0x80000000
	#1G的一个大页: 0xffffffff_80000000 --> 0x80000000

	#前510项置0
	.zero 8
	.zero 8
	.quad (0x80000 << 10) | 0xef #0x80000000 --> 0x80000000

	.zero 8 * 507
	#倒数第二项，PPN=0x80000(当转换为物理地址时还需左移12位), 标志位DAG_XWRV置1
	.quad (0x80000 << 10) | 0xef
	.zero 8


```

## 添加 unmatched 的 地址空间信息

在  /zCore/src/platform/riscv/const.rs 里 

添加 unmatched 信息

把 

```rust
cfg_if! {
    if #[cfg(feature = "board-qemu")] {
        pub const KERNEL_OFFSET: usize = 0xFFFF_FFFF_8000_0000;
        pub const PHYS_MEMORY_BASE: usize = 0x8000_0000;
    } else if #[cfg(feature = "board-d1")] {
        pub const KERNEL_OFFSET: usize = 0xFFFF_FFFF_C000_0000;
        pub const PHYS_MEMORY_BASE: usize = 0x4000_0000;
    }
}
```
修改为

```rust
cfg_if! {
    if #[cfg(feature = "board-qemu")] {
        pub const KERNEL_OFFSET: usize = 0xFFFF_FFFF_8000_0000;
        pub const PHYS_MEMORY_BASE: usize = 0x8000_0000;
    } else if #[cfg(feature = "board-d1")] {
        pub const KERNEL_OFFSET: usize = 0xFFFF_FFFF_C000_0000;
        pub const PHYS_MEMORY_BASE: usize = 0x4000_0000;
    } else if #[cfg(feature = "board-unmatched")] {
        pub const KERNEL_OFFSET: usize = 0xFFFF_FFFF_8000_0000;
        pub const PHYS_MEMORY_BASE: usize = 0x8000_0000;
    }
}
```

## 添加 新建 的 boot_matched.asm 到 zcore

在 /zCore/src/platform/riscv/const.rs 里 加入 asm文件

把 

```rust
#[cfg(feature = "board-qemu")]
global_asm!(include_str!("boot/boot_qemu.asm"));

#[cfg(feature = "board-d1")]
global_asm!(include_str!("boot/boot_d1.asm"));

global_asm!(include_str!("boot/entry64.asm"));
```


修改为

```rust
#[cfg(feature = "board-qemu")]
global_asm!(include_str!("boot/boot_qemu.asm"));

#[cfg(feature = "board-d1")]
global_asm!(include_str!("boot/boot_d1.asm"));

#[cfg(feature = "board-unmatched")]
global_asm!(include_str!("boot/board_unmatched.asm"));

global_asm!(include_str!("boot/entry64.asm"));
```

## 在 cargo.toml 里 添加 feature

在 /zCore/Cargo.toml 里 [features] 一项 下面 添加

```toml
board-unmatched = ["link-user-img"]
```


## 修改 makefile

在 /zCore/Makefile

找到 __################ QEMU options ################__

在 __else ifeq ($(ARCH), riscv64)__ 下 修改 

把

```Makefile
else ifeq ($(ARCH), riscv64)
  qemu_opts += \
                -machine virt \
                -bios default \
                -m 512M \
                -no-reboot \
                -no-shutdown \
                -serial mon:stdio \
                -drive format=qcow2,id=userdisk,file=$(qemu_disk) \
                -device virtio-blk-device,drive=userdisk \
                -kernel $(kernel_img) \
                -initrd $(USER_IMG) \
                -append "LOG=$(LOG)"
endif
```

改为

```Makefile
else ifeq ($(ARCH), riscv64)
    ifeq ($(PLATFORM), qemu)
        qemu_opts += \
		-machine virt \
		-bios default \
		-m 512M \
		-no-reboot \
		-no-shutdown \
		-serial mon:stdio \
		-drive format=qcow2,id=userdisk,file=$(qemu_disk) \
		-device virtio-blk-device,drive=userdisk \
		-kernel $(kernel_img) \
		-initrd $(USER_IMG) \
		-append "LOG=$(LOG)"
	endif
	ifeq ($(PLATFORM), unmatched)
        qemu_opts := \
		-machine sifive_u \
		-smp 5 \
		-bios default \
		-m 512M \
		-append "LOG=$(LOG)" \
		-initrd $(USER_IMG) \
		-kernel $(kernel_img)
    endif

endif
```

在 makefile 末尾 追加

```makefile
unmatched:
	gzip -9 -cvf $(build_path)/zcore.bin > $(build_path)/zcore.bin.gz
	mkimage -A riscv -O linux -C gzip -T kernel -a 80200000 -e 80200000 -n "zCore-unmatched" -d $(build_path)/zcore.bin.gz $(build_path)/zcore-unmatched
	@echo 'Build zcore unmatched image done'

```

## qemu运行

在 项目 根目录下 运行
```sh
make riscv-image
```
然后 执行 

```sh
cd zCore

make run ARCH=riscv64 LINUX=1 PLATFORM=unmatched MODE=release
```

## 真机 运行 

执行 完 qemu运行 确认 成功 

运行

make unmatched ARCH=riscv64 LINUX=1 PLATFORM=unmatched MODE=release


然后 会在 /target/riscv64/release/ 目录下 生成 zcore-unmatched 文件 


把这个zcore-unmatched  文件 复制放入 unmatched 自带 的 sd卡的 boot 分区下

然后修改 /boot里的extlinux/extlinux.conf

把 image.gz 改成zcore-unmatched

正常 启动 

理论 可进入 zcore