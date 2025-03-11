import os
import argparse
from pubmed_fetcher import PubMedFetcher  # Import the PubMedFetcher class
from tabulate import tabulate

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-f", "--file", type=str, help="Output CSV file name")

    args = parser.parse_args()
    
    if args.debug:
        print(f"Debug: Received query: {args.query}")
        print(f"Debug: Output filename: {args.file if args.file else 'results/default_results.csv'}")

    try:
        print("Fetching papers...")
        fetcher = PubMedFetcher(query=args.query)  # Instantiate the PubMedFetcher
        paper_ids = fetcher.fetch_papers()  # Call the method to fetch paper IDs
        
        if args.debug:
            print(f"Debug: Retrieved paper IDs: {paper_ids}")

        paper_details = [fetcher.fetch_paper_details(pid) for pid in paper_ids]  # Fetch details for each paper

        # Ensure results directory exists
        os.makedirs("results", exist_ok=True)

        # Generate filename dynamically based on query if not provided
        filename = args.file if args.file else f"results/{args.query.replace(' ', '_')}_results.csv"

        # Save the results to a CSV file
        fetcher.save_to_csv(paper_details, filename)

        # Format data for tabular display
        table_data = [
            [
                paper["PubmedID"],
                paper["Title"],
                paper["Publication Date"],
                ", ".join(paper.get("Non-academic Author(s)", [])),
                ", ".join(paper.get("Company Affiliation(s)", [])),
                paper.get("Corresponding Author Email", "N/A")
            ]
            for paper in paper_details
        ]

        # Print results in table format
        print("\n🔹 Research Papers Found:")
        print(tabulate(table_data, headers=["PubmedID", "Title", "Publication Date", "Non-academic Authors", "Company Affiliations", "Corresponding Email"], tablefmt="grid"))

    except Exception as e:
        print(f"An error occurred: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()