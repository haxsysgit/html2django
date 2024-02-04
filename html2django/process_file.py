#!/usr/bin/python3

import os
import sys
from djangohtml import djangoify

def process_html_file(file_path):
    # Perform your operations on the HTML file here
    # For demonstration, it just prints the file path
    djangoify(file_path)
    print("Processing:", file_path)

def main(directory):
    # Check if the directory exists
    if not os.path.exists(directory):
        print("Directory not found:", directory)
        sys.exit(1)

    # Check if the path is a directory
    if not os.path.isdir(directory):
        print("The given path is not a directory:", directory)
        sys.exit(1)

    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                process_html_file(file_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory_path>")
        sys.exit(1)

    main(sys.argv[1])

