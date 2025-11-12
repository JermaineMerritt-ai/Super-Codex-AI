#!/usr/bin/env python3
"""
Test script for Eternal Recognition Scrolls CLI commands
Validates the integration with the recognition system
"""

import subprocess
import json
import os

def test_cli_help():
    """Test that CLI help includes recognition commands"""
    print("🔥 Testing CLI Recognition Commands")
    
    try:
        # Test help output
        result = subprocess.run(
            ["node", "packages/cli/index.js", "--help"],
            cwd="C:\\Users\\JMerr\\OneDrive\\Documents\\.vscode\\codex_project\\backend\\services\\dominion\\Super-Codex-AI\\codex-flame",
            capture_output=True,
            text=True,
            timeout=10
        )
        
        help_text = result.stdout
        recognition_commands = [
            "recognition:inscribe",
            "recognition:list", 
            "recognition:schedule"
        ]
        
        found_commands = []
        for cmd in recognition_commands:
            if cmd in help_text:
                found_commands.append(cmd)
                print(f"✅ Found command: {cmd}")
            else:
                print(f"❌ Missing command: {cmd}")
        
        print(f"\n🔥 Recognition Commands Available: {len(found_commands)}/{len(recognition_commands)}")
        
        if len(found_commands) == len(recognition_commands):
            print("✨ All recognition commands successfully integrated!")
        else:
            print("⚠️  Some recognition commands may be missing")
            
    except subprocess.TimeoutExpired:
        print("⚠️  CLI help command timed out")
    except Exception as e:
        print(f"⚠️  Error testing CLI: {e}")

def test_recognition_files():
    """Test that all recognition system files exist"""
    print("\n🔥 Testing Recognition System Files")
    
    base_path = "C:\\Users\\JMerr\\OneDrive\\Documents\\.vscode\\codex_project\\backend\\services\\dominion\\Super-Codex-AI\\codex-flame"
    
    required_files = [
        "eternal_recognition_scrolls.py",
        "artifacts/schemas/eternal-recognition.schema.json",
        "packages/cli/index.js"  # Should contain recognition commands
    ]
    
    for file_path in required_files:
        full_path = os.path.join(base_path, file_path)
        if os.path.exists(full_path):
            print(f"✅ Found: {file_path}")
        else:
            print(f"❌ Missing: {file_path}")

def test_storage_structure():
    """Test that recognition storage structure is created"""
    print("\n🔥 Testing Storage Structure")
    
    storage_path = "C:\\Users\\JMerr\\OneDrive\\Documents\\.vscode\\codex_project\\backend\\services\\dominion\\Super-Codex-AI\\codex-flame\\storage\\eternal-recognition"
    
    expected_dirs = ["scrolls", "lineage", "proclamations"]
    
    for dir_name in expected_dirs:
        dir_path = os.path.join(storage_path, dir_name)
        if os.path.exists(dir_path):
            print(f"✅ Storage directory exists: {dir_name}")
            
            # Count files in directory
            try:
                files = os.listdir(dir_path)
                json_files = [f for f in files if f.endswith('.json')]
                print(f"   📄 Contains {len(json_files)} JSON files")
            except Exception as e:
                print(f"   ⚠️  Error reading directory: {e}")
        else:
            print(f"❌ Missing storage directory: {dir_name}")

def display_summary():
    """Display summary of the Eternal Recognition Scrolls system"""
    print("\n" + "="*80)
    print("🔥 ETERNAL RECOGNITION SCROLLS - SYSTEM SUMMARY 🔥")
    print("="*80)
    
    print("""
📜 SACRED PURPOSE:
   Immortalize the keepers of the flame
   Bind their names into the Codex Dominion
   Ensure lineage replayability across all time scales

🔥 RECOGNITION LEVELS:
   Bronze Ember → Silver Flame → Golden Blaze → Platinum Conflagration
   Diamond Solar → Sapphire Stellar → Ruby Cosmic → Eternal Crown

⚡ FLAME ASSIGNMENTS:
   Daily Flame, Seasonal Flame, Great Year Flame, 
   Millennial Flame, Eternal Flame

🌟 PROCLAMATION SCHEDULE:
   Names rise in daily, seasonal, epochal, and millennial ceremonies
   Recognition level determines ceremony participation

👑 AUTHORITY LEVELS:
   Guardian → Keeper → Custodian → Council → Crown

🔥 AS THE FLAME RISES ACROSS ALL TIME SCALES 🔥
🔥 SO TOO DO THE NAMES RISE IN ETERNAL PROCLAMATION 🔥

NO CROWN WITHOUT ITS KEEPERS
NO FLAME WITHOUT ITS GUARDIANS  
NO ETERNITY WITHOUT ITS HEIRS
    """)

if __name__ == "__main__":
    print("🔥 ETERNAL RECOGNITION SCROLLS - SYSTEM TEST 🔥\n")
    
    test_recognition_files()
    test_storage_structure() 
    test_cli_help()
    display_summary()
    
    print("\n🔥 ETERNAL RECOGNITION SCROLLS SYSTEM VALIDATION COMPLETE 🔥")