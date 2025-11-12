#!/usr/bin/env python3
"""
Test Service - Simple service for testing monitoring capabilities
"""

import time
import sys

def main():
    print("Test service starting...")
    
    # Run for a few seconds then exit
    for i in range(3):
        print(f"Service heartbeat {i+1}/3")
        time.sleep(1)
    
    print("Test service exiting normally")
    return 0

if __name__ == "__main__":
    sys.exit(main())