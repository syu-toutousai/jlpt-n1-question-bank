# 来源校对日志 (Source Log)

每次根据互联网资源核对用户录入内容时，在此记录。**只记录非版权元数据**；
下载的版权材料（PDF/图片/答案档）放入本地 `refs/`（gitignore 排除，绝不推送），
本文件本身可入库。

## 索引

| 日期 | 范围 | 来源 URL | 校对结论 | 本地文件 (refs/) |
|------|------|----------|----------|------------------|
| 2026-09-06 | 2024年7月 N1 全部答案速查（词汇/语法/读解/听力） | https://www.diliushixian.com/information/4374.html | 参照（与羊驼有1处差异，见下） | refs/2024-07_answerkey_diliushixian.md |
| 2026-09-06 | 2024年7月 N1 答案速查（羊驼） | https://www.youtibao.net/kaoshi/nxkalqgph3.html | 抓取失败，内容来自搜索摘要；题8应为4 | refs/2024-07_answerkey_youtibao.md |
| 2026-09-06 | 2024年7月 N1 逐题题干+选项+答案+解析（笔试全95题+听力） | https://www.jlptzhen.com/n1%E7%9C%9F%E9%A2%98%E5%9C%A8%E7%BA%BF%E5%81%9A2024%E5%B9%B407%E6%9C%88%E6%97%A5%E6%9C%AC%E8%AF%AD%E8%83%BD%E5%8A%9B%E8%AF%95%E9%AA%8C/ | 录入时逐题对照的首选源 | refs/2024-07_jlptzhen_full.html |
| 2026-09-06 | 2024-07 N1 文法/読解 逐题 | https://passjapanese.com/en/jlpt/n1/exam/2024-07-grammar-reading | 在线参照（未存档） | - |
| 2026-09-06 | 2024-07 N1 聴解 逐题 | https://passjapanese.com/en/jlpt/n1/exam/2024-07-listening | 在线参照（未存档） | - |
| 2026-09-06 | 2024-07 N1 词汇/语法/读解答案（沪江） | https://jp.hujiang.com/nenglikaon1/p1439200/ 等 | 在线参照（未存档） | - |
| 2026-09-06 | 学习材料语注生成：MOJi辞書（读音/释义/JLPT例句+TTS） | https://www.mojidict.com （本地 moji CLI 查询） | 逐词查询，用于生成 analysis/2024-07-vocab-reading-words.md | - |
| 2026-09-06 | 学习材料例句生成：Nadeshiko 动漫/日剧台词库（含截图/音频 URL） | https://nadeshiko.co （本地 nadeshiko CLI 查询） | 每个词条取 SAFE 等级例句，示例见 guides 说明 | - |
| 2026-09-07 | 2024-07 N1 词彙問題1全部题及答案词全文（含問題2 Q7-13 正确答案词） | http://aixinjp.com/a/lianxifangshi/zhentidaan/2024/0708/1143.html | ✅ Q7-13 答案（2・4・4・1・1・3・2）；Q8=返上4 与第六时限=2 相左，判定 4 | - |
| 2026-09-07 | 2024-07 N1 問題2 Q13 题干+4选项（骨折り/足手まとい/裏目/および腰） | https://nihongoaz.com/jlpt-n1-vocabulary-practice-test-30.html | ✅ 与 learnjapaneseaz 同源互证，答案=足手まとい | - |
| 2026-09-07 | 2024-07 N1 語彙・文法・読解 逐题（越南语题面，可核对 Q13 题干） | https://trynihongo.com/ja/de-thi-jlpt-tu-vung-ngu-phap-doc-hieu-n1-07-2024-q1353 | 参照（在线，未存档） | - |
| 2026-09-07 | 問題2 Q7-13 学习材料语注生成（正解7词＋干扰项21词）：MOJi辞書 | https://www.mojidict.com （本地 moji CLI，音频→~/moji_audio） | 逐词查询 → analysis/2024-07-vocab-context-words.md | - |
| 2026-09-07 | 問題2 Q7-13 学习材料例句/截图/音频：Nadeshiko | https://nadeshiko.co （本地 nadeshiko CLI） | SAFE 优先；繰り越す/低迷 无台词、および腰仅1条 | - |
| 2026-09-07 | 「足手まとい」标准读法确认 | コトバンク(大辞泉/精選版)・weblio | ✅ 通行读法 あしてまとい（「あしでまとい」とも）；moji 表记为 あしでまとい④ | www.kotobank.jp/word/足手纏い-424568 |

## 结论标记

- ✅ 已核对一致（附来源）
- ⚠️ 未能确认，保留用户录入原样
- ❌ 发现不符（修正或待用户确认）

## 归档规则

1. 下载/截图版权材料 → `refs/`（文件名格式：`YYYY-MM_科目_来源.ext`）
2. 在本表追加一行：范围、URL、结论、refs 文件名
3. 若某来源已失效，保留记录并将 URL 标记为「失效」