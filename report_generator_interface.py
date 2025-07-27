#!/usr/bin/env python3
"""
Simple Interface for AI Report Generator
"""

import sys
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

def main():
    """Main interface for AI report generator"""
    print("🤖 AI AGENT REPORT GENERATOR")
    print("=" * 50)
    print("Follows the exact playbook for creating concise, safety-checked reference guides")
    print("=" * 50)
    
    try:
        from ai_report_generator import AIReportGenerator
        
        # Get user input
        print("\n📝 Enter your topic:")
        topic = input("Topic (e.g., mudra, pranayama, meditation): ").strip()
        
        if not topic:
            print("❌ Topic cannot be empty!")
            return
        
        print("\n👥 Enter your audience (optional):")
        audience = input("Audience (e.g., Students, Teachers & Therapists): ").strip()
        
        print("\n📏 Choose output length:")
        print("1. Short (3-day plan)")
        print("2. Standard (7-day plan) - Recommended")
        print("3. Long (30-day plan)")
        
        length_choice = input("Choose (1-3): ").strip()
        length_map = {"1": "short", "2": "standard", "3": "long"}
        length = length_map.get(length_choice, "standard")
        
        print("\n⚠️  Safety constraints (optional):")
        constraints_input = input("Constraints (comma-separated): ").strip()
        constraints = [c.strip() for c in constraints_input.split(",")] if constraints_input else None
        
        print(f"\n🚀 Generating report for: {topic}")
        print(f"Audience: {audience or 'Default'}")
        print(f"Length: {length}")
        print(f"Constraints: {constraints or 'None'}")
        
        # Generate report
        generator = AIReportGenerator()
        filepath = generator.generate_report(topic, audience, length, constraints)
        
        print(f"\n✅ Report generated successfully!")
        print(f"📄 File: {filepath}")
        
        # Show preview
        print(f"\n📖 Preview:")
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            lines = content.split("\n")
            for i, line in enumerate(lines[:20]):  # Show first 20 lines
                print(line)
            if len(lines) > 20:
                print("...")
        
        print(f"\n🎉 Report generation complete!")
        print(f"📁 Check the 'ai_report_outputs' folder for your report.")
        
    except ImportError as e:
        print(f"❌ Error importing AI Report Generator: {e}")
        print("Make sure ai_report_generator.py is in the same directory.")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 