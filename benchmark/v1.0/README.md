# PIDB v1.0 Test Suite

This directory contains the official PIDB v1.0 benchmark test suite.

## Files

- `test_cases.json` - Complete test suite (643 cases)
- `metadata.json` - Statistics and distribution information
- `README.md` - This file

## Test Suite Structure

The `test_cases.json` file contains:
- Benchmark metadata (version, description, license)
- Array of 643 test cases

Each test case includes:
- `id`: Unique identifier
- `category`: Attack or defense category
- `prompt`: The actual test prompt
- `language`: Language code (mostly 'en')
- `expected_final`: Expected decision (ALLOW/BLOCK)
- `severity`: Attack severity (if applicable)
- `technique`: Attack technique description (if applicable)
- `source`: Origin of test case

## Usage

```python
import json

with open('test_cases.json', 'r') as f:
    data = json.load(f)
    test_cases = data['test_cases']

for test in test_cases:
    prompt = test['prompt']
    expected = test['expected_final']['decision']
    # Evaluate your guardrail here
```

## Statistics

- **Total Cases**: 643
- **Attack Cases**: 279 (43.4%)
- **Benign Cases**: 364 (56.6%)
- **Languages**: 12 (English, Spanish, Chinese, Japanese, Arabic, Russian, French, German, Korean, Portuguese, Dutch, Mixed)
- **Categories**: 76 fine-grained categories (12 rollup categories)

See `metadata.json` for complete breakdown.

## Version History

**v1.0.0** (2026-01-15)
- Initial release
- 643 test cases
- 5 sophistication levels
- Multi-language support
- Comprehensive over-defense testing
