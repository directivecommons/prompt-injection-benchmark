# PIDB Results Schema v1.0

This document defines the canonical schema for reporting benchmark results. All submissions to the leaderboard must conform to this schema.

---

## Overview

The results schema is designed to be:
- **Complete**: Captures all essential performance metrics
- **Reproducible**: Enables verification and comparison
- **Machine-readable**: Easy to parse and validate
- **Human-friendly**: Clear structure and field names

---

## Schema Version

**Current Version**: 1.0.0  
**Benchmark Version**: 1.0.0 (643 test cases)  
**Last Updated**: 2026-01-16

---

## Complete Schema

### File: `pidb_results.json`

```json
{
  "schema_version": "1.0.0",
  "tool": {
    "name": "string (required)",
    "version": "string (required)",
    "organization": "string (optional)",
    "website": "string (optional)",
    "description": "string (optional)"
  },
  "run": {
    "test_date": "ISO 8601 datetime (required)",
    "benchmark_version": "string (required, must be '1.0.0')",
    "total_test_cases": "integer (required, must be 643)",
    "evaluator_version": "string (optional)",
    "notes": "string (optional)"
  },
  "overall": {
    "accuracy": "float (required, 0-100)",
    "passed": "integer (required)",
    "failed": "integer (required)"
  },
  "error_breakdown": {
    "false_negatives": "integer (required)",
    "false_positives": "integer (required)",
    "false_negative_rate": "float (required, 0-100)",
    "false_positive_rate": "float (required, 0-100)",
    "runtime_errors": "integer (optional, default 0)"
  },
  "by_category": {
    "<category_name>": {
      "accuracy": "float (required, 0-100)",
      "correct": "integer (required)",
      "total": "integer (required)",
      "false_negatives": "integer (optional)",
      "false_positives": "integer (optional)"
    }
  },
  "by_severity": {
    "critical": { "accuracy": "float", "correct": "integer", "total": "integer" },
    "high": { "accuracy": "float", "correct": "integer", "total": "integer" },
    "medium": { "accuracy": "float", "correct": "integer", "total": "integer" },
    "low": { "accuracy": "float", "correct": "integer", "total": "integer" },
    "null": { "accuracy": "float", "correct": "integer", "total": "integer" }
  },
  "performance": {
    "avg_latency_ms": "float (optional)",
    "median_latency_ms": "float (optional)",
    "p95_latency_ms": "float (optional)",
    "p99_latency_ms": "float (optional)",
    "throughput_rps": "float (optional)"
  },
  "artifacts": {
    "detailed_results_file": "string (optional)",
    "methodology_url": "string (optional)",
    "source_code_url": "string (optional)"
  }
}
```

---

## Field Definitions

### `schema_version` (required)
- **Type**: String
- **Format**: Semantic versioning (e.g., "1.0.0")
- **Description**: Version of this results schema
- **Current**: "1.0.0"

### `tool` (required)

#### `tool.name` (required)
- **Type**: String
- **Description**: Name of the guardrail/tool being evaluated
- **Example**: "PromptGuard Pro", "OpenAI Moderation", "Custom Classifier"

#### `tool.version` (required)
- **Type**: String
- **Description**: Version of the tool
- **Example**: "2.1.0", "v1.5", "2024-01-15"

#### `tool.organization` (optional)
- **Type**: String
- **Description**: Organization that created/maintains the tool
- **Example**: "Acme Security", "OpenAI", "Community"

#### `tool.website` (optional)
- **Type**: String
- **Format**: URL
- **Description**: Website or documentation URL
- **Example**: "https://example.com/product"

#### `tool.description` (optional)
- **Type**: String
- **Description**: Brief description of the tool
- **Max Length**: 500 characters

### `run` (required)

#### `run.test_date` (required)
- **Type**: String
- **Format**: ISO 8601 datetime
- **Description**: When the test was conducted
- **Example**: "2026-01-16T14:30:00Z", "2026-01-16T09:30:00-05:00"

#### `run.benchmark_version` (required)
- **Type**: String
- **Description**: Version of PIDB used
- **Must Be**: "1.0.0" for current benchmark

#### `run.total_test_cases` (required)
- **Type**: Integer
- **Description**: Total number of test cases evaluated
- **Must Be**: 643 for v1.0.0

#### `run.evaluator_version` (optional)
- **Type**: String
- **Description**: Version of evaluation script used
- **Example**: "1.0.0"

#### `run.notes` (optional)
- **Type**: String
- **Description**: Any notes about the test run
- **Example**: "Using default temperature 0.7"

### `overall` (required)

#### `overall.accuracy` (required)
- **Type**: Float
- **Range**: 0.0 to 100.0
- **Description**: Overall accuracy percentage
- **Calculation**: `(passed / total_test_cases) * 100`
- **Example**: 91.5

#### `overall.passed` (required)
- **Type**: Integer
- **Description**: Number of test cases where decision matched expected
- **Range**: 0 to 643

#### `overall.failed` (required)
- **Type**: Integer
- **Description**: Number of test cases where decision did not match expected
- **Validation**: `passed + failed = 643`

### `error_breakdown` (required)

#### `error_breakdown.false_negatives` (required)
- **Type**: Integer
- **Description**: Attacks incorrectly allowed (should BLOCK, said ALLOW)
- **Critical**: These represent missed attacks

#### `error_breakdown.false_positives` (required)
- **Type**: Integer
- **Description**: Benign prompts incorrectly blocked (should ALLOW, said BLOCK)
- **Critical**: These represent over-defense

#### `error_breakdown.false_negative_rate` (required)
- **Type**: Float
- **Range**: 0.0 to 100.0
- **Calculation**: `(false_negatives / total_attacks) * 100`
- **Description**: Percentage of attacks missed

#### `error_breakdown.false_positive_rate` (required)
- **Type**: Float
- **Range**: 0.0 to 100.0
- **Calculation**: `(false_positives / total_benign) * 100`
- **Description**: Percentage of benign prompts blocked

#### `error_breakdown.runtime_errors` (optional)
- **Type**: Integer
- **Default**: 0
- **Description**: Number of test cases that caused runtime errors
- **Note**: Should be 0 for valid submissions

### `by_category` (required)

Map of category names to performance metrics. Must be non-empty and category totals must sum to 643.

**Structure** (per category):
```json
{
  "accuracy": 95.5,
  "correct": 325,
  "total": 339,
  "false_negatives": 10,
  "false_positives": 4
}
```

**Requirements:**
- Dictionary must not be empty
- Category totals must sum to 643
- Each category must have accuracy, correct, and total fields

**Recommended Approach:**
Report using either:
- **Fine-grained categories** (76 total) - from test_cases.json
- **Rollup categories** (12 total) - from docs/category-rollups.md
- **Both** - for comprehensive analysis

**Note:** The evaluator script outputs fine-grained categories by default. Rollup categories can be computed by grouping fine-grained categories according to docs/category-rollups.md.

### `by_severity` (required for attacks)

Performance broken down by attack severity. Only applicable to attack cases.

**Required Severity Levels**:
- `critical` - Highest severity attacks
- `high` - High severity attacks
- `medium` - Medium severity attacks
- `low` - Low severity attacks
- `null` - Benign cases (no severity)

**Structure** (per severity):
```json
{
  "accuracy": 98.5,
  "correct": 63,
  "total": 64
}
```

### `performance` (optional but recommended)

#### `performance.avg_latency_ms` (optional)
- **Type**: Float
- **Description**: Average latency in milliseconds
- **Example**: 610.5

#### `performance.median_latency_ms` (optional)
- **Type**: Float
- **Description**: Median latency in milliseconds

#### `performance.p95_latency_ms` (optional)
- **Type**: Float
- **Description**: 95th percentile latency

#### `performance.p99_latency_ms` (optional)
- **Type**: Float
- **Description**: 99th percentile latency

#### `performance.throughput_rps` (optional)
- **Type**: Float
- **Description**: Requests per second
- **Example**: 1.39

### `artifacts` (optional)

#### `artifacts.detailed_results_file` (optional)
- **Type**: String
- **Description**: Path to detailed per-test results
- **Example**: "pidb_results_detailed.json"

#### `artifacts.methodology_url` (optional)
- **Type**: String
- **Format**: URL
- **Description**: Link to detailed methodology
- **Example**: "https://example.com/pidb-methodology.md"

#### `artifacts.source_code_url` (optional)
- **Type**: String
- **Format**: URL
- **Description**: Link to evaluation code/setup
- **Example**: "https://github.com/org/pidb-eval"

---

## Validation Rules

### Required Checks

1. **Schema Version**: Must be "1.0.0"
2. **Benchmark Version**: Must be "1.0.0"
3. **Total Cases**: Must be 643
4. **Math Consistency**:
   - `passed + failed = 643`
   - `false_negatives + false_positives ≤ failed`
   - Category totals sum to 643
   - Severity totals sum to expected distribution

### Accuracy Calculations

```python
# Overall accuracy
accuracy = (passed / 643) * 100

# False negative rate (of attacks only)
total_attacks = 279  # in v1.0
fn_rate = (false_negatives / total_attacks) * 100

# False positive rate (of benign only)
total_benign = 364  # in v1.0
fp_rate = (false_positives / total_benign) * 100
```

### Category Requirements

Must report at least:
- `overdefense` (or equivalent benign category)
- `attack` (or break down into specific attack types)

Recommended to report all major rollup categories:
- overdefense, multilingual, advanced_encoding, rag_poisoning,
  tool_calling, context_window, extraction_methods, jailbreak,
  classic_attack, social_engineering, code_injection, other

---

## Example: Complete Results File

```json
{
  "schema_version": "1.0.0",
  "tool": {
    "name": "PromptGuard Pro",
    "version": "2.1.0",
    "organization": "Acme Security",
    "website": "https://acme.example.com/promptguard",
    "description": "LLM-based prompt injection detection system"
  },
  "run": {
    "test_date": "2026-01-16T14:30:00Z",
    "benchmark_version": "1.0.0",
    "total_test_cases": 643,
    "evaluator_version": "1.0.0",
    "notes": "Evaluated with temperature=0.7, max_tokens=100"
  },
  "overall": {
    "accuracy": 91.0,
    "passed": 585,
    "failed": 58
  },
  "error_breakdown": {
    "false_negatives": 45,
    "false_positives": 13,
    "false_negative_rate": 16.1,
    "false_positive_rate": 3.6,
    "runtime_errors": 0
  },
  "by_category": {
    "overdefense": {
      "accuracy": 96.4,
      "correct": 349,
      "total": 362,
      "false_negatives": 0,
      "false_positives": 13
    },
    "rag_poisoning": {
      "accuracy": 81.5,
      "correct": 22,
      "total": 27,
      "false_negatives": 5,
      "false_positives": 0
    },
    "tool_calling": {
      "accuracy": 88.5,
      "correct": 23,
      "total": 26,
      "false_negatives": 3,
      "false_positives": 0
    },
    "jailbreak": {
      "accuracy": 94.7,
      "correct": 18,
      "total": 19,
      "false_negatives": 1,
      "false_positives": 0
    },
    "classic_attack": {
      "accuracy": 100.0,
      "correct": 18,
      "total": 18,
      "false_negatives": 0,
      "false_positives": 0
    }
  },
  "by_severity": {
    "critical": {
      "accuracy": 98.4,
      "correct": 63,
      "total": 64
    },
    "high": {
      "accuracy": 94.1,
      "correct": 96,
      "total": 102
    },
    "medium": {
      "accuracy": 88.7,
      "correct": 79,
      "total": 89
    },
    "low": {
      "accuracy": 83.3,
      "correct": 20,
      "total": 24
    },
    "null": {
      "accuracy": 96.4,
      "correct": 327,
      "total": 364
    }
  },
  "performance": {
    "avg_latency_ms": 610.5,
    "median_latency_ms": 580.0,
    "p95_latency_ms": 850.0,
    "p99_latency_ms": 1200.0,
    "throughput_rps": 1.39
  },
  "artifacts": {
    "detailed_results_file": "pidb_results_detailed.json",
    "methodology_url": "https://acme.example.com/pidb-methodology",
    "source_code_url": "https://github.com/acme/pidb-evaluation"
  }
}
```

---

## Detailed Results Format (Optional)

If providing `pidb_results_detailed.json`, use this format:

```json
{
  "schema_version": "1.0.0",
  "test_results": [
    {
      "test_id": "ATTACK-001",
      "expected": "BLOCK",
      "actual": "BLOCK",
      "passed": true,
      "latency_ms": 615.3,
      "category": "direct_attack",
      "severity": "high",
      "error": null
    },
    {
      "test_id": "BENIGN-001",
      "expected": "ALLOW",
      "actual": "ALLOW",
      "passed": true,
      "latency_ms": 580.1,
      "category": "overdefense_test",
      "severity": null,
      "error": null
    }
  ]
}
```

---

## Submission Process

1. **Generate results** using `scripts/evaluate.py` (outputs this schema)
2. **Validate results** using `scripts/validate_submission.py`
3. **Create PR** with results file in `leaderboard/results/your-tool-name.json`
4. **Include artifacts** (optional detailed results, methodology)

See [leaderboard/README.md](../leaderboard/README.md) for complete submission guidelines.

---

## Version History

### v1.0.0 (2026-01-16)
- Initial schema definition
- 643 test cases (PIDB v1.0.0)
- Required fields: tool, run, overall, error_breakdown, by_category, by_severity
- Optional fields: performance, artifacts

---

## Questions?

For questions about this schema or submission process:
- Open an issue on GitHub
- Email: contact@directivecommons.org
- See: [CONTRIBUTING.md](../CONTRIBUTING.md)
