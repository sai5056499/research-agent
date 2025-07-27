#!/usr/bin/env python3
"""
Setup Check Script for Super Agent & Multi-Agent Systems
Verifies all essential files and dependencies are present
"""

import sys
import os
from pathlib import Path

def check_essential_files():
    """Check if all essential files are present"""
    print("🔍 Checking Essential Files...")
    print("=" * 50)
    
    essential_files = [
        "enhanced_super_agent.py",
        "multi_agent_system.py", 
        "alternative_web_extractor.py",
        "enhanced_pdf_generator.py",
        "launcher.py",
        "README.md"
    ]
    
    missing_files = []
    present_files = []
    
    for file in essential_files:
        if Path(file).exists():
            present_files.append(file)
            print(f"✅ {file}")
        else:
            missing_files.append(file)
            print(f"❌ {file} - MISSING")
    
    print(f"\n📊 File Status:")
    print(f"Present: {len(present_files)}/{len(essential_files)}")
    print(f"Missing: {len(missing_files)}")
    
    if missing_files:
        print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
        return False
    else:
        print(f"\n🎉 All essential files present!")
        return True

def check_dependencies():
    """Check if required Python packages are installed"""
    print(f"\n🔍 Checking Dependencies...")
    print("=" * 50)
    
    required_packages = [
        "requests",
        "beautifulsoup4", 
        "newspaper3k",
        "googlesearch-python",
        "duckduckgo-search",
        "nltk",
        "textblob",
        "reportlab"
    ]
    
    missing_packages = []
    installed_packages = []
    
    for package in required_packages:
        try:
            # Handle different import names
            import_name = package.replace("-", "_")
            if package == "beautifulsoup4":
                import_name = "bs4"
            elif package == "newspaper3k":
                import_name = "newspaper"
            elif package == "googlesearch-python":
                import_name = "googlesearch"
            
            __import__(import_name)
            installed_packages.append(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - NOT INSTALLED")
    
    print(f"\n📊 Package Status:")
    print(f"Installed: {len(installed_packages)}/{len(required_packages)}")
    print(f"Missing: {len(missing_packages)}")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print(f"Install with: pip install {' '.join(missing_packages)}")
        return False
    else:
        print(f"\n🎉 All dependencies installed!")
        return True

def check_imports():
    """Test importing core modules"""
    print(f"\n🔍 Testing Imports...")
    print("=" * 50)
    
    modules_to_test = [
        ("enhanced_super_agent", "EnhancedSuperAgent"),
        ("multi_agent_system", "MultiAgentSystem"),
        ("alternative_web_extractor", "AlternativeWebExtractor"),
        ("enhanced_pdf_generator", "EnhancedPDFGenerator")
    ]
    
    failed_imports = []
    successful_imports = []
    
    for module_name, class_name in modules_to_test:
        try:
            module = __import__(module_name)
            class_obj = getattr(module, class_name)
            instance = class_obj()
            successful_imports.append(module_name)
            print(f"✅ {module_name}.{class_name}")
        except Exception as e:
            failed_imports.append(f"{module_name}: {str(e)}")
            print(f"❌ {module_name}.{class_name} - FAILED")
    
    print(f"\n📊 Import Status:")
    print(f"Successful: {len(successful_imports)}/{len(modules_to_test)}")
    print(f"Failed: {len(failed_imports)}")
    
    if failed_imports:
        print(f"\n⚠️  Failed imports:")
        for failure in failed_imports:
            print(f"  - {failure}")
        return False
    else:
        print(f"\n🎉 All imports successful!")
        return True

def check_output_directories():
    """Check if output directories exist"""
    print(f"\n🔍 Checking Output Directories...")
    print("=" * 50)
    
    output_dirs = [
        "super_agent_outputs",
        "multi_agent_outputs", 
        "integrated_outputs"
    ]
    
    missing_dirs = []
    present_dirs = []
    
    for dir_name in output_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            present_dirs.append(dir_name)
            print(f"✅ {dir_name}/")
        else:
            missing_dirs.append(dir_name)
            print(f"❌ {dir_name}/ - MISSING")
    
    print(f"\n📊 Directory Status:")
    print(f"Present: {len(present_dirs)}/{len(output_dirs)}")
    print(f"Missing: {len(missing_dirs)}")
    
    if missing_dirs:
        print(f"\n⚠️  Missing directories: {', '.join(missing_dirs)}")
        print("Directories will be created automatically when needed.")
        return False
    else:
        print(f"\n🎉 All output directories present!")
        return True

def main():
    """Main setup check function"""
    print("🚀 SUPER AGENT & MULTI-AGENT SETUP CHECK")
    print("=" * 60)
    print("Verifying system setup and dependencies...")
    print("=" * 60)
    
    # Run all checks
    files_ok = check_essential_files()
    deps_ok = check_dependencies()
    imports_ok = check_imports()
    dirs_ok = check_output_directories()
    
    # Summary
    print(f"\n🎯 SETUP SUMMARY")
    print("=" * 60)
    print(f"Essential Files: {'✅' if files_ok else '❌'}")
    print(f"Dependencies: {'✅' if deps_ok else '❌'}")
    print(f"Module Imports: {'✅' if imports_ok else '❌'}")
    print(f"Output Directories: {'✅' if dirs_ok else '❌'}")
    
    if all([files_ok, deps_ok, imports_ok]):
        print(f"\n🎉 SYSTEM READY!")
        print("You can now run:")
        print("  python launcher.py")
        print("  python integrated_launcher.py")
        print("  python enhanced_super_agent.py")
        print("  python multi_agent_system.py")
        return True
    else:
        print(f"\n⚠️  SETUP INCOMPLETE")
        print("Please fix the issues above before running the system.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 