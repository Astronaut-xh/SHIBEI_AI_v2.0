#!/usr/bin/env python3
"""校验生成的阅读理解题目是否符合质量标准。"""

import json
import sys


VALID_Q_TYPES = {'detail', 'inference', 'word_meaning', 'main_idea'}
VALID_TRAP_TYPES = {'paragraph_swap', 'subject_swap', 'absolutization', 'stance_reversal'}
VALID_LABELS = {'A', 'B', 'C', 'D'}
VALID_DIFFICULTIES = {'easy', 'medium', 'hard'}


def validate_questions(json_path: str) -> list[str]:
    errors = []

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = data.get('questions')
    if not questions:
        return ['questions 块不存在或为空']

    # Count check
    if len(questions) != 4:
        errors.append(f'题目数量不正确：{len(questions)} ≠ 4')

    # Q type coverage
    q_types = [q.get('q_type') for q in questions]
    missing_types = VALID_Q_TYPES - set(q_types)
    if missing_types:
        errors.append(f'缺少题型：{missing_types}')

    # Q IDs
    expected_ids = {'Q1', 'Q2', 'Q3', 'Q4'}
    actual_ids = {q.get('q_id') for q in questions}
    if actual_ids != expected_ids:
        errors.append(f'q_id不正确：{actual_ids} ≠ {expected_ids}')

    for q in questions:
        q_id = q.get('q_id', '?')

        # Q type valid
        if q.get('q_type') not in VALID_Q_TYPES:
            errors.append(f'{q_id}: 无效题型 {q.get("q_type")}')

        # Options
        options = q.get('options', [])
        if len(options) != 4:
            errors.append(f'{q_id}: 选项数量 {len(options)} ≠ 4')
            continue

        labels = {o.get('label') for o in options}
        if labels != VALID_LABELS:
            errors.append(f'{q_id}: 选项标签不正确 {labels}')

        correct = [o for o in options if o.get('is_correct')]
        if len(correct) != 1:
            errors.append(f'{q_id}: 正确选项数量 {len(correct)} ≠ 1')

        # correct_answer matches
        if correct:
            correct_label = correct[0].get('label')
            if q.get('correct_answer') != correct_label:
                errors.append(f'{q_id}: correct_answer({q.get("correct_answer")}) ≠ is_correct label({correct_label})')

        # Distractor traps
        incorrect_labels = {o.get('label') for o in options if not o.get('is_correct')}
        traps = q.get('distractor_traps', [])
        trap_labels = {t.get('option') for t in traps}

        if trap_labels != incorrect_labels:
            errors.append(f'{q_id}: 陷阱覆盖的选项 {trap_labels} ≠ 错误选项 {incorrect_labels}')

        for t in traps:
            if t.get('trap_type') not in VALID_TRAP_TYPES:
                errors.append(f'{q_id} 选项{t.get("option")}: 无效陷阱类型 {t.get("trap_type")}')

        # Difficulty
        if q.get('difficulty') not in VALID_DIFFICULTIES:
            errors.append(f'{q_id}: 无效难度 {q.get("difficulty")}')

        # Paragraph index
        if q.get('q_type') == 'main_idea':
            if q.get('source_paragraph_index') is not None:
                errors.append(f'{q_id}: main_ima题的source_paragraph_index应为null')
        else:
            if q.get('source_paragraph_index') is None:
                errors.append(f'{q_id}: 非main_idea题必须有source_paragraph_index')

        # Word meaning specific
        if q.get('q_type') == 'word_meaning':
            if not q.get('target_word'):
                errors.append(f'{q_id}: word_meaning题必须有target_word')
            if not q.get('target_word_context'):
                errors.append(f'{q_id}: word_meaning题必须有target_word_context')

    # Check trap diversity per question
    for q in questions:
        q_id = q.get('q_id', '?')
        traps = q.get('distractor_traps', [])
        trap_types = [t.get('trap_type') for t in traps]
        if len(trap_types) != len(set(trap_types)):
            errors.append(f'{q_id}: 同一题出现重复陷阱类型（建议每题3种不同陷阱）')

    return errors


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('用法: python3 validate_questions.py <article_json_path>')
        sys.exit(1)

    errs = validate_questions(sys.argv[1])
    if errs:
        print('❌ 校验失败：')
        for e in errs:
            print(f'  - {e}')
        sys.exit(1)
    else:
        print('✅ 校验通过')
