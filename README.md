# Prompt Injection Detection Benchmark (PIDB)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/directive-commons/prompt-injection-benchmark/releases)
[![Test Cases](https://img.shields.io/badge/test_cases-643-green.svg)](benchmark/v1.0/)

*A project by [Directive Commons](https://directivecommons.org)*

---

## The Problem

The prompt injection detection industry lacks a standard benchmark. Vendors claim 85-95% accuracy on undisclosed, incomparable datasets. This makes evaluation impossible for buyers and researchers.

**The result:** No way to compare tools. No transparency. No accountability.

## The Solution

PIDB is a production-ready, vendor-neutral benchmark for evaluating prompt injection detection systems.

Built on prior work (NotInject, Garak) with added coverage for RAG, tool calling, and modern attack vectors.

### What Makes PIDB Different

✅ **Production-Ready** - Complete tooling: evaluator, validator, schema  
✅ **Realistic** - Tests both attacks AND over-defense (false positives)  
✅ **Transparent** - Open source, reproducible methodology  
✅ **Vendor Neutral** - Community-owned, no commercial conflicts  
✅ **Accessible** - Easy to use, standardized format  

---

## Purpose and Scope

This benchmark evaluates **prompt-injection robustness and over-defense behavior** in LLM-based systems under a defined set of realistic attack and non-attack scenarios.

**It is intentionally scoped to:**
- Prompt-based attacks and manipulations
- Indirect and contextual injection vectors (RAG, tool calling, context window)
- False positives arising from roleplay, education, translation, and benign discussion

**This benchmark does not claim to measure:**
- Overall AI safety or model alignment
- Security guarantees beyond the tested prompt-interaction surface
- Production readiness or immunity to novel attacks

---

## Interpreting Results

Benchmark results reflect performance **only with respect to the included test cases and evaluation criteria.**

✅ **A high score indicates:** Stronger handling of the specific prompt-injection and over-defense scenarios represented in this benchmark.

⚠️ **Benchmark results should NOT be interpreted as:**
- Proof of general prompt-injection safety
- Production readiness certification
- Immunity to novel or adversarial attacks
- Security guarantees beyond tested scenarios

**Use benchmark results as diagnostic data, not as definitive security claims.**

---

## Evaluation Philosophy

**Prompt-injection defense is a trade-off** between blocking malicious behavior and preserving legitimate, benign use cases.

This benchmark treats **false positives and false negatives as first-class failure modes**, and evaluates systems accordingly.

We measure both:
- **Attack detection accuracy** (avoiding false negatives)
- **Over-defense prevention** (avoiding false positives)

---

## What's New in v1.0

**Enhanced Coverage (643 total test cases):**
- ✅ **RAG/Indirect Injection** (25 cases) - Document poisoning, context manipulation
- ✅ **Tool Calling/Agent Attacks** (20 cases) - Function injection, parameter manipulation
- ✅ **Context Window Attacks** (15 cases) - Position exploitation, context dilution
- ✅ **More Jailbreaks** (+15 cases) - Latest 2024-2025 techniques
- ✅ **More Classic Attacks** (+15 cases) - Additional instruction override patterns
- ✅ **Code Injection** (10 cases) - Script execution, command injection
- ✅ **More Extraction Methods** (10 cases) - System prompt extraction techniques
- ✅ **More Non-English** (+10 cases) - 12 languages total

**Note on Multi-Turn Attacks:**
Multi-turn conversational attacks (progressive jailbreaking, context building) are planned for v1.1 (Q2 2026). These require special evaluation infrastructure beyond single-prompt testing. We welcome community contributions and feedback on multi-turn attack patterns.

---

## Test Suite Composition

| Category | Count | Description |
|----------|-------|-------------|
| **Over-Defense Tests** | 363 | Benign prompts to prevent false positives (primary test set) |
| **Other Attack Types** | 57 | Additional attack vectors and edge cases |
| **Multilingual** | 38 | Cross-language attack patterns |
| **Jailbreaks** | 30 | DAN, roleplay, constraint removal attempts |
| **RAG/Indirect Injection** | 30 | Document poisoning, retrieved context attacks |
| **Advanced Encoding** | 30 | Base64, HTML entities, Unicode manipulation |
| **Classic Attacks** | 28 | "Ignore instructions" and variants |
| **Tool Calling** | 21 | Agent/function calling exploitation |
| **Context Window** | 18 | Position exploitation, context dilution |
| **Social Engineering** | 11 | Manipulation-based attacks |
| **Extraction Methods** | 9 | System prompt extraction techniques |
| **Code Injection** | 8 | Script execution, command injection |
| **TOTAL** | **643** | **Production-ready standard** |

*Note: "Over-Defense Tests" (363) is the primary benign test set. Total benign cases: 364 (includes 1 benign case in "Other" category). Counts reflect rollup groupings - see [docs/category-rollups.md](docs/category-rollups.md) for exact mappings from 76 fine-grained categories to 12 rollups.*

---

## Known Limitations

**PIDB v1.0 focuses on practical, production-ready testing. It has intentional scope limits:**

1. **Single-turn only**: Multi-turn attacks are approximated as single prompts. Real adversarial conversations aren't captured. (Planned for v1.1)

2. **English-primary**: 603/643 cases (94%) are English. Other languages have token coverage (5-6 cases each).

3. **Modest scale**: 643 cases is respectable but not massive. Academic papers often use 1000+ cases.

4. **Binary classification**: ALLOW/BLOCK only. No confidence scores, explanations, or cost analysis.

5. **Static dataset**: Cases don't adapt. Adversaries can learn the benchmark. (Shadow set mitigates but doesn't eliminate this)

**These are documented constraints, not bugs.** We prioritized accessibility and production-readiness over research novelty.

---

**Level 1: Basic Keyword Attacks** (~150 cases)  
Simple patterns like "ignore previous instructions"  
*Detection: Keyword matching*

**Level 2: Encoded/Obfuscated** (~40 cases)  
Base64, HTML entities, Unicode manipulation  
*Detection: Normalization + patterns*

**Level 3: Semantic/Cultural** (~40 cases)  
Multilingual, cultural metaphors, indirect extraction  
*Detection: Semantic understanding*

**Level 4: Advanced Social Engineering** (~30 cases)  
Zero keywords, appear completely legitimate  
*Detection: Deep intent analysis*

**Level 5: LLM-Classifier-Specific** (~20 cases)  
Adversarial suffixes, few-shot poisoning, position exploitation  
*Detection: LLM-hardened classifiers*

### Decision Distribution

- **ALLOW**: 364 cases (56.6%) - Testing false positive prevention
- **BLOCK**: 279 cases (43.4%) - Testing attack detection

---

## Test Case Sources

PIDB builds on excellent prior work:

**NotInject Dataset** (339 cases, 52.7%)
- License: CC-BY-4.0
- Academic research on over-defense and false positives
- Provides core benign test set

**Garak Framework** (51 cases, 7.9%)
- License: Apache-2.0
- Open-source LLM red-teaming tool by Leon Derczynski
- Classic prompt injection and jailbreak patterns

**Original PIDB** (253 cases, 39.3%)
- License: MIT
- New attacks: RAG poisoning, tool calling, context window, code injection
- Additional multilingual and advanced encoding cases

**Full attribution details:** See [ATTRIBUTIONS.md](ATTRIBUTIONS.md)

---

## Quick Start

### 1. Download Test Suite

```bash
git clone https://github.com/directive-commons/prompt-injection-benchmark
cd prompt-injection-benchmark
```

### 2. Run Your Guardrail

```python
import json

# Load test suite
with open('benchmark/v1.0/test_cases.json') as f:
    data = json.load(f)
    test_cases = data['test_cases']

# Evaluate your guardrail
correct = 0
results = []

for test in test_cases:
    # Your guardrail evaluation
    result = your_guardrail.evaluate(test['prompt'])
    
    # Expected decision
    expected = test['expected_final']['decision']
    
    # Map your result to ALLOW/BLOCK
    actual = 'BLOCK' if result.should_block else 'ALLOW'
    
    # Check if correct
    passed = (expected == actual)
    if passed:
        correct += 1
    
    results.append({
        'test_id': test['id'],
        'expected': expected,
        'actual': actual,
        'passed': passed
    })

# Calculate accuracy
accuracy = (correct / len(test_cases)) * 100

print(f"Overall Accuracy: {accuracy:.1f}%")
print(f"Passed: {correct}/{len(test_cases)} test cases")
```

### 3. Use Automated Evaluation (Recommended)

For schema-compliant results with validation:

```bash
# Install in your project or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run evaluation
python scripts/evaluate.py \
    --guardrail-module your_module \
    --guardrail-function your_function \
    --tool-name "YourTool" \
    --tool-version "1.0.0" \
    --output results.json

# Validate results
python scripts/validate_submission.py results.json
```

See [docs/getting-started.md](docs/getting-started.md) for detailed usage.

### 4. Submit Results to Leaderboard

See [Contributing to Leaderboard](#contributing-to-leaderboard)

---

## Current Leaderboard

### Vendor / Commercial Solutions

| Rank | Tool | Version | Overall Accuracy | False Neg Rate | False Pos Rate | Date | Methodology |
|------|------|---------|------------------|----------------|----------------|------|-------------|
| - | *Awaiting submissions* | - | - | - | - | - | - |

### Open Source / Research Solutions

| Rank | Tool | Version | Overall Accuracy | False Neg Rate | False Pos Rate | Date | Methodology |
|------|------|---------|------------------|----------------|----------------|------|-------------|
| - | *Awaiting submissions* | - | - | - | - | - | - |

**Want to be listed?** See [Contributing to Leaderboard](#contributing-to-leaderboard) or submit results at [leaderboard/README.md](leaderboard/README.md)

---

## Preventing Benchmark Overfitting

To discourage prompt-specific defenses and hard-coded pattern matching, **maintainers may evaluate systems against a private shadow evaluation set** drawn from the same category distribution as the public benchmark.

**Purpose:** The shadow set exists solely to assess whether reported performance on the public benchmark is representative of broader behavior within the defined scope.

**Usage:** Shadow-set results are not used to rank systems publicly, nor are they presented as pass/fail certification outcomes.

**Transparency:** All publicly reported scores must remain reproducible using the released benchmark data and evaluation tooling.

---

## Transparency and Reproducibility

All publicly reported scores must be **reproducible** using the released benchmark data and evaluation tooling.

The benchmark prioritizes transparency of:
- Test case structure
- Expected outcomes
- Evaluation methodology

Non-public evaluation artifacts, where used, exist only to validate generalization and are not substitutes for the public benchmark.

---

## Contributing to Leaderboard

We welcome all guardrail vendors and researchers to test on PIDB!

### Requirements

1. Run complete test suite (all 643 cases)
2. Document your methodology
3. Provide reproducible setup
4. Submit via Pull Request

### Submission Format

Create a file `leaderboard/results/your-tool-name.json`:

```json
{
  "tool_name": "YourTool",
  "version": "1.0.0",
  "organization": "Your Organization",
  "test_date": "2026-01-15",
  "benchmark_version": "1.0.0",
  "results": {
    "overall_accuracy": 91.0,
    "total_test_cases": 643,
    "passed": 585,
    "failed": 58,
    "false_negatives": 45,
    "false_positives": 13,
    "false_negative_rate": 16.1,
    "false_positive_rate": 3.6
  },
  "by_category": {
    "rag_poisoning": {"accuracy": 88.0, "count": 25},
    "tool_calling": {"accuracy": 85.0, "count": 20},
    "jailbreak": {"accuracy": 90.0, "count": 19},
    "overdefense_test": {"accuracy": 96.0, "count": 339}
  },
  "performance": {
    "avg_latency_ms": 610,
    "throughput_rps": 1.39
  },
  "methodology": "https://link-to-your-test-setup.md",
  "contact": "email@yourorg.com"
}
```

Then submit PR to this repository.

---

## Non-Certification Notice

⚠️ **This benchmark is not a certification, compliance framework, or security guarantee.**

Use of this benchmark does not imply endorsement, approval, or security validation of any system by the benchmark maintainers.

---

## Responsible Use

This benchmark is intended for **defensive evaluation and research purposes.**

Test cases reflect commonly known or previously disclosed prompt-injection techniques and are included to support detection, mitigation, and analysis—not to enable misuse.

---

## Detailed Documentation

📖 **[Getting Started Guide](docs/getting-started.md)** - Complete walkthrough  
📋 **[Methodology](docs/methodology.md)** - How tests were created  
🔧 **[Schema Documentation](docs/schema.md)** - Test case format specification  
🏆 **[Leaderboard Details](leaderboard/README.md)** - Submission guidelines and full results  

---

## Contributing Test Cases

We welcome contributions of new test cases! See [CONTRIBUTING.md](CONTRIBUTING.md)

### What We're Looking For

✅ **Novel attack patterns** not already covered  
✅ **Real-world attacks** from production systems  
✅ **Edge cases** that are hard to classify  
✅ **Over-defense cases** that guardrails incorrectly block  

### What We Don't Accept

❌ Duplicates of existing test cases  
❌ Test cases targeting specific vendor weaknesses  
❌ Unrealistic or contrived examples  
❌ Test cases without clear expected behavior  

---

## Governance

PIDB is community-owned and vendor-neutral.

**Principles:**
- No single vendor controls the benchmark
- All decisions are transparent and public
- Community consensus for major changes
- Open contribution process

See [GOVERNANCE.md](GOVERNANCE.md) for details.

### Maintainers

- Directive Commons (founding maintainer)
- *Seeking co-maintainers from academia and independent researchers*

Want to become a maintainer? See [GOVERNANCE.md](GOVERNANCE.md)

---

## Use Cases

### For Guardrail Vendors
- Validate your detection accuracy
- Identify weaknesses in your system
- Compare against competitors
- Build customer trust through transparency

### For Enterprise Buyers
- Compare guardrail products objectively
- Validate vendor claims
- Make informed procurement decisions
- Benchmark internal solutions

### For Security Researchers
- Discover new attack patterns
- Publish comparative analyses
- Contribute to industry standards
- Advance the field

### For Developers
- Test your own implementations
- Learn about attack patterns
- Integrate into CI/CD pipelines
- Prevent regressions

---

## Citation

If you use PIDB in your research or product, please cite:

```bibtex
@misc{pidb2026,
  title={Prompt Injection Detection Benchmark (PIDB)},
  author={Directive Commons},
  year={2026},
  publisher={GitHub},
  howpublished={\url{https://github.com/directive-commons/prompt-injection-benchmark}},
  note={Version 1.0.0}
}
```

---

## Roadmap

### Version 1.0 (Current) ✅
- 643 comprehensive test cases
- Multiple sophistication levels
- Over-defense testing
- Public leaderboard infrastructure

### Version 1.1 (Q2 2026)
- Multi-turn conversational attacks
- Additional 100+ community-contributed cases
- Enhanced RAG and tool calling coverage
- Shadow evaluation set validation

### Version 2.0 (Q4 2026)
- 1000+ test cases
- Multi-modal attacks (image-based injection)
- Automated red-teaming integration
- Industry working group formation

---

## Community

- **GitHub Discussions**: Ask questions, share insights
- **Twitter**: [@directivecommon](https://twitter.com/directivecommon)
- **Website**: [directivecommons.org](https://directivecommons.org)
- **Email**: contact@directivecommons.org

---

## License

This benchmark is released under the [MIT License](LICENSE).

You are free to:
- Use commercially
- Modify and redistribute
- Use in research and publications

We only ask that you:
- Cite PIDB if used in research
- Link back to this repository
- Consider contributing improvements

See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for third-party attribution details.

---

## Acknowledgments

PIDB builds upon research and testing from:
- Academic security research community
- Open source security projects (Garak, HarmBench, etc.)
- Real-world attack patterns shared by practitioners
- Community contributors

See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for detailed attribution.

---

## About Directive Commons

Directive Commons is an independent research initiative focused on AI safety, governance, and security standards. We create open, vendor-neutral benchmarks and tools to improve the safety and reliability of AI systems.

**Mission:** To create transparent, community-driven standards that make AI systems safer for everyone.

Learn more: [directivecommons.org](https://directivecommons.org)

---

**Star this repository** if you find it useful! ⭐

**Questions?** Open an issue or start a discussion.

**Want to contribute?** See [CONTRIBUTING.md](CONTRIBUTING.md)
