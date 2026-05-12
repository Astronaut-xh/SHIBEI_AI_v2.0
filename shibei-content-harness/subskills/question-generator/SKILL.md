---
name: question-generator
description: 阅读理解出题子skill。根据改写后的文章生成4道阅读理解题，覆盖细节/推理/词义/主旨4类题型，配备偷换段落/偷换主语/绝对化/立场反转4类干扰项陷阱。由harness编排调用，也可独立使用。
subskill-of: shibei-content-harness
allowed-tools: Read,Write,Bash(python3:*),Grep,Glob
---

# 师倍AI · 阅读理解出题 Skill

## 概述与输入输出

本skill根据改写后的文章生成4道高考级别阅读理解题。

**输入**：文章JSON文件（含 `source` + `rewritten_article` 块）
**输出**：同一JSON文件追加 `questions` 块

---

## ⚠️ 关键注意事项（必读）

### 0. 4题4型，缺一不可
每篇文章必须生成恰好4道题，4种题型各1道：
- **细节理解题** (detail) — 定位原文具体信息
- **推理判断题** (inference) — 基于原文合理推断
- **词义猜测题** (word_meaning) — 根据上下文猜词义
- **主旨大意题** (main_idea) — 概括文章主旨

### 1. 干扰项陷阱设计
每个错误选项必须使用以下陷阱之一：
- **偷换段落陷阱** (paragraph_swap) — 将其他段落的信息混入本段题目
- **偷换主语陷阱** (subject_swap) — 将动作的主体/客体偷换
- **绝对化陷阱** (absolutization) — 将原文的限定性表述绝对化
- **立场反转陷阱** (stance_reversal) — 将作者态度/观点反向表述

### 2. 答案唯一性
- 每题有且仅有1个正确答案
- 干扰项必须"看着像对的，仔细读才发现不对"
- 不能出现模棱两可、两可之间的选项

### 3. 题目引用段落
- 每道题必须标注所考查的段落索引（`source_paragraph_index`）
- 主旨大意题的 `source_paragraph_index` 为 null

---

## 执行流程

### Step 1：确认输入

读取文章JSON文件，确认以下字段存在：
- `rewritten_article.body` — 改写后文章正文
- `rewritten_article.paragraphs` — 段落数组
- `source.topic_category` — 话题类别

如果JSON中已有 `questions` 块且来自审核返工：
- 保留 `review.dimension_reviews` 中的具体意见作为约束

### Step 2：读取Prompt模板和参考文档

读取以下文件：
- `prompts/generate_questions_prompt.md` — 出题Prompt模板
- `references/question_type_specs.md` — 4题型详细规格
- `references/distractor_specs.md` — 4类干扰项陷阱详细规格
- `references/gaokao_vocabulary_3500.md` — 新课标3500词汇表，题干和选项词汇应全部在3500词范围内
- `references/gaokao_exam_syllabus.md` — 高考英语考试大纲，遵循考纲命题惯例

### Step 3：执行出题

将改写后文章代入Prompt模板，生成4道题目。每题必须包含：
- `q_id` — Q1-Q4
- `q_type` — detail/inference/word_meaning/main_idea
- `stem` — 题干
- `options` — 4个选项（A-D），恰好1个正确
- `distractor_traps` — 每个错误选项的陷阱类型和说明
- `source_paragraph_index` — 考查段落
- `difficulty` — easy/medium/hard

### Step 4：校验输出

运行校验脚本：
```bash
python3 scripts/validate_questions.py <article_json_path>
```

校验项：
- 恰好4道题
- 4种题型各1道
- 每题4个选项，恰好1个正确
- 每个错误选项有明确的陷阱类型
- 选项标签为A-D

校验失败则重新生成（最多重试2次）。

### Step 5：写入JSON

将 `questions` 数组写入文章JSON文件：

```json
{
  "questions": [
    {
      "q_id": "Q1",
      "q_type": "detail",
      "stem": "According to the passage, ...",
      "options": [
        {"label": "A", "text": "...", "is_correct": false},
        {"label": "B", "text": "...", "is_correct": true},
        {"label": "C", "text": "...", "is_correct": false},
        {"label": "D", "text": "...", "is_correct": false}
      ],
      "correct_answer": "B",
      "distractor_traps": [
        {"option": "A", "trap_type": "absolutization", "explanation": "..."},
        {"option": "C", "trap_type": "stance_reversal", "explanation": "..."},
        {"option": "D", "trap_type": "subject_swap", "explanation": "..."}
      ],
      "source_paragraph_index": 1,
      "difficulty": "medium"
    }
  ]
}
```

更新 `pipeline_status.current_step` 为 `"question_generator"`。

---

## 独立使用

用户可直接调用此skill出题：
- 提供：改写后的文章文本
- 输出：4道阅读理解题的JSON数组
