#!/bin/bash
# ============================================================
#  aria2 图形下载器 · 停止
#  先让 aria2 把任务清单存好再退，下次启动接着下
# ============================================================

curl -s --noproxy '*' --max-time 3 -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":"1","method":"aria2.shutdown"}' \
  "http://127.0.0.1:6800/jsonrpc" >/dev/null 2>&1

for i in $(seq 1 8); do
  pgrep -f "aria2c.*--enable-rpc" >/dev/null || break
  sleep 0.5
done

pgrep -f "aria2c.*--enable-rpc" >/dev/null && pkill -f "aria2c.*--enable-rpc"

notify-send "aria2 下载器" "已停止。没下完的任务记在 aria2.session 里，下次启动自动接着下。" 2>/dev/null
