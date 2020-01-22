# A rough debug
a try of using gdb to debug program which is suggested in https://rcore-os.github.io/rCore_tutorial_doc/chapter1/part4.html

---
## [环境]
1. ubuntu
2. 安装好gdb
3. 按文档build完成

---
### Step 1
假设当前目录为os文件夹下  
进入os文件夹下target文件夹下的debug文件夹  
> cd target/debug/
### step 2
使用gdb加载已build好的os文件
> gdb os
### step 3
设置在启动入口设置断点
> b _start
### step 4
run一下看看有没有到断点停下
> run
### step 5 [Option]
如果成功请根据口味自己调制
if not , um... 还请认真思考与分析。

## 例子
