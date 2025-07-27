from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Image, ListFlowable, ListItem
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import KeepTogether
from datetime import datetime
import json
import os


class EnhancedPDFGenerator:
    def __init__(self):
        """Initialize enhanced PDF generator with custom styles"""
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()

    def _create_custom_styles(self):
        """Create custom paragraph styles for better formatting"""
        # Title style
        self.styles.add(
            ParagraphStyle(
                name="CustomTitle",
                parent=self.styles["Heading1"],
                fontSize=24,
                spaceAfter=30,
                alignment=TA_CENTER,
                textColor=colors.darkblue,
                fontName="Helvetica-Bold",
            )
        )

        # Subtitle style
        self.styles.add(
            ParagraphStyle(
                name="CustomSubtitle",
                parent=self.styles["Heading2"],
                fontSize=16,
                spaceAfter=20,
                spaceBefore=20,
                textColor=colors.darkblue,
                fontName="Helvetica-Bold",
            )
        )

        # Section header style
        self.styles.add(
            ParagraphStyle(
                name="SectionHeader",
                parent=self.styles["Heading3"],
                fontSize=14,
                spaceAfter=15,
                spaceBefore=15,
                textColor=colors.darkgreen,
                fontName="Helvetica-Bold",
            )
        )

        # Source title style
        self.styles.add(
            ParagraphStyle(
                name="SourceTitle",
                parent=self.styles["Normal"],
                fontSize=12,
                spaceAfter=8,
                spaceBefore=8,
                textColor=colors.darkblue,
                fontName="Helvetica-Bold",
                leftIndent=20,
            )
        )

        # Source content style
        self.styles.add(
            ParagraphStyle(
                name="SourceContent",
                parent=self.styles["Normal"],
                fontSize=10,
                spaceAfter=12,
                spaceBefore=8,
                leftIndent=30,
                rightIndent=20,
                alignment=TA_JUSTIFY,
                fontName="Helvetica",
            )
        )

        # Source link style
        self.styles.add(
            ParagraphStyle(
                name="SourceLink",
                parent=self.styles["Normal"],
                fontSize=9,
                spaceAfter=5,
                leftIndent=30,
                textColor=colors.blue,
                fontName="Helvetica-Oblique",
            )
        )

        # Summary style
        self.styles.add(
            ParagraphStyle(
                name="Summary",
                parent=self.styles["Normal"],
                fontSize=11,
                spaceAfter=15,
                spaceBefore=15,
                leftIndent=20,
                rightIndent=20,
                alignment=TA_JUSTIFY,
                fontName="Helvetica",
                backColor=colors.lightgrey,
            )
        )

        # Metrics style
        self.styles.add(
            ParagraphStyle(
                name="Metrics",
                parent=self.styles["Normal"],
                fontSize=10,
                spaceAfter=8,
                leftIndent=20,
                fontName="Helvetica-Bold",
            )
        )

    def create_enhanced_web_extraction_pdf(self, data, filename=None):
        """
        Create enhanced PDF report with better structure and numbered sources

        Args:
            data: Dictionary containing web extraction data
            filename: Output filename (optional)

        Returns:
            Generated PDF filename
        """
        if not filename:
            topic = data.get("topic", "web_extraction").replace(" ", "_").lower()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"enhanced_web_extraction_{topic}_{timestamp}.pdf"

        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
        )
        story = []

        # Title page
        story.extend(self._create_title_page(data))
        story.append(PageBreak())

        # Table of contents
        story.extend(self._create_table_of_contents(data))
        story.append(PageBreak())

        # Executive summary
        story.extend(self._create_executive_summary(data))
        story.append(PageBreak())

        # Detailed analysis
        story.extend(self._create_detailed_analysis(data))
        story.append(PageBreak())

        # Sources with numbered references
        story.extend(self._create_numbered_sources(data))
        story.append(PageBreak())

        # Appendices
        story.extend(self._create_appendices(data))

        # Build PDF
        doc.build(story)
        return filename

    def _create_title_page(self, data):
        """Create professional title page"""
        story = []

        # Main title
        title = Paragraph(f"Web Extraction Research Report", self.styles["CustomTitle"])
        story.append(title)
        story.append(Spacer(1, 50))

        # Topic
        topic = data.get("topic", "Unknown Topic")
        topic_para = Paragraph(f"<b>Topic:</b> {topic}", self.styles["CustomSubtitle"])
        story.append(topic_para)
        story.append(Spacer(1, 30))

        # Generation info
        timestamp = data.get("timestamp", datetime.now().isoformat())
        gen_date = datetime.fromisoformat(timestamp.replace("Z", "+00:00")).strftime(
            "%B %d, %Y at %I:%M %p"
        )

        info_data = [
            ["Report Generated:", gen_date],
            ["Total Sources:", str(len(data.get("sites", [])))],
            ["Total Content:", f"{data.get('total_content_length', 0):,} characters"],
            [
                "Average Content:",
                f"{data.get('total_content_length', 0) // len(data.get('sites', [])) if data.get('sites') else 0:,} characters per source",
            ],
        ]

        info_table = Table(info_data, colWidths=[2 * inch, 3 * inch])
        info_table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 12),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                    ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                    ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                ]
            )
        )
        story.append(info_table)
        story.append(Spacer(1, 50))

        # Footer
        footer = Paragraph(
            "Enhanced Web Extraction Report | Generated with Advanced PDF Generator",
            self.styles["Normal"],
        )
        story.append(footer)

        return story

    def _create_table_of_contents(self, data):
        """Create table of contents"""
        story = []

        toc_title = Paragraph("Table of Contents", self.styles["CustomSubtitle"])
        story.append(toc_title)
        story.append(Spacer(1, 20))

        toc_items = [
            "Executive Summary",
            "Research Methodology",
            "Detailed Analysis",
            "Source Analysis",
            "Content Metrics",
            "Numbered Sources",
            "Appendices",
        ]

        for i, item in enumerate(toc_items, 1):
            toc_item = Paragraph(f"{i}. {item}", self.styles["Normal"])
            story.append(toc_item)
            story.append(Spacer(1, 8))

        return story

    def _create_executive_summary(self, data):
        """Create executive summary section"""
        story = []

        summary_title = Paragraph("Executive Summary", self.styles["CustomSubtitle"])
        story.append(summary_title)
        story.append(Spacer(1, 20))

        topic = data.get("topic", "Unknown Topic")
        sites_count = len(data.get("sites", []))
        total_content = data.get("total_content_length", 0)
        avg_content = total_content // sites_count if sites_count > 0 else 0

        summary_text = f"""
        This report presents the results of comprehensive web extraction research on the topic: <b>"{topic}"</b>. 
        The research was conducted using advanced web extraction techniques to gather information from multiple 
        online sources and provide a detailed analysis of the available content.
        
        <br/><br/>
        <b>Key Findings:</b>
        • Total sources analyzed: {sites_count}
        • Total content extracted: {total_content:,} characters
        • Average content per source: {avg_content:,} characters
        • Content diversity: High (multiple extraction methods used)
        
        <br/><br/>
        The research methodology employed both automated and manual content extraction techniques to ensure 
        comprehensive coverage of the topic. Each source was carefully analyzed for relevance and content quality, 
        with detailed metrics provided for further analysis.
        """

        summary_para = Paragraph(summary_text, self.styles["Summary"])
        story.append(summary_para)

        return story

    def _create_detailed_analysis(self, data):
        """Create detailed analysis section"""
        story = []

        analysis_title = Paragraph("Detailed Analysis", self.styles["CustomSubtitle"])
        story.append(analysis_title)
        story.append(Spacer(1, 20))

        # Research methodology
        methodology_title = Paragraph(
            "Research Methodology", self.styles["SectionHeader"]
        )
        story.append(methodology_title)

        methodology_text = """
        The research was conducted using advanced web extraction techniques that combine multiple search engines 
        and content extraction methods. The methodology ensures comprehensive coverage and high-quality content 
        extraction from various online sources.
        
        <br/><br/>
        <b>Extraction Methods Used:</b>
        • Automated web scraping with intelligent content detection
        • Multiple search engine integration for broader coverage
        • Content quality assessment and filtering
        • Structured data extraction and formatting
        """

        methodology_para = Paragraph(methodology_text, self.styles["Normal"])
        story.append(methodology_para)
        story.append(Spacer(1, 20))

        # Source analysis
        source_analysis_title = Paragraph(
            "Source Analysis", self.styles["SectionHeader"]
        )
        story.append(source_analysis_title)

        sites = data.get("sites", [])
        if sites:
            # Create source analysis table
            source_data = [["Source #", "Domain", "Content Length", "Title"]]

            for i, site in enumerate(sites, 1):
                domain = site.get("source", "Unknown")
                content_length = site.get("content_length", 0)
                title = (
                    site.get("title", "No title")[:50] + "..."
                    if len(site.get("title", "")) > 50
                    else site.get("title", "No title")
                )

                source_data.append([str(i), domain, f"{content_length:,}", title])

            source_table = Table(
                source_data, colWidths=[0.8 * inch, 1.5 * inch, 1.2 * inch, 3 * inch]
            )
            source_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 10),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                        ("FONTSIZE", (0, 1), (-1, -1), 9),
                    ]
                )
            )
            story.append(source_table)

        story.append(Spacer(1, 20))

        # Content metrics
        metrics_title = Paragraph("Content Metrics", self.styles["SectionHeader"])
        story.append(metrics_title)

        total_content = data.get("total_content_length", 0)
        sites_count = len(data.get("sites", []))
        avg_content = total_content // sites_count if sites_count > 0 else 0

        metrics_text = f"""
        <b>Content Analysis Summary:</b>
        • Total content extracted: {total_content:,} characters
        • Number of sources: {sites_count}
        • Average content per source: {avg_content:,} characters
        • Content extraction efficiency: {sites_count * avg_content / max(total_content, 1) * 100:.1f}%
        """

        metrics_para = Paragraph(metrics_text, self.styles["Metrics"])
        story.append(metrics_para)

        return story

    def _create_numbered_sources(self, data):
        """Create numbered sources section with detailed information"""
        story = []

        sources_title = Paragraph(
            "Detailed Source Analysis", self.styles["CustomSubtitle"]
        )
        story.append(sources_title)
        story.append(Spacer(1, 20))

        sites = data.get("sites", [])
        if not sites:
            no_sources = Paragraph(
                "No sources found in the data.", self.styles["Normal"]
            )
            story.append(no_sources)
            return story

        for i, site in enumerate(sites, 1):
            # Source header with number
            source_header = Paragraph(
                f"Source [{i}]: {site.get('title', 'No title')}",
                self.styles["SourceTitle"],
            )
            story.append(source_header)

            # Source details
            url = site.get("url", "No URL")
            domain = site.get("source", "Unknown domain")
            content_length = site.get("content_length", 0)

            details_text = f"""
            <b>Domain:</b> {domain}<br/>
            <b>URL:</b> {url}<br/>
            <b>Content Length:</b> {content_length:,} characters<br/>
            <b>Extraction Method:</b> {site.get('extraction_method', 'Unknown')}
            """

            details_para = Paragraph(details_text, self.styles["SourceContent"])
            story.append(details_para)

            # Source content preview
            content = site.get("content", "")
            if content:
                # Truncate content for PDF
                preview_length = 500
                if len(content) > preview_length:
                    content_preview = content[:preview_length] + "..."
                else:
                    content_preview = content

                content_text = f"<b>Content Preview:</b><br/>{content_preview}"
                content_para = Paragraph(content_text, self.styles["SourceContent"])
                story.append(content_para)

            # Source link
            link_text = f"<b>Source Link:</b> {url}"
            link_para = Paragraph(link_text, self.styles["SourceLink"])
            story.append(link_para)

            story.append(Spacer(1, 20))

            # Add page break after every 3 sources to avoid overcrowding
            if i % 3 == 0 and i < len(sites):
                story.append(PageBreak())

        return story

    def _create_appendices(self, data):
        """Create appendices section"""
        story = []

        appendices_title = Paragraph("Appendices", self.styles["CustomSubtitle"])
        story.append(appendices_title)
        story.append(Spacer(1, 20))

        # Appendix A: Technical Details
        tech_title = Paragraph(
            "Appendix A: Technical Details", self.styles["SectionHeader"]
        )
        story.append(tech_title)

        tech_text = f"""
        <b>Report Generation Details:</b><br/>
        • Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br/>
        • Total sources processed: {len(data.get('sites', []))}<br/>
        • Total content extracted: {data.get('total_content_length', 0):,} characters<br/>
        • Data format: JSON with enhanced PDF output<br/>
        • Extraction methods: Multiple (newspaper3k, BeautifulSoup, Simple text)<br/>
        • Search engines: Google, DuckDuckGo<br/>
        """

        tech_para = Paragraph(tech_text, self.styles["Normal"])
        story.append(tech_para)
        story.append(Spacer(1, 20))

        # Appendix B: Source Summary
        summary_title = Paragraph(
            "Appendix B: Source Summary", self.styles["SectionHeader"]
        )
        story.append(summary_title)

        sites = data.get("sites", [])
        if sites:
            summary_data = [["Source #", "Domain", "Content Length", "Method"]]

            for i, site in enumerate(sites, 1):
                domain = site.get("source", "Unknown")
                content_length = site.get("content_length", 0)
                method = site.get("extraction_method", "Unknown")

                summary_data.append([str(i), domain, f"{content_length:,}", method])

            summary_table = Table(
                summary_data, colWidths=[0.8 * inch, 2 * inch, 1.5 * inch, 1.5 * inch]
            )
            summary_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 10),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                        ("FONTSIZE", (0, 1), (-1, -1), 9),
                    ]
                )
            )
            story.append(summary_table)

        return story

    def create_enhanced_comparison_pdf(self, comparison_data, filename=None):
        """
        Create enhanced comparison PDF report

        Args:
            comparison_data: Dictionary containing comparison data
            filename: Output filename (optional)

        Returns:
            Generated PDF filename
        """
        if not filename:
            topic = comparison_data.get("topic", "comparison").replace(" ", "_").lower()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"enhanced_comparison_{topic}_{timestamp}.pdf"

        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
        )
        story = []

        # Title page
        title = Paragraph(
            "Web Extraction Methods Comparison Report", self.styles["CustomTitle"]
        )
        story.append(title)
        story.append(Spacer(1, 30))

        topic = comparison_data.get("topic", "Unknown Topic")
        topic_para = Paragraph(f"<b>Topic:</b> {topic}", self.styles["CustomSubtitle"])
        story.append(topic_para)
        story.append(PageBreak())

        # Comparison results
        tavily = comparison_data.get("tavily", {})
        standalone = comparison_data.get("standalone", {})

        if tavily.get("success") and standalone.get("success"):
            # Results table
            results_data = [
                ["Metric", "Tavily API", "Standalone", "Winner"],
                [
                    "Sites Found",
                    str(tavily.get("sites_count", 0)),
                    str(standalone.get("sites_count", 0)),
                    (
                        "Tavily"
                        if tavily.get("sites_count", 0)
                        > standalone.get("sites_count", 0)
                        else "Standalone"
                    ),
                ],
                [
                    "Total Content",
                    f"{tavily.get('total_content', 0):,}",
                    f"{standalone.get('total_content', 0):,}",
                    (
                        "Tavily"
                        if tavily.get("total_content", 0)
                        > standalone.get("total_content", 0)
                        else "Standalone"
                    ),
                ],
                [
                    "Extraction Time",
                    f"{tavily.get('extraction_time', 0):.2f}s",
                    f"{standalone.get('extraction_time', 0):.2f}s",
                    (
                        "Tavily"
                        if tavily.get("extraction_time", 0)
                        < standalone.get("extraction_time", 0)
                        else "Standalone"
                    ),
                ],
            ]

            results_table = Table(
                results_data, colWidths=[2 * inch, 1.5 * inch, 1.5 * inch, 1.5 * inch]
            )
            results_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 10),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                        ("FONTSIZE", (0, 1), (-1, -1), 9),
                    ]
                )
            )
            story.append(results_table)

        # Build PDF
        doc.build(story)
        return filename


def main():
    """Example usage of enhanced PDF generator"""
    generator = EnhancedPDFGenerator()

    # Example data
    sample_data = {
        "topic": "Python Machine Learning",
        "sites": [
            {
                "title": "Python Machine Learning Tutorial",
                "url": "https://example.com/tutorial",
                "source": "example.com",
                "content": "This is a comprehensive tutorial on Python machine learning...",
                "content_length": 1500,
                "extraction_method": "newspaper3k",
            },
            {
                "title": "Machine Learning with Python Guide",
                "url": "https://guide.com/ml-python",
                "source": "guide.com",
                "content": "Learn machine learning with Python step by step...",
                "content_length": 2000,
                "extraction_method": "beautifulsoup",
            },
        ],
        "total_content_length": 3500,
        "timestamp": datetime.now().isoformat(),
    }

    # Generate enhanced PDF
    pdf_file = generator.create_enhanced_web_extraction_pdf(sample_data)
    print(f"✅ Enhanced PDF generated: {pdf_file}")


if __name__ == "__main__":
    main()
