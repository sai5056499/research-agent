#!/usr/bin/env python3
"""
Enhanced Web Extractor with Anti-Detection Measures
Handles 403 Forbidden errors and other blocking mechanisms
"""

import requests
import json
import time
import random
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import re
from datetime import datetime
from googlesearch import search
from duckduckgo_search import DDGS
from newspaper import Article
import nltk
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class EnhancedWebExtractor:
    def __init__(self):
        """Initialize enhanced web extractor with anti-detection measures"""
        
        # Download required NLTK data
        try:
            nltk.download("punkt", quiet=True)
        except:
            pass
        
        # Rotating User Agents to avoid detection
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        
        # Additional headers to appear more human-like
        self.base_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Cache-Control": "max-age=0"
        }
        
        # Proxy rotation (optional - add your proxies here)
        self.proxies = None  # Add proxies if available
        
        # Rate limiting settings
        self.min_delay = 2
        self.max_delay = 5
        self.max_retries = 3
        
    def _get_session(self) -> requests.Session:
        """Create a new session with random user agent and headers"""
        session = requests.Session()
        
        # Random user agent
        user_agent = random.choice(self.user_agents)
        
        # Update headers
        headers = self.base_headers.copy()
        headers["User-Agent"] = user_agent
        
        session.headers.update(headers)
        
        # Configure session
        session.verify = False
        session.timeout = 15
        
        # Add proxies if available
        if self.proxies:
            session.proxies = random.choice(self.proxies)
        
        return session
    
    def _smart_delay(self):
        """Add intelligent delays to avoid detection"""
        # Random delay between requests
        delay = random.uniform(self.min_delay, self.max_delay)
        time.sleep(delay)
        
        # Occasionally add longer delays
        if random.random() < 0.1:  # 10% chance
            extra_delay = random.uniform(3, 8)
            time.sleep(extra_delay)
    
    def _extract_with_retry(self, url: str, max_retries: int = 3) -> Optional[Dict]:
        """Extract content with retry mechanism and anti-detection"""
        
        for attempt in range(max_retries):
            try:
                session = self._get_session()
                
                # Add random delay before request
                self._smart_delay()
                
                # Try newspaper3k first (best for articles)
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
                            "publish_date": str(article.publish_date) if article.publish_date else None,
                            "extraction_method": "newspaper3k",
                            "attempt": attempt + 1
                        }
                except Exception as e:
                    if "403" in str(e) or "Forbidden" in str(e):
                        print(f"   ⚠️  Newspaper3k blocked (attempt {attempt + 1}): {e}")
                        if attempt < max_retries - 1:
                            time.sleep(random.uniform(5, 10))  # Longer delay for 403
                            continue
                    else:
                        print(f"   ⚠️  Newspaper3k failed: {e}")
                
                # Try BeautifulSoup with enhanced headers
                try:
                    response = session.get(url, timeout=15)
                    
                    # Check for blocking
                    if response.status_code == 403:
                        print(f"   ⚠️  BeautifulSoup blocked (attempt {attempt + 1}): 403 Forbidden")
                        if attempt < max_retries - 1:
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
                        if attempt < max_retries - 1:
                            time.sleep(random.uniform(5, 10))
                            continue
                    else:
                        print(f"   ⚠️  BeautifulSoup failed: {e}")
                
                # Try simple text extraction as last resort
                try:
                    response = session.get(url, timeout=15)
                    
                    if response.status_code == 403:
                        print(f"   ⚠️  Simple extraction blocked (attempt {attempt + 1}): 403 Forbidden")
                        if attempt < max_retries - 1:
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
                        if attempt < max_retries - 1:
                            time.sleep(random.uniform(5, 10))
                            continue
                    else:
                        print(f"   ⚠️  Simple extraction failed: {e}")
                
                # If all methods failed, try with different approach
                if attempt < max_retries - 1:
                    print(f"   🔄 Retrying with different approach (attempt {attempt + 2})")
                    time.sleep(random.uniform(3, 7))
                
            except Exception as e:
                print(f"   ❌ Extraction attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
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
    
    def search_google(self, query: str, num_results: int = 10) -> List[Dict]:
        """Search using Google with enhanced error handling"""
        results = []
        try:
            print(f"🔍 Searching Google for: {query}")
            
            search_results = search(query, num_results=num_results, lang="en")
            
            for url in search_results:
                try:
                    result = self._extract_with_retry(url)
                    if result:
                        results.append(result)
                        print(f"   ✅ Extracted: {result.get('title', 'Unknown')} (Method: {result.get('extraction_method', 'unknown')})")
                    else:
                        print(f"   ❌ Failed to extract: {url}")
                    
                    # Smart delay between extractions
                    self._smart_delay()
                    
                except Exception as e:
                    print(f"   ❌ Failed to extract {url}: {e}")
                    continue
                    
        except Exception as e:
            print(f"❌ Google search error: {e}")
        
        return results
    
    def search_duckduckgo(self, query: str, num_results: int = 10) -> List[Dict]:
        """Search using DuckDuckGo with enhanced error handling"""
        results = []
        try:
            print(f"🔍 Searching DuckDuckGo for: {query}")
            
            with DDGS() as ddgs:
                search_results = ddgs.text(query, max_results=num_results)
                
                for result in search_results:
                    try:
                        url = result.get("link", "")
                        if url:
                            extracted = self._extract_with_retry(url)
                            if extracted:
                                # Add search result metadata
                                extracted["search_snippet"] = result.get("body", "")
                                extracted["search_rank"] = len(results) + 1
                                results.append(extracted)
                                print(f"   ✅ Extracted: {extracted.get('title', 'Unknown')} (Method: {extracted.get('extraction_method', 'unknown')})")
                            else:
                                print(f"   ❌ Failed to extract: {url}")
                            
                            # Smart delay
                            self._smart_delay()
                            
                    except Exception as e:
                        print(f"   ❌ Failed to extract: {e}")
                        continue
                        
        except Exception as e:
            print(f"❌ DuckDuckGo search error: {e}")
        
        return results
    
    def get_topic_data(self, topic: str, max_sites: int = 10) -> Dict:
        """Get comprehensive data for a topic with enhanced extraction"""
        print(f"🔬 Researching topic: {topic}")
        print(f"🛡️  Using enhanced anti-detection measures")
        
        # Search using multiple engines
        all_results = []
        
        # Google search
        google_results = self.search_google(topic, max_sites // 2)
        all_results.extend(google_results)
        
        # DuckDuckGo search
        ddg_results = self.search_duckduckgo(topic, max_sites // 2)
        all_results.extend(ddg_results)
        
        # Remove duplicates
        unique_results = []
        seen_urls = set()
        
        for result in all_results:
            url = result.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)
        
        # Process results
        complete_data = {
            "topic": topic,
            "sites": [],
            "total_content_length": 0,
            "search_engines_used": ["Google", "DuckDuckGo"],
            "extraction_methods": set(),
            "blocked_sites": 0,
            "successful_extractions": 0,
            "timestamp": datetime.now().isoformat(),
        }
        
        for i, result in enumerate(unique_results[:max_sites]):
            if result:
                complete_data["sites"].append(result)
                complete_data["total_content_length"] += result.get("content_length", 0)
                complete_data["extraction_methods"].add(result.get("extraction_method", "unknown"))
                complete_data["successful_extractions"] += 1
                
                print(f"📄 {i+1}/{min(len(unique_results), max_sites)}: {result.get('title', 'Unknown')}")
                print(f"   Method: {result.get('extraction_method', 'unknown')}")
                print(f"   Content: {result.get('content_length', 0)} characters")
                print(f"   Attempts: {result.get('attempt', 1)}")
        
        # Convert set to list for JSON serialization
        complete_data["extraction_methods"] = list(complete_data["extraction_methods"])
        
        print(f"\n✅ Enhanced research complete!")
        print(f"   Sites processed: {complete_data['successful_extractions']}")
        print(f"   Total content: {complete_data['total_content_length']:,} characters")
        print(f"   Extraction methods: {', '.join(complete_data['extraction_methods'])}")
        print(f"   Anti-detection measures: Active")
        
        return complete_data

def main():
    """Test the enhanced web extractor"""
    extractor = EnhancedWebExtractor()
    
    # Test with a topic that was previously blocked
    topic = "artificial intelligence agents"
    results = extractor.get_topic_data(topic, max_sites=5)
    
    print(f"\n📊 Results Summary:")
    print(f"Topic: {results['topic']}")
    print(f"Successful extractions: {results['successful_extractions']}")
    print(f"Total content: {results['total_content_length']:,} characters")

if __name__ == "__main__":
    main() 