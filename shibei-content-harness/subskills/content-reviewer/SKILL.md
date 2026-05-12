---
name: content-reviewer
description: 内容审核子skill。模拟高中英语教师视角，从通顺度/答案唯一性/解析说服力/干扰项合理性/收获有用性5个维度审核生成内容质量。由harness编排调用，也可独立使用。
subskill-of: shibei-content-harness
allowed-tools: Read,Write,Bash(python3:*),Grep,Glob
---

# 师倍AI · 内容审核 Skill

## 概述与输入输出

本skill模拟高中英语教师视角，对生成的完整内容进行5维度质量审核。

**输入**：文章JSON文件（含全部块：source → rewritten_article → questions → explanations → takeaways）
**输出**：同一JSON文件追加 `review` 块

---

## ⚠️ 关键注意事项（必读）

### 0. 5个审核维度

| 维度 | 英文键名 | 通过阈值 | 考查内容 |
|------|---------|---------|---------|
| 通顺度 | fluency | ≥7 | 文章通顺、语法正确、长难句连贯 |
| 答案唯一性 | unique_correct_answer | ≥9 | 每题有且仅有1个无争议的正确答案 |
| 解析说服力 | explanation_persuasiveness | ≥7 | 推理链引用原文、排除链逐一分析 |
| 干扰项合理性 | distractor_reasonableness | ≥7 | 干扰项看似合理、陷阱类型清晰 |
| 收获有用性 | takeaway_usefulness | ≥7 | 搭配有价值、熟词生义准确、易错点有操作性 |

### 1. 评分范围
- 每个维度 1-10 分
- 10分=完美，8-9分=优秀，6-7分=合格，5分以下=不合格

### 2. 通过条件
- `overall_pass = true` 当且仅当所有5个维度都通过阈值
- 任何1个维度未通过，`overall_pass = false`

### 3. 返工目标
- 审核失败时，必须明确指出哪些块需要返工（`rewrite_targets`）
- 返工目标只能是：`rewritten_article`、`questions`、`explanations`、`takeaways`

---

## 执行流程

### Step 1：确认输入

读取文章JSON文件，确认以下字段都存在：
- `rewritten_article` — 改写后文章
- `questions` — 题目数组
- `explanations` — 解析数组
- `takeaways` — 收获块

### Step 2：读取Prompt模板和参考文档

读取以下文件：
- `prompts/review_prompt.md`
- `references/review_checklist.md`

需要时读取以下参考文件（可从出题skill目录获取）：
- `subskills/question-generator/references/gaokao_vocabulary_3500.md` — 用于审核文章词汇是否符合3500词范围
- `subskills/question-generator/references/gaokao_exam_syllabus.md` — 用于审核题目是否符合考纲命题惯例

### Step 3：执行审核

对5个维度逐一评分和评审。

### Step 4：运行评分汇总脚本

```bash
python3 scripts/compute_review_score.py <article_json_path>
```

### Step 5：写入JSON

将 `review` 块写入文章JSON文件：

```json
{
  "review": {
    "review_version": 1,
    "overall_pass": false,
    "scores": {
      "fluency": 8,
      "unique_correct_answer": 9,
      "explanation_persuasiveness": 6,
      "distractor_reasonableness": 8,
      "takeaway_usefulness": 7
    },
    "dimension_reviews": {
      "fluency": {
        "pass": true,
        "comment": "文章通顺，长难句结构清晰",
        "issues": []
      },
      "unique_correct_answer": {
        "pass": true,
        "comment": "4题答案均唯一确定",
        "issues": []
      },
      "explanation_persuasiveness": {
        "pass": false,
        "comment": "Q2推理链未引用原文具体位置",
        "issues": ["Q2推理链缺少段落引用", "Q4排除链未分析选项D的陷阱"]
      },
      "distractor_reasonableness": {
        "pass": true,
        "comment": "干扰项设计合理",
        "issues": []
      },
      "takeaway_usefulness": {
        "pass": true,
        "comment": "搭配和熟词生义选择恰当",
        "issues": []
      }
    },
    "rewrite_needed": true,
    "rewrite_targets": ["explanations"],
    "review_timestamp": "2026-05-09T14:30:00Z"
  }
}
```

更新 `pipeline_status.current_step` 为 `"content_reviewer"`。
