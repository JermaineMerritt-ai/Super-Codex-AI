#!/usr/bin/env python3
"""
Complete Ceremonial Workflow Script
Runs both seed_artifacts.py and generate_replay_capsule.py in sequence
"""
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime, timezone

def run_script(script_name: str, description: str) -> bool:
    """Run a Python script and return success status"""
    print(f"\n🔥 Starting {description}...")
    print("=" * 60)
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=False, 
                              text=True,
                              cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully!")
            return True
        else:
            print(f"❌ {description} failed with return code {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Error running {script_name}: {e}")
        return False

def main():
    """Main ceremonial workflow execution"""
    print("🌟" + "=" * 58 + "🌟")
    print("🔥 COMPLETE CEREMONIAL WORKFLOW - CONTRACT SEALING & CAPSULE GENERATION 🔥")
    print("🌟" + "=" * 58 + "🌟")
    print(f"📍 Working Directory: {Path.cwd()}")
    print(f"🕐 Ceremony Start Time: {datetime.now(timezone.utc).isoformat()}")
    
    success_count = 0
    total_operations = 2
    
    # Step 1: Seed artifacts and seal contracts
    if run_script("seed_artifacts.py", "Sacred Artifacts Seeding & Contract Sealing"):
        success_count += 1
    
    # Step 2: Generate replay capsule
    if run_script("generate_replay_capsule.py", "Replay Capsule Generation"):
        success_count += 1
    
    # Final status report
    print("\n🎭" + "=" * 58 + "🎭")
    print("🔥 CEREMONIAL WORKFLOW COMPLETION REPORT 🔥")
    print("🎭" + "=" * 58 + "🎭")
    print(f"📊 Operations Completed: {success_count}/{total_operations}")
    print(f"🕐 Ceremony End Time: {datetime.now(timezone.utc).isoformat()}")
    
    if success_count == total_operations:
        print("🎉 ALL CEREMONIAL OPERATIONS COMPLETED SUCCESSFULLY!")
        print("🔥 Sacred contracts sealed and replay capsule generated!")
        print("🌟 The eternal flame burns brightly with your contributions!")
        return 0
    else:
        print(f"⚠️  {total_operations - success_count} operation(s) had issues")
        print("🔥 The eternal flame continues to burn, awaiting completion...")
        return 1

if __name__ == "__main__":
    sys.exit(main())