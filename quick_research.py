#!/usr/bin/env python3
"""
Quick Research Script - Simple one-command research
Usage: python quick_research.py "your research topic"
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

def quick_research(topic, max_sites=8, generate_pdf=True, generate_json=True):
    """Perform quick research on a topic"""
    print(f"🔬 Quick Research: {topic}")
    print(f"📊 Target sites: {max_sites}")
    print("-" * 50)
    
    # Initialize extractors
    extractor = AlternativeWebExtractor()
    pdf_generator = EnhancedPDFGenerator()
    
    # Perform extraction
    print("🚀 Starting web extraction...")
    results = extractor.get_topic_data(topic)
    
    if not results or 'error' in results:
        print("❌ Research failed!")
        return None
    
    print(f"✅ Research completed!")
    print(f"📈 Sites found: {len(results.get('sites', []))}")
    print(f"📝 Total content: {results.get('total_content_length', 0):,} characters")
    
    # Create output directory
    output_dir = Path("quick_outputs")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    topic_safe = topic.replace(' ', '_').replace('/', '_')[:30]
    
    outputs = []
    
    # Generate JSON
    if generate_json:
        json_filename = f"quick_{topic_safe}_{timestamp}.json"
        json_path = output_dir / json_filename
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        outputs.append(f"📄 JSON: {json_path}")
        print(f"✅ JSON saved: {json_path}")
    
    # Generate PDF
    if generate_pdf:
        pdf_filename = f"quick_{topic_safe}_{timestamp}.pdf"
        pdf_path = output_dir / pdf_filename
        
        try:
            # Prepare data for PDF
            pdf_data = {
                'topic': topic,
                'sites': results.get('sites', []),
                'total_content_length': results.get('total_content_length', 0),
                'search_engines_used': results.get('search_engines_used', []),
                'extraction_methods': results.get('extraction_methods', []),
                'timestamp': results.get('timestamp', datetime.now().isoformat())
            }
            
            pdf_generator.create_enhanced_web_extraction_pdf(pdf_data, str(pdf_path))
            outputs.append(f"📄 PDF: {pdf_path}")
            print(f"✅ PDF saved: {pdf_path}")
            
        except Exception as e:
            print(f"❌ PDF generation failed: {e}")
    
    # Display summary
    print("\n" + "=" * 50)
    print("📊 QUICK SUMMARY")
    print("=" * 50)
    
    sites = results.get('sites', [])
    print(f"🎯 Topic: {topic}")
    print(f"📈 Sites processed: {len(sites)}")
    print(f"📝 Total content: {results.get('total_content_length', 0):,} characters")
    print(f"⏱️  Time: {results.get('extraction_time', 0):.2f} seconds")
    
    print(f"\n🏆 TOP SOURCES:")
    for i, site in enumerate(sites[:3], 1):
        title = site.get('title', 'No title')
        content_len = site.get('content_length', 0)
        method = site.get('extraction_method', 'unknown')
        print(f"   {i}. {title[:50]}... ({content_len:,} chars)")
    
    if outputs:
        print(f"\n📁 Files saved:")
        for output in outputs:
            print(f"   {output}")
    
    print("\n" + "=" * 50)
    return results

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python quick_research.py \"your research topic\"")
        print("Example: python quick_research.py \"artificial intelligence\"")
        print("\nOptional flags:")
        print("  --no-pdf     Skip PDF generation")
        print("  --no-json    Skip JSON generation")
        print("  --sites N    Number of sites (default: 8)")
        sys.exit(1)
    
    # Parse arguments
    topic = sys.argv[1]
    generate_pdf = "--no-pdf" not in sys.argv
    generate_json = "--no-json" not in sys.argv
    
    # Get number of sites
    max_sites = 8
    for i, arg in enumerate(sys.argv):
        if arg == "--sites" and i + 1 < len(sys.argv):
            try:
                max_sites = int(sys.argv[i + 1])
            except ValueError:
                pass
    
    try:
        results = quick_research(topic, max_sites, generate_pdf, generate_json)
        if results:
            print("🎉 Quick research completed successfully!")
        else:
            print("❌ Quick research failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Research interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install requests beautifulsoup4 newspaper3k googlesearch-python duckduckgo-search reportlab nltk textblob")

if __name__ == "__main__":
    main() 