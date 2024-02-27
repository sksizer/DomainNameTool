import requests

def download_tlds():
    url = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"
    response = requests.get(url)
    if response.status_code == 200:
        with open("tlds-alpha-by-domain.txt", "w") as file:
            file.write(response.text)
    else:
        print(f"Failed to download TLDs list. Status code: {response.status_code}")

if __name__ == "__main__":
    download_tlds()
