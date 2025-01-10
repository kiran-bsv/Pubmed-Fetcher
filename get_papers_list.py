import argparse
import itertools
import sys
import threading
import time
from pubmed_fetcher_kiran import fetch_pubmed_ids, fetch_paper_details, parse_pubmed_xml, save_to_csv

def spinner(msg: str, stop_event: threading.Event):
    """
    Display a spinning loader with a message while the stop_event is not set.
    """
    spinner_cycle = itertools.cycle(["|", "/", "-", "\\"])
    while not stop_event.is_set():
        sys.stdout.write(f"\r{msg} {next(spinner_cycle)}")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * len(msg) + " \r") 

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers based on a query.")
    parser.add_argument("query", type=str, help="PubMed query string")
    parser.add_argument("-n", "--num-results", type=int, default=100, help="Number of results to fetch")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-f", "--file", type=str, help="Filename to save the results (CSV)")
    args = parser.parse_args()

    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=spinner, args=("Processing...", stop_event))

    try:
        spinner_thread.start()
        pubmed_ids = fetch_pubmed_ids(args.query, retmax=args.num_results, debug=args.debug)

        if not pubmed_ids:
            print("\nNo results found for the query.")
            return

        papers_xml = fetch_paper_details(pubmed_ids, debug=args.debug)
        processed_data = parse_pubmed_xml(papers_xml)

    finally:
        stop_event.set()
        spinner_thread.join()

    # Save to CSV or print to console
    if args.file:
        save_to_csv(processed_data, args.file)
        print(f"Results saved to {args.file}")
    else:
        # Print to console
        print("PubmedID, Title, Publication Date, Non academic Authors -  Company Affiliations - Corresponding Author Email")

        def flatten(row):
            return [str(item) if not isinstance(item, list) else ", ".join(map(str, item)) for item in row]

        for row in processed_data:
            flattened_row = flatten(row)
            print(", ".join(flattened_row))

        # for row in processed_data:
        #     print(", ".join(row))

if __name__ == "__main__":
    main()
