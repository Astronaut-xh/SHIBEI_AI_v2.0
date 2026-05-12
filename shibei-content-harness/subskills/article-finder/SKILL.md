---
name: article-finder
description: 外刊文章查找子skill。根据话题类别和来源偏好，从NYT/Guardian/Economist/SciAm等外刊中查找适合高中英语阅读理解题源的文章。由harness编排调用，也可独立使用。
subskill-of: shibei-content-harness
allowed-tools: Read,Write,Bash(python3:*),WebFetch,WebSearch,Grep,Glob
---

# 师倍AI · 外刊文章查找 Skill

## 概述与输入输出

本skill从外刊来源中查找适合高中英语阅读理解的文章。

**输入**：话题类别偏好（可选），来源偏好（可选）
**输出**：文章JSON文件写入 `source` 块 + 原文Markdown文件

---

## ⚠️ 关键注意事项（必读）

### 0. 四大外刊来源
- **The New York Times (NYT)** — 时事、社会、健康
- **The Guardian** — 环境、社会、科技
- **The Economist** — 经济、科技、社会
- **Scientific American (SciAm)** — 科技、健康、环境

### 1. 四大话题类别
- **technology** — 科技
- **environment** — 环境
- **society** — 社会
- **health** — 健康

### 2. 文章筛选标准
- 原文词数 > 500词（太短的文章信息量不够）
- 内容有深度，有观点/发现/论证
- 包含长难句（适合高考D篇出题）
- 非纯新闻（避免纯事实报道，需要分析/观点）
- 近三年内发布

---

## 执行流程

### Step 1：确认需求

确定以下信息（用户提供或使用默认值）：
- `topic_category` — 话题偏好（默认4类各1篇）
- `preferred_sources` — 来源偏好（可选）
- `issue_id` — 期号（harness提供）
- `article_seq` — 文章序号（harness提供）

### Step 2：读取参考文档

读取以下文件：
- `references/source_guide.md` — 外刊来源选择指南、搜索策略与话题匹配

### Step 3：搜索和筛选文章

使用WebSearch搜索外刊文章，然后使用WebFetch获取文章内容。

搜索策略：
1. 按话题类别构造搜索查询
2. 限定来源域名（nytimes.com, theguardian.com, economist.com, scientificamerican.com）
3. 筛选近期文章
4. 评估文章是否符合筛选标准

### Step 4：提取文章内容

使用WebFetch获取文章全文，转为Markdown格式保存为原文文件。

### Step 5：写入JSON

将 `source` 块写入文章JSON文件：

```json
{
  "source": {
    "url": "https://www.economist.com/...",
    "publication": "The Economist",
    "topic_category": "technology",
    "original_title": "AI and the Future of Work",
    "original_word_count": 2800,
    "found_date": "2026-05-09",
    "finder_notes": "信息密度高，长难句丰富，适合出题"
  }
}
```

同时保存原文为 `{issue_id}_article_{seq}_original.md`。

更新 `pipeline_status.current_step` 为 `"article_finder"`。

---

## 独立使用

用户可直接调用此skill查找文章：
- 提供：话题偏好（如"科技类"）
- 输出：符合条件的文章URL和基本信息
