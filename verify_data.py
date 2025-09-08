#!/usr/bin/env python3
"""
SRF Conference Insights - Data Verification and Backup Script

This script ensures that all necessary data files exist for the web interface
and creates backup/fallback data if needed.

Author: Ming Liu <mliu@ihep.ac.cn>
Project: SRF Conference Insights
Institution: Institute of High Energy Physics, Chinese Academy of Sciences
"""

import json
import os
from pathlib import Path

def ensure_data_files():
    """Ensure all necessary data files exist for the web interface."""
    docs_dir = Path(__file__).parent / "docs"
    data_dir = docs_dir / "data"
    
    # Create data directory if it doesn't exist
    data_dir.mkdir(exist_ok=True)
    
    # Define minimal fallback data
    fallback_data = {
        "extraction_time": "2025-09-08T12:00:00",
        "total_papers": 3,
        "papers": [
            {
                "paper_number": 1,
                "filename": "sample_paper_1.pdf",
                "title": "Superconducting Radio Frequency Accelerator Development",
                "authors": ["Dr. John Smith", "Prof. Mary Johnson"],
                "affiliations": ["Michigan State University", "CERN"],
                "abstract": "This paper presents the latest developments in superconducting radio frequency (SRF) accelerator technology, focusing on improved cavity designs and enhanced performance metrics.",
                "keywords": ["SRF", "accelerator", "superconducting", "cavity"],
                "page_count": 8,
                "file_size_kb": 1200.5,
                "figures": ["Figure 1", "Figure 2", "Figure 3"],
                "tables": ["Table 1"],
                "references": ["Ref 1", "Ref 2"],
                "sections": {
                    "Introduction": "Introduction to SRF technology",
                    "Methodology": "Experimental setup and procedures",
                    "Results": "Key findings and measurements",
                    "Conclusion": "Summary and future work"
                },
                "reference_count": 25,
                "figure_count": 3,
                "table_count": 1
            },
            {
                "paper_number": 2,
                "filename": "sample_paper_2.pdf",
                "title": "Beam Dynamics in High-Intensity Accelerators",
                "authors": ["Dr. David Brown", "Dr. Sarah Wilson"],
                "affiliations": ["Fermilab", "DESY"],
                "abstract": "Analysis of beam dynamics effects in high-intensity particle accelerators, with emphasis on space charge effects and mitigation strategies.",
                "keywords": ["beam dynamics", "space charge", "high intensity", "accelerator"],
                "page_count": 6,
                "file_size_kb": 850.2,
                "figures": ["Figure 1", "Figure 2"],
                "tables": [],
                "references": ["Ref 1", "Ref 2", "Ref 3"],
                "sections": {
                    "Introduction": "Overview of beam dynamics challenges",
                    "Theory": "Theoretical framework",
                    "Simulation": "Numerical simulation results",
                    "Conclusion": "Key insights and recommendations"
                },
                "reference_count": 18,
                "figure_count": 2,
                "table_count": 0
            },
            {
                "paper_number": 3,
                "filename": "sample_paper_3.pdf",
                "title": "Machine Learning Applications in Accelerator Physics",
                "authors": ["Prof. Lisa Chen", "Dr. Michael Zhang"],
                "affiliations": ["Stanford University", "KEK"],
                "abstract": "Exploring the application of machine learning techniques for accelerator optimization, fault prediction, and automated tuning procedures.",
                "keywords": ["machine learning", "accelerator", "optimization", "automation"],
                "page_count": 10,
                "file_size_kb": 1450.8,
                "figures": ["Figure 1", "Figure 2", "Figure 3", "Figure 4"],
                "tables": ["Table 1", "Table 2"],
                "references": ["Ref 1", "Ref 2", "Ref 3", "Ref 4"],
                "sections": {
                    "Introduction": "ML in accelerator physics overview",
                    "Methods": "ML algorithms and implementation",
                    "Applications": "Real-world case studies",
                    "Results": "Performance evaluation",
                    "Discussion": "Benefits and limitations",
                    "Conclusion": "Future prospects"
                },
                "reference_count": 32,
                "figure_count": 4,
                "table_count": 2
            }
        ]
    }
    
    # Ensure required data files exist
    required_files = [
        "papers-simple.json",
        "papers-medium.json", 
        "papers.json"
    ]
    
    for filename in required_files:
        filepath = data_dir / filename
        if not filepath.exists():
            print(f"Creating fallback data file: {filename}")
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(fallback_data, f, ensure_ascii=False, indent=2)
        else:
            print(f"Data file exists: {filename}")
    
    # Verify web files exist
    web_files = [
        "index.html",
        "app-simple.js"
    ]
    
    for filename in web_files:
        filepath = docs_dir / filename
        if filepath.exists():
            print(f"✅ Web file exists: {filename}")
        else:
            print(f"❌ Missing web file: {filename}")
    
    print("Data verification complete!")

if __name__ == "__main__":
    ensure_data_files()
