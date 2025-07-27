#!/usr/bin/env python3
"""
Multi-Agent Research System
Specialized agents working together for comprehensive research
"""

import sys
import os
import json
import asyncio
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod
import time
import queue

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

try:
    from alternative_web_extractor import AlternativeWebExtractor
    from enhanced_pdf_generator import EnhancedPDFGenerator
except ImportError as e:
    print(f"Error importing core modules: {e}")
    sys.exit(1)

class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, name: str, capabilities: List[str]):
        self.name = name
        self.capabilities = capabilities
        self.status = "idle"
        self.work_queue = queue.Queue()
        self.results = {}
    
    @abstractmethod
    async def process_task(self, task: Dict) -> Dict:
        """Process a task and return results"""
        pass
    
    def get_status(self) -> Dict:
        """Get agent status"""
        return {
            "name": self.name,
            "status": self.status,
            "capabilities": self.capabilities,
            "queue_size": self.work_queue.qsize()
        }

class WebExtractionAgent(BaseAgent):
    """Specialized agent for web content extraction"""
    
    def __init__(self):
        super().__init__("WebExtractionAgent", ["web_extraction", "content_parsing"])
        self.extractor = AlternativeWebExtractor()
    
    async def process_task(self, task: Dict) -> Dict:
        """Extract web content based on task parameters"""
        self.status = "processing"
        
        try:
            topic = task.get('topic', '')
            max_sites = task.get('max_sites', 10)
            search_engines = task.get('search_engines', ['google', 'duckduckgo'])
            
            print(f"🔍 {self.name}: Extracting content for '{topic}'")
            
            # Perform extraction
            results = self.extractor.get_topic_data(topic)
            
            if results and 'error' not in results:
                self.status = "completed"
                return {
                    "agent": self.name,
                    "status": "success",
                    "data": results,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                self.status = "failed"
                return {
                    "agent": self.name,
                    "status": "failed",
                    "error": "Extraction failed",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            self.status = "failed"
            return {
                "agent": self.name,
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

class ContentAnalysisAgent(BaseAgent):
    """Specialized agent for content analysis"""
    
    def __init__(self):
        super().__init__("ContentAnalysisAgent", ["content_analysis", "pattern_recognition", "sentiment_analysis"])
    
    async def process_task(self, task: Dict) -> Dict:
        """Analyze content for patterns, insights, and trends"""
        self.status = "processing"
        
        try:
            sites = task.get('sites', [])
            topic = task.get('topic', '')
            
            print(f"🧠 {self.name}: Analyzing {len(sites)} sites for '{topic}'")
            
            analysis = {
                "content_metrics": self._analyze_content_metrics(sites),
                "topic_coverage": self._analyze_topic_coverage(sites, topic),
                "source_diversity": self._analyze_source_diversity(sites),
                "content_quality": self._analyze_content_quality(sites),
                "trend_analysis": self._analyze_trends(sites, topic)
            }
            
            self.status = "completed"
            return {
                "agent": self.name,
                "status": "success",
                "data": analysis,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.status = "failed"
            return {
                "agent": self.name,
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _analyze_content_metrics(self, sites: List[Dict]) -> Dict:
        """Analyze basic content metrics"""
        if not sites:
            return {}
        
        content_lengths = [site.get('content_length', 0) for site in sites]
        return {
            "total_sites": len(sites),
            "total_content": sum(content_lengths),
            "average_content": sum(content_lengths) / len(content_lengths),
            "max_content": max(content_lengths),
            "min_content": min(content_lengths),
            "content_distribution": {
                "short": len([l for l in content_lengths if l < 1000]),
                "medium": len([l for l in content_lengths if 1000 <= l < 5000]),
                "long": len([l for l in content_lengths if l >= 5000])
            }
        }
    
    def _analyze_topic_coverage(self, sites: List[Dict], topic: str) -> Dict:
        """Analyze how well sites cover the topic"""
        topic_words = set(topic.lower().split())
        coverage_scores = []
        
        for site in sites:
            title = site.get('title', '').lower()
            content = site.get('content', '').lower()
            
            title_matches = sum(1 for word in topic_words if word in title)
            content_matches = sum(1 for word in topic_words if word in content)
            
            coverage_score = (title_matches * 2) + content_matches
            coverage_scores.append(coverage_score)
        
        return {
            "average_coverage": sum(coverage_scores) / len(coverage_scores) if coverage_scores else 0,
            "high_coverage_sites": len([s for s in coverage_scores if s >= 3]),
            "coverage_distribution": {
                "excellent": len([s for s in coverage_scores if s >= 5]),
                "good": len([s for s in coverage_scores if 3 <= s < 5]),
                "fair": len([s for s in coverage_scores if 1 <= s < 3]),
                "poor": len([s for s in coverage_scores if s < 1])
            }
        }
    
    def _analyze_source_diversity(self, sites: List[Dict]) -> Dict:
        """Analyze source diversity and credibility"""
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
        
        return {
            "unique_domains": len(domains),
            "domain_distribution": domains,
            "extraction_methods": methods,
            "top_domains": dict(sorted(domains.items(), key=lambda x: x[1], reverse=True)[:5])
        }
    
    def _analyze_content_quality(self, sites: List[Dict]) -> Dict:
        """Analyze content quality indicators"""
        quality_scores = []
        
        for site in sites:
            content = site.get('content', '')
            title = site.get('title', '')
            
            # Simple quality indicators
            score = 0
            
            # Content length score
            if len(content) > 2000:
                score += 30
            elif len(content) > 1000:
                score += 20
            elif len(content) > 500:
                score += 10
            
            # Title quality score
            if len(title) > 10 and len(title) < 100:
                score += 20
            
            # URL quality score
            url = site.get('url', '')
            if url and ('https://' in url or 'http://' in url):
                score += 10
            
            quality_scores.append(score)
        
        return {
            "average_quality": sum(quality_scores) / len(quality_scores) if quality_scores else 0,
            "high_quality_sites": len([s for s in quality_scores if s >= 50]),
            "quality_distribution": {
                "excellent": len([s for s in quality_scores if s >= 70]),
                "good": len([s for s in quality_scores if 50 <= s < 70]),
                "fair": len([s for s in quality_scores if 30 <= s < 50]),
                "poor": len([s for s in quality_scores if s < 30])
            }
        }
    
    def _analyze_trends(self, sites: List[Dict], topic: str) -> Dict:
        """Analyze trends and patterns in the content"""
        # Simple trend analysis based on content patterns
        trend_keywords = []
        common_phrases = []
        
        for site in sites:
            content = site.get('content', '').lower()
            title = site.get('title', '').lower()
            
            # Extract potential trend keywords (words that appear frequently)
            words = content.split()
            if len(words) > 50:  # Only analyze substantial content
                from collections import Counter
                word_counts = Counter(words)
                # Get most common words (excluding common stop words)
                stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
                trend_words = [word for word, count in word_counts.most_common(10) 
                             if word not in stop_words and len(word) > 3]
                trend_keywords.extend(trend_words[:3])
        
        return {
            "trend_keywords": list(set(trend_keywords))[:10],
            "content_patterns": {
                "average_title_length": sum(len(site.get('title', '')) for site in sites) / len(sites) if sites else 0,
                "content_types": {
                    "articles": len([s for s in sites if 'article' in s.get('title', '').lower()]),
                    "guides": len([s for s in sites if 'guide' in s.get('title', '').lower()]),
                    "tutorials": len([s for s in sites if 'tutorial' in s.get('title', '').lower()])
                }
            }
        }

class InsightGenerationAgent(BaseAgent):
    """Specialized agent for generating insights and recommendations"""
    
    def __init__(self):
        super().__init__("InsightGenerationAgent", ["insight_generation", "recommendation_engine", "pattern_analysis"])
    
    async def process_task(self, task: Dict) -> Dict:
        """Generate insights and recommendations based on analysis data"""
        self.status = "processing"
        
        try:
            extraction_data = task.get('extraction_data', {})
            analysis_data = task.get('analysis_data', {})
            topic = task.get('topic', '')
            
            print(f"💡 {self.name}: Generating insights for '{topic}'")
            
            insights = {
                "key_insights": self._generate_key_insights(extraction_data, analysis_data),
                "recommendations": self._generate_recommendations(extraction_data, analysis_data),
                "trends": self._identify_trends(extraction_data, analysis_data),
                "gaps": self._identify_gaps(extraction_data, analysis_data),
                "opportunities": self._identify_opportunities(extraction_data, analysis_data)
            }
            
            self.status = "completed"
            return {
                "agent": self.name,
                "status": "success",
                "data": insights,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.status = "failed"
            return {
                "agent": self.name,
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _generate_key_insights(self, extraction_data: Dict, analysis_data: Dict) -> List[str]:
        """Generate key insights from the data"""
        insights = []
        
        sites = extraction_data.get('sites', [])
        content_metrics = analysis_data.get('content_metrics', {})
        topic_coverage = analysis_data.get('topic_coverage', {})
        source_diversity = analysis_data.get('source_diversity', {})
        
        # Content insights
        if content_metrics:
            insights.append(f"Successfully analyzed {content_metrics.get('total_sites', 0)} sources")
            insights.append(f"Total content volume: {content_metrics.get('total_content', 0):,} characters")
            
            avg_content = content_metrics.get('average_content', 0)
            if avg_content > 2000:
                insights.append("Content depth is substantial, indicating comprehensive coverage")
            elif avg_content < 500:
                insights.append("Content is concise, may need additional sources for depth")
        
        # Coverage insights
        if topic_coverage:
            high_coverage = topic_coverage.get('high_coverage_sites', 0)
            insights.append(f"{high_coverage} sites have excellent topic coverage")
        
        # Source insights
        if source_diversity:
            unique_domains = source_diversity.get('unique_domains', 0)
            insights.append(f"Content sourced from {unique_domains} unique domains")
            
            if unique_domains >= 5:
                insights.append("Good source diversity indicates comprehensive research")
            else:
                insights.append("Limited source diversity - consider expanding sources")
        
        return insights
    
    def _generate_recommendations(self, extraction_data: Dict, analysis_data: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        sites = extraction_data.get('sites', [])
        content_metrics = analysis_data.get('content_metrics', {})
        topic_coverage = analysis_data.get('topic_coverage', {})
        
        # Content recommendations
        if len(sites) < 5:
            recommendations.append("Consider increasing the number of sources for more comprehensive analysis")
        
        if content_metrics.get('total_content', 0) < 10000:
            recommendations.append("Content volume is low - expand search scope or sources")
        
        # Coverage recommendations
        if topic_coverage.get('coverage_distribution', {}).get('poor', 0) > len(sites) * 0.3:
            recommendations.append("Refine search terms for better topic alignment")
        
        # Quality recommendations
        if content_metrics.get('content_distribution', {}).get('short', 0) > len(sites) * 0.5:
            recommendations.append("Focus on sources with more detailed content")
        
        return recommendations
    
    def _identify_trends(self, extraction_data: Dict, analysis_data: Dict) -> List[str]:
        """Identify trends in the data"""
        trends = []
        
        trend_analysis = analysis_data.get('trend_analysis', {})
        trend_keywords = trend_analysis.get('trend_keywords', [])
        
        if trend_keywords:
            trends.append(f"Emerging keywords: {', '.join(trend_keywords[:5])}")
        
        content_types = trend_analysis.get('content_patterns', {}).get('content_types', {})
        if content_types.get('tutorials', 0) > 0:
            trends.append("Tutorial content is prominent in this topic")
        if content_types.get('guides', 0) > 0:
            trends.append("Guide-style content is common")
        
        return trends
    
    def _identify_gaps(self, extraction_data: Dict, analysis_data: Dict) -> List[str]:
        """Identify gaps in the research"""
        gaps = []
        
        topic_coverage = analysis_data.get('topic_coverage', {})
        coverage_dist = topic_coverage.get('coverage_distribution', {})
        
        if coverage_dist.get('poor', 0) > 0:
            gaps.append(f"{coverage_dist['poor']} sources have poor topic relevance")
        
        source_diversity = analysis_data.get('source_diversity', {})
        if source_diversity.get('unique_domains', 0) < 3:
            gaps.append("Limited source diversity")
        
        return gaps
    
    def _identify_opportunities(self, extraction_data: Dict, analysis_data: Dict) -> List[str]:
        """Identify opportunities for further research"""
        opportunities = []
        
        opportunities.extend([
            "Consider longitudinal analysis for trend identification",
            "Explore comparative analysis with related topics",
            "Investigate emerging subtopics within the research area",
            "Analyze content sentiment and public opinion trends"
        ])
        
        return opportunities

class ReportGenerationAgent(BaseAgent):
    """Specialized agent for generating comprehensive reports"""
    
    def __init__(self):
        super().__init__("ReportGenerationAgent", ["report_generation", "pdf_creation", "data_export"])
        self.pdf_generator = EnhancedPDFGenerator()
    
    async def process_task(self, task: Dict) -> Dict:
        """Generate comprehensive reports based on all agent results"""
        self.status = "processing"
        
        try:
            topic = task.get('topic', '')
            extraction_results = task.get('extraction_results', {})
            analysis_results = task.get('analysis_results', {})
            insights_results = task.get('insights_results', {})
            output_dir = task.get('output_dir', Path("multi_agent_outputs"))
            
            print(f"📄 {self.name}: Generating reports for '{topic}'")
            
            # Create output directory
            output_dir = Path(output_dir)
            output_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            topic_safe = topic.replace(' ', '_').replace('/', '_')[:30]
            
            reports = []
            
            # Generate comprehensive PDF
            pdf_filename = f"multi_agent_{topic_safe}_{timestamp}.pdf"
            pdf_path = output_dir / pdf_filename
            
            pdf_data = {
                'topic': topic,
                'extraction': extraction_results,
                'analysis': analysis_results,
                'insights': insights_results,
                'timestamp': timestamp
            }
            
            self.pdf_generator.create_enhanced_web_extraction_pdf(pdf_data, str(pdf_path))
            reports.append({
                'type': 'comprehensive_pdf',
                'path': str(pdf_path),
                'size': pdf_path.stat().st_size if pdf_path.exists() else 0
            })
            
            # Generate JSON summary
            json_filename = f"multi_agent_{topic_safe}_{timestamp}.json"
            json_path = output_dir / json_filename
            
            summary_data = {
                'topic': topic,
                'timestamp': timestamp,
                'extraction_summary': {
                    'sites': len(extraction_results.get('sites', [])),
                    'total_content': extraction_results.get('total_content_length', 0)
                },
                'analysis_summary': analysis_results,
                'insights_summary': insights_results
            }
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(summary_data, f, indent=2, ensure_ascii=False)
            
            reports.append({
                'type': 'json_summary',
                'path': str(json_path),
                'size': json_path.stat().st_size if json_path.exists() else 0
            })
            
            self.status = "completed"
            return {
                "agent": self.name,
                "status": "success",
                "data": {"reports": reports},
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.status = "failed"
            return {
                "agent": self.name,
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

class MultiAgentSystem:
    """Orchestrates multiple specialized agents for comprehensive research"""
    
    def __init__(self):
        """Initialize the multi-agent system"""
        self.agents = {
            "extraction": WebExtractionAgent(),
            "analysis": ContentAnalysisAgent(),
            "insights": InsightGenerationAgent(),
            "reports": ReportGenerationAgent()
        }
        
        self.output_dir = Path("multi_agent_outputs")
        self.output_dir.mkdir(exist_ok=True)
        
        self.research_sessions = []
    
    def get_system_status(self) -> Dict:
        """Get status of all agents"""
        return {
            "system": "MultiAgentSystem",
            "agents": {name: agent.get_status() for name, agent in self.agents.items()},
            "total_agents": len(self.agents)
        }
    
    async def perform_comprehensive_research(self, topic: str, options: Dict = None) -> Dict:
        """Perform comprehensive research using all agents"""
        print(f"🤖 Multi-Agent System: Starting comprehensive research on '{topic}'")
        print("=" * 60)
        
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        session_results = {
            "session_id": session_id,
            "topic": topic,
            "start_time": datetime.now().isoformat(),
            "agent_results": {},
            "final_results": {}
        }
        
        try:
            # Step 1: Web Extraction
            print("🔍 Step 1: Web Extraction Agent")
            extraction_task = {
                "topic": topic,
                "max_sites": options.get('max_sites', 10) if options else 10,
                "search_engines": options.get('search_engines', ['google', 'duckduckgo']) if options else ['google', 'duckduckgo']
            }
            
            extraction_results = await self.agents["extraction"].process_task(extraction_task)
            session_results["agent_results"]["extraction"] = extraction_results
            
            if extraction_results["status"] != "success":
                raise Exception(f"Extraction failed: {extraction_results.get('error', 'Unknown error')}")
            
            extraction_data = extraction_results["data"]
            print(f"✅ Extraction completed: {len(extraction_data.get('sites', []))} sites found")
            
            # Step 2: Content Analysis
            print("\n🧠 Step 2: Content Analysis Agent")
            analysis_task = {
                "sites": extraction_data.get('sites', []),
                "topic": topic
            }
            
            analysis_results = await self.agents["analysis"].process_task(analysis_task)
            session_results["agent_results"]["analysis"] = analysis_results
            
            if analysis_results["status"] != "success":
                raise Exception(f"Analysis failed: {analysis_results.get('error', 'Unknown error')}")
            
            analysis_data = analysis_results["data"]
            print(f"✅ Analysis completed: {len(analysis_data)} analysis categories")
            
            # Step 3: Insight Generation
            print("\n💡 Step 3: Insight Generation Agent")
            insights_task = {
                "extraction_data": extraction_data,
                "analysis_data": analysis_data,
                "topic": topic
            }
            
            insights_results = await self.agents["insights"].process_task(insights_task)
            session_results["agent_results"]["insights"] = insights_results
            
            if insights_results["status"] != "success":
                raise Exception(f"Insights generation failed: {insights_results.get('error', 'Unknown error')}")
            
            insights_data = insights_results["data"]
            print(f"✅ Insights generated: {len(insights_data.get('key_insights', []))} key insights")
            
            # Step 4: Report Generation
            print("\n📄 Step 4: Report Generation Agent")
            report_task = {
                "topic": topic,
                "extraction_results": extraction_data,
                "analysis_results": analysis_data,
                "insights_results": insights_data,
                "output_dir": self.output_dir
            }
            
            report_results = await self.agents["reports"].process_task(report_task)
            session_results["agent_results"]["reports"] = report_results
            
            if report_results["status"] != "success":
                raise Exception(f"Report generation failed: {report_results.get('error', 'Unknown error')}")
            
            reports_data = report_results["data"]
            print(f"✅ Reports generated: {len(reports_data.get('reports', []))} reports")
            
            # Compile final results
            session_results["final_results"] = {
                "topic": topic,
                "extraction_summary": {
                    "sites": len(extraction_data.get('sites', [])),
                    "total_content": extraction_data.get('total_content_length', 0)
                },
                "analysis_summary": analysis_data,
                "insights_summary": insights_data,
                "reports": reports_data.get('reports', []),
                "performance_metrics": {
                    "total_agents": len(self.agents),
                    "successful_agents": len([r for r in session_results["agent_results"].values() if r["status"] == "success"]),
                    "total_processing_time": time.time()
                }
            }
            
            session_results["end_time"] = datetime.now().isoformat()
            session_results["status"] = "completed"
            
            self.research_sessions.append(session_results)
            
            print("\n" + "=" * 60)
            print("🎉 Multi-Agent Research Completed Successfully!")
            print("=" * 60)
            
            return session_results
            
        except Exception as e:
            session_results["status"] = "failed"
            session_results["error"] = str(e)
            session_results["end_time"] = datetime.now().isoformat()
            
            print(f"\n❌ Multi-Agent Research Failed: {e}")
            return session_results
    
    def display_comprehensive_results(self, results: Dict):
        """Display comprehensive multi-agent results"""
        if results["status"] != "completed":
            print(f"❌ Research failed: {results.get('error', 'Unknown error')}")
            return
        
        final_results = results["final_results"]
        
        print("\n" + "=" * 80)
        print("📊 MULTI-AGENT RESEARCH RESULTS")
        print("=" * 80)
        
        print(f"🎯 Topic: {final_results['topic']}")
        print(f"🤖 Agents Used: {final_results['performance_metrics']['total_agents']}")
        print(f"✅ Successful Agents: {final_results['performance_metrics']['successful_agents']}")
        
        # Extraction Summary
        extraction = final_results['extraction_summary']
        print(f"\n🔍 EXTRACTION SUMMARY:")
        print(f"   Sites analyzed: {extraction['sites']}")
        print(f"   Total content: {extraction['total_content']:,} characters")
        
        # Analysis Summary
        analysis = final_results['analysis_summary']
        if analysis.get('content_metrics'):
            cm = analysis['content_metrics']
            print(f"\n🧠 ANALYSIS SUMMARY:")
            print(f"   Average content per site: {cm.get('average_content', 0):.0f} characters")
            print(f"   Content distribution: {cm.get('content_distribution', {})}")
        
        if analysis.get('source_diversity'):
            sd = analysis['source_diversity']
            print(f"   Unique domains: {sd.get('unique_domains', 0)}")
        
        # Insights Summary
        insights = final_results['insights_summary']
        if insights.get('key_insights'):
            print(f"\n💡 KEY INSIGHTS:")
            for i, insight in enumerate(insights['key_insights'][:5], 1):
                print(f"   {i}. {insight}")
        
        if insights.get('recommendations'):
            print(f"\n🎯 RECOMMENDATIONS:")
            for i, rec in enumerate(insights['recommendations'][:3], 1):
                print(f"   {i}. {rec}")
        
        # Reports Summary
        reports = final_results['reports']
        if reports:
            print(f"\n📁 GENERATED REPORTS:")
            for report in reports:
                size_kb = report.get('size', 0) / 1024
                print(f"   📄 {report['type']}: {report['path']} ({size_kb:.1f} KB)")
        
        print("\n" + "=" * 80)
    
    async def run_interactive_mode(self):
        """Run the multi-agent system in interactive mode"""
        while True:
            print("\n" + "=" * 80)
            print("🤖 MULTI-AGENT RESEARCH SYSTEM")
            print("=" * 80)
            print("Specialized agents working together for comprehensive research")
            print("=" * 80)
            
            print("\n🎯 MAIN MENU:")
            print("1. 🔬 Start Multi-Agent Research")
            print("2. 📊 View System Status")
            print("3. 📋 Research History")
            print("4. 📁 View Outputs")
            print("5. ❓ Help")
            print("6. 🚪 Exit")
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == "1":
                await self._handle_research_request()
            elif choice == "2":
                self._show_system_status()
            elif choice == "3":
                self._show_research_history()
            elif choice == "4":
                self._show_outputs()
            elif choice == "5":
                self._show_help()
            elif choice == "6":
                print("\n👋 Thank you for using the Multi-Agent Research System!")
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
                input("Press Enter to continue...")
    
    async def _handle_research_request(self):
        """Handle research request in interactive mode"""
        print("\n🔬 MULTI-AGENT RESEARCH")
        print("-" * 30)
        
        topic = input("Enter research topic: ").strip()
        if not topic:
            print("❌ Topic cannot be empty!")
            input("Press Enter to continue...")
            return
        
        print("\n📊 RESEARCH OPTIONS:")
        max_sites = input("Number of sites (default 10): ").strip() or "10"
        try:
            max_sites = int(max_sites)
        except ValueError:
            max_sites = 10
        
        print("\n🚀 Starting multi-agent research...")
        print("This will use all specialized agents for comprehensive analysis.")
        
        options = {
            'max_sites': max_sites,
            'search_engines': ['google', 'duckduckgo']
        }
        
        results = await self.perform_comprehensive_research(topic, options)
        self.display_comprehensive_results(results)
        
        input("\nPress Enter to continue...")
    
    def _show_system_status(self):
        """Show status of all agents"""
        print("\n📊 SYSTEM STATUS")
        print("-" * 30)
        
        status = self.get_system_status()
        print(f"System: {status['system']}")
        print(f"Total Agents: {status['total_agents']}")
        
        print("\nAgent Status:")
        for name, agent_status in status['agents'].items():
            status_icon = "✅" if agent_status['status'] == 'idle' else "🔄" if agent_status['status'] == 'processing' else "❌"
            print(f"   {status_icon} {name}: {agent_status['status']} (Queue: {agent_status['queue_size']})")
        
        input("\nPress Enter to continue...")
    
    def _show_research_history(self):
        """Show research history"""
        print("\n📋 RESEARCH HISTORY")
        print("-" * 30)
        
        if not self.research_sessions:
            print("No research sessions found.")
        else:
            for i, session in enumerate(self.research_sessions[-10:], 1):  # Show last 10
                status_icon = "✅" if session['status'] == 'completed' else "❌"
                print(f"{i}. {status_icon} {session['topic']} - {session['start_time'][:19]}")
                if session['status'] == 'completed':
                    extraction = session['final_results']['extraction_summary']
                    print(f"   Sites: {extraction['sites']}, Content: {extraction['total_content']:,} chars")
        
        input("\nPress Enter to continue...")
    
    def _show_outputs(self):
        """Show generated outputs"""
        print(f"\n📁 OUTPUT DIRECTORY: {self.output_dir.absolute()}")
        print("-" * 50)
        
        if self.output_dir.exists():
            files = list(self.output_dir.glob("*"))
            if files:
                for file in files[-10:]:  # Show last 10 files
                    size_kb = file.stat().st_size / 1024
                    print(f"   {file.name} ({size_kb:.1f} KB)")
            else:
                print("No output files found.")
        else:
            print("Output directory not found.")
        
        input("\nPress Enter to continue...")
    
    def _show_help(self):
        """Show help and documentation"""
        print("\n❓ HELP & DOCUMENTATION")
        print("-" * 30)
        print("Multi-Agent Research System Features:")
        print("• WebExtractionAgent: Specialized web content extraction")
        print("• ContentAnalysisAgent: Advanced content analysis and pattern recognition")
        print("• InsightGenerationAgent: Intelligent insight and recommendation generation")
        print("• ReportGenerationAgent: Comprehensive report creation")
        print("\nBenefits:")
        print("• Parallel processing for faster results")
        print("• Specialized expertise for each research phase")
        print("• Comprehensive analysis and insights")
        print("• Professional report generation")
        print("\nUsage:")
        print("• Each agent works independently on their specialized task")
        print("• Results are combined for comprehensive analysis")
        print("• Multiple output formats available")
        
        input("\nPress Enter to continue...")

async def main():
    """Main entry point for multi-agent system"""
    try:
        system = MultiAgentSystem()
        await system.run_interactive_mode()
    except KeyboardInterrupt:
        print("\n\n👋 Multi-Agent System interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 