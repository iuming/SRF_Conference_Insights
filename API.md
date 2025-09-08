"""
SRF Conference Insights - API Documentation Generator

This script generates comprehensive API documentation for the SRF Conference Insights project.

Author: Ming Liu <mliu@ihep.ac.cn>
Project: SRF Conference Insights
Institution: Institute of High Energy Physics, Chinese Academy of Sciences
"""

# API Documentation

## Overview

SRF Conference Insights provides a comprehensive API for processing and analyzing conference papers from the superconducting radio frequency research community.

## Core Modules

### conferences.IPAC2025.improved_real_crawler

The main crawler module for extracting paper data from IPAC2025 conference.

#### ImprovedIPAC2025Crawler

**Class**: `ImprovedIPAC2025Crawler`

Main crawler class for IPAC2025 conference data extraction.

**Methods**:

- `__init__()`: Initialize crawler with default configuration
- `get_page_content(url, max_retries=3)`: Fetch webpage content with retry logic
- `find_contribution_links(html_content)`: Extract paper URLs from HTML
- `extract_paper_info(contribution_url)`: Extract detailed paper information
- `crawl_conference(max_papers=None)`: Main crawling orchestration
- `save_papers(papers, filename)`: Save extracted data to JSON

**Example Usage**:

```python
from conferences.IPAC2025.improved_real_crawler import ImprovedIPAC2025Crawler

crawler = ImprovedIPAC2025Crawler()
papers = crawler.crawl_conference()
crawler.save_papers(papers, 'ipac2025_papers.json')
```

### conferences.IPAC2025.analyze_real_data

Data analysis module for processing extracted paper datasets.

#### analyze_papers

**Function**: `analyze_papers(filename)`

Analyze extracted paper data and generate comprehensive statistics.

**Parameters**:
- `filename` (str): Path to JSON file containing paper data

**Returns**:
- `bool`: True if analysis completed successfully

**Example Usage**:

```python
from conferences.IPAC2025.analyze_real_data import analyze_papers

success = analyze_papers('ipac2025_real_papers.json')
```

## Data Schema

### Paper Object Structure

```json
{
    "url": "https://indico.jacow.org/event/81/contributions/123",
    "title": "Paper Title",
    "authors": ["Author 1", "Author 2"],
    "institutions": ["Institution A", "Institution B"],
    "abstract": "Paper abstract content...",
    "category": "Paper category",
    "session": "Conference session",
    "type": "Paper type",
    "datetime": "Presentation datetime",
    "keywords": ["keyword1", "keyword2"],
    "conference": "IPAC2025",
    "contribution_id": "123"
}
```

### Dataset Structure

```json
{
    "conference": "IPAC2025",
    "source": "Real Indico Website",
    "url": "https://indico.jacow.org/event/81/",
    "crawl_date": "2025-01-01 12:00:00",
    "statistics": {
        "total_papers": 1438,
        "papers_with_abstracts": 1429,
        "papers_with_authors": 1438,
        "average_title_length": 75.5
    },
    "papers": [...]
}
```

## Error Handling

The API implements comprehensive error handling:

- **Network Errors**: Automatic retry with exponential backoff
- **Parsing Errors**: Graceful degradation with partial data extraction
- **File I/O Errors**: Clear error messages and recovery suggestions
- **Data Validation**: Schema validation for all extracted data

## Rate Limiting

To respect target servers:

- Default delay: 1-3 seconds between requests
- Batch processing: 5 papers per batch with extended delay
- User-Agent identification for transparency
- Compliance with robots.txt when available

## Configuration

### Environment Variables

- `SRF_CI_DELAY`: Override default request delay (seconds)
- `SRF_CI_MAX_RETRIES`: Maximum retry attempts for failed requests
- `SRF_CI_TIMEOUT`: Request timeout in seconds

### Command Line Interface

```bash
# Crawl IPAC2025 papers
srf-insights crawl ipac2025 --limit 100 --output papers.json

# Analyze extracted data
srf-insights analyze --input papers.json
```

## Testing

Run the test suite:

```bash
pytest tests/ --cov=conferences --cov-report=html
```

## Support

For API questions and support:

- GitHub Issues: https://github.com/iuming/SRF_Conference_Insights/issues
- Email: mliu@ihep.ac.cn
- Documentation: https://iuming.github.io/SRF_Conference_Insights/
