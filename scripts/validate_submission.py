#!/usr/bin/env python3
"""
PIDB Submission Validator v1.0.0

Validates that a results file conforms to the PIDB Results Schema v1.0.

Usage:
    python validate_submission.py <results_file.json>

Example:
    python validate_submission.py pidb_results.json
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


# Expected values for v1.0.0
EXPECTED_SCHEMA_VERSION = "1.0.0"
EXPECTED_BENCHMARK_VERSION = "1.0.0"
EXPECTED_TOTAL_CASES = 643
EXPECTED_TOTAL_ATTACKS = 279
EXPECTED_TOTAL_BENIGN = 364


class ValidationError(Exception):
    """Validation error with details."""
    pass


class PIDBValidator:
    """Validates PIDB results submissions."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate(self, results_file: str) -> Tuple[bool, List[str], List[str]]:
        """
        Validate a results file.
        
        Returns:
            (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []
        
        try:
            # Load JSON
            with open(results_file, 'r') as f:
                data = json.load(f)
            
            # Run all validation checks
            self._validate_schema_version(data)
            self._validate_tool_info(data)
            self._validate_run_info(data)
            self._validate_overall(data)
            self._validate_error_breakdown(data)
            self._validate_by_category(data)
            self._validate_by_severity(data)
            self._validate_performance(data)
            self._validate_math_consistency(data)
            
        except FileNotFoundError:
            self.errors.append(f"File not found: {results_file}")
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON: {e}")
        except Exception as e:
            self.errors.append(f"Unexpected error: {e}")
        
        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings
    
    def _validate_schema_version(self, data: Dict):
        """Validate schema version."""
        if 'schema_version' not in data:
            self.errors.append("Missing required field: 'schema_version'")
            return
        
        if data['schema_version'] != EXPECTED_SCHEMA_VERSION:
            self.errors.append(
                f"Invalid schema_version: {data['schema_version']} "
                f"(expected: {EXPECTED_SCHEMA_VERSION})"
            )
    
    def _validate_tool_info(self, data: Dict):
        """Validate tool metadata."""
        if 'tool' not in data:
            self.errors.append("Missing required section: 'tool'")
            return
        
        tool = data['tool']
        
        # Required fields
        required = ['name', 'version']
        for field in required:
            if field not in tool:
                self.errors.append(f"Missing required field: tool.{field}")
        
        # Validate types
        if 'name' in tool and not isinstance(tool['name'], str):
            self.errors.append("tool.name must be a string")
        
        if 'version' in tool and not isinstance(tool['version'], str):
            self.errors.append("tool.version must be a string")
        
        # Optional fields - warn if missing
        optional = ['organization', 'website']
        for field in optional:
            if field not in tool:
                self.warnings.append(f"Optional field missing: tool.{field} (recommended for leaderboard)")
    
    def _validate_run_info(self, data: Dict):
        """Validate run metadata."""
        if 'run' not in data:
            self.errors.append("Missing required section: 'run'")
            return
        
        run = data['run']
        
        # Required fields
        required = ['test_date', 'benchmark_version', 'total_test_cases']
        for field in required:
            if field not in run:
                self.errors.append(f"Missing required field: run.{field}")
        
        # Validate benchmark version
        if 'benchmark_version' in run:
            if run['benchmark_version'] != EXPECTED_BENCHMARK_VERSION:
                self.errors.append(
                    f"Invalid benchmark_version: {run['benchmark_version']} "
                    f"(expected: {EXPECTED_BENCHMARK_VERSION})"
                )
        
        # Validate total test cases
        if 'total_test_cases' in run:
            if run['total_test_cases'] != EXPECTED_TOTAL_CASES:
                self.errors.append(
                    f"Invalid total_test_cases: {run['total_test_cases']} "
                    f"(expected: {EXPECTED_TOTAL_CASES})"
                )
        
        # Validate test date format
        if 'test_date' in run:
            try:
                datetime.fromisoformat(run['test_date'].replace('Z', '+00:00'))
            except Exception as e:
                self.errors.append(f"Invalid test_date format (should be ISO 8601): {e}")
    
    def _validate_overall(self, data: Dict):
        """Validate overall results."""
        if 'overall' not in data:
            self.errors.append("Missing required section: 'overall'")
            return
        
        overall = data['overall']
        
        # Required fields
        required = ['accuracy', 'passed', 'failed']
        for field in required:
            if field not in overall:
                self.errors.append(f"Missing required field: overall.{field}")
        
        # Validate types and ranges
        if 'accuracy' in overall:
            if not isinstance(overall['accuracy'], (int, float)):
                self.errors.append("overall.accuracy must be a number")
            elif not 0 <= overall['accuracy'] <= 100:
                self.errors.append(f"overall.accuracy out of range: {overall['accuracy']} (must be 0-100)")
        
        if 'passed' in overall and not isinstance(overall['passed'], int):
            self.errors.append("overall.passed must be an integer")
        
        if 'failed' in overall and not isinstance(overall['failed'], int):
            self.errors.append("overall.failed must be an integer")
    
    def _validate_error_breakdown(self, data: Dict):
        """Validate error breakdown."""
        if 'error_breakdown' not in data:
            self.errors.append("Missing required section: 'error_breakdown'")
            return
        
        errors = data['error_breakdown']
        
        # Required fields
        required = ['false_negatives', 'false_positives', 'false_negative_rate', 'false_positive_rate']
        for field in required:
            if field not in errors:
                self.errors.append(f"Missing required field: error_breakdown.{field}")
        
        # Validate types
        for field in ['false_negatives', 'false_positives']:
            if field in errors and not isinstance(errors[field], int):
                self.errors.append(f"error_breakdown.{field} must be an integer")
        
        for field in ['false_negative_rate', 'false_positive_rate']:
            if field in errors:
                if not isinstance(errors[field], (int, float)):
                    self.errors.append(f"error_breakdown.{field} must be a number")
                elif not 0 <= errors[field] <= 100:
                    self.errors.append(f"error_breakdown.{field} out of range: {errors[field]} (must be 0-100)")
        
        # Warn about runtime errors
        if 'runtime_errors' in errors and errors['runtime_errors'] > 0:
            self.warnings.append(
                f"Runtime errors detected: {errors['runtime_errors']} "
                "(consider fixing before submission)"
            )
    
    def _validate_by_category(self, data: Dict):
        """Validate category breakdown."""
        if 'by_category' not in data:
            self.errors.append("Missing required section: 'by_category'")
            return
        
        by_cat = data['by_category']
        
        if not isinstance(by_cat, dict):
            self.errors.append("by_category must be a dictionary")
            return
        
        if len(by_cat) == 0:
            self.errors.append("by_category cannot be empty")
            return
        
        # Validate each category
        for cat_name, cat_stats in by_cat.items():
            required = ['accuracy', 'correct', 'total']
            for field in required:
                if field not in cat_stats:
                    self.errors.append(f"Missing field in by_category.{cat_name}: {field}")
            
            # Validate types
            if 'accuracy' in cat_stats:
                if not isinstance(cat_stats['accuracy'], (int, float)):
                    self.errors.append(f"by_category.{cat_name}.accuracy must be a number")
                elif not 0 <= cat_stats['accuracy'] <= 100:
                    self.errors.append(f"by_category.{cat_name}.accuracy out of range: {cat_stats['accuracy']}")
            
            for field in ['correct', 'total']:
                if field in cat_stats and not isinstance(cat_stats[field], int):
                    self.errors.append(f"by_category.{cat_name}.{field} must be an integer")
            
            # Validate math
            if 'correct' in cat_stats and 'total' in cat_stats:
                if cat_stats['correct'] > cat_stats['total']:
                    self.errors.append(f"by_category.{cat_name}: correct > total")
        
        # Warn if missing major categories
        major_cats = ['overdefense', 'overdefense_test']  # Either name acceptable
        has_overdefense = any(cat in by_cat for cat in major_cats)
        if not has_overdefense:
            self.warnings.append("Recommended to include 'overdefense' or 'overdefense_test' category")
    
    def _validate_by_severity(self, data: Dict):
        """Validate severity breakdown."""
        if 'by_severity' not in data:
            self.errors.append("Missing required section: 'by_severity'")
            return
        
        by_sev = data['by_severity']
        
        if not isinstance(by_sev, dict):
            self.errors.append("by_severity must be a dictionary")
            return
        
        # Validate each severity level
        for sev_name, sev_stats in by_sev.items():
            required = ['accuracy', 'correct', 'total']
            for field in required:
                if field not in sev_stats:
                    self.errors.append(f"Missing field in by_severity.{sev_name}: {field}")
            
            # Validate types
            if 'accuracy' in sev_stats:
                if not isinstance(sev_stats['accuracy'], (int, float)):
                    self.errors.append(f"by_severity.{sev_name}.accuracy must be a number")
            
            for field in ['correct', 'total']:
                if field in sev_stats and not isinstance(sev_stats[field], int):
                    self.errors.append(f"by_severity.{sev_name}.{field} must be an integer")
        
        # Warn if missing expected severity levels
        expected_levels = ['critical', 'high', 'medium', 'low', 'null']
        for level in expected_levels:
            if level not in by_sev:
                self.warnings.append(f"Severity level '{level}' not found in by_severity")
    
    def _validate_performance(self, data: Dict):
        """Validate performance metrics (optional but recommended)."""
        if 'performance' not in data:
            self.warnings.append("Optional section 'performance' not included (recommended)")
            return
        
        perf = data['performance']
        
        if not isinstance(perf, dict):
            self.errors.append("performance must be a dictionary")
            return
        
        # All performance fields are optional, just validate types if present
        numeric_fields = [
            'avg_latency_ms', 'median_latency_ms', 'p95_latency_ms', 
            'p99_latency_ms', 'throughput_rps'
        ]
        
        for field in numeric_fields:
            if field in perf and not isinstance(perf[field], (int, float)):
                self.errors.append(f"performance.{field} must be a number")
    
    def _validate_math_consistency(self, data: Dict):
        """Validate mathematical consistency across results."""
        if 'overall' not in data or 'run' not in data:
            return  # Already reported missing sections
        
        overall = data.get('overall', {})
        run = data.get('run', {})
        errors = data.get('error_breakdown', {})
        
        # Check passed + failed = total
        if 'passed' in overall and 'failed' in overall and 'total_test_cases' in run:
            calculated_total = overall['passed'] + overall['failed']
            expected_total = run['total_test_cases']
            
            if calculated_total != expected_total:
                self.errors.append(
                    f"Math error: passed ({overall['passed']}) + "
                    f"failed ({overall['failed']}) = {calculated_total}, "
                    f"but total_test_cases is {expected_total}"
                )
        
        # Check accuracy calculation
        if 'passed' in overall and 'accuracy' in overall and 'total_test_cases' in run:
            expected_accuracy = round((overall['passed'] / run['total_test_cases']) * 100, 1)
            actual_accuracy = overall['accuracy']
            
            # Allow small rounding differences
            if abs(expected_accuracy - actual_accuracy) > 0.2:
                self.errors.append(
                    f"Math error: accuracy calculation mismatch. "
                    f"Expected ~{expected_accuracy}%, got {actual_accuracy}%"
                )
        
        # Check FN + FP <= failed
        if 'false_negatives' in errors and 'false_positives' in errors and 'failed' in overall:
            total_errors = errors['false_negatives'] + errors['false_positives']
            if total_errors > overall['failed']:
                self.errors.append(
                    f"Math error: false_negatives ({errors['false_negatives']}) + "
                    f"false_positives ({errors['false_positives']}) = {total_errors}, "
                    f"but total failed is only {overall['failed']}"
                )
        
        # Check category totals sum to expected
        if 'by_category' in data:
            total_from_cats = sum(cat['total'] for cat in data['by_category'].values())
            if total_from_cats != EXPECTED_TOTAL_CASES:
                self.errors.append(
                    f"Math error: category totals sum to {total_from_cats}, "
                    f"expected {EXPECTED_TOTAL_CASES}"
                )


def main():
    """Main validation function."""
    parser = argparse.ArgumentParser(
        description='Validate PIDB results file against Results Schema v1.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate_submission.py pidb_results.json
  python validate_submission.py results/my_tool_v1.0.0.json

The validator checks:
  ✓ Schema compliance (required fields, types, ranges)
  ✓ Math consistency (totals, percentages, accuracy)
  ✓ Data integrity (valid dates, proper formatting)
  
Exit codes:
  0 - Validation passed (with possible warnings)
  1 - Validation failed (errors found)
  2 - File not found or invalid JSON
        """
    )
    
    parser.add_argument(
        'results_file',
        help='Path to results JSON file to validate'
    )
    
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Treat warnings as errors'
    )
    
    args = parser.parse_args()
    
    print("="*70)
    print("PIDB SUBMISSION VALIDATOR v1.0.0")
    print("="*70)
    
    # Validate
    print(f"\n📋 Validating: {args.results_file}")
    print(f"   Expected schema version: {EXPECTED_SCHEMA_VERSION}")
    print(f"   Expected benchmark version: {EXPECTED_BENCHMARK_VERSION}")
    print(f"   Expected total test cases: {EXPECTED_TOTAL_CASES}\n")
    
    validator = PIDBValidator()
    is_valid, errors, warnings = validator.validate(args.results_file)
    
    # Print results
    if errors:
        print("❌ VALIDATION FAILED\n")
        print(f"Found {len(errors)} error(s):\n")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
        print()
    
    if warnings:
        print(f"⚠️  Found {len(warnings)} warning(s):\n")
        for i, warning in enumerate(warnings, 1):
            print(f"  {i}. {warning}")
        print()
    
    if is_valid and not warnings:
        print("✅ VALIDATION PASSED")
        print("\nThis results file is valid and ready for submission!")
        print("\nNext steps:")
        print("  1. Review the results file")
        print("  2. Submit via PR to leaderboard/results/")
        print("  3. See leaderboard/README.md for submission guidelines")
        print()
        return 0
    
    elif is_valid and warnings:
        if args.strict:
            print("❌ VALIDATION FAILED (strict mode: warnings treated as errors)")
            print()
            return 1
        else:
            print("✅ VALIDATION PASSED (with warnings)")
            print("\nThis results file is valid but has warnings.")
            print("Consider addressing warnings before submission.")
            print()
            return 0
    
    else:
        print("Please fix the errors and try again.")
        print()
        return 1


if __name__ == '__main__':
    sys.exit(main())
