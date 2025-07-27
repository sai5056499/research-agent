#!/usr/bin/env python3
"""
Unified Research System - Combines Super Agent and Multi-Agent capabilities
Choose the best approach for your research needs dynamically
"""

import sys
import os
import json
import asyncio
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import time
import queue

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

try:
    from enhanced_super_agent import EnhancedSuperAgent
    from multi_agent_system import MultiAgentSystem
    from alternative_web_extractor import AlternativeWebExtractor
    from enhanced_pdf_generator import EnhancedPDFGenerator
except ImportError as e:
    print(f"Error importing core modules: {e}")
    sys.exit(1)

class UnifiedResearchSystem:
    """Unified system that combines Super Agent and Multi-Agent capabilities"""
    
    def __init__(self):
        """Initialize the unified research system"""
        self.super_agent = EnhancedSuperAgent()
        self.multi_agent = MultiAgentSystem()
        self.extractor = AlternativeWebExtractor()
        self.pdf_generator = EnhancedPDFGenerator()
        
        # System configuration
        self.config = {
            'default_mode': 'auto',  # 'auto', 'super', 'multi'
            'auto_threshold': {
                'simple_topics': 3,      # Use super agent for topics with <= 3 words
                'complex_analysis': 10,  # Use multi-agent for > 10 sites
                'resource_limit': 0.8    # Use super agent if CPU > 80%
            },
            'hybrid_mode': True,         # Enable hybrid research
            'comparison_mode': False     # Compare both systems
        }
        
        # Research sessions
        self.research_sessions = []
        self.comparison_results = []
        
        # Output directories
        self.output_dir = Path("unified_outputs")
        self.output_dir.mkdir(exist_ok=True)
        
        for subdir in ["super_agent", "multi_agent", "hybrid", "comparisons", "combined"]:
            (self.output_dir / subdir).mkdir(exist_ok=True)
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system("cls" if os.name == "nt" else "clear")
    
    def print_banner(self):
        """Print unified system banner"""
        print("=" * 80)
        print("🚀 UNIFIED RESEARCH SYSTEM")
        print("=" * 80)
        print("Super Agent + Multi-Agent = Ultimate Research Power")
        print("=" * 80)
    
    def analyze_topic_complexity(self, topic: str) -> Dict:
        """Analyze topic complexity to determine best approach"""
        words = topic.split()
        word_count = len(words)
        
        # Check for complex keywords
        complex_keywords = [
            'artificial intelligence', 'machine learning', 'deep learning',
            'blockchain', 'cryptocurrency', 'quantum computing',
            'biotechnology', 'nanotechnology', 'robotics',
            'comparison', 'analysis', 'research', 'study',
            'trends', 'future', 'development', 'evolution'
        ]
        
        complexity_score = 0
        for keyword in complex_keywords:
            if keyword.lower() in topic.lower():
                complexity_score += 2
        
        # Check for technical terms
        technical_indicators = ['api', 'framework', 'algorithm', 'protocol', 'architecture']
        for indicator in technical_indicators:
            if indicator.lower() in topic.lower():
                complexity_score += 1
        
        # Determine complexity level
        if word_count <= 3 and complexity_score <= 2:
            complexity = "simple"
        elif word_count <= 5 and complexity_score <= 4:
            complexity = "medium"
        else:
            complexity = "complex"
        
        return {
            "topic": topic,
            "word_count": word_count,
            "complexity_score": complexity_score,
            "complexity_level": complexity,
            "recommended_approach": self._get_recommended_approach(complexity, word_count, complexity_score)
        }
    
    def _get_recommended_approach(self, complexity: str, word_count: int, complexity_score: int) -> str:
        """Get recommended research approach based on analysis"""
        if self.config['default_mode'] == 'super':
            return 'super_agent'
        elif self.config['default_mode'] == 'multi':
            return 'multi_agent'
        elif self.config['default_mode'] == 'auto':
            if complexity == "simple" and word_count <= 3:
                return 'super_agent'
            elif complexity == "complex" or complexity_score >= 4:
                return 'multi_agent'
            elif complexity == "medium":
                return 'hybrid'
            else:
                return 'super_agent'
        else:
            return 'super_agent'
    
    async def perform_unified_research(self, topic: str, options: Dict = None) -> Dict:
        """Perform research using the best approach automatically"""
        print(f"🔍 Analyzing topic complexity: {topic}")
        
        # Analyze topic complexity
        analysis = self.analyze_topic_complexity(topic)
        recommended_approach = analysis['recommended_approach']
        
        print(f"📊 Topic Analysis:")
        print(f"   Words: {analysis['word_count']}")
        print(f"   Complexity Score: {analysis['complexity_score']}")
        print(f"   Complexity Level: {analysis['complexity_level']}")
        print(f"   Recommended Approach: {recommended_approach.replace('_', ' ').title()}")
        
        # Perform research based on recommended approach
        if recommended_approach == 'super_agent':
            return await self._perform_super_agent_research(topic, options, analysis)
        elif recommended_approach == 'multi_agent':
            return await self._perform_multi_agent_research(topic, options, analysis)
        elif recommended_approach == 'hybrid':
            return await self._perform_hybrid_research(topic, options, analysis)
        else:
            return await self._perform_super_agent_research(topic, options, analysis)
    
    async def _perform_super_agent_research(self, topic: str, options: Dict, analysis: Dict) -> Dict:
        """Perform research using Super Agent"""
        print(f"\n🤖 Using Super Agent for research...")
        
        # Determine complexity level for Super Agent
        complexity_map = {
            "simple": "simple",
            "medium": "medium", 
            "complex": "advanced"
        }
        
        super_options = {
            'complexity': complexity_map.get(analysis['complexity_level'], 'medium')
        }
        if options:
            super_options.update(options)
        
        results = await self.super_agent.perform_advanced_research(topic, super_options)
        
        # Add metadata
        results['research_approach'] = 'super_agent'
        results['topic_analysis'] = analysis
        results['system_used'] = 'Enhanced Super Agent'
        
        return results
    
    async def _perform_multi_agent_research(self, topic: str, options: Dict, analysis: Dict) -> Dict:
        """Perform research using Multi-Agent System"""
        print(f"\n🤝 Using Multi-Agent System for research...")
        
        # Configure multi-agent options
        multi_options = {
            'max_sites': 15 if analysis['complexity_level'] == 'complex' else 10,
            'search_engines': ['google', 'duckduckgo']
        }
        if options:
            multi_options.update(options)
        
        results = await self.multi_agent.perform_comprehensive_research(topic, multi_options)
        
        # Add metadata
        results['research_approach'] = 'multi_agent'
        results['topic_analysis'] = analysis
        results['system_used'] = 'Multi-Agent System'
        
        return results
    
    async def _perform_hybrid_research(self, topic: str, options: Dict, analysis: Dict) -> Dict:
        """Perform hybrid research using both systems"""
        print(f"\n🔄 Using Hybrid Approach (Super Agent + Multi-Agent)...")
        
        # Phase 1: Quick Super Agent research
        print("Phase 1: Quick Super Agent Analysis")
        super_results = await self._perform_super_agent_research(topic, options, analysis)
        
        # Phase 2: Detailed Multi-Agent analysis
        print("Phase 2: Detailed Multi-Agent Analysis")
        multi_results = await self._perform_multi_agent_research(topic, options, analysis)
        
        # Combine results
        hybrid_results = {
            'topic': topic,
            'research_approach': 'hybrid',
            'topic_analysis': analysis,
            'system_used': 'Hybrid (Super Agent + Multi-Agent)',
            'timestamp': datetime.now().isoformat(),
            'super_agent_results': super_results,
            'multi_agent_results': multi_results,
            'combined_insights': self._combine_insights(super_results, multi_results),
            'performance_comparison': self._compare_performance(super_results, multi_results)
        }
        
        return hybrid_results
    
    def _combine_insights(self, super_results: Dict, multi_results: Dict) -> Dict:
        """Combine insights from both systems"""
        combined = {
            'key_insights': [],
            'recommendations': [],
            'trends': [],
            'gaps': [],
            'opportunities': []
        }
        
        # Combine Super Agent insights
        if super_results.get('insights'):
            super_insights = super_results['insights']
            combined['key_insights'].extend(super_insights.get('key_insights', [])[:3])
            combined['recommendations'].extend(super_insights.get('recommendations', [])[:2])
        
        # Combine Multi-Agent insights
        if multi_results.get('final_results', {}).get('insights_summary'):
            multi_insights = multi_results['final_results']['insights_summary']
            combined['key_insights'].extend(multi_insights.get('key_insights', [])[:3])
            combined['recommendations'].extend(multi_insights.get('recommendations', [])[:2])
            combined['trends'].extend(multi_insights.get('trends', [])[:2])
            combined['gaps'].extend(multi_insights.get('gaps', [])[:2])
            combined['opportunities'].extend(multi_insights.get('opportunities', [])[:2])
        
        # Remove duplicates and limit
        for key in combined:
            combined[key] = list(dict.fromkeys(combined[key]))[:5]  # Remove duplicates, limit to 5
        
        return combined
    
    def _compare_performance(self, super_results: Dict, multi_results: Dict) -> Dict:
        """Compare performance between systems"""
        comparison = {
            'super_agent': {},
            'multi_agent': {},
            'recommendation': ''
        }
        
        # Super Agent metrics
        if super_results.get('performance_metrics'):
            comparison['super_agent'] = {
                'sites': super_results['performance_metrics'].get('total_sites', 0),
                'content': super_results['performance_metrics'].get('total_content', 0),
                'insights': super_results['performance_metrics'].get('insight_count', 0)
            }
        
        # Multi-Agent metrics
        if multi_results.get('final_results', {}).get('performance_metrics'):
            comparison['multi_agent'] = {
                'sites': multi_results['final_results']['performance_metrics'].get('total_sites', 0),
                'content': multi_results['final_results']['performance_metrics'].get('total_content', 0),
                'insights': multi_results['final_results']['performance_metrics'].get('insight_count', 0)
            }
        
        # Generate recommendation
        super_sites = comparison['super_agent'].get('sites', 0)
        multi_sites = comparison['multi_agent'].get('sites', 0)
        
        if multi_sites > super_sites * 1.5:
            comparison['recommendation'] = 'Multi-Agent provided more comprehensive coverage'
        elif super_sites > multi_sites * 1.2:
            comparison['recommendation'] = 'Super Agent was more efficient for this topic'
        else:
            comparison['recommendation'] = 'Both systems performed similarly'
        
        return comparison
    
    async def compare_systems(self, topic: str, options: Dict = None) -> Dict:
        """Compare both systems on the same topic"""
        print(f"🔬 Comparing Super Agent vs Multi-Agent on: {topic}")
        print("=" * 60)
        
        comparison_results = {
            'topic': topic,
            'timestamp': datetime.now().isoformat(),
            'super_agent': {},
            'multi_agent': {},
            'comparison': {}
        }
        
        # Run Super Agent
        print("\n🤖 Running Super Agent...")
        start_time = time.time()
        # Create proper analysis structure for comparison
        analysis = self.analyze_topic_complexity(topic)
        super_results = await self._perform_super_agent_research(topic, options, analysis)
        super_time = time.time() - start_time
        
        comparison_results['super_agent'] = {
            'results': super_results,
            'execution_time': super_time,
            'sites_analyzed': super_results.get('performance_metrics', {}).get('total_sites', 0),
            'insights_generated': super_results.get('performance_metrics', {}).get('insight_count', 0)
        }
        
        # Run Multi-Agent
        print("\n🤝 Running Multi-Agent System...")
        start_time = time.time()
        multi_results = await self._perform_multi_agent_research(topic, options, analysis)
        multi_time = time.time() - start_time
        
        comparison_results['multi_agent'] = {
            'results': multi_results,
            'execution_time': multi_time,
            'sites_analyzed': multi_results.get('final_results', {}).get('extraction_summary', {}).get('sites', 0),
            'insights_generated': len(multi_results.get('final_results', {}).get('insights_summary', {}).get('key_insights', []))
        }
        
        # Generate comparison
        comparison_results['comparison'] = {
            'speed_winner': 'super_agent' if super_time < multi_time else 'multi_agent',
            'coverage_winner': 'multi_agent' if comparison_results['multi_agent']['sites_analyzed'] > comparison_results['super_agent']['sites_analyzed'] else 'super_agent',
            'insights_winner': 'multi_agent' if comparison_results['multi_agent']['insights_generated'] > comparison_results['super_agent']['insights_generated'] else 'super_agent',
            'time_difference': abs(super_time - multi_time),
            'site_difference': abs(comparison_results['multi_agent']['sites_analyzed'] - comparison_results['super_agent']['sites_analyzed']),
            'recommendation': self._generate_comparison_recommendation(comparison_results)
        }
        
        self.comparison_results.append(comparison_results)
        return comparison_results
    
    def _generate_comparison_recommendation(self, comparison: Dict) -> str:
        """Generate recommendation based on comparison results"""
        super_agent = comparison['super_agent']
        multi_agent = comparison['multi_agent']
        comp = comparison['comparison']
        
        if comp['speed_winner'] == 'super_agent' and comp['coverage_winner'] == 'super_agent':
            return "Super Agent is clearly better for this topic - faster and more comprehensive"
        elif comp['speed_winner'] == 'multi_agent' and comp['coverage_winner'] == 'multi_agent':
            return "Multi-Agent System is clearly better for this topic - faster and more comprehensive"
        elif comp['speed_winner'] == 'super_agent' and comp['coverage_winner'] == 'multi_agent':
            return "Trade-off: Super Agent is faster, Multi-Agent provides better coverage"
        elif comp['speed_winner'] == 'multi_agent' and comp['coverage_winner'] == 'super_agent':
            return "Trade-off: Multi-Agent is faster, Super Agent provides better coverage"
        else:
            return "Both systems performed similarly - choose based on preference"
    
    def display_unified_results(self, results: Dict):
        """Display results from unified research"""
        print("\n" + "=" * 80)
        print("📊 UNIFIED RESEARCH RESULTS")
        print("=" * 80)
        
        topic = results.get('topic', 'Unknown')
        approach = results.get('research_approach', 'unknown')
        system_used = results.get('system_used', 'Unknown')
        
        print(f"🎯 Topic: {topic}")
        print(f"🤖 Approach: {approach.replace('_', ' ').title()}")
        print(f"⚙️  System: {system_used}")
        
        if approach == 'hybrid':
            self._display_hybrid_results(results)
        elif approach == 'super_agent':
            self.super_agent.display_comprehensive_results(results)
        elif approach == 'multi_agent':
            self.multi_agent.display_comprehensive_results(results)
        
        print("\n" + "=" * 80)
    
    def _display_hybrid_results(self, results: Dict):
        """Display hybrid research results"""
        super_results = results.get('super_agent_results', {})
        multi_results = results.get('multi_agent_results', {})
        combined = results.get('combined_insights', {})
        comparison = results.get('performance_comparison', {})
        
        print(f"\n🔄 HYBRID ANALYSIS:")
        print(f"   Super Agent Sites: {comparison.get('super_agent', {}).get('sites', 0)}")
        print(f"   Multi-Agent Sites: {comparison.get('multi_agent', {}).get('sites', 0)}")
        print(f"   Combined Insights: {len(combined.get('key_insights', []))}")
        
        if combined.get('key_insights'):
            print(f"\n💡 COMBINED KEY INSIGHTS:")
            for i, insight in enumerate(combined['key_insights'][:5], 1):
                print(f"   {i}. {insight}")
        
        if combined.get('recommendations'):
            print(f"\n🎯 COMBINED RECOMMENDATIONS:")
            for i, rec in enumerate(combined['recommendations'][:3], 1):
                print(f"   {i}. {rec}")
        
        print(f"\n📈 PERFORMANCE COMPARISON:")
        print(f"   {comparison.get('recommendation', 'No comparison available')}")
    
    def display_comparison_results(self, results: Dict):
        """Display system comparison results"""
        print("\n" + "=" * 80)
        print("🔬 SYSTEM COMPARISON RESULTS")
        print("=" * 80)
        
        topic = results.get('topic', 'Unknown')
        super_agent = results.get('super_agent', {})
        multi_agent = results.get('multi_agent', {})
        comparison = results.get('comparison', {})
        
        print(f"🎯 Topic: {topic}")
        
        print(f"\n🤖 SUPER AGENT:")
        print(f"   Execution Time: {super_agent.get('execution_time', 0):.2f} seconds")
        print(f"   Sites Analyzed: {super_agent.get('sites_analyzed', 0)}")
        print(f"   Insights Generated: {super_agent.get('insights_generated', 0)}")
        
        print(f"\n🤝 MULTI-AGENT SYSTEM:")
        print(f"   Execution Time: {multi_agent.get('execution_time', 0):.2f} seconds")
        print(f"   Sites Analyzed: {multi_agent.get('sites_analyzed', 0)}")
        print(f"   Insights Generated: {multi_agent.get('insights_generated', 0)}")
        
        print(f"\n📊 COMPARISON:")
        print(f"   Speed Winner: {comparison.get('speed_winner', 'N/A').replace('_', ' ').title()}")
        print(f"   Coverage Winner: {comparison.get('coverage_winner', 'N/A').replace('_', ' ').title()}")
        print(f"   Insights Winner: {comparison.get('insights_winner', 'N/A').replace('_', ' ').title()}")
        print(f"   Time Difference: {comparison.get('time_difference', 0):.2f} seconds")
        print(f"   Site Difference: {comparison.get('site_difference', 0)} sites")
        
        print(f"\n🎯 RECOMMENDATION:")
        print(f"   {comparison.get('recommendation', 'No recommendation available')}")
        
        print("\n" + "=" * 80)
    
    async def run_interactive_mode(self):
        """Run the unified system in interactive mode"""
        while True:
            self.clear_screen()
            self.print_banner()
            
            print("\n🎯 UNIFIED RESEARCH SYSTEM MENU:")
            print("1. 🔬 Smart Research (Auto-choose best approach)")
            print("2. 🤖 Super Agent Research")
            print("3. 🤝 Multi-Agent Research")
            print("4. 🔄 Hybrid Research (Both systems)")
            print("5. 🔬 Compare Systems")
            print("6. ⚙️  System Configuration")
            print("7. 📊 Research History")
            print("8. 📁 View Outputs")
            print("9. ❓ Help")
            print("0. 🚪 Exit")
            
            choice = input("\nEnter your choice (0-9): ").strip()
            
            if choice == "1":
                await self._handle_smart_research()
            elif choice == "2":
                await self._handle_super_agent_research()
            elif choice == "3":
                await self._handle_multi_agent_research()
            elif choice == "4":
                await self._handle_hybrid_research()
            elif choice == "5":
                await self._handle_system_comparison()
            elif choice == "6":
                self._configure_system()
            elif choice == "7":
                self._show_research_history()
            elif choice == "8":
                self._show_outputs()
            elif choice == "9":
                self._show_help()
            elif choice == "0":
                print("\n👋 Thank you for using the Unified Research System!")
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
                input("Press Enter to continue...")
    
    async def _handle_smart_research(self):
        """Handle smart research with auto-selection"""
        print("\n🔬 SMART RESEARCH")
        print("-" * 30)
        
        topic = input("Enter research topic: ").strip()
        if not topic:
            print("❌ Topic cannot be empty!")
            input("Press Enter to continue...")
            return
        
        print(f"\n🚀 Starting smart research on: {topic}")
        print("The system will automatically choose the best approach...")
        
        results = await self.perform_unified_research(topic)
        
        if results and 'error' not in results:
            self.display_unified_results(results)
            self.research_sessions.append({
                'topic': topic,
                'timestamp': datetime.now().isoformat(),
                'approach': results.get('research_approach', 'unknown'),
                'system': results.get('system_used', 'Unknown')
            })
        else:
            print("❌ Research failed!")
        
        input("\nPress Enter to continue...")
    
    async def _handle_super_agent_research(self):
        """Handle Super Agent research"""
        print("\n🤖 SUPER AGENT RESEARCH")
        print("-" * 30)
        
        topic = input("Enter research topic: ").strip()
        if not topic:
            print("❌ Topic cannot be empty!")
            input("Press Enter to continue...")
            return
        
        print(f"\n🚀 Starting Super Agent research on: {topic}")
        
        # Create proper analysis structure
        analysis = self.analyze_topic_complexity(topic)
        results = await self._perform_super_agent_research(topic, {}, analysis)
        
        if results and 'error' not in results:
            self.super_agent.display_comprehensive_results(results)
            self.research_sessions.append({
                'topic': topic,
                'timestamp': datetime.now().isoformat(),
                'approach': 'super_agent',
                'system': 'Enhanced Super Agent'
            })
        else:
            print("❌ Research failed!")
        
        input("\nPress Enter to continue...")
    
    async def _handle_multi_agent_research(self):
        """Handle Multi-Agent research"""
        print("\n🤝 MULTI-AGENT RESEARCH")
        print("-" * 30)
        
        topic = input("Enter research topic: ").strip()
        if not topic:
            print("❌ Topic cannot be empty!")
            input("Press Enter to continue...")
            return
        
        print(f"\n🚀 Starting Multi-Agent research on: {topic}")
        
        # Create proper analysis structure
        analysis = self.analyze_topic_complexity(topic)
        results = await self._perform_multi_agent_research(topic, {}, analysis)
        
        if results and 'error' not in results:
            self.multi_agent.display_comprehensive_results(results)
            self.research_sessions.append({
                'topic': topic,
                'timestamp': datetime.now().isoformat(),
                'approach': 'multi_agent',
                'system': 'Multi-Agent System'
            })
        else:
            print("❌ Research failed!")
        
        input("\nPress Enter to continue...")
    
    async def _handle_hybrid_research(self):
        """Handle hybrid research"""
        print("\n🔄 HYBRID RESEARCH")
        print("-" * 30)
        
        topic = input("Enter research topic: ").strip()
        if not topic:
            print("❌ Topic cannot be empty!")
            input("Press Enter to continue...")
            return
        
        print(f"\n🚀 Starting hybrid research on: {topic}")
        print("This will use both Super Agent and Multi-Agent systems...")
        
        # Create proper analysis structure
        analysis = self.analyze_topic_complexity(topic)
        results = await self._perform_hybrid_research(topic, {}, analysis)
        
        if results and 'error' not in results:
            self.display_unified_results(results)
            self.research_sessions.append({
                'topic': topic,
                'timestamp': datetime.now().isoformat(),
                'approach': 'hybrid',
                'system': 'Hybrid (Super Agent + Multi-Agent)'
            })
        else:
            print("❌ Research failed!")
        
        input("\nPress Enter to continue...")
    
    async def _handle_system_comparison(self):
        """Handle system comparison"""
        print("\n🔬 SYSTEM COMPARISON")
        print("-" * 30)
        
        topic = input("Enter research topic: ").strip()
        if not topic:
            print("❌ Topic cannot be empty!")
            input("Press Enter to continue...")
            return
        
        print(f"\n🔬 Comparing systems on: {topic}")
        print("This will run both systems and compare their performance...")
        
        results = await self.compare_systems(topic)
        
        if results and 'error' not in results:
            self.display_comparison_results(results)
        else:
            print("❌ Comparison failed!")
        
        input("\nPress Enter to continue...")
    
    def _configure_system(self):
        """Configure system settings"""
        print("\n⚙️  SYSTEM CONFIGURATION")
        print("-" * 30)
        
        print("Current Configuration:")
        print(f"   Default Mode: {self.config['default_mode']}")
        print(f"   Hybrid Mode: {'Enabled' if self.config['hybrid_mode'] else 'Disabled'}")
        print(f"   Comparison Mode: {'Enabled' if self.config['comparison_mode'] else 'Disabled'}")
        
        print("\nConfiguration Options:")
        print("1. Set default mode (auto/super/multi)")
        print("2. Toggle hybrid mode")
        print("3. Toggle comparison mode")
        print("4. Reset to defaults")
        
        choice = input("Choose option (1-4): ").strip()
        
        if choice == "1":
            print("\nDefault modes:")
            print("1. auto - Automatically choose best approach")
            print("2. super - Always use Super Agent")
            print("3. multi - Always use Multi-Agent")
            
            mode_choice = input("Choose mode (1-3): ").strip()
            mode_map = {"1": "auto", "2": "super", "3": "multi"}
            if mode_choice in mode_map:
                self.config['default_mode'] = mode_map[mode_choice]
                print(f"✅ Default mode set to: {self.config['default_mode']}")
        
        elif choice == "2":
            self.config['hybrid_mode'] = not self.config['hybrid_mode']
            print(f"✅ Hybrid mode: {'Enabled' if self.config['hybrid_mode'] else 'Disabled'}")
        
        elif choice == "3":
            self.config['comparison_mode'] = not self.config['comparison_mode']
            print(f"✅ Comparison mode: {'Enabled' if self.config['comparison_mode'] else 'Disabled'}")
        
        elif choice == "4":
            self.config = {
                'default_mode': 'auto',
                'auto_threshold': {
                    'simple_topics': 3,
                    'complex_analysis': 10,
                    'resource_limit': 0.8
                },
                'hybrid_mode': True,
                'comparison_mode': False
            }
            print("✅ Configuration reset to defaults")
        
        input("\nPress Enter to continue...")
    
    def _show_research_history(self):
        """Show research history"""
        print("\n📊 RESEARCH HISTORY")
        print("-" * 30)
        
        if not self.research_sessions:
            print("No research sessions found.")
        else:
            for i, session in enumerate(self.research_sessions[-10:], 1):  # Show last 10
                print(f"{i}. {session['topic']} ({session['approach']}) - {session['timestamp'][:19]}")
                print(f"   System: {session['system']}")
        
        if self.comparison_results:
            print(f"\n🔬 COMPARISON RESULTS ({len(self.comparison_results)}):")
            for i, comp in enumerate(self.comparison_results[-5:], 1):  # Show last 5
                print(f"{i}. {comp['topic']} - {comp['timestamp'][:19]}")
        
        input("\nPress Enter to continue...")
    
    def _show_outputs(self):
        """Show generated outputs"""
        print(f"\n📁 OUTPUT DIRECTORY: {self.output_dir.absolute()}")
        print("-" * 50)
        
        for subdir in ["super_agent", "multi_agent", "hybrid", "comparisons", "combined"]:
            subdir_path = self.output_dir / subdir
            if subdir_path.exists():
                files = list(subdir_path.glob("*"))
                if files:
                    print(f"\n{subdir.upper()}:")
                    for file in files[-3:]:  # Show last 3 files
                        size_kb = file.stat().st_size / 1024
                        print(f"   {file.name} ({size_kb:.1f} KB)")
        
        input("\nPress Enter to continue...")
    
    def _show_help(self):
        """Show help and documentation"""
        print("\n❓ HELP & DOCUMENTATION")
        print("=" * 60)
        
        print("Unified Research System Features:")
        print("• Smart Research: Automatically chooses the best approach")
        print("• Super Agent: Single powerful agent for quick research")
        print("• Multi-Agent: Specialized agents for detailed analysis")
        print("• Hybrid Research: Combines both systems for comprehensive results")
        print("• System Comparison: Compare performance of both systems")
        print("• Topic Analysis: Analyzes complexity to determine best approach")
        
        print("\nResearch Approaches:")
        print("• Simple topics (≤3 words): Super Agent")
        print("• Complex topics (>5 words + technical terms): Multi-Agent")
        print("• Medium complexity: Hybrid approach")
        print("• Auto mode: System decides based on topic analysis")
        
        print("\nBenefits:")
        print("• Best of both worlds: Speed + Detail")
        print("• Intelligent approach selection")
        print("• Performance comparison and optimization")
        print("• Comprehensive research capabilities")
        
        input("\nPress Enter to continue...")

async def main():
    """Main entry point for unified research system"""
    try:
        system = UnifiedResearchSystem()
        await system.run_interactive_mode()
    except KeyboardInterrupt:
        print("\n\n👋 Unified Research System interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 