# 解析三层结构详细规格与示例

## 三层结构总览

```
推理链 → 排除链 → 考点一句话
为什么对 → 为什么错 → 考什么
```

三层缺一不可。学生看完解析后应该能：
1. 知道正确答案为什么对（推理链）
2. 知道自己为什么选错了（排除链）
3. 知道这道题考什么能力（考点一句话）

---

## 第一层：推理链 (reasoning_chain)

### 功能
展示从原文信息到正确答案的完整推理过程。

### 结构
```
定位原文 → 提取关键信息 → 推理 → 匹配选项
```

### 写法要求
- **必须引用原文具体位置**：第X段 / 第X段第Y句 / 文章开头 / 文章结尾
- **必须展示推理过程**：不是直接说"答案选B"，而是展示如何从原文推导到B
- **必须同义改写**：正确选项通常不是原文原话，要展示改写对应关系
- 长度 ≥ 50字

### 示例

**细节题推理链：**
> 题目问AI应用的主要担忧。根据第2段第3句"AI may displace workers in routine tasks while creating new categories of employment"，原文指出AI可能取代常规岗位的同时创造新的就业类别，B选项"displace workers in routine tasks while creating new roles"是对原文的准确概括，其中categories of employment ≈ roles。

**推理题推理链：**
> 题目问可从第2段推断出什么。第2段提到"the most productive applications involve collaborative frameworks in which human judgment and machine processing power complement one another"，虽未直接说AI不能完全替代人类，但"complement one another"暗示双方缺一不可，因此可推断C选项"human involvement remains essential in AI-driven systems"。

**词义题推理链：**
> 题目问displace的含义。根据第2段上下文，前文讨论AI对就业的影响，后文提到"creating new categories of employment"作为对比，由此推断displace与employment形成对立关系，不是"移动位置"而是"取代、使失业"，A选项replace最为接近。

**主旨题推理链：**
> 文章第1段引出AI对就业的影响话题，第2段分析AI对不同类型工作的差异化影响，第3段指出人机协作是最有效的应用模式，第4段总结社会适应能力是关键。全文围绕"AI对就业的复杂影响"展开，B选项最准确概括了这一主旨。

---

## 第二层：排除链 (elimination_chain)

### 功能
逐一分析3个错误选项，指出每个干扰项的陷阱类型和具体错误。

### 结构
```
选项A → 陷阱类型 → 具体错误 | 选项C → ... | 选项D → ...
```

### 写法要求
- **必须逐一分析**每个错误选项，不能遗漏
- **必须指出陷阱类型**：偷换段落/偷换主语/绝对化/立场反转
- **必须引用原文对照**：指出干扰项与原文的具体差异
- 长度 ≥ 100字

### 示例

> A选项使用了**绝对化陷阱**：原文第2段说"AI may displace workers in **some** routine tasks"，A选项将"some"替换为"all"，将可能性"may"变为确定性"will"，夸大了原文的表述。C选项使用了**立场反转陷阱**：原文明确指出AI"has indeed displaced certain categories of routine labor"，说明AI对就业有显著影响，C选项却说"no significant impact"，与原文立场完全相反。D选项使用了**偷换主语陷阱**：原文讨论的是全球范围内的就业影响，D选项将范围缩小为"developing countries"，原文并未限定地理范围。

---

## 第三层：考点一句话 (test_point_one_liner)

### 功能
用一句话概括这道题的核心考点，帮助学生理解考查的能力。

### 格式
```
题型：核心考点概括
```

### 写法要求
- 格式固定：`题型：考点`
- 题型必须与q_type对应：细节理解题/推理判断题/词义猜测题/主旨大意题
- 考点要具体，不能笼统地说"理解文章"
- 不超过30字

### 各题型考点示例

| 题型 | 考点一句话示例 |
|------|-------------|
| detail | 细节理解题：精准定位原文关键句，识别绝对化和偷换主语陷阱 |
| inference | 推理判断题：基于原文合理推断，区分事实与推论 |
| word_meaning | 词义猜测题：利用上下文对比关系推断词义 |
| main_idea | 主旨大意题：区分核心论点与支持细节 |
