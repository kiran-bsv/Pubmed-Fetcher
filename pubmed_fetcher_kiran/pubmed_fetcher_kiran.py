import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional, Union
import csv


PUBMED_API_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
FETCH_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def fetch_pubmed_ids(query: str,retmax: 100, debug = False) -> List[str]:
    """Fetch PubMed IDs based on the query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": retmax,
    }
    if debug:
        print(f"Fetching PubMed IDs with query: {query}")
    response = requests.get(PUBMED_API_BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])


def fetch_paper_details(pubmed_ids: List[str], debug = False) -> str:
    """Fetch paper details for the given PubMed IDs."""
    ids = ",".join(pubmed_ids)
    params = {
        "db": "pubmed",
        "id": ids,
        "retmode": "xml",
    }
    if debug:
        print(f"Fetching details for PubMed IDs: {ids}")
    response = requests.get(FETCH_BASE_URL, params=params)
    response.raise_for_status()
    return response.text


def parse_pubmed_xml(xml_data: str) ->  List[List[Optional[Union[str, Dict]]]]:
    """Parse PubMed XML to extract details."""
    root = ET.fromstring(xml_data)
    articles = []
    academic_keywords = {"university", "college", "institute", "academy", "labs", "school"}
    company_keywords = {"company", "biotech", "pharmaceutical", "corporation", "inc", "ltd"}

    for article in root.findall(".//PubmedArticle"):
        # Extract PubMed ID
        pmid = article.find(".//PMID").text if article.find(".//PMID") is not None else ""

        # Extract and handle ArticleTitle with nested tags
        title_element = article.find(".//ArticleTitle")
        title = "".join(title_element.itertext()) if title_element is not None else ""

        # Extract publication date with year, month, and day
        pub_date_element = article.find(".//PubDate")
        pub_date = ""
        if pub_date_element is not None:
            year = pub_date_element.find("Year").text if pub_date_element.find("Year") is not None else ""
            month = pub_date_element.find("Month").text if pub_date_element.find("Month") is not None else ""
            day = pub_date_element.find("Day").text if pub_date_element.find("Day") is not None else ""
            pub_date = "-".join(filter(None, [year, month, day])) or None

        authors_data = []
        for author in article.findall(".//Author"):  # Fix scope of authors
            # Extract author details
            last_name = author.find("LastName").text if author.find("LastName") is not None else ""
            fore_name = author.find("ForeName").text if author.find("ForeName") is not None else ""
            full_name = f"{fore_name} {last_name}".strip()
            
            # Extract affiliation
            affiliation_element = author.find("AffiliationInfo/Affiliation")
            affiliation = affiliation_element.text if affiliation_element is not None else ""
            
            # Extract email if present
            email = next((word for word in (affiliation or "").split() if "@" in word), "")

            # Determine if the author is non-academic or part of a company
            affiliation_lower = affiliation.lower()
            is_academic = any(keyword in affiliation_lower for keyword in academic_keywords)
            is_company = any(keyword in affiliation_lower for keyword in company_keywords)
            
            # Add non-academic authors and their details
            if not is_academic:
                # Remove email from affiliation
                if email:
                    affiliation = affiliation.replace(email, "").strip()
                
                authors_data.append({
                    "name": full_name,
                    "affiliation": affiliation,
                    "email": email,
                })
        if not authors_data: authors_data = "There are no non-academic authors"
        articles.append([pmid, title, pub_date, authors_data])

    return articles


def save_to_csv(data: List[List[Optional[Union[str, Dict]]]], filename: str) -> None:
    """Save data to a CSV file."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write headers
        writer.writerow(["PubmedID", "Title", "Publication Date", "Non academic Authors -  Company Affiliations - Corresponding Author Email"])
        # Write data
        writer.writerows(data)