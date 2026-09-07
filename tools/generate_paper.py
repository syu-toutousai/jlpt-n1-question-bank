#!/usr/bin/env python3
"""Generate per-question plaintext JSON from a refs/ session source.

Input source, tried in order:
    1. refs/<session>_full_jlptzhen.json   (jlptzhen quiz pages, 2024-07 …)
    2. refs/<session>_jlpt247.json         (jlpt247 verbatim transcription)

writes one JSON per question to past-exams/<year>/<month>/<section>/<type>_<NN>.json.

Existing files are NEVER overwritten unless --force (files may hold manual
user edits, e.g. the Q8 stem hiragana correction) — see AGENTS.md §4.

The jlptzhen quiz pages interleave the 聴解 blocks under the same 問題1–5
headings (no "聴解" prefix); questions carrying an audio URL belong to the
listening block, the earlier ones (with num) to the written block.

Standard N1 (2010+) written paper (verified against 2024-07/2024-12):
  文字語彙  問題1 reading(1–6) 問題2 context(7–13) 問題3 paraphrase(14–19)
            問題4 usage(20–25)
  文法      問題5 choice(26–35) 問題6 composition(36–40) 問題7 passage(41–44)
  読解      問題8 short(45–48) 問題9 mid(49–56) 問題10 long(57–59)
            問題11 long(60–61) 問題12 long(62–64) 問題13 long(65–66)
  聴解      問題1 point(課題理解) … 問題5 implication(統合理解)  (local 1..N)

Usage:
    python3 tools/generate_paper.py 2024-07 [--force]
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REFS = ROOT / "refs"
PAST = ROOT / "past-exams"

# (問題N, repo section, type, group size). Group sizes drive the official
# global numbering for blocks whose stems carry no number.
GROUPS = [
    ("問題1", "vocab", "reading", 6),
    ("問題2", "vocab", "context", 7),
    ("問題3", "vocab", "paraphrase", 6),
    ("問題4", "vocab", "usage", 6),
    ("問題5", "grammar", "choice", 10),
    ("問題6", "grammar", "composition", 5),
    ("問題7", "grammar", "passage", 4),
    ("問題8", "reading", "short", 4),
    ("問題9", "reading", "mid", 8),
    ("問題10", "reading", "long", 3),
    ("問題11", "reading", "long", 2),
    ("問題12", "reading", "long", 3),
    ("問題13", "reading", "long", 2),
]
SECTION_JP = {"vocab": "言語知識(文字・語彙)", "grammar": "言語知識(文法)",
              "reading": "読解", "listening": "聴解"}
LISTEN_TYPE = {1: "point", 2: "grammar", 3: "overview", 4: "detailed", 5: "implication"}
DIFFICULTY = {"問題1": "easy", "問題2": "medium", "問題3": "medium", "問題4": "medium",
              "問題5": "medium", "問題6": "medium", "問題7": "medium",
              "問題8": "hard", "問題9": "hard",
              "問題10": "medium", "問題11": "medium", "問題12": "medium", "問題13": "medium"}
TAGS_EXTRA = {"reading": ["読み方", "漢字"], "context": ["言葉の意味", "文脈規定"],
              "paraphrase": ["言い換え"], "usage": ["使い方"], "choice": ["文法選択"],
              "composition": ["並べ替え"], "passage": ["文章の文法"]}

# Known gaps inside a quiz page, filled from independent transcriptions.
# Real past-exam material, verified against the cited sources.
EXTRA = {
    ("2024-07", "問題2"): [
        {
            "num": 13,
            "stem": "登山に誘われたが、あまり経験がないので、みんなの（　　）になると思い、断った。",
            "target": "足手まとい",
            "options": ["骨折り", "足手まとい", "裏目", "および腰"],
            "answer": 2,
            "explanation": "「足手まといになる」＝他人の進行をじゃまする役目。答えは2)。",
            "notes": "jlptzhen 存档缺本题(17913缺失)，题干/选项来自 jlpt247 全文転写，答案与両答案键第7位=2 一致。",
            "extra_sources": ["https://jlpt247.com/n1-jlpt-7-2024/ (全文転写)",
                              "refs/2024-07_answerkey_diliushixian.md (問題2=2241132)",
                              "refs/2024-07_answerkey_youtibao.md (問題2=2441132)"],
        }
    ],
}

# per (session, 問題N): (status, note). status ∈ matched / partial.
VERIFY = {
    ("2024-07", "問題1"): ("matched", "数字键 第六时限=羊驼=132243"),
    ("2024-07", "問題2"): ("matched", "site Q7-12=244113=羊驼；Q8=4返上；Q13(補)=2足手まとい"),
    ("2024-07", "問題3"): ("matched", "键 323144"),
    ("2024-07", "問題4"): ("matched", "键 213314"),
    ("2024-07", "問題5"): ("matched", "site=3143413241；Q29=3 なるかどうかはともかく 已判明(jlpt247 共证)"),
    ("2024-07", "問題6"): ("matched", "键 23214"),
    ("2024-07", "問題7"): ("matched", "site=羊驼3241；Q44=1 というわけです 已判明"),
    ("2024-07", "問題8"): ("matched", "键 4323"),
    ("2024-07", "問題9"): ("partial", "Q52=3 已判明(段落明示)；Q54 jlptzhen=2 vs 羊驼=3 争议待确认"),
    ("2024-07", "問題10"): ("matched", "键 441"),
    ("2024-07", "問題11"): ("matched", "键 44"),
    ("2024-07", "問題12"): ("matched", "键 331"),
    ("2024-07", "問題13"): ("matched", "键 12"),
    # 2024-12 — jlpt247 has no answer markers; keys: aixinjp (66题) + learnjapaneseaz (Q1-44)
    ("2024-12", "問題1"): ("matched", "键 aixinjp=learnjapaneseaz=211343"),
    ("2024-12", "問題2"): ("matched", "键 1434213；aixinjp=learnjapaneseaz Q7-12 全符；Q13 learnjapaneseaz=1(じきに,疑误) 取 aixinjp=3(とっさに)"),
    ("2024-12", "問題3"): ("matched", "键 224311 (两源一致)"),
    ("2024-12", "問題4"): ("matched", "键 244321 (两源一致)"),
    ("2024-12", "問題5"): ("matched", "键 4323141132；Q34 键自引文本=选项2(あってはならない)，键标③系笔误"),
    ("2024-12", "問題6"): ("matched", "由 aixinjp 重建句逐空推导 ★ 答案：1,4,4,1,3"),
    ("2024-12", "問題7"): ("matched", "键 3412 (两源一致)"),
    ("2024-12", "問題8"): ("matched", "aixinjp 3412；选项文本逐一匹配"),
    ("2024-12", "問題9"): ("matched", "aixinjp 42242321；选项文本逐一匹配"),
    ("2024-12", "問題10"): ("matched", "aixinjp 231；选项文本匹配"),
    ("2024-12", "問題11"): ("matched", "aixinjp 43；选项文本匹配"),
    ("2024-12", "問題12"): ("matched", "aixinjp 234；选项文本匹配"),
    ("2024-12", "問題13"): ("matched", "aixinjp 11；选项文本匹配"),
}
VERIFY_SOURCES = {
    "2024-07": ["refs/2024-07_full_jlptzhen.json (jlptzhen quiz)",
                "refs/2024-07_answerkey_diliushixian.md",
                "refs/2024-07_answerkey_youtibao.md"],
    "2024-12": ["refs/2024-12_jlpt247.json (jlpt247 全文転写)",
                "refs/2024-12_answerkey_aixinjp.html (66题 答案+选项文本)",
                "refs/2024-12_answerkey_learnjapaneseaz.html (文字・語彙/文法官方 Q14-44 交叉)",
                "refs/2024-12_jlpt247_full.html (原始页面 已存档)"],
}
FLAG_TEXT = {"(2024-07, 54)": "⚠️ 答案争议：jlptzhen=2「常に客観視…」 vs 羊驼=3「正義に結びつける」 — 待用户确认"}

# Answers for sessions whose source carries no correct-answer markers
# (jlpt247 watupro quiz has no ⭕/correct flag). Every value comes from the
# archived answer keys cited in VERIFY / guides/source-log.md:
#   aixinjp  (66 written answers, digit + option text)
#   learnjapaneseaz (文字・語彙/文法 Q1-44, independent second source)
# Composition (問題6) = option number that fills the ★ blank, derived from the
# aixinjp full-sentence reconstruction (phrases numbered identically there).
# num -> (answer digit, optional note)
ANSWER_OVERRIDES = {
    "2024-12": {
        1: 2, 2: 1, 3: 1, 4: 3, 5: 4, 6: 3,                      # 問題1
        7: 1, 8: 4, 9: 3, 10: 4, 11: 2, 12: 1, 13: 3,            # 問題2 (Q13 见备注)
        14: 2, 15: 2, 16: 4, 17: 3, 18: 1, 19: 1,                # 問題3
        20: 2, 21: 4, 22: 4, 23: 3, 24: 2, 25: 1,                # 問題4
        26: 4, 27: 3, 28: 2, 29: 3, 30: 1, 31: 4, 32: 1, 33: 1, 34: 2, 35: 2,  # 問題5
        36: 1, 37: 4, 38: 4, 39: 1, 40: 3,                       # 問題6 並べ替え ★
        41: 3, 42: 4, 43: 1, 44: 2,                               # 問題7
        45: 3, 46: 4, 47: 1, 48: 2,                               # 問題8
        49: 4, 50: 2, 51: 2, 52: 4, 53: 2, 54: 3, 55: 2, 56: 1,   # 問題9
        57: 2, 58: 3, 59: 1,                                      # 問題10
        60: 4, 61: 3,                                             # 問題11
        62: 2, 63: 3, 64: 4,                                      # 問題12
        65: 1, 66: 1,                                             # 問題13
    },
}
# Per-question notes for answers resolved from conflicting keys.
ANSWER_NOTES = {
    ("2024-12", 13): "答案键分歧：aixinjp=3(とっさに 邻文义正) vs learnjapaneseaz=1(じきに, 疑误)；取 3。",
    ("2024-12", 34): "aixinjp键写了③但自引文本「あってはならない」对应本卷选项2(ことがあってはならない)；取 2。",
    ("2024-12", 54): "aixinjp=3「消費者の反応が変わっていくことを考慮して分析するべきだ」(选项文本逐一匹配)；单源。",
    ("2024-12", 60): "aixinjp=4「上司に言われたことを行うのが仕事だと思っていること」；单源。",
}

TRAILING_NUM_RE = re.compile(r"(?:^|\n)\s*(\d{1,2})\.\s*\S")


def section_offsets():
    off = {}
    run = 1
    for sect, _, _, size in GROUPS:
        off[sect] = run
        run += size
    return off


def find_num_from_stem(stem):
    # 読解 stems end with a line like "45. 筆者の考えに合うのはどれか。"
    m = list(TRAILING_NUM_RE.finditer(stem or ""))
    return int(m[-1].group(1)) if m else None


def build_verified(session, sect, extra_sources, num):
    status, note = VERIFY.get((session, sect), ("pending", ""))
    sources = list(VERIFY_SOURCES.get(
        session, [f"refs/{session}_full_jlptzhen.json (jlptzhen quiz)"]))
    if extra_sources:
        sources = list(extra_sources) + sources[1:]
    return {"status": status, "note": note, "sources": sources}


def emit(question, summary):
    path = PAST / str(question["year"]) / f"{question['month']:02d}" / question["section"]
    path.mkdir(parents=True, exist_ok=True)
    f = path / f"{question['type']}_{question['number']:02d}.json"
    if f.exists() and not FORCE:
        summary["skipped"] += 1
        summary["skip_list"].append(str(f.name))
        return
    f.write_text(json.dumps(question, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary["written"] += 1
    summary["files"].append(str(f.relative_to(ROOT)))


def main():
    global FORCE
    ap = argparse.ArgumentParser()
    ap.add_argument("session", help="e.g. 2024-07")
    ap.add_argument("--force", action="store_true",
                    help="overwrite existing per-question files")
    args = ap.parse_args()
    FORCE = args.force
    session = args.session
    year, month = (int(x) for x in session.split("-"))
    ref = REFS / f"{session}_full_jlptzhen.json"
    if not ref.exists():
        ref = REFS / f"{session}_jlpt247.json"
    if not ref.exists():
        print(f"! missing refs for {session} — run tools/fetch_jlptzhen.py / fetch_jlpt247.py first")
        sys.exit(1)
    refs_tag = ref.name
    data = json.load(open(ref, encoding="utf-8"))
    off = section_offsets()
    listen_sects = {f"問題{i}" for i in LISTEN_TYPE}
    summary = {"written": 0, "skipped": 0, "files": [], "skip_list": [], "warns": []}
    idx = {"written": 0, "listening": 0}
    cur_sect = None

    for q in data["questions"]:
        sect = q["section"]
        g = next((g for g in GROUPS if g[0] == sect), None)
        if g is None:
            summary["warns"].append(f"unknown section {sect!r} (qid {q['qid']})")
            continue
        if sect != cur_sect:
            cur_sect = sect
            idx = {"written": 0, "listening": 0}
        sname, rsec, rtype, _ = g
        is_listen = bool(q["audio"])

        if is_listen and sname in listen_sects:
            idx["listening"] += 1
            num = idx["listening"]
            ltype = LISTEN_TYPE[int(sname[-1])]
            question = {
                "id": f"{session}-listening-{ltype}-{num:02d}",
                "year": year, "month": month, "section": "listening", "type": ltype,
                "number": num, "question": q["stem"], "audio": q["audio"],
                "options": list(q["options"]), "answer": str(q["answer"]),
                "explanation": q.get("explanation", "").strip(),
                "difficulty": "medium", "tags": ["聴解"],
                "source": f"JLPT N1 {year}年{month}月 聴解 問題{sname[-1]}({num})",
                "notes": "站方解析已含完整听力脚本(见 explanation)与音频 URL；听写转写另议。",
                "verified": {"status": "structural-unverified",
                             "note": "答案标记为站点自带，尚未独立核验",
                             "sources": [f"refs/{session}_full_jlptzhen.json"]},
            }
            emit(question, summary)
            continue

        # written block
        idx["written"] += 1
        pos = idx["written"]
        num = q["num"] if q["num"] is not None else find_num_from_stem(q["stem"])
        if num is None:
            num = off[sname] + pos - 1
        else:
            expected = off[sname] + pos - 1
            if num != expected:
                summary["warns"].append(
                    f"{sname} qid{q['qid']}: site num={num}, expected {expected} (official numbering "
                    f"assumes complete groups; verify against the paper)")
        target = q.get("target") or ""
        opts = list(q["options"])

        # resolve the answer digit (jlpt247 carries no correct marker)
        answer = q["answer"]
        note = ""
        if answer in (None, ""):
            ao = ANSWER_OVERRIDES.get(session, {}).get(num)
            if ao is None:
                summary["warns"].append(f"{sname} Q{num}: 无答案来源，跳过写入")
                continue
            if isinstance(ao, tuple):
                answer, extra_note = ao
                note = (extra_note + " " if extra_note else "") + (ANSWER_NOTES.get((session, num), "") or "")
            else:
                answer = ao
                note = ANSWER_NOTES.get((session, num), "")
        answer = int(answer)

        notes = FLAG_TEXT.get(f"({session}, {num})", "")
        if note:
            notes = (notes + " " if notes else "") + note
        tags = ([target] if target else ([opts[answer - 1]] if opts else [])) \
            + TAGS_EXTRA.get(rtype, [])
        question = {
            "id": f"{session}-{rsec}-{rtype}-{num:02d}",
            "year": year, "month": month, "section": rsec, "type": rtype,
            "number": num, "question": q["stem"].strip(), "target": target,
            "options": opts, "answer": str(answer),
            "explanation": (q.get("explanation") or "").strip(),
            "difficulty": DIFFICULTY[sname], "tags": tags,
            "source": f"JLPT N1 {year}年{month}月 {SECTION_JP[rsec]} {sname}({num})",
            "notes": notes,
            "verified": build_verified(session, sname, [], num),
        }
        emit(question, summary)

    for extra in EXTRA.get((session, "問題2"), []):
        num = extra["num"]
        question = {
            "id": f"{session}-vocab-context-{num:02d}", "year": year, "month": month,
            "section": "vocab", "type": "context", "number": num,
            "question": extra["stem"], "target": extra["target"],
            "options": extra["options"], "answer": str(extra["answer"]),
            "explanation": extra["explanation"], "difficulty": "medium",
            "tags": [extra["target"], "言葉の意味", "文脈規定"],
            "source": f"JLPT N1 {year}年{month}月 言語知識(文字・語彙) 問題2({num})",
            "notes": extra["notes"],
            "verified": build_verified(session, "問題2", extra["extra_sources"], num),
        }
        emit(question, summary)

    print(f"[{session}] source={refs_tag} — wrote {summary['written']} new file(s), "
          f"{summary['skipped']} skipped (exist, kept)")
    for f in summary["files"]:
        print("  +", f)
    for f in summary["skip_list"]:
        print("  =", f)
    for w in summary["warns"]:
        print("  !", w)


if __name__ == "__main__":
    main()