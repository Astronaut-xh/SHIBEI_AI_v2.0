---
name: explanation-generator
description: 解析生成子skill。为阅读理解题生成三层结构解析：推理链+排除链+考点一句话。由harness编排调用，也可独立使用。
subskill-of: shibei-content-harness
allowed-tools: Read,Write,Bash(python3:*),Grep,Glob
---

# 师倍AI · 解析生成 Skill

## 概述与输入输出

本skill为每道阅读理解题生成三层结构解析。

**输入**：文章JSON文件（含 `source` + `rewritten_article` + `questions` 块）
**输出**：同一JSON文件追加 `explanations` 块

---

## ⚠️ 关键注意事项（必读）

### 0. 三层结构，缺一不可
每道题的解析必须包含三层：
1. **推理链** (reasoning_chain) — 为什么正确答案是对的
2. **排除链** (elimination_chain) — 为什么其他三个选项是错的
3. **考点一句话** (test_point_one_liner) — 这道题考什么

### 1. 推理链要求
- 必须引用原文具体位置（段落号、句子号）
- 必须展示从原文信息到正确答案的推理过程
- 不能只说"根据原文可知"，必须说"根据第X段第Y句...，因此..."
- 长度 ≥ 50字

### 2. 排除链要求
- 必须逐一分析3个错误选项
- 每个选项必须指出其陷阱类型和具体错误
- 不能只说"A错误"，必须说"A选项使用了绝对化陷阱，原文说'some'而选项说'all'"
- 长度 ≥ 100字

### 3. 考点一句话格式
- 格式：`题型：核心考点概括`
- 示例：`细节理解题：精准定位原文关键句，识别绝对化陷阱`
- 一句话，不超过30字

---

## 执行流程

### Step 1：确认输入

读取文章JSON文件，确认以下字段存在：
- `rewritten_article.body` — 文章正文
- `rewritten_article.paragraphs` — 段落数组
- `questions` — 题目数组（4道题）

### Step 2：读取Prompt模板和参考文档

读取以下文件：
- `prompts/generate_explanation_prompt.md` — 解析Prompt模板
- `references/explanation_structure.md` — 三层结构详细规格与示例

需要时读取以下参考文件（从出题skill目录获取）：
- `subskills/question-generator/references/gaokao_exam_syllabus.md` — 参考考纲命题惯例，确保解析符合考试规范

### Step 3：执行解析生成

对每道题，将文章和题目信息代入Prompt模板，生成三层解析。

### Step 4：写入JSON

将 `explanations` 数组写入文章JSON文件：

```json
{
  "explanations": [
    {
      "q_id": "Q1",
      "reasoning_chain": "题目问AI应用的主要担忧。根据第2段第3句'AI may displace workers in routine tasks while creating new categories of employment'，可知B选项是对原文的准确概括。",
      "elimination_chain": "A选项使用'all existing jobs'属于绝对化陷阱，原文只说'some jobs'；C选项'no significant impact'与原文立场相反，属于立场反转陷阱；D选项将范围从全球偷换为'developing countries'，属于偷换主语陷阱。",
      "test_point_one_liner": "细节理解题：精准定位原文关键句，识别绝对化和偷换主语陷阱",
      "explanation_version": 1
    }
  ]
}
```

更新 `pipeline_status.current_step` 为 `"explanation_generator"`。
