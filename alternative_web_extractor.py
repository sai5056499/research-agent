#!/usr/bin/env python3
"""
Enhanced Alternative Web Extractor with Anti-Detection Measures
Improved version with rotating User-Agents, smart delays, and enhanced error handling
"""

import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
from newspaper import Article
import time
import random
import re
from urllib.parse import urlparse, urljoin
from typing import Dict, List, Optional, Any
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlternativeWebExtractor:
    def __init__(self):
        """Initialize the enhanced web extractor with anti-detection measures"""
        
        # Rotating User-Agents for anti-detection
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0",
        ]
        
        # Enhanced headers for more realistic requests
        self.base_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        }
        
        # Anti-detection settings
        self.max_retries = 3
        self.delay_range = (2, 6)  # Random delay between requests
        self.retry_delay_range = (5, 15)  # Longer delay on retries
        
        # Session for connection reuse
        self.session = None
        
        # Fallback URLs for common topics when search engines fail
        self.fallback_urls = {
            "artificial intelligence": [
                "https://en.wikipedia.org/wiki/Artificial_intelligence",
                "https://www.ibm.com/topics/artificial-intelligence",
                "https://www.mit.edu/~echeng/artificial-intelligence/"
            ],
            "machine learning": [
                "https://en.wikipedia.org/wiki/Machine_learning",
                "https://www.coursera.org/articles/what-is-machine-learning",
                "https://www.ibm.com/topics/machine-learning"
            ],
            "weight loss": [
                "https://www.mayoclinic.org/healthy-lifestyle/weight-loss/basics/weightloss-basics/hlv-20049483",
                "https://www.healthline.com/nutrition/how-to-lose-weight-as-fast-as-possible",
                "https://www.webmd.com/diet/obesity/features/10-ways-to-lose-weight-without-dieting"
            ],
            "meditation": [
                "https://www.mayoclinic.org/tests-procedures/meditation/in-depth/meditation/art-20045858",
                "https://www.mindful.org/how-to-meditate/",
                "https://en.wikipedia.org/wiki/Meditation"
            ],
            "yoga": [
                "https://www.mayoclinic.org/healthy-lifestyle/stress-management/in-depth/yoga/art-20044733",
                "https://www.yogajournal.com/poses/",
                "https://en.wikipedia.org/wiki/Yoga"
            ],
            "climate change": [
                "https://climate.nasa.gov/what-is-climate-change/",
                "https://www.un.org/en/climatechange/what-is-climate-change",
                "https://en.wikipedia.org/wiki/Climate_change"
            ],
            "nutrition": [
                "https://www.nutrition.gov/topics/basic-nutrition",
                "https://www.mayoclinic.org/healthy-lifestyle/nutrition-and-healthy-eating/basics/nutrition-basics/hlv-20049477",
                "https://en.wikipedia.org/wiki/Nutrition"
            ]
        }
        
    def _get_session(self) -> requests.Session:
        """Get or create a session with random headers"""
        if not self.session:
            self.session = requests.Session()
            
        # Update headers with random User-Agent
        headers = self.base_headers.copy()
        headers["User-Agent"] = random.choice(self.user_agents)
        self.session.headers.update(headers)
        
        return self.session
    
    def _smart_delay(self):
        """Add smart delay to avoid detection"""
        delay = random.uniform(*self.delay_range)
        time.sleep(delay)
    
    def _get_fallback_urls(self, query: str) -> List[str]:
        """Get fallback URLs when search engines fail"""
        query_lower = query.lower()
        
        # Direct match
        if query_lower in self.fallback_urls:
            print(f"📋 Using fallback URLs for: {query}")
            return self.fallback_urls[query_lower]
        
        # Partial match
        for topic, urls in self.fallback_urls.items():
            if any(word in query_lower for word in topic.split()):
                print(f"📋 Using fallback URLs for related topic: {topic}")
                return urls[:3]  # Return first 3 URLs
        
        # Generic fallback for any topic
        print(f"📋 Using generic fallback URLs for: {query}")
        return [
            f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}",
            f"https://www.google.com/search?q={query.replace(' ', '+')}",
            f"https://www.britannica.com/search?query={query.replace(' ', '+')}"
        ]
    
    def search_google(self, query: str, num_results: int = 10) -> List[str]:
        """
        Search Google for URLs related to the query with anti-detection measures
        """
        try:
            from googlesearch import search
            
            print(f"🔍 Searching Google for: '{query}'")
            
            urls = []
            # Fix: Remove the 'stop' parameter that's causing the error
            for url in search(query, num_results=num_results, pause=2.0):
                urls.append(url)
                self._smart_delay()  # Add delay between searches
                if len(urls) >= num_results:  # Manual limit
                    break
                
            print(f"📋 Found {len(urls)} URLs from Google")
            return urls
            
        except Exception as e:
            print(f"❌ Google search failed: {e}")
            # Return fallback URLs for common topics
            return self._get_fallback_urls(query)

    def search_duckduckgo(self, query: str, max_results: int = 10) -> List[str]:
        """
        Search DuckDuckGo for URLs with enhanced error handling
        """
        try:
            from duckduckgo_search import DDGS
            
            print(f"🦆 Searching DuckDuckGo for: '{query}'")
            
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
                urls = [result['href'] for result in results if 'href' in result]
                
                self._smart_delay()  # Add delay after search
                
            print(f"📋 Found {len(urls)} URLs from DuckDuckGo")
            return urls
            
        except Exception as e:
            print(f"❌ DuckDuckGo search failed: {e}")
            # Return fallback URLs for common topics
            return self._get_fallback_urls(query)

    def get_search_urls(self, topic: str, max_urls: int = 15) -> List[str]:
        """
        Get search URLs from multiple search engines with better distribution
        """
        print(f"\n🔍 Searching for: {topic}")
        all_urls = []
        
        # Try Google first (usually better results)
        google_urls = self.search_google(topic, max_urls // 2)
        all_urls.extend(google_urls)
        
        # Add delay between search engines
        if google_urls:
            time.sleep(random.uniform(3, 7))
        
        # Try DuckDuckGo as backup/supplement
        remaining = max_urls - len(all_urls)
        if remaining > 0:
            duckduckgo_urls = self.search_duckduckgo(topic, remaining)
            all_urls.extend(duckduckgo_urls)
        
        # Remove duplicates while preserving order
        unique_urls = []
        seen = set()
        for url in all_urls:
            if url not in seen:
                unique_urls.append(url)
                seen.add(url)
        
        print(f"✅ Total unique URLs found: {len(unique_urls)}")
        return unique_urls[:max_urls]

    async def extract_content_async(self, url: str, session: aiohttp.ClientSession) -> Optional[Dict]:
        """
        Asynchronously extract content from a URL with enhanced anti-detection
        """
        try:
            # Random delay
            await asyncio.sleep(random.uniform(1, 3))
            
            # Enhanced headers for async requests
            headers = self.base_headers.copy()
            headers["User-Agent"] = random.choice(self.user_agents)
            
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=15)) as response:
                if response.status == 403:
                    print(f"   ⚠️  Async request blocked: 403 Forbidden for {url}")
                    return None
                    
                response.raise_for_status()
                html = await response.text()
                
                # Parse with BeautifulSoup
                soup = BeautifulSoup(html, 'html.parser')
                
                # Remove unwanted elements
                for element in soup(['script', 'style', 'nav', 'header', 'footer']):
                    element.decompose()
                
                # Extract content
                title = soup.find('title')
                title_text = title.get_text().strip() if title else "No title"
                
                content = self._extract_main_content(soup)
                
                if content and len(content) > 100:
                    return {
                        "title": title_text,
                        "url": url,
                        "content": content[:8000],
                        "content_length": len(content),
                        "source": urlparse(url).netloc,
                        "extraction_method": "async_beautifulsoup"
                    }
                    
        except Exception as e:
            print(f"   ❌ Async extraction failed for {url}: {e}")
            return None

    def _extract_content_from_url(self, url: str) -> Optional[Dict]:
        """
        Enhanced content extraction with anti-detection measures and retry logic
        
        Args:
            url: URL to extract content from
            
        Returns:
            Dictionary containing extracted content
        """
        for attempt in range(self.max_retries):
            try:
                session = self._get_session()
                
                # Add random delay before request
                self._smart_delay()
                
                # Method 1: Try newspaper3k first (best for articles)
                try:
                    article = Article(url)
                    article.config.verify_ssl = False
                    
                    # Set custom headers for newspaper3k
                    article.config.browser_user_agent = session.headers["User-Agent"]
                    
                    article.download()
                    article.parse()
                    article.nlp()

                    if article.text and len(article.text) > 100:
                        return {
                            "title": article.title or "No title",
                            "url": url,
                            "content": article.text,
                            "content_length": len(article.text),
                            "source": urlparse(url).netloc,
                            "summary": article.summary,
                            "keywords": article.keywords,
                            "publish_date": (
                                str(article.publish_date) if article.publish_date else None
                            ),
                            "extraction_method": "newspaper3k",
                            "attempt": attempt + 1
                        }
                except Exception as e:
                    if "403" in str(e) or "Forbidden" in str(e):
                        print(f"   ⚠️  Newspaper3k blocked (attempt {attempt + 1}): {e}")
                        if attempt < self.max_retries - 1:
                            time.sleep(random.uniform(5, 10))  # Longer delay for 403
                            continue
                    else:
                        print(f"   ⚠️  Newspaper3k failed: {e}")

                # Method 2: Try BeautifulSoup with enhanced headers
                try:
                    response = session.get(url, timeout=15)
                    
                    # Check for blocking
                    if response.status_code == 403:
                        print(f"   ⚠️  BeautifulSoup blocked (attempt {attempt + 1}): 403 Forbidden")
                        if attempt < self.max_retries - 1:
                            time.sleep(random.uniform(5, 10))
                            continue
                        else:
                            break
                    
                    response.raise_for_status()

                    soup = BeautifulSoup(response.content, "html.parser")

                    # Remove script and style elements
                    for script in soup(["script", "style", "nav", "header", "footer"]):
                        script.decompose()

                    # Get title
                    title = soup.find("title")
                    title_text = title.get_text().strip() if title else "No title"

                    # Enhanced content extraction
                    content = self._extract_main_content(soup)

                    if content and len(content) > 100:
                        return {
                            "title": title_text,
                            "url": url,
                            "content": content[:8000],  # Increased limit
                            "content_length": len(content),
                            "source": urlparse(url).netloc,
                            "extraction_method": "beautifulsoup",
                            "attempt": attempt + 1
                        }

                except Exception as e:
                    if "403" in str(e) or "Forbidden" in str(e):
                        print(f"   ⚠️  BeautifulSoup blocked (attempt {attempt + 1}): {e}")
                        if attempt < self.max_retries - 1:
                            time.sleep(random.uniform(5, 10))
                            continue
                    else:
                        print(f"   ⚠️  BeautifulSoup failed: {e}")

                # Method 3: Simple text extraction as last resort
                try:
                    response = session.get(url, timeout=15)
                    
                    if response.status_code == 403:
                        print(f"   ⚠️  Simple extraction blocked (attempt {attempt + 1}): 403 Forbidden")
                        if attempt < self.max_retries - 1:
                            time.sleep(random.uniform(5, 10))
                            continue
                        else:
                            break
                    
                    response.raise_for_status()

                    # Simple text extraction
                    text = re.sub(r"<[^>]+>", "", response.text)
                    text = re.sub(r"\s+", " ", text).strip()

                    if text and len(text) > 100:
                        return {
                            "title": "Extracted Content",
                            "url": url,
                            "content": text[:5000],
                            "content_length": len(text),
                            "source": urlparse(url).netloc,
                            "extraction_method": "simple_text",
                            "attempt": attempt + 1
                        }

                except Exception as e:
                    if "403" in str(e) or "Forbidden" in str(e):
                        print(f"   ⚠️  Simple extraction blocked (attempt {attempt + 1}): {e}")
                        if attempt < self.max_retries - 1:
                            time.sleep(random.uniform(5, 10))
                            continue
                    else:
                        print(f"   ⚠️  Simple extraction failed: {e}")
                
                # If all methods failed, try with different approach
                if attempt < self.max_retries - 1:
                    print(f"   🔄 Retrying with different approach (attempt {attempt + 2})")
                    time.sleep(random.uniform(3, 7))

            except Exception as e:
                print(f"   ❌ Extraction attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(random.uniform(2, 5))

        return None

    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """Enhanced content extraction with multiple strategies"""
        
        # Strategy 1: Look for article content
        content_selectors = [
            "article",
            '[role="main"]',
            ".content",
            ".post-content", 
            ".entry-content",
            ".article-content",
            ".blog-content",
            ".post-body",
            ".entry-body",
            "main",
            ".main-content",
            "#content",
            ".content-area",
            ".post-text",
            ".article-text"
        ]
        
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                content = content_elem.get_text(separator=" ", strip=True)
                if len(content) > 300:
                    return content
        
        # Strategy 2: Look for paragraphs in body
        body = soup.find("body")
        if body:
            paragraphs = body.find_all("p")
            if paragraphs:
                content = " ".join([p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 50])
                if len(content) > 200:
                    return content
        
        # Strategy 3: Get all text from body
        if body:
            content = body.get_text(separator=" ", strip=True)
            return content
        
        return ""

    def get_topic_data(self, topic: str, max_sites: int = 10) -> Dict:
        """
        Enhanced topic data extraction with anti-detection measures
        """
        print(f"\n🚀 Enhanced Web Extraction for: {topic}")
        print("=" * 50)
        
        # Get URLs from search engines
        urls = self.get_search_urls(topic, max_sites)
        
        if not urls:
            return {
                "topic": topic,
                "sites": [],
                "total_content_length": 0,
                "extraction_summary": "No URLs found"
            }
        
        extracted_sites = []
        total_content_length = 0
        
        print(f"\n📊 Extracting content from {len(urls)} URLs...")
        
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] Processing: {url}")
            
            try:
                result = self._extract_content_from_url(url)
                
                if result:
                    extracted_sites.append(result)
                    total_content_length += result.get("content_length", 0)
                    print(f"   ✅ Success: {result['content_length']} chars via {result['extraction_method']}")
                else:
                    print(f"   ❌ Failed to extract content")
                    
            except Exception as e:
                print(f"   ❌ Error processing {url}: {e}")
            
            # Add delay between sites to avoid detection
            if i < len(urls):
                time.sleep(random.uniform(2, 5))
        
        success_rate = len(extracted_sites) / len(urls) * 100 if urls else 0
        
        print(f"\n📈 Extraction Summary:")
        print(f"   • URLs processed: {len(urls)}")
        print(f"   • Successful extractions: {len(extracted_sites)}")
        print(f"   • Success rate: {success_rate:.1f}%")
        print(f"   • Total content: {total_content_length:,} characters")
        
        return {
            "topic": topic,
            "sites": extracted_sites,
            "total_content_length": total_content_length,
            "extraction_summary": f"Extracted {len(extracted_sites)}/{len(urls)} sites ({success_rate:.1f}% success)",
            "urls_processed": len(urls),
            "successful_extractions": len(extracted_sites),
            "timestamp": datetime.now().isoformat()
        }

    async def get_topic_data_async(self, topic: str, max_sites: int = 10) -> Dict:
        """
        Async version of topic data extraction for better performance
        """
        print(f"\n🚀 Async Enhanced Web Extraction for: {topic}")
        print("=" * 50)
        
        # Get URLs from search engines (synchronous)
        urls = self.get_search_urls(topic, max_sites)
        
        if not urls:
            return {
                "topic": topic,
                "sites": [],
                "total_content_length": 0,
                "extraction_summary": "No URLs found"
            }
        
        extracted_sites = []
        
        print(f"\n📊 Async extracting content from {len(urls)} URLs...")
        
        # Create async session with enhanced settings
        connector = aiohttp.TCPConnector(limit=5, limit_per_host=2)
        timeout = aiohttp.ClientTimeout(total=30)
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            # Create tasks for async extraction
            tasks = [
                self.extract_content_async(url, session)
                for url in urls
            ]
            
            # Execute with some delay between requests
            results = []
            for i, task in enumerate(tasks):
                try:
                    result = await task
                    if result:
                        extracted_sites.append(result)
                        print(f"   ✅ [{i+1}/{len(urls)}] Success: {result['content_length']} chars")
                    else:
                        print(f"   ❌ [{i+1}/{len(urls)}] Failed")
                except Exception as e:
                    print(f"   ❌ [{i+1}/{len(urls)}] Error: {e}")
                
                # Add delay between requests
                if i < len(tasks) - 1:
                    await asyncio.sleep(random.uniform(1, 3))
        
        total_content_length = sum(site.get("content_length", 0) for site in extracted_sites)
        success_rate = len(extracted_sites) / len(urls) * 100 if urls else 0
        
        print(f"\n📈 Async Extraction Summary:")
        print(f"   • URLs processed: {len(urls)}")
        print(f"   • Successful extractions: {len(extracted_sites)}")
        print(f"   • Success rate: {success_rate:.1f}%")
        print(f"   • Total content: {total_content_length:,} characters")
        
        return {
            "topic": topic,
            "sites": extracted_sites,
            "total_content_length": total_content_length,
            "extraction_summary": f"Async extracted {len(extracted_sites)}/{len(urls)} sites ({success_rate:.1f}% success)",
            "urls_processed": len(urls),
            "successful_extractions": len(extracted_sites),
            "timestamp": datetime.now().isoformat()
        }

# Test function
def test_enhanced_extraction():
    """Test the enhanced extraction capabilities"""
    extractor = AlternativeWebExtractor()
    
    test_topics = [
        "artificial intelligence latest developments",
        "climate change solutions 2024"
    ]
    
    for topic in test_topics:
        print(f"\n{'='*60}")
        print(f"Testing Enhanced Extraction: {topic}")
        print(f"{'='*60}")
        
        result = extractor.get_topic_data(topic, max_sites=5)
        
        print(f"\nResults for '{topic}':")
        print(f"Sites extracted: {len(result['sites'])}")
        print(f"Total content: {result['total_content_length']} characters")
        
        for i, site in enumerate(result['sites'][:2], 1):
            print(f"\nSite {i}: {site['title']}")
            print(f"URL: {site['url']}")
            print(f"Length: {site['content_length']} chars")
            print(f"Method: {site['extraction_method']}")

if __name__ == "__main__":
    test_enhanced_extraction() 