# JLPT N1 Question Bank (日本語能力試験 N1 問題集)

Comprehensive question bank for JLPT N1 exam preparation, with past exam questions organized by type, year, and theme.

## Exam Structure (試験構成)

### 言語知識 (Language Knowledge) - 110分
| 問題 | 題型 | 数量 |
|------|------|------|
| 問題1 | 文脈規定 (語彙) | 6題 |
| 問題2 | 言い換え (語彙) | 7題 |
| 問題3 | 文脈規定 (文法) | 6題 |
| 問題4 | 文法選択 (文法) | 10題 |
| 問題5 | 文法排列 (文法) | 5題 |
| 問題6 | 文章文法 (文法) | 5題 |

### 読解 (Reading) - 60分
| 問題 | 題型 | 數量 |
|------|------|------|
| 問題7 | 短文読解 (4篇) | 4題 |
| 問題8 | 中文読解 (3篇) | 9題 |
| 問題9 | 長文読解 (1篇) | 3題 |
| 問題10 | 統合理解 (2篇) | 2題 |
| 問題11 | 情報検索 (1篇) | 2題 |

### 聴解 (Listening) - 60分
| 問題 | 題型 | 數量 |
|------|------|------|
| 問題1 | 課題理解 | 6題 |
| 問題2 | 要点理解 | 7題 |
| 問題3 | 概要理解 | 3題 |
| 問題4 | 即時応答 | 12題 |
| 問題5 | 統合理解 | 4題 |

## Repository Structure

```
jlpt-n1-question-bank/
├── past-exams/          # 按年份整理的真題
│   ├── 2010/           # 2010年7月・12月
│   ├── 2012/           # 2012年7月・12月
│   ├── ...
│   └── 2025/           # 2025年7月
├── question-bank/       # 按題型分類的題庫
│   ├── by-type/         # 縱向整理（按題型）
│   │   ├── vocab-context/
│   │   ├── vocab-paraphrase/
│   │   ├── vocab-usage/
│   │   ├── grammar-usage/
│   │   ├── grammar-choice/
│   │   ├── grammar-composition/
│   │   ├── reading-short/
│   │   ├── reading-mid/
│   │   ├── reading-long/
│   │   ├── listening-point/
│   │   ├── listening-grammar/
│   │   ├── listening-overview/
│   │   ├── listening-detailed/
│   │   └── listening-implication/
│   ├── by-year/          # 橫向整理（按年份）
│   └── by-theme/         # 按主題分類（語法・詞彙等）
├── analysis/             # 分析與統計
├── guides/               # 備考指南
└── tools/                # 工具腳本
```

## Usage

### 按題型練習 (Vertical Practice)
```bash
# 練習所有年份的「語彙・文脈規定」題
ls question-bank/by-type/vocab-context/
```

### 按年份練習 (Horizontal Practice)
```bash
# 練習2024年的所有題目
ls past-exams/2024/
```

### 按主題練習 (Theme-based Practice)
```bash
# 練習所有「語法」相關題目
ls question-bank/by-theme/grammar/
```

## File Format (JSON)

Each question is stored in JSON format:
```json
{
  "id": "2024-12-vocab-01",
  "year": 2024,
  "month": 12,
  "section": "vocab",
  "type": "context",
  "number": 1,
  "question": "問題文...",
  "options": ["A", "B", "C", "D"],
  "answer": "C",
  "explanation": "解説...",
  "difficulty": "medium",
  "tags": ["副詞", "曖昧表現"]
}
```

## Contributing

1. Fork this repository
2. Create a feature branch
3. Submit a pull request

## License

MIT
