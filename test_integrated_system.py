#!/usr/bin/env python3
"""
Test Integrated Research System
Demonstrates the complete research workflow with AI report generation
"""

import asyncio
import sys
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

async def test_integrated_system():
    """Test the integrated research system"""
    print("🧪 TESTING INTEGRATED RESEARCH SYSTEM")
    print("=" * 60)
    
    try:
        from integrated_research_system import IntegratedResearchSystem
        
        # Initialize the system
        system = IntegratedResearchSystem()
        
        # Test topics of different complexity levels
        test_topics = [
            "yoga",  # Simple topic
            "machine learning applications",  # Medium complexity
            "artificial intelligence in healthcare trends"  # Complex topic
        ]
        
        for i, topic in enumerate(test_topics, 1):
            print(f"\n🔬 TEST {i}: {topic.upper()}")
            print("-" * 40)
            
            # Analyze topic complexity
            analysis = system.analyze_topic_complexity(topic)
            print(f"Topic Analysis:")
            print(f"  Words: {analysis['word_count']}")
            print(f"  Complexity Score: {analysis['complexity_score']}")
            print(f"  Complexity Level: {analysis['complexity_level']}")
            print(f"  Recommended Approach: {analysis['recommended_approach'].replace('_', ' ').title()}")
            
            # Perform integrated research
            print(f"\n🚀 Performing integrated research...")
            results = await system.perform_integrated_research(topic)
            
            if results and 'error' not in results:
                print(f"✅ Research completed successfully!")
                print(f"Approach used: {results.get('research_approach', 'Unknown')}")
                print(f"System used: {results.get('system_used', 'Unknown')}")
                
                # Show AI reports
                if 'ai_reports' in results:
                    print(f"\n🤖 AI Reports Generated:")
                    for report_type, filepath in results['ai_reports'].items():
                        if report_type != 'error':
                            print(f"  📄 {report_type.replace('_', ' ').title()}: {filepath}")
                
                # Show insights for complex topics
                if analysis['complexity_level'] in ['medium', 'complex']:
                    if results.get('research_approach') == 'hybrid':
                        combined = results.get('combined_insights', {})
                        if combined.get('key_insights'):
                            print(f"\n💡 Key Insights:")
                            for insight in combined['key_insights'][:3]:
                                print(f"  • {insight}")
                    else:
                        insights = results.get('insights', {})
                        if insights.get('key_insights'):
                            print(f"\n💡 Key Insights:")
                            for insight in insights['key_insights'][:3]:
                                print(f"  • {insight}")
            else:
                print(f"❌ Research failed for topic: {topic}")
            
            print("\n" + "=" * 60)
        
        print(f"\n🎉 INTEGRATED SYSTEM TEST COMPLETED!")
        print(f"Check the 'integrated_outputs' directory for generated files.")
        
    except ImportError as e:
        print(f"❌ Error importing Integrated Research System: {e}")
        print("Make sure all required files are in the same directory.")
    except Exception as e:
        print(f"❌ Error testing Integrated Research System: {e}")
        import traceback
        traceback.print_exc()

async def test_smart_research():
    """Test smart research with auto-selection"""
    print("\n🧪 TESTING SMART RESEARCH (AUTO-SELECTION)")
    print("=" * 60)
    
    try:
        from integrated_research_system import IntegratedResearchSystem
        
        system = IntegratedResearchSystem()
        
        # Test with a complex topic to see hybrid approach
        topic = "blockchain technology in supply chain management"
        
        print(f"Topic: {topic}")
        print("This should trigger hybrid research approach...")
        
        results = await system.perform_integrated_research(topic)
        
        if results and 'error' not in results:
            print(f"✅ Smart research completed!")
            print(f"Approach: {results.get('research_approach', 'Unknown')}")
            print(f"System: {results.get('system_used', 'Unknown')}")
            
            # Show hybrid results
            if results.get('research_approach') == 'hybrid':
                comparison = results.get('performance_comparison', {})
                print(f"\n📊 Performance Comparison:")
                print(f"  Super Agent Sites: {comparison.get('super_agent', {}).get('sites', 0)}")
                print(f"  Multi-Agent Sites: {comparison.get('multi_agent', {}).get('sites', 0)}")
                print(f"  Recommendation: {comparison.get('recommendation', 'N/A')}")
            
            # Show AI reports
            if 'ai_reports' in results:
                print(f"\n🤖 Generated Reports:")
                for report_type, filepath in results['ai_reports'].items():
                    if report_type != 'error':
                        print(f"  📄 {report_type.replace('_', ' ').title()}")
        else:
            print(f"❌ Smart research failed!")
        
    except Exception as e:
        print(f"❌ Error testing smart research: {e}")

async def test_ai_report_generation():
    """Test standalone AI report generation"""
    print("\n🧪 TESTING AI REPORT GENERATION")
    print("=" * 60)
    
    try:
        from ai_report_generator import AIReportGenerator
        
        generator = AIReportGenerator()
        
        # Test different audiences and topics
        test_cases = [
            {
                'topic': 'meditation techniques',
                'audience': 'Beginners',
                'length': 'standard'
            },
            {
                'topic': 'quantum computing',
                'audience': 'Advanced Practitioners & Researchers',
                'length': 'comprehensive'
            }
        ]
        
        for i, case in enumerate(test_cases, 1):
            print(f"\n📝 Test Case {i}: {case['topic']} for {case['audience']}")
            print("-" * 40)
            
            report = generator.generate_report(
                topic=case['topic'],
                audience=case['audience'],
                length=case['length'],
                constraints=None
            )
            
            if report:
                print(f"✅ Report generated successfully!")
                print(f"File: {report}")
                
                # Show first few lines
                try:
                    with open(report, 'r', encoding='utf-8') as f:
                        lines = f.readlines()[:10]
                        print(f"\n📄 Preview (first 10 lines):")
                        for line in lines:
                            print(f"  {line.rstrip()}")
                except Exception as e:
                    print(f"Could not read file: {e}")
            else:
                print(f"❌ Report generation failed!")
        
    except Exception as e:
        print(f"❌ Error testing AI report generation: {e}")

def main():
    """Main test function"""
    print("🚀 INTEGRATED RESEARCH SYSTEM - COMPREHENSIVE TEST")
    print("=" * 80)
    print("Testing complete research workflow with AI report generation")
    print("=" * 80)
    
    async def run_all_tests():
        await test_integrated_system()
        await test_smart_research()
        await test_ai_report_generation()
        
        print(f"\n🎉 ALL TESTS COMPLETED!")
        print(f"Check the output directories for generated files:")
        print(f"  • integrated_outputs/ - Integrated system outputs")
        print(f"  • ai_report_outputs/ - AI report generator outputs")
    
    try:
        asyncio.run(run_all_tests())
    except KeyboardInterrupt:
        print("\n\n⏹️  Testing interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 