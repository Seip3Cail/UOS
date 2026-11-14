#!/bin/bash
# ============================================================
#  aria2 图形下载器 · 启动
#  双击本文件 → 后台起 aria2 → 自动打开浏览器遥控页面
# ============================================================

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOWN_DIR="$HOME/下载"              # 默认保存位置，页面里也能随时改
SESSION="$APP_DIR/aria2.session"   # 任务清单：关掉再开，没下完的接着下
LOG="$APP_DIR/aria2.log"
PORT=6800

mkdir -p "$DOWN_DIR"

# 已经在跑 → 只开页面，不重复启动
if pgrep -f "aria2c.*--enable-rpc" >/dev/null; then
  xdg-open "$APP_DIR/index.html" >/dev/null 2>&1
  exit 0
fi

ARGS=(
  --enable-rpc                              # 打开遥控接口
  --rpc-listen-port=$PORT                   # 端口 6800
  --rpc-listen-all=false                    # 只允许本机连，外人连不上
  --rpc-allow-origin-all                    # 允许网页页面调用
  -x16 -s16                                 # 每个文件分 16 段、每段 16 条连接（提速主力）
  -j5                                       # 同时下 5 个任务，多的排队
  --continue=true                           # 断点续传
  --dir="$DOWN_DIR"                         # 默认存这里
  --save-session="$SESSION"                 # 任务清单存盘
  --save-session-interval=30                # 每 30 秒存一次
  --force-save=true                         # 退出时强制存一次
)

[ -f "$SESSION" ] && ARGS+=(--input-file="$SESSION")   # 有旧清单就接着下

setsid nohup aria2c "${ARGS[@]}" >"$LOG" 2>&1 < /dev/null &
disown

# 等接口就绪（最多 5 秒）
OK=0
for i in $(seq 1 20); do
  curl -s --noproxy '*' --max-time 1 -o /dev/null -H 'Content-Type: application/json' \
    -d '{"jsonrpc":"2.0","id":"1","method":"aria2.getVersion"}' \
    "http://127.0.0.1:$PORT/jsonrpc" && { OK=1; break; }
  sleep 0.25
done

if [ "$OK" = "1" ]; then
  notify-send -t 3000 "aria2 下载器" "已启动，正在打开遥控页面"
  xdg-open "$APP_DIR/index.html" >/dev/null 2>&1
else
  notify-send -t 8000 -u critical "aria2 下载器" "启动失败，看本目录 aria2.log 最后几行"
  xdg-open "$APP_DIR/aria2.log" >/dev/null 2>&1
fi
