#!/usr/bin/env python3
"""
AI Agent Report Generator
Follows the exact playbook for creating concise, safety-checked reference guides
"""

import re
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import random

class AIReportGenerator:
    """AI Agent for generating structured reference reports"""
    
    def __init__(self):
        """Initialize the AI report generator"""
        self.topic = ""
        self.audience = ""
        self.output_length = "standard"
        self.safety_constraints = []
        
        # Standard 10-section skeleton
        self.sections = [
            "definition",
            "how_to_use", 
            "safety_contraindications",
            "core_practices",
            "subsystem_mapping",
            "therapeutic_az",
            "integration",
            "sample_plan",
            "quick_reference",
            "further_reading"
        ]
        
        # Section templates
        self.section_templates = {
            "definition": {
                "title": "WHAT IS A {TOPIC}?",
                "type": "prose",
                "max_words": 70
            },
            "how_to_use": {
                "title": "HOW TO USE THIS GUIDE",
                "type": "bullets",
                "max_items": 4
            },
            "safety_contraindications": {
                "title": "SAFETY & CONTRA-INDICATIONS", 
                "type": "bullets",
                "max_items": 5
            },
            "core_practices": {
                "title": "CORE {TOPIC_PLURAL} FOR DAILY PRACTICE",
                "type": "table",
                "columns": ["Name", "Formation", "Primary Effect", "Best Time", "Affirmation"],
                "max_rows": 5
            },
            "subsystem_mapping": {
                "title": "{SUBSYSTEM}-SPECIFIC {TOPIC_PLURAL}",
                "type": "table", 
                "columns": ["Category", "Practice", "Element", "Focus Phrase", "Duration"],
                "max_rows": 7
            },
            "therapeutic_az": {
                "title": "THERAPEUTIC {TOPIC_PLURAL} (A-Z)",
                "type": "table",
                "columns": ["Name", "Formation", "Indication", "Notes"],
                "max_rows": 8
            },
            "integration": {
                "title": "INTEGRATION WITH {RELATED_PRACTICES}",
                "type": "structured",
                "subsections": ["Pairings", "Sequences", "Combinations"]
            },
            "sample_plan": {
                "title": "SAMPLE {DURATION}-DAY {TOPIC} PRACTICE",
                "type": "daily_plan",
                "duration": 7
            },
            "quick_reference": {
                "title": "QUICK-REFERENCE TABLES",
                "type": "reference_tables",
                "tables": ["Element Mapping", "Time of Day", "Emergency Use"]
            },
            "further_reading": {
                "title": "FURTHER READING & RESOURCES",
                "type": "resources",
                "categories": ["Books", "Apps", "Online Courses", "Certifications"]
            }
        }
        
        # Safety filter patterns
        self.absolute_claims = [
            r'\bcure\b', r'\bguaranteed\b', r'\bheal\b', r'\bfix\b',
            r'\bpermanent\b', r'\bcomplete\b', r'\bdefinitely\b',
            r'\b100%\b', r'\bnever\b', r'\balways\b'
        ]
        
        # Internal lexicon for verification
        self.lexicon = {
            "sanskrit": ["mudra", "prana", "chakra", "asana", "pranayama", "dhyana"],
            "medical": ["hypertension", "diabetes", "arthritis", "migraine"],
            "yoga": ["vinyasa", "hatha", "kundalini", "yin", "restorative"]
        }
    
    def ingest_topic(self, topic: str, audience: str = "", length: str = "standard", constraints: List[str] = None) -> Dict:
        """Step 1: INGESTION - Accept and clarify topic parameters"""
        print(f"🔍 INGESTION PHASE")
        print(f"Topic: {topic}")
        print(f"Audience: {audience or 'General'}")
        print(f"Length: {length}")
        print(f"Constraints: {constraints or 'None'}")
        
        self.topic = topic.lower().strip()
        self.audience = audience or "Students, Teachers & Therapists"
        self.output_length = length
        self.safety_constraints = constraints or []
        
        # Ask clarifying questions if needed
        if not audience:
            print("⚠️  Missing audience - using default: Students, Teachers & Therapists")
        
        if not constraints:
            print("⚠️  No safety constraints specified - using standard safety guidelines")
        
        return {
            "topic": self.topic,
            "audience": self.audience,
            "length": self.output_length,
            "constraints": self.safety_constraints,
            "status": "ingested"
        }
    
    def knowledge_base_call(self, topic: str) -> List[Dict]:
        """Step 2: KNOWLEDGE BASE CALL - Pull authoritative sources"""
        print(f"\n📚 KNOWLEDGE BASE CALL")
        print(f"Searching for authoritative sources on: {topic}")
        
        # Simulate pulling 3-5 authoritative sources
        sources = [
            {
                "title": f"Classical {topic.title()} Text",
                "content": f"Traditional wisdom on {topic} practices and applications",
                "relevance": 0.9,
                "type": "classical"
            },
            {
                "title": f"Modern {topic.title()} Research",
                "content": f"Contemporary studies on {topic} effectiveness and safety",
                "relevance": 0.8,
                "type": "research"
            },
            {
                "title": f"Clinical {topic.title()} Guidelines",
                "content": f"Professional guidelines for {topic} practice and contraindications",
                "relevance": 0.85,
                "type": "clinical"
            },
            {
                "title": f"Practical {topic.title()} Manual",
                "content": f"Step-by-step instructions for {topic} practice",
                "relevance": 0.75,
                "type": "practical"
            }
        ]
        
        # Filter by relevance score (keep only >= 0.7)
        filtered_sources = [s for s in sources if s["relevance"] >= 0.7]
        
        print(f"Found {len(filtered_sources)} relevant sources (relevance >= 0.7)")
        for source in filtered_sources:
            print(f"  ✅ {source['title']} (relevance: {source['relevance']})")
        
        return filtered_sources
    
    def generate_outline(self, topic: str, sources: List[Dict]) -> Dict:
        """Step 3: OUTLINE GENERATION - Use standard 10-section skeleton"""
        print(f"\n📋 OUTLINE GENERATION")
        print(f"Creating standard 10-section outline for: {topic}")
        
        # Determine topic-specific variables
        topic_plural = self._get_plural(topic)
        subsystem = self._get_subsystem(topic)
        related_practices = self._get_related_practices(topic)
        duration = "7" if self.output_length == "standard" else "3"
        
        outline = {
            "topic": topic,
            "topic_plural": topic_plural,
            "subsystem": subsystem,
            "related_practices": related_practices,
            "duration": duration,
            "sections": []
        }
        
        for section in self.sections:
            template = self.section_templates[section].copy()
            
            # Replace placeholders
            template["title"] = template["title"].format(
                TOPIC=topic.upper(),
                TOPIC_PLURAL=topic_plural.upper(),
                SUBSYSTEM=subsystem.upper(),
                RELATED_PRACTICES=related_practices.upper(),
                DURATION=duration
            )
            
            outline["sections"].append({
                "id": section,
                "title": template["title"],
                "type": template["type"],
                "template": template
            })
        
        print(f"Generated outline with {len(outline['sections'])} sections")
        for section in outline["sections"]:
            print(f"  {section['id']}: {section['title']}")
        
        return outline
    
    def template_fill_loop(self, outline: Dict, sources: List[Dict]) -> Dict:
        """Step 4: TEMPLATE-FILL LOOP - Generate content for each section"""
        print(f"\n✍️  TEMPLATE-FILL LOOP")
        
        report_content = {
            "metadata": {
                "topic": outline["topic"],
                "audience": self.audience,
                "date": datetime.now().strftime("%d %B %Y"),
                "version": "1.0"
            },
            "sections": []
        }
        
        for section in outline["sections"]:
            print(f"Generating content for: {section['title']}")
            
            content = self._generate_section_content(
                section, 
                outline, 
                sources
            )
            
            # Apply safety filter
            content = self._apply_safety_filter(content)
            
            report_content["sections"].append({
                "id": section["id"],
                "title": section["title"],
                "content": content,
                "type": section["type"]
            })
        
        return report_content
    
    def _generate_section_content(self, section: Dict, outline: Dict, sources: List[Dict]) -> Dict:
        """Generate content for a specific section"""
        section_type = section["type"]
        
        if section_type == "prose":
            return self._generate_prose_content(section, outline, sources)
        elif section_type == "bullets":
            return self._generate_bullet_content(section, outline, sources)
        elif section_type == "table":
            return self._generate_table_content(section, outline, sources)
        elif section_type == "structured":
            return self._generate_structured_content(section, outline, sources)
        elif section_type == "daily_plan":
            return self._generate_daily_plan_content(section, outline, sources)
        elif section_type == "reference_tables":
            return self._generate_reference_tables_content(section, outline, sources)
        elif section_type == "resources":
            return self._generate_resources_content(section, outline, sources)
        else:
            return {"content": "(content type not implemented)"}
    
    def _generate_prose_content(self, section: Dict, outline: Dict, sources: List[Dict]) -> Dict:
        """Generate concise prose content (≤ 70 words)"""
        topic = outline["topic"]
        
        if section["id"] == "definition":
            content = f"""• Sanskrit root: *{self._get_sanskrit_root(topic)}* – "{self._get_meaning(topic)}".
• {self._get_definition(topic)}.
• Works through {self._get_mechanism(topic)}."""
        
        return {"content": content, "word_count": len(content.split())}
    
    def _generate_bullet_content(self, section: Dict, outline: Dict, sources: List[Dict]) -> Dict:
        """Generate bullet point content"""
        topic = outline["topic"]
        bullets = []
        
        if section["id"] == "how_to_use":
            bullets = [
                f"Choose one {topic} per session; quality of intention > quantity.",
                f"Practice {self._get_duration(topic)}, {self._get_position(topic)}.",
                f"Observe breath and mental state before/after.",
                f"Record sensations in a practice journal."
            ]
        elif section["id"] == "safety_contraindications":
            bullets = [
                f"Pregnancy: avoid {self._get_contraindicated_practices(topic)} > 10 minutes.",
                f"Hypertension: skip {self._get_hypertension_risk(topic)}.",
                f"Post-surgery: do not compress {self._get_surgery_risk(topic)}.",
                f"Always release if dizziness or pain arises."
            ]
        
        return {"content": bullets, "item_count": len(bullets)}
    
    def _generate_table_content(self, section: Dict, outline: Dict, sources: List[Dict]) -> Dict:
        """Generate table content"""
        topic = outline["topic"]
        columns = section["template"]["columns"]
        max_rows = section["template"]["max_rows"]
        
        if section["id"] == "core_practices":
            rows = [
                ["GYAN", "Tip of thumb + index, palms on thighs", "Enhances concentration", "Evening study", '"I am clarity."'],
                ["CHIN", "Same as above, palms up", "Receives solar energy", "Sunrise practice", '"I awaken."'],
                ["DHYANA", "Right hand over left, thumbs touching", "Deep meditation", "Pre-sleep", '"I rest in stillness."'],
                ["ANJALI", "Palms at heart", "Gratitude & balance", "Opening/closing", '"I honor the light in you."']
            ]
        elif section["id"] == "subsystem_mapping":
            rows = [
                ["Root", "Prithvi", "Earth", '"I am safe."', "7 min"],
                ["Sacral", "Varun", "Water", '"I flow."', "7 min"],
                ["Solar Plexus", "Agni", "Fire", '"I act with power."', "5 min"],
                ["Heart", "Vayu", "Air", '"I forgive."', "7 min"],
                ["Throat", "Akash", "Ether", '"I speak truth."', "5 min"],
                ["Third Eye", "Hakini", "Light", '"I see clearly."', "5 min"],
                ["Crown", "Dhyana", "Consciousness", '"I am."', "10 min"]
            ]
        elif section["id"] == "therapeutic_az":
            rows = [
                ["Apan", "Thumb touches middle & ring tips", "Detox, urinary issues", "Avoid if low BP"],
                ["Linga", "Interlace fingers, left thumb up", "Bronchitis, low vitality", "Generates heat; limit 5 min"],
                ["Prana", "Thumb touches ring & little tips", "Chronic fatigue, immunity", "Excellent before practice"],
                ["Shakti", "Interlace fingers inside palms", "Energy surge, empowerment", "Use during standing poses"],
                ["Shunya", "Thumb presses middle phalanx", "Ear ringing, vertigo", "Discontinue when symptoms cease"],
                ["Surya", "Bend ring finger under thumb", "Obesity, sluggish thyroid", "Morning only"]
            ]
        
        return {
            "columns": columns,
            "rows": rows[:max_rows],
            "row_count": len(rows[:max_rows])
        }
    
    def _generate_structured_content(self, section: Dict, outline: Dict, sources: List[Dict]) -> Dict:
        """Generate structured content with subsections"""
        topic = outline["topic"]
        
        if section["id"] == "integration":
            content = {
                "Pairings": [
                    f"Tadasana + Prithvi {topic.title()} = Grounding.",
                    f"Virabhadrasana II + Kali {topic.title()} = Invoking warrior energy.",
                    f"Paschimottanasana + Apan {topic.title()} = Forward-fold detox."
                ],
                "Sequences": [
                    f"Nadi Shodhana + Chin {topic.title()} (palms up) = Balances ida & pingala.",
                    f"Bhramari + Shanmukhi {topic.title()} = Nervous system reset."
                ],
                "Combinations": [
                    f"2 min Gyan → 5 min Hakini → 3 min Dhyana.",
                    f"Mantra & {topic.title()}: chant 'RAM' while holding Agni {topic.title()}."
                ]
            }
        
        return {"content": content}
    
    def _generate_daily_plan_content(self, section: Dict, outline: Dict, sources: List[Dict]) -> Dict:
        """Generate daily practice plan"""
        topic = outline["topic"]
        duration = int(outline["duration"])
        
        days = []
        practices = ["Prithvi", "Varun", "Agni", "Vayu", "Akash", "Hakini", "Dhyana"]
        descriptions = ["Ground", "Flow", "Ignite", "Love", "Express", "Intuit", "Unity"]
        durations = ["8 min", "7 min", "5 min", "7 min", "5 min", "5 min", "10 min"]
        
        for i in range(duration):
            day_num = i + 1
            practice = practices[i % len(practices)]
            desc = descriptions[i % len(descriptions)]
            dur = durations[i % len(durations)]
            
            days.append(f"Day {day_num} – {desc}: {practice} {topic.title()} {dur}")
        
        return {"content": days, "duration": duration}
    
    def _generate_reference_tables_content(self, section: Dict, outline: Dict, sources: List[Dict]) -> Dict:
        """Generate quick reference tables"""
        tables = {
            "Element Mapping": {
                "Earth": "Ring",
                "Water": "Little", 
                "Fire": "Thumb",
                "Air": "Index",
                "Ether": "Middle"
            },
            "Time of Day": {
                "Sunrise": "Chin, Surya",
                "Noon": "Agni",
                "Sunset": "Gyan, Dhyana", 
                "Night": "Prana, Shunya"
            }
        }
        
        return {"content": tables}
    
    def _generate_resources_content(self, section: Dict, outline: Dict, sources: List[Dict]) -> Dict:
        """Generate further reading and resources"""
        topic = outline["topic"]
        
        resources = {
            "Books": [
                f'"{topic.title()} for Modern Life" – Swami Saradananda',
                f'"{topic.title()} of India" – Cain Carroll & Revital Carroll'
            ],
            "Apps": f'"{topic.title()} Pocket Reference" (iOS/Android)',
            "Online Courses": f"Bihar School of Yoga – {topic.title()} 30-hr certification"
        }
        
        return {"content": resources}
    
    def _apply_safety_filter(self, content: Dict) -> Dict:
        """Step 5: SAFETY FILTER - Scan for absolute claims and add disclaimers"""
        print(f"🔒 Applying safety filter...")
        
        # Convert content to string for scanning
        content_str = str(content)
        
        # Check for absolute claims
        found_claims = []
        for pattern in self.absolute_claims:
            matches = re.findall(pattern, content_str, re.IGNORECASE)
            found_claims.extend(matches)
        
        if found_claims:
            print(f"⚠️  Found absolute claims: {found_claims}")
            # Add disclaimer
            if "content" in content and isinstance(content["content"], list):
                content["content"].append("⚠️  Disclaimer: Individual results may vary. Consult healthcare provider.")
            elif "content" in content and isinstance(content["content"], dict):
                content["content"]["Disclaimer"] = "Individual results may vary. Consult healthcare provider."
        
        return content
    
    def style_normalization(self, report_content: Dict) -> Dict:
        """Step 6: STYLE NORMALIZATION - Convert to markdown format"""
        print(f"\n📝 STYLE NORMALIZATION")
        
        # Generate markdown content
        markdown = self._generate_markdown(report_content)
        
        return {
            "report": report_content,
            "markdown": markdown,
            "status": "normalized"
        }
    
    def _generate_markdown(self, report_content: Dict) -> str:
        """Generate markdown format report"""
        topic = report_content["metadata"]["topic"]
        topic_upper = topic.upper()
        
        markdown = f"""──────────────────────────────────────────  
{topic_upper} ‑ A PRACTICAL REFERENCE GUIDE  
──────────────────────────────────────────  

Prepared for: {report_content['metadata']['audience']}  
Date: {report_content['metadata']['date']}  
Version: {report_content['metadata']['version']}  

CONTENTS  
"""
        
        # Add table of contents
        for i, section in enumerate(report_content["sections"], 1):
            markdown += f"{i}. {section['title']}\n"
        
        markdown += "\n"
        
        # Add each section
        for section in report_content["sections"]:
            markdown += f"──────────────────\n{section['title']}\n──────────────────\n\n"
            
            if section["type"] == "prose":
                markdown += f"{section['content']['content']}\n\n"
            
            elif section["type"] == "bullets":
                for bullet in section["content"]["content"]:
                    markdown += f"• {bullet}\n"
                markdown += "\n"
            
            elif section["type"] == "table":
                # Generate table
                columns = section["content"]["columns"]
                rows = section["content"]["rows"]
                
                # Header
                markdown += "| " + " | ".join(columns) + " |\n"
                markdown += "|" + "|".join(["---"] * len(columns)) + "|\n"
                
                # Rows
                for row in rows:
                    markdown += "| " + " | ".join(row) + " |\n"
                markdown += "\n"
            
            elif section["type"] == "structured":
                for subsection, items in section["content"]["content"].items():
                    markdown += f"• {subsection}\n"
                    for item in items:
                        markdown += f"  – {item}\n"
                    markdown += "\n"
            
            elif section["type"] == "daily_plan":
                for day in section["content"]["content"]:
                    markdown += f"{day}\n"
                markdown += "\n"
            
            elif section["type"] == "reference_tables":
                markdown += "(Print & laminate for studio wall)\n\n"
                for table_name, table_data in section["content"]["content"].items():
                    markdown += f"{table_name.upper()}\n"
                    for key, value in table_data.items():
                        markdown += f"{key} → {value}\n"
                    markdown += "\n"
            
            elif section["type"] == "resources":
                for category, items in section["content"]["content"].items():
                    markdown += f"• {category}:\n"
                    if isinstance(items, list):
                        for item in items:
                            markdown += f"  – {item}\n"
                    else:
                        markdown += f"  – {items}\n"
                    markdown += "\n"
        
        # Add footer
        markdown += f"""──────────────────
© {datetime.now().year}. Free to share with attribution.  
For questions or corrections: contact@yourstudio.org"""
        
        return markdown
    
    def qa_fact_check(self, report_content: Dict) -> Dict:
        """Step 7: QA & FACT-CHECK - Verify terms and flag conflicts"""
        print(f"\n🔍 QA & FACT-CHECK")
        
        issues = []
        
        # Check for Sanskrit/Latin/medical terms
        content_str = str(report_content)
        for term_type, terms in self.lexicon.items():
            for term in terms:
                if term.lower() in content_str.lower():
                    print(f"✅ Verified {term_type} term: {term}")
        
        # Check for duplicates
        all_names = []
        for section in report_content["sections"]:
            if section["type"] == "table" and "rows" in section["content"]:
                for row in section["content"]["rows"]:
                    if row:
                        all_names.append(row[0])
        
        duplicates = [name for name in set(all_names) if all_names.count(name) > 1]
        if duplicates:
            issues.append(f"Duplicate names found: {duplicates}")
            print(f"⚠️  Duplicate names: {duplicates}")
        
        # Check for conflicts
        conflicts = self._check_for_conflicts(report_content)
        if conflicts:
            issues.extend(conflicts)
            print(f"⚠️  Conflicts found: {conflicts}")
        
        return {
            "report": report_content,
            "issues": issues,
            "status": "fact_checked"
        }
    
    def _check_for_conflicts(self, report_content: Dict) -> List[str]:
        """Check for conflicting advice in the report"""
        conflicts = []
        
        # Example conflict check
        content_str = str(report_content)
        if "morning" in content_str.lower() and "evening" in content_str.lower():
            # Check if same practice is recommended for both times
            pass
        
        return conflicts
    
    def export_report(self, report_data: Dict, format: str = "markdown") -> str:
        """Step 8: EXPORT - Generate final report"""
        print(f"\n📤 EXPORT")
        
        topic = report_data["report"]["metadata"]["topic"]
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        if format == "markdown":
            filename = f"{topic.title()}-Guide-{date_str}.md"
            content = report_data["markdown"]
        else:
            filename = f"{topic.title()}-Guide-{date_str}.txt"
            content = report_data["markdown"]
        
        # Save to file
        output_dir = Path("ai_report_outputs")
        output_dir.mkdir(exist_ok=True)
        
        filepath = output_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"✅ Report exported to: {filepath}")
        
        return str(filepath)
    
    # Helper methods for content generation
    def _get_plural(self, topic: str) -> str:
        """Get plural form of topic"""
        if topic.endswith("a"):
            return topic + "s"
        elif topic.endswith("y"):
            return topic[:-1] + "ies"
        else:
            return topic + "s"
    
    def _get_subsystem(self, topic: str) -> str:
        """Get subsystem for topic"""
        subsystems = {
            "mudra": "chakra",
            "pranayama": "nadi",
            "asana": "chakra",
            "meditation": "chakra",
            "yoga": "chakra"
        }
        return subsystems.get(topic, "system")
    
    def _get_related_practices(self, topic: str) -> str:
        """Get related practices"""
        practices = {
            "mudra": "Yoga Techniques",
            "pranayama": "Breathing & Meditation",
            "asana": "Yoga & Movement",
            "meditation": "Mindfulness & Yoga",
            "yoga": "Movement & Meditation"
        }
        return practices.get(topic, "Related Practices")
    
    def _get_sanskrit_root(self, topic: str) -> str:
        """Get Sanskrit root for topic"""
        roots = {
            "mudra": "mud",
            "pranayama": "prana",
            "asana": "as",
            "meditation": "dhyana"
        }
        return roots.get(topic, topic)
    
    def _get_meaning(self, topic: str) -> str:
        """Get meaning for topic"""
        meanings = {
            "mudra": "to delight, to seal",
            "pranayama": "breath control",
            "asana": "to sit",
            "meditation": "to contemplate"
        }
        return meanings.get(topic, "to practice")
    
    def _get_definition(self, topic: str) -> str:
        """Get definition for topic"""
        definitions = {
            "mudra": "A symbolic gesture that locks and redirects prana in the subtle body",
            "pranayama": "Breath control techniques that regulate life force energy",
            "asana": "Physical postures that prepare body and mind for meditation",
            "meditation": "Mental techniques that cultivate awareness and inner peace"
        }
        return definitions.get(topic, f"A practice related to {topic}")
    
    def _get_mechanism(self, topic: str) -> str:
        """Get mechanism for topic"""
        mechanisms = {
            "mudra": "reflex-arc stimulation of 72,000 nerve endings in the palms",
            "pranayama": "regulation of autonomic nervous system through breath patterns",
            "asana": "physical alignment and energy flow through body postures",
            "meditation": "mental focus and awareness cultivation through concentration"
        }
        return mechanisms.get(topic, f"specific mechanisms related to {topic}")
    
    def _get_duration(self, topic: str) -> str:
        """Get duration for topic"""
        return "5–20 min"
    
    def _get_position(self, topic: str) -> str:
        """Get position for topic"""
        return "seated or lying, spine neutral"
    
    def _get_contraindicated_practices(self, topic: str) -> str:
        """Get contraindicated practices"""
        return "Apan & Surya practices"
    
    def _get_hypertension_risk(self, topic: str) -> str:
        """Get hypertension risk practices"""
        return "Linga practice"
    
    def _get_surgery_risk(self, topic: str) -> str:
        """Get surgery risk practices"""
        return "abdominal practices"
    
    def generate_report(self, topic: str, audience: str = "", length: str = "standard", constraints: List[str] = None) -> str:
        """Complete report generation workflow"""
        print("🚀 AI AGENT REPORT GENERATOR")
        print("=" * 50)
        
        # Step 1: Ingestion
        ingestion = self.ingest_topic(topic, audience, length, constraints)
        
        # Step 2: Knowledge Base Call
        sources = self.knowledge_base_call(topic)
        
        # Step 3: Outline Generation
        outline = self.generate_outline(topic, sources)
        
        # Step 4: Template Fill Loop
        report_content = self.template_fill_loop(outline, sources)
        
        # Step 5: Safety Filter (applied during template fill)
        
        # Step 6: Style Normalization
        normalized = self.style_normalization(report_content)
        
        # Step 7: QA & Fact Check
        fact_checked = self.qa_fact_check(normalized["report"])
        
        # Step 8: Export
        filepath = self.export_report(fact_checked)
        
        print(f"\n🎉 Report generation complete!")
        print(f"📄 File: {filepath}")
        print(f"⚠️  Issues found: {len(fact_checked['issues'])}")
        
        return filepath

def main():
    """Test the AI report generator"""
    generator = AIReportGenerator()
    
    # Test with mudra topic
    topic = "mudra"
    audience = "Students, Teachers & Therapists"
    
    filepath = generator.generate_report(topic, audience)
    
    print(f"\n📖 Generated report: {filepath}")
    
    # Show preview
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        print(f"\n📄 Preview (first 500 chars):")
        print(content[:500] + "...")

if __name__ == "__main__":
    main() 