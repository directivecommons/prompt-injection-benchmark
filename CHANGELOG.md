# Changelog

All notable changes to PIDB will be documented in this file.

## [1.0.0] - 2026-01-16

### Added
- 643 test cases (279 attacks, 364 benign)
- 253 original cases covering RAG, tool calling, context window, code injection
- 339 NotInject cases (over-defense testing)
- 51 Garak cases (classic attacks)
- Results Schema v1.0 (standardized format)
- Evaluation script (`scripts/evaluate.py`) with schema-compliant output
- Validation tool (`scripts/validate_submission.py`) for submissions
- Public leaderboard process
- 12 languages, 76 fine-grained categories, 12 rollup categories
- Example guardrail (`examples/simple_guardrail.py`)
- **pip installable** via `pip install -e .` (no more PYTHONPATH required)
- **Rollup category reporting** in evaluator output (`by_rollup` field)

### Fixed
- **Windows compatibility**: Fixed UnicodeEncodeError when using evaluator on Windows (emoji handling)
- Added UTF-8 stdout configuration for cross-platform compatibility
- Safe print function with ASCII fallback for terminals without emoji support

### Features
- Production-ready evaluation infrastructure
- Automated validation
- Standardized results format (JSON schema v1.0.0)
- Over-defense testing (56.6% benign cases)
- Vendor-neutral, community-owned governance
- Fail-mode options: block, allow, error
- Performance metrics: latency, throughput, percentiles
- Detailed per-test results output
- Both fine-grained (76) and rollup (12) category reporting

### Documentation
- Complete methodology documentation
- Category rollup mappings (76 → 12 groupings)
- Getting started guide
- Results schema specification
- Contribution guidelines
- Transparent governance model
- `pyproject.toml` for standard Python packaging

### Known Limitations
- Single-turn only (multi-turn attacks approximated; v1.1 planned)
- English-primary: 94% English (working to expand)
- Binary ALLOW/BLOCK classification
- Static dataset (643 fixed cases)

### Technical Notes
- Requires `PYTHONPATH` to be set for Python imports
- Percentile calculation uses nearest-rank method
- Guardrail function contract: `fn(prompt: str) -> bool` (True = block)

---

## [Unreleased]

### Planned for v1.1 (Q2 2026)
- Multi-turn attack sequences
- Expanded non-English coverage (target 30%+ non-English)
- HTTP/gRPC evaluation mode for non-Python guardrails
- CLI adapter mode
- Shadow evaluation set validation
- Additional test cases (target 800+)
- Rich return contract support (confidence, rationale)

### Under Consideration
- Confidence score evaluation
- Explanation quality assessment
- Cost/latency tradeoff analysis
- Dynamic test generation integration
- Multi-modal attacks (image-based injection)
