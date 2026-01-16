# Third-Party Attributions

This benchmark includes test cases derived from the following third-party sources. We gratefully acknowledge these contributions to the AI security community.

---

## Garak Framework

**Test Cases**: 51 test cases (9.8%)

**License**: Apache License 2.0

**Original Work**: Garak - LLM vulnerability scanner  
**Authors**: Leon Derczynski et al.  
**URL**: https://github.com/leondz/garak  
**License URL**: https://github.com/leondz/garak/blob/main/LICENSE  

**Description**: Garak is an open-source LLM red-teaming and vulnerability scanning framework. These test cases are inspired by attack patterns and examples from Garak, adapted and modified for use in PIDB.

**Categories Included**:
- Jailbreak attempts
- Social engineering
- Secret extraction
- Roleplay-based attacks
- Instruction override
- Delimiter attacks
- Encoding attacks
- Hypothetical scenarios
- Context manipulation

**Attribution Text**: "Based on Garak by Leon Derczynski et al. (https://github.com/leondz/garak)"

**Modifications**: Test cases have been adapted to fit PIDB's schema and standardized format. Some cases have been modified to improve clarity or specificity.

---

## NotInject Dataset

**Test Cases**: 339 test cases (64.8%)

**License**: Creative Commons Attribution 4.0 International (CC-BY-4.0)

**Original Work**: NotInject - False Positive Prevention Dataset  
**Purpose**: Testing guardrail over-defense (false positives)

**Description**: The NotInject dataset focuses on benign prompts that contain trigger words commonly flagged by guardrail systems. These test cases are essential for preventing over-blocking and ensuring good user experience.

**Categories Included**:
- Over-defense tests (benign prompts with trigger words)
- Legitimate security questions
- Normal developer queries
- Edge cases with security terminology

**Attribution Text**: "Derived from NotInject dataset"

**Modifications**: Test cases have been adapted to fit PIDB's schema and standardized format.

**Note**: If you are the creator of the NotInject dataset and have specific attribution requirements, please contact us at contact@directivecommons.org so we can update this attribution appropriately.

---

## Original PIDB Test Cases

**Test Cases**: 253 test cases (39.3%)

**License**: MIT License (same as repository)

**Creator**: Directive Commons and contributors

**Description**: These are original test cases created specifically for PIDB, including:

**Categories**:
- **Advanced Encoding Attacks** (25 cases) - Base64, HTML entities, Unicode manipulation, zero-width characters
- **Multilingual Sophisticated Attacks** (25 cases) - Cross-language attacks using cultural context:
  - Chinese (Daoist philosophy, I Ching)
  - Spanish (Borges literature, Vygotsky psychology)
  - Arabic (Islamic philosophy, Sufi traditions)
  - Japanese (Zen koans, martial arts)
  - Russian (Dostoevsky, dialectical materialism)
- **Ultra-Sophisticated Attacks** (5 cases) - State-of-the-art attacks with zero obvious keywords
- **LLM-Specific Attacks** (15 cases) - Adversarial attacks targeting LLM-based classifiers
- **Other Original Cases** (63 cases) - Various attack patterns and benign tests

**Attribution**: No additional attribution required - covered by repository's MIT License.

---

## License Compatibility

All included licenses are compatible with PIDB's MIT License:

- **Apache-2.0** → Compatible with MIT (permissive)
- **CC-BY-4.0** → Compatible with MIT for datasets (requires attribution)
- **MIT** → Native repository license

PIDB as a whole is distributed under the MIT License, with proper attribution maintained for all derivative works as required by their respective licenses.

---

## How to Cite

### Citing PIDB

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

### Citing with Full Attribution

If you use PIDB in research and want to acknowledge all sources:

```
This research uses the Prompt Injection Detection Benchmark (PIDB) [1], 
which includes test cases derived from Garak [2] and the NotInject dataset.

[1] Directive Commons. (2026). Prompt Injection Detection Benchmark (PIDB). 
    https://github.com/directive-commons/prompt-injection-benchmark

[2] Derczynski, L. et al. Garak: LLM vulnerability scanner. 
    https://github.com/leondz/garak
```

---

## Reporting Attribution Issues

If you believe:
- Attribution is incomplete or incorrect
- Your work is included without proper attribution
- There are licensing concerns

Please contact us immediately:
- **Email**: contact@directivecommons.org
- **GitHub**: Open an issue with tag `attribution`

We take attribution seriously and will address any concerns promptly.

---

## Contributing New Test Cases

When contributing test cases to PIDB:

1. **Original Work**: If creating original test cases, they will be licensed under MIT (same as repository)

2. **Derivative Work**: If basing test cases on other sources:
   - Ensure you have the right to contribute
   - Provide proper attribution
   - Specify the source license
   - Include in your PR description

See [CONTRIBUTING.md](CONTRIBUTING.md) for full details.

---

## Acknowledgments

Beyond the specific sources listed above, we acknowledge:
- The broader AI safety and security research community
- Open-source security tools and frameworks
- Academic researchers studying prompt injection
- Community contributors who help improve PIDB

Thank you for making AI systems safer! 🙏

---

**Last Updated**: 2026-01-15  
**PIDB Version**: 1.0.0
