#!/usr/bin/env python3
"""
SRF Conference Insights - Command Line Interface

This module provides a command-line interface for the SRF Conference Insights project,
allowing users to run crawlers, analyzers, and other tools from the command line.

Author: Ming Liu <mliu@ihep.ac.cn>
Project: SRF Conference Insights
Institution: Institute of High Energy Physics, Chinese Academy of Sciences

Features:
- Command-line interface for all major functions
- Configuration management
- Logging and error handling
- Multi-conference support

Development Log:
- v1.0: Initial CLI implementation
- v1.1: Added comprehensive command support
- v1.2: Enhanced error handling and logging

Usage:
    srf-insights --help
    srf-insights crawl ipac2025
    srf-insights analyze --input data.json
"""

import argparse
import sys
import logging
from pathlib import Path

def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def crawl_command(args):
    """Execute crawling command."""
    print(f"Starting crawl for conference: {args.conference}")
    
    if args.conference.lower() == 'ipac2025':
        from conferences.IPAC2025.improved_real_crawler import ImprovedIPAC2025Crawler
        crawler = ImprovedIPAC2025Crawler()
        papers = crawler.crawl_conference(max_papers=args.limit)
        crawler.save_papers(papers, args.output)
    else:
        print(f"Error: Conference '{args.conference}' not supported yet.")
        return 1
    
    return 0

def analyze_command(args):
    """Execute analysis command."""
    print(f"Analyzing data from: {args.input}")
    
    if args.input.endswith('ipac2025_real_papers.json'):
        from conferences.IPAC2025.analyze_real_data import analyze_papers
        success = analyze_papers(args.input)
        return 0 if success else 1
    else:
        print("Error: Unsupported data format.")
        return 1

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='SRF Conference Insights - Command Line Interface',
        epilog='For more information, visit: https://github.com/iuming/SRF_Conference_Insights'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Crawl command
    crawl_parser = subparsers.add_parser('crawl', help='Crawl conference papers')
    crawl_parser.add_argument('conference', help='Conference name (e.g., ipac2025)')
    crawl_parser.add_argument('--limit', type=int, help='Limit number of papers to crawl')
    crawl_parser.add_argument('--output', default='papers.json', help='Output file name')
    crawl_parser.set_defaults(func=crawl_command)
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze paper data')
    analyze_parser.add_argument('--input', required=True, help='Input data file')
    analyze_parser.set_defaults(func=analyze_command)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    # Execute command
    if hasattr(args, 'func'):
        return args.func(args)
    else:
        parser.print_help()
        return 0

if __name__ == '__main__':
    sys.exit(main())
