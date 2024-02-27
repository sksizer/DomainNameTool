#!/usr/bin/env python
import subprocess
import sys

def main():
    script_path = "tld_finder/find_tlds.py"
    if len(sys.argv) < 2:
        print("Usage: ./run_tld_finder.py words [words ...]")
        print("Example: ./run_tld_finder.py google amazon facebook")
        sys.exit(1) 
    subprocess.run(["python", script_path] + sys.argv[1:], check=True)

if __name__ == "__main__":
    main()
