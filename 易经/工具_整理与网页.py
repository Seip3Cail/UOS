#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
曾仕强《易经的智慧》听讲笔记 —— 改名 + 网页版
================================================
跑一次干两件事：
  1) booknotes/ 里的笔记文件名统一加上集号（和你视频文件上的编号一致），只改名、不删除；
  2) 生成【网页版】笔记.html —— 双击就能在浏览器里点着看，不依赖 VS Code。

可以反复跑：改过名的、生成过的，第二遍自动跳过。
以后每做完一篇新笔记，再跑一遍，网页版自动把新篇收进去。

用法（deepin 终端里敲这一行）：
  python3 /mnt/winc/WorkBuddyData/wsqw_UOS/易经/工具_整理与网页.py
"""
import os
import re
import html
import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.join(BASE, "booknotes")

# ---------------------------------------------------------------
# 1) 旧文件名 → 新文件名（新名 = 视频集号 + 原名）
#    同一集有两篇的（屯、蒙），共用同一个集号。
# ---------------------------------------------------------------
RENAMES = [
    ("易经：001阴阳之道.md",        "001_阴阳之道.md"),
    ("易经：002八卦定乾坤.md",      "002_八卦定乾坤.md"),
    ("易经与命运.md",               "003_易经与命运.md"),
    ("破解占卦.md",                 "004_破解占卦.md"),
    ("乾坤卦.md",                   "005_乾坤卦.md"),
    ("乾卦六龙.md",                 "006_乾卦六龙.md"),
    ("六龙御天.md",                 "007_六龙御天.md"),
    ("乾卦——孔子的文言传.md",      "008_乾卦——孔子的文言传.md"),
    ("坤卦.md",                     "009_坤卦.md"),
    ("坤卦——地道柔刚.md",          "010_坤卦——地道柔刚.md"),
    ("乾坤之道.md",                 "011_乾坤之道.md"),
    ("屯卦——始生之难.md",          "012_屯卦——始生之难.md"),
    ("屯卦——创始之道.md",          "012_屯卦——创始之道.md"),
    ("蒙卦——蒙以养正.md",          "013_蒙卦——蒙以养正.md"),
    ("蒙卦——教化之道.md",          "013_蒙卦——教化之道.md"),
    ("需卦——需要等待.md",          "014_需卦——需要等待.md"),
    ("需卦——待机之道.md",          "015_需卦——待机之道.md"),
    ("讼卦——争强好胜.md",          "016_讼卦——争强好胜.md"),
    ("讼卦——化除讼累.md",          "017_讼卦——化除讼累.md"),
    ("师卦——师忧比乐.md",          "018_师卦——师忧比乐.md"),
    ("师卦——师出正道.md",          "019_师卦——师出正道.md"),
    ("比卦——亲比和谐.md",          "020_比卦——亲比和谐.md"),
    ("比卦——情投意合.md",          "021_比卦——情投意合.md"),
    ("小畜卦——小有畜聚.md",        "023_小畜卦——小有畜聚.md"),
    ("小畜卦——以小养大.md",        "024_小畜卦——以小养大.md"),
    ("履卦——实践天道.md",          "025_履卦——实践天道.md"),
    ("履卦——柔能克刚.md",          "026_履卦——柔能克刚.md"),
    ("泰卦——天下太平.md",          "027_泰卦——天下太平.md"),
    ("泰卦——君子的责任.md",        "028_泰卦——君子的责任.md"),
    ("否卦——否从泰来.md",          "029_否卦——否从泰来.md"),
    ("否卦——无道则愚.md",          "030_否卦——无道则愚.md"),
    ("泰否综述——否极泰来.md",      "031_泰否综述——否极泰来.md"),
]

# 总论那几集（不落卦的），网页版里单独归一组
ZONGLUN = {1, 2, 3, 4, 5, 8, 11, 31}


def do_rename():
    """按对照表改名；顺手把【目录】点着看.md 里的链接也换成新名。"""
    done = kept = 0
    for old, new in RENAMES:
        po = os.path.join(BOOK, old)
        pn = os.path.join(BOOK, new)
        if os.path.exists(pn):
            kept += 1
            continue
        if os.path.exists(po):
            os.rename(po, pn)
            done += 1
    print("改名：%d 个（%d 个本来就是新名，跳过）" % (done, kept))

    # 目录页里的链接同步换新名
    mulu = os.path.join(BASE, "【目录】点着看.md")
    if os.path.exists(mulu):
        with open(mulu, encoding="utf-8") as f:
            text = f.read()
        n = 0
        for old, new in RENAMES:
            a, b = "booknotes/" + old, "booknotes/" + new
            if a in text:
                text = text.replace(a, b)
                n += 1
        if n:
            with open(mulu, "w", encoding="utf-8") as f:
                f.write(text)
            print("目录页链接同步：%d 处换成新名" % n)


# ---------------------------------------------------------------
# 2) Markdown → HTML（只覆盖笔记里用得到的写法，不引外部库）
# ---------------------------------------------------------------
def fix_img(src):
    src = src.strip().strip("<>").replace("../images/", "images/")
    return src


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)",
               lambda m: '<img src="%s" alt="%s">' % (fix_img(m.group(2)), m.group(1)),
               s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
               lambda m: '<a href="%s">%s</a>' % (m.group(2), m.group(1)),
               s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


IMG_ONLY = re.compile(r"^\s*!\[[^\]]*\]\([^)]+\)\s*$")
IMG_ANY = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")


def md_to_html(text):
    out = []
    stack = []          # 每层记：是不是有序列表
    grid = False        # 是不是正开着图片格

    def close_to(depth):
        while len(stack) > depth:
            out.append("</ol>" if stack.pop() else "</ul>")

    def close_grid():
        nonlocal grid
        if grid:
            out.append("</div>")
            grid = False

    for raw in text.splitlines() + [""]:
        line = raw.rstrip()

        # 一张图独占一行 → 收进图片格：连着的几张并排成格，省地方
        if IMG_ONLY.match(line):
            close_to(0)
            if not grid:
                out.append('<div class="grid">')
                grid = True
            mi = IMG_ANY.search(line)
            out.append('<img src="%s" alt="%s">'
                       % (fix_img(mi.group(2)), html.escape(mi.group(1), quote=True)))
            continue

        # 空行：图与图之间隔的空行不断组；别处的空行收掉列表
        if not line.strip():
            if grid:
                continue
            close_to(0)
            continue

        m = re.match(r"^(\s*)([-*+]|\d+[.、])\s+(.*)$", line)
        if m:
            close_grid()
            width = len(m.group(1).replace("\t", "  "))
            depth = width // 2 + 1
            ordered = m.group(2)[0].isdigit()
            if depth > len(stack):
                while len(stack) < depth:
                    stack.append(ordered)
                    out.append("<ol>" if ordered else "<ul>")
            else:
                close_to(depth)
                if stack and stack[-1] != ordered:
                    out.append("</ol>" if stack.pop() else "</ul>")
                    stack.append(ordered)
                    out.append("<ol>" if ordered else "<ul>")
            out.append("<li>%s</li>" % inline(m.group(3)))
            continue

        close_grid()
        close_to(0)

        if line.strip() == "---":
            out.append("<hr>")
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            lv = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (lv, inline(m.group(2)), lv))
            continue
        if line.startswith(">"):
            out.append("<blockquote>%s</blockquote>" % inline(line.lstrip("> ").strip()))
            continue
        out.append("<p>%s</p>" % inline(line.strip()))
    close_grid()
    return "\n".join(out)


def note_num(fn):
    m = re.match(r"(\d+)", fn)
    return int(m.group(1)) if m else 9999


def note_title(fn, text):
    """侧栏标题：优先取文件名里的标题（NNN_标题.md），没编号才回落到正文第一个 #。"""
    stem = os.path.splitext(fn)[0]
    m = re.match(r"^\d+[_\-\s]*(.+)$", stem)
    if m and m.group(1).strip():
        return m.group(1).strip()
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return stem


CSS = """
*{box-sizing:border-box}
body{margin:0;background:#faf9f7;color:#2b2b2b;font-size:16px;line-height:1.9;
     font-family:'Noto Sans CJK SC','Source Han Sans SC','Microsoft YaHei',sans-serif}
/* ---------- 左侧目录 ---------- */
#side{position:fixed;left:0;top:0;bottom:0;width:290px;overflow:auto;
      background:#f0ede8;border-right:1px solid #ddd;padding:18px 14px}
#side h1{font-size:17px;line-height:1.4;margin:0 0 3px;color:#4a3f33}
#side .meta{font-size:12px;line-height:1.6;color:#989082;margin:0 0 8px}
#side h2{font-size:13px;line-height:1.4;color:#8a7f6f;margin:16px 0 5px;
         border-bottom:1px solid #ddd;padding-bottom:3px}
#side a{display:block;padding:4px 9px;font-size:14px;line-height:1.5;
        color:#3d3a35;text-decoration:none;border-radius:5px}
#side a:hover{background:#e2ddd4}
#side a.on{background:#b5544a;color:#fff}
/* ---------- 正文区 ---------- */
main{margin-left:290px;padding:34px 46px;max-width:960px}
.note{display:none}
.note .crumb{font-size:13px;color:#a29889;margin:0 0 12px;text-indent:0}
.note h1,.note h2,.note h3,.note h4,.note h5,.note h6{
     margin:1.1em 0 .45em;line-height:1.6;letter-spacing:.2px;
     color:#2f2a24;text-indent:0}
.note h1{font-size:22px;font-weight:600;margin-top:.1em;
     padding-bottom:8px;border-bottom:2px solid #b5544a}
.note h2{font-size:17px;font-weight:400;margin-top:1.4em;
     padding-left:10px;border-left:4px solid #b5544a}
.note h3,.note h4,.note h5,.note h6{font-size:16px;font-weight:400;
     margin:.7em 0 .3em;color:#2f2a24}
.note p{margin:.55em 0;text-indent:2em}
.note p:has(img){text-indent:0}
.note ul,.note ol{margin:.35em 0 .9em;padding-left:1.7em}
.note li{margin:.18em 0;line-height:1.85}
.note li>ul,.note li>ol{margin:.18em 0}
.note strong{font-weight:600;color:#1f1c18}
.note blockquote{margin:.8em 0;padding:.3em 14px;text-indent:0;
     border-left:3px solid #c9c2b5;background:#f3f0ea;color:#666}
.note code{padding:1px 6px;font-size:14px;border-radius:3px;background:#ece9e2}
.note hr{margin:1.5em 0;border:none;border-top:1px dashed #ccc}
/* ---------- 配图：一律统一小图（居中裁切），鼠标划上看大图 ---------- */
.note img{width:160px;height:120px;object-fit:cover;object-position:center;
     margin:3px 6px 3px 0;vertical-align:middle;background:#f6f3ee;
     border:1px solid #ddd;border-radius:4px;cursor:zoom-in}
.note img:hover{border-color:#b5544a}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));
     gap:6px;margin:.6em 0;text-indent:0}
.grid img{width:100%;height:120px;margin:0;display:block}
#imgzoom{position:fixed;left:0;top:0;right:0;bottom:0;z-index:99;cursor:zoom-out;
     display:flex;align-items:center;justify-content:center;background:rgba(28,25,20,.88)}
#imgzoom img{width:auto;height:auto;max-width:94vw;max-height:94vh;margin:0;
     border:none;border-radius:4px;cursor:zoom-out;box-shadow:0 10px 50px rgba(0,0,0,.6)}
"""


def do_html():
    if not os.path.isdir(BOOK):
        print("找不到 booknotes/，网页版没生成。")
        return
    files = sorted(
        (f for f in os.listdir(BOOK) if f.endswith(".md")),
        key=lambda f: (note_num(f), f),
    )
    notes = []
    for fn in files:
        with open(os.path.join(BOOK, fn), encoding="utf-8") as f:
            text = f.read()
        notes.append((note_num(fn), fn, note_title(fn, text), md_to_html(text)))

    side = ['<h1>易经的智慧 · 听讲笔记</h1>',
            '<p class="meta">%d 集 · %d 篇<br>网页生成于 %s</p>'
            % (len({n[0] for n in notes}), len(notes),
               datetime.date.today().strftime("%Y-%m-%d"))]
    body = []
    for group, picks in (("总论（不落卦）", [n for n in notes if n[0] in ZONGLUN]),
                         ("按卦走", [n for n in notes if n[0] not in ZONGLUN])):
        if not picks:
            continue
        side.append("<h2>%s</h2>" % group)
        for num, fn, title, _ in picks:
            i = len(body)
            if num == 9999:
                side.append('<a href="#n%d">%s</a>' % (i, html.escape(title)))
                crumb = ""
            else:
                side.append('<a href="#n%d">%03d %s</a>' % (i, num, html.escape(title)))
                crumb = '<p class="crumb">第 %03d 集 · %s</p>' % (num, html.escape(title))
            body.append('<section class="note" id="n%d">%s%s</section>' % (i, crumb, _))

    page = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>易经的智慧 · 听讲笔记</title>
<style>%s</style>
</head>
<body>
<nav id="side">%s</nav>
<main>%s</main>
<script>
var links=document.querySelectorAll('#side a');
links.forEach(function(a){
  a.addEventListener('click',function(e){
    e.preventDefault();
    document.querySelectorAll('.note').forEach(function(n){n.style.display='none';});
    links.forEach(function(x){x.classList.remove('on');});
    var t=document.querySelector(a.getAttribute('href'));
    if(t){t.style.display='block';}
    a.classList.add('on');
    window.scrollTo(0,0);
  });
});
if(links.length){links[0].click();}
document.querySelectorAll('.note img').forEach(function(im){
  im.addEventListener('mouseenter',function(){
    var ov=document.createElement('div');ov.id='imgzoom';
    var big=document.createElement('img');big.src=im.src;
    ov.appendChild(big);
    ov.addEventListener('click',function(){ov.remove();});
    document.body.appendChild(ov);
  });
  im.addEventListener('mouseleave',function(){
    var ov=document.getElementById('imgzoom');if(ov){ov.remove();}
  });
});
</script>
</body>
</html>
""" % (CSS, "\n".join(side), "\n".join(body))

    out = os.path.join(BASE, "【网页版】笔记.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    print("网页版：%s（%.0f KB）" % (os.path.basename(out), os.path.getsize(out) / 1024))


if __name__ == "__main__":
    print("=== 易经笔记：改名 + 网页版 ===")
    do_rename()
    do_html()
    print("完成。网页版在易经文件夹里，双击【网页版】笔记.html 就能看。")
