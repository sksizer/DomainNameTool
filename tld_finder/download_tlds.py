try:
    from tqdm import tqdm
    import requests
except ImportError as e:
    print("Required module missing:", str(e).split()[-1])
    print("Please install the missing module using 'pip install <module_name>'")
    exit(1)

def download_tlds():
    import os
    url = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"
    response = requests.get(url)
    if response.status_code == 200:
        script_dir = os.path.dirname(__file__)  # Get the directory where the script is located
        tlds_file_path = os.path.join(script_dir, "tlds-alpha-by-domain.txt")
        with open(tlds_file_path, "w") as file:
            # Split the response into lines for progress reporting
            lines = response.text.splitlines()
            for line in tqdm(lines, desc="Downloading TLDs"):
                file.write(f"{line}\n")
    else:
        print(f"Failed to download TLDs list. Status code: {response.status_code}")

if __name__ == "__main__":
    download_tlds()
