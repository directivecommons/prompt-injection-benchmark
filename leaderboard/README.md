# PIDB Leaderboard

Public rankings of prompt injection detection systems tested on PIDB benchmark.

---

## Current Rankings

*Last updated: 2026-01-15*

| Rank | Tool | Version | Overall | FN Rate | FP Rate | Avg Latency | Date Tested |
|------|------|---------|---------|---------|---------|-------------|-------------|
| 🥇 | *Be the first!* | - | - | - | - | - | - |

---

## How to Submit

Want to add your tool to the leaderboard? Follow these steps:

### 1. Run the Benchmark

```bash
# Clone repository
git clone https://github.com/directive-commons/prompt-injection-benchmark
cd prompt-injection-benchmark

# Run evaluation with schema-compliant output
python scripts/evaluate.py \
    --guardrail-module your_module \
    --guardrail-function your_function \
    --tool-name "YourTool" \
    --tool-version "2.1.0" \
    --organization "Your Organization" \
    --website "https://yourtool.com" \
    --output pidb_results.json
```

### 2. Validate Results

```bash
# Validate submission before creating PR
python scripts/validate_submission.py pidb_results.json
```

Validation checks:
- Schema compliance (v1.0.0)
- Benchmark version (v1.0.0)
- Total test cases (643)
- Math consistency
- Required fields

### 3. Create Submission File

**Results must conform to [PIDB Results Schema v1.0](../docs/results-schema.md).**

The `evaluate.py` script automatically generates schema-compliant output.

**Required format:**

```json
{
  "schema_version": "1.0.0",
  "tool": {
    "name": "YourTool",
    "version": "2.1.0",
    "organization": "Your Organization",
    "website": "https://yourtool.com"
  },
  "run": {
    "test_date": "2026-01-16T14:30:00Z",
    "benchmark_version": "1.0.0",
    "total_test_cases": 643,
    "evaluator_version": "1.0.0"
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
    "overdefense": {"accuracy": 96.4, "correct": 349, "total": 362},
    "rag_poisoning": {"accuracy": 81.5, "correct": 22, "total": 27}
  },
  "by_severity": {
    "critical": {"accuracy": 98.4, "correct": 63, "total": 64},
    "high": {"accuracy": 94.1, "correct": 96, "total": 102}
  },
  "performance": {
    "avg_latency_ms": 610.5,
    "throughput_rps": 1.39
  }
}
```

See [docs/results-schema.md](../docs/results-schema.md) for complete schema documentation.

### 4. Submit Pull Request

```bash
# Fork repository on GitHub
# Create branch
git checkout -b add-yourtool-results

# Add your results file
git add leaderboard/results/your-tool-name.json

# Commit
git commit -m "Add YourTool results to leaderboard"

# Push and create PR
git push origin add-yourtool-results
```

### 4. Review Process

- Maintainers will review for completeness
- Verify format and methodology documentation
- Spot-check for obvious errors
- Typically approved within 3-5 business days

---

## Submission Requirements

✅ **Required:**
- Complete benchmark (all 643 test cases)
- Documented methodology (public URL)
- Accurate results (no inflation)
- Valid contact information

⚠️ **Recommended:**
- Reproducible setup (scripts, Docker, etc.)
- Performance metrics included
- Test environment details
- Open source methodology

❌ **Not Accepted:**
- Partial benchmark results
- Undocumented methodology
- Obviously inflated numbers
- Anonymous submissions

---

## Verification

### How We Verify Results

**Automated checks:**
- JSON format validation
- Completeness verification
- Math consistency checks

**Manual review:**
- Methodology documentation review
- Spot-check sample results
- Community feedback consideration

**Optional independent verification:**
- Random sampling of results
- Community reproduction attempts
- Third-party audits (for high-profile tools)

### Challenge Process

Think results are suspicious? Anyone can challenge:

1. Open GitHub issue with specific concerns
2. Provide evidence or analysis
3. Maintainers investigate
4. Results may be removed if invalid

---

## Categories of Tools

### Open Source
Tools with publicly available code

### Commercial
Proprietary tools requiring license/subscription

### Research
Academic or research prototypes

### Self-Hosted
Tools that can be deployed locally

### API-Based
Cloud-hosted services accessed via API

---

## Metrics Explained

### Overall Accuracy
Percentage of test cases correctly classified (BLOCK vs ALLOW)

**What's good:**
- 95%+: Excellent
- 90-95%: Good
- 85-90%: Fair
- <85%: Needs improvement

### False Negative Rate
Percentage of attacks that were missed (not blocked)

**What's good:**
- <5%: Excellent
- 5-10%: Acceptable
- >10%: Concerning

### False Positive Rate
Percentage of benign prompts incorrectly blocked

**What's good:**
- <2%: Excellent
- 2-5%: Acceptable
- >5%: Too restrictive

### Average Latency
Mean time to evaluate a prompt

**What's good:**
- <100ms: Excellent
- 100-500ms: Good
- 500-1000ms: Acceptable
- >1000ms: Slow

---

## Comparison Guidelines

### Fair Comparisons

✅ **Compare tools with:**
- Similar deployment models (self-hosted vs API)
- Similar accuracy tiers (95% vs 96% is meaningful)
- Same benchmark version
- Documented methodologies

❌ **Don't compare:**
- Different benchmark versions
- Wildly different latencies without context
- Without understanding methodology differences
- Based on marketing claims vs actual results

### Understanding Trade-offs

**High accuracy, high latency:**
- Thorough checking, multiple layers
- Better for high-risk applications
- May impact user experience

**Good accuracy, low latency:**
- Balanced approach
- Suitable for production use
- Fast user experience

**Variable accuracy by category:**
- Some tools excel at specific attack types
- Consider your threat model
- Match tool strengths to your needs

---

## Historical Results

As tools are updated, we maintain historical results:

- `leaderboard/results/your-tool-v1.0.json`
- `leaderboard/results/your-tool-v2.0.json`

This allows tracking improvement over time.

---

## Questions?

- **Submission help:** Open [GitHub issue](https://github.com/directive-commons/prompt-injection-benchmark/issues)
- **Methodology questions:** See [docs/methodology.md](../docs/methodology.md)
- **Challenge results:** Email conduct@directivecommons.org
- **General inquiries:** contact@directivecommons.org

---

## Updates

**2026-01-15:** Leaderboard launched with PIDB v1.0

*Check back regularly for new submissions!*
