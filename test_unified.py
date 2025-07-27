#!/usr/bin/env python3
"""
Test script for Unified Research System
"""

import sys
import os
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        from enhanced_super_agent import EnhancedSuperAgent
        print("✅ EnhancedSuperAgent imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import EnhancedSuperAgent: {e}")
        return False
    
    try:
        from multi_agent_system import MultiAgentSystem
        print("✅ MultiAgentSystem imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import MultiAgentSystem: {e}")
        return False
    
    try:
        from alternative_web_extractor import AlternativeWebExtractor
        print("✅ AlternativeWebExtractor imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import AlternativeWebExtractor: {e}")
        return False
    
    try:
        from enhanced_pdf_generator import EnhancedPDFGenerator
        print("✅ EnhancedPDFGenerator imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import EnhancedPDFGenerator: {e}")
        return False
    
    try:
        from unified_research_system import UnifiedResearchSystem
        print("✅ UnifiedResearchSystem imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import UnifiedResearchSystem: {e}")
        return False
    
    return True

def test_system_creation():
    """Test if systems can be created"""
    print("\nTesting system creation...")
    
    try:
        from unified_research_system import UnifiedResearchSystem
        system = UnifiedResearchSystem()
        print("✅ UnifiedResearchSystem created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create UnifiedResearchSystem: {e}")
        return False

def test_topic_analysis():
    """Test topic analysis functionality"""
    print("\nTesting topic analysis...")
    
    try:
        from unified_research_system import UnifiedResearchSystem
        system = UnifiedResearchSystem()
        
        # Test simple topic
        simple_analysis = system.analyze_topic_complexity("AI")
        print(f"✅ Simple topic analysis: {simple_analysis['complexity_level']}")
        
        # Test complex topic
        complex_analysis = system.analyze_topic_complexity("artificial intelligence machine learning deep learning trends")
        print(f"✅ Complex topic analysis: {complex_analysis['complexity_level']}")
        
        return True
    except Exception as e:
        print(f"❌ Failed topic analysis: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing Unified Research System")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Check dependencies.")
        return
    
    # Test system creation
    if not test_system_creation():
        print("\n❌ System creation failed.")
        return
    
    # Test topic analysis
    if not test_topic_analysis():
        print("\n❌ Topic analysis failed.")
        return
    
    print("\n🎉 All tests passed! Unified Research System is ready to use.")
    print("\nTo start the system, run:")
    print("python run_unified.py")

if __name__ == "__main__":
    main() 