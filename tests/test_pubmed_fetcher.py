from pubmed_fetcher_kiran import fetch_pubmed_ids
import requests
from unittest.mock import patch


@patch("requests.get")
def test_fetch_pubmed_ids(mock_get):
    mock_response = {
        "esearchresult": {
            "idlist": ["12345", "67890"]
        }
    }
    mock_get.return_value.json.return_value = mock_response
    result = fetch_pubmed_ids("cancer")
    assert result == ["12345", "67890"]
