# WorkBuddy 签到技能在 Linux 上的结论（实测）

- 日期：2026-11-02
- 环境：deepin 25 / Linux，客户端 codebuddy / WorkBuddy
- 技能：`totorosir-workbuddy-checkin` v3.1.7
- 结论：**Linux 上跑不通，签到请手动点。**

---

## 一句话结论

签到需要接口令牌；令牌在登录态文件里是加密的；解密密钥只有 **Windows** 能从客户端进程内存取得。Linux 上没有任何本地途径拿到这把密钥，所以 automate 不了。

---

## 排查过程与实测数据

| 步骤 | 结果 |
|---|---|
| `auto_checkin.py --probe` | 三通道全不可用，`recommendation: need_setup` |
| 找登录态文件 | 实际位置 `~/.local/share/CodeBuddyExtension/Data/Public/auth/workbuddy-desktop.info`；脚本只查 `~/.config/...` 与 `~/.workbuddy/auth/`，故报「共 0 个」 |
| 建软链接后重试 | 找到 1 个候选，但报「无法在本机定位 atRestSecretKey（已尝试 0 个 DPAPI blob 与运行中客户端进程内存扫描）」 |
| 通道 B（网页授权） | `www.workbuddy.cn` 打开只是官网下载页，**没有登录界面**，取不到会话 |
| 已有 atrest.key | 10 月 13 日遗留的 root 文件，keyId 与当前登录态不匹配 |

## 技能本身的两处缺口

1. **Linux 路径遗漏**：登录态实际在 `~/.local/share/CodeBuddyExtension/`，脚本候选列表没有这一条。
2. **通道 B 前提不成立**：文档假设能在 `www.workbuddy.cn` 登录，实际该站无登录入口，所以 Linux / macOS 上这条兜底路也是死的。

## 可用的做法

- **手动签到**：客户端左下角「个人信息 → Buddy 加油站 → 签到」，每天 +100。
- **要在 Windows 上跑**：同一脚本零配置，密钥可从进程内存取。

## Linux 与 Windows 的差别（这次踩到的）

| 项 | Windows | Linux |
|---|---|---|
| 登录态路径 | `%LOCALAPPDATA%\CodeBuddyExtension\...` | 实际 `~/.local/share/CodeBuddyExtension/...`（脚本没写这条） |
| 加密密钥来源 | 可从客户端进程内存读 | 无本地途径 |
| 网页授权兜底 | 可用（官网有登录） | 不可用 |

## 清理状态

- 软链接 `~/.config/CodeBuddyExtension/...` 已删除
- `~/.workbuddy/scripts/` 已删除（含旧的 atrest.key，无用途，不影响客户端）
- 真实登录态文件完好，客户端账号不受影响
