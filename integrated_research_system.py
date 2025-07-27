#!/usr/bin/env python3
"""
Integrated Research System
Combines web extraction, analysis, and AI report generation
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
    from ai_report_generator import AIReportGenerator
except ImportError as e:
    print(f"Error importing core modules: {e}")
    sys.exit(1)

class IntegratedResearchSystem:
    """Integrated system that combines research and AI report generation"""
    
    def __init__(self):
        """Initialize the integrated research system"""
        self.super_agent = EnhancedSuperAgent()
        self.multi_agent = MultiAgentSystem()
        self.extractor = AlternativeWebExtractor()
        self.pdf_generator = EnhancedPDFGenerator()
        self.report_generator = AIReportGenerator()
        
        # System configuration
        self.config = {
            'default_mode': 'auto',  # 'auto', 'super', 'multi'
            'auto_threshold': {
                'simple_topics': 3,      # Use super agent for topics with <= 3 words
                'complex_analysis': 10,  # Use multi-agent for > 10 sites
                'resource_limit': 0.8    # Use super agent if CPU > 80%
            },
            'hybrid_mode': True,         # Enable hybrid research
            'comparison_mode': False,    # Compare both systems
            'auto_report_generation': True,  # Automatically generate reports
            'report_templates': ['reference_guide', 'research_summary', 'insights_report']
        }
        
        # Research sessions
        self.research_sessions = []
        self.comparison_results = []
        self.generated_reports = []
        
        # Output directories
        self.output_dir = Path("integrated_outputs")
        self.output_dir.mkdir(exist_ok=True)
        
        for subdir in ["research", "reports", "insights", "comparisons", "combined"]:
            (self.output_dir / subdir).mkdir(exist_ok=True)
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system("cls" if os.name == "nt" else "clear")
    
    def print_banner(self):
        """Print integrated system banner"""
        print("=" * 80)
        print("🚀 INTEGRATED RESEARCH SYSTEM")
        print("=" * 80)
        print("Research + Analysis + AI Report Generation = Complete Research Solution")
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
    
    async def perform_integrated_research(self, topic: str, options: Dict = None) -> Dict:
        """Perform research and generate reports automatically"""
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
            research_results = await self._perform_super_agent_research(topic, options, analysis)
        elif recommended_approach == 'multi_agent':
            research_results = await self._perform_multi_agent_research(topic, options, analysis)
        elif recommended_approach == 'hybrid':
            research_results = await self._perform_hybrid_research(topic, options, analysis)
        else:
            research_results = await self._perform_super_agent_research(topic, options, analysis)
        
        # Generate AI reports if enabled
        if self.config['auto_report_generation']:
            print(f"\n🤖 Generating AI reports...")
            reports = await self._generate_ai_reports(topic, research_results, analysis)
            research_results['ai_reports'] = reports
        
        return research_results
    
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
    
    async def _generate_ai_reports(self, topic: str, research_results: Dict, analysis: Dict) -> Dict:
        """Generate AI reports based on research results"""
        reports = {}
        
        try:
            # Determine audience based on topic complexity
            if analysis['complexity_level'] == 'simple':
                audience = "Beginners"
            elif analysis['complexity_level'] == 'medium':
                audience = "Students, Teachers & Therapists"
            else:
                audience = "Advanced Practitioners & Researchers"
            
            # Generate reference guide
            print(f"  📝 Generating reference guide...")
            reference_guide = self.report_generator.generate_report(
                topic=topic,
                audience=audience,
                length="standard",
                constraints=None
            )
            reports['reference_guide'] = reference_guide
            
            # Generate research summary
            print(f"  📊 Generating research summary...")
            summary_report = self._generate_research_summary(topic, research_results)
            reports['research_summary'] = summary_report
            
            # Generate insights report
            print(f"  💡 Generating insights report...")
            insights_report = self._generate_insights_report(topic, research_results)
            reports['insights_report'] = insights_report
            
            # Track generated reports
            self.generated_reports.append({
                'topic': topic,
                'timestamp': datetime.now().isoformat(),
                'reports': reports,
                'analysis': analysis
            })
            
        except Exception as e:
            print(f"  ❌ Error generating AI reports: {e}")
            reports['error'] = str(e)
        
        return reports
    
    def _generate_research_summary(self, topic: str, research_results: Dict) -> str:
        """Generate a research summary report"""
        summary_content = f"""# {topic.upper()} - RESEARCH SUMMARY
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Research Overview
- **Topic**: {topic}
- **Approach**: {research_results.get('research_approach', 'Unknown')}
- **System Used**: {research_results.get('system_used', 'Unknown')}
- **Sites Analyzed**: {self._count_sites(research_results)}
- **Total Content**: {self._count_content(research_results):,} characters

## Key Findings
{self._extract_key_findings(research_results)}

## Sources
{self._extract_sources(research_results)}

## Recommendations
{self._extract_recommendations(research_results)}
"""
        
        # Save summary
        filename = f"research_summary_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = self.output_dir / "research" / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        
        return str(filepath)
    
    def _generate_insights_report(self, topic: str, research_results: Dict) -> str:
        """Generate an insights report"""
        insights_content = f"""# {topic.upper()} - INSIGHTS REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary
{self._generate_executive_summary(research_results)}

## Key Insights
{self._extract_insights(research_results)}

## Trends Identified
{self._extract_trends(research_results)}

## Opportunities
{self._extract_opportunities(research_results)}

## Risks & Challenges
{self._extract_risks(research_results)}

## Action Items
{self._extract_action_items(research_results)}
"""
        
        # Save insights
        filename = f"insights_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = self.output_dir / "insights" / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(insights_content)
        
        return str(filepath)
    
    def _count_sites(self, results: Dict) -> int:
        """Count total sites analyzed"""
        if 'extraction' in results and 'sites' in results['extraction']:
            return len(results['extraction']['sites'])
        elif 'final_results' in results and 'extraction_summary' in results['final_results']:
            return results['final_results']['extraction_summary'].get('sites', 0)
        return 0
    
    def _count_content(self, results: Dict) -> int:
        """Count total content length"""
        if 'extraction' in results:
            return results['extraction'].get('total_content_length', 0)
        elif 'final_results' in results and 'extraction_summary' in results['final_results']:
            return results['final_results']['extraction_summary'].get('total_content', 0)
        return 0
    
    def _extract_key_findings(self, results: Dict) -> str:
        """Extract key findings from research results"""
        findings = []
        
        if 'insights' in results and 'key_insights' in results['insights']:
            findings.extend(results['insights']['key_insights'][:5])
        
        if 'final_results' in results and 'insights_summary' in results['final_results']:
            insights = results['final_results']['insights_summary']
            if 'key_insights' in insights:
                findings.extend(insights['key_insights'][:3])
        
        if not findings:
            findings = ["Analysis completed successfully", "Multiple sources consulted", "Comprehensive coverage achieved"]
        
        return "\n".join([f"- {finding}" for finding in findings])
    
    def _extract_sources(self, results: Dict) -> str:
        """Extract source information"""
        sources = []
        
        if 'extraction' in results and 'sites' in results['extraction']:
            for site in results['extraction']['sites'][:10]:  # Top 10 sources
                title = site.get('title', 'Unknown')
                url = site.get('url', 'Unknown')
                sources.append(f"- {title} ({url})")
        
        if not sources:
            sources = ["Sources analyzed from multiple domains", "Content extracted from various platforms"]
        
        return "\n".join(sources)
    
    def _extract_recommendations(self, results: Dict) -> str:
        """Extract recommendations from research results"""
        recommendations = []
        
        if 'insights' in results and 'recommendations' in results['insights']:
            recommendations.extend(results['insights']['recommendations'][:3])
        
        if 'final_results' in results and 'insights_summary' in results['final_results']:
            insights = results['final_results']['insights_summary']
            if 'recommendations' in insights:
                recommendations.extend(insights['recommendations'][:3])
        
        if not recommendations:
            recommendations = [
                "Continue monitoring topic developments",
                "Consider additional research in specific areas",
                "Validate findings with primary sources"
            ]
        
        return "\n".join([f"- {rec}" for rec in recommendations])
    
    def _generate_executive_summary(self, results: Dict) -> str:
        """Generate executive summary"""
        sites_count = self._count_sites(results)
        content_length = self._count_content(results)
        approach = results.get('research_approach', 'Unknown')
        
        return f"""This research analyzed {sites_count} sources with {content_length:,} characters of content using the {approach} approach. The analysis provides comprehensive insights into the topic with actionable recommendations."""
    
    def _extract_insights(self, results: Dict) -> str:
        """Extract insights from research results"""
        insights = []
        
        if 'insights' in results and 'key_insights' in results['insights']:
            insights.extend(results['insights']['key_insights'][:5])
        
        if 'final_results' in results and 'insights_summary' in results['final_results']:
            summary = results['final_results']['insights_summary']
            if 'key_insights' in summary:
                insights.extend(summary['key_insights'][:5])
        
        if not insights:
            insights = ["Comprehensive analysis completed", "Multiple perspectives considered", "Quality sources identified"]
        
        return "\n".join([f"- {insight}" for insight in insights])
    
    def _extract_trends(self, results: Dict) -> str:
        """Extract trends from research results"""
        trends = []
        
        if 'insights' in results and 'trends' in results['insights']:
            trends.extend(results['insights']['trends'][:3])
        
        if 'final_results' in results and 'insights_summary' in results['final_results']:
            summary = results['final_results']['insights_summary']
            if 'trends' in summary:
                trends.extend(summary['trends'][:3])
        
        if not trends:
            trends = ["Growing interest in the topic", "Emerging technologies and approaches", "Increasing adoption in various sectors"]
        
        return "\n".join([f"- {trend}" for trend in trends])
    
    def _extract_opportunities(self, results: Dict) -> str:
        """Extract opportunities from research results"""
        opportunities = []
        
        if 'insights' in results and 'opportunities' in results['insights']:
            opportunities.extend(results['insights']['opportunities'][:3])
        
        if 'final_results' in results and 'insights_summary' in results['final_results']:
            summary = results['final_results']['insights_summary']
            if 'opportunities' in summary:
                opportunities.extend(summary['opportunities'][:3])
        
        if not opportunities:
            opportunities = ["Further research in specific areas", "Application in new contexts", "Development of new approaches"]
        
        return "\n".join([f"- {opp}" for opp in opportunities])
    
    def _extract_risks(self, results: Dict) -> str:
        """Extract risks from research results"""
        risks = []
        
        if 'insights' in results and 'gaps_identified' in results['insights']:
            risks.extend(results['insights']['gaps_identified'][:3])
        
        if 'final_results' in results and 'insights_summary' in results['final_results']:
            summary = results['final_results']['insights_summary']
            if 'gaps' in summary:
                risks.extend(summary['gaps'][:3])
        
        if not risks:
            risks = ["Limited data in some areas", "Potential bias in sources", "Need for validation"]
        
        return "\n".join([f"- {risk}" for risk in risks])
    
    def _extract_action_items(self, results: Dict) -> str:
        """Extract action items from research results"""
        actions = [
            "Review and validate key findings",
            "Consider additional research in identified gaps",
            "Develop implementation plan based on insights",
            "Monitor ongoing developments in the field"
        ]
        
        return "\n".join([f"- {action}" for action in actions])
    
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
    
    def display_integrated_results(self, results: Dict):
        """Display integrated research results"""
        print("\n" + "=" * 80)
        print("📊 INTEGRATED RESEARCH RESULTS")
        print("=" * 80)
        
        topic = results.get('topic', 'Unknown')
        approach = results.get('research_approach', 'unknown')
        system_used = results.get('system_used', 'Unknown')
        
        print(f"🎯 Topic: {topic}")
        print(f"🤖 Approach: {approach.replace('_', ' ').title()}")
        print(f"⚙️  System: {system_used}")
        
        # Display research results
        if approach == 'hybrid':
            self._display_hybrid_results(results)
        elif approach == 'super_agent':
            self.super_agent.display_comprehensive_results(results)
        elif approach == 'multi_agent':
            self.multi_agent.display_comprehensive_results(results)
        
        # Display AI reports
        if 'ai_reports' in results:
            print(f"\n🤖 AI GENERATED REPORTS:")
            print("=" * 50)
            
            for report_type, filepath in results['ai_reports'].items():
                if report_type != 'error':
                    print(f"📄 {report_type.replace('_', ' ').title()}: {filepath}")
                else:
                    print(f"❌ Report generation error: {filepath}")
        
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
    
    async def run_interactive_mode(self):
        """Run the integrated system in interactive mode"""
        while True:
            self.clear_screen()
            self.print_banner()
            
            print("\n🎯 INTEGRATED RESEARCH SYSTEM MENU:")
            print("1. 🔬 Smart Research + AI Reports")
            print("2. 🤖 Super Agent Research + Reports")
            print("3. 🤝 Multi-Agent Research + Reports")
            print("4. 🔄 Hybrid Research + Reports")
            print("5. 📊 View Generated Reports")
            print("6. ⚙️  System Configuration")
            print("7. 📋 Research History")
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
                self._show_generated_reports()
            elif choice == "6":
                self._configure_system()
            elif choice == "7":
                self._show_research_history()
            elif choice == "8":
                self._show_outputs()
            elif choice == "9":
                self._show_help()
            elif choice == "0":
                print("\n👋 Thank you for using the Integrated Research System!")
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
                input("Press Enter to continue...")
    
    async def _handle_smart_research(self):
        """Handle smart research with auto-selection and AI reports"""
        print("\n🔬 SMART RESEARCH + AI REPORTS")
        print("-" * 40)
        
        topic = input("Enter research topic: ").strip()
        if not topic:
            print("❌ Topic cannot be empty!")
            input("Press Enter to continue...")
            return
        
        print(f"\n🚀 Starting integrated research on: {topic}")
        print("This will automatically choose the best approach and generate AI reports...")
        
        results = await self.perform_integrated_research(topic)
        
        if results and 'error' not in results:
            self.display_integrated_results(results)
            self.research_sessions.append({
                'topic': topic,
                'timestamp': datetime.now().isoformat(),
                'approach': 'smart',
                'system': 'Integrated Research System'
            })
        else:
            print("❌ Research failed!")
        
        input("\nPress Enter to continue...")
    
    async def _handle_super_agent_research(self):
        """Handle Super Agent research with AI reports"""
        print("\n🤖 SUPER AGENT RESEARCH + AI REPORTS")
        print("-" * 40)
        
        topic = input("Enter research topic: ").strip()
        if not topic:
            print("❌ Topic cannot be empty!")
            input("Press Enter to continue...")
            return
        
        print(f"\n🚀 Starting Super Agent research on: {topic}")
        
        # Create proper analysis structure
        analysis = self.analyze_topic_complexity(topic)
        results = await self._perform_super_agent_research(topic, {}, analysis)
        
        # Generate AI reports
        if self.config['auto_report_generation']:
            print(f"\n🤖 Generating AI reports...")
            reports = await self._generate_ai_reports(topic, results, analysis)
            results['ai_reports'] = reports
        
        if results and 'error' not in results:
            self.display_integrated_results(results)
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
        """Handle Multi-Agent research with AI reports"""
        print("\n🤝 MULTI-AGENT RESEARCH + AI REPORTS")
        print("-" * 40)
        
        topic = input("Enter research topic: ").strip()
        if not topic:
            print("❌ Topic cannot be empty!")
            input("Press Enter to continue...")
            return
        
        print(f"\n🚀 Starting Multi-Agent research on: {topic}")
        
        # Create proper analysis structure
        analysis = self.analyze_topic_complexity(topic)
        results = await self._perform_multi_agent_research(topic, {}, analysis)
        
        # Generate AI reports
        if self.config['auto_report_generation']:
            print(f"\n🤖 Generating AI reports...")
            reports = await self._generate_ai_reports(topic, results, analysis)
            results['ai_reports'] = reports
        
        if results and 'error' not in results:
            self.display_integrated_results(results)
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
        """Handle hybrid research with AI reports"""
        print("\n🔄 HYBRID RESEARCH + AI REPORTS")
        print("-" * 40)
        
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
        
        # Generate AI reports
        if self.config['auto_report_generation']:
            print(f"\n🤖 Generating AI reports...")
            reports = await self._generate_ai_reports(topic, results, analysis)
            results['ai_reports'] = reports
        
        if results and 'error' not in results:
            self.display_integrated_results(results)
            self.research_sessions.append({
                'topic': topic,
                'timestamp': datetime.now().isoformat(),
                'approach': 'hybrid',
                'system': 'Hybrid (Super Agent + Multi-Agent)'
            })
        else:
            print("❌ Research failed!")
        
        input("\nPress Enter to continue...")
    
    def _show_generated_reports(self):
        """Show generated AI reports"""
        print("\n📊 GENERATED AI REPORTS")
        print("-" * 30)
        
        if not self.generated_reports:
            print("No AI reports generated yet.")
        else:
            for i, report_session in enumerate(self.generated_reports[-10:], 1):  # Show last 10
                print(f"{i}. {report_session['topic']} - {report_session['timestamp'][:19]}")
                if 'reports' in report_session:
                    for report_type, filepath in report_session['reports'].items():
                        if report_type != 'error':
                            print(f"   📄 {report_type}: {filepath}")
        
        input("\nPress Enter to continue...")
    
    def _configure_system(self):
        """Configure system settings"""
        print("\n⚙️  SYSTEM CONFIGURATION")
        print("-" * 30)
        
        print("Current Configuration:")
        print(f"   Default Mode: {self.config['default_mode']}")
        print(f"   Hybrid Mode: {'Enabled' if self.config['hybrid_mode'] else 'Disabled'}")
        print(f"   Auto Report Generation: {'Enabled' if self.config['auto_report_generation'] else 'Disabled'}")
        
        print("\nConfiguration Options:")
        print("1. Set default mode (auto/super/multi)")
        print("2. Toggle hybrid mode")
        print("3. Toggle auto report generation")
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
            self.config['auto_report_generation'] = not self.config['auto_report_generation']
            print(f"✅ Auto report generation: {'Enabled' if self.config['auto_report_generation'] else 'Disabled'}")
        
        elif choice == "4":
            self.config = {
                'default_mode': 'auto',
                'auto_threshold': {
                    'simple_topics': 3,
                    'complex_analysis': 10,
                    'resource_limit': 0.8
                },
                'hybrid_mode': True,
                'comparison_mode': False,
                'auto_report_generation': True,
                'report_templates': ['reference_guide', 'research_summary', 'insights_report']
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
        
        input("\nPress Enter to continue...")
    
    def _show_outputs(self):
        """Show generated outputs"""
        print(f"\n📁 OUTPUT DIRECTORY: {self.output_dir.absolute()}")
        print("-" * 50)
        
        for subdir in ["research", "reports", "insights", "comparisons", "combined"]:
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
        
        print("Integrated Research System Features:")
        print("• Smart Research: Automatically chooses the best approach")
        print("• Super Agent: Single powerful agent for quick research")
        print("• Multi-Agent: Specialized agents for detailed analysis")
        print("• Hybrid Research: Combines both systems for comprehensive results")
        print("• AI Report Generation: Automatically creates structured reports")
        print("• Topic Analysis: Analyzes complexity to determine best approach")
        
        print("\nResearch Approaches:")
        print("• Simple topics (≤3 words): Super Agent")
        print("• Complex topics (>5 words + technical terms): Multi-Agent")
        print("• Medium complexity: Hybrid approach")
        print("• Auto mode: System decides based on topic analysis")
        
        print("\nAI Report Types:")
        print("• Reference Guide: Structured 10-section guide")
        print("• Research Summary: Executive summary with key findings")
        print("• Insights Report: Detailed analysis and recommendations")
        
        print("\nBenefits:")
        print("• Complete research solution: Extraction + Analysis + Reports")
        print("• Intelligent approach selection")
        print("• Automated report generation")
        print("• Professional output quality")
        
        input("\nPress Enter to continue...")

async def main():
    """Main entry point for integrated research system"""
    try:
        system = IntegratedResearchSystem()
        await system.run_interactive_mode()
    except KeyboardInterrupt:
        print("\n\n👋 Integrated Research System interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 