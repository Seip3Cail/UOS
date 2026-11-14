# Brave 浏览器安装与更新笔记（Deepin）

> 整理日期：2026-10-18
> 当前状态：**已安装 Brave Browser 1.97.59**，一切正常
> 本笔记三用：日常更新查「第二步」、重装系统查「第三步」、出毛病查「报错对照表」

---

## 一、背景

- Brave 官网的 apt 更新源在国外，时通时断，更新断在半路会把安装弄残
- 所以：**安装包改从 GitHub Releases 下载，更新改手动**，主动权在自己手里
- GitHub 直连只肯开 2~3 条连接，慢；**gh-proxy.com 加速站**背后是 CDN，肯开多线程
- `brave-keyring` 这个依赖是"官方仓库的签名钥匙"，独立安装用不上，用占位包绕过

## 二、安装（重装系统 / 换机时照抄）

```bash
# ① 装多线程下载引擎（一次即可）
sudo apt install -y aria2 libvulkan1 libu2f-udev equivs

# ② 造占位钥匙，绕过 brave-keyring 依赖（一次性）
mkdir -p /tmp/brave-fix && cd /tmp/brave-fix
printf 'Section: misc\nPriority: optional\nPackage: brave-keyring\nVersion: 1.0\nArchitecture: amd64\nDescription: placeholder, not the real keyring\n' > keyring.ctl
equivs-build keyring.ctl
sudo dpkg -i ./brave-keyring_1.0_amd64.deb

# ③ 一键下载安装主包
bash /mnt/winc/WorkBuddyData/wsqw_UOS/Network/装Brave.sh

# ④ 验收
brave-browser --version
```

装完应用菜单里就有 Brave 图标。

- 启动：应用菜单里的 Brave，或终端 `brave-browser`
- Brave 自动更新已无效（没有源了），**不更新不影响使用**
- 你的数据（书签/扩展/密码）在 `~/.config/BraveSoftware/`，与程序分离

## 三、更新（隔一两个月跑一次）

```bash
bash /mnt/winc/WorkBuddyData/wsqw_UOS/Network/装Brave.sh
```

一条命令全自动：查最新版 → gh-proxy 16 线程下载 → 覆盖安装 → 报版本号。
书签、扩展、设置**全部保留**。

## 四、报错对照表（出事先来这查）

| 现象                                       | 是什么                             | 怎么办                                     |
| ------------------------------------------ | ---------------------------------- | ------------------------------------------ |
| `依赖: brave-keyring 但无法安装`           | 缺占位钥匙                         | 跑第三步的 ②                               |
| `无法被用户'_apt'访问…提权为根用户`        | **警告不是错误**，apt 自己绕过去了 | 不用管                                     |
| 下载只有 200KB/s、`CN:2`                   | GitHub 源只给 2 条连接             | 确认已装 aria2；脚本已默认走 gh-proxy      |
| 双击 .deb 没反应                           | 图形安装器遇依赖错就哑了           | 永远用 `sudo apt-get install -y ./xxx.deb` |
| `没有那个文件`：brave-browser-release.list | 以前没用官方源装过                 | 不是错，跳过                               |

## 五、卸载（哪天不要了）

```bash
sudo apt remove --purge brave-browser brave-keyring
rm -rf ~/.config/BraveSoftware        # 连个人数据一起清（想保留书签就别删这行）
```

## 六、路径对账表

| 东西                           | 在哪                                                  |
| ------------------------------ | ----------------------------------------------------- |
| 程序本体                       | `/opt/brave.com/brave/`                               |
| 启动入口                       | `/usr/bin/brave-browser`                              |
| 个人数据（书签/扩展/密码）     | `~/.config/BraveSoftware/`                            |
| 下载的安装包（更新断点续传用） | `~/Downloads/brave-deb/`                              |
| 一键脚本                       | `/mnt/winc/WorkBuddyData/wsqw_UOS/Network/装Brave.sh` |

***gh-proxy.com**：GitHub 下载加速，用法 = 原链接前面拼上 `https://gh-proxy.com/`
