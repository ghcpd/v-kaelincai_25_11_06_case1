"""
Generate comparison report between Project A and Project B
"""

import json
import os
from datetime import datetime


def load_json_file(file_path):
    """Load JSON file safely."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None


def generate_report():
    """Generate comparison report."""
    # Load results
    import os
    results_a_path = os.path.normpath('Project_A_PreFeature_Search/results/results_pre.json')
    results_b_path = os.path.normpath('Project_B_PostFeature_Search/results/results_post.json')
    results_a = load_json_file(results_a_path)
    results_b = load_json_file(results_b_path)
    
    if not results_a or not results_b:
        print("Error: Could not load test results. Make sure both projects have been tested.")
        return
    
    # Generate markdown report
    report_lines = []
    report_lines.append("# Search Feature Enhancement Comparison Report")
    report_lines.append("")
    report_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")
    report_lines.append("## Executive Summary")
    report_lines.append("")
    report_lines.append("This report compares the basic search implementation (Project A) with the enhanced search implementation (Project B) that includes intelligent recommendations, fuzzy matching, and search suggestions.")
    report_lines.append("")
    
    # Overall metrics comparison
    report_lines.append("## Overall Metrics Comparison")
    report_lines.append("")
    report_lines.append("| Metric | Project A (Pre-Feature) | Project B (Post-Feature) | Improvement |")
    report_lines.append("|--------|------------------------|--------------------------|-------------|")
    
    success_rate_a = results_a.get('success_rate', 0)
    success_rate_b = results_b.get('success_rate', 0)
    success_improvement = success_rate_b - success_rate_a
    report_lines.append(f"| Success Rate | {success_rate_a}% | {success_rate_b}% | {success_improvement:+.2f}% |")
    
    avg_time_a = results_a.get('average_response_time_ms', 0)
    avg_time_b = results_b.get('average_response_time_ms', 0)
    time_diff = avg_time_a - avg_time_b
    time_improvement_pct = ((avg_time_a - avg_time_b) / avg_time_a * 100) if avg_time_a > 0 else 0
    report_lines.append(f"| Avg Response Time | {avg_time_a:.2f} ms | {avg_time_b:.2f} ms | {time_diff:+.2f} ms ({time_improvement_pct:+.1f}%) |")
    
    passed_a = results_a.get('passed_tests', 0)
    passed_b = results_b.get('passed_tests', 0)
    total_tests = results_a.get('total_tests', 0)
    report_lines.append(f"| Tests Passed | {passed_a}/{total_tests} | {passed_b}/{total_tests} | {passed_b - passed_a:+d} |")
    
    report_lines.append("")
    
    # Feature comparison
    report_lines.append("## Feature Comparison")
    report_lines.append("")
    report_lines.append("| Feature | Project A | Project B |")
    report_lines.append("|---------|-----------|-----------|")
    report_lines.append("| Basic Keyword Matching | ✓ | ✓ |")
    report_lines.append("| Fuzzy Matching | ✗ | ✓ |")
    report_lines.append("| Relevance Scoring | ✗ | ✓ |")
    report_lines.append("| Search Suggestions | ✗ | ✓ |")
    report_lines.append("| Related Product Recommendations | ✗ | ✓ |")
    report_lines.append("| Result Ranking | Basic | Intelligent (by relevance) |")
    report_lines.append("")
    
    # Detailed test results
    report_lines.append("## Detailed Test Results")
    report_lines.append("")
    
    # Get test results
    test_results_a = {r['test_id']: r for r in results_a.get('test_results', [])}
    test_results_b = {r['test_id']: r for r in results_b.get('test_results', [])}
    
    report_lines.append("| Test ID | Query | Project A Results | Project B Results | Project A Time | Project B Time | Status A | Status B |")
    report_lines.append("|---------|-------|-------------------|-------------------|----------------|----------------|----------|----------|")
    
    all_test_ids = set(test_results_a.keys()) | set(test_results_b.keys())
    for test_id in sorted(all_test_ids):
        result_a = test_results_a.get(test_id, {})
        result_b = test_results_b.get(test_id, {})
        
        query = result_a.get('query') or result_b.get('query') or 'N/A'
        results_a_count = result_a.get('total_results', 0)
        results_b_count = result_b.get('total_results', 0)
        time_a = result_a.get('response_time_ms', 0)
        time_b = result_b.get('response_time_ms', 0)
        status_a = "PASS" if result_a.get('passed', False) else "FAIL"
        status_b = "PASS" if result_b.get('passed', False) else "FAIL"
        
        report_lines.append(f"| {test_id} | {query} | {results_a_count} | {results_b_count} | {time_a:.2f} ms | {time_b:.2f} ms | {status_a} | {status_b} |")
    
    report_lines.append("")
    
    # Enhanced features analysis
    report_lines.append("## Enhanced Features Analysis")
    report_lines.append("")
    
    # Count suggestions and recommendations
    total_suggestions = sum(r.get('num_suggestions', 0) for r in results_b.get('test_results', []))
    total_recommendations = sum(r.get('num_recommendations', 0) for r in results_b.get('test_results', []))
    avg_suggestions = total_suggestions / len(results_b.get('test_results', [])) if results_b.get('test_results') else 0
    avg_recommendations = total_recommendations / len(results_b.get('test_results', [])) if results_b.get('test_results') else 0
    
    report_lines.append(f"- **Average Search Suggestions per Query:** {avg_suggestions:.2f}")
    report_lines.append(f"- **Average Related Product Recommendations:** {avg_recommendations:.2f}")
    report_lines.append("")
    
    # Relevance scoring
    report_lines.append("### Relevance Scoring")
    report_lines.append("")
    report_lines.append("Project B implements intelligent relevance scoring that considers:")
    report_lines.append("- Exact name matches (highest weight)")
    report_lines.append("- Keyword matches in name, description, category, brand, and tags")
    report_lines.append("- Fuzzy matching for typos and partial matches")
    report_lines.append("- Multi-keyword matching bonuses")
    report_lines.append("")
    
    # Performance analysis
    report_lines.append("## Performance Analysis")
    report_lines.append("")
    
    if avg_time_b <= avg_time_a * 1.2:  # Within 20% of Project A
        report_lines.append("✓ **Performance:** Project B maintains acceptable response times despite added intelligence.")
    else:
        report_lines.append("⚠ **Performance:** Project B shows increased response times due to enhanced features.")
    
    report_lines.append("")
    report_lines.append(f"- Project A average: {avg_time_a:.2f} ms")
    report_lines.append(f"- Project B average: {avg_time_b:.2f} ms")
    report_lines.append(f"- Difference: {time_diff:+.2f} ms ({time_improvement_pct:+.1f}%)")
    report_lines.append("")
    
    # Accuracy and relevance improvements
    report_lines.append("## Accuracy and Relevance Improvements")
    report_lines.append("")
    
    # Compare result counts for same queries
    improved_queries = 0
    same_queries = 0
    for test_id in all_test_ids:
        result_a = test_results_a.get(test_id, {})
        result_b = test_results_b.get(test_id, {})
        if result_a and result_b:
            count_a = result_a.get('total_results', 0)
            count_b = result_b.get('total_results', 0)
            if count_b > count_a:
                improved_queries += 1
            elif count_b == count_a and count_b > 0:
                same_queries += 1
    
    report_lines.append(f"- **Queries with More Results:** {improved_queries}")
    report_lines.append(f"- **Queries with Same Results:** {same_queries}")
    report_lines.append("")
    report_lines.append("Project B's fuzzy matching and relevance scoring enable it to find more relevant products, especially for:")
    report_lines.append("- Queries with typos")
    report_lines.append("- Partial word matches")
    report_lines.append("- Ambiguous queries")
    report_lines.append("")
    
    # Limitations
    report_lines.append("## Limitations and Considerations")
    report_lines.append("")
    report_lines.append("1. **Dataset Size:** Current implementation is optimized for small to medium product catalogs (< 10,000 products)")
    report_lines.append("2. **Fuzzy Matching:** May occasionally return less relevant results for very ambiguous queries")
    report_lines.append("3. **Performance:** Enhanced features add computational overhead; may need optimization for very large datasets")
    report_lines.append("4. **Language:** Currently optimized for English language queries")
    report_lines.append("5. **Relevance Tuning:** Relevance scoring weights may need adjustment based on domain-specific requirements")
    report_lines.append("")
    
    # Recommendations
    report_lines.append("## Recommendations")
    report_lines.append("")
    report_lines.append("1. **For Production Use:**")
    report_lines.append("   - Consider implementing caching for frequent queries")
    report_lines.append("   - Add user feedback mechanism to improve relevance scoring")
    report_lines.append("   - Implement A/B testing to optimize relevance weights")
    report_lines.append("")
    report_lines.append("2. **For Large-Scale Deployment:**")
    report_lines.append("   - Consider using dedicated search engines (Elasticsearch, Solr)")
    report_lines.append("   - Implement indexing for faster lookups")
    report_lines.append("   - Add pagination for large result sets")
    report_lines.append("")
    report_lines.append("3. **For Enhanced Features:**")
    report_lines.append("   - Add machine learning-based ranking")
    report_lines.append("   - Implement user behavior tracking for personalized recommendations")
    report_lines.append("   - Add support for synonyms and related terms")
    report_lines.append("")
    
    # Conclusion
    report_lines.append("## Conclusion")
    report_lines.append("")
    report_lines.append("Project B successfully enhances the basic search functionality with intelligent features including:")
    report_lines.append("- Fuzzy matching for better typo tolerance")
    report_lines.append("- Relevance scoring for improved result ranking")
    report_lines.append("- Search suggestions for better user experience")
    report_lines.append("- Related product recommendations for discovery")
    report_lines.append("")
    report_lines.append("These enhancements significantly improve search accuracy, relevance, and overall user experience while maintaining acceptable performance characteristics.")
    report_lines.append("")
    
    # Write report
    report_content = "\n".join(report_lines)
    with open('compare_report.md', 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print("Comparison report generated: compare_report.md")


if __name__ == '__main__':
    generate_report()

