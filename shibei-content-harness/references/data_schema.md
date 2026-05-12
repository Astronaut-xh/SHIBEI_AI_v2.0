# 完整JSON Schema文档

## 文章JSON Schema

每篇文章对应一个JSON文件，字段随流水线步骤逐步累积。

### 完整字段一览

```json
{
  "issue_id": "W2026W19",
  "article_seq": 1,

  "source": {
    "url": "string (URL)",
    "publication": "NYT | The Guardian | The Economist | Scientific American | China Daily",
    "topic_category": "technology | environment | society | health",
    "original_title": "string",
    "original_word_count": "integer > 500",
    "found_date": "string (YYYY-MM-DD)",
    "finder_notes": "string",
    "image_url": "string (data:image/svg+xml;base64,...) — 必需，由阶段7配图生成步骤写入"
  },

  "rewritten_article": {
    "title_en": "string",
    "title_zh": "string",
    "body": "string (250-350 words)",
    "word_count": "integer",
    "long_sentences_count": "integer ≥ 2",
    "paragraphs": [
      {
        "index": "integer ≥ 0",
        "text": "string",
        "word_count": "integer > 0"
      }
    ],
    "rewrite_version": "integer ≥ 1",
    "rewriter_notes": "string"
  },

  "questions": [
    {
      "q_id": "Q1 | Q2 | Q3 | Q4",
      "q_type": "detail | inference | word_meaning | main_idea",
      "stem": "string",
      "options": [
        {
          "label": "A | B | C | D",
          "text": "string",
          "is_correct": "boolean"
        }
      ],
      "correct_answer": "A | B | C | D",
      "distractor_traps": [
        {
          "option": "A | B | C | D",
          "trap_type": "paragraph_swap | subject_swap | absolutization | stance_reversal",
          "explanation": "string"
        }
      ],
      "source_paragraph_index": "integer | null",
      "difficulty": "easy | medium | hard",
      "target_word": "string (仅word_meaning题)",
      "target_word_context": "string (仅word_meaning题)"
    }
  ],

  "explanations": [
    {
      "q_id": "Q1 | Q2 | Q3 | Q4",
      "reasoning_chain": "string ≥ 50 chars",
      "elimination_chain": "string ≥ 100 chars",
      "test_point_one_liner": "string ≤ 30 chars",
      "explanation_version": "integer ≥ 1"
    }
  ],

  "takeaways": {
    "new_collocations": [
      {
        "collocation": "string",
        "meaning_zh": "string",
        "example_sentence": "string",
        "source_paragraph_index": "integer"
      }
    ],
    "familiar_words_unfamiliar_meanings": [
      {
        "word": "string",
        "familiar_meaning": "string",
        "new_meaning_in_context": "string",
        "example_sentence": "string",
        "source_paragraph_index": "integer"
      }
    ],
    "common_errors": [
      {
        "error_description": "string",
        "related_q_id": "string",
        "tip": "string"
      }
    ],
    "takeaway_version": "integer ≥ 1"
  },

  "review": {
    "review_version": "integer ≥ 1",
    "overall_pass": "boolean",
    "scores": {
      "fluency": "integer 1-10",
      "unique_correct_answer": "integer 1-10",
      "explanation_persuasiveness": "integer 1-10",
      "distractor_reasonableness": "integer 1-10",
      "takeaway_usefulness": "integer 1-10"
    },
    "dimension_reviews": {
      "fluency": { "pass": "boolean", "comment": "string", "issues": ["string"] },
      "unique_correct_answer": { "pass": "boolean", "comment": "string", "issues": ["string"] },
      "explanation_persuasiveness": { "pass": "boolean", "comment": "string", "issues": ["string"] },
      "distractor_reasonableness": { "pass": "boolean", "comment": "string", "issues": ["string"] },
      "takeaway_usefulness": { "pass": "boolean", "comment": "string", "issues": ["string"] }
    },
    "rewrite_needed": "boolean",
    "rewrite_targets": ["rewritten_article | questions | explanations | takeaways"],
    "review_timestamp": "string (ISO 8601)"
  },

  "pipeline_status": {
    "article_finder": "pending | completed | failed",
    "article_rewriter": "pending | completed | failed",
    "question_generator": "pending | completed | failed",
    "explanation_generator": "pending | completed | failed",
    "takeaway_generator": "pending | completed | failed",
    "content_reviewer": "pending | completed | failed",
    "image_generator": "pending | completed | failed",
    "current_step": "initialized | article_finder | article_rewriter | question_generator | explanation_generator | takeaway_generator | content_reviewer | image_generator | completed | needs_manual_review",
    "retry_count": "integer ≥ 0",
    "max_retries": "integer (default 2)",
    "last_modified": "string (ISO 8601)"
  }
}
```

### 约束规则

1. **4题4型**：questions数组恰好4项，q_type覆盖4种题型各1次
2. **4选项**：每题4个options，label为A-D，恰好1个is_correct=true
3. **3陷阱**：每题3个distractor_traps，对应3个错误选项，每项有trap_type
4. **版本号**：rewrite_version/explanation_version/takeaway_version/review_version，每次返工递增
5. **词数**：rewritten_article.word_count必须在250-350之间
6. **长难句**：long_sentences_count ≥ 2

### 字段名硬约束（严禁变更）

以下字段名是组装脚本和校验脚本的依赖项，**严禁使用别名**：

| 块 | 正确字段名 | 禁止使用的别名 |
|---|---|---|
| questions | `q_id` | ~~seq~~ |
| questions | `q_type` | ~~type~~ |
| questions | `correct_answer` | 必须存在，值与is_correct=true的label一致 |
| questions | `distractor_traps` | 不得省略，不得将trap_type放在options内 |
| questions.options | 仅 `label/text/is_correct` | 不得在此处放trap_type |
| takeaways.new_collocations | `example_sentence` | ~~source_sentence~~ |
| takeaways.new_collocations | `source_paragraph_index` | 必须存在 |
| takeaways.familiar_words | `new_meaning_in_context` | ~~article_meaning~~ |
| takeaways.familiar_words | `example_sentence` | ~~source_sentence~~ |
| takeaways.familiar_words | `source_paragraph_index` | 必须存在 |
| takeaways.common_errors | `error_description` | ~~trap_option_summary~~/~~analysis~~ |
| takeaways.common_errors | `tip` | ~~strategy~~ |

## 索引JSON Schema

```json
{
  "issue_id": "string",
  "issue_title_zh": "string",
  "issue_date": "string (YYYY-MM-DD)",
  "articles": [
    {
      "seq": "integer 1-4",
      "file": "string (filename)",
      "topic": "string",
      "source": "string",
      "status": "completed | needs_manual_review"
    }
  ],
  "topic_distribution": { "technology": 1, "environment": 1, "health": 1, "society": 1 },
  "source_distribution": { "The Economist": 1, ... }
}
```
