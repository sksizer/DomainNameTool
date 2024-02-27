import argparse
import json

def load_tlds():
    with open("tlds-alpha-by-domain.txt", "r") as file:
        return [line.strip().lower() for line in file.readlines() if not line.startswith("#")]

def find_matching_tlds(words, tlds):
    matches = {}
    for word in words:
        for tld in tlds:
            if word.endswith(tld):
                domain = f"{word[:-len(tld)]}.{tld}"
                if word in matches:
                    matches[word].append(domain)
                else:
                    matches[word] = [domain]
    return matches

def main():
    parser = argparse.ArgumentParser(description="Find TLDs that can complete the end of given words.")
    parser.add_argument("words", nargs="+", help="List of words to check for matching TLDs.")
    parser.add_argument("--output", "-o", default="tld_matches.json", help="Output JSON file name.")
    args = parser.parse_args()

    tlds = load_tlds()
    matches = find_matching_tlds(args.words, tlds)

    with open(args.output, "w") as file:
        json.dump(matches, file, indent=4)

if __name__ == "__main__":
    main()
