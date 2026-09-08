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
| 2026-09-08 | 全 58 词卡辞典発音内嵌（MOJi 词条 TTS，_w_ 音频→data URI，覆盖 問題1/問題2 全部卡片；另补下 29 词词条发音） | https://www.mojidict.com （本地 moji CLI，音频库 ~/moji_audio） | ✅ 58/58 内嵌，mp3 校验通过 | - |
| 2026-09-08 | 题干速览 13 条题干文の発音（Edge TTS ja-JP-NanamiNeural，→~/edge_tts_examples）＋ 例文29条合成与 27条MOJi原声 | https://www.mojidict.com / edge-tts | ✅ 13 题干 + 56 例文（27 原声/29 合成）全部发音内嵌 | - |
| 2026-09-08 | 学习页発音ボタン内联化（词/例句/台词/题干 直后按钮，去标签）＋ 发行源凡例区分（MOJi 蓝 / Edge 橙 / Nadeshiko 绿） | 生成器 tools/build_words_html.py | ✅ js 交互/几何位置验证通过；修复题干速览行此前未渲染的问题 | - |
| 2026-09-08 | 2024年12月 N1 真題全文（笔试 問題1-13 共66题，逐句原文） | https://jlpt247.com/n1-jlpt-12-2024/ | ✅ 主题干出处；无正确标记，答案另行交叉核对 | refs/2024-12_jlpt247_full.html |
| 2026-09-08 | 2024年12月 N1 答案66题（数字+选项文本，含並べ替え重建句） | http://aixinjp.com/a/lianxifangshi/zhentidaan/2024/1203/1172.html | ✅ 主答案源；问题1-7/8-13 选项文本逐一匹配；Q34键标③系笔误(自引文本=选项2)；Q13=3とっさに | refs/2024-12_answerkey_aixinjp.html |
| 2026-09-08 | 2024年12月 N1 文字・語彙/文法答案 Q1-44（第二大源） | https://learnjapaneseaz.com/jlpt-n1-12-2024.html | ⚠️ 与aixinjp Q1-44全符，唯一分歧 Q13=1じきに(疑误)；读解未收录 | refs/2024-12_answerkey_learnjapaneseaz.html |
| 2026-09-08 | 2024年12月 N1 答案（第六时限）——页面正文无答案内容 | https://www.diliushixian.com/information/4519.html | ⚠️ 空页（未发布答案），仅存档 | refs/2024-12_answerkey_diliushixian.html |
| 2026-09-08 | 2024年12月 N1 答案（沪江语法/读解） | https://jp.hujiang.com/nenglikaon1/p1443106/ 、 m.hujiang.com/jp_nenglikaoN1/p1443108/ | ⚠️ 页面无正文（仅导航，JS渲染），未采用 | refs/2024-12_answerkey_hujiang_gram.html |
| 2026-09-08 | 2024年12月 N1 答案（nihongoaz / 新干线） | https://nihongoaz.com/jlpt-n1-12-2024.html 、 https://www.xgxedu.com/html/kszx/6401.html | ⚠️ 无正文（JS渲染/GBK图片），未采用 | refs/2024-12_answerkey_nihongoaz.html 、 refs/2024-12_answerkey_xgxedu.html |
| 2026-09-08 | 常用漢字表 本表 2136字（字種・音訓・例・備考，H22内閣告示） | https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/kanji/joyokanjisakuin/index.html | ✅ 公表HTML、Shift_JIS、2136行；生成 data/joyo-kanji-2136.json 的元数据（例=音訓索引原文，弥/朕/阜等が例無し、極 は〔副〕を例に合流） | refs/joyo_kanji_sakuin_bunkacho.html |
| 2026-09-08 | 学年（教育漢字1026字）＝文部科学省 H29 学習指導要領 学年別漢字配当表 | https://fragment-database.com/kanji.html | ✅ 1年80/2年160/3年200/4年202/5年193/6年191（計1026）；残り1110字→中学(7)。Wikipedia 常用漢字一覧 と学年0差分 | refs/joyo_gakunenbetsu_haitou_fragment-db.html |
| 2026-09-08 | 総画数＝Unicode UCD Unihan kTotalStrokes（国際基準） | https://www.unicode.org/Public/15.1.0/ucd/Unihan.zip | ✅ 2136/2136 全収録；日本の辞書画数（以=5画など）と175字で相違（meta.caveats に記載） | refs/unihan/ |
| 2026-09-08 | 部首＝Unicode UCD 8.0 Unihan kRSKangXi（康熙214部首） | https://www.unicode.org/Public/8.0.0/ucd/Unihan.zip | ✅ 2136/2136 全収録；部首名は康熙214部首表（日本語常用形） | refs/unihan8/ |
| 2026-09-08 | 独立クロスチェック：ja.wikipedia 常用漢字一覧（部首/総画/学年） | https://ja.wikipedia.org/wiki/%E5%B8%B8%E7%94%A8%E6%BC%A2%E5%AD%97%E4%B8%80%E8%A6%A7 | ✅ 学年0差分；部首名は大体KangXi一致（ウィキの部首帰属に方言あり医→酉等）；画数の JP 流は UCD と175字相違（上述 caveat 根拠） | - |
| 2026-09-08 | 2024年7月 N1 聴解フル音声（問題1-5 全30問，128kbps 51:56） | 百度网盘（用户上传 baidupcs 云端 `2013-2021年N1音频/2024年7月新日语能力考试 N1.mp3`，47.55MB） | ✅ ローカル archive のみ（refs/、gitignore・不推送）；本页聴解音声は per-Q リモートURL（jlptzhen.com 202407N10X_Y.mp3，29/29 200 OK）を引き続き使用 | refs/2024-07_listening_baidupcs.mp3 |

## 结论标记

- ✅ 已核对一致（附来源）
- ⚠️ 未能确认，保留用户录入原样
- ❌ 发现不符（修正或待用户确认）

## 归档规则

1. 下载/截图版权材料 → `refs/`（文件名格式：`YYYY-MM_科目_来源.ext`）
2. 在本表追加一行：范围、URL、结论、refs 文件名
3. 若某来源已失效，保留记录并将 URL 标记为「失效」

## 衍生数据（無版权・可入库）

| 日期 | 范围 | 来源 | 结论 | 本地文件 |
|------|------|------|------|----------|
| 2026-09-08 | 2024-07+2024-12 全问题バンク 162 问 漢字走査（语幹/选项/正解/読解パッセージ/聴解原文・カナ行のみ） | `past-exams/**/*.json`（自録） | 1070 字（語彙480・文法394・読解754・聴解570），表外 23 字 | `joyokanjihyo-annotated/data/kanji_labels.json` |
| 2026-09-08 | 表外漢字 23 字の音・訓（付録用） | Unihan 8.0 `kJapaneseKun` / `kJapaneseOn`（`refs/unihan8/Unihan_Readings.txt`） | 例（问题バンクの実例）とともに `tools/annotate_pdf.py::EXTRA` に反映 | `refs/unihan8/Unihan_Readings.txt` |