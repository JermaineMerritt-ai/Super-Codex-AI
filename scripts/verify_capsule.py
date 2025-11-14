#!/usr/bin/env python3
"""
Capsule Verification Script
Verifies the SHA256 checksum of a capsule file against an expected value
"""

import zipfile
import hashlib
import sys

def main():
    """Main function to verify capsule checksum"""
    if len(sys.argv) < 3:
        print("Usage: python verify_capsule.py <capsule_file> <expected_sha256>")
        sys.exit(1)
    
    capsule = sys.argv[1]
    expected = sys.argv[2]  # expected SHA256
    
    try:
        h = hashlib.sha256()
        with open(capsule, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        digest = h.hexdigest()
        print("Capsule SHA256:", digest)
        print("OK" if digest == expected else "MISMATCH")
        
        # Exit with appropriate code
        sys.exit(0 if digest == expected else 1)
        
    except FileNotFoundError:
        print(f"Error: Capsule file '{capsule}' not found")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied reading '{capsule}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()