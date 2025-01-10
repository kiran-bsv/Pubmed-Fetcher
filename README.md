# PubMed Fetcher

`pubmed-fetcher-kiran` is a Python tool designed to fetch research papers from PubMed based on a user-specified query. The program identifies papers with at least one author affiliated with a pharmaceutical or biotech company and returns the results in a CSV file.

## Features

- Fetch papers using PubMed's full query syntax.
- Identifies non-academic authors and their affiliations with pharmaceutical or biotech companies.
- Returns the results as a CSV with columns: `PubmedID`, `Title`, `Publication Date`, `Non-academic Author -Company Affiliation(s) - Corresponding Author Email`.
- Command-line interface (CLI) with flexible options.

## Installation

### Using Test PyPI

You can install the package from Test PyPI with the following command:

```bash
pip install -i https://test.pypi.org/simple/ pubmed-fetcher-kiran
```

## Installation from Source

Alternatively, to install from source, clone the repository and use Poetry for dependency management:

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/pubmed-fetcher-kiran.git
    cd pubmed-fetcher
    ```

2. Install dependencies using Poetry:

    ```bash
    poetry install
    ```

3. Make sure to activate the virtual environment created by Poetry:

    ```bash
    poetry shell
    ```



## Usage

Once the tool is installed, you can run the program via the command line.

### Basic Command

To fetch research papers based on a PubMed query and display the results in the console:

```bash
get-papers-list "pharmaceutical research"
```

### Save Results to CSV

To save the results to a CSV file:

```bash
get-papers-list "pharmaceutical research" -f "results.csv"
```

### Optional Arguments

- `-n` or `--num-results`: Specify the number of results to fetch (default is 100).  
- `-d` or `--debug`: Enable debug mode for additional logging.  
- `-f` or `--file`: Specify the filename to save the results (CSV). If not provided, the output will be displayed on the console.


#### Help
To view the help message with all available options:
```bash
get-papers-list -h
```

## Example Output

When running the program, the output will either be displayed in the console or saved in a CSV file with the following columns:

| PubmedID  | Title            | Publication Date | Non-academic Author - Company Affiliation - Corresponding Author Email |
|-----------|------------------|------------------|--------------------------------------------------------------------------------|
| 39791013  | Ventricular tachycardia unveiling severe undiagnosed hypothyroidism.     | 2025-Jan-09      |[{'name': 'Swaraj S Waddankeri', 'affiliation': 'Division of Diabetes and Endocrinology.', 'email': 'xyz @gmail.com'}]|

If saved to a CSV file, the result will be stored in a file named `results.csv` (or another filename you specify).



## How It Works

1. **Query**: You provide a query string (e.g., `"pharmaceutical research"`) for which the program fetches PubMed records.

2. **Fetching PubMed IDs**: The program uses the PubMed E-utilities API to fetch PubMed IDs based on the query.

3. **Fetching Paper Details**: The program then fetches the detailed paper information, including authors, titles, affiliations, and publication dates.

4. **Parsing XML**: It parses the XML data to extract the relevant details and identify non-academic authors affiliated with pharmaceutical or biotech companies.

5. **Output**: The results are displayed in the console or saved to a CSV file.

## Code Organization

The project is organized as follows:

```bash
Pubmed-Fetcher/
├── get_papers_list.ipynb           # Jupyter notebook for exploration and testing
├── get_papers_list.py              # Main script for fetching papers and processing results
├── pyproject.toml                  # Poetry configuration file
├── pubmed_fetcher_kiran/           # Module for fetching and processing PubMed papers
│   ├── __init__.py                 # Package initialization file
│   ├── cli.py                      # CLI entry point
│   └── pubmed_fetcher_kiran.py     # Main logic for fetching and processing data
└── tests/                          # Unit tests for the project
    ├── __init__.py
    ├── test_cli.py                 # Tests for the command-line interface
    └── test_pubmed_fetcher.py      # Tests for the main PubMed fetching logic
```


## Key Files

- **`pubmed_fetcher_kiran/pubmed_fetcher_kiran.py`**: Contains the core logic for fetching and parsing PubMed paper details.
- **`pubmed_fetcher_kiran/cli.py`**: Handles the command-line interface and orchestrates the program flow.
- **`tests/test_pubmed_fetcher.py`**: Unit tests for fetching and parsing PubMed paper details.
- **`tests/test_cli.py`**: Unit tests for the command-line interface.



## Dependencies

This project uses Poetry for dependency management. The following libraries are required:

- **`requests`**: For making HTTP requests to the PubMed API.
- **`xml.etree.ElementTree`**: For parsing XML data from the PubMed API.
- **`pandas`**: For working with tabular data (in .iypnb).
- **`pytest`**: For running tests.

## Contributing

Contributions are welcome! Feel free to fork the repository, create a new branch, and submit a pull request with your changes.


## Acknowledgements

- **[PubMed API - NCBI database](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi)** for fetching paper data.
- **[Poetry](https://python-poetry.org/)** for dependency management.
- **[Test PyPI](https://test.pypi.org/)** for testing package distribution.
