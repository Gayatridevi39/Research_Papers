import logging
import requests
import pandas as pd
import xml.etree.ElementTree as ET
from typing import List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class PubMedFetcher:
    PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

    def __init__(self, query: str, max_results: int = 10):
        self.query = query
        self.max_results = max_results

    def fetch_papers(self) -> List[str]:
        """Fetch research paper IDs from PubMed."""
        params = {
            "db": "pubmed",
            "term": self.query,
            "retmode": "json",
            "retmax": self.max_results
        }
        response = requests.get(self.PUBMED_API_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        return data["esearchresult"].get("idlist", [])

    def fetch_paper_details(self, paper_id: str) -> Dict:
        """Fetch details of a research paper from PubMed."""
        params = {
            "db": "pubmed",
            "id": paper_id,
            "retmode": "xml"
        }
        response = requests.get(self.PUBMED_FETCH_URL, params=params)
        response.raise_for_status()
        
        root = ET.fromstring(response.text)
        paper_info = {
            "PubmedID": paper_id,
            "Title": root.find(".//ArticleTitle").text if root.find(".//ArticleTitle") is not None else "",
            "Publication Date": root.find(".//PubDate/Year").text if root.find(".//PubDate/Year") is not None else "",
            "Non-academic Author(s)": [],
            "Company Affiliation(s)": [],
            "Corresponding Author Email": ""
        }
        return paper_info

    def save_to_csv(self, papers: List[Dict], filename: str = "results/output.csv"):
        """Save research papers to a CSV file."""
        if not papers:
            logging.warning("⚠ No papers found. CSV file was not created.")
            return

        df = pd.DataFrame(papers)
        df.to_csv(filename, index=False, quoting=1)
        logging.info(f"✅ Results successfully saved to: {filename}")
