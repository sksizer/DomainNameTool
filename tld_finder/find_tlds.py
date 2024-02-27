from tqdm import tqdm
from download_tlds import download_tlds
import webbrowser
import http.server
import argparse
import json
import whois

def load_tlds():
    import os
    script_dir = os.path.dirname(__file__)  # Get the directory where the script is located
    tlds_file_path = os.path.join(script_dir, "tlds-alpha-by-domain.txt")
    if not os.path.exists(tlds_file_path):
        print("TLDs file not found. Downloading TLDs list...")
        download_tlds()
        if not os.path.exists(tlds_file_path):
            print("Failed to download TLDs list. Please check your internet connection.")
            exit(1)
    with open(tlds_file_path, "r") as file:
        return [line.strip().lower() for line in file.readlines() if not line.startswith("#")]

def find_matching_tlds(words, tlds):
    matches = {}
    for word in words:
        if word not in matches:
            matches[word] = []
        domain = None  # Ensure domain is defined before conditional checks
        for tld in tlds:
            if word.endswith("." + tld):
                domain = f"{word}"
            elif word.endswith(tld):
                domain = f"{word[:-len(tld)]}.{tld}"
            if domain:
                if word in matches:
                    if domain not in matches[word]:
                        matches[word].append(domain)
                else:
                    matches[word] = [domain]
    return matches

def check_domain_availability(domains, verbose=False):
    availability = {}
    domains_iter = tqdm(domains, desc="Checking domain availability") if verbose else domains
    for domain in domains_iter:
        try:
            w = whois.whois(domain)
            # If the WHOIS library can find a record, the domain is likely registered.
            # Note: WHOIS data structures can be inconsistent across TLDs; this is a basic check.
            # Change to boolean: false for available, true for registered or unknown
            availability[domain] = False if not w.domain_name else True
        except Exception as e:
            # Handle exceptions, e.g., rate limits, connectivity issues, etc.
            # Treat unknown as true to indicate not available for registration without specific status
            availability[domain] = True
    return availability

def main():
    parser = argparse.ArgumentParser(description="Find TLDs that can complete the end of given words.")
    parser.add_argument("words", nargs="+", help="List of words to check for matching TLDs.")
    parser.add_argument("--output", "-o", default="tld_matches.json", help="Output JSON file name.")
    parser.add_argument("--serve", action="store_true", help="Serve the results via a web server.")
    args = parser.parse_args()

    tlds = load_tlds()
    matches = find_matching_tlds(args.words, tlds)

    # Flatten the list of domains to check their availability
    all_domains = [domain for match_list in matches.values() for domain in match_list]
    availability = check_domain_availability(all_domains, verbose=True)

    # Include availability information in the matches output
    for word, domains in matches.items():
        # Adjust the structure to nest results under "results" key and change availability to boolean
        matches[word] = {"results": [{'domain': domain, 'available': not availability[domain]} for domain in domains]}

    import os
    output_file_path = os.path.join(os.path.dirname(__file__), args.output)
    with open(output_file_path, "w") as file:
        json.dump(matches, file, indent=4)

    if args.serve:
        port = 8000
        directory = os.path.dirname(__file__)
        os.chdir(directory)  # Change the current working directory
        handler = http.server.SimpleHTTPRequestHandler
        httpd = http.server.HTTPServer(("", port), handler)
        print(f"Serving at port {port}. Open http://localhost:{port}/index.html in your browser.")
        webbrowser.open(f'http://localhost:{port}/index.html')
        httpd.serve_forever()

if __name__ == "__main__":
    main()
