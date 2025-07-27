#!/usr/bin/env python3
"""
Integrated Launcher - Complete Research System
Combines all research capabilities and AI report generation
"""

import sys
import os
import asyncio
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

def main():
    """Main launcher function"""
    print("🚀 INTEGRATED RESEARCH SYSTEM LAUNCHER")
    print("=" * 60)
    print("Complete Research Solution with AI Report Generation")
    print("=" * 60)
    
    try:
        from integrated_research_system import IntegratedResearchSystem
        system = IntegratedResearchSystem()
        asyncio.run(system.run_interactive_mode())
    except ImportError as e:
        print(f"❌ Error importing Integrated Research System: {e}")
        print("Make sure all required files are in the same directory.")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"❌ Error running Integrated Research System: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main() 