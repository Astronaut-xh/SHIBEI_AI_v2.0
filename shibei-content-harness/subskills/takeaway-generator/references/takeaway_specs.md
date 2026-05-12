# 收获板块详细规格

## 1. 新搭配 (new_collocations)

### 什么是搭配
搭配（collocation）是英语中词与词的习惯组合，不是任意组合。学生学习搭配有助于提升地道表达能力。

### 选择标准
1. **必须是文章中实际出现的搭配**，不能编造
2. **必须是高中阶段有价值学习的**，排除过于简单的（如make a decision）和过于专业的（如quantum entanglement）
3. **优先选择以下类型**：
   - 动词+名词：displace workers, generate demand, pose a challenge
   - 形容词+名词：significant impact, considerable concern, routine tasks
   - 动词+介词+名词：adapt to changes, contribute to growth
   - 介词+名词组合：in response to, with respect to

### 数量：1-5个

### 字段说明
| 字段 | 说明 |
|------|------|
| collocation | 搭配本身（英文） |
| meaning_zh | 中文释义 |
| example_sentence | 使用该搭配的例句（可用文章原句或新造句） |
| source_paragraph_index | 搭配出现在文章的哪一段 |

---

## 2. 熟词生义 (familiar_words_unfamiliar_meanings)

### 什么是熟词生义
学生在课本中学过这个词的常见含义，但在本文中它被用在不同的含义上。

### 选择标准
1. **常见义确实是高中学生熟知的**
2. **文中含义与常见义有明显差异**
3. **文中含义是高考可能考查的**
4. 优先选择：动词的抽象用法 > 名词的引申义 > 形容词的特殊用法

### 数量：0-3个

### 常见熟词生义示例
| 单词 | 常见义 | 文中可能义 |
|------|--------|-----------|
| displace | 移动，移位 | 取代，使失业 |
| address | 地址 | 处理，应对 |
| discipline | 纪律 | 学科 |
| exploit | 剥削 | 利用，开发 |
| observe | 观察 | 遵守（规则） |
| accommodate | 容纳 | 适应，迎合 |
| coordinate | 坐标 | 协调 |

### 字段说明
| 字段 | 说明 |
|------|------|
| word | 单词 |
| familiar_meaning | 学生熟悉的意思 |
| new_meaning_in_context | 在本文中的意思 |
| example_sentence | 使用新义的例句 |
| source_paragraph_index | 该词出现在文章的哪一段 |

---

## 3. 易错点 (common_errors)

### 什么是易错点
基于题目中的干扰项陷阱，总结学生容易犯的思维错误。

### 设计方法
1. 从 `questions` 的 `distractor_traps` 中提取陷阱模式
2. 将具体陷阱抽象为通用思维错误
3. 给出避免该错误的tips

### 数量：0+个（无上限，但通常2-4个）

### 字段说明
| 字段 | 说明 |
|------|------|
| error_description | 错误描述：学生容易怎么错 |
| related_q_id | 关联的题目ID |
| tip | 避免该错误的建议 |

### 易错点分类
| 陷阱类型 | 对应易错点 | tip示例 |
|---------|-----------|---------|
| absolutization | 将限定性表述误读为绝对表述 | 注意some/most/all/must等限定词 |
| subject_swap | 混淆动作的主体和客体 | 精读时标记"谁做了什么" |
| paragraph_swap | 将不同段落的信息混淆 | 先定位段落再选择答案 |
| stance_reversal | 将作者态度理解反了 | 注意态度词的褒贬色彩 |
