"""
Project A: Test Suite for Basic Search
Tests the pre-feature basic keyword matching functionality
"""
import json
import sys
import os
import time
from typing import Dict, List, Any
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add parent directory to path to import search_engine
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from search_engine import BasicSearchEngine


class TestRunner:
    """Test runner for Project A"""
    
    def __init__(self, data_file: str, test_cases_file: str, results_dir: str, log_file: str):
        """Initialize test runner"""
        self.engine = BasicSearchEngine(data_file)
        self.test_cases = self._load_test_cases(test_cases_file)
        self.results_dir = results_dir
        self.log_file = log_file
        self.results = []
        self.metrics = {
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'success_rate': 0.0,
            'avg_response_time_ms': 0.0,
            'total_time_ms': 0.0
        }
    
    def _load_test_cases(self, test_cases_file: str) -> List[Dict]:
        """Load test cases from JSON file"""
        try:
            with open(test_cases_file, 'r') as f:
                data = json.load(f)
                return data.get('test_cases', [])
        except FileNotFoundError:
            logger.error(f"Test cases file not found: {test_cases_file}")
            return []
    
    def run_tests(self) -> None:
        """Run all test cases"""
        logger.info("="*60)
        logger.info("PROJECT A: BASIC SEARCH - TEST EXECUTION")
        logger.info("="*60)
        
        start_time = time.time()
        self.metrics['total_tests'] = len(self.test_cases)
        
        for test_case in self.test_cases:
            self._run_single_test(test_case)
        
        total_time = (time.time() - start_time) * 1000
        self.metrics['total_time_ms'] = total_time
        self._calculate_metrics()
        
        logger.info("="*60)
        logger.info(f"TEST EXECUTION COMPLETED in {total_time:.2f}ms")
        logger.info("="*60)
    
    def _run_single_test(self, test_case: Dict[str, Any]) -> None:
        """Run a single test case"""
        test_id = test_case['test_id']
        query = test_case['query']
        expected_results = test_case['expected_results']
        description = test_case['description']
        
        logger.info(f"\n[{test_id}] {description}")
        logger.info(f"Query: '{query}'")
        logger.info(f"Expected: {expected_results}")
        
        # Execute search
        search_result = self.engine.search(query)
        actual_results = [r['id'] for r in search_result['results']]
        response_time = search_result['response_time_ms']
        
        logger.info(f"Actual: {actual_results}")
        logger.info(f"Response Time: {response_time:.2f}ms")
        
        # Determine pass/fail
        # For basic search, we check if expected results are in actual results
        # (may have additional matches due to partial matches)
        passed = all(exp_id in actual_results for exp_id in expected_results)
        
        self.results.append({
            'test_id': test_id,
            'description': description,
            'type': test_case['type'],
            'query': query,
            'expected_results': expected_results,
            'actual_results': actual_results,
            'total_results': search_result['total_results'],
            'response_time_ms': response_time,
            'passed': passed,
            'match_type': 'keyword_matching'
        })
        
        if passed:
            logger.info(f"✓ PASSED")
            self.metrics['passed'] += 1
        else:
            logger.info(f"✗ FAILED")
            self.metrics['failed'] += 1
    
    def _calculate_metrics(self) -> None:
        """Calculate evaluation metrics"""
        if self.metrics['total_tests'] > 0:
            self.metrics['success_rate'] = (self.metrics['passed'] / self.metrics['total_tests']) * 100
        
        response_times = [r['response_time_ms'] for r in self.results]
        if response_times:
            self.metrics['avg_response_time_ms'] = sum(response_times) / len(response_times)
    
    def generate_report(self) -> None:
        """Generate and save test report"""
        os.makedirs(self.results_dir, exist_ok=True)
        
        # Save results to JSON
        results_file = os.path.join(self.results_dir, 'results_pre.json')
        report = {
            'project': 'Project A - Pre-Feature (Basic Search)',
            'timestamp': datetime.now().isoformat(),
            'metrics': self.metrics,
            'test_results': self.results
        }
        
        with open(results_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"\nResults saved to: {results_file}")
        
        # Print summary metrics
        logger.info("\n" + "="*60)
        logger.info("METRICS SUMMARY")
        logger.info("="*60)
        logger.info(f"Total Tests: {self.metrics['total_tests']}")
        logger.info(f"Passed: {self.metrics['passed']}")
        logger.info(f"Failed: {self.metrics['failed']}")
        logger.info(f"Success Rate: {self.metrics['success_rate']:.1f}%")
        logger.info(f"Average Response Time: {self.metrics['avg_response_time_ms']:.2f}ms")
        logger.info(f"Total Execution Time: {self.metrics['total_time_ms']:.2f}ms")
        logger.info("="*60)


def main():
    """Main entry point"""
    # Determine file paths
    test_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(test_dir)
    data_file = os.path.join(project_dir, 'data', 'products.json')
    test_cases_file = os.path.join(os.path.dirname(project_dir), 'shared_artifacts', 'test_data.json')
    results_dir = os.path.join(project_dir, 'results')
    log_file = os.path.join(project_dir, 'logs', 'log_pre.txt')
    
    # Ensure log directory exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Add file handler to logger
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)
    
    # Run tests
    runner = TestRunner(data_file, test_cases_file, results_dir, log_file)
    runner.run_tests()
    runner.generate_report()


if __name__ == '__main__':
    main()
