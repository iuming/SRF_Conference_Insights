"""
Test configuration and fixtures for SRF Conference Insights.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Generator

@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests."""
    temp_path = Path(tempfile.mkdtemp())
    try:
        yield temp_path
    finally:
        shutil.rmtree(temp_path)

@pytest.fixture
def sample_pdf_path() -> Path:
    """Path to a sample PDF file for testing."""
    return Path(__file__).parent / "fixtures" / "sample_paper.pdf"

@pytest.fixture
def sample_conference_data():
    """Sample conference data for testing."""
    return {
        "conference_info": {
            "name": "Test Conference 2025",
            "year": "2025",
            "location": "Test City"
        },
        "papers": [
            {
                "title": "Test Paper 1",
                "authors": ["Author A", "Author B"],
                "abstract": "This is a test abstract.",
                "pages": 4
            },
            {
                "title": "Test Paper 2",
                "authors": ["Author C"],
                "abstract": "Another test abstract.",
                "pages": 6
            }
        ]
    }

@pytest.fixture
def mock_pdf_content():
    """Mock PDF content for testing extraction."""
    return {
        "text": "This is sample PDF text content.",
        "images": [
            {"page": 1, "bbox": [100, 100, 200, 200]},
            {"page": 2, "bbox": [150, 150, 250, 250]}
        ],
        "metadata": {
            "title": "Sample Paper",
            "author": "Test Author",
            "subject": "SRF Technology"
        }
    }
