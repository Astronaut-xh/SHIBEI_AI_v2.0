---
name: article-rewriter
description: 文章改写子skill。将外刊原文AI改写为250-350词、保留长难句、去口语化的高中阅读理解文章。由harness编排调用，也可独立使用。
subskill-of: shibei-content-harness
allowed-tools: Read,Write,Bash(python3:*),Grep,Glob
---

# 师倍AI · 文章改写 Skill

## 概述与输入输出

本skill将外刊原文改写为适合高中英语阅读理解的文章。

**输入**：文章JSON文件（含 `source` 块）+ 原文Markdown文件
**输出**：同一JSON文件追加 `rewritten_article` 块

---

## ⚠️ 关键注意事项（必读）

### 0. 词数硬约束
- 改写后文章 **必须** 在 250-350 词之间
- 不在范围内的输出视为无效，必须重新改写

### 1. 保留长难句
- 至少保留 2 个长度超过 25 词的复杂句
- 长难句是高考D篇的核心特征，不可简化为短句

### 2. 去口语化
- 删除所有口语表达、俚语、非正式用语
- 使用书面学术风格，但不刻意堆砌生僻词

### 3. 段落结构
- 改写后文章分为 3-5 个自然段
- 每段有明确主题句
- 段落间有逻辑衔接

### 4. 不改变核心信息
- 原文的事实、数据、观点必须保留
- 可以精简细节，但不能捏造或歪曲

---

## 执行流程

### Step 1：确认输入

读取文章JSON文件，确认以下字段存在：
- `source.url` — 原文链接
- `source.original_title` — 原文标题
- `source.topic_category` — 话题类别

读取原文Markdown文件，确认内容非空。

如果JSON中已有 `rewritten_article` 块且 `rewrite_version` 存在：
- 询问用户是否要重新改写（可能来自审核返工）
- 如果是审核返工，将 `review.dimension_reviews.fluency.issues` 作为额外约束

### Step 2：读取Prompt模板

读取 `prompts/rewrite_prompt.md`，获取改写Prompt模板。

### Step 3：读取参考文档

读取以下文件：
- `references/rewrite_rules.md` — 详细改写规则和示例
- `references/gaokao_vocabulary_3500.md` — 新课标3500词汇表，超纲词控制在≤5个，不可替换的核心概念要保留上下文线索（如文件不存在则跳过）
- `references/gaokao_exam_syllabus.md` — 高考英语考试大纲，了解文章规格和体裁要求（如文件不存在则跳过）

需要时读取以下参考文件（从article-finder子skill目录获取）：
- `subskills/article-finder/references/source_guide.md` — 了解文章来源类型，根据不同来源（新闻时事/科普学术/生活文化）调整改写风格

### Step 4：执行改写

将原文内容代入Prompt模板，执行改写生成。输出必须包含：
- `title_en` — 英文标题（可与原标题不同，但须反映文章内容）
- `title_zh` — 中文标题翻译
- `body` — 改写后文章正文（250-350词）
- `paragraphs` — 段落数组，每段含 index、text、word_count

### Step 5：校验输出

运行校验脚本验证改写结果：
```bash
python3 scripts/validate_article.py <article_json_path>
```

校验项：
- 词数在 250-350 范围内
- 长难句（>25词）数量 ≥ 2
- 段落数在 3-5 之间
- 每段词数 > 0

如果校验失败，根据失败原因调整Prompt重新生成（最多重试2次）。

### Step 6：写入JSON

将 `rewritten_article` 块写入文章JSON文件。字段结构：

```json
{
  "rewritten_article": {
    "title_en": "AI and the Future of Work",
    "title_zh": "AI与工作的未来",
    "body": "The rapid advancement of artificial intelligence has...",
    "word_count": 312,
    "long_sentences_count": 4,
    "paragraphs": [
      {"index": 0, "text": "The rapid advancement...", "word_count": 82},
      {"index": 1, "text": "While some economists argue...", "word_count": 95}
    ],
    "rewrite_version": 1,
    "rewriter_notes": "保留了2个长难句，去除了3处口语表达"
  }
}
```

同时更新 `pipeline_status.current_step` 为 `"article_rewriter"`。

### Step 7：报告结果

向用户报告：
- 改写后词数
- 保留的长难句数量
- 去除的口语表达数量（如有）
- 段落分布

---

## 独立使用

用户可直接调用此skill改写一篇文章：
- 提供：文章URL或文本内容
- 输出：`rewritten_article` JSON块 + 改写后文章全文

不需要完整的文章JSON文件，skill可临时创建。
