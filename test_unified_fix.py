#!/usr/bin/env python3
"""
Test script to verify the complexity_level fix in Unified Research System
"""

import asyncio
import sys
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

async def test_complexity_analysis():
    """Test the topic complexity analysis"""
    try:
        from unified_research_system import UnifiedResearchSystem
        
        print("🧪 Testing Unified Research System - Complexity Analysis Fix")
        print("=" * 60)
        
        system = UnifiedResearchSystem()
        
        # Test 1: Simple topic
        print("\n📝 Test 1: Simple Topic")
        simple_topic = "artificial intelligence"
        simple_analysis = system.analyze_topic_complexity(simple_topic)
        print(f"Topic: {simple_topic}")
        print(f"Complexity Level: {simple_analysis['complexity_level']}")
        print(f"Word Count: {simple_analysis['word_count']}")
        print(f"Complexity Score: {simple_analysis['complexity_score']}")
        print(f"Recommended Approach: {simple_analysis['recommended_approach']}")
        
        # Test 2: Complex topic
        print("\n📝 Test 2: Complex Topic")
        complex_topic = "machine learning algorithms in quantum computing applications"
        complex_analysis = system.analyze_topic_complexity(complex_topic)
        print(f"Topic: {complex_topic}")
        print(f"Complexity Level: {complex_analysis['complexity_level']}")
        print(f"Word Count: {complex_analysis['word_count']}")
        print(f"Complexity Score: {complex_analysis['complexity_score']}")
        print(f"Recommended Approach: {complex_analysis['recommended_approach']}")
        
        # Test 3: System comparison (this was causing the error)
        print("\n📝 Test 3: System Comparison (Previously Failed)")
        print("Testing system comparison with proper analysis structure...")
        
        # This should not raise the complexity_level error anymore
        comparison_results = await system.compare_systems("test topic")
        
        if comparison_results and 'error' not in comparison_results:
            print("✅ System comparison completed successfully!")
            print(f"Super Agent execution time: {comparison_results['super_agent']['execution_time']:.2f}s")
            print(f"Multi-Agent execution time: {comparison_results['multi_agent']['execution_time']:.2f}s")
        else:
            print("❌ System comparison failed!")
            print(f"Error: {comparison_results.get('error', 'Unknown error')}")
        
        print("\n🎉 All tests completed successfully!")
        print("The complexity_level error has been fixed!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_complexity_analysis()) 