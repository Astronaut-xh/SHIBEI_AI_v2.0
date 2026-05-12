# 4类干扰项陷阱详细规格

## 设计原则

**好的干扰项 = 看着像对的，仔细读才发现不对**

干扰项不是"随便写一个错误答案"，而是有意识设计的认知陷阱。每个干扰项必须：
1. 与原文有某种关联（不是完全无关的胡说）
2. 在快速阅读时容易被误选
3. 仔细对照原文后能发现其错误

---

## 1. 偷换段落陷阱 (paragraph_swap)

### 定义
将文章其他段落的信息混入当前段落的题目中，形成"信息张冠李戴"的干扰项。

### 设计方法
1. 确定题目考查的段落P
2. 在其他段落P'中找到一个与P相关但不同的信息
3. 将P'的信息包装为P的信息，形成干扰项

### 示例
- 文章第1段讲AI在制造业的影响，第3段讲AI在医疗领域的影响
- 题目考查第1段（制造业）
- 干扰项："AI has significantly improved diagnostic accuracy in medical imaging."（这是第3段的内容，不是第1段）

### 识别特征
- 干扰项的内容在原文中确实存在，只是不在题目考查的段落
- 学生如果只扫读全文而不精读目标段落，容易误选

---

## 2. 偷换主语陷阱 (subject_swap)

### 定义
将动作的主体或客体偷换，形成"张冠李戴"的干扰项。

### 设计方法
1. 找到原文中的关键句：A做了X
2. 将主语从A替换为B（B在文章中也出现了）：B做了X
3. 或者将宾语从X替换为Y：A做了Y

### 示例
- 原文："Workers in routine tasks are being displaced by automation."
- 干扰项："Automation is being displaced by workers in routine tasks."（主宾反转）
- 或干扰项："Workers in creative fields are being displaced by automation."（偷换定语）

### 识别特征
- 干扰项与原文高度相似，但主语/宾语/定语被偷换
- 学生如果快速阅读不仔细，容易忽略主语的差异

---

## 3. 绝对化陷阱 (absolutization)

### 定义
将原文中有限定条件的表述绝对化，删除或替换限定词。

### 设计方法
1. 找到原文中有限定词的表述："some/most/certain/likely/often..."
2. 替换为绝对化表述："all/every/never/always/must/certainly..."

### 常见替换对
| 原文限定词 | 绝对化替换 |
|-----------|-----------|
| some | all / every |
| most | all |
| likely | certain / must |
| often | always |
| may / might | will / must |
| tend to | always |
| in some cases | in all cases |
| one of the main | the only |

### 示例
- 原文："Some jobs may be displaced by AI."
- 干扰项："All jobs will be displaced by AI."

### 识别特征
- 干扰项比正确选项更"绝对""肯定"
- 学生倾向于选择看起来更确定的答案，这是认知偏误

---

## 4. 立场反转陷阱 (stance_reversal)

### 定义
将作者的态度、观点或文章的结论反向表述。

### 设计方法
1. 识别作者的核心立场：正面/负面/中立
2. 将立场反转：正面→负面，或否定→肯定
3. 或将原文的条件关系反转：因果倒置、目的手段倒置

### 示例
- 原文："The author argues that AI will create more jobs than it eliminates."
- 干扰项："The author believes that AI will eliminate more jobs than it creates."

### 常见反转模式
| 原文立场 | 反转干扰项 |
|---------|-----------|
| 支持/肯定 | 反对/否定 |
| 乐观 | 悲观 |
| 因→果 | 果→因 |
| 目的→手段 | 手段→目的 |
| 问题→方案 | 方案→问题 |

### 识别特征
- 干扰项与原文立场截然相反
- 学生如果只关注关键词而忽略逻辑关系，容易误选

---

## 4题陷阱分配建议

每篇文章的4道题，3个错误选项共12个干扰项，建议分布：
- paragraph_swap: 3个
- subject_swap: 3个
- absolutization: 3个
- stance_reversal: 3个

每题的3个干扰项尽量使用不同陷阱类型，避免同一题出现2个同类型陷阱。
