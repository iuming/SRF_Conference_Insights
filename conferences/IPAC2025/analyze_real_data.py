#!/usr/bin/env python3
"""
SRF Conference Insights - IPAC2025 Real Data Analysis Tool

This module provides comprehensive analysis capabilities for the IPAC2025 conference
paper dataset extracted from the official Indico website.

Author: Ming Liu <mliu@ihep.ac.cn>
Project: SRF Conference Insights
Institution: Institute of High Energy Physics, Chinese Academy of Sciences

Features:
- Statistical analysis of paper metadata (titles, authors, abstracts)
- Data quality assessment and coverage metrics
- Export analysis reports in multiple formats

Dependencies:
- json: Data loading and parsing
- collections.Counter: Statistical counting operations

Development Log:
- v1.0: Basic statistical analysis implementation
- v1.1: Enhanced data quality metrics and reporting
- v1.2: Added comprehensive coverage analysis

Usage:
    python analyze_real_data.py
    
Input:
    ipac2025_real_papers.json - Raw paper data from crawler
    
Output:
    Console report with detailed statistics and metrics
"""

import json
import sys
from collections import Counter

def analyze_papers(filename="ipac2025_real_papers.json"):
    """
    Analyze extracted paper data and generate comprehensive statistics.
    
    Args:
        filename (str): Path to the JSON file containing paper data
        
    Returns:
        bool: True if analysis completed successfully, False otherwise
    """
    try:
        print("Loading data file...")
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        papers = data.get('papers', [])
        
        print("=== IPAC2025 Real Data Analysis Report ===")
        print(f"Data source: {data.get('source', 'Unknown')}")
        print(f"Crawl date: {data.get('crawl_date', 'Unknown')}")
        print(f"Conference website: {data.get('url', 'Unknown')}")
        print()
        
        # Basic statistics
        print("📊 Basic Statistics:")
        print(f"  Total papers: {len(papers)}")
        
        papers_with_abstracts = [p for p in papers if p.get('abstract') and p.get('abstract').strip()]
        papers_with_authors = [p for p in papers if p.get('authors') and len(p.get('authors', [])) > 0]
        papers_with_categories = [p for p in papers if p.get('category') and p.get('category').strip()]
        
        print(f"  Papers with abstracts: {len(papers_with_abstracts)}")
        print(f"  Papers with authors: {len(papers_with_authors)}")
        print(f"  Papers with categories: {len(papers_with_categories)}")
        print()
        
        # Coverage percentages
        total = len(papers)
        if total > 0:
            print("📈 Data Coverage:")
            print(f"  Abstract coverage: {len(papers_with_abstracts)/total*100:.1f}%")
            print(f"  Author coverage: {len(papers_with_authors)/total*100:.1f}%")
            print(f"  Category coverage: {len(papers_with_categories)/total*100:.1f}%")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return False

if __name__ == "__main__":
    analyze_papers()
