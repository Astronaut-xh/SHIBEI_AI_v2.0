#!/usr/bin/env python3
"""计算审核评分汇总。"""

import json
import sys
from datetime import datetime


THRESHOLDS = {
    'fluency': 7,
    'unique_correct_answer': 9,
    'explanation_persuasiveness': 7,
    'distractor_reasonableness': 7,
    'takeaway_usefulness': 7,
}

SCORE_TO_REWRITE_TARGET = {
    'fluency': 'rewritten_article',
    'unique_correct_answer': 'questions',
    'explanation_persuasiveness': 'explanations',
    'distractor_reasonableness': 'questions',
    'takeaway_usefulness': 'takeaways',
}


def compute_review(json_path: str) -> None:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    review = data.get('review', {})
    scores = review.get('scores', {})

    # Validate scores
    for dim, threshold in THRESHOLDS.items():
        score = scores.get(dim)
        if score is None:
            print(f'⚠️ 缺少维度评分: {dim}')
            continue
        if not (1 <= score <= 10):
            print(f'⚠️ 评分超出范围: {dim}={score}')
            continue

        passed = score >= threshold
        status = '✅ 通过' if passed else '❌ 未通过'
        print(f'{dim}: {score}/10 (阈值{threshold}) {status}')

    # Compute overall
    all_pass = all(
        scores.get(dim, 0) >= threshold
        for dim, threshold in THRESHOLDS.items()
    )

    # Compute rewrite targets
    rewrite_targets = []
    for dim, threshold in THRESHOLDS.items():
        if scores.get(dim, 0) < threshold:
            target = SCORE_TO_REWRITE_TARGET[dim]
            if target not in rewrite_targets:
                rewrite_targets.append(target)

    print(f'\n总体结果: {"✅ 通过" if all_pass else "❌ 未通过"}')
    if rewrite_targets:
        print(f'需返工: {rewrite_targets}')
    else:
        print('无需返工')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('用法: python3 compute_review_score.py <article_json_path>')
        sys.exit(1)

    compute_review(sys.argv[1])
