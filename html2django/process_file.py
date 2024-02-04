from djangohtml import djangoify
import sys


def main():
    # Check if a file path is provided as a command line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    # Call the djangoify function from the djangohtml module
    djangoify(file_path)

if __name__ == "__main__":
    main()

