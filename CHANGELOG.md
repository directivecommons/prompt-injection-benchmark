# Changelog

All notable changes to PIDB will be documented in this file.

## [1.0.0] - 2026-01-16

### Added
- 643 test cases (279 attacks, 364 benign)
- 253 original cases covering RAG, tool calling, modern attacks
- 339 NotInject cases (over-defense testing)
- 51 Garak cases (classic attacks)
- Results Schema v1.0 (standardized format)
- Evaluation script with schema-compliant output
- Validation tool for submissions
- Public leaderboard process
- 12 languages, 76 fine-grained categories

### Features
- Production-ready evaluation infrastructure
- Automated validation (validate_submission.py)
- Standardized results format
- Over-defense testing (56% benign cases)
- Vendor-neutral, community-owned

### Documentation
- Complete methodology documentation
- Category rollup mappings
- Getting started guide
- Results schema specification
- Contribution guidelines

### Known Limitations
- Single-turn only (multi-turn planned for v1.1)
- 94% English (working to expand)
- Binary ALLOW/BLOCK classification
- Static dataset (643 fixed cases)

---

## [Unreleased]

### Planned for v1.1 (Q2 2026)
- Multi-turn attack sequences
- Expanded non-English coverage
- Additional test cases
- Shadow set validation
