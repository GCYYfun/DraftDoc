# Sifive Unmatched 调查

## 关于 制作 默认sd 带的 启动盘

https://github.com/sifive/freedom-u-sdk

## 关于 从零 启动

目前无 现成 方法 ，但有 可借鉴 的 资料


fu540的 bootloader 

https://github.com/sifive/freedom-u540-c000-bootloader/tree/master/sifive/devices

包含 从零启动 过程 可按 fu740 迁移

## 关于fbsl 使用

https://github.com/sifive/freedom-u540-c000-bootloader/issues/9


## 关于 自己 烧录

https://github.com/carlosedp/riscv-bringup/tree/master/unmatched

## 关于 debug 

https://www.reddit.com/r/RISCV/comments/no4a3e/hifive_unmatched_openocd_gdb_beginning_bare_metal/

openocd + gdb 

openocd cfg文件  
https://gist.github.com/a4lg/df51da397b72299042182ccc19f75371


## 关于 s7

需要 去掉 uboot 才能 用 ，现在 的 boot flow ，或许需要自己改u-boot。

https://forums.sifive.com/t/how-about-the-s7-core/5028/13