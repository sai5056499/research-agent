#!/usr/bin/env python3
"""
Super Agent Launcher - Choose your research assistant
"""

import sys
import os
import asyncio
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

def clear_screen():
    """Clear terminal screen"""
    os.system("cls" if os.name == "nt" else "clear")

def print_banner():
    """Print launcher banner"""
    print("=" * 80)
    print("🚀 SUPER AGENT LAUNCHER")
    print("=" * 80)
    print("Choose your AI research assistant")
    print("=" * 80)

def main():
    """Main launcher function"""
    while True:
        clear_screen()
        print_banner()
        
        print("\n🤖 AVAILABLE SYSTEMS:")
        print("1. 🚀 Integrated Research System (Recommended)")
        print("   Complete solution: Research + Analysis + AI Reports")
        print("   • Smart approach selection • Auto AI report generation")
        print("   • Reference guides • Research summaries • Insights reports")
        print()
        print("2. 🔬 Enhanced Super Agent")
        print("   Advanced single agent with comprehensive capabilities")
        print("   • Web extraction • Content analysis • Insight generation")
        print("   • Report creation • Research history • Configuration")
        print()
        print("3. 🤝 Multi-Agent System")
        print("   Specialized agents working together")
        print("   • WebExtractionAgent • ContentAnalysisAgent")
        print("   • InsightGenerationAgent • ReportGenerationAgent")
        print()
        print("4. 🤖 AI Report Generator")
        print("   Standalone AI report generation system")
        print("   • Structured reference guides • Safety-checked content")
        print("   • Professional templates • Multiple output formats")
        print()
        print("5. 📊 Compare Systems")
        print("   View differences between agent systems")
        print()
        print("6. ❓ Help")
        print("   Learn about each system")
        print()
        print("7. 🚪 Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            print("\n🚀 Launching Integrated Research System...")
            try:
                from integrated_research_system import IntegratedResearchSystem
                system = IntegratedResearchSystem()
                asyncio.run(system.run_interactive_mode())
            except ImportError as e:
                print(f"❌ Error importing Integrated Research System: {e}")
                input("Press Enter to continue...")
            except Exception as e:
                print(f"❌ Error running Integrated Research System: {e}")
                input("Press Enter to continue...")
                
        elif choice == "2":
            print("\n🚀 Launching Enhanced Super Agent...")
            try:
                from enhanced_super_agent import EnhancedSuperAgent
                agent = EnhancedSuperAgent()
                asyncio.run(agent.run_interactive_mode())
            except ImportError as e:
                print(f"❌ Error importing Enhanced Super Agent: {e}")
                input("Press Enter to continue...")
            except Exception as e:
                print(f"❌ Error running Enhanced Super Agent: {e}")
                input("Press Enter to continue...")
                
        elif choice == "3":
            print("\n🚀 Launching Multi-Agent System...")
            try:
                from multi_agent_system import MultiAgentSystem
                system = MultiAgentSystem()
                asyncio.run(system.run_interactive_mode())
            except ImportError as e:
                print(f"❌ Error importing Multi-Agent System: {e}")
                input("Press Enter to continue...")
            except Exception as e:
                print(f"❌ Error running Multi-Agent System: {e}")
                input("Press Enter to continue...")
                
        elif choice == "4":
            print("\n🚀 Launching AI Report Generator...")
            try:
                from report_generator_interface import main as run_report_generator
                run_report_generator()
            except ImportError as e:
                print(f"❌ Error importing AI Report Generator: {e}")
                input("Press Enter to continue...")
            except Exception as e:
                print(f"❌ Error running AI Report Generator: {e}")
                input("Press Enter to continue...")
                
        elif choice == "5":
            show_comparison()
            
        elif choice == "6":
            show_help()
            
        elif choice == "7":
            print("\n👋 Thank you for using the Super Agent Launcher!")
            break
            
        else:
            print("\n❌ Invalid choice. Please try again.")
            input("Press Enter to continue...")

def show_comparison():
    """Show comparison between agent systems"""
    print("\n📊 SYSTEM COMPARISON")
    print("=" * 60)
    
    print("\n🔬 ENHANCED SUPER AGENT:")
    print("   ✅ Single powerful agent with all capabilities")
    print("   ✅ Simpler to use and understand")
    print("   ✅ Faster for straightforward research")
    print("   ✅ Lower resource usage")
    print("   ❌ Limited parallel processing")
    print("   ❌ Less specialized expertise")
    
    print("\n🤝 MULTI-AGENT SYSTEM:")
    print("   ✅ Specialized agents for each task")
    print("   ✅ Parallel processing capabilities")
    print("   ✅ More detailed analysis")
    print("   ✅ Better error isolation")
    print("   ❌ More complex to manage")
    print("   ❌ Higher resource usage")
    print("   ❌ Potential coordination overhead")
    
    print("\n🎯 RECOMMENDATIONS:")
    print("   • Use Enhanced Super Agent for: Quick research, simple topics, limited resources")
    print("   • Use Multi-Agent System for: Complex research, detailed analysis, multiple topics")
    
    input("\nPress Enter to continue...")

def show_help():
    """Show help information"""
    print("\n❓ HELP & DOCUMENTATION")
    print("=" * 60)
    
    print("\n🚀 INTEGRATED RESEARCH SYSTEM (Recommended):")
    print("   Complete research solution that combines all capabilities:")
    print("   • Smart approach selection based on topic complexity")
    print("   • Automatic AI report generation (reference guides, summaries, insights)")
    print("   • Hybrid research combining Super Agent and Multi-Agent systems")
    print("   • Professional report templates with safety checks")
    print("   • Comprehensive output management and organization")
    print("   • Best choice for most research needs")
    
    print("\n🔬 ENHANCED SUPER AGENT:")
    print("   A single, powerful AI agent that handles all aspects of research:")
    print("   • Web content extraction from multiple sources")
    print("   • Intelligent content analysis and pattern recognition")
    print("   • Automated insight generation and recommendations")
    print("   • Comprehensive report generation (PDF, JSON, insights)")
    print("   • Research history tracking and management")
    print("   • Configurable capabilities and output options")
    
    print("\n🤝 MULTI-AGENT SYSTEM:")
    print("   Multiple specialized agents working together:")
    print("   • WebExtractionAgent: Handles web content extraction")
    print("   • ContentAnalysisAgent: Analyzes content patterns and quality")
    print("   • InsightGenerationAgent: Generates insights and recommendations")
    print("   • ReportGenerationAgent: Creates comprehensive reports")
    print("   • Each agent specializes in their domain for better results")
    print("   • Parallel processing for faster completion")
    
    print("\n🤖 AI REPORT GENERATOR:")
    print("   Standalone system for creating professional reports:")
    print("   • Structured reference guides with 10-section format")
    print("   • Safety-checked content with automatic disclaimers")
    print("   • Professional templates for different audiences")
    print("   • Multiple output formats (markdown, PDF-ready)")
    print("   • Quality assurance and fact-checking")
    print("   • Ideal for creating educational and reference materials")
    
    print("\n📁 OUTPUTS:")
    print("   All systems generate organized outputs:")
    print("   • PDF reports with numbered sources and analysis")
    print("   • JSON data files for further processing")
    print("   • Insight reports with key findings")
    print("   • Research summaries and recommendations")
    print("   • AI-generated reference guides and educational materials")
    
    print("\n🎯 RECOMMENDATIONS:")
    print("   • Use Integrated Research System for: Complete research workflow")
    print("   • Use Enhanced Super Agent for: Quick research, simple topics")
    print("   • Use Multi-Agent System for: Complex research, detailed analysis")
    print("   • Use AI Report Generator for: Creating educational materials")
    
    print("\n🛠️  REQUIREMENTS:")
    print("   • Python 3.7+")
    print("   • Required packages: requests, beautifulsoup4, newspaper3k")
    print("   • googlesearch-python, duckduckgo-search, reportlab")
    print("   • nltk, textblob")
    
    input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Launcher interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("Press Enter to continue...") 