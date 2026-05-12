---
name: takeaway-generator
description: "我的收获"生成子skill。从文章中提取新搭配(≤5)、熟词生义(≤3)和易错点，生成结构化学习收获内容。由harness编排调用，也可独立使用。
subskill-of: shibei-content-harness
allowed-tools: Read,Write,Bash(python3:*),Grep,Glob
---

# 师倍AI · 我的收获生成 Skill

## 概述与输入输出

本skill从文章中提取学生可学习的语言知识点，生成"我的收获"板块。

**输入**：文章JSON文件（含 `source` + `rewritten_article` + `questions` + `explanations` 块）
**输出**：同一JSON文件追加 `takeaways` 块

---

## ⚠️ 关键注意事项（必读）

### 0. 三个板块，数量硬约束
- **新搭配** (new_collocations)：1-5个
- **熟词生义** (familiar_words_unfamiliar_meanings)：0-3个
- **易错点** (common_errors)：0+个（无上限）

### 1. 新搭配选择标准
- 必须是高中阶段有价值的英语搭配（collocation）
- 不是单词本身，而是词与词的习惯组合
- 优先选择：动词+名词、形容词+名词、动词+介词+名词
- 必须来自文章，不能凭空编造

### 2. 熟词生义选择标准
- 学生"认识"这个词的常见义，但在本文中用了不同含义
- 必须是高考高频词的非常见用法
- 优先选择：动词的抽象用法、名词的引申义

### 3. 易错点设计
- 基于题目中的干扰项陷阱设计
- 帮助学生识别常见的出题套路
- 与具体题目关联（related_q_id）

---

## 执行流程

### Step 1：确认输入

读取文章JSON文件，确认以下字段存在：
- `rewritten_article.body` — 文章正文
- `questions` — 题目数组
- `explanations` — 解析数组

### Step 2：读取Prompt模板和参考文档

读取以下文件：
- `prompts/generate_takeaway_prompt.md`
- `references/takeaway_specs.md`

需要时读取以下参考文件（从出题skill目录获取）：
- `subskills/question-generator/references/gaokao_vocabulary_3500.md` — 用于确认提取的搭配和熟词生义是否在3500词范围内

### Step 3：执行收获生成

从文章和题目中提取学习要点，生成三个板块内容。

### Step 4：写入JSON

将 `takeaways` 块写入文章JSON文件：

```json
{
  "takeaways": {
    "new_collocations": [
      {
        "collocation": "displace workers",
        "meaning_zh": "取代工人",
        "example_sentence": "Automation may displace workers in manufacturing.",
        "source_paragraph_index": 1
      }
    ],
    "familiar_words_unfamiliar_meanings": [
      {
        "word": "displace",
        "familiar_meaning": "移动，移位",
        "new_meaning_in_context": "取代，使失业",
        "example_sentence": "AI may displace workers in routine tasks.",
        "source_paragraph_index": 1
      }
    ],
    "common_errors": [
      {
        "error_description": "将displace理解为'移动位置'而非'取代（工作岗位）'",
        "related_q_id": "Q3",
        "tip": "在就业语境中，displace常指'取代'，而非物理位移"
      }
    ],
    "takeaway_version": 1
  }
}
```

更新 `pipeline_status.current_step` 为 `"takeaway_generator"`。
