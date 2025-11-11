"""
Test suite for Project A - Pre-Feature Basic Search
"""

import sys
import os
import json
import time
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from search_engine import BasicSearchEngine


class TestRunner:
    """Test runner for basic search functionality."""
    
    def __init__(self, test_data_file: str, products_file: str):
        """
        Initialize test runner.
        
        Args:
            test_data_file: Path to test data JSON file
            products_file: Path to products JSON file
        """
        self.test_data_file = test_data_file
        self.products_file = products_file
        self.search_engine = BasicSearchEngine(products_file)
        self.results = []
        
    def load_test_cases(self):
        """Load test cases from JSON file."""
        try:
            with open(self.test_data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Test data file not found: {self.test_data_file}")
            return []
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in test data file: {e}")
            return []
    
    def run_test_case(self, test_case: dict) -> dict:
        """
        Run a single test case.
        
        Args:
            test_case: Test case dictionary
            
        Returns:
            Test result dictionary
        """
        test_id = test_case.get('test_id', 'unknown')
        query = test_case.get('input_query', '')
        expected_results = test_case.get('expected_results', {})
        
        # Perform search
        start_time = time.time()
        search_result = self.search_engine.search(query)
        end_time = time.time()
        
        # Extract metrics
        actual_results = search_result.get('results', [])
        total_results = search_result.get('total_results', 0)
        response_time = search_result.get('response_time_ms', 0)
        
        # Validate results
        expected_count = expected_results.get('min_results', 0)
        expected_max = expected_results.get('max_results', float('inf'))
        
        # Check if test passed
        passed = True
        failure_reason = None
        
        # Check result count
        if total_results < expected_count or total_results > expected_max:
            passed = False
            failure_reason = f"Result count {total_results} not in expected range [{expected_count}, {expected_max}]"
        
        # Check for expected product IDs if specified
        expected_product_ids = expected_results.get('must_contain_ids', [])
        if expected_product_ids:
            actual_ids = [r.get('id') for r in actual_results]
            missing_ids = [pid for pid in expected_product_ids if pid not in actual_ids]
            if missing_ids:
                passed = False
                failure_reason = f"Missing expected product IDs: {missing_ids}"
        
        # Check for error cases
        if expected_results.get('should_error', False):
            if 'error' not in search_result:
                passed = False
                failure_reason = "Expected error but none occurred"
        else:
            if 'error' in search_result:
                passed = False
                failure_reason = f"Unexpected error: {search_result.get('error')}"
        
        return {
            'test_id': test_id,
            'query': query,
            'passed': passed,
            'failure_reason': failure_reason,
            'total_results': total_results,
            'response_time_ms': round(response_time, 2),
            'actual_execution_time_ms': round((end_time - start_time) * 1000, 2),
            'result_ids': [r.get('id') for r in actual_results[:10]],  # First 10 IDs
            'timestamp': datetime.now().isoformat()
        }
    
    def run_all_tests(self) -> dict:
        """Run all test cases and return aggregated results."""
        test_cases = self.load_test_cases()
        
        if not test_cases:
            return {
                'total_tests': 0,
                'passed_tests': 0,
                'failed_tests': 0,
                'success_rate': 0.0,
                'average_response_time_ms': 0.0,
                'test_results': []
            }
        
        passed_count = 0
        total_response_time = 0.0
        
        for test_case in test_cases:
            result = self.run_test_case(test_case)
            self.results.append(result)
            
            if result['passed']:
                passed_count += 1
            
            total_response_time += result['response_time_ms']
        
        success_rate = (passed_count / len(test_cases)) * 100 if test_cases else 0
        avg_response_time = total_response_time / len(test_cases) if test_cases else 0
        
        return {
            'total_tests': len(test_cases),
            'passed_tests': passed_count,
            'failed_tests': len(test_cases) - passed_count,
            'success_rate': round(success_rate, 2),
            'average_response_time_ms': round(avg_response_time, 2),
            'test_results': self.results
        }
    
    def save_results(self, output_file: str):
        """Save test results to JSON file."""
        results = self.run_all_tests()
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        return results


def main():
    """Main test execution function."""
    # Get paths
    base_dir = os.path.dirname(os.path.dirname(__file__))
    test_data_file = os.path.normpath(os.path.join(base_dir, '..', 'test_data.json'))
    products_file = os.path.normpath(os.path.join(base_dir, 'data', 'products.json'))
    results_file = os.path.normpath(os.path.join(base_dir, 'results', 'results_pre.json'))
    
    # Run tests
    runner = TestRunner(test_data_file, products_file)
    results = runner.save_results(results_file)
    
    # Print summary
    print("\n" + "="*60)
    print("PROJECT A - PRE-FEATURE SEARCH TEST RESULTS")
    print("="*60)
    print(f"Total Tests: {results['total_tests']}")
    print(f"Passed: {results['passed_tests']}")
    print(f"Failed: {results['failed_tests']}")
    print(f"Success Rate: {results['success_rate']}%")
    print(f"Average Response Time: {results['average_response_time_ms']} ms")
    print("="*60)
    
    # Print individual test results
    print("\nIndividual Test Results:")
    for result in results['test_results']:
        status = "PASS" if result['passed'] else "FAIL"
        print(f"  {result['test_id']}: {status} - Query: '{result['query']}' "
              f"({result['total_results']} results, {result['response_time_ms']} ms)")
        if not result['passed'] and result['failure_reason']:
            print(f"    Reason: {result['failure_reason']}")
    
    return 0 if results['failed_tests'] == 0 else 1


if __name__ == '__main__':
    exit(main())

