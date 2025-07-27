import requests
import json
import time
from typing import Dict, List, Any, Optional
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from simple_comprehensive import get_topic_complete_data, save_complete_data
from pdf_generator import PDFGenerator
import nltk
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import networkx as nx
from datetime import datetime
import os


class KimiResearchAgent:
    def __init__(
        self, model_name: str = "moonshotai/Kimi-K2-Instruct", api_key: str = None
    ):
        """
        Initialize Kimi Research Agent

        Args:
            model_name: Hugging Face model name
            api_key: API key for external services
        """
        self.model_name = model_name
        self.api_key = api_key
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Initialize model and tokenizer
        print(f"🔄 Loading Kimi-K2 model... (Device: {self.device})")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto" if self.device == "cuda" else None,
            trust_remote_code=True,
        )

        # Download required NLTK data
        try:
            nltk.download("punkt", quiet=True)
            nltk.download("stopwords", quiet=True)
            nltk.download("vader_lexicon", quiet=True)
        except:
            pass

        print("✅ Kimi Research Agent initialized!")

    def generate_response(self, prompt: str, max_length: int = 2048) -> str:
        """
        Generate response using Kimi-K2 model

        Args:
            prompt: Input prompt
            max_length: Maximum response length

        Returns:
            Generated response
        """
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                )

            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response.replace(prompt, "").strip()

        except Exception as e:
            return f"Error generating response: {str(e)}"

    def analyze_topic_deep(self, topic: str, max_sites: int = 10) -> Dict:
        """
        Perform deep analysis of a topic using Kimi-K2

        Args:
            topic: Research topic
            max_sites: Number of sites to analyze

        Returns:
            Comprehensive analysis results
        """
        print(f"🔬 Starting deep analysis of: {topic}")

        # Step 1: Collect web data
        web_data = get_topic_complete_data(topic, max_sites)

        if "error" in web_data:
            return {"error": web_data["error"]}

        # Step 2: Generate research questions
        research_questions = self._generate_research_questions(topic, web_data)

        # Step 3: Analyze content with Kimi-K2
        analysis_results = self._analyze_content_with_kimi(
            topic, web_data, research_questions
        )

        # Step 4: Generate insights and recommendations
        insights = self._generate_insights(topic, web_data, analysis_results)

        # Step 5: Create visualizations
        visualizations = self._create_visualizations(web_data, analysis_results)

        # Step 6: Compile comprehensive report
        comprehensive_report = {
            "topic": topic,
            "timestamp": datetime.now().isoformat(),
            "web_data": web_data,
            "research_questions": research_questions,
            "analysis_results": analysis_results,
            "insights": insights,
            "visualizations": visualizations,
            "summary": self._generate_executive_summary(topic, insights),
        }

        return comprehensive_report

    def _generate_research_questions(self, topic: str, web_data: Dict) -> List[str]:
        """Generate research questions using Kimi-K2"""
        prompt = f"""
        As a research expert, generate 5-7 specific research questions for the topic: "{topic}"
        
        Based on the available web data, what are the key areas that need deeper investigation?
        
        Format your response as a numbered list of questions.
        """

        response = self.generate_response(prompt)
        questions = [
            q.strip()
            for q in response.split("\n")
            if q.strip() and any(c.isdigit() for c in q)
        ]
        return questions[:7]  # Limit to 7 questions

    def _analyze_content_with_kimi(
        self, topic: str, web_data: Dict, questions: List[str]
    ) -> Dict:
        """Analyze content using Kimi-K2 model"""
        print("🧠 Analyzing content with Kimi-K2...")

        # Combine all content for analysis
        all_content = " ".join(
            [site.get("content", "") for site in web_data.get("sites", [])]
        )

        analysis_results = {}

        # Analyze each research question
        for i, question in enumerate(questions):
            prompt = f"""
            Topic: {topic}
            Research Question: {question}
            
            Based on the following web content, provide a detailed analysis:
            
            {all_content[:5000]}  # Limit content length
            
            Provide:
            1. Key findings
            2. Supporting evidence
            3. Gaps in information
            4. Recommendations for further research
            """

            analysis = self.generate_response(prompt, max_length=1024)
            analysis_results[f"question_{i+1}"] = {
                "question": question,
                "analysis": analysis,
            }

        # Overall content analysis
        overall_prompt = f"""
        Topic: {topic}
        
        Analyze the following web content comprehensively:
        
        {all_content[:3000]}
        
        Provide:
        1. Main themes and patterns
        2. Key insights
        3. Credibility assessment
        4. Information gaps
        5. Emerging trends
        """

        overall_analysis = self.generate_response(overall_prompt, max_length=1500)
        analysis_results["overall_analysis"] = overall_analysis

        return analysis_results

    def _generate_insights(
        self, topic: str, web_data: Dict, analysis_results: Dict
    ) -> Dict:
        """Generate insights and recommendations"""
        print("💡 Generating insights...")

        # Sentiment analysis
        sentiments = []
        for site in web_data.get("sites", []):
            blob = TextBlob(site.get("content", ""))
            sentiments.append(blob.sentiment.polarity)

        # Key insights prompt
        insights_prompt = f"""
        Based on the analysis of "{topic}", provide:
        
        1. Key Insights (3-5 main findings)
        2. Trends and Patterns
        3. Recommendations for Action
        4. Future Research Directions
        5. Risk Assessment
        
        Analysis Summary: {analysis_results.get('overall_analysis', '')}
        """

        insights_text = self.generate_response(insights_prompt, max_length=1200)

        return {
            "text_insights": insights_text,
            "sentiment_analysis": {
                "average_sentiment": (
                    sum(sentiments) / len(sentiments) if sentiments else 0
                ),
                "sentiment_distribution": sentiments,
            },
            "content_metrics": {
                "total_sources": len(web_data.get("sites", [])),
                "total_content_length": web_data.get("total_content_length", 0),
                "average_content_length": (
                    web_data.get("total_content_length", 0)
                    // len(web_data.get("sites", []))
                    if web_data.get("sites")
                    else 0
                ),
            },
        }

    def _create_visualizations(self, web_data: Dict, analysis_results: Dict) -> Dict:
        """Create data visualizations"""
        print("📊 Creating visualizations...")

        viz_data = {}

        try:
            # Create output directory
            os.makedirs("visualizations", exist_ok=True)

            # 1. Content length distribution
            content_lengths = [
                site.get("content_length", 0) for site in web_data.get("sites", [])
            ]
            plt.figure(figsize=(10, 6))
            plt.hist(content_lengths, bins=10, alpha=0.7, color="skyblue")
            plt.title("Content Length Distribution")
            plt.xlabel("Content Length (characters)")
            plt.ylabel("Number of Sources")
            plt.savefig(
                "visualizations/content_distribution.png", dpi=300, bbox_inches="tight"
            )
            plt.close()
            viz_data["content_distribution"] = "visualizations/content_distribution.png"

            # 2. Source analysis
            sources = [
                site.get("source", "Unknown") for site in web_data.get("sites", [])
            ]
            source_counts = pd.Series(sources).value_counts()

            plt.figure(figsize=(12, 8))
            source_counts.plot(kind="bar")
            plt.title("Sources by Frequency")
            plt.xlabel("Source Domain")
            plt.ylabel("Number of Articles")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(
                "visualizations/source_analysis.png", dpi=300, bbox_inches="tight"
            )
            plt.close()
            viz_data["source_analysis"] = "visualizations/source_analysis.png"

            # 3. Word cloud from content
            all_text = " ".join(
                [site.get("content", "") for site in web_data.get("sites", [])]
            )
            wordcloud = WordCloud(
                width=800, height=400, background_color="white"
            ).generate(all_text)

            plt.figure(figsize=(10, 6))
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            plt.title("Content Word Cloud")
            plt.savefig("visualizations/wordcloud.png", dpi=300, bbox_inches="tight")
            plt.close()
            viz_data["wordcloud"] = "visualizations/wordcloud.png"

        except Exception as e:
            print(f"⚠️  Visualization error: {e}")
            viz_data["error"] = str(e)

        return viz_data

    def _generate_executive_summary(self, topic: str, insights: Dict) -> str:
        """Generate executive summary"""
        prompt = f"""
        Create a concise executive summary for research on "{topic}".
        
        Key insights: {insights.get('text_insights', '')}
        
        Provide a 2-3 paragraph executive summary suitable for business leaders.
        """

        return self.generate_response(prompt, max_length=800)

    def create_research_report(self, analysis_data: Dict, filename: str = None) -> str:
        """Create comprehensive research report"""
        if not filename:
            topic = analysis_data.get("topic", "research").replace(" ", "_").lower()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{topic}_deep_research_report_{timestamp}.pdf"

        generator = PDFGenerator()

        # Create custom PDF content
        report_content = self._format_report_content(analysis_data)

        # Generate PDF
        pdf_file = generator.create_text_to_pdf(
            report_content,
            f"Deep Research Report: {analysis_data.get('topic', 'Unknown')}",
            filename,
        )

        return pdf_file

    def _format_report_content(self, analysis_data: Dict) -> str:
        """Format analysis data for PDF report"""
        content = f"""
DEEP RESEARCH REPORT
Topic: {analysis_data.get('topic', 'Unknown')}
Generated: {analysis_data.get('timestamp', 'Unknown')}

EXECUTIVE SUMMARY
{analysis_data.get('summary', 'No summary available')}

RESEARCH QUESTIONS
"""

        for i, (key, value) in enumerate(
            analysis_data.get("research_questions", {}).items(), 1
        ):
            if isinstance(value, dict):
                content += f"\n{i}. {value.get('question', 'Unknown question')}\n"
                content += (
                    f"Analysis: {value.get('analysis', 'No analysis available')}\n"
                )

        content += f"\n\nKEY INSIGHTS\n{analysis_data.get('insights', {}).get('text_insights', 'No insights available')}"

        content += f"\n\nCONTENT METRICS\n"
        metrics = analysis_data.get("insights", {}).get("content_metrics", {})
        for key, value in metrics.items():
            content += f"{key.replace('_', ' ').title()}: {value}\n"

        return content


def main():
    """Example usage of Kimi Research Agent"""
    print("🚀 Initializing Kimi Deep Research Agent...")

    # Initialize agent
    agent = KimiResearchAgent()

    # Example research topic
    topic = "artificial intelligence in healthcare"

    print(f"\n🔬 Starting deep research on: {topic}")

    # Perform deep analysis
    analysis = agent.analyze_topic_deep(topic, max_sites=5)

    if "error" not in analysis:
        # Save analysis
        filename = f"{topic.replace(' ', '_')}_deep_analysis.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)

        print(f"✅ Analysis saved to: {filename}")

        # Generate PDF report
        pdf_file = agent.create_research_report(analysis)
        print(f"✅ PDF report generated: {pdf_file}")

        # Show summary
        print(f"\n📊 RESEARCH SUMMARY:")
        print(f"Topic: {analysis.get('topic')}")
        print(f"Sources analyzed: {len(analysis.get('web_data', {}).get('sites', []))}")
        print(f"Research questions: {len(analysis.get('research_questions', []))}")
        print(f"Visualizations created: {len(analysis.get('visualizations', {}))}")

    else:
        print(f"❌ Error: {analysis['error']}")


if __name__ == "__main__":
    main()
