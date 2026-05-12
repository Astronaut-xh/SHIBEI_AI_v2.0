#!/usr/bin/env python3
"""校验改写后的文章是否符合质量标准。"""

import json
import sys
import re


def count_words(text: str) -> int:
    return len(text.split())


def count_long_sentences(text: str, threshold: int = 25) -> int:
    sentences = re.split(r'[.!?]+', text)
    return sum(1 for s in sentences if count_words(s.strip()) > threshold)


def validate_article(json_path: str) -> list[str]:
    errors = []

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    ra = data.get('rewritten_article')
    if not ra:
        return ['rewritten_article 块不存在']

    # Word count
    body = ra.get('body', '')
    word_count = count_words(body)
    reported_wc = ra.get('word_count', 0)

    if word_count < 250:
        errors.append(f'词数不足：{word_count} < 250')
    elif word_count > 350:
        errors.append(f'词数超标：{word_count} > 350')

    if abs(word_count - reported_wc) > 5:
        errors.append(f'词数不一致：实际{word_count} vs 报告{reported_wc}')

    # Long sentences
    long_sents = count_long_sentences(body)
    reported_ls = ra.get('long_sentences_count', 0)
    if long_sents < 2:
        errors.append(f'长难句不足：{long_sents} < 2')
    if abs(long_sents - reported_ls) > 1:
        errors.append(f'长难句数不一致：实际{long_sents} vs 报告{reported_ls}')

    # Colloquialisms
    colloquial = re.findall(r"\b(don't|it's|can't|won't|isn't|aren't|wasn't|weren't|gonna|kinda|sorta|awesome|cool)\b", body, re.IGNORECASE)
    if colloquial:
        errors.append(f'存在口语表达：{colloquial}')

    # Paragraphs
    paragraphs = ra.get('paragraphs', [])
    if len(paragraphs) < 3:
        errors.append(f'段落数不足：{len(paragraphs)} < 3')
    elif len(paragraphs) > 5:
        errors.append(f'段落数过多：{len(paragraphs)} > 5')

    for p in paragraphs:
        pw = count_words(p.get('text', ''))
        if pw == 0:
            errors.append(f'段落{p.get("index", "?")}为空')

    # Title
    if not ra.get('title_en'):
        errors.append('缺少英文标题')
    if not ra.get('title_zh'):
        errors.append('缺少中文标题')

    return errors


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('用法: python3 validate_article.py <article_json_path>')
        sys.exit(1)

    errs = validate_article(sys.argv[1])
    if errs:
        print('❌ 校验失败：')
        for e in errs:
            print(f'  - {e}')
        sys.exit(1)
    else:
        print('✅ 校验通过')
