#!/usr/bin/env python3
"""将周练JSON数据渲染为报纸风格HTML文件。"""

import json
import sys
import os
import html as html_module

ARTICLE_TAGS = [
    {"label": "A", "color_class": "", "color": "#1E6BB8"},
    {"label": "B", "color_class": "green", "color": "#27AE60"},
    {"label": "C", "color_class": "purple", "color": "#8E44AD"},
    {"label": "D", "color_class": "red", "color": "#C0392B"},
]

CSS = """
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

    .half-page {
        height: calc(50% - 3px);
        margin-bottom: 6px;
        overflow: hidden;
    }

    .half-page:last-child {
        margin-bottom: 0;
        margin-top: 6px;
    }

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

    .article-tag {
        display: inline-block;
        width: 20px;
        height: 20px;
        background: #1E6BB8;
        color: white;
        font-size: 11px;
        font-weight: bold;
        text-align: center;
        line-height: 20px;
        border-radius: 3px;
        font-family: "Arial Black", sans-serif;
        flex-shrink: 0;
    }

    .article-tag.green { background: #27AE60; }
    .article-tag.purple { background: #8E44AD; }
    .article-tag.red { background: #C0392B; }

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

    .article-image {
        width: 100%;
        max-height: 28mm;
        object-fit: cover;
        border-radius: 3px;
        margin-bottom: 3px;
    }

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
        content: "\\25CB  ";
        color: #CCC;
        position: absolute;
        left: 0;
    }

    .footer {
        text-align: center;
        margin-top: 4px;
        padding-top: 3px;
        border-top: 1px solid #E0E0E0;
        color: #999;
        font-size: 6px;
        font-family: "Arial", sans-serif;
    }

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

    .answer-header .article-title {
        font-size: 10px;
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
        margin-bottom: 6px;
    }

    .word-bank strong {
        color: #8E44AD;
    }

    .traps-section {
        font-size: 7px;
        line-height: 1.4;
        color: #666;
        padding-left: 5px;
        margin-bottom: 6px;
    }
"""

FOOTER_TEXT = "师倍AI · 外刊英语周周练 — 质量是命 · 减负是刀 · 单品是路"


def esc(text):
    return html_module.escape(str(text)) if text else ""


def render_masthead(issue_id, page_num, total_pages):
    return f"""<div class="masthead">
    <h1>师倍AI · 外刊英语周周练</h1>
    <div class="week-info">{esc(issue_id)}</div>
    <div class="page-number">{page_num} <span>/ {total_pages}</span></div>
</div>"""


def render_article(art, tag_info):
    ra = art.get("rewritten_article", {})
    source = art.get("source", {})
    questions = art.get("questions", [])

    header = f"""<div class="article-header">
    <span class="article-tag {tag_info['color_class']}">{tag_info['label']}</span>
    <div>
        <div class="article-title">{esc(ra.get('title_en', ''))}</div>
        <div class="article-source">{esc(source.get('publication', ''))} | {esc(source.get('topic_category', ''))}</div>
    </div>
</div>"""

    image = ""
    image_url = art.get("image_url") or source.get("image_url")
    if image_url:
        image = f'<img class="article-image" src="{esc(image_url)}" alt="{esc(ra.get("title_en", ""))}">'

    flow_parts = []

    for idx, p in enumerate(ra.get("paragraphs", [])):
        if idx == 0:
            cls = f"article-text first-para drop-{tag_info['label']}"
        else:
            cls = "article-text"
        flow_parts.append(f'<p class="{cls}">{esc(p["text"])}</p>')

    if questions:
        flow_parts.append('<div class="questions-header">Questions</div>')
        for q in questions:
            opts = "\n".join(
                f"            <li>{opt['label']}. {esc(opt['text'])}</li>"
                for opt in q.get("options", [])
            )
            flow_parts.append(f"""<div class="question-item">
        <div class="question-title">{q['q_id']}. ({q['q_type']}) {esc(q['stem'])}</div>
        <ul class="question-options">
{opts}
        </ul>
    </div>""")

    flow_html = "\n        ".join(flow_parts)

    return f"""<div class="half-page">
    {header}
    {image}
    <div class="three-col-flow">
        {flow_html}
    </div>
</div>"""


def render_answer_section(art, tag_info):
    ra = art.get("rewritten_article", {})
    questions = art.get("questions", [])
    explanations = art.get("explanations", [])
    takeaways = art.get("takeaways", {})

    header = f"""<div class="answer-header">
    <span class="article-tag {tag_info['color_class']}">{tag_info['label']}</span>
    <div>
        <div class="article-title">{esc(ra.get('title_en', ''))}</div>
    </div>
</div>"""

    choices_html = " ".join(
        f'<span class="answer-choice">{q["q_id"]}: {q["correct_answer"]}</span>'
        for q in questions
    )
    choices_div = f'<div class="answer-choices">{choices_html}</div>'

    exp_parts = []
    for exp in explanations:
        exp_parts.append(f"""<div class="explanation-block">
    <strong>{esc(exp['q_id'])}</strong> {esc(exp.get('test_point_one_liner', ''))}<br>
    推理链：{esc(exp.get('reasoning_chain', ''))}<br>
    排除链：{esc(exp.get('elimination_chain', ''))}
</div>""")

    traps_parts = []
    for q in questions:
        for trap in q.get("distractor_traps", []):
            traps_parts.append(
                f'{q["q_id"]}-{trap["option"]} [{trap["trap_type"]}]: {esc(trap.get("explanation", ""))}'
            )
    traps_html = ""
    if traps_parts:
        traps_html = f'<div class="traps-section">{"<br>".join(traps_parts)}</div>'

    bank_parts = []

    collocations = takeaways.get("new_collocations", [])
    if collocations:
        items = "<br>".join(
            f'• <strong>{esc(c["collocation"])}</strong> — {esc(c.get("meaning_zh", ""))}'
            for c in collocations
        )
        bank_parts.append(f"<strong>新搭配</strong><br>{items}")

    familiar = takeaways.get("familiar_words_unfamiliar_meanings", [])
    if familiar:
        items = "<br>".join(
            f'• <strong>{esc(fw["word"])}</strong>：常见义"{esc(fw.get("familiar_meaning", ""))}" → 文中义"{esc(fw.get("new_meaning_in_context", ""))}"'
            for fw in familiar
        )
        bank_parts.append(f"<strong>熟词生义</strong><br>{items}")

    errors = takeaways.get("common_errors", [])
    if errors:
        items = "<br>".join(
            f'• {esc(err.get("error_description", ""))}（{err.get("related_q_id", "")}）💡 {esc(err.get("tip", ""))}'
            for err in errors
        )
        bank_parts.append(f"<strong>易错点</strong><br>{items}")

    bank_html = ""
    if bank_parts:
        bank_html = f'<div class="word-bank">{"<br><br>".join(bank_parts)}</div>'

    return f"""<div class="answer-section">
    {header}
    {choices_div}
    {"".join(exp_parts)}
    {traps_html}
    {bank_html}
</div>"""


def main():
    if len(sys.argv) != 3:
        print("用法: python3 render_html.py <workspace_dir> <issue_id>")
        sys.exit(1)

    workspace_dir = sys.argv[1]
    issue_id = sys.argv[2]

    full_set_path = os.path.join(workspace_dir, "output", f"{issue_id}_full_set.json")

    if not os.path.exists(full_set_path):
        intermediate_dir = os.path.join(workspace_dir, "intermediate")
        articles = []
        for seq in range(1, 5):
            json_path = os.path.join(intermediate_dir, f"{issue_id}_article_{seq:02d}.json")
            if os.path.exists(json_path):
                with open(json_path, "r", encoding="utf-8") as f:
                    articles.append(json.load(f))
            else:
                print(f"⚠️ 文件不存在: {json_path}")
        full_set = {"issue_id": issue_id, "articles": articles}
    else:
        with open(full_set_path, "r", encoding="utf-8") as f:
            full_set = json.load(f)

    articles = full_set.get("articles", [])
    if len(articles) != 4:
        print(f"⚠️ 只找到 {len(articles)}/4 篇文章")

    total_pages = 3

    page1_inner = render_masthead(issue_id, 1, total_pages)
    for i in range(min(2, len(articles))):
        page1_inner += render_article(articles[i], ARTICLE_TAGS[i])
    page1_inner += f'<div class="footer">{FOOTER_TEXT}</div>'

    page2_inner = render_masthead(issue_id, 2, total_pages)
    for i in range(2, min(4, len(articles))):
        page2_inner += render_article(articles[i], ARTICLE_TAGS[i])
    page2_inner += f'<div class="footer">{FOOTER_TEXT}</div>'

    page3_inner = render_masthead(issue_id, 3, total_pages)
    for i in range(len(articles)):
        page3_inner += render_answer_section(articles[i], ARTICLE_TAGS[i])
    page3_inner += f'<div class="footer">{FOOTER_TEXT}</div>'

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>师倍AI · 外刊英语周周练 {esc(issue_id)}</title>
    <style>{CSS}
    </style>
</head>
<body>
    <div class="page">
        {page1_inner}
    </div>

    <div class="page">
        {page2_inner}
    </div>

    <div class="page">
        {page3_inner}
    </div>
</body>
</html>"""

    output_dir = os.path.join(workspace_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{issue_id}_printable.html")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ HTML文件: {output_path}")

    topics = [a.get("source", {}).get("topic_category", "?") for a in articles]
    sources = [a.get("source", {}).get("publication", "?") for a in articles]
    images = sum(1 for a in articles if a.get("image_url") or a.get("source", {}).get("image_url"))
    print(f"   话题: {', '.join(topics)}")
    print(f"   来源: {', '.join(sources)}")
    print(f"   配图: {images}/4")
    print(f"   浏览器打开后 Ctrl+P 打印为PDF")


if __name__ == "__main__":
    main()
