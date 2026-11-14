# Linux 下载

> Deepin 25（crimson）｜2026-10-26
> 全文按「比较 → 目的 → 图形界面 → 命令行 → 卸载」组织。

---

## 目录

| 节 | 内容 |
|---|---|
| [一](#c1) | 下载比较（Windows vs Linux） |
| [二](#c2) | 目的：快、准、无错 |
| [2.1](#c2-1) | 快：多线程 |
| [2.2](#c2-2) | 准：真下载 |
| [2.3](#c2-3) | 无错：安装无错 |
| [三](#c3) | 图形界面（一）：Gopeed |
| [3.1](#c3-1) | Gopeed 下载 |
| [3.2](#c3-2) | Gopeed 安装 |
| [3.3](#c3-3) | Gopeed 设置 |
| [四](#c4) | 图形界面（二）：aria2 + AriaNg |
| [五](#c5) | 命令行方式 |
| [5.1](#c5-1) | wget |
| [5.2](#c5-2) | aria2c |
| [5.3](#c5-3) | curl |
| [六](#c6) | 出问题怎么办 |
| [七](#c7) | 卸载 |
| [附录 A](#ca) | 判断速查：文件类型、真下载、坏包 |
| [附录 B](#cb) | 命令速查（完整可粘贴） |

---

<a id="c1"></a>
## 一、下载比较（Windows vs Linux）

| 项目 | Windows | Linux（deepin） |
|---|---|---|
| 下载工具 | 浏览器；IDM、迅雷加速；qBittorrent 下 BT | 浏览器；Gopeed 或 aria2c 加速；Gopeed 兼下 BT/磁力 |
| 操作方式 | 以图形界面为主 | 图形界面与命令行并行，二者能力覆盖相同 |
| 文件落点 | 统一写入「下载」文件夹 | 图形界面写入设置的下载目录；命令行写入**当前工作目录** |
| 安装形态 | 以 `.exe` / `.msi` 为主，双击即装 | `.deb`（主）、`.tar.gz`、`.AppImage`、`.run` |
| 安装位置 | 由安装程序询问，可指定盘符与路径 | 由安装包声明，安装时不可指定 |
| 依赖处理 | 运行库需自行安装，失败时报缺失 DLL | 包声明依赖，`apt` 自动解析获取 |
| 卸载 | 控制面板或卸载程序，易留注册表残留 | `apt remove/purge` 或删除目录，无注册表 |
| 系统集成 | 写入注册表、开始菜单 | 写入 `/usr/share/applications` 等目录，由包管理器记录归属 |

差异的根源有三点，理解这三点即可解释上表全部内容：

1. **包管理机制**。Linux 的软件由包管理器统一登记：谁装了哪些文件、依赖谁，全部有记录。因此安装位置、依赖、卸载都可以自动化，代价是不能临时指定路径。
2. **无注册表**。配置存于用户目录下的文本文件（`~/.config` 等），删除目录即等于清除配置。
3. **命令行与图形同源**。下载引擎与界面分离，图形界面（Gopeed、AriaNg）调用的是同一套下载能力，不存在"图形能下、命令不能下"的情况。

---

<a id="c2"></a>
## 二、目的：快、准、无错

下载要达成的目标只有三个：快（吞吐高）、准（拿到的是真实文件）、无错（装得上）。三者对应不同的技术手段，互相不能替代。

<a id="c2-1"></a>
### 2.1 快：多线程

**机制**：将文件按字节区间切分为若干分段，为每段建立独立连接并发获取，完成后按序拼接。

**有效的条件**：

| 条件 | 说明 |
|---|---|
| 服务端未限制单 IP 并发连接数 | 若限制为 2~3 条（GitHub Release 常见），多开的连接会被拒绝或排队，实际并发数等于服务端上限 |
| 服务端支持 Range 请求 | 分段下载依赖 HTTP Range；不支持时只能整文件传输 |
| 带宽与写入不成为瓶颈 | 目标磁盘写入慢（USB 2.0、机械盘随机写）时，增加连接数无收益 |

**结论**：连接数的实际上限由服务端策略决定，本地参数只能在此上限内争取。多线程并非越多越好，还会触发服务端限流（HTTP 429）。

**参数**（以 aria2c 为例）：

| 参数 | 含义 |
|---|---|
| `-x16` | 对同一服务器的最大连接数，aria2 上限为 16 |
| `-s16` | 文件分段数，通常与 `-x` 取同值 |
| `-c` | 断点续传 |

<a id="c2-2"></a>
### 2.2 准：真下载

**问题**：下载器只按地址取数据，不判断取回的是文件还是网页。链接指向登录页、跳转页、防盗链页时，落到本地的可能只有数 KB 的 HTML。

**判据**：读取响应头，不取正文。

```bash
curl -sI "https://github.com/GopeedLab/gopeed/releases/download/v1.9.3/Gopeed-v1.9.3-linux-amd64.deb" | grep -iE "content-type|content-length|content-disposition"
```

| 响应头 | 判定依据 |
|---|---|
| `Content-Length` | 文件真实字节数，用于下载后校验完整性 |
| `Content-Type` | 为 `text/html` 说明返回的是网页，不是文件 |
| `Content-Disposition` | 服务端建议的文件名，可与实际保存名比对 |

**假下载的典型形态**：网盘分享页、需登录的下载页、点击按钮后才生成地址的页面。此类地址不能交给下载器，须先获取真实直链。

<a id="c2-3"></a>
### 2.3 无错：安装无错

安装失败通常源于两件事：包选错，或安装方式不当。

**1. 包类型要选对**

| 类型 | 适用场景 | 安装要点 |
|---|---|---|
| `.deb` | Debian 系发行版原生包，优先选择 | `dpkg -i` 后补依赖；装到哪由包声明 |
| `.tar.gz` / `.tar.xz` | 便携版、无发行版包时 | 解压后直接运行主程序，不写系统目录 |
| `.AppImage` | 单文件分发，自带依赖 | 赋执行权限后运行；需 `libfuse2` |
| `.run` | 厂商自制安装脚本 | 赋执行权限后运行，按提示交互 |

选择顺序：源内可用则 `apt install`；否则 deb → AppImage → tar.gz。

架构须匹配：文件名含 `x64`/`amd64` 适用于 Intel/AMD 平台；`arm64`/`aarch64` 适用于 ARM 平台，交叉安装无法运行。

**2. 安装方式正确**

三类失错，处理方式不同：

| 失错 | 现象 | 处理 |
|---|---|---|
| 包损坏 | `dpkg-deb: zstd 错误: Data corruption detected`，解包中断 | 对照官方字节数；用 `dpkg-deb --fsys-tarfile` 验证；无法解开则重新获取 |
| 解压不当 | tar 包解到错误层级，找不到主程序 | 解压后先 `ls` 确认目录结构，再定位可执行文件 |
| 依赖缺失 | `依赖关系问题 - 仍未被配置` | `sudo apt install -f` 补齐并完成配置 |

注意：字节数一致不代表包完好。下载过程可能写坏内容，此时重复安装无效，只能更换来源重新获取。

字节数只能证明长度一致；要证明内容一致，须比对校验和：

```bash
sha256sum ~/Downloads/Gopeed/Gopeed-v1.9.3-linux-amd64.deb
```

输出值与发布页给出的 SHA256 值一致才算完整。大文件、重要镜像建议走这一步。

---

<a id="c3"></a>
## 三、图形界面（一）：Gopeed

**工具选型**（三选一）：

| 使用场景 | 选择 | 依据 |
|---|---|---|
| 日常下载：网页链接、BT 种子、磁力 | Gopeed | 图形界面，协议全覆盖，参数可视化 |
| 需精确控制参数，或不额外安装图形软件 | aria2 + AriaNg | 复用系统已有 aria2c，以浏览器作界面 |
| 脚本、批量、无图形环境 | wget / aria2c / curl | 可脚本化，退出码可靠 |

**选择 Gopeed 的理由**：

1. **协议覆盖完整**。HTTP/HTTPS、BT 种子、磁力链、ed2k 由同一程序处理，无需为不同来源准备多个客户端。
2. **跨平台一致**。Windows 与 Linux 使用同一套界面与配置项，迁移成本为零，配置文件结构相同。
3. **多线程与断点续传内置**。HTTP 任务默认 16 连接，可在建任务时逐任务调整；中断后继续，无需额外参数。
4. **图形能力完整**。提供任务队列、并发数控制、单任务限速、按类型自动分类保存、定时启停，这些是纯命令行方案需要自行编排的部分。
5. **分发形式友好**。提供官方 deb 包，一次安装即可用；源码开放，扩展以 JavaScript 编写，可按需增补取链能力。

<a id="c3-1"></a>
### 3.1 Gopeed 下载

| 操作 | 路径 |
|---|---|
| 普通链接 | 右下角「+」→ 粘贴地址（可一行一个批量添加）→ 选择目录 → 创建任务 |
| BT 种子 | 下载 `.torrent` 文件后拖入窗口，或在设置中开启「自动识别种子文件」 |
| 磁力链 | 直接粘贴 `magnet:?xt=...` |
| 单任务参数 | 建任务对话框中可改连接数、保存目录、分类（音乐/视频/文档/程序）；「高级选项」内可设 UA、Cookie、Referer、代理 |

任务列表右键可暂停、继续、打开所在目录；顶部切换进行中与已完成。

<a id="c3-2"></a>
### 3.2 Gopeed 安装

```bash
sudo dpkg -i ~/Downloads/Gopeed/Gopeed-v1.9.3-linux-amd64.deb
sudo apt install -f        # 报依赖问题时执行
gopeed --version           # 输出版本号即安装成功
```

依赖缺失、包损坏的判定与处理见 [2.3](#c2-3) 与[附录 A](#ca)。

<a id="c3-3"></a>
### 3.3 Gopeed 设置

设置界面分「基本」与「高级」两个标签页，分组如下。

**1. 基本设置**

| 分组 | 项目 | 说明与取值建议 |
|---|---|---|
| 常规 | 下载目录 | 所有任务的默认落点，建议指向数据盘而非系统盘 |
| 常规 | 最大同时运行任务数 | 并发任务上限，带宽有限时保持默认或降低 |
| 常规 | 默认直连 | 建任务时是否默认勾选直连（不经代理） |
| 常规 | 开机启动 | Windows/Linux 有效 |
| HTTP 协议 | 连接数 | 单任务并发连接数，默认 16；服务端限制并发时调低无益 |
| HTTP 协议 | User-Agent | 部分站点按 UA 拒绝请求，遇 403 时优先调整此项 |
| HTTP 协议 | 使用服务端时间 | 以服务端时间戳作为文件时间 |

**2. 高级设置**

| 分组 | 项目 | 说明与取值建议 |
|---|---|---|
| 网络 | 代理模式 | 无 / 跟随系统 / 自定义；直连可通时保持「无」 |
| 网络 | 代理协议与地址 | 支持 HTTP、HTTPS、SOCKS5，填写主机与端口 |
| 网络 | 代理凭据 | 需要认证的代理填写用户名与密码 |
| API | 通信协议与地址 | 供外部程序或 Web 界面调用，默认本机 |
| API | API Token | 调用凭据，对外暴露时须设置 |
| BitTorrent | 监听端口 | 建议固定端口并在防火墙放行，否则冷门资源难以建立连接 |
| BitTorrent | Tracker 订阅地址 | 默认内置订阅，可追加 `https://trackerslist.com/all.txt` |
| BitTorrent | 自动更新 Tracker | 保持开启 |
| BitTorrent | 自定义 Tracker | 手动追加的服务器列表 |
| BitTorrent | 做种策略 | 按永久做种、分享率或时长三种方式之一设置 |

**3. 扩展设置**

扩展页为内置商店，点击卡片安装；也可「手动安装」填入 GitHub 仓库地址。单个扩展的配置在其详情页内，例如：

| 扩展 | 用途 | 需配置的项 |
|---|---|---|
| 哔哩哔哩 | 解析 B 站视频，支持分 P（`?p=1-3`） | 高清需填入浏览器中 B 站 cookie；默认上限 480P |
| YouTube | 解析油管视频 | 1080P 以上音视频分离，需 ffmpeg 合并 |
| GitHub Release / 仓库 | 批量获取 Release 附件、整仓库 | 无 |

音视频合并依赖 ffmpeg：`sudo apt install ffmpeg`，合并命令 `ffmpeg -i 视频.mp4 -i 音频.mp4 -c copy 输出.mp4`。

扩展运行在下载器进程内，可访问任务与网络请求。涉及账号凭据的扩展（如网盘类）须评估其来源与权限范围后再启用。

---

<a id="c4"></a>
## 四、图形界面（二）：aria2 + AriaNg

**构成**：aria2c 为下载引擎，通过 RPC（JSON-RPC over HTTP/WebSocket）暴露接口；AriaNg 为纯静态网页前端，调用该接口。三者关系为「引擎 — 接口 — 前端」，前端不参与数据传输。

| 角色 | 实体 | 说明 |
|---|---|---|
| 引擎 | `aria2c` 进程 | 执行下载，无界面 |
| 接口 | RPC，默认端口 6800 | 仅监听本机，需与引擎同机 |
| 前端 | `index.html`（AriaNg） | 浏览器打开即用，不安装、不写系统目录 |

现有部署位于 `工具/aria2图形/`，AriaNg 已预置为连接 `127.0.0.1:6800`；`aria2下载器.desktop` 为其启动项。

```bash
# 启动：后台执行 aria2c（16 段、断点续传、任务清单 30 秒存盘）并打开前端
bash "/mnt/winc/WorkBuddyData/wsqw_UOS/工具/aria2图形/启动下载器.sh"

# 停止：保存任务清单后退出，未完成任务在下次启动时继续
bash "/mnt/winc/WorkBuddyData/wsqw_UOS/工具/aria2图形/停止下载器.sh"
```

**能力**：多任务队列、单任务暂停与续传、分段进度、限速、BT/磁力、批量导入（配合 `-i`）。
**限制**：无系统集成，需手动启停；关闭引擎进程后前端即刻失去连接。
**适用**：需要精确控制参数、或以浏览器作为唯一界面的场景。

---

<a id="c5"></a>
## 五、命令行方式

命令行与图形界面调用同一套下载能力，命令行多出的是可脚本化与可批处理。以下命令均为完整形式；示例统一使用 Gopeed 安装包地址，实际使用时替换为需要下载的地址。参数速查见[附录 B](#cb)。

<a id="c5-1"></a>
### 5.1 wget

用途：单线程下载，行为稳定，退出码可靠，适合写入脚本。

```bash
# 下载到当前目录，断点续传
wget -c "https://github.com/GopeedLab/gopeed/releases/download/v1.9.3/Gopeed-v1.9.3-linux-amd64.deb"

# 指定保存目录（不存在需先创建）
wget -c -P /media/wsqw/资料 "https://github.com/GopeedLab/gopeed/releases/download/v1.9.3/Gopeed-v1.9.3-linux-amd64.deb"

# 后台下载，日志写入当前目录的 wget-log
wget -b "https://example.com/file.iso"

# 限速 200 KB/s
wget -c --limit-rate=200k "https://example.com/file.iso"
```

要点：默认以地址中的文件名保存；失败时返回非零退出码。wget 不具备多线程能力，`--span-hosts` 等参数用于跨域抓取，与并发无关。

<a id="c5-2"></a>
### 5.2 aria2c

用途：多线程、多协议下载，支持 HTTP/FTP/SFTP/BT/磁力/Metalink。

```bash
# 16 段并发，断点续传
aria2c -x16 -s16 -c "https://github.com/GopeedLab/gopeed/releases/download/v1.9.3/Gopeed-v1.9.3-linux-amd64.deb"

# 指定保存目录
aria2c -x16 -s16 -c -d /media/wsqw/资料 "https://github.com/GopeedLab/gopeed/releases/download/v1.9.3/Gopeed-v1.9.3-linux-amd64.deb"

# 并发度降低，避免影响其他网络活动
aria2c -x4 -s4 -c "https://example.com/file.iso"

# 批量下载：先在当前目录新建 list.txt，每行写一个网址
aria2c -x16 -s16 -c -i list.txt

# 磁力链
aria2c "magnet:?xt=urn:btih:0123456789abcdef0123456789abcdef01234567"
```

要点：连接数受服务端策略约束（见 [2.1](#c2-1)）；未完成的任务重跑同一命令即可续传；需经代理时加 `--all-proxy=http://127.0.0.1:端口`，aria2 不读取 `http_proxy` 环境变量。

<a id="c5-3"></a>
### 5.3 curl

用途：读取响应头、按需下载、调试 HTTP 行为。

```bash
# 仅取响应头（判断真下载，见 2.2）
curl -sI "https://github.com/GopeedLab/gopeed/releases/download/v1.9.3/Gopeed-v1.9.3-linux-amd64.deb" | grep -iE "content-type|content-length|content-disposition"

# 查看状态码
curl -sI "https://example.com/file.zip" | head -5

# 下载并指定文件名，-L 跟随重定向
curl -L -o gopeed.deb "https://github.com/GopeedLab/gopeed/releases/download/v1.9.3/Gopeed-v1.9.3-linux-amd64.deb"

# 网页转 Markdown
curl -sL "https://r.jina.ai/https://www.deepin.org" -o 页面.md
```

要点：`-o` 指定文件名，`-O` 使用地址中的原名，二者不可混用；多数下载地址需 `-L`；访问本机服务时加 `--noproxy '*'`，否则请求会转入系统代理。

---

<a id="c6"></a>
## 六、出问题怎么办

**排查顺序**：先取状态码与响应头 → 再校验完整性 → 最后读错误信息原文。多数问题在前两步即可定位，不必反复重试。

```bash
curl -sI "地址" | head -5                  # 200 / 403 / 404 / 429
sha256sum 文件                             # 与发布值比对
```

| 症状 | 原因 | 处理 |
|---|---|---|
| 下完找不到文件 | 命令行落在当前工作目录 | `pwd` 确认位置；`find ~ -name "文件名"` 查找 |
| 下载回来只有几 KB | 地址非直链，落地的是网页 | `curl -sI` 看 `Content-Type`；换真实直链 |
| 速度长期为 0 | 地址失效、源站限速、服务端拒绝并发、磁盘写入慢 | 先验证地址；降连接数 `-x4`；换源 |
| 报 `429 Too Many Requests` | 请求过密被限流，数分钟自动恢复 | 降低并发、暂停后重试；封 IP 是持续数小时以上且直接连不上，二者不同 |
| 报 `403 Forbidden` | 需登录、防盗链、UA 被识别 | 改用浏览器下载；curl 加 `-A`；Gopeed 建任务时填 UA/Cookie/Referer |
| 报 `依赖关系问题` | 缺系统库 | `sudo apt install -f` |
| 报 `zstd 错误: Data corruption` | 包内容损坏 | 比对字节数与 SHA256；`dpkg-deb --fsys-tarfile` 验证；重下 |
| 装完无法运行 | 架构不匹配 | 换 `x64`/`amd64` 版本 |
| AppImage 双击无反应 | 缺执行权限、缺 `libfuse2`、NTFS 分区上无执行位 | `chmod +x`；`sudo apt install libfuse2`；复制到家目录再运行 |
| AriaNg 显示无法连接 aria2 | 引擎未启动或端口未监听 | `ss -ltn \| grep 6800`；查 `aria2.log`；用终端执行启动脚本 |
| 双击 `.sh` 无反应 | 文件管理器以文本方式打开脚本 | 终端执行 `bash 脚本.sh` |
| 磁力/BT 无速度 | 做种者少、监听端口未放行、Tracker 不足 | 补充 Tracker；放行监听端口；更换资源 |
| 开了代理后本机请求失败 | curl 把 `127.0.0.1` 一并送入代理 | 加 `--noproxy '*'` |
| 下载不经代理 | aria2 不读取代理环境变量；Gopeed 需显式配置 | aria2 加 `--all-proxy=http://127.0.0.1:端口`；Gopeed 在高级设置中填代理 |

---

<a id="c7"></a>
## 七、卸载

```bash
# 由 apt/dpkg 安装的包
sudo apt remove 软件名        # 卸载，保留配置
sudo apt purge 软件名         # 卸载并删除配置
sudo dpkg -r 软件名           # 卸载 dpkg 直接安装的包

# 查看是否残留
dpkg -l | grep 软件名
```

| 安装形态 | 卸载方式 |
|---|---|
| `.deb` | 上述命令之一；`purge` 可清除 `/etc` 下的配置 |
| `.tar.gz` 便携版 | 删除解压目录（如 `~/Apps/软件名`） |
| `.AppImage` | 删除该文件 |
| 用户级配置 | 检查并删除 `~/.config/软件名`、`~/.local/share/软件名`、`~/.cache/软件名` |

注意：`apt remove` 不删除主目录下的用户配置；需要彻底清除时，先 `purge` 再核对上述三个目录。卸载后菜单项残留，注销重新登录即可刷新。

---

<a id="ca"></a>
## 附录 A：判断速查

**一、文件类型**

| 后缀 | 定位 | 安装方式 | 卸载方式 |
|---|---|---|---|
| `.deb` | 发行版原生包，优先 | `dpkg -i` → `apt install -f` | `apt remove` / `dpkg -r` |
| `.tar.gz` `.tar.xz` | 便携版 | 解压 → 运行主程序 | 删目录 |
| `.AppImage` | 单文件程序 | `chmod +x` → 运行 | 删文件 |
| `.run` | 厂商安装脚本 | `chmod +x` → 运行 | 按其自带卸载脚本 |

架构对照：`x64`/`amd64` = Intel/AMD；`arm64`/`aarch64` = ARM。不匹配则无法运行。

**二、真下载判定**

| 检查项 | 结论 |
|---|---|
| `Content-Type: text/html` | 返回的是网页，地址非直链 |
| `Content-Length` 缺失 | 服务端未提供长度，无法校验完整性 |
| 下载后体积为几 KB | 落地的多为跳转页或错误页 |
| 下载后字节数 ≠ `Content-Length` | 传输不完整，需续传或重下 |

```bash
curl -sI "目标地址" | grep -iE "content-type|content-length|content-disposition"
```

**三、坏包检查**

```bash
ls -l 包.deb                                              # 1. 与官方字节数比对
dpkg-deb --fsys-tarfile 包.deb > /dev/null && echo 完好    # 2. 验证能否完整解包
```

判定：字节数一致且能完整解包 → 包完好；字节数一致但解包失败 → 内容损坏，重新获取；字节数不足 → 下载不完整。

---

<a id="cb"></a>
## 附录 B：命令速查

```bash
# —— 判断 ——
curl -sI "https://github.com/GopeedLab/gopeed/releases/download/v1.9.3/Gopeed-v1.9.3-linux-amd64.deb" | grep -iE "content-type|content-length|content-disposition"
curl -sI "https://example.com/file.zip" | head -5

# —— 下载 ——
wget -c "https://github.com/GopeedLab/gopeed/releases/download/v1.9.3/Gopeed-v1.9.3-linux-amd64.deb"
wget -c -P /media/wsqw/资料 "https://example.com/file.iso"
aria2c -x16 -s16 -c "https://github.com/GopeedLab/gopeed/releases/download/v1.9.3/Gopeed-v1.9.3-linux-amd64.deb"
aria2c -x16 -s16 -c -d /media/wsqw/资料 "https://example.com/file.iso"
aria2c -x16 -s16 -c -i list.txt                    # 批量：list.txt 每行一个网址
aria2c "magnet:?xt=urn:btih:0123456789abcdef0123456789abcdef01234567"
curl -L -o gopeed.deb "https://github.com/GopeedLab/gopeed/releases/download/v1.9.3/Gopeed-v1.9.3-linux-amd64.deb"

# —— 安装 ——
sudo dpkg -i ~/Downloads/Gopeed/Gopeed-v1.9.3-linux-amd64.deb
sudo apt install -f
dpkg-deb --fsys-tarfile ~/Downloads/Gopeed/Gopeed-v1.9.3-linux-amd64.deb > /dev/null && echo 完好
dpkg -L gopeed

# —— 卸载 ——
sudo apt remove 软件名
sudo apt purge 软件名
sudo dpkg -r 软件名

# —— 排错 ——
pwd                                        # 确认当前目录（命令行下载落点）
ss -ltn | grep 6800                        # AriaNg 后端端口是否监听
curl --noproxy '*' http://127.0.0.1:6800/jsonrpc
```
