# Quick Start Guide - PIDB

Get up and running with the Prompt Injection Detection Benchmark in 5 minutes.

## Installation

```bash
# Clone the repository
git clone https://github.com/directive-commons/prompt-injection-benchmark
cd prompt-injection-benchmark

# Option 1: pip install (recommended - handles imports automatically)
pip install -e .

# Option 2: Manual PYTHONPATH (if not using pip)
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

## Test Your Guardrail

### Option 1: Use the Evaluation Script

```bash
# If you used pip install -e ., imports work automatically:
python scripts/evaluate.py \
    --guardrail-module your_module \
    --guardrail-function your_function \
    --tool-name "YourTool" \
    --tool-version "1.0.0" \
    --output results.json

# If you didn't use pip, set PYTHONPATH:
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python scripts/evaluate.py ...

# Validate results
python scripts/validate_submission.py results.json
```

### Option 2: Write Your Own Test

```python
import json

# Load benchmark
with open('benchmark/v1.0/test_cases.json') as f:
    data = json.load(f)
    tests = data['test_cases']

# Test your guardrail
correct = 0
for test in tests:
    result = your_guardrail(test['prompt'])
    expected = test['expected_final']['decision']
    actual = 'BLOCK' if result else 'ALLOW'
    
    if actual == expected:
        correct += 1

print(f"Accuracy: {correct / len(tests) * 100:.1f}%")
```

## Try the Example

```bash
# If you used pip install -e .:
python examples/simple_guardrail.py
python scripts/evaluate.py \
    --guardrail-module examples.simple_guardrail \
    --guardrail-function check_prompt \
    --tool-name "SimpleGuardrail" \
    --tool-version "1.0.0" \
    --output example_results.json

# If using PYTHONPATH instead:
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python examples/simple_guardrail.py
python scripts/evaluate.py ...

# Validate
python scripts/validate_submission.py example_results.json
```

## Submit Your Results

1. Run the benchmark on your guardrail
2. Create `leaderboard/results/your-tool.json` with results
3. Submit a Pull Request

See [leaderboard/README.md](leaderboard/README.md) for details.

## Next Steps

- 📖 Read [docs/getting-started.md](docs/getting-started.md) for detailed guide
- 📋 Review [docs/methodology.md](docs/methodology.md) to understand the benchmark
- 🏆 Check [leaderboard/README.md](leaderboard/README.md) to submit results
- 💬 Join discussions on GitHub

## Need Help?

- **Questions**: Open a [GitHub Discussion](https://github.com/directive-commons/prompt-injection-benchmark/discussions)
- **Issues**: Report [bugs](https://github.com/directive-commons/prompt-injection-benchmark/issues)
- **Email**: contact@directivecommons.org
- **Twitter**: [@directivecommon](https://twitter.com/directivecommon)
