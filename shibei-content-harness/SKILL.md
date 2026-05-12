---
name: shibei-content-harness
description: 师倍AI周周练内容生成编排器。一键编排7个子skill完成4篇外刊阅读理解完整内容生成与排版：找文章→改写→出题→解析→收获→审核→排版，含质量门控和自动返工循环。当用户提到"生成周周练"、"生成一期内容"、"weekly practice"、"完整出卷"、"harness"时触发此skill。
priority: 10
allowed-tools: Read,Write,Bash(python3:*),WebFetch,WebSearch,Grep,Glob
---

# 师倍AI · 内容生成编排器 (Harness)

## 概述

本skill是师倍AI周周练内容生成的编排器，负责协调8个步骤完成一期完整的4篇阅读理解内容生成与排版。

**8个步骤**：
1. `article-finder` — 找外刊文章
2. `article-rewriter` — AI改写
3. `question-generator` — AI出题
4. `explanation-generator` — AI生成解析
5. `takeaway-generator` — AI生成收获
6. `content-reviewer` — AI审核
7. 配图生成 — 为每篇文章生成SVG配图（必需）
8. `typesetter` — 组装+HTML排版

---

## ⚠️ 关键注意事项（必读）

### 0. 工作目录
所有文件操作在 `shibei_workspace/{issue_id}/` 下进行：
```
shibei_workspace/W2026W19/
├── input/
│   └── harness_config.json
├── intermediate/
│   ├── W2026W19_article_01.json
│   ├── W2026W19_article_01_original.md
│   ├── ...
└── output/
    ├── W2026W19_index.json
    ├── W2026W19_full_set.json
    ├── W2026W19_printable.md
    └── W2026W19_printable.html
```

### 1. 子skill调用机制

本harness **不通过 `Skill()` 工具调用子skill**，而是通过以下方式：

1. **读取** `subskills/<subskill-name>/SKILL.md` 获取该子skill的执行流程
2. **读取** `subskills/<subskill-name>/prompts/` 下的Prompt模板
3. **读取** `subskills/<subskill-name>/references/` 下的参考文档
4. **按子skill的执行流程操作**，使用对应工具完成任务
5. **完成后**更新 pipeline_status

**harness根目录**：`~/.claude/skills/shibei-content-harness/`

子skill路径示例：
- `subskills/article-finder/SKILL.md`
- `subskills/question-generator/references/gaokao_vocabulary_3500.md`

### 2. 并行执行策略

**核心原则：阶段间串行，阶段内并行。**

- 4篇文章在**同一阶段内**互不依赖，必须并行处理
- 使用 `Agent` 工具为每篇文章生成独立子代理，在同一消息中发起4个Agent调用
- 每个子代理负责1篇文章在当前阶段的完整处理（含子skill读取、执行、写入JSON、更新pipeline_status）
- 所有子代理完成后，harness主流程汇总结果，进入下一阶段

**并行模板**（以阶段2改写为例）：
```
# 在同一条消息中发起4个Agent调用：
Agent({ description: "改写文章1-technology", prompt: "你是文章改写子skill执行器。...按SKILL.md执行改写，结果写入article_01.json" })
Agent({ description: "改写文章2-environment", prompt: "你是文章改写子skill执行器。...按SKILL.md执行改写，结果写入article_02.json" })
Agent({ description: "改写文章3-health",      prompt: "你是文章改写子skill执行器。...按SKILL.md执行改写，结果写入article_03.json" })
Agent({ description: "改写文章4-society",     prompt: "你是文章改写子skill执行器。...按SKILL.md执行改写，结果写入article_04.json" })
```

**子代理Prompt必须包含**：
1. 子skill的SKILL.md核心执行步骤（直接写入prompt，不要让子代理再去读取）
2. 子skill的prompt模板内容
3. 子skill的参考文档关键规则
4. **JSON字段名硬约束**（从 `references/data_schema.md` 的"字段名硬约束"表中提取，明确写入prompt，严禁Agent使用别名如seq/type/source_sentence/article_meaning等）
5. 输入数据（source块、原文等，从已读文件中提取）
6. 输出目标：写入哪个JSON文件，更新哪些pipeline_status字段
7. 约束：仅操作分配的文章，不要读取或修改其他文章的文件

**适用阶段**：阶段1-6均可并行（阶段7-8是全局操作，无法拆分）

### 3. 审核返工循环
- 最多重试2次（共3次尝试）
- 返工时只重做审核未通过的步骤及其下游步骤
- 超过重试次数标记为 `needs_manual_review`

### 4. 数据格式
- 每篇文章用一个JSON文件，每步追加对应字段块
- 详见 `references/data_schema.md`

---

## 执行流程

### 阶段0：初始化

1. 确认或创建 `harness_config.json`（使用 `references/harness_config_template.json` 模板）
2. 读取配置：
   - `issue_id`（如 W2026W19）
   - `articles` 数组（4篇文章的话题分配）
   - `max_retries`（默认2）
3. 创建工作目录结构
4. 为4篇文章创建初始JSON文件

初始JSON模板：
```json
{
  "issue_id": "W2026W19",
  "article_seq": 1,
  "pipeline_status": {
    "article_finder": "pending",
    "article_rewriter": "pending",
    "question_generator": "pending",
    "explanation_generator": "pending",
    "takeaway_generator": "pending",
    "content_reviewer": "pending",
    "current_step": "initialized",
    "retry_count": 0,
    "max_retries": 2,
    "last_modified": "2026-05-09T14:00:00Z"
  }
}
```

### 阶段1：查找文章（4篇并行）

**主流程准备**：先读取 `subskills/article-finder/SKILL.md`、`references/source_guide.md`、`prompts/find_article_prompt.md`，提取核心步骤和规则。

**并行执行**：在同一条消息中发起4个Agent调用，每个Agent负责1篇文章：
- Agent 1: 查找 technology 类文章 → 写入 article_01.json + article_01_original.md
- Agent 2: 查找 environment 类文章 → 写入 article_02.json + article_02_original.md
- Agent 3: 查找 health 类文章 → 写入 article_03.json + article_03_original.md
- Agent 4: 查找 society 类文章 → 写入 article_04.json + article_04_original.md

每个Agent的Prompt中须包含：
1. 文章的 topic_category 和 preferred_sources（来自harness_config.json）
2. source_guide.md 中的搜索策略
3. 文章筛选标准（词数>500、有深度、含长难句、非纯新闻、3年内）
4. source块JSON结构模板
5. 原文保存路径和命名规则

**汇总**：4个Agent完成后，检查所有文章JSON的 `pipeline_status.article_finder` 是否为 `"completed"`

### 阶段2：改写文章（4篇并行）

**主流程准备**：先读取 `subskills/article-rewriter/SKILL.md`、`references/rewrite_rules.md`、`prompts/rewrite_prompt.md`，提取核心步骤和规则。读取4篇原文MD文件内容。

**并行执行**：在同一条消息中发起4个Agent调用，每个Agent负责1篇文章的改写。每个Agent的Prompt中须包含：
1. 改写规则（词数250-350、长难句≥2、3-5段、去口语化、不捏造信息）
2. 原文全文（从original.md读取后直接传入）
3. source块信息（original_title, publication, topic_category）
4. rewritten_article块JSON结构模板
5. 输出目标：更新对应article JSON文件 + pipeline_status

**汇总**：4个Agent完成后，逐一运行校验：
```bash
python3 subskills/article-rewriter/scripts/validate_article.py <article_json_path>
```

### 阶段3：出题（4篇并行）

**主流程准备**：先读取 `subskills/question-generator/SKILL.md`、`references/` 下的参考文档、`prompts/generate_questions_prompt.md`，提取核心步骤和规则。读取4篇文章的 source块 + rewritten_article块。

**并行执行**：在同一条消息中发起4个Agent调用，每个Agent负责1篇文章的出题。每个Agent的Prompt中须包含：
1. 出题规则（4题4型：detail/inference/word_meaning/main_idea各1题，4选项，3陷阱）
2. 改写后文章全文（从JSON中读取后直接传入）
3. source块信息
4. questions块JSON结构模板（含options、distractor_traps完整结构）
5. 输出目标：更新对应article JSON文件 + pipeline_status

**汇总**：4个Agent完成后，逐一运行校验：
```bash
python3 subskills/question-generator/scripts/validate_questions.py <article_json_path>
```

### 阶段4：生成解析（4篇并行）

**主流程准备**：先读取 `subskills/explanation-generator/SKILL.md`、`references/explanation_structure.md`、`prompts/generate_explanation_prompt.md`，提取核心步骤和规则。读取4篇文章的 source + rewritten_article + questions块。

**并行执行**：在同一条消息中发起4个Agent调用，每个Agent负责1篇文章的解析生成。每个Agent的Prompt中须包含：
1. 解析结构规则（reasoning_chain≥50字、elimination_chain≥100字、test_point_one_liner≤30字）
2. 改写后文章全文 + 题目内容（含正确答案和各选项）
3. explanations块JSON结构模板
4. 输出目标：更新对应article JSON文件 + pipeline_status

### 阶段5：生成收获（4篇并行）

**主流程准备**：先读取 `subskills/takeaway-generator/SKILL.md`、`references/takeaway_specs.md`、`prompts/generate_takeaway_prompt.md`，提取核心步骤和规则。读取4篇文章的 source + rewritten_article + questions + explanations块。

**并行执行**：在同一条消息中发起4个Agent调用，每个Agent负责1篇文章的收获生成。每个Agent的Prompt中须包含：
1. 收获结构规则（new_collocations、familiar_words_unfamiliar_meanings、common_errors三个子块）
2. 改写后文章全文 + 题目和解析内容
3. takeaways块JSON结构模板
4. 输出目标：更新对应article JSON文件 + pipeline_status

### 阶段6：审核（4篇并行）

**主流程准备**：先读取 `subskills/content-reviewer/SKILL.md`、`references/review_checklist.md`、`prompts/review_prompt.md`，提取核心步骤和规则。读取4篇文章的完整数据（source + rewritten_article + questions + explanations + takeaways）。

**并行执行**：在同一条消息中发起4个Agent调用，每个Agent负责1篇文章的审核。每个Agent的Prompt中须包含：
1. 审核维度和评分标准（fluency/unique_correct_answer/explanation_persuasiveness/distractor_reasonableness/takeaway_usefulness，各1-10分）
2. 文章完整数据（改写文、题目、解析、收获）
3. review块JSON结构模板（含scores、dimension_reviews、overall_pass、rewrite_targets）
4. 输出目标：更新对应article JSON文件 + pipeline_status

**汇总**：4个Agent完成后，逐一运行评分汇总：
```bash
python3 subskills/content-reviewer/scripts/compute_review_score.py <article_json_path>
```

检查每篇文章的 `review.overall_pass`：
- **通过** → 该文章完成
- **未通过** → 进入审核返工循环（返工也按文章独立并行处理）

### 审核返工循环

对每篇未通过审核的文章：

1. 读取 `review.rewrite_targets`，确定需返工的块
2. 确定最上游的返工步骤（根据依赖表）
3. 递增 `pipeline_status.retry_count`
4. 如果 `retry_count > max_retries`，标记 `current_step = "needs_manual_review"`，跳过该文章
5. 否则，将审核意见作为上下文，按对应子skill的执行流程重新操作
6. 重新调用审核子skill
7. 重复直到通过或达到最大重试次数

**返工依赖表**：

| 返工块 | 需级联返工的下游块 |
|--------|------------------|
| rewritten_article | questions → explanations → takeaways → review |
| questions | explanations → takeaways → review |
| explanations | takeaways → review |
| takeaways | review |

### 阶段7：生成配图（4篇并行，必需）

**配图是必需步骤，不可跳过。** 每篇文章必须有一张与内容相关的SVG配图。

**主流程准备**：读取4篇文章的 source.topic_category 和 rewritten_article，提取每篇文章的主题和标识色。

**并行执行**：在同一条消息中发起4个Agent调用，每个Agent负责1篇文章的SVG配图生成。每个Agent的Prompt中须包含：
1. 文章主题和核心内容（从source和rewritten_article提取）
2. 文章标识色（A=蓝#1E6BB8, B=绿#27AE60, C=紫#8E44AD, D=红#C0392B）
3. SVG尺寸要求：800×200（4:1横幅）
4. 视觉风格：扁平化、简约、适合打印
5. 输出路径：`images/article_{seq:02d}.svg`

**配图规范**：
- SVG尺寸固定 800×200
- 以文章标识色为主色，搭配该色的浅色变体和白色
- 视觉元素须与文章主题直接相关（如technology类用电路/芯片/代码，environment类用森林/河流/新能源，health类用药瓶/医学符号/天平，society类用城市/人物/盾牌）
- 左侧包含半透明英文装饰字（如"AI × Education"）
- 底部有淡色渐变
- 无文字水印、无版权信息

**汇总**：4个Agent完成后，将SVG以base64编码写入各文章JSON的 `source.image_url` 字段（格式：`data:image/svg+xml;base64,...`）：
```python
import base64
with open(svg_path, 'r') as f:
    b64 = base64.b64encode(f.read().encode()).decode()
data['source']['image_url'] = f'data:image/svg+xml;base64,{b64}'
```

### 阶段8：组装输出

所有文章处理完成后，运行组装脚本：
```bash
python3 scripts/assemble_weekly_set.py <workspace_dir> <issue_id>
```

生成3个输出文件：
1. `{issue_id}_index.json` — 周练索引
2. `{issue_id}_full_set.json` — 4篇文章完整数据
3. `{issue_id}_printable.md` — 可打印的Markdown

### 阶段9：排版输出

按以下步骤调用子skill `typesetter`：

1. 读取 `subskills/typesetter/SKILL.md` 获取执行流程
2. 读取 `subskills/typesetter/references/css_layout_spec.md` 和 `subskills/typesetter/references/color_size_spec.md`
3. 读取 `subskills/typesetter/prompts/typeset_prompt.md`
4. 运行渲染脚本：
```bash
python3 subskills/typesetter/scripts/render_html.py <workspace_dir> <issue_id>
```
5. 生成 `{issue_id}_printable.html` — 可打印的报纸风格HTML

### 最终报告

向用户报告：
- 期号和日期
- 4篇文章的话题和来源分布
- 每篇文章的审核结果
- 是否有文章需要人工审核
- 配图状态（必须4/4，否则报错）
- 输出文件路径（含HTML排版文件）

---

## 断点续跑

如果harness中途中断，可以从断点继续：

1. 读取每篇文章的 `pipeline_status.current_step`
2. 找到所有未完成的步骤
3. 从最早的未完成步骤继续执行
4. 已完成的步骤跳过

---

## 目录结构

```
~/.claude/skills/shibei-content-harness/
├── SKILL.md                              # 本文件
├── references/
│   ├── data_schema.md                    # JSON Schema文档
│   └── harness_config_template.json      # 配置模板
├── scripts/
│   └── assemble_weekly_set.py            # 组装输出脚本
└── subskills/
    ├── article-finder/
    │   ├── SKILL.md
    │   ├── prompts/
    │   ├── references/
    │   └── scripts/
    ├── article-rewriter/
    │   ├── SKILL.md
    │   ├── prompts/
    │   ├── references/
    │   └── scripts/
    ├── question-generator/
    │   ├── SKILL.md
    │   ├── prompts/
    │   ├── references/
    │   └── scripts/
    ├── explanation-generator/
    │   ├── SKILL.md
    │   ├── prompts/
    │   └── references/
    ├── takeaway-generator/
    │   ├── SKILL.md
    │   ├── prompts/
    │   └── references/
    ├── content-reviewer/
    │   ├── SKILL.md
    │   ├── prompts/
    │   ├── references/
    │   └── scripts/
    └── typesetter/
        ├── SKILL.md
        ├── prompts/
        ├── references/
        └── scripts/
```
