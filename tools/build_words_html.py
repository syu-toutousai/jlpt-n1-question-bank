#!/usr/bin/env python3
"""Build docs/vocab-words.html — standalone study page from the analysis markdown."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MD = ROOT / "analysis" / "2024-07-vocab-reading-words.md"
OUT = ROOT / "docs" / "vocab-words.html"

TITLE = "2024年7月 JLPT N1 問題1 語注・例句集"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def autolink(s):
    def repl(m):
        url = m.group(0)
        label = url
        if (url.endswith(".mp3") or url.endswith(".webp") or url.endswith(".png") or url.endswith(".jpg")):
            return f'<span class="url">{esc(url)}</span>'
        return f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(label)}</a>'
    return re.sub(r"https?://[^\s\u3000]+", repl, s)


def fmt_inline(s):
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return autolink(s)


def render(lines):
    body = []
    cards = 0
    dist = 0
    word_idx = 0
    q_idx = 0
    cur = None
    open_detail = False

    def close_card():
        nonlocal open_detail
        if open_detail:
            body.append("</div></details>")
            open_detail = False

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.startswith("# "):
            close_card()
            body.append(f'<h1>{esc(line[2:])}</h1>')
            continue
        if line.startswith("> "):
            close_card()
            body.append(f'<p class="note">{fmt_inline(line[2:])}</p>')
            continue
        if line == "---":
            close_card()
            body.append('<div class="hr"></div>')
            continue
        if line.startswith("## "):
            close_card()
            title = line[3:]
            if title.startswith(("题干速览", "干扰项一览", "干扰项")):
                body.append(f'<h2 class="sec">{esc(title)}</h2>')
            else:
                q_idx += 1
                body.append(f'<h2 class="sec" id="q{q_idx}">{esc(title)}'
                            f' <a class="qanchor" href="#q{q_idx}">#q{q_idx}</a></h2>')
            continue
        if line.startswith("### "):
            close_card()
            t = line[4:]
            if t.startswith("【干扰项】"):
                body.append('<div class="dist-h">⚑ 干扰项 查缺补漏（假名选项对应之真实汉字词）</div>')
                continue
            m = re.match(r"(.+?)（([^）]+)）", t)
            word = m.group(1) if m else t
            yomi = m.group(2) if m else ""
            word_idx += 1
            cards += 1
            is_dist = "　" in t
            if is_dist:
                dist += 1
            body.append(
                f'<details class="card" id="w-{esc(word)}" data-w="{esc(word)}"><summary>'
                f'<span class="wn">{esc(word)}</span>'
                f'{"<span class=\"wy\">" + esc(yomi) + "</span>" if yomi else ""}'
                f'{"<span class=\"tag\">干扰项</span>" if is_dist else ""}'
                f'</summary><div class="cbody">')
            open_detail = True
            cur = body
            continue
        if cur is None:
            continue
        # bullet lines
        m = re.match(r"^(\s*)[-*]\s+(.*)$", line)
        if m:
            depth = m.group(1).count(" ")
            if depth == 0:
                text = m.group(2)
                if text.startswith("**备注**"):
                    cur.append(f'<p class="kv note-p">{fmt_inline(text)}</p>')
                elif "：" in text and text.split("：")[0].startswith("**"):
                    label, rest = text.split("：", 1)
                    if label.strip("**") == "作品台词":
                        cur.append(f'<p class="kv drain">{fmt_inline(text)}</p>')
                    else:
                        cur.append(f'<p class="kv">{fmt_inline(label)}<span>：</span>{fmt_inline(rest)}</p>')
                else:
                    cur.append(f'<p>{fmt_inline(text)}</p>')
            elif depth == 2:
                t = m.group(2)
                if t.startswith("*") and t.endswith("*"):
                    cur.append(f'<p class="rare">{fmt_inline(t.strip("*"))}</p>')
                else:
                    cur.append(f'<div class="s-h"><span class="m-ico">🎬</span>{fmt_inline(t)}</div>')
            elif depth == 4:
                t = m.group(2)
                if t.startswith("EN:"):
                    cur.append(f'<div class="en">{fmt_inline(t)}</div>')
                elif t.startswith("≪"):
                    cur.append(f'<div class="meta">{fmt_inline(t)}</div>')
                elif "http" in t:
                    urls = re.findall(r"https?://[^\s\u3000]+", t)
                    au = None
                    img = None
                    for u in urls:
                        if u.endswith(".mp3"):
                            au = u
                        elif u.endswith((".webp", ".png", ".jpg")):
                            img = u
                    if au:
                        cur.append(f'<audio controls preload="none" src="{esc(au)}"></audio>')
                    if img:
                        cur.append(f'<img loading="lazy" src="{esc(img)}" alt="场景截图">')
                    if not au and not img:
                        cur.append(f'<div class="linkline">{fmt_inline(t)}</div>')
                else:
                    cur.append(f'<div class="meta">{fmt_inline(t)}</div>')
            else:
                cur.append(f'<p>{fmt_inline(m.group(2))}</p>')
            continue
        cur.append(f'<p>{fmt_inline(line)}</p>')
    close_card()
    return body, cards, dist


def main():
    text = MD.read_text(encoding="utf-8")
    body, cards, dist = render(text.splitlines())
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{TITLE}</title>
<style>
:root{{--bg:#f5f7fb;--card:#fff;--ink:#1c2333;--sub:#5b6478;--line:#e4e7f0;--acc:#4f6ef7;--acc2:#eef1ff;--warn:#e8590c;--ok:#1f9d55;--c:#7a4ff7}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:"PingFang SC","Hiragino Sans GB","Noto Sans CJK SC","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--ink);line-height:1.85}}
header{{background:linear-gradient(135deg,#33418f,#7a4ff7);color:#fff;padding:40px 20px 34px;text-align:center}}
header h1{{font-size:23px;letter-spacing:1.5px}}
header p{{opacity:.92;font-size:13.5px;margin-top:10px}}
header .tags span{{display:inline-block;background:rgba(255,255,255,.22);border-radius:99px;padding:3px 12px;font-size:12px;margin:12px 4px 0}}
main{{max-width:960px;margin:-14px auto 40px;padding:0 16px}}
.note{{background:var(--acc2);border-left:3px solid var(--acc);border-radius:10px;padding:10px 14px;font-size:13px;color:#38405a;margin:14px 0}}
h2.sec{{background:var(--card);border-radius:16px;box-shadow:0 4px 16px rgba(30,40,90,.08);padding:16px 20px;margin:22px 0 14px;font-size:16px;color:#33418f;border-left:5px solid var(--c);word-break:break-all}}
.qanchor{{font-size:12px;color:#a8aebc;font-weight:600;text-decoration:none;margin-left:8px}}
.qanchor:hover{{color:var(--acc)}}
details.card{{scroll-margin-top:64px}}
.dist-h{{background:#fff8f2;border:1.5px solid var(--warn);color:#c2410c;border-radius:12px;padding:9px 16px;margin:16px 0;font-size:13px;font-weight:700}}
details.card{{background:var(--card);border-radius:16px;box-shadow:0 4px 16px rgba(30,40,90,.08);margin:12px 0;border:1.5px solid var(--line);overflow:hidden}}
details.card>summary{{list-style:none;cursor:pointer;padding:14px 18px;font-size:16.5px;font-weight:700;display:flex;align-items:baseline;gap:12px}}
details.card>summary::-webkit-details-marker{{display:none}}
details.card>summary:hover{{background:var(--acc2)}}
details.card[open]>summary{{border-bottom:1px solid var(--line);background:var(--acc2)}}
.wn{{color:#33418f}}
.wy{{color:var(--c);font-size:14px;font-weight:600}}
.tag{{margin-left:auto;background:var(--warn);color:#fff;border-radius:99px;padding:2px 12px;font-size:11.5px;flex:none}}
.cbody{{padding:4px 18px 16px}}
.cbody p,.cbody div{{margin:7px 0;font-size:14px}}
.kv b{{color:var(--acc)}}
.note-p{{background:var(--acc2);border-radius:8px;padding:6px 10px;font-size:13px}}
.drain{{color:#7f2ff7}}
.en{{color:#5b6478;font-size:13px}}
.meta{{color:#5b6478;font-size:12.5px;word-break:break-all}}
.s-h{{font-size:15.5px;margin-top:12px!important}}
.m-ico{{margin-right:6px}}
.rare{{color:#e8590c;font-size:13px;background:#fff8f2;border-radius:8px;padding:6px 10px}}
audio{{width:100%;max-width:420px;height:40px;display:block;margin:8px 0}}
img{{max-width:280px;width:100%;border-radius:10px;border:1px solid var(--line);margin:6px 0;display:block;cursor:zoom-in}}
img:active{{transform:scale(1.6);transform-origin:top left;cursor:zoom-out}}
.linkline{{word-break:break-all;font-size:12.5px}}
.url{{color:var(--sub);font-size:11.5px;word-break:break-all}}
a{{color:var(--acc)}}
.hr{{border-top:2px dashed var(--line);margin:22px 0}}
.toolbar{{position:sticky;top:0;z-index:30;background:rgba(255,255,255,.94);backdrop-filter:blur(6px);border-bottom:1px solid var(--line);padding:10px 16px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}}
.toolbar input{{flex:1;min-width:200px;border:1.5px solid var(--line);border-radius:99px;padding:8px 16px;font-size:13.5px;outline:none;background:#fff}}
.toolbar .cnt{{font-size:12.5px;color:var(--sub);font-weight:600}}
footer{{text-align:center;font-size:12px;color:var(--sub);padding:18px}}
.hidden{{display:none!important}}
a.toplink{{color:#fff;opacity:.9;font-size:12.5px;text-decoration:underline}}
</style>
</head>
<body>
<header>
  <h1>{esc(TITLE)}</h1>
  <p>题干汉字词 × 有意义干扰项 ・ MOJi辞書 读音/释义/例句 ＋ Nadeshiko 动漫日剧真实台词</p>
  <div class="tags"><span>{cards} 词条</span><span>{dist} 干扰项（{cards - dist} 题干词）</span><span>音频/截图可直接播放</span></div>
</header>
<div class="toolbar">
  <input id="q" placeholder="🔍 搜索词条 / 读音 / 例句…">
  <span class="cnt" id="cnt"></span>
</div>
<main id="main">
{chr(10).join(body)}
</main>
<footer>学习材料由 moji × nadeshiko 生成・仅供个人备考学习 ・ <a href="index.html">← 返回题库首页</a></footer>
<script>
const cards=[...document.querySelectorAll('details.card')];
const cnt=document.getElementById('cnt');
function apply(){{
 const k=document.getElementById('q').value.trim().toLowerCase();
 let shown=0;
 cards.forEach(c=>{{const hit=c.dataset.w.includes(k)||c.textContent.toLowerCase().includes(k);c.classList.toggle('hidden',!hit);if(hit)shown++;}});
 cnt.textContent=shown+' / '+cards.length;
}}
document.getElementById('q').addEventListener('input',apply);
apply();
</script>
</body>
</html>"""
    OUT.write_text(html, encoding="utf-8")
    print(f"WROTE {OUT}  [{cards}] cards, {dist} distractor + {cards - dist} stem words, {len(html)//1024} KB")


if __name__ == "__main__":
    main()