#!/usr/bin/env python3
"""
Test Service for Systemd Crown
Sacred flame test service
"""

import time
import sys

print('Sacred flame test service ignited!')
sys.stdout.flush()

while True:
    print(f'Flame burning at {time.strftime("%Y-%m-%d %H:%M:%S")}')
    sys.stdout.flush()
    time.sleep(10)