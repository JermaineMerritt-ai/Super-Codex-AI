#!/usr/bin/env python3
"""
Lesson to Scroll Conversion Script
Converts lesson JSON files to sealed scrolls in the Codex Dominion system
"""

import json
import sys
import requests
import os

# Configuration
API = os.getenv("API_URL", "https://codexdominion.app/v1")
HEAD = {"Authorization": f"Bearer {os.getenv('CLI_API_KEY')}"}

def main():
    """Main function to convert lesson to sealed scroll"""
    if len(sys.argv) < 2:
        print("Usage: python lesson_to_scroll.py <lesson.json>")
        sys.exit(1)
    
    lesson_file = sys.argv[1]
    
    try:
        # Load lesson data
        with open(lesson_file, 'r') as f:
            lesson = json.load(f)
        
        # Create artifact payload
        payload = {
            "title": lesson["title"],
            "slug": lesson["slug"], 
            "type": "Guide",
            "content_uri": lesson["pdf_path"]
        }
        
        # Create artifact
        r = requests.post(f"{API}/artifacts", json=payload, headers=HEAD)
        r.raise_for_status()
        aid = r.json()["id"]
        
        # Seal the artifact
        requests.post(f"{API}/artifacts/{aid}/seal", headers=HEAD).raise_for_status()
        
        print("Sealed lesson scroll:", aid)
        
    except FileNotFoundError:
        print(f"Error: Lesson file '{lesson_file}' not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in '{lesson_file}'")
        sys.exit(1)
    except KeyError as e:
        print(f"Error: Missing required field {e} in lesson data")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error: API request failed - {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()