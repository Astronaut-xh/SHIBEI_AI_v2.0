---
name: typesetter
description: 排版子skill。将4篇文章的JSON数据按固定报纸风格模板渲染为可打印HTML，含A4分页、三栏流淌、答案解析页。由harness编排调用，也可独立使用。
subskill-of: shibei-content-harness
allowed-tools: Read,Write,Bash(python3:*),Grep,Glob
---

# 师倍AI · 排版 Skill

## 概述与输入输出

本skill将周练JSON数据按固定报纸风格CSS模板渲染为可打印HTML文件。

**输入**：`output/{issue_id}_full_set.json`（harness阶段7的产出）
**输出**：`output/{issue_id}_printable.html`（可直接浏览器打印为PDF）

---

## ⚠️ 关键注意事项（必读）

### 0. 固定模板
- CSS布局、颜色、尺寸均为固定规范，不可随意修改
- 模板定义在 `references/css_layout_spec.md`，颜色尺寸速查在 `references/color_size_spec.md`
- 任何视觉调整应修改参考文档和脚本，而非运行时硬编码

### 1. A4分页
- 每页严格A4尺寸（210mm × 297mm）
- 第1页：Passage A（上半）+ Passage B（下半）
- 第2页：Passage C（上半）+ Passage D（下半）
- 第3页：答案解析（整页不分栏）

### 2. 三栏流淌
- 文章正文和题目使用 CSS `columns: 3` 实现三栏从左至右流淌
- 栏间距10px，无竖线分隔，留白干净
- 文章正文在前，题目紧跟其后，同一流淌区域内
- 正文段落两端对齐（`text-align: justify`）
- 答案解析页不分栏，全宽排列

### 3. 文章标识颜色
- A = 蓝色 `#1E6BB8`
- B = 绿色 `#27AE60`
- C = 紫色 `#8E44AD`
- D = 红色 `#C0392B`

### 4. 首字母下沉
- 每篇文章第一段首字母下沉（drop cap），字号2.8em，Georgia衬线体加粗
- 首字母颜色与文章标识色一致（A蓝/B绿/C紫/D红）
- 第一段取消首行缩进，后续段落保留1.5em缩进

### 5. 配图
- **配图为必需项，不可省略** — 每篇文章必须有 `source.image_url` 字段
- image_url 格式：`data:image/svg+xml;base64,...`（base64编码的SVG）
- 配图在阶段7（生成配图）中生成并写入JSON
- 渲染时始终渲染配图，无image_url则报错而非跳过

---

## 执行流程

### Step 1：确认输入

读取 `output/{issue_id}_full_set.json`，确认：
- `articles` 数组包含4篇文章
- 每篇文章包含 `rewritten_article`、`questions`、`explanations`、`takeaways` 块
- 如果文件不存在，回退读取 `intermediate/` 下4个单篇JSON并组装

如果JSON中缺少必要字段，报告错误并终止。

### Step 2：读取参考文档

读取以下文件，获取排版规范：
- `references/css_layout_spec.md` — 完整CSS布局规范（含HTML结构示例）
- `references/color_size_spec.md` — 颜色尺寸速查表

这些规范已在 `scripts/render_html.py` 中内嵌，读取用于确认规范一致或按需调整。

### Step 3：读取排版指令

读取 `prompts/typeset_prompt.md`，获取排版指令和页面布局要求。

### Step 4：运行渲染脚本

```bash
python3 scripts/render_html.py <workspace_dir> <issue_id>
```

脚本完成以下工作：
1. 读取 `output/{issue_id}_full_set.json`
2. 按固定CSS模板渲染3页HTML
3. 输出到 `output/{issue_id}_printable.html`

### Step 5：验证输出

检查生成的HTML文件：
- 文件非空且为合法HTML
- 包含3个 `.page` 容器
- 每篇文章有正确的标识颜色class
- 答案解析页包含4篇文章的答案和解析

### Step 6：报告结果

向用户报告：
- 生成HTML文件路径
- 3页结构概览
- 是否有文章缺少配图
- 浏览器打印为PDF的提示

---

## 独立使用

用户可直接调用此skill排版已有的周练数据：
- 提供：workspace目录路径和issue_id
- 输出：可打印HTML文件

不需要运行完整harness流水线，只要有 `full_set.json` 即可。

---

## 与harness集成

本子skill由harness在阶段8调用。harness会：
1. 读取本文件获取执行流程
2. 读取 `subskills/typesetter/references/` 和 `subskills/typesetter/prompts/`
3. 运行 `python3 subskills/typesetter/scripts/render_html.py <workspace_dir> <issue_id>`
4. 验证并报告输出

当前harness阶段7的 `printable.md` 仍保留作为纯文本备选，HTML排版为新增阶段。
