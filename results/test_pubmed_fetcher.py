import pytest
from pubmed_fetcher import fetch_papers, fetch_paper_details, save_to_csv

def test_fetch_papers():
    """Test fetching paper IDs from PubMed API"""
    result = fetch_papers("cancer", max_results=5)
    assert isinstance(result, list)
    assert len(result) > 0  # Ensure we get at least one result
    assert all(isinstance(i, str) for i in result)  # Ensure IDs are strings

def test_fetch_paper_details():
    """Test fetching paper details from PubMed API"""
    sample_id = "40064631"  # Example PubMed ID
    result = fetch_paper_details(sample_id)
    assert isinstance(result, dict)
    assert "PubmedID" in result
    assert "Title" in result
    assert "Publication Date" in result

# Run tests with pytest
if __name__ == "__main__":
    pytest.main()
