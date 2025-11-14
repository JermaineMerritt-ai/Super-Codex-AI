#!/usr/bin/env python3
"""
File Checksum Script
Generates SHA256 checksum for any given file
"""

import hashlib
import sys

def main():
    """Main function to calculate and print file checksum"""
    if len(sys.argv) < 2:
        print("Usage: python checksum_file.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    try:
        with open(file_path, "rb") as f:
            print(hashlib.sha256(f.read()).hexdigest())
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied reading '{file_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()