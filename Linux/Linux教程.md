# Linux教程

# **Linux教程**

Linux 内核最初只是由芬兰人林纳斯·托瓦兹（Linus Torvalds）在赫尔辛基大学上学时出于个人爱好而编写的。

## Linux vs Windows

目前国内 Linux 更多的是应用于服务器上，而桌面操作系统更多使用的是 Windows。

| **比较** | **Windows** | **Linux** |
| --- | --- | --- |
| 界面 | 界面统一，外壳程序固定所有 Windows 程序菜单几乎一致，快捷键也几乎相同 | 图形界面风格依发布版不同而不同，可能互不兼容。 |
| 驱动程序 | 驱动程序丰富，版本更新频繁。默认安装程序里面一般包含有该版本发布时流行的硬件驱动程序，之后所出的新硬件驱动依赖于硬件厂商提供。 | 由志愿者开发，由 Linux 核心开发小组发布，很多硬件厂商基于版权考虑并未提供驱动程序 |
| 使用 | 使用比较简单，容易入门。图形化界面对没有计算机背景知识的用户使用十分有利。 | 图形界面使用简单，容易入门。文字界面，需要学习才能掌握。 |
| 学习 | 系统构造复杂、变化频繁，且知识、技能淘汰快，深入学习困难。 | 系统构造简单、稳定，且知识、技能传承性好，深入学习相对容易。 |
| 软件 | 每一种特定功能可能都需要商业软件的支持，需要购买相应的授权。 | 大部分软件都可以自由获取，同样功能的软件选择较少。 |

## Linux 系统启动过程

linux启动时我们会看到许多启动信息。

Linux系统的启动过程可以分为5个阶段：

- 内核的引导。
- 运行 init。
- 系统初始化。
- 建立终端 。
- 用户登录系统。

### 内核引导

当计算机打开电源后，首先是BIOS开机自检，按照BIOS中设置的启动设备（通常是硬盘）来启动。

操作系统接管硬件以后，首先读入 /boot 目录下的内核文件。

![](assets/19ee6ca66114e6094af278adb744f9d868d1715e.png)

### 运行init

init 进程是系统所有进程的起点，你可以把它比拟成系统所有进程的老祖宗，没有这个进程，系统中任何进程都不会启动。

init 程序首先是需要读取配置文件 /etc/inittab。

![](assets/ovgVJ79BzOheO0DDpebdV4.png)

### 运行级别

许多程序需要开机启动。它们在Windows叫做"服务"（service），在Linux就叫做"守护进程"（daemon）。

init进程的一大任务，就是去运行这些开机启动的程序。

但是，不同的场合需要启动不同的程序，比如用作服务器时，需要启动Apache，用作桌面就不需要。

Linux允许为不同的场合，分配不同的开机启动程序，这就叫做"运行级别"（runlevel）。也就是说，启动时根据"运行级别"，确定要运行哪些程序。

![](assets/4059d166a63cbd1c19075a8c5819c8003bc0427a.png)

Linux系统有7个运行级别(runlevel)：

- 运行级别0：系统停机状态，系统默认运行级别不能设为0，否则不能正常启动
- 运行级别1：单用户工作状态，root权限，用于系统维护，禁止远程登录
- 运行级别2：多用户状态(没有NFS)
- 运行级别3：完全的多用户状态(有NFS)，登录后进入控制台命令行模式
- 运行级别4：系统未使用，保留
- 运行级别5：X11控制台，登录后进入图形GUI模式
- 运行级别6：系统正常关闭并重启，默认运行级别不能设为6，否则不能正常启动

### 系统初始化

在init的配置文件中有这么一行： sysinit:/etc/rc.d/rc.sysinit　它调用执行了/etc/rc.d/rc.sysinit，而rc.sysinit是一个bash shell的脚本，它主要是完成一些系统初始化的工作，rc.sysinit是每一个运行级别都要首先运行的重要脚本。

它主要完成的工作有：激活交换分区，检查磁盘，加载硬件模块以及其它一些需要优先执行任务。

![](assets/88fd3af0a0653c7883d87d62489988edaeb5cb92.png)

### 建立终端

rc执行完毕后，返回init。这时基本系统环境已经设置好了，各种守护进程也已经启动了。

init接下来会打开6个终端，以便用户登录系统。在inittab中的以下6行就是定义了6个终端：

1:2345:respawn:/sbin/mingetty tty1
2:2345:respawn:/sbin/mingetty tty2
3:2345:respawn:/sbin/mingetty tty3
4:2345:respawn:/sbin/mingetty tty4
5:2345:respawn:/sbin/mingetty tty5
6:2345:respawn:/sbin/mingetty tty6

可以看出在2、3、4、5的运行级别中都将以respawn方式运行mingetty程序，mingetty程序能打开终端、设置模式。

同时它会显示一个文本登录界面，这个界面就是我们经常看到的登录界面，在这个登录界面中会提示用户输入用户名，而用户输入的用户将作为参数传给login程序来验证用户的身份。

### 用户登录系统

一般来说，用户的登录方式有三种：

- （1）命令行登录
- （2）ssh登录
- （3）图形界面登录

正确的关机流程为：sync \> shutdown \> reboot \> halt

关机指令为：shutdown

## Linux 系统目录结构

```bash
ls /l
```

在 Linux 中，下列目录属于系统关键区，误删或乱改都会直接破坏系统运行：

**/etc — 系统配置核心**

所有关键配置集中于此。任何错误修改都可能导致服务挂掉，甚至系统无法启动。

**/bin、/sbin、/usr/bin、/usr/sbin — 系统指令区**

系统预置命令的所在位置。

- **/bin、/usr/bin**：供普通用户使用的基础指令（如 `ls` 位于 `/bin/ls`）。
- **/sbin、/usr/sbin**：系统管理指令，主要由 root 使用。

**/var — 动态数据区**

系统运行时不断写入的数据都落在这里。
重点是 **/var/log**，各种服务日志全部存放此处；邮件、缓存、队列等内容也在此目录下维护。

## Linux 文件基本属性

Linux 系统是一种典型的多用户系统，不同的用户处于不同的地位，拥有不同的权限。

为了保护系统的安全性，Linux 系统对不同的用户访问同一文件（包括目录文件）的权限做了不同的规定。

在 Linux 中我们通常使用以下两个命令来修改文件或目录的所属用户与权限：

- chgrp：更改文件属组` chgrp [-R] 属组名 文件名`
- chown (change owner) ： 修改所属用户与组。
  ```bash
  chown [–R] 所有者 文件名
  chown [-R] 所有者:属组名 文件名
  ```
- chmod (change mode) ： 修改用户的权限。

**通过 chown 来授权用户，通过 chmod 为用户设置的权限。**

![](assets/3aeda8ea130cf5013c843f9ee813a3ead7f0b573.png)

文件类型(首字母)

- **d** 是目录
- **-** 是文件；
- **l** 表示为链接文档(link file)；
- **b** 则表示为装置文件里面的可供储存的接口设备(可随机存取装置)；
- **c** 表示为装置文件里面的串行端口设备，例如键盘、鼠标(一次性读取装置)。

![](assets/f7063759406530dc21c1a06e3ff129e12e69fbb3.png)

## Linux 文件与目录管理

Linux 的目录结构为树状结构，最顶级的目录为根目录 **/**。

其他目录通过挂载可以将它们添加到树中，通过解除挂载可以移除它们。

- **绝对路径：**
路径的写法，由根目录 **/** 写起，例如： /usr/share/doc 这个目录。
- **相对路径：**
路径的写法，不是由 **/** 写起，例如由 /usr/share/doc 要到 /usr/share/man 底下时，可以写成： **cd ../man** 这就是相对路径的写法。
- **注意**：通常使用时，都是./开始，表示从当前目录开始，而/开始则在环境变量PATH里去找

### 文件

### 普通文件的分类

1. 文本文件    file /etc/hosts    #/etc/hosts: ASCII text
2. 二进制可执行文件 file /bin/ls    #/bin/Ls: ELF 64-bit LSB executable
3. 编译后的目标文件 file hello.o    #hello.o: ELF 64-bit LSB relocatable
4. 数据文件 file /var/log/syslog    #/var/Log/syslog: ASCII text

### 普通文件的操作

- 创建空文件： touch test.txt
- 写入内容： echo "Hello Linux" \> test.txt
- 查看内容 ：cat test.txt
- 统计文件信息：wc -l test.txt
- 复制文件或目录cp（英文全拼：copy file）:
- 移动修改文件与目录mv（英文全拼：move file）:

### 目录

常见的处理目录的命令吧：

- ls（英文全拼：list files）: 列出目录及文件名

```bash
ls -lah ~/Downloads/    #以人类方式用长文件格式显示文件夹~/Downloads(含隐藏)文件
```

- cd（英文全拼：change directory）：切换目录
- pwd（英文全拼：print work directory）：显示目前的目录

```bash
- pwd [-P] 
    -P：显示确实的路径，而非链接 (link) 路径。
```

- mkdir（英文全拼：make directory）：创建一个新的目录

```bash
mkdir [-mp] 目录名称
    -m ：配置文件的权限喔！直接配置，不需要看默认权限 (umask) 的脸色
    -p ：帮助你直接将所需要的目录(包含上一级目录)递归创建起来！
    
# 创建myproject文件夹以及其子文件夹src,docs,tests,build
mkdir -p myproject/{src,docs,tests,build} 
```

- rmdir（英文全拼：remove directory）：删除一个空的目录
- rm（英文全拼：remove）: 删除文件或目录

```bash
rmdir：只能空目录
rm：什么都删除（空与非空）
    -P：从该目录起，一次删除多级空目录
rm删除是彻底删除，所以一定要ls查看清楚得到确定后才删除，最好使用rm -i组合
```

### Linux 文件内容查看

Linux系统中使用以下命令来查看文件的内容：

- cat  由第一行开始显示文件内容
- tac  从最后一行开始显示，可以看出 tac 是 cat 的倒着写！
- nl   显示的时候，顺道输出行号！
- more 一页一页的显示文件内容
- less 与 more 类似，但是比 more 更好的是，他可以往前翻页！
- head 只看头几行
- tail 只看尾巴几行

### Linux系统用户账号的管理

用户账号的管理工作主要涉及到用户账号的添加、修改和删除。

添加用户账号就是在系统中创建一个新账号，然后为新账号分配用户号、用户组、主目录和登录Shell等资源。刚添加的账号是被锁定的，无法使用。

```bash
# 1.添加新的用户账号
useradd 选项 用户名
# 2.删除账号
userdel 选项 用户名
# 3.修改账号
usermod 选项 用户名
# 4.修改密码
passwd 选项 用户名
# 5.增加一个新的用户组
groupadd 选项 用户组
# 6.删除一个已有的用户组
groupdel 用户组
# 7.修改用户组的属性
groupmod 选项 用户组
# 8.切换到其他用户组
newgrp root # 切换到root组
```

## Linux 磁盘管理

Linux 磁盘管理好坏直接关系到整个系统的性能问题。

Linux 磁盘管理常用三个命令为 **df**、**du** 和 **fdisk**。

- **df**（英文全称：disk free）：列出文件系统的整体磁盘使用量
- **du**（英文全称：disk used）：检查磁盘空间使用量
- **fdisk**：用于磁盘分区

```bash
df [-ahikHTm] [目录或文件名]
du [-ahskm] 文件或目录名称
fdisk [-l] 装置名称
mkfs [-t 文件系统格式] 装置文件名    # 磁盘分割完毕后自然就是要进行文件系统的格式化
fsck [-t 文件系统] [-ACay] 装置名称    # fsck（file system check）用来检查和维护不一致的文件系统。
```

## 磁盘挂载与卸除

mount \[-t 文件系统\] \[-L Label名\] \[-o 额外选项\] \[-n\]  装置文件名  挂载点

umount \[-fn\] 装置文件名或挂载点

参见：

/home/wsqw/wsqw\_UOS/Markdown/挂载与卸载应用.md

/home/wsqw/wsqw\_UOS/Markdown/磁盘挂载与卸载笔记.md

## Linux yum 命令

yum（ Yellow dog Updater, Modified）是一个在 Fedora 和 RedHat 以及 SUSE 中的 Shell 前端软件包管理器。

### yum 语法

yum \[options\] \[command\] \[package ...\]

### 常用命令

- 
  1. 列出所有可更新的软件清单命令：**yum check-update**
- 
  1. 更新所有软件命令：**yum update**
- 
  1. 仅安装指定的软件命令：**yum install \<package\_****name\>**
- 
  1. 仅更新指定的软件命令：**yum update \<package\_****name\>**
- 
  1. 列出所有可安裝的软件清单命令：**yum list**
- 
  1. 删除软件包命令：**yum remove \<package\_****name\>**
- 
  1. 查找软件包命令：**yum search ******
- 
  1. 清除缓存命令:
  - **yum clean packages**: 清除缓存目录下的软件包
  - **yum clean headers**: 清除缓存目录下的 headers
  - **yum clean oldheaders**: 清除缓存目录下旧的 headers
  - **yum clean, yum clean all (= yum clean packages; yum clean oldheaders)** :清除缓存目录下的软件包及旧的 headers

## Linux apt 命令

apt（Advanced Packaging Tool）是一个在 Debian 和 Ubuntu 中的 Shell 前端软件包管理器。

apt 命令提供了查找、安装、升级、删除某一个、一组甚至全部软件包的命令，而且命令简洁而又好记。

apt 命令执行需要超级管理员权限(root)。

### apt 语法

apt \[options\] \[command\] \[package ...\]

### 常用命令

- 列出所有可更新的软件清单命令：**sudo apt update**
- 升级软件包：**sudo apt upgrade**
  列出可更新的软件包及版本信息：**apt list --upgradable**

  升级软件包，升级前先删除需要更新软件包：**sudo apt full-upgrade**
- 安装指定的软件命令：**sudo apt install \<package\_****name\>**
  安装多个软件包：**sudo apt install \<package\_****1\> \<package\_****2\> \<package\_****3\>**
- 更新指定的软件命令：**sudo apt update \<package\_****name\>**
- 显示软件包具体信息,例如：版本号，安装大小，依赖关系等等：**sudo apt show \<package\_****name\>**
- 删除软件包命令：**sudo apt remove \<package\_****name\>**
- 清理不再使用的依赖和库文件: **sudo apt autoremove**
- 移除软件包及配置文件: **sudo apt purge \<package\_****name\>**
- 查找软件包命令： **sudo apt search ******
- 列出所有已安装的包：**apt list --installed**
- 列出所有已安装的包的版本信息：**apt list --all-versions**

```bash
sudo apt install <package_name> --no-upgrade    # 安装不升级

sudo apt install <package_name> --only-upgrade    #仅升级
```

## Shell 变量

在 Shell 编程中，变量是用于存储数据值的名称

### 定义变量

变量名="值"

`POINT='/etc/mnt'`

变量名命名规范：

- **只包含字母、数字和下划线：** 变量名可以包含字母（大小写敏感）、数字和下划线 **\_**，不能包含其他特殊字符。
- **不能以数字开头：** 变量名不能以数字开头，但可以包含数字。
- **避免使用 Shell 关键字：** 不要使用Shell的关键字（例如 if、then、else、fi、for、while 等）作为变量名，以免引起混淆。
- **使用大写字母表示常量：** 习惯上，常量的变量名通常使用大写字母，例如 **PI=3.14**。
- **避免使用特殊符号：** 尽量避免在变量名中使用特殊符号，因为它们可能与 Shell 的语法产生冲突。
- \*\*避免使用空格：\*\*变量名中不应该包含空格，因为空格通常用于分隔命令和参数。

### 使用变量

使用一个定义过的变量，只要在变量名前面加美元符号即可

```bash
定义的变量名是POINT，其值为'/etc/mnt'与下面等价
定义的变量名是POINT，其值为$POINT
```

### 删除变量

unset variable\_name

## Shell 输入/输出重定向

系统命令从你的终端接受输入并将所产生的输出发送回​​到您的终端。

一般情况下，每个 Unix/Linux 命令运行时都会打开三个文件：

- 标准输入文件(stdin)：stdin的文件描述符为0，Unix程序默认从stdin读取数据。
- 标准输出文件(stdout)：stdout 的文件描述符为1，Unix程序默认向stdout输出数据。
- 标准错误文件(stderr)：stderr的文件描述符为2，Unix程序会向stderr流中写入错误信息。

默认情况下，command \> file 将 stdout 重定向到 file，command \< file 将stdin 重定向到 file。

注意：输出重定向是大于号(\>)，输入重定向是小于号(\<)。

> `sudo ls -l > /dev/null 2>&1`

### 认识shell

```bash
# 1.查看使用的shell
echo $SHELL
# 2.查shell类型
cat /etc/shells
```
    /bin/sh
    /usr/bin/sh
    /bin/bash
    /usr/bin/bash
    /bin/rbash
    /usr/bin/rbash
    /bin/dash
    /usr/bin/dash
 ```
 常见Shell种类:
·Bash (Bourne Again Shell):最常用的Shell,Linux默认Shell
·Zsh:功能更强大，支持主题和插件
Fish:用户友好，语法更简洁
```

### 典型的shell提示符

username@hostname:\~\$

#### 各部分含义

- #username:当前用户名
- #hostname:主机名
- #\~:当前目录(家目录)
- #\$:普通用户提示符(root用户为#)

### 命令语法基础

命令格式 command \[options\] \[arguments\]

#### 命令参数

![](assets/998b6ac01ff0256c187c1089bd5c9a41272675e1.png)

##### 参数的灵活运用

组合使用短选项 \$ ls-lha # = ls -l -h -a

##### 长选项通常更易读

ls --sort=time --size
带参数的选项

grep -i "error" 1og.txt     # -i是选项,"error"是选项的参数，Log.txt 是位置参数

find . -name "\*.txt"  -type f     # -name 和 -type都带参数

### 输出重定向

#### 标准输出重定向

##### #覆盖写入(\>)

ls -l \> filelist.txt     #将输出保存到文件(覆盖已有内容)

echo "Hello World" \> greetings.txt

##### #追加写入(\>\>)

ls -la  \>\> filelist.txt

echo "Another line" \>\> greetings.txt     # 到文件末尾

#### #标准输出重定向(显式写法)

ls -l 1\> filelist.txt     #1 是 stdout 的文件述符，可省略

#### 标准错误重定向

##### #只重定向错误输出

ls nonexistent 2\> error.log     # 错误信息写入 error.Log

##### #同时重定向stdout 和 stderr

ls goodfile.txt badfile.txt \> output.txt 2\> error.log    #分开重定向

ls goodfile.txt badfile.txt \> al1.log 2\>&1 #合并到一个文件(最常用)

ls goodfile.txt badfile.txt &\> al1.log     #简化写法

### 链接:文件的别名

#### 硬链(Hard Link)

硬链接是文件的另一个名字，与原文件共享同一个inode:

#创建硬链接 In /path/to/original /path/to/link

#查看链接关系 ls -li original link

# 12345 -rw-r--r-- 2 user user 100 May 10 10:00 original

12345 -rw-r--r-- 2 user user 100 May 10 10:00 Link

#两个文件具有相同的innode号(12345)和链接数(2)

**硬链接的特性:**

- 不能跨文件系统
- 不能链接目录
- 删除原文件不影响硬链接

#### 符号链(Symbolic Link)

符号链接(软链接)是一个特殊文件，包含指向目标文件的路径:
