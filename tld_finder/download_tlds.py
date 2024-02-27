from tqdm import tqdm
import requests

def download_tlds():
    url = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"
    response = requests.get(url)
    if response.status_code == 200:
        with open("tlds-alpha-by-domain.txt", "w") as file:
            # Split the response into lines for progress reporting
            lines = response.text.splitlines()
            for line in tqdm(lines, desc="Downloading TLDs"):
                file.write(f"{line}\n")
    else:
        print(f"Failed to download TLDs list. Status code: {response.status_code}")

if __name__ == "__main__":
    download_tlds()
