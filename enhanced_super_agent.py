#!/usr/bin/env python3
"""
Enhanced Super Agent - Advanced AI Research Assistant
Features: Multi-modal research, advanced analysis, intelligent insights
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
import random

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

try:
    from alternative_web_extractor import AlternativeWebExtractor
    from enhanced_pdf_generator import EnhancedPDFGenerator
except ImportError as e:
    print(f"Error importing core modules: {e}")
    sys.exit(1)

class EnhancedSuperAgent:
    """Enhanced Super Agent with advanced research capabilities"""
    
    def __init__(self):
        """Initialize the enhanced super agent"""
        self.extractor = AlternativeWebExtractor()
        self.pdf_generator = EnhancedPDFGenerator()
        
        # Agent capabilities
        self.capabilities = {
            'web_extraction': True,
            'content_analysis': True,
            'insight_generation': True,
            'report_generation': True,
            'data_visualization': True,
            'trend_analysis': True,
            'comparative_analysis': True,
            'recommendation_engine': True
        }
        
        # Research sessions
        self.active_sessions = {}
        self.research_history = []
        
        # Output directories
        self.output_dir = Path("super_agent_outputs")
        self.output_dir.mkdir(exist_ok=True)
        
        for subdir in ["reports", "data", "insights", "visualizations", "comparisons"]:
            (self.output_dir / subdir).mkdir(exist_ok=True)
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system("cls" if os.name == "nt" else "clear")
    
    def print_banner(self):
        """Print enhanced banner"""
        print("=" * 80)
        print("🤖 ENHANCED SUPER AGENT - AI-Powered Research Assistant")
        print("=" * 80)
        print("Advanced web extraction • Intelligent analysis • Multi-modal insights")
        print("=" * 80)
    
    def get_research_strategy(self, topic: str, complexity: str = "medium") -> Dict:
        """Generate intelligent research strategy based on topic and complexity"""
        strategies = {
            "simple": {
                "max_sites": 5,
                "search_engines": ["google"],
                "extraction_methods": ["newspaper3k"],
                "analysis_depth": "basic",
                "output_types": ["summary", "pdf"]
            },
            "medium": {
                "max_sites": 10,
                "search_engines": ["google", "duckduckgo"],
                "extraction_methods": ["newspaper3k", "beautifulsoup"],
                "analysis_depth": "comprehensive",
                "output_types": ["summary", "pdf", "insights", "json"]
            },
            "advanced": {
                "max_sites": 15,
                "search_engines": ["google", "duckduckgo", "bing"],
                "extraction_methods": ["newspaper3k", "beautifulsoup", "simple_text"],
                "analysis_depth": "deep",
                "output_types": ["summary", "pdf", "insights", "json", "visualizations", "comparisons"]
            }
        }
        
        strategy = strategies.get(complexity, strategies["medium"])
        
        # Enhance strategy based on topic keywords
        topic_lower = topic.lower()
        if any(word in topic_lower for word in ["ai", "artificial intelligence", "machine learning"]):
            strategy["max_sites"] += 3
            strategy["analysis_depth"] = "deep"
        elif any(word in topic_lower for word in ["business", "market", "industry"]):
            strategy["output_types"].append("trend_analysis")
        elif any(word in topic_lower for word in ["academic", "research", "study"]):
            strategy["output_types"].append("academic_report")
        
        return strategy
    
    async def perform_advanced_research(self, topic: str, options: Dict = None) -> Dict:
        """Perform advanced research with multiple analysis layers"""
        print(f"🚀 Starting advanced research on: {topic}")
        
        # Generate research strategy
        complexity = options.get('complexity', 'medium') if options else 'medium'
        strategy = self.get_research_strategy(topic, complexity)
        
        print(f"📊 Strategy: {complexity} complexity, {strategy['max_sites']} sites")
        
        # Phase 1: Web Extraction
        print("\n🔍 Phase 1: Web Extraction")
        extraction_results = await self._extract_web_content(topic, strategy)
        
        if not extraction_results:
            return {"error": "Web extraction failed"}
        
        # Phase 2: Content Analysis
        print("\n🧠 Phase 2: Content Analysis")
        analysis_results = await self._analyze_content(extraction_results, strategy)
        
        # Phase 3: Insight Generation
        print("\n💡 Phase 3: Insight Generation")
        insights = await self._generate_insights(extraction_results, analysis_results, topic)
        
        # Phase 4: Report Generation
        print("\n📄 Phase 4: Report Generation")
        reports = await self._generate_reports(extraction_results, analysis_results, insights, topic, strategy)
        
        # Compile comprehensive results
        comprehensive_results = {
            "topic": topic,
            "timestamp": datetime.now().isoformat(),
            "strategy": strategy,
            "extraction": extraction_results,
            "analysis": analysis_results,
            "insights": insights,
            "reports": reports,
            "performance_metrics": {
                "total_sites": len(extraction_results.get('sites', [])),
                "total_content": extraction_results.get('total_content_length', 0),
                "analysis_time": time.time(),
                "insight_count": len(insights.get('key_insights', [])),
                "report_count": len(reports)
            }
        }
        
        return comprehensive_results
    
    async def _extract_web_content(self, topic: str, strategy: Dict) -> Dict:
        """Extract web content using multiple methods"""
        try:
            # Use the extractor with strategy parameters
            results = self.extractor.get_topic_data(topic)
            
            if not results or 'error' in results:
                return None
            
            # Enhance results with strategy metadata
            results['strategy'] = strategy
            results['extraction_timestamp'] = datetime.now().isoformat()
            
            return results
            
        except Exception as e:
            print(f"❌ Extraction error: {e}")
            return None
    
    async def _analyze_content(self, extraction_results: Dict, strategy: Dict) -> Dict:
        """Analyze extracted content for patterns and insights"""
        sites = extraction_results.get('sites', [])
        
        if not sites:
            return {"error": "No content to analyze"}
        
        analysis = {
            "content_metrics": {},
            "topic_coverage": {},
            "source_analysis": {},
            "sentiment_analysis": {},
            "keyword_analysis": {}
        }
        
        # Content metrics
        content_lengths = [site.get('content_length', 0) for site in sites]
        analysis["content_metrics"] = {
            "total_sites": len(sites),
            "total_content": sum(content_lengths),
            "average_content": sum(content_lengths) / len(content_lengths) if content_lengths else 0,
            "max_content": max(content_lengths) if content_lengths else 0,
            "min_content": min(content_lengths) if content_lengths else 0
        }
        
        # Source analysis
        domains = {}
        methods = {}
        for site in sites:
            # Domain analysis
            url = site.get('url', '')
            if url:
                from urllib.parse import urlparse
                domain = urlparse(url).netloc
                domains[domain] = domains.get(domain, 0) + 1
            
            # Method analysis
            method = site.get('extraction_method', 'unknown')
            methods[method] = methods.get(method, 0) + 1
        
        analysis["source_analysis"] = {
            "unique_domains": len(domains),
            "domain_distribution": domains,
            "extraction_methods": methods,
            "top_domains": dict(sorted(domains.items(), key=lambda x: x[1], reverse=True)[:5])
        }
        
        # Topic coverage analysis
        topic_words = set(extraction_results.get('topic', '').lower().split())
        coverage_scores = []
        
        for site in sites:
            title = site.get('title', '').lower()
            content = site.get('content', '').lower()
            
            title_matches = sum(1 for word in topic_words if word in title)
            content_matches = sum(1 for word in topic_words if word in content)
            
            coverage_score = (title_matches * 2) + content_matches
            coverage_scores.append(coverage_score)
        
        analysis["topic_coverage"] = {
            "average_coverage": sum(coverage_scores) / len(coverage_scores) if coverage_scores else 0,
            "high_coverage_sites": len([s for s in coverage_scores if s >= 3]),
            "coverage_distribution": {
                "excellent": len([s for s in coverage_scores if s >= 5]),
                "good": len([s for s in coverage_scores if 3 <= s < 5]),
                "fair": len([s for s in coverage_scores if 1 <= s < 3]),
                "poor": len([s for s in coverage_scores if s < 1])
            }
        }
        
        return analysis
    
    async def _generate_insights(self, extraction_results: Dict, analysis_results: Dict, topic: str) -> Dict:
        """Generate intelligent insights from research data"""
        insights = {
            "key_insights": [],
            "trends": [],
            "recommendations": [],
            "gaps_identified": [],
            "future_directions": []
        }
        
        sites = extraction_results.get('sites', [])
        analysis = analysis_results
        
        # Key insights based on content analysis
        if analysis.get('content_metrics'):
            metrics = analysis['content_metrics']
            insights["key_insights"].append(
                f"Successfully analyzed {metrics['total_sites']} sources with {metrics['total_content']:,} characters of content"
            )
            
            if metrics['average_content'] > 2000:
                insights["key_insights"].append("Content depth is substantial, indicating comprehensive coverage")
            elif metrics['average_content'] < 500:
                insights["key_insights"].append("Content is concise, may need additional sources for depth")
        
        # Source diversity insights
        if analysis.get('source_analysis'):
            source_analysis = analysis['source_analysis']
            insights["key_insights"].append(
                f"Content sourced from {source_analysis['unique_domains']} unique domains"
            )
            
            if source_analysis['unique_domains'] >= 5:
                insights["key_insights"].append("Good source diversity indicates comprehensive research")
            else:
                insights["recommendations"].append("Consider expanding to more diverse sources")
        
        # Topic coverage insights
        if analysis.get('topic_coverage'):
            coverage = analysis['topic_coverage']
            insights["key_insights"].append(
                f"Topic coverage: {coverage['high_coverage_sites']} sites with excellent coverage"
            )
            
            if coverage['coverage_distribution']['poor'] > len(sites) * 0.3:
                insights["gaps_identified"].append("Significant portion of sources have poor topic relevance")
                insights["recommendations"].append("Refine search terms for better topic alignment")
        
        # Method effectiveness insights
        if analysis.get('source_analysis', {}).get('extraction_methods'):
            methods = analysis['source_analysis']['extraction_methods']
            best_method = max(methods, key=methods.get) if methods else "unknown"
            insights["key_insights"].append(f"Most effective extraction method: {best_method}")
        
        # Generate recommendations
        if len(sites) < 5:
            insights["recommendations"].append("Consider increasing the number of sources for more comprehensive analysis")
        
        if analysis.get('content_metrics', {}).get('total_content', 0) < 10000:
            insights["recommendations"].append("Content volume is low - expand search scope or sources")
        
        # Future directions
        insights["future_directions"].extend([
            "Consider longitudinal analysis for trend identification",
            "Explore comparative analysis with related topics",
            "Investigate emerging subtopics within the research area"
        ])
        
        return insights
    
    async def _generate_reports(self, extraction_results: Dict, analysis_results: Dict, 
                              insights: Dict, topic: str, strategy: Dict) -> List[Dict]:
        """Generate comprehensive reports based on research data"""
        reports = []
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        topic_safe = topic.replace(' ', '_').replace('/', '_')[:30]
        
        # Comprehensive PDF Report
        if "pdf" in strategy.get('output_types', []):
            try:
                pdf_filename = f"super_agent_{topic_safe}_{timestamp}.pdf"
                pdf_path = self.output_dir / "reports" / pdf_filename
                
                # Prepare comprehensive data for PDF
                pdf_data = {
                    'topic': topic,
                    'sites': extraction_results.get('sites', []),
                    'analysis': analysis_results,
                    'insights': insights,
                    'strategy': strategy,
                    'timestamp': timestamp
                }
                
                self.pdf_generator.create_enhanced_web_extraction_pdf(pdf_data, str(pdf_path))
                reports.append({
                    'type': 'comprehensive_pdf',
                    'path': str(pdf_path),
                    'size': pdf_path.stat().st_size if pdf_path.exists() else 0
                })
                print(f"✅ Comprehensive PDF: {pdf_path}")
                
            except Exception as e:
                print(f"❌ PDF generation failed: {e}")
        
        # JSON Data Export
        if "json" in strategy.get('output_types', []):
            json_filename = f"super_agent_{topic_safe}_{timestamp}.json"
            json_path = self.output_dir / "data" / json_filename
            
            comprehensive_data = {
                'topic': topic,
                'extraction': extraction_results,
                'analysis': analysis_results,
                'insights': insights,
                'strategy': strategy,
                'timestamp': timestamp
            }
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(comprehensive_data, f, indent=2, ensure_ascii=False)
            
            reports.append({
                'type': 'json_data',
                'path': str(json_path),
                'size': json_path.stat().st_size if json_path.exists() else 0
            })
            print(f"✅ JSON Data: {json_path}")
        
        # Insights Report
        if "insights" in strategy.get('output_types', []):
            insights_filename = f"insights_{topic_safe}_{timestamp}.json"
            insights_path = self.output_dir / "insights" / insights_filename
            
            with open(insights_path, 'w', encoding='utf-8') as f:
                json.dump(insights, f, indent=2, ensure_ascii=False)
            
            reports.append({
                'type': 'insights_report',
                'path': str(insights_path),
                'size': insights_path.stat().st_size if insights_path.exists() else 0
            })
            print(f"✅ Insights Report: {insights_path}")
        
        return reports
    
    def display_comprehensive_results(self, results: Dict):
        """Display comprehensive research results"""
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE RESEARCH RESULTS")
        print("=" * 80)
        
        topic = results.get('topic', 'Unknown')
        extraction = results.get('extraction', {})
        analysis = results.get('analysis', {})
        insights = results.get('insights', {})
        reports = results.get('reports', [])
        metrics = results.get('performance_metrics', {})
        
        print(f"🎯 Topic: {topic}")
        print(f"📈 Sites analyzed: {metrics.get('total_sites', 0)}")
        print(f"📝 Total content: {metrics.get('total_content', 0):,} characters")
        print(f"💡 Insights generated: {metrics.get('insight_count', 0)}")
        print(f"📄 Reports created: {metrics.get('report_count', 0)}")
        
        # Content Analysis Summary
        if analysis.get('content_metrics'):
            cm = analysis['content_metrics']
            print(f"\n📊 CONTENT ANALYSIS:")
            print(f"   Average content per site: {cm.get('average_content', 0):.0f} characters")
            print(f"   Content range: {cm.get('min_content', 0):,} - {cm.get('max_content', 0):,} characters")
        
        # Source Analysis
        if analysis.get('source_analysis'):
            sa = analysis['source_analysis']
            print(f"\n🌐 SOURCE ANALYSIS:")
            print(f"   Unique domains: {sa.get('unique_domains', 0)}")
            print(f"   Extraction methods: {', '.join(sa.get('extraction_methods', {}).keys())}")
        
        # Key Insights
        if insights.get('key_insights'):
            print(f"\n💡 KEY INSIGHTS:")
            for i, insight in enumerate(insights['key_insights'][:5], 1):
                print(f"   {i}. {insight}")
        
        # Recommendations
        if insights.get('recommendations'):
            print(f"\n🎯 RECOMMENDATIONS:")
            for i, rec in enumerate(insights['recommendations'][:3], 1):
                print(f"   {i}. {rec}")
        
        # Generated Reports
        if reports:
            print(f"\n📁 GENERATED REPORTS:")
            for report in reports:
                size_kb = report.get('size', 0) / 1024
                print(f"   📄 {report['type']}: {report['path']} ({size_kb:.1f} KB)")
        
        print("\n" + "=" * 80)
    
    async def run_interactive_mode(self):
        """Run the enhanced super agent in interactive mode"""
        while True:
            self.clear_screen()
            self.print_banner()
            
            print("\n🎯 ENHANCED SUPER AGENT MENU:")
            print("1. 🔬 Advanced Research")
            print("2. 📊 View Research History")
            print("3. 🛠️  Agent Configuration")
            print("4. 📁 View Outputs")
            print("5. ❓ Help & Documentation")
            print("6. 🚪 Exit")
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == "1":
                await self._handle_advanced_research()
            elif choice == "2":
                self._show_research_history()
            elif choice == "3":
                self._configure_agent()
            elif choice == "4":
                self._show_outputs()
            elif choice == "5":
                self._show_help()
            elif choice == "6":
                print("\n👋 Thank you for using the Enhanced Super Agent!")
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
                input("Press Enter to continue...")
    
    async def _handle_advanced_research(self):
        """Handle advanced research request"""
        print("\n🔬 ADVANCED RESEARCH")
        print("-" * 30)
        
        topic = input("Enter research topic: ").strip()
        if not topic:
            print("❌ Topic cannot be empty!")
            input("Press Enter to continue...")
            return
        
        print("\n📊 COMPLEXITY LEVEL:")
        print("1. Simple (5 sites, basic analysis)")
        print("2. Medium (10 sites, comprehensive analysis)")
        print("3. Advanced (15 sites, deep analysis)")
        
        complexity_choice = input("Choose complexity (1-3, default 2): ").strip() or "2"
        complexity_map = {"1": "simple", "2": "medium", "3": "advanced"}
        complexity = complexity_map.get(complexity_choice, "medium")
        
        print(f"\n🚀 Starting {complexity} research on: {topic}")
        
        options = {'complexity': complexity}
        results = await self.perform_advanced_research(topic, options)
        
        if results and 'error' not in results:
            self.display_comprehensive_results(results)
            self.research_history.append({
                'topic': topic,
                'timestamp': datetime.now().isoformat(),
                'complexity': complexity,
                'results_summary': {
                    'sites': results.get('performance_metrics', {}).get('total_sites', 0),
                    'insights': results.get('performance_metrics', {}).get('insight_count', 0)
                }
            })
        else:
            print("❌ Research failed!")
        
        input("\nPress Enter to continue...")
    
    def _show_research_history(self):
        """Show research history"""
        print("\n📊 RESEARCH HISTORY")
        print("-" * 30)
        
        if not self.research_history:
            print("No research sessions found.")
        else:
            for i, session in enumerate(self.research_history[-10:], 1):  # Show last 10
                print(f"{i}. {session['topic']} ({session['complexity']}) - {session['timestamp'][:19]}")
                print(f"   Sites: {session['results_summary']['sites']}, Insights: {session['results_summary']['insights']}")
        
        input("\nPress Enter to continue...")
    
    def _configure_agent(self):
        """Configure agent settings"""
        print("\n🛠️  AGENT CONFIGURATION")
        print("-" * 30)
        
        print("Current capabilities:")
        for capability, enabled in self.capabilities.items():
            status = "✅" if enabled else "❌"
            print(f"   {status} {capability.replace('_', ' ').title()}")
        
        print("\nConfiguration options:")
        print("1. Toggle capabilities")
        print("2. Set output directory")
        print("3. Reset to defaults")
        
        choice = input("Choose option (1-3): ").strip()
        
        if choice == "1":
            print("\nToggle capabilities (enter capability name or 'all'):")
            capability = input("Capability: ").strip().lower()
            if capability == "all":
                for cap in self.capabilities:
                    self.capabilities[cap] = not self.capabilities[cap]
            elif capability in self.capabilities:
                self.capabilities[capability] = not self.capabilities[capability]
            print("✅ Capabilities updated!")
        
        input("\nPress Enter to continue...")
    
    def _show_outputs(self):
        """Show generated outputs"""
        print(f"\n📁 OUTPUT DIRECTORY: {self.output_dir.absolute()}")
        print("-" * 50)
        
        for subdir in ["reports", "data", "insights", "visualizations", "comparisons"]:
            subdir_path = self.output_dir / subdir
            if subdir_path.exists():
                files = list(subdir_path.glob("*"))
                if files:
                    print(f"\n{subdir.upper()}:")
                    for file in files[-5:]:  # Show last 5 files
                        size_kb = file.stat().st_size / 1024
                        print(f"   {file.name} ({size_kb:.1f} KB)")
        
        input("\nPress Enter to continue...")
    
    def _show_help(self):
        """Show help and documentation"""
        print("\n❓ HELP & DOCUMENTATION")
        print("-" * 30)
        print("Enhanced Super Agent Features:")
        print("• Advanced web extraction with multiple engines")
        print("• Intelligent content analysis and pattern recognition")
        print("• Automated insight generation and recommendations")
        print("• Comprehensive report generation (PDF, JSON, insights)")
        print("• Research history tracking and management")
        print("• Configurable capabilities and output options")
        print("\nUsage Tips:")
        print("• Use 'Advanced' complexity for in-depth research")
        print("• Check research history for previous sessions")
        print("• Configure capabilities based on your needs")
        print("• All outputs are saved in organized directories")
        
        input("\nPress Enter to continue...")

async def main():
    """Main entry point"""
    try:
        agent = EnhancedSuperAgent()
        await agent.run_interactive_mode()
    except KeyboardInterrupt:
        print("\n\n👋 Enhanced Super Agent interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 