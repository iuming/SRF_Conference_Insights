#!/usr/bin/env python3
"""
SRF Conference Insights - IPAC2025 Real Data Crawler

This module provides an improved web crawler for extracting real conference paper data
from the official IPAC2025 Indico website (https://indico.jacow.org/event/81/).

Author: Ming Liu <mliu@ihep.ac.cn>
Project: SRF Conference Insights
Institution: Institute of High Energy Physics, Chinese Academy of Sciences

Features:
- Real-time data extraction from official Indico conference management system
- Robust error handling and retry mechanisms
- Large-scale data processing capabilities (1,400+ papers)
- Comprehensive paper metadata extraction including titles, authors, abstracts
- JSON data export with detailed statistics

Dependencies:
- requests: HTTP client for web scraping
- beautifulsoup4: HTML parsing and content extraction
- json: Data serialization and export

Development Log:
- v1.0: Initial implementation with basic crawling functionality
- v1.1: Added retry mechanisms and error handling
- v1.2: Enhanced data extraction accuracy and comprehensive statistics
- v1.3: Optimized for large-scale data processing without artificial limits

Usage:
    python improved_real_crawler.py

Output:
    ipac2025_real_papers.json - Complete dataset with 1,400+ authentic papers
"""

import requests
import re
import json
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import random

class ImprovedIPAC2025Crawler:
    """
    Enhanced web crawler for IPAC2025 conference papers.
    
    This class implements a robust web scraping system specifically designed
    for extracting paper data from the IPAC2025 conference Indico website.
    
    Attributes:
        base_url (str): Base URL for the Indico system
        event_url (str): Specific event URL for IPAC2025
        session (requests.Session): HTTP session with optimized headers
    """
    def __init__(self):
        self.base_url = "https://indico.jacow.org"
        self.event_url = "https://indico.jacow.org/event/81/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
    def get_page_content(self, url, max_retries=3):
        """
        Fetch web page content with retry mechanism.
        
        Args:
            url (str): Target URL to fetch
            max_retries (int): Maximum number of retry attempts
            
        Returns:
            str: HTML content if successful, None if failed
        """
        for attempt in range(max_retries):
            try:
                print(f"Fetching: {url}")
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                
                # Check content type
                content_type = response.headers.get('content-type', '')
                if 'text/html' in content_type:
                    return response.text
                else:
                    print(f"Warning: Non-HTML content type: {content_type}")
                    return response.text
                    
            except Exception as e:
                print(f"Page fetch failed (attempt {attempt+1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(random.uniform(2, 5))
                else:
                    return None
        return None
    
    def find_contribution_links(self, html_content):
        """
        Extract all paper contribution links from HTML content.
        
        Args:
            html_content (str): HTML source code from the contributions page
            
        Returns:
            list: List of unique contribution URLs
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        contribution_links = set()  # Use set to avoid duplicates
        
        # Method 1: Find all links containing /event/81/contributions/
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if href and '/event/81/contributions/' in href:
                # Ensure it's a specific paper link, not a list page
                if re.match(r'.*/event/81/contributions/\d+/?$', href):
                    full_url = urljoin(self.base_url, href)
                    contribution_links.add(full_url)
        
        # Method 2: Find links through regex pattern matching
        link_pattern = re.compile(r'https://indico\.jacow\.org/event/81/contributions/(\d+)/?')
        for match in link_pattern.finditer(html_content):
            contribution_links.add(match.group(0))
        
        contribution_list = list(contribution_links)
        print(f"Found {len(contribution_list)} unique paper links")
        
        if contribution_list:
            print(f"Sample links:")
            for i, link in enumerate(contribution_list[:3]):
                print(f"  {i+1}. {link}")
        
        return contribution_list
    
    def extract_paper_info(self, contribution_url):
        """
        Extract detailed paper information from a single contribution page.
        
        Args:
            contribution_url (str): URL of the specific paper contribution page
            
        Returns:
            dict: Paper information containing title, authors, abstract, etc.
                 None if extraction fails
        """
        html_content = self.get_page_content(contribution_url)
        if not html_content:
            return None
            
        soup = BeautifulSoup(html_content, 'html.parser')
        
        paper_info = {
            'url': contribution_url,
            'title': '',
            'authors': [],
            'institutions': [],
            'abstract': '',
            'category': '',
            'session': '',
            'type': '',
            'datetime': '',
            'keywords': [],
            'conference': 'IPAC2025'
        }
        
        try:
            # Extract title
            title_elem = soup.find('h1') or soup.find('title')
            if title_elem:
                paper_info['title'] = title_elem.get_text().strip()
            
            # Extract author information
            # Look for elements containing author information
            author_patterns = [
                soup.find_all('span', class_=re.compile(r'author', re.I)),
                soup.find_all('div', class_=re.compile(r'author', re.I)),
                soup.find_all('a', href=re.compile(r'/person/')),
            ]
            
            for pattern in author_patterns:
                if pattern:
                    for elem in pattern:
                        author_name = elem.get_text().strip()
                        if author_name and len(author_name) > 2:
                            paper_info['authors'].append(author_name)
                    if paper_info['authors']:
                        break
            
            # Extract abstract
            abstract_selectors = [
                'div.abstract',
                'div.description', 
                'div.summary',
                'div[class*="abstract"]',
                'div[class*="description"]'
            ]
            
            for selector in abstract_selectors:
                abstract_elem = soup.select_one(selector)
                if abstract_elem:
                    paper_info['abstract'] = abstract_elem.get_text().strip()
                    break
            
            # Extract category/session information
            category_selectors = [
                'span.category',
                'div.category',
                'span[class*="category"]',
                'div[class*="track"]',
                'div[class*="session"]'
            ]
            
            for selector in category_selectors:
                category_elem = soup.select_one(selector)
                if category_elem:
                    paper_info['category'] = category_elem.get_text().strip()
                    break
            
            # Extract time information
            time_selectors = [
                'time',
                'span.datetime', 
                'div.datetime',
                'span[class*="time"]',
                'div[class*="time"]'
            ]
            
            for selector in time_selectors:
                time_elem = soup.select_one(selector)
                if time_elem:
                    paper_info['datetime'] = time_elem.get_text().strip()
                    break
            
            # Extract ID from URL
            url_match = re.search(r'/contributions/(\d+)', contribution_url)
            if url_match:
                paper_info['contribution_id'] = url_match.group(1)
            
            print(f"✓ Successfully extracted: {paper_info['title'][:50]}...")
            
        except Exception as e:
            print(f"Error extracting paper information: {e}")
            return None
            
        return paper_info
    
    def crawl_conference(self, max_papers=None):
        """
        Main crawling function to extract all conference papers.
        
        Args:
            max_papers (int, optional): Maximum number of papers to crawl.
                                      If None, crawls all available papers.
                                      
        Returns:
            list: List of paper dictionaries with extracted information
        """
        print("=== IPAC2025 Real Data Crawler ===")
        print(f"Target website: {self.event_url}")
        
        papers = []
        
        # 1. Get main contributions list page
        contributions_url = f"{self.event_url}contributions/"
        print(f"\nStep 1: Fetching contributions list page")
        html_content = self.get_page_content(contributions_url)
        
        if not html_content:
            print("❌ Failed to fetch contributions list page")
            return papers
        
        # 2. Extract all paper links
        print(f"\nStep 2: Parsing paper links")
        contribution_links = self.find_contribution_links(html_content)
        
        if not contribution_links:
            print("❌ No paper links found")
            return papers
        
        # 3. Optional limit on number of papers to crawl
        if max_papers and len(contribution_links) > max_papers:
            contribution_links = contribution_links[:max_papers]
            print(f"Limiting to first {max_papers} papers")
        else:
            print(f"Will crawl all {len(contribution_links)} papers")
        
        # 4. Extract detailed information for each paper
        print(f"\nStep 3: Extracting detailed paper information")
        success_count = 0
        
        for i, link in enumerate(contribution_links, 1):
            print(f"\nProcessing paper {i}/{len(contribution_links)}")
            
            paper_info = self.extract_paper_info(link)
            if paper_info and paper_info.get('title'):
                papers.append(paper_info)
                success_count += 1
            
            # Add delay to avoid too frequent requests
            if i % 5 == 0:
                print(f"Processed {i} papers, taking a break...")
                time.sleep(random.uniform(1, 3))
        
        print(f"\n=== Crawling Complete ===")
        print(f"Paper links found: {len(contribution_links)}")
        print(f"Successfully extracted: {success_count}")
        print(f"Failed: {len(contribution_links) - success_count}")
        
        return papers
    
    def save_papers(self, papers, filename="ipac2025_real_papers.json"):
        """
        Save extracted paper data to JSON file with statistics.
        
        Args:
            papers (list): List of paper dictionaries to save
            filename (str): Output filename for the JSON data
        """
        output_file = filename
        
        # Create statistics
        stats = {
            'total_papers': len(papers),
            'papers_with_abstracts': len([p for p in papers if p.get('abstract')]),
            'papers_with_authors': len([p for p in papers if p.get('authors')]),
            'average_title_length': sum(len(p.get('title', '')) for p in papers) / len(papers) if papers else 0
        }
        
        data = {
            'conference': 'IPAC2025',
            'source': 'Real Indico Website',
            'url': self.event_url,
            'crawl_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'statistics': stats,
            'papers': papers
        }
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"\n✓ Data saved to: {output_file}")
            print(f"Statistics:")
            for key, value in stats.items():
                print(f"  {key}: {value}")
        except Exception as e:
            print(f"❌ Failed to save file: {e}")

def main():
    """
    Main execution function for the IPAC2025 crawler.
    
    Initializes the crawler, extracts all available papers without limits,
    saves the data to JSON file, and displays sample results.
    """
    crawler = ImprovedIPAC2025Crawler()
    
    # Crawl all paper data (no limits)
    papers = crawler.crawl_conference()  # Remove max_papers limit
    
    if papers:
        # Save data
        crawler.save_papers(papers)
        
        # Display samples
        print(f"\n=== Data Samples ===")
        for i, paper in enumerate(papers[:3], 1):
            print(f"\n{i}. {paper.get('title', 'No Title')}")
            print(f"   Authors: {', '.join(paper.get('authors', [])[:3])}")
            print(f"   Abstract: {paper.get('abstract', 'No Abstract')[:100]}...")
            print(f"   URL: {paper.get('url', '')}")
    else:
        print("❌ Failed to retrieve any paper data")

if __name__ == "__main__":
    main()
