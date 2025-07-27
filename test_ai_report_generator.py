#!/usr/bin/env python3
"""
Test script for AI Report Generator
Demonstrates the system with different topics
"""

import sys
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

def test_ai_report_generator():
    """Test the AI report generator with different topics"""
    try:
        from ai_report_generator import AIReportGenerator
        
        print("🧪 Testing AI Report Generator")
        print("=" * 50)
        
        generator = AIReportGenerator()
        
        # Test topics
        test_cases = [
            {
                "topic": "mudra",
                "audience": "Students, Teachers & Therapists",
                "length": "standard",
                "constraints": None
            },
            {
                "topic": "pranayama", 
                "audience": "Yoga Practitioners",
                "length": "short",
                "constraints": ["pregnancy", "hypertension"]
            },
            {
                "topic": "meditation",
                "audience": "Beginners",
                "length": "standard", 
                "constraints": None
            }
        ]
        
        generated_files = []
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📝 Test Case {i}: {test_case['topic'].title()}")
            print(f"Audience: {test_case['audience']}")
            print(f"Length: {test_case['length']}")
            print(f"Constraints: {test_case['constraints']}")
            
            try:
                filepath = generator.generate_report(
                    test_case["topic"],
                    test_case["audience"], 
                    test_case["length"],
                    test_case["constraints"]
                )
                generated_files.append(filepath)
                print(f"✅ Generated: {filepath}")
                
            except Exception as e:
                print(f"❌ Failed to generate report: {e}")
        
        print(f"\n📊 Test Summary:")
        print(f"Total test cases: {len(test_cases)}")
        print(f"Successfully generated: {len(generated_files)}")
        print(f"Failed: {len(test_cases) - len(generated_files)}")
        
        if generated_files:
            print(f"\n📁 Generated files:")
            for filepath in generated_files:
                print(f"  📄 {filepath}")
        
        print(f"\n🎉 AI Report Generator test completed!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

def test_single_topic():
    """Test with a single topic and show detailed output"""
    try:
        from ai_report_generator import AIReportGenerator
        
        print("🧪 Single Topic Test - Mudra Guide")
        print("=" * 50)
        
        generator = AIReportGenerator()
        
        # Test with mudra topic
        topic = "mudra"
        audience = "Students, Teachers & Therapists"
        
        print(f"Generating report for: {topic}")
        print(f"Audience: {audience}")
        
        filepath = generator.generate_report(topic, audience)
        
        print(f"\n✅ Report generated: {filepath}")
        
        # Show full content
        print(f"\n📖 Full Report Content:")
        print("=" * 50)
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            print(content)
        
        print(f"\n🎉 Single topic test completed!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "single":
        test_single_topic()
    else:
        test_ai_report_generator() 