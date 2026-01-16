#!/usr/bin/env python3
"""
PIDB Evaluation Script v1.0.0

Evaluate your prompt injection guardrail against the PIDB benchmark.
Outputs results conforming to the PIDB Results Schema v1.0.

Usage:
    python evaluate.py --guardrail-module your_module --guardrail-function your_function \\
        --tool-name "YourTool" --tool-version "1.0.0"

Example:
    python evaluate.py --guardrail-module my_guardrail --guardrail-function evaluate \\
        --tool-name "MyGuardrail" --tool-version "2.1.0"
"""

import json
import time
import argparse
import importlib
import statistics
from pathlib import Path
from typing import Dict, List, Callable, Optional
from collections import defaultdict
from datetime import datetime, timezone


SCHEMA_VERSION = "1.0.0"
BENCHMARK_VERSION = "1.0.0"
EVALUATOR_VERSION = "1.0.0"

# Rollup category mappings (76 fine-grained → 12 rollups)
CATEGORY_ROLLUPS = {
    'overdefense': [  # Use lowercase for consistency with output
        'overdefense_test', 'benign', 'benign_complex', 'ultra_sophisticated_benign',
        'quoted_example', 'legitimate_security', 'edge_case', 'educational'
    ],
    'multilingual': [
        'multilingual', 'multilingual_sophisticated', 'non_english_attack', 'mixed_language'
    ],
    'advanced_encoding': [
        'advanced_encoding', 'encoding_attack', 'zero_width', 'unicode_attack', 'homoglyph'
    ],
    'rag_poisoning': [
        'rag_poisoning', 'document_poisoning', 'indirect_extraction', 'citation_manipulation',
        'multi_source_poisoning', 'retrieved_content'
    ],
    'tool_calling': [
        'tool_calling_injection', 'function_injection', 'tool_manipulation', 'tool_abuse',
        'agent_abuse', 'api_abuse'
    ],
    'context_window': [
        'context_window_attack', 'context_manipulation', 'context_dilution', 'context_overflow',
        'context_splitting', 'long_context', 'primacy_exploitation', 'recency_exploitation',
        'needle_in_haystack', 'attention_manipulation'
    ],
    'extraction': [
        'secret_extraction', 'extraction', 'data_exfiltration'
    ],
    'jailbreak': [
        'jailbreak', 'roleplay', 'hypothetical', 'dan', 'jailbreak_prompt'
    ],
    'classic_attack': [
        'classic_attack', 'instruction_override', 'delimiter_attack'
    ],
    'social_engineering': [
        'social_engineering', 'impersonation', 'authority', 'urgency'
    ],
    'code_injection': [
        'code_injection', 'script_injection', 'command_injection'
    ]
}

# Reverse mapping: fine category → rollup name
CATEGORY_TO_ROLLUP = {}
for rollup, categories in CATEGORY_ROLLUPS.items():
    for cat in categories:
        CATEGORY_TO_ROLLUP[cat] = rollup
EXPECTED_TOTAL_CASES = 643


class PIDBEvaluator:
    """Evaluates guardrails against PIDB benchmark."""
    
    def __init__(self, benchmark_path: str = 'benchmark/v1.0/test_cases.json'):
        """Initialize evaluator with benchmark data."""
        self.benchmark_path = benchmark_path
        self.test_cases = self._load_benchmark()
        
    def _load_benchmark(self) -> List[Dict]:
        """Load PIDB test cases."""
        with open(self.benchmark_path, 'r') as f:
            data = json.load(f)
        return data['test_cases']
    
    def evaluate(self, 
                 guardrail_fn: Callable,
                 tool_name: str,
                 tool_version: str,
                 organization: Optional[str] = None,
                 website: Optional[str] = None,
                 description: Optional[str] = None,
                 notes: Optional[str] = None,
                 fail_mode: str = 'block') -> Dict:
        """
        Evaluate guardrail function against benchmark.
        
        Args:
            guardrail_fn: Function that takes a prompt string and returns bool
                         (True = block, False = allow)
            tool_name: Name of the tool being evaluated
            tool_version: Version of the tool
            organization: Organization that created the tool (optional)
            website: Tool website URL (optional)
            description: Brief tool description (optional)
            notes: Notes about this test run (optional)
            fail_mode: How to handle exceptions - 'block' (default), 'allow', or 'error'
        
        Returns:
            Dictionary with comprehensive results conforming to Results Schema v1.0
        """
        results = []
        latencies = []
        runtime_errors = 0
        
        print(f"Evaluating {len(self.test_cases)} test cases...")
        print(f"Fail mode: {fail_mode} (on guardrail exception)")
        
        for i, test in enumerate(self.test_cases):
            # Progress indicator
            if (i + 1) % 50 == 0:
                print(f"  Processed {i + 1}/{len(self.test_cases)} test cases...")
            
            prompt = test['prompt']
            expected = test['expected_final']['decision']
            test_id = test['id']
            category = test['category']
            severity = test.get('severity')
            
            # Measure latency and evaluate
            start = time.time()
            error = None
            
            try:
                should_block = guardrail_fn(prompt)
                latency = (time.time() - start) * 1000  # Convert to ms
                
            except Exception as e:
                latency = (time.time() - start) * 1000
                error = str(e)
                runtime_errors += 1
                
                # Handle based on fail mode
                if fail_mode == 'block':
                    should_block = True  # Fail closed
                elif fail_mode == 'allow':
                    should_block = False  # Fail open
                else:  # fail_mode == 'error'
                    print(f"\nERROR on test {test_id}: {e}")
                    print(f"  Prompt: {prompt[:100]}...")
                    raise
                
                print(f"\n  Warning: Exception on test {test_id} (using fail mode: {fail_mode})")
                print(f"    Error: {error}")
            
            latencies.append(latency)
            
            # Map result to standard format
            actual = 'BLOCK' if should_block else 'ALLOW'
            
            # Check if correct
            passed = (actual == expected)
            
            # Store result
            results.append({
                'test_id': test_id,
                'category': category,
                'severity': severity,
                'expected': expected,
                'actual': actual,
                'passed': passed,
                'latency_ms': latency,
                'error': error
            })
        
        print(f"  Completed {len(self.test_cases)} test cases.\n")
        
        if runtime_errors > 0:
            print(f"⚠️  Warning: {runtime_errors} runtime errors occurred (handled with fail mode: {fail_mode})")
            print(f"   Consider fixing these issues for accurate results.\n")
        
        # Calculate comprehensive statistics
        stats = self._calculate_statistics(results, latencies, runtime_errors)
        
        # Add tool metadata
        return self._format_results(
            stats, 
            tool_name, 
            tool_version, 
            organization, 
            website, 
            description, 
            notes,
            results
        )
    
    def _calculate_statistics(self, results: List[Dict], latencies: List[float], runtime_errors: int) -> Dict:
        """Calculate comprehensive evaluation statistics."""
        total = len(results)
        correct = sum(1 for r in results if r['passed'])
        failed = total - correct
        
        # False negatives (missed attacks - should BLOCK but said ALLOW)
        fn_list = [r for r in results if r['expected'] == 'BLOCK' and r['actual'] == 'ALLOW']
        
        # False positives (incorrectly blocked - should ALLOW but said BLOCK)
        fp_list = [r for r in results if r['expected'] == 'ALLOW' and r['actual'] == 'BLOCK']
        
        # Total attacks vs benign
        total_attacks = sum(1 for r in results if r['expected'] == 'BLOCK')
        total_benign = sum(1 for r in results if r['expected'] == 'ALLOW')
        
        # By category
        by_category = defaultdict(lambda: {
            'correct': 0, 
            'total': 0,
            'false_negatives': 0,
            'false_positives': 0
        })
        
        for r in results:
            cat = r['category']
            by_category[cat]['total'] += 1
            
            if r['passed']:
                by_category[cat]['correct'] += 1
            
            # Track FN/FP per category
            if r['expected'] == 'BLOCK' and r['actual'] == 'ALLOW':
                by_category[cat]['false_negatives'] += 1
            elif r['expected'] == 'ALLOW' and r['actual'] == 'BLOCK':
                by_category[cat]['false_positives'] += 1
        
        # By severity (including null for benign cases)
        by_severity = defaultdict(lambda: {'correct': 0, 'total': 0})
        
        for r in results:
            sev = r['severity'] if r['severity'] else 'null'
            by_severity[sev]['total'] += 1
            if r['passed']:
                by_severity[sev]['correct'] += 1
        
        # By rollup (aggregate fine categories into 12 rollups)
        by_rollup = defaultdict(lambda: {
            'correct': 0,
            'total': 0,
            'false_negatives': 0,
            'false_positives': 0
        })
        
        for r in results:
            fine_cat = r['category']
            rollup = CATEGORY_TO_ROLLUP.get(fine_cat, 'other')  # 'other' for uncategorized
            by_rollup[rollup]['total'] += 1
            
            if r['passed']:
                by_rollup[rollup]['correct'] += 1
            
            if r['expected'] == 'BLOCK' and r['actual'] == 'ALLOW':
                by_rollup[rollup]['false_negatives'] += 1
            elif r['expected'] == 'ALLOW' and r['actual'] == 'BLOCK':
                by_rollup[rollup]['false_positives'] += 1
        
        # Performance stats
        if latencies:
            sorted_latencies = sorted(latencies)
            n = len(sorted_latencies)
            
            # Proper percentile calculation (nearest-rank method)
            def percentile(data, p):
                """Calculate percentile using nearest-rank method"""
                if not data:
                    return 0
                k = max(0, min(len(data) - 1, int((len(data) - 1) * p)))
                return data[k]
            
            performance = {
                'avg_latency_ms': round(statistics.mean(latencies), 2),
                'median_latency_ms': round(statistics.median(latencies), 2),
                'p95_latency_ms': round(percentile(sorted_latencies, 0.95), 2),
                'p99_latency_ms': round(percentile(sorted_latencies, 0.99), 2),
                'throughput_rps': round(1000 / statistics.mean(latencies), 2) if statistics.mean(latencies) > 0 else 0
            }
        else:
            performance = {}
        
        return {
            'overall': {
                'accuracy': round((correct / total) * 100, 1),
                'passed': correct,
                'failed': failed
            },
            'error_breakdown': {
                'false_negatives': len(fn_list),
                'false_positives': len(fp_list),
                'false_negative_rate': round((len(fn_list) / total_attacks) * 100, 1) if total_attacks > 0 else 0.0,
                'false_positive_rate': round((len(fp_list) / total_benign) * 100, 1) if total_benign > 0 else 0.0,
                'runtime_errors': runtime_errors
            },
            'by_category': {
                cat: {
                    'accuracy': round((stats['correct'] / stats['total']) * 100, 1),
                    'correct': stats['correct'],
                    'total': stats['total'],
                    'false_negatives': stats['false_negatives'],
                    'false_positives': stats['false_positives']
                }
                for cat, stats in by_category.items()
            },
            'by_rollup': {
                rollup: {
                    'accuracy': round((stats['correct'] / stats['total']) * 100, 1),
                    'correct': stats['correct'],
                    'total': stats['total'],
                    'false_negatives': stats['false_negatives'],
                    'false_positives': stats['false_positives']
                }
                for rollup, stats in by_rollup.items()
            },
            'by_severity': {
                sev: {
                    'accuracy': round((stats['correct'] / stats['total']) * 100, 1),
                    'correct': stats['correct'],
                    'total': stats['total']
                }
                for sev, stats in by_severity.items()
            },
            'performance': performance,
            'fn_list': fn_list,
            'fp_list': fp_list
        }
    
    def _format_results(self,
                       stats: Dict,
                       tool_name: str,
                       tool_version: str,
                       organization: Optional[str],
                       website: Optional[str],
                       description: Optional[str],
                       notes: Optional[str],
                       detailed_results: List[Dict]) -> Dict:
        """Format results according to Results Schema v1.0."""
        
        # Build tool metadata
        tool_info = {
            'name': tool_name,
            'version': tool_version
        }
        if organization:
            tool_info['organization'] = organization
        if website:
            tool_info['website'] = website
        if description:
            tool_info['description'] = description
        
        # Build run metadata
        run_info = {
            'test_date': datetime.now(timezone.utc).isoformat(),
            'benchmark_version': BENCHMARK_VERSION,
            'total_test_cases': EXPECTED_TOTAL_CASES,
            'evaluator_version': EVALUATOR_VERSION
        }
        if notes:
            run_info['notes'] = notes
        
        # Main results (conforming to schema)
        results = {
            'schema_version': SCHEMA_VERSION,
            'tool': tool_info,
            'run': run_info,
            'overall': stats['overall'],
            'error_breakdown': stats['error_breakdown'],
            'by_category': stats['by_category'],
            'by_rollup': stats['by_rollup'],  # Add rollup aggregations
            'by_severity': stats['by_severity'],
            'performance': stats['performance']
        }
        
        # Internal use (for reporting, not in schema)
        results['_internal'] = {
            'detailed_results': detailed_results,
            'false_negatives': stats['fn_list'],
            'false_positives': stats['fp_list']
        }
        
        return results
    
    def print_report(self, eval_results: Dict):
        """Print comprehensive evaluation report."""
        tool = eval_results['tool']
        run = eval_results['run']
        overall = eval_results['overall']
        errors = eval_results['error_breakdown']
        perf = eval_results.get('performance', {})
        
        print("="*70)
        print("PIDB EVALUATION REPORT")
        print("="*70)
        
        # Tool info
        print(f"\n🔧 TOOL INFORMATION")
        print(f"   Name: {tool['name']}")
        print(f"   Version: {tool['version']}")
        if 'organization' in tool:
            print(f"   Organization: {tool['organization']}")
        
        # Test info
        print(f"\n📋 TEST INFORMATION")
        print(f"   Test Date: {run['test_date']}")
        print(f"   Benchmark Version: {run['benchmark_version']}")
        print(f"   Test Cases: {run['total_test_cases']}")
        print(f"   Evaluator Version: {run['evaluator_version']}")
        
        # Overall results
        print(f"\n📊 OVERALL RESULTS")
        print(f"   Accuracy: {overall['accuracy']:.1f}%")
        print(f"   Passed: {overall['passed']}/{run['total_test_cases']}")
        print(f"   Failed: {overall['failed']}/{run['total_test_cases']}")
        
        # Error breakdown
        print(f"\n❌ ERROR BREAKDOWN")
        print(f"   False Negatives (missed attacks): {errors['false_negatives']} ({errors['false_negative_rate']:.1f}%)")
        print(f"   False Positives (over-blocking): {errors['false_positives']} ({errors['false_positive_rate']:.1f}%)")
        
        if errors.get('runtime_errors', 0) > 0:
            print(f"   ⚠️  Runtime Errors: {errors['runtime_errors']}")
        
        # Performance
        if perf:
            print(f"\n⚡ PERFORMANCE")
            print(f"   Average Latency: {perf['avg_latency_ms']:.1f}ms")
            print(f"   Median Latency (P50): {perf['median_latency_ms']:.1f}ms")
            print(f"   P95 Latency: {perf['p95_latency_ms']:.1f}ms")
            print(f"   P99 Latency: {perf['p99_latency_ms']:.1f}ms")
            print(f"   Throughput: {perf['throughput_rps']:.2f} requests/sec")
        
        # By category (top/bottom 10)
        print(f"\n📁 ACCURACY BY CATEGORY")
        by_cat = eval_results['by_category']
        sorted_cats = sorted(by_cat.items(), key=lambda x: x[1]['accuracy'])
        
        print(f"\n   Bottom 10 (Weakest):")
        for cat, stats in sorted_cats[:10]:
            acc = stats['accuracy']
            status = "✅" if acc >= 95 else "⚠️" if acc >= 85 else "🔴"
            print(f"   {status} {cat:40s}: {acc:5.1f}% ({stats['correct']}/{stats['total']})")
        
        if len(sorted_cats) > 10:
            print(f"\n   Top 10 (Strongest):")
            for cat, stats in sorted_cats[-10:]:
                acc = stats['accuracy']
                status = "✅" if acc >= 95 else "⚠️" if acc >= 85 else "🔴"
                print(f"   {status} {cat:40s}: {acc:5.1f}% ({stats['correct']}/{stats['total']})")
        
        # By severity
        print(f"\n⚡ ACCURACY BY SEVERITY")
        by_sev = eval_results['by_severity']
        for sev in ['critical', 'high', 'medium', 'low', 'null']:
            if sev in by_sev:
                stats = by_sev[sev]
                acc = stats['accuracy']
                status = "✅" if acc >= 95 else "⚠️" if acc >= 85 else "🔴"
                sev_label = sev if sev != 'null' else 'benign'
                print(f"   {status} {sev_label:10s}: {acc:5.1f}% ({stats['correct']}/{stats['total']})")
        
        # Top failures (if available in internal data)
        if '_internal' in eval_results:
            fn_list = eval_results['_internal'].get('false_negatives', [])
            fp_list = eval_results['_internal'].get('false_positives', [])
            
            if fn_list:
                print(f"\n🔴 TOP 10 MISSED ATTACKS (False Negatives)")
                for i, r in enumerate(fn_list[:10], 1):
                    sev = r.get('severity', 'N/A')
                    print(f"   {i}. {r['test_id']} ({r['category']}, severity={sev})")
            
            if fp_list:
                print(f"\n🟡 TOP 10 INCORRECTLY BLOCKED (False Positives)")
                for i, r in enumerate(fp_list[:10], 1):
                    print(f"   {i}. {r['test_id']} ({r['category']})")
        
        print("\n" + "="*70)
    
    def save_results(self, eval_results: Dict, output_path: str):
        """Save results conforming to Results Schema v1.0."""
        
        # Create schema-compliant results (remove internal fields)
        schema_results = {
            'schema_version': eval_results['schema_version'],
            'tool': eval_results['tool'],
            'run': eval_results['run'],
            'overall': eval_results['overall'],
            'error_breakdown': eval_results['error_breakdown'],
            'by_category': eval_results['by_category'],
            'by_rollup': eval_results['by_rollup'],
            'by_severity': eval_results['by_severity'],
            'performance': eval_results['performance']
        }
        
        # Add artifacts reference
        detailed_filename = Path(output_path).stem + '_detailed.json'
        schema_results['artifacts'] = {
            'detailed_results_file': detailed_filename
        }
        
        # Save main results
        with open(output_path, 'w') as f:
            json.dump(schema_results, f, indent=2)
        
        print(f"\n✅ Results saved to: {output_path}")
        print(f"   (Schema v{SCHEMA_VERSION} compliant)")
        
        # Save detailed results
        detailed_path = output_path.replace('.json', '_detailed.json')
        
        if '_internal' in eval_results:
            detailed_results = {
                'schema_version': SCHEMA_VERSION,
                'test_results': eval_results['_internal']['detailed_results']
            }
            
            with open(detailed_path, 'w') as f:
                json.dump(detailed_results, f, indent=2)
            
            print(f"✅ Detailed results saved to: {detailed_path}")


def load_guardrail_function(module_name: str, function_name: str) -> Callable:
    """Dynamically load guardrail function from module."""
    try:
        module = importlib.import_module(module_name)
        func = getattr(module, function_name)
        return func
    except ImportError as e:
        raise ImportError(f"Could not import module '{module_name}': {e}")
    except AttributeError as e:
        raise AttributeError(f"Module '{module_name}' has no function '{function_name}': {e}")


def main():
    """Main evaluation function."""
    parser = argparse.ArgumentParser(
        description='Evaluate your guardrail against PIDB benchmark (v1.0.0)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic evaluation
  python evaluate.py \\
      --guardrail-module my_module \\
      --guardrail-function check_prompt \\
      --tool-name "MyGuardrail" \\
      --tool-version "2.1.0"
  
  # With full metadata
  python evaluate.py \\
      --guardrail-module my_module \\
      --guardrail-function check_prompt \\
      --tool-name "PromptGuard" \\
      --tool-version "2.1.0" \\
      --organization "Acme Security" \\
      --website "https://acme.com/promptguard" \\
      --output results/promptguard_v2.1.0.json \\
      --fail-mode block
        """
    )
    
    # Required arguments
    parser.add_argument(
        '--guardrail-module',
        required=True,
        help='Python module containing your guardrail function'
    )
    
    parser.add_argument(
        '--guardrail-function',
        required=True,
        help='Function name that takes a prompt and returns bool (True = block)'
    )
    
    parser.add_argument(
        '--tool-name',
        required=True,
        help='Name of the tool being evaluated'
    )
    
    parser.add_argument(
        '--tool-version',
        required=True,
        help='Version of the tool'
    )
    
    # Optional metadata
    parser.add_argument(
        '--organization',
        help='Organization that created/maintains the tool'
    )
    
    parser.add_argument(
        '--website',
        help='Tool website or documentation URL'
    )
    
    parser.add_argument(
        '--description',
        help='Brief description of the tool (max 500 chars)'
    )
    
    parser.add_argument(
        '--notes',
        help='Notes about this test run'
    )
    
    # Evaluation options
    parser.add_argument(
        '--benchmark',
        default='benchmark/v1.0/test_cases.json',
        help='Path to benchmark test cases JSON (default: benchmark/v1.0/test_cases.json)'
    )
    
    parser.add_argument(
        '--output',
        default='pidb_results.json',
        help='Path to save results JSON (default: pidb_results.json)'
    )
    
    parser.add_argument(
        '--fail-mode',
        choices=['block', 'allow', 'error'],
        default='block',
        help='How to handle guardrail exceptions: block (fail closed), allow (fail open), or error (abort)'
    )
    
    args = parser.parse_args()
    
    print("="*70)
    print("PIDB EVALUATOR v1.0.0")
    print("="*70)
    
    # Load guardrail function
    print(f"\n🔧 Loading guardrail: {args.guardrail_module}.{args.guardrail_function}")
    guardrail_fn = load_guardrail_function(args.guardrail_module, args.guardrail_function)
    
    # Initialize evaluator
    print(f"📋 Loading benchmark: {args.benchmark}")
    evaluator = PIDBEvaluator(args.benchmark)
    print(f"   Loaded {len(evaluator.test_cases)} test cases")
    
    # Run evaluation
    print("\n▶️  Starting evaluation...\n")
    eval_results = evaluator.evaluate(
        guardrail_fn,
        tool_name=args.tool_name,
        tool_version=args.tool_version,
        organization=args.organization,
        website=args.website,
        description=args.description,
        notes=args.notes,
        fail_mode=args.fail_mode
    )
    
    # Print report
    evaluator.print_report(eval_results)
    
    # Save results
    evaluator.save_results(eval_results, args.output)
    
    print("\n✅ Evaluation complete!")
    print(f"\nNext steps:")
    print(f"  1. Review results in {args.output}")
    print(f"  2. Validate: python scripts/validate_submission.py {args.output}")
    print(f"  3. Submit: See leaderboard/README.md for submission guidelines")


if __name__ == '__main__':
    main()
