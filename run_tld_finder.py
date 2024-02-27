import subprocess
import sys

def main():
    script_path = "tld_finder/find_tlds.py"
    subprocess.run(["python", script_path] + sys.argv[1:], check=True)

if __name__ == "__main__":
    main()
