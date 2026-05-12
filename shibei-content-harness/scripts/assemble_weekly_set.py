#!/usr/bin/env python3
"""组装周练输出：合并4篇文章JSON，生成索引和可打印Markdown。"""

import json
import sys
import os
from datetime import datetime


def load_article(json_path: str) -> dict:
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_index(articles: list[dict], issue_id: str, issue_date: str) -> dict:
    topic_dist = {}
    source_dist = {}

    article_entries = []
    for art in articles:
        seq = art['article_seq']
        topic = art.get('source', {}).get('topic_category', 'unknown')
        source = art.get('source', {}).get('publication', 'unknown')
        status = 'completed' if art.get('review', {}).get('overall_pass', False) else 'needs_manual_review'

        article_entries.append({
            'seq': seq,
            'file': f"{issue_id}_article_{seq:02d}.json",
            'topic': topic,
            'source': source,
            'status': status
        })

        topic_dist[topic] = topic_dist.get(topic, 0) + 1
        source_dist[source] = source_dist.get(source, 0) + 1

    return {
        'issue_id': issue_id,
        'issue_title_zh': f'师倍AI · 外刊英语周周练 {issue_id}',
        'issue_date': issue_date,
        'articles': article_entries,
        'topic_distribution': topic_dist,
        'source_distribution': source_dist
    }


def generate_printable(articles: list[dict], issue_id: str) -> str:
    lines = []
    lines.append(f'# 师倍AI · 外刊英语周周练 {issue_id}')
    lines.append('')
    lines.append('---')
    lines.append('')

    for art in articles:
        ra = art.get('rewritten_article', {})
        source = art.get('source', {})
        questions = art.get('questions', [])
        explanations = art.get('explanations', [])
        takeaways = art.get('takeaways', {})

        # Article header
        lines.append(f'## Passage {art["article_seq"]}')
        lines.append('')
        lines.append(f'**{ra.get("title_en", "")}**')
        lines.append(f'*{ra.get("title_zh", "")}*')
        lines.append(f'> Source: {source.get("publication", "")} | Topic: {source.get("topic_category", "")}')
        lines.append('')

        # Article body
        for p in ra.get('paragraphs', []):
            lines.append(f'　　{p["text"]}')
            lines.append('')

        lines.append('---')
        lines.append('')

        # Questions
        lines.append('### Questions')
        lines.append('')
        for q in questions:
            lines.append(f'**{q["q_id"]}.** ({q["q_type"]}) {q["stem"]}')
            for opt in q.get('options', []):
                marker = ' ✓' if opt.get('is_correct') else ''
                lines.append(f'- {opt["label"]}. {opt["text"]}{marker}')
            lines.append('')

        lines.append('---')
        lines.append('')

        # Explanations
        lines.append('### Explanations')
        lines.append('')
        for exp in explanations:
            lines.append(f'**{exp["q_id"]}.** {exp["test_point_one_liner"]}')
            lines.append(f'- **推理链**：{exp["reasoning_chain"]}')
            lines.append(f'- **排除链**：{exp["elimination_chain"]}')
            lines.append('')

        lines.append('---')
        lines.append('')

        # Takeaways
        lines.append('### 我的收获')
        lines.append('')

        collocations = takeaways.get('new_collocations', [])
        if collocations:
            lines.append('**新搭配**：')
            for c in collocations:
                lines.append(f'- **{c["collocation"]}** — {c["meaning_zh"]}')
                lines.append(f'  例：{c["example_sentence"]}')
            lines.append('')

        familiar = takeaways.get('familiar_words_unfamiliar_meanings', [])
        if familiar:
            lines.append('**熟词生义**：')
            for fw in familiar:
                lines.append(f'- **{fw["word"]}**：常见义"{fw["familiar_meaning"]}" → 文中义"{fw["new_meaning_in_context"]}"')
                lines.append(f'  例：{fw["example_sentence"]}')
            lines.append('')

        errors = takeaways.get('common_errors', [])
        if errors:
            lines.append('**易错点**：')
            for err in errors:
                lines.append(f'- {err["error_description"]}（{err["related_q_id"]}）')
                lines.append(f'  💡 {err["tip"]}')
            lines.append('')

        lines.append('---')
        lines.append('')

    # Footer
    lines.append('*师倍AI · 外刊英语周周练 — 质量是命 · 减负是刀 · 单品是路*')

    return '\n'.join(lines)


def main():
    if len(sys.argv) != 3:
        print('用法: python3 assemble_weekly_set.py <workspace_dir> <issue_id>')
        sys.exit(1)

    workspace_dir = sys.argv[1]
    issue_id = sys.argv[2]
    intermediate_dir = os.path.join(workspace_dir, 'intermediate')
    output_dir = os.path.join(workspace_dir, 'output')

    os.makedirs(output_dir, exist_ok=True)

    # Load all 4 articles
    articles = []
    for seq in range(1, 5):
        json_path = os.path.join(intermediate_dir, f'{issue_id}_article_{seq:02d}.json')
        if os.path.exists(json_path):
            articles.append(load_article(json_path))
        else:
            print(f'⚠️ 文件不存在: {json_path}')

    if len(articles) != 4:
        print(f'⚠️ 只找到 {len(articles)}/4 篇文章')

    # Get issue_date from first article
    issue_date = articles[0].get('source', {}).get('found_date', '2026-05-09') if articles else '2026-05-09'

    # Generate index
    index = generate_index(articles, issue_id, issue_date)
    index_path = os.path.join(output_dir, f'{issue_id}_index.json')
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f'✅ 索引文件: {index_path}')

    # Generate full set
    full_set = {
        'issue_id': issue_id,
        'issue_date': issue_date,
        'articles': articles
    }
    full_set_path = os.path.join(output_dir, f'{issue_id}_full_set.json')
    with open(full_set_path, 'w', encoding='utf-8') as f:
        json.dump(full_set, f, ensure_ascii=False, indent=2)
    print(f'✅ 完整数据: {full_set_path}')

    # Generate printable markdown
    printable = generate_printable(articles, issue_id)
    printable_path = os.path.join(output_dir, f'{issue_id}_printable.md')
    with open(printable_path, 'w', encoding='utf-8') as f:
        f.write(printable)
    print(f'✅ 可打印MD: {printable_path}')


if __name__ == '__main__':
    main()
