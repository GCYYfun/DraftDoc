# About the umatched debug

## 缘由

想调试代码，但代码要跑在硬件上

听说 jtag 可以硬件调试

就有了这个文档

## 目的 

在硬件上看看我的代码跑到哪了

## 需要的准备

### 硬件

- 一个装配完毕的 unmatched 的主机
- 一个 ubuntu20.04 的 电脑 (我使用的环境)
- 一个 unmatched 自带的 连接线 ，就是 串口 那根
- 一个 unmatched 的 电源线

### 软件

- [OpenOCD](https://github.com/xpack-dev-tools/openocd-xpack/releases) (选择对应平台，比如我是ubuntu20.04，我选择的是 __xpack-openocd-0.11.0-2-linux-x64.tar.gz__)

- [riscv-gdb](https://github.com/riscv-collab/riscv-gnu-toolchain/releases)(riscv-gnu-toolchain 中携带，非必要不用自己编译，徒增烦恼，下载编译好的文件，进行使用，我选的 __riscv64-elf-ubuntu-20.04-nightly-2021.09.21-nightly.tar.gz__)

- 一个可以 裸机 执行 的 elf 文件 (这个大家根据喜好各自定义，可以参考 [unmatched_survey.md](/unmatched_survey.md) 中 提到的 从零启动 fu540 bootloader ，来编写，注意imac)

### 文件

- [openocd.cfg](https://github.com/sifive/freedom-e-sdk/blob/master/bsp/sifive-hifive-unmatched/openocd.cfg) (这是openocd使用的配置文件，um..之前我使用的别的文件，试图从0x0000_0000启动，发现是只读内存不对，腾讯会议上[阿龙]同学，给了这个库的连接，这个是从0x2000_0000地址启动)

```
                   BOOT MODE SEL               BATT CONN
 +==================+-+-+-+-+-+=================|======|===+
 |                  | | | | |X| ON              (      )   |
 |                  | | | | | |                 (      )   |
 |        CHIP_ID-> |X|X|X|X| | OFF             (______)   |
 |                +-+-+-+-+-+-+                            |
 |                     3 2 1 0 <--MSEL                     |
 |                                                         |

```

使用时 请把 mesl 开关 放置图片对应位置

## 使用

ok! 启动调试,开机。

1. 首先 打开 一个 终端 串口连接 到 unmatched (ubuntu和unmatched串口线已连接的情况下)
```
比如：
    picocom -b 115200 /dev/ttyUSB1
```

2. 显示连接成功后，新打开一个终端，执行 (前提是以上提到的文件已经安装，并正确配置环境变量，在openocd.cfg所在目录执行)
```
    openocd -f openocd.cfg
```
如果 __Error: libusb_open() failed with LIBUSB_ERROR_ACCESS__
请
```
    sudo chmod -R 777 /dev/bus/usb/
```
![openocd](/openocd.png)

3. openocd 连接成功后，开启riscv-gdb，然后加载文件

```
riscv64-unknown-elf-gdb
target remote localhost:3333
file XX(elf文件)
load XX(elf文件)
b main
c
```

![gdb](/gdb.png)


文档或有遗漏，如有问题或不同，欢迎指出和频繁联系。
