#!/usr/bin/env python3
"""
Standalone Research Interface - No Django Required
"""

import sys
import os
from pathlib import Path
import json
from datetime import datetime

# Add the tavily directory to the path (it's in the parent directory)
tavily_path = Path(__file__).parent.parent / 'tavily'
sys.path.append(str(tavily_path))

# Also add the current directory for imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

try:
    from alternative_web_extractor import AlternativeWebExtractor
    from enhanced_pdf_generator import EnhancedPDFGenerator
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you're in the correct directory and all dependencies are installed.")
    sys.exit(1)

class StandaloneResearchInterface:
    def __init__(self):
        """Initialize the standalone research interface"""
        self.extractor = AlternativeWebExtractor()
        self.pdf_generator = EnhancedPDFGenerator()
        
        # Create output directories
        self.output_dir = Path("standalone_outputs")
        self.output_dir.mkdir(exist_ok=True)
        
        (self.output_dir / "pdfs").mkdir(exist_ok=True)
        (self.output_dir / "json").mkdir(exist_ok=True)
        (self.output_dir / "reports").mkdir(exist_ok=True)
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system("cls" if os.name == "nt" else "clear")
    
    def print_banner(self):
        """Print the application banner"""
        print("=" * 70)
        print("🔬 STANDALONE RESEARCH ASSISTANT")
        print("=" * 70)
        print("Web extraction, PDF generation, and comprehensive reporting")
        print("=" * 70)
    
    def get_user_input(self):
        """Get research parameters from user"""
        print("\n📝 RESEARCH PARAMETERS")
        print("-" * 30)
        
        # Topic
        topic = input("Enter research topic: ").strip()
        if not topic:
            print("❌ Topic cannot be empty!")
            return None
        
        # Number of sites
        try:
            max_sites = int(input("Number of sites (default 10): ").strip() or "10")
            if max_sites < 1 or max_sites > 20:
                max_sites = 10
        except ValueError:
            max_sites = 10
        
        # Extraction type
        print("\n🔍 EXTRACTION TYPE:")
        print("1. Standalone (Google + DuckDuckGo)")
        print("2. Quick (Google only)")
        print("3. Comprehensive (Multiple engines)")
        
        extraction_choice = input("Choose extraction type (1-3, default 1): ").strip() or "1"
        
        extraction_types = {
            "1": "standalone",
            "2": "quick", 
            "3": "comprehensive"
        }
        extraction_type = extraction_types.get(extraction_choice, "standalone")
        
        # Output options
        print("\n📄 OUTPUT OPTIONS:")
        generate_pdf = input("Generate PDF report? (y/n, default y): ").strip().lower() != "n"
        generate_json = input("Generate JSON data? (y/n, default y): ").strip().lower() != "n"
        include_summary = input("Include research summary? (y/n, default y): ").strip().lower() != "n"
        
        return {
            'topic': topic,
            'max_sites': max_sites,
            'extraction_type': extraction_type,
            'generate_pdf': generate_pdf,
            'generate_json': generate_json,
            'include_summary': include_summary
        }
    
    def perform_research(self, options):
        """Perform the research based on options"""
        print(f"\n🚀 Starting research on: {options['topic']}")
        print(f"📊 Target sites: {options['max_sites']}")
        print(f"🔍 Method: {options['extraction_type']}")
        print("-" * 50)
        
        # Perform extraction
        results = self.extractor.get_topic_data(options['topic'])
        
        if not results or 'error' in results:
            print("❌ Research failed!")
            return None
        
        print(f"\n✅ Research completed!")
        print(f"📈 Sites found: {len(results.get('sites', []))}")
        print(f"📝 Total content: {results.get('total_content_length', 0):,} characters")
        
        return results
    
    def generate_outputs(self, results, options):
        """Generate output files"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        topic_safe = options['topic'].replace(' ', '_').replace('/', '_')[:30]
        
        outputs = []
        
        # Generate JSON
        if options['generate_json']:
            json_filename = f"research_{topic_safe}_{timestamp}.json"
            json_path = self.output_dir / "json" / json_filename
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            outputs.append(f"📄 JSON: {json_path}")
            print(f"✅ JSON saved: {json_path}")
        
        # Generate PDF
        if options['generate_pdf']:
            pdf_filename = f"research_{topic_safe}_{timestamp}.pdf"
            pdf_path = self.output_dir / "pdfs" / pdf_filename
            
            try:
                # Prepare data for PDF
                pdf_data = {
                    'topic': options['topic'],
                    'sites': results.get('sites', []),
                    'total_content_length': results.get('total_content_length', 0),
                    'search_engines_used': results.get('search_engines_used', []),
                    'extraction_methods': results.get('extraction_methods', []),
                    'timestamp': results.get('timestamp', datetime.now().isoformat()),
                    'options': options
                }
                
                self.pdf_generator.create_enhanced_web_extraction_pdf(pdf_data, str(pdf_path))
                outputs.append(f"📄 PDF: {pdf_path}")
                print(f"✅ PDF saved: {pdf_path}")
                
            except Exception as e:
                print(f"❌ PDF generation failed: {e}")
        
        # Generate summary
        if options['include_summary']:
            summary = self.generate_summary(results, options)
            summary_filename = f"summary_{topic_safe}_{timestamp}.json"
            summary_path = self.output_dir / "reports" / summary_filename
            
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            outputs.append(f"📊 Summary: {summary_path}")
            print(f"✅ Summary saved: {summary_path}")
        
        return outputs
    
    def generate_summary(self, results, options):
        """Generate a comprehensive summary"""
        sites = results.get('sites', [])
        
        # Calculate metrics
        total_content = results.get('total_content_length', 0)
        avg_content = sum(site.get('content_length', 0) for site in sites) / len(sites) if sites else 0
        
        # Method analysis
        methods = {}
        for site in sites:
            method = site.get('extraction_method', 'unknown')
            methods[method] = methods.get(method, 0) + 1
        
        # Domain analysis
        domains = set()
        for site in sites:
            url = site.get('url', '')
            if url:
                from urllib.parse import urlparse
                domain = urlparse(url).netloc
                domains.add(domain)
        
        # Top sources
        top_sources = sorted(sites, key=lambda x: x.get('content_length', 0), reverse=True)[:5]
        
        summary = {
            'research_info': {
                'topic': options['topic'],
                'timestamp': datetime.now().isoformat(),
                'extraction_type': options['extraction_type']
            },
            'performance_metrics': {
                'total_sites': len(sites),
                'total_content_length': total_content,
                'average_content_length': round(avg_content, 2),
                'unique_domains': len(domains)
            },
            'extraction_analysis': {
                'methods_used': methods,
                'success_rate': f"{(len(sites) / max(len(sites), 1)) * 100:.1f}%"
            },
            'top_sources': [
                {
                    'rank': i + 1,
                    'title': site.get('title', 'No title'),
                    'url': site.get('url', ''),
                    'content_length': site.get('content_length', 0),
                    'method': site.get('extraction_method', 'unknown')
                }
                for i, site in enumerate(top_sources)
            ],
            'key_findings': [
                f"Successfully extracted content from {len(sites)} sources",
                f"Average content length: {avg_content:.0f} characters",
                f"Content sourced from {len(domains)} unique domains",
                f"Most effective method: {max(methods, key=methods.get) if methods else 'N/A'}"
            ]
        }
        
        return summary
    
    def display_results(self, results, outputs):
        """Display research results"""
        print("\n" + "=" * 70)
        print("📊 RESEARCH RESULTS")
        print("=" * 70)
        
        sites = results.get('sites', [])
        print(f"🎯 Topic: {results.get('topic', 'Unknown')}")
        print(f"📈 Sites processed: {len(sites)}")
        print(f"📝 Total content: {results.get('total_content_length', 0):,} characters")
        print(f"⏱️  Extraction time: {results.get('extraction_time', 0):.2f} seconds")
        
        print(f"\n🔍 EXTRACTION METHODS:")
        methods = results.get('extraction_methods', [])
        for method in methods:
            print(f"   - {method}")
        
        print(f"\n🏆 TOP SOURCES:")
        for i, site in enumerate(sites[:5], 1):
            title = site.get('title', 'No title')
            content_len = site.get('content_length', 0)
            method = site.get('extraction_method', 'unknown')
            print(f"   {i}. {title[:60]}... ({content_len:,} chars, {method})")
        
        if outputs:
            print(f"\n📁 GENERATED FILES:")
            for output in outputs:
                print(f"   {output}")
        
        print("\n" + "=" * 70)
    
    def run(self):
        """Main application loop"""
        while True:
            self.clear_screen()
            self.print_banner()
            
            print("\n🎯 MAIN MENU:")
            print("1. 🔬 Start New Research")
            print("2. 📁 View Output Directory")
            print("3. ❓ Help")
            print("4. 🚪 Exit")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                # Get research parameters
                options = self.get_user_input()
                if not options:
                    input("\nPress Enter to continue...")
                    continue
                
                # Perform research
                results = self.perform_research(options)
                if not results:
                    input("\nPress Enter to continue...")
                    continue
                
                # Generate outputs
                outputs = self.generate_outputs(results, options)
                
                # Display results
                self.display_results(results, outputs)
                
                input("\nPress Enter to continue...")
                
            elif choice == "2":
                print(f"\n📁 Output directory: {self.output_dir.absolute()}")
                print("Generated files:")
                for file_type in ["pdfs", "json", "reports"]:
                    type_dir = self.output_dir / file_type
                    if type_dir.exists():
                        files = list(type_dir.glob("*"))
                        if files:
                            print(f"\n{file_type.upper()}:")
                            for file in files[-5:]:  # Show last 5 files
                                print(f"   {file.name}")
                
                input("\nPress Enter to continue...")
                
            elif choice == "3":
                print("\n❓ HELP")
                print("-" * 30)
                print("This standalone research assistant can:")
                print("• Extract content from multiple websites")
                print("• Generate comprehensive PDF reports")
                print("• Create JSON data files")
                print("• Provide research summaries")
                print("\nAll files are saved in the 'standalone_outputs' directory.")
                input("\nPress Enter to continue...")
                
            elif choice == "4":
                print("\n👋 Thank you for using the Standalone Research Assistant!")
                break
            
            else:
                print("\n❌ Invalid choice. Please try again.")
                input("Press Enter to continue...")

def main():
    """Main entry point"""
    try:
        interface = StandaloneResearchInterface()
        interface.run()
    except KeyboardInterrupt:
        print("\n\n👋 Research interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install requests beautifulsoup4 newspaper3k googlesearch-python duckduckgo-search reportlab nltk textblob")

if __name__ == "__main__":
    main() 