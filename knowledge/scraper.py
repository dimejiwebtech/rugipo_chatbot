"""
Generic web scraper for RUGIPO information
Extracts data from multiple configured websites
"""
import requests
from bs4 import BeautifulSoup
from django.utils.timezone import now
from knowledge.models import RUGIPOKnowledge, ScraperURL
from datetime import datetime
import logging
import re

logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Keywords to identify RUGIPO-related content
RUGIPO_KEYWORDS = ['rugipo', 'rufus giwa', 'rufus giwa polytechnic', 'rgip']


class GenericScraper:
    """
    Generic scraper for any website containing RUGIPO-related content
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
    
    def fetch_page(self, url):
        """Fetch a webpage safely"""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None
    
    def is_rugipo_related(self, text):
        """Check if text contains RUGIPO-related keywords"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in RUGIPO_KEYWORDS)
    
    def extract_content(self, html, url):
        """
        Extract text content and structure from HTML
        Looks for paragraphs, headings, and other text content
        """
        qa_list = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer"]):
                script.decompose()
            
            # Get all text-containing elements
            headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            paragraphs = soup.find_all('p')
            articles = soup.find_all(['article', 'section', 'div'], class_=['post', 'article', 'news', 'entry', 'content'])
            
            # Extract from articles/sections
            for article in articles:
                try:
                    title_elem = article.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong'])
                    content_elem = article.find('p') or article.find('div')
                    
                    if title_elem and content_elem:
                        title = title_elem.get_text(strip=True)
                        content = content_elem.get_text(strip=True)
                        
                        # Check if RUGIPO-related
                        if self.is_rugipo_related(title) or self.is_rugipo_related(content):
                            # Create Q&A from title and content
                            question = title if len(title) < 200 else title[:200]
                            answer = content[:1000]  # Limit answer length to ~300 words
                            
                            qa_list.append({
                                'question': question,
                                'answer': answer,
                                'category': self._determine_category(title + ' ' + content),
                                'source_url': url,
                                'keywords': self._extract_keywords(title + ' ' + content)
                            })
                except Exception as e:
                    logger.warning(f"Error parsing article: {str(e)}")
                    continue
            
            # Extract from heading + following paragraph pairs
            for i, heading in enumerate(headings):
                try:
                    heading_text = heading.get_text(strip=True)
                    
                    # Find next paragraph(s) after this heading
                    next_elem = heading.find_next('p')
                    if next_elem:
                        # Collect multiple paragraphs to get more content
                        para_text = next_elem.get_text(strip=True)
                        
                        # Try to get next 2 more paragraphs to build fuller answer
                        sibling = next_elem.find_next_sibling('p')
                        if sibling:
                            sibling_text = sibling.get_text(strip=True)
                            if len(sibling_text) > 10:
                                para_text += ' ' + sibling_text
                        
                        if self.is_rugipo_related(heading_text) or self.is_rugipo_related(para_text):
                            # Skip if too short
                            if len(heading_text) > 5 and len(para_text) > 20:
                                qa_list.append({
                                    'question': heading_text,
                                    'answer': para_text[:1000],
                                    'category': self._determine_category(heading_text + ' ' + para_text),
                                    'source_url': url,
                                    'keywords': self._extract_keywords(heading_text + ' ' + para_text)
                                })
                except Exception as e:
                    logger.warning(f"Error parsing heading-paragraph pair: {str(e)}")
                    continue
        
        except Exception as e:
            logger.error(f"Error extracting content: {str(e)}")
        
        return qa_list
    
    def _determine_category(self, text):
        """Determine content category from text"""
        text_lower = text.lower()
        
        # Check for specific keywords
        if any(word in text_lower for word in ['news', 'event', 'announcement', 'update', 'report']):
            return 'news'
        elif any(word in text_lower for word in ['admission', 'register', 'application', 'enroll']):
            return 'admissions'
        elif any(word in text_lower for word in ['fee', 'payment', 'tuition', 'cost', 'charge', 'price']):
            return 'fees'
        elif any(word in text_lower for word in ['facility', 'building', 'campus', 'hostel', 'library']):
            return 'facilities'
        elif any(word in text_lower for word in ['course', 'program', 'curriculum', 'academic']):
            return 'academic'
        elif any(word in text_lower for word in ['civil', 'construction', 'structural', 'cet']):
            return 'cet'
        elif any(word in text_lower for word in ['computer', 'software', 'programming', 'cte', 'it']):
            return 'cte'
        elif any(word in text_lower for word in ['electrical', 'electronics', 'power', 'eeet']):
            return 'eeet'
        elif any(word in text_lower for word in ['mechanical', 'machine', 'met', 'engine']):
            return 'met'
        elif any(word in text_lower for word in ['agricultural', 'bio', 'environmental', 'abet']):
            return 'abet'
        elif any(word in text_lower for word in ['student', 'service', 'counseling', 'support']):
            return 'student_services'
        else:
            return 'general'
    
    def _extract_keywords(self, text, max_keywords=8):
        """Extract keywords from text"""
        # Split by common delimiters
        words = re.split(r'[\s,;:.!?-]+', text.lower())
        
        # Filter out common words and short words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'is', 'was', 'are', 'been', 'be', 'have', 'has', 'had', 'do', 'does', 'did'}
        keywords = [w for w in words if len(w) > 2 and w not in stop_words and w not in RUGIPO_KEYWORDS]
        
        # Return unique keywords
        return ', '.join(list(dict.fromkeys(keywords[:max_keywords])))
    
    def scrape_url(self, url):
        """Scrape a single URL"""
        logger.info(f"Scraping: {url}")
        
        html = self.fetch_page(url)
        if not html:
            return []
        
        return self.extract_content(html, url)
    
    def save_qa_to_db(self, qa_list, source_url, knowledge_type='general'):
        """Save extracted Q&As to database"""
        added = 0
        updated = 0
        
        for qa in qa_list:
            try:
                # Avoid duplicates by checking question + category
                existing = RUGIPOKnowledge.objects.filter(
                    question__iexact=qa['question'],
                    category=qa['category']
                ).first()
                
                if existing:
                    # Update existing
                    existing.answer = qa['answer']
                    existing.keywords = qa['keywords']
                    existing.source_url = qa['source_url']
                    existing.knowledge_type = knowledge_type
                    existing.save()
                    updated += 1
                else:
                    # Create new
                    RUGIPOKnowledge.objects.create(
                        knowledge_type=knowledge_type,
                        category=qa['category'],
                        question=qa['question'],
                        answer=qa['answer'],
                        keywords=qa['keywords'],
                        source_url=qa['source_url'],
                        is_active=True
                    )
                    added += 1
            except Exception as e:
                logger.error(f"Error saving Q&A: {str(e)}")
                continue
        
        return {'added': added, 'updated': updated}


def scrape_single_url(url):
    """Scrape a single URL and return results"""
    scraper = GenericScraper()
    qa_list = scraper.scrape_url(url)
    result = scraper.save_qa_to_db(qa_list, url)
    result['total'] = len(qa_list)
    logger.info(f"URL {url}: Added {result['added']}, Updated {result['updated']}")
    return result


def scrape_rugipo_data():
    """
    Scrape all active configured URLs
    """
    logger.info("Starting RUGIPO data scrape from configured URLs...")
    
    scraper = GenericScraper()
    total_added = 0
    total_updated = 0
    total_urls = 0
    
    # Get all active scraper URLs from database
    urls = ScraperURL.objects.filter(is_active=True)
    
    if not urls.exists():
        logger.warning("No active scraper URLs configured")
        return {'added': 0, 'updated': 0, 'total': 0}
    
    for scraper_url in urls:
        try:
            logger.info(f"Processing: {scraper_url.url}")
            qa_list = scraper.scrape_url(scraper_url.url)
            
            if qa_list:
                result = scraper.save_qa_to_db(qa_list, scraper_url.url, knowledge_type='general')
                total_added += result['added']
                total_updated += result['updated']
                
                # Update last scraped time
                scraper_url.last_scraped = now()
                scraper_url.save()
                
                logger.info(f"✓ {scraper_url.url}: Added {result['added']}, Updated {result['updated']}")
            else:
                logger.info(f"⚠ {scraper_url.url}: No RUGIPO-related content found")
                
        except Exception as e:
            logger.error(f"Error scraping {scraper_url.url}: {str(e)}")
            continue
        
        total_urls += 1
    
    logger.info(f"Scrape complete: {total_added} added, {total_updated} updated from {total_urls} URLs")
    return {'added': total_added, 'updated': total_updated, 'total': total_urls}
