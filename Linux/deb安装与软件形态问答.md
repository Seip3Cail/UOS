# deb安装与软件形态问答

# deb 安装的形形色色

> 整理：

---

### 1.双击.deb 没反应

排查三步（对应三条命令）：

```bash
which deepin-deb-installer       # ① 程序在不在,没有输出就是软件不存在
dpkg -l | grep deepin-deb-installer   # ② 包装没装
xdg-mime query default application/vnd.debian.binary-package   # ③ 关联deb
```

实际踩过的坑：①② 都为空（**安装器根本没装**），③ 输出的是文件管理器的"占位入口"
（`dde-file-manager-custom-open-...`）——双击被转给一个只会弹"选个应用"的空壳，所以看着像没反应。

### 2.修复方法

```bash
sudo apt install deepin-deb-installer
xdg-mime default deepin-deb-installer.desktop application/vnd.debian.binary-package
```

也可以图形补救：右键 .deb → 打开方式 → 选"软件包安装器" → 勾"设为默认"。

### 3.`sudo apt install` 装不上的排查

先确认**给它的到底是不是 .deb 文件**：

```bash
ls -lh ~/Downloads/          # 看下载目录里都有什么
file 路径                     # 判断这东西到底是什么类型
```

- `apt install` 只认 **.deb 文件**；给个文件夹、zip、AppImage 它都不认
- 如果下载的是**文件夹**，deb 往往在里面：`cd` 进去 `ls -lh` 找
- 装本地 deb 的命令，**开头 **`./`** 不能少**：

```bash
sudo apt install -y ./文件名.deb
```

### 4.Linux 软件的四种形态

| 形态 | 长什么样 | 怎么处理 |
| --- | --- | --- |
| 仓库包 | 没有文件，直接 `apt install 名字` | **最优先**，干净好卸载 |
| `.deb` | 单个文件（像 .msi） | `sudo apt install ./xxx.deb` |
| AppImage | 单个文件，加执行权就跑 | 绿色软件路线 |
| 源码编译 | `.tar.gz` + configure/make | 能避开就避开 |

选型顺序：先搜仓库 → 没有再找 deb/AppImage → 源码是最后手段。

### 5.终端路径 `~` 和绝对路径

- `pwd` 给的是**绝对路径**：`/home/wsqw/Downloads/xxx`
- `~/Downloads/xxx` 里的 `~` 由 shell 自动展开成 `/home/wsqw`，**展开后就是同一个绝对路径**

**两种写法等价，不用改写。** 只记一个坑：

- `~` **放在双引号里不展开**——要用 `"$HOME/Downloads"`，别写 `"~/Downloads"`

### 6.装 .deb 的纪律

1. **永远命令行装**：`sudo apt install -y ./xxx.deb`——报错看得见，图形安装器遇错会装哑巴亏
2. **依赖报错先读懂**：缺什么装什么；用不上的依赖（如仓库签名钥匙）可用占位包绕过
3. `_apt 权限不够`**是警告不是错误**——apt 自己会提权处理，不用管
