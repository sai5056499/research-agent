#!/usr/bin/env python3
"""
Test script to verify enhanced web extraction with anti-detection measures
"""

import sys
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

def test_enhanced_extraction():
    """Test the enhanced web extraction"""
    try:
        from alternative_web_extractor import AlternativeWebExtractor
        
        print("🧪 Testing Enhanced Web Extraction - Anti-Detection Measures")
        print("=" * 70)
        
        extractor = AlternativeWebExtractor()
        
        # Test with a topic that was previously blocked
        topic = "artificial intelligence agents"
        print(f"🔍 Testing extraction for topic: {topic}")
        print("🛡️  Using enhanced anti-detection measures...")
        print()
        
        results = extractor.get_topic_data(topic, max_sites=3)
        
        print(f"\n📊 Results Summary:")
        print(f"Topic: {results['topic']}")
        print(f"Successful extractions: {len(results['sites'])}")
        print(f"Total content: {results['total_content_length']:,} characters")
        print(f"Extraction methods used: {', '.join(results['extraction_methods'])}")
        
        if results['sites']:
            print(f"\n📄 Extracted Sites:")
            for i, site in enumerate(results['sites'], 1):
                print(f"{i}. {site.get('title', 'Unknown')}")
                print(f"   URL: {site.get('url', 'Unknown')}")
                print(f"   Method: {site.get('extraction_method', 'unknown')}")
                print(f"   Content: {site.get('content_length', 0)} characters")
                print(f"   Attempts: {site.get('attempt', 1)}")
                print()
        else:
            print("❌ No sites were successfully extracted")
        
        print("🎉 Enhanced extraction test completed!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_enhanced_extraction() 