import sys
import os
import json
from datetime import datetime
from simple_comprehensive import (
    get_topic_complete_data,
    print_complete_data,
    save_complete_data,
)
from pdf_generator import PDFGenerator
from kimi_research_agent import KimiResearchAgent


def clear_screen():
    """Clear the terminal screen"""
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    """Print the application banner"""
    print("=" * 70)
    print("🤖 SUPER RESEARCH AGENT - Powered by Kimi-K2 & Tavily")
    print("=" * 70)
    print("Advanced web extraction, AI analysis, and comprehensive reporting")
    print("=" * 70)


def main_menu():
    """Main menu interface for super agent"""
    while True:
        clear_screen()
        print_banner()

        print("\n🎯 SUPER AGENT CAPABILITIES:")
        print("1. 🔬 Deep Research with Kimi-K2 AI Analysis")
        print("2. 📊 Quick Web Extraction & PDF Generation")
        print("3. 📝 Convert Text to Professional PDF")
        print("4. 📈 Convert Existing Data to Advanced Reports")
        print("5. 🧠 AI-Powered Content Analysis")
        print("6. 📁 Research Data Management")
        print("7. ⚙️  Agent Settings & Configuration")
        print("8. ❓ Help & Documentation")
        print("9. 🚪 Exit")

        choice = input("\nEnter your choice (1-9): ").strip()

        if choice == "1":
            deep_research_with_kimi()
        elif choice == "2":
            quick_research_and_pdf()
        elif choice == "3":
            text_to_pdf()
        elif choice == "4":
            existing_data_to_advanced_reports()
        elif choice == "5":
            ai_content_analysis()
        elif choice == "6":
            research_data_management()
        elif choice == "7":
            agent_settings()
        elif choice == "8":
            show_help()
        elif choice == "9":
            print("\n👋 Thank you for using the Super Research Agent!")
            sys.exit(0)
        else:
            print("\n❌ Invalid choice. Please try again.")
            input("Press Enter to continue...")


def deep_research_with_kimi():
    """Perform deep research using Kimi-K2 AI"""
    clear_screen()
    print_banner()

    print("\n🧠 DEEP RESEARCH WITH KIMI-K2 AI")
    print("=" * 50)

    # Get topic
    topic = input("Enter research topic: ").strip()
    if not topic:
        print("❌ Topic cannot be empty!")
        input("Press Enter to continue...")
        return

    # Get number of sites
    try:
        max_sites = int(
            input("Number of sites to analyze (default 8): ").strip() or "8"
        )
        if max_sites < 1 or max_sites > 15:
            max_sites = 8
    except ValueError:
        max_sites = 8

    print(f"\n🚀 Initializing Kimi-K2 AI Agent...")
    print("This may take a few moments to load the model...")

    try:
        # Initialize Kimi agent
        agent = KimiResearchAgent()

        print(f"\n🔬 Starting deep AI analysis of: {topic}")
        print("=" * 50)

        # Perform deep analysis
        analysis = agent.analyze_topic_deep(topic, max_sites)

        if "error" in analysis:
            print(f"❌ Error: {analysis['error']}")
            input("Press Enter to continue...")
            return

        # Display results
        print("\n📊 DEEP ANALYSIS RESULTS:")
        print(f"Topic: {analysis.get('topic')}")
        print(f"Sources analyzed: {len(analysis.get('web_data', {}).get('sites', []))}")
        print(
            f"Research questions generated: {len(analysis.get('research_questions', []))}"
        )
        print(f"Visualizations created: {len(analysis.get('visualizations', {}))}")

        # Show executive summary
        print(f"\n📋 EXECUTIVE SUMMARY:")
        print(analysis.get("summary", "No summary available"))

        # Ask for output options
        print("\n📄 OUTPUT OPTIONS:")
        print("1. Save as JSON only")
        print("2. Generate AI Research Report PDF")
        print("3. Both JSON and PDF")
        print("4. Skip saving")

        output_choice = input("Enter choice (1-4): ").strip()

        if output_choice in ["1", "3"]:
            filename = f"{topic.replace(' ', '_')}_deep_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            print(f"✅ Deep analysis saved to: {filename}")

        if output_choice in ["2", "3"]:
            pdf_file = agent.create_research_report(analysis)
            print(f"✅ AI Research Report PDF: {pdf_file}")

        print(f"\n✅ Deep research complete for: {topic}")

    except Exception as e:
        print(f"❌ Error during deep research: {e}")
        print("Make sure you have the required dependencies installed.")

    input("\nPress Enter to continue...")


def quick_research_and_pdf():
    """Quick research and PDF generation"""
    clear_screen()
    print_banner()

    print("\n📊 QUICK RESEARCH & PDF GENERATION")
    print("=" * 50)

    # Get topic
    topic = input("Enter research topic: ").strip()
    if not topic:
        print("❌ Topic cannot be empty!")
        input("Press Enter to continue...")
        return

    # Get number of sites
    try:
        max_sites = int(input("Number of sites (default 6): ").strip() or "6")
        if max_sites < 1 or max_sites > 15:
            max_sites = 6
    except ValueError:
        max_sites = 6

    print(f"\n🔍 Researching '{topic}' from {max_sites} sites...")

    # Get data
    data = get_topic_complete_data(topic, max_sites)

    if "error" in data:
        print(f"❌ Error during research: {data['error']}")
        input("Press Enter to continue...")
        return

    # Show results
    print_complete_data(data)

    # Ask for output options
    print("\n📄 OUTPUT OPTIONS:")
    print("1. Save as JSON only")
    print("2. Generate PDF only")
    print("3. Both JSON and PDF")
    print("4. Skip saving")

    output_choice = input("Enter choice (1-4): ").strip()

    if output_choice in ["1", "3"]:
        save_complete_data(data)
        print("✅ Data saved as JSON")

    if output_choice in ["2", "3"]:
        pdf_choice = input("\n📄 PDF type: 1=Full report, 2=Summary, 3=Both: ").strip()

        generator = PDFGenerator()

        if pdf_choice in ["1", "3"]:
            full_pdf = generator.create_web_extraction_pdf(data)
            print(f"✅ Full report PDF: {full_pdf}")

        if pdf_choice in ["2", "3"]:
            summary_pdf = generator.create_summary_pdf(data)
            print(f"✅ Summary PDF: {summary_pdf}")

        if pdf_choice not in ["1", "2", "3"]:
            print("⚠️  Creating both PDFs...")
            full_pdf = generator.create_web_extraction_pdf(data)
            summary_pdf = generator.create_summary_pdf(data)
            print(f"✅ Full report PDF: {full_pdf}")
            print(f"✅ Summary PDF: {summary_pdf}")

    print(f"\n✅ Research complete for: {topic}")
    input("\nPress Enter to continue...")


def text_to_pdf():
    """Convert text input to PDF"""
    clear_screen()
    print_banner()

    print("\n📝 TEXT TO PDF CONVERTER")
    print("=" * 40)

    # Get text input
    print("Enter your text content (press Enter twice to finish):")
    lines = []
    while True:
        line = input()
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)

    text = "\n".join(lines[:-1])  # Remove the last empty line

    if not text.strip():
        print("❌ No text provided!")
        input("Press Enter to continue...")
        return

    # Get title
    title = input("\nEnter document title (optional): ").strip() or "Document"

    # Get filename
    filename = input("Enter PDF filename (optional): ").strip()

    # Generate PDF
    try:
        generator = PDFGenerator()
        pdf_file = generator.create_text_to_pdf(text, title, filename)
        print(f"\n✅ PDF created successfully: {pdf_file}")
    except Exception as e:
        print(f"\n❌ Error creating PDF: {e}")

    input("\nPress Enter to continue...")


def existing_data_to_advanced_reports():
    """Convert existing data to advanced reports"""
    clear_screen()
    print_banner()

    print("\n📈 CONVERT EXISTING DATA TO ADVANCED REPORTS")
    print("=" * 50)

    # Find JSON files
    json_files = [f for f in os.listdir(".") if f.endswith("_complete_data.json")]

    if not json_files:
        print("No JSON data files found in current directory.")
        input("Press Enter to continue...")
        return

    print("Available JSON files:")
    for i, filename in enumerate(json_files, 1):
        file_size = os.path.getsize(filename)
        print(f"{i}. {filename} ({file_size:,} bytes)")

    try:
        choice = int(input(f"\nSelect file (1-{len(json_files)}): ").strip())
        if choice < 1 or choice > len(json_files):
            print("❌ Invalid choice!")
            input("Press Enter to continue...")
            return

        filename = json_files[choice - 1]

        # Load data
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Show data preview
        print(f"\n📄 Data Preview:")
        print(f"Topic: {data.get('topic', 'Unknown')}")
        print(f"Sites: {len(data.get('sites', []))}")
        print(f"Total Content: {data.get('total_content_length', 0):,} characters")

        # Ask for report type
        print("\n📄 Choose Report Type:")
        print("1. Standard PDF Report")
        print("2. AI-Enhanced Analysis (requires Kimi-K2)")
        print("3. Both")

        report_choice = input("Enter choice (1-3): ").strip()

        generator = PDFGenerator()

        if report_choice in ["1", "3"]:
            # Standard PDF
            pdf_choice = input("PDF type: 1=Full report, 2=Summary, 3=Both: ").strip()

            if pdf_choice in ["1", "3"]:
                full_pdf = generator.create_web_extraction_pdf(data)
                print(f"✅ Full report PDF: {full_pdf}")

            if pdf_choice in ["2", "3"]:
                summary_pdf = generator.create_summary_pdf(data)
                print(f"✅ Summary PDF: {summary_pdf}")

        if report_choice in ["2", "3"]:
            # AI-Enhanced Analysis
            print("\n🧠 Initializing Kimi-K2 for AI analysis...")
            try:
                agent = KimiResearchAgent()
                analysis = agent.analyze_topic_deep(
                    data.get("topic", "Unknown"), len(data.get("sites", []))
                )
                ai_pdf = agent.create_research_report(analysis)
                print(f"✅ AI-Enhanced Report: {ai_pdf}")
            except Exception as e:
                print(f"❌ AI analysis failed: {e}")

        if report_choice not in ["1", "2", "3"]:
            print("⚠️  Creating standard reports...")
            full_pdf = generator.create_web_extraction_pdf(data)
            summary_pdf = generator.create_summary_pdf(data)
            print(f"✅ Full report PDF: {full_pdf}")
            print(f"✅ Summary PDF: {summary_pdf}")

    except (ValueError, IndexError):
        print("❌ Invalid choice!")
    except Exception as e:
        print(f"❌ Error: {e}")

    input("\nPress Enter to continue...")


def ai_content_analysis():
    """AI-powered content analysis"""
    clear_screen()
    print_banner()

    print("\n🧠 AI CONTENT ANALYSIS")
    print("=" * 40)

    print("This feature provides AI-powered analysis of content.")
    print("Choose an option:")
    print("1. Analyze existing research data")
    print("2. Analyze custom text input")
    print("3. Back to main menu")

    choice = input("Enter choice (1-3): ").strip()

    if choice == "1":
        # Analyze existing data
        json_files = [f for f in os.listdir(".") if f.endswith("_complete_data.json")]

        if not json_files:
            print("No JSON data files found.")
            input("Press Enter to continue...")
            return

        print("Available files:")
        for i, filename in enumerate(json_files, 1):
            print(f"{i}. {filename}")

        try:
            file_choice = int(input(f"Select file (1-{len(json_files)}): ").strip())
            if 1 <= file_choice <= len(json_files):
                filename = json_files[file_choice - 1]

                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)

                print(f"\n🧠 Analyzing: {data.get('topic', 'Unknown')}")

                # Initialize Kimi agent for analysis
                agent = KimiResearchAgent()
                analysis = agent.analyze_topic_deep(
                    data.get("topic", "Unknown"), len(data.get("sites", []))
                )

                print(f"\n📊 AI Analysis Complete!")
                print(
                    f"Research questions: {len(analysis.get('research_questions', []))}"
                )
                print(f"Insights generated: {len(analysis.get('insights', {}))}")
                print(f"Visualizations: {len(analysis.get('visualizations', {}))}")

                # Save AI analysis
                ai_filename = f"{data.get('topic', 'analysis').replace(' ', '_')}_ai_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(ai_filename, "w", encoding="utf-8") as f:
                    json.dump(analysis, f, indent=2, ensure_ascii=False)
                print(f"✅ AI analysis saved to: {ai_filename}")

        except (ValueError, IndexError):
            print("❌ Invalid choice!")

    elif choice == "2":
        # Analyze custom text
        print("\nEnter text to analyze (press Enter twice to finish):")
        lines = []
        while True:
            line = input()
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)

        text = "\n".join(lines[:-1])

        if text.strip():
            print("\n🧠 Analyzing custom text...")
            try:
                agent = KimiResearchAgent()

                # Create a simple analysis prompt
                prompt = f"""
                Analyze the following text and provide:
                1. Key themes and topics
                2. Main insights
                3. Sentiment analysis
                4. Recommendations
                
                Text: {text[:2000]}
                """

                analysis = agent.generate_response(prompt)
                print(f"\n📊 AI Analysis Results:")
                print(analysis)

            except Exception as e:
                print(f"❌ Analysis failed: {e}")

    input("\nPress Enter to continue...")


def research_data_management():
    """Manage research data files"""
    clear_screen()
    print_banner()

    print("\n📁 RESEARCH DATA MANAGEMENT")
    print("=" * 50)

    # Find all relevant files
    json_files = [f for f in os.listdir(".") if f.endswith("_complete_data.json")]
    pdf_files = [f for f in os.listdir(".") if f.endswith(".pdf")]
    ai_files = [
        f for f in os.listdir(".") if "ai_analysis" in f and f.endswith(".json")
    ]

    print(f"📊 File Summary:")
    print(f"Research data files: {len(json_files)}")
    print(f"PDF reports: {len(pdf_files)}")
    print(f"AI analysis files: {len(ai_files)}")

    print(f"\n📄 Available Actions:")
    print("1. View research data files")
    print("2. View PDF reports")
    print("3. View AI analysis files")
    print("4. Clean up old files")
    print("5. Export data summary")
    print("6. Back to main menu")

    choice = input("Enter choice (1-6): ").strip()

    if choice == "1":
        view_files(json_files, "Research Data Files")
    elif choice == "2":
        view_files(pdf_files, "PDF Reports")
    elif choice == "3":
        view_files(ai_files, "AI Analysis Files")
    elif choice == "4":
        cleanup_files()
    elif choice == "5":
        export_data_summary(json_files, pdf_files, ai_files)

    input("\nPress Enter to continue...")


def view_files(files, title):
    """View file details"""
    print(f"\n📄 {title}:")
    print("=" * 50)

    if not files:
        print("No files found.")
        return

    for i, filename in enumerate(files, 1):
        file_size = os.path.getsize(filename)
        file_time = datetime.fromtimestamp(os.path.getmtime(filename)).strftime(
            "%Y-%m-%d %H:%M"
        )
        print(f"{i}. {filename}")
        print(f"   Size: {file_size:,} bytes | Modified: {file_time}")


def cleanup_files():
    """Clean up old files"""
    print("\n🧹 File Cleanup")
    print("=" * 30)

    # Find files older than 30 days
    import time

    current_time = time.time()
    thirty_days = 30 * 24 * 60 * 60

    old_files = []
    for filename in os.listdir("."):
        if filename.endswith((".json", ".pdf")) and "complete_data" in filename:
            file_time = os.path.getmtime(filename)
            if current_time - file_time > thirty_days:
                old_files.append(filename)

    if not old_files:
        print("No old files found to clean up.")
        return

    print(f"Found {len(old_files)} old files:")
    for filename in old_files:
        print(f"- {filename}")

    confirm = input("\nDelete these files? (y/n): ").strip().lower()
    if confirm == "y":
        for filename in old_files:
            try:
                os.remove(filename)
                print(f"✅ Deleted: {filename}")
            except Exception as e:
                print(f"❌ Failed to delete {filename}: {e}")


def export_data_summary(json_files, pdf_files, ai_files):
    """Export data summary"""
    print("\n📊 Exporting Data Summary")
    print("=" * 30)

    summary = {
        "timestamp": datetime.now().isoformat(),
        "total_files": len(json_files) + len(pdf_files) + len(ai_files),
        "research_data_files": len(json_files),
        "pdf_reports": len(pdf_files),
        "ai_analysis_files": len(ai_files),
        "file_details": {
            "json_files": [{"name": f, "size": os.path.getsize(f)} for f in json_files],
            "pdf_files": [{"name": f, "size": os.path.getsize(f)} for f in pdf_files],
            "ai_files": [{"name": f, "size": os.path.getsize(f)} for f in ai_files],
        },
    }

    filename = f"research_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"✅ Data summary exported to: {filename}")


def agent_settings():
    """Agent settings and configuration"""
    clear_screen()
    print_banner()

    print("\n⚙️  AGENT SETTINGS & CONFIGURATION")
    print("=" * 50)

    print("Current Settings:")
    print("1. Model: Kimi-K2-Instruct (moonshotai/Kimi-K2-Instruct)")
    print("2. Web Extraction: Tavily API")
    print("3. PDF Generation: ReportLab")
    print("4. Analysis: NLTK, TextBlob, Matplotlib")

    print(f"\n📋 Configuration Options:")
    print("1. View current configuration")
    print("2. Test model connectivity")
    print("3. Check dependencies")
    print("4. Back to main menu")

    choice = input("Enter choice (1-4): ").strip()

    if choice == "1":
        print("\n📋 Current Configuration:")
        print("=" * 30)
        print("Model: moonshotai/Kimi-K2-Instruct")
        print("Device: CUDA (if available) / CPU")
        print("Max sites: 15")
        print("PDF format: A4")
        print("Analysis depth: Deep")

    elif choice == "2":
        print("\n🔍 Testing model connectivity...")
        try:
            agent = KimiResearchAgent()
            test_response = agent.generate_response(
                "Hello, this is a test.", max_length=50
            )
            print(f"✅ Model test successful: {test_response[:100]}...")
        except Exception as e:
            print(f"❌ Model test failed: {e}")

    elif choice == "3":
        print("\n📦 Checking dependencies...")
        try:
            import transformers
            import torch
            import nltk
            import matplotlib
            import pandas

            print("✅ All dependencies available")
        except ImportError as e:
            print(f"❌ Missing dependency: {e}")

    input("\nPress Enter to continue...")


def show_help():
    """Show help information"""
    clear_screen()
    print_banner()

    print("\n❓ SUPER AGENT HELP & DOCUMENTATION")
    print("=" * 60)
    print(
        """
🤖 SUPER RESEARCH AGENT CAPABILITIES:

🔬 DEEP RESEARCH WITH KIMI-K2 AI:
   • Advanced AI-powered content analysis
   • Automatic research question generation
   • Sentiment analysis and insights
   • Data visualizations and charts
   • Executive summaries for business leaders

📊 QUICK RESEARCH & PDF GENERATION:
   • Fast web extraction from multiple sources
   • Professional PDF report generation
   • JSON data storage for later analysis
   • Summary and detailed report options

📝 TEXT TO PDF CONVERTER:
   • Convert any text content to professional PDFs
   • Custom formatting and styling
   • Multiple paragraph support

📈 ADVANCED REPORTS:
   • Convert existing data to AI-enhanced reports
   • Multiple report types and formats
   • Professional business presentations

🧠 AI CONTENT ANALYSIS:
   • Analyze existing research data with AI
   • Custom text analysis and insights
   • Sentiment and theme detection

📁 RESEARCH DATA MANAGEMENT:
   • Browse and manage research files
   • Clean up old files automatically
   • Export data summaries
   • File organization and tracking

⚙️  AGENT SETTINGS:
   • Model configuration and testing
   • Dependency management
   • Performance optimization

📄 OUTPUT FORMATS:
   • JSON data files with complete analysis
   • Professional PDF reports
   • Data visualizations (PNG)
   • Executive summaries
   • AI-enhanced insights

🚀 ADVANCED FEATURES:
   • Multi-source web extraction
   • AI-powered content analysis
   • Automatic visualization generation
   • Sentiment analysis
   • Research question generation
   • Executive summary creation
   • Professional report formatting
    """
    )

    input("Press Enter to continue...")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
