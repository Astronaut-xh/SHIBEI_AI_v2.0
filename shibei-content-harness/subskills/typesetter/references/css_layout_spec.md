# CSS布局完整规范

## 页面基础

```css
@page {
    size: A4;
    margin: 10mm;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: "Times New Roman", Georgia, serif;
    background-color: #F5F5F0;
    color: #333;
    font-size: 10px;
    line-height: 1.5;
}
```

## 页面容器

```css
.page {
    width: 210mm;
    min-height: 297mm;
    margin: 0 auto;
    padding: 8mm;
    background: white;
}

@media print {
    .page { page-break-after: always; }
    .page:last-child { page-break-after: auto; }
}
```

## 页眉 Masthead

```css
.masthead {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #1E6BB8;
    padding-bottom: 5px;
    margin-bottom: 6px;
}

.masthead h1 {
    font-family: "Microsoft YaHei", "SimHei", sans-serif;
    font-size: 14px;
    color: #1E6BB8;
    letter-spacing: 1px;
}

.masthead .week-info {
    font-size: 8px;
    color: #666;
}

.page-number {
    font-size: 16px;
    font-weight: bold;
    color: #1E6BB8;
    font-family: "Arial Black", sans-serif;
}

.page-number span {
    font-size: 9px;
    color: #333;
    font-weight: normal;
}
```

## 文章半页容器

```css
.half-page {
    height: calc(50% - 3px);
    margin-bottom: 6px;
}

.half-page:last-child {
    margin-bottom: 0;
    margin-top: 6px;
}
```

## 文章头部

```css
.article-header {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 3px 5px;
    background: linear-gradient(to right, #F0F7FF, #FAFAFA);
    border: 1px solid #D0E4F5;
    border-radius: 3px;
    margin-bottom: 3px;
}
```

## 文章标识ABCD

```css
.article-tag {
    display: inline-block;
    width: 20px;
    height: 20px;
    background: #1E6BB8;  /* A-蓝色 */
    color: white;
    font-size: 11px;
    font-weight: bold;
    text-align: center;
    line-height: 20px;
    border-radius: 3px;
    font-family: "Arial Black", sans-serif;
}

.article-tag.green { background: #27AE60; }   /* B-绿色 */
.article-tag.purple { background: #8E44AD; } /* C-紫色 */
.article-tag.red { background: #C0392B; }     /* D-红色 */
```

## 文章标题和来源

```css
.article-title {
    font-size: 11px;
    font-weight: bold;
    color: #1a1a1a;
    line-height: 1.3;
}

.article-source {
    font-size: 7px;
    color: #999;
}
```

## 文章图片

```css
.article-image {
    width: 100%;
    max-height: 28mm;
    object-fit: cover;
    border-radius: 3px;
    margin-bottom: 3px;
}
```

## 三栏流淌区域

```css
.three-col-flow {
    columns: 3;
    column-gap: 10px;
    column-rule: none;
    padding: 0 3px;
}

.three-col-flow p.article-text {
    text-indent: 1.5em;
    margin-bottom: 0.3em;
    font-size: 10px;
    line-height: 1.45;
    text-align: justify;
}

.three-col-flow p.article-text.first-para {
    text-indent: 0;
}

.three-col-flow p.article-text.first-para::first-letter {
    float: left;
    font-size: 2.8em;
    line-height: 0.85;
    padding-right: 3px;
    padding-top: 2px;
    font-weight: bold;
    font-family: "Georgia", serif;
}

.three-col-flow p.article-text.first-para.drop-A::first-letter { color: #1E6BB8; }
.three-col-flow p.article-text.first-para.drop-B::first-letter { color: #27AE60; }
.three-col-flow p.article-text.first-para.drop-C::first-letter { color: #8E44AD; }
.three-col-flow p.article-text.first-para.drop-D::first-letter { color: #C0392B; }
```

## 题目区域

```css
.three-col-flow .questions-header {
    font-size: 9px;
    font-weight: bold;
    color: #E67E22;
    margin: 4px 0 3px 0;
    padding: 3px 5px;
    background: #FFF8F0;
    border: 1px dashed #E67E22;
    border-radius: 2px;
}

.three-col-flow .question-item {
    font-size: 9px;
    line-height: 1.35;
    margin-bottom: 5px;
    padding: 4px;
    background: #FAFAFA;
    border-radius: 2px;
    border-left: 3px solid #E67E22;
}

.three-col-flow .question-title {
    font-weight: bold;
    color: #333;
    margin-bottom: 2px;
    font-family: "Arial", sans-serif;
}

.three-col-flow .question-options {
    list-style: none;
    font-size: 8px;
    line-height: 1.3;
    padding-left: 4px;
}

.three-col-flow .question-options li {
    padding-left: 12px;
    position: relative;
}

.three-col-flow .question-options li::before {
    content: "○ ";
    color: #CCC;
    position: absolute;
    left: 0;
}
```

## 页脚

```css
.footer {
    text-align: center;
    margin-top: 4px;
    padding-top: 3px;
    border-top: 1px solid #E0E0E0;
    color: #999;
    font-size: 6px;
    font-family: "Arial", sans-serif;
}
```

## 答案解析页

```css
.answer-section {
    margin-bottom: 12px;
    page-break-inside: avoid;
}

.answer-header {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 4px 6px;
    background: linear-gradient(to right, #FFF8F0, #FFFDF9);
    border: 1px solid #E8D4C4;
    border-radius: 3px;
    margin-bottom: 6px;
}

.answer-choices {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 6px;
}

.answer-choice {
    font-size: 9px;
    font-weight: bold;
    color: #27AE60;
    background: #E8F8F0;
    padding: 2px 6px;
    border-radius: 3px;
}

.explanation-block {
    font-size: 8px;
    line-height: 1.5;
    padding: 4px 5px;
    background: #FAFAFA;
    border-left: 3px solid #1E6BB8;
    margin-bottom: 4px;
}

.explanation-block strong {
    color: #1E6BB8;
}

.word-bank {
    font-size: 8px;
    line-height: 1.5;
    padding: 4px 5px;
    background: #F8F8FF;
    border: 1px solid #E0E0E8;
    border-radius: 3px;
}

.word-bank strong {
    color: #8E44AD;
}

.traps-section {
    font-size: 7px;
    line-height: 1.4;
    color: #666;
    padding-left: 5px;
}
```

## HTML结构示例

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>师倍AI · 外刊英语周周练 W2026W19</title>
    <style>/* 上述全部CSS */</style>
</head>
<body>
    <!-- 第1页: Passage A + B -->
    <div class="page">
        <div class="masthead">...</div>
        <div class="half-page">[Passage A]</div>
        <div class="half-page">[Passage B]</div>
        <div class="footer">...</div>
    </div>

    <!-- 第2页: Passage C + D -->
    <div class="page">
        <div class="masthead">...</div>
        <div class="half-page">[Passage C]</div>
        <div class="half-page">[Passage D]</div>
        <div class="footer">...</div>
    </div>

    <!-- 第3页: 答案解析 -->
    <div class="page">
        <div class="masthead">...</div>
        [4篇文章的答案解析]
        <div class="footer">...</div>
    </div>
</body>
</html>
```
