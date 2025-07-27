#!/usr/bin/env python3
"""
Unified Research System Launcher
Quick start for the combined Super Agent + Multi-Agent system
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
    print("🚀 Starting Unified Research System...")
    print("Combining Super Agent + Multi-Agent capabilities")
    print("=" * 60)
    
    try:
        from unified_research_system import UnifiedResearchSystem
        system = UnifiedResearchSystem()
        asyncio.run(system.run_interactive_mode())
    except ImportError as e:
        print(f"❌ Error importing Unified Research System: {e}")
        print("Make sure all required files are in the same directory.")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"❌ Error running Unified Research System: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main() 