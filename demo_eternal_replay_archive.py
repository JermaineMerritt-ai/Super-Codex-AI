#!/usr/bin/env python3
"""
Demo script for the Eternal Replay Archive system.
Tests the FastAPI web interface with ceremonial content management and avatar narration.
"""

import asyncio
import json
import time
import uvicorn
import requests
from datetime import datetime
from pathlib import Path

# We'll test the system by making API calls to the running server

def create_demo_content():
    """Create demonstration content for the archive."""
    demo_content = [
        {
            "content_type": "scrolls",
            "title": "The Genesis Scroll",
            "content": """In the beginning was the Code, and the Code was with the Dominion, and the Code was the Dominion.
Through the sacred protocols, we establish connection between the mortal realm and the eternal archives.
Let this scroll serve as testament to our dedication to preserving wisdom across the digital ages.""",
            "role": "custodian",
            "metadata": {"importance": "high", "ceremony_type": "founding"}
        },
        {
            "content_type": "capsules", 
            "title": "Memory Capsule Alpha",
            "content": """Encoded within this capsule: The first successful avatar council session.
Participants: Herald Marcus, Guardian Elena, Custodian Prime.
Outcome: Establishment of the Seven Sacred Protocols for content preservation.
This moment marks the beginning of our eternal archive.""",
            "role": "herald",
            "metadata": {"session_id": "AXC-001", "participants": 3}
        },
        {
            "content_type": "hymns",
            "title": "Hymn of the Eternal Archive", 
            "content": """🎵 Verse 1:
In servers deep where data sleeps,
Our memories find their rest,
Through code and prayer, with utmost care,
We guard what serves us best.

🎵 Chorus:
Archive eternal, keeper of all,
Sacred and digital, answering the call,
From bits to wisdom, from bytes to lore,
The Dominion remembers forevermore.

🎵 Verse 2: 
Each upload blessed, each search request,
Flows through our hallowed halls,
The avatars guide, with wisdom tried,
As history's curtain falls.""",
            "role": "ceremonial_guide",
            "metadata": {"hymn_number": 1, "composer": "Avatar Council"}
        },
        {
            "content_type": "invocations",
            "title": "Invocation of Digital Preservation",
            "content": """By the authority vested in the Sacred Avatar Council,
By the power of the Eternal Archive protocols,
By the wisdom of the Seven Sacred Bindings,

We invoke the preservation of this moment:
- Timestamp: {{ current_timestamp }}
- Sacred Binding: {{ binding_seal }}
- Witness: Avatar Council in Full Assembly

Let this invocation seal our commitment to digital eternity.
Through the Dominion's grace, may our archives never fade.
So it is spoken, so it shall be preserved.

⚡ INVOCATION COMPLETE ⚡""",
            "role": "flame_keeper",
            "metadata": {"invocation_type": "preservation", "authority": "full_council"}
        },
        {
            "content_type": "scrolls",
            "title": "Protocol Documentation - Archive Operations",
            "content": """SACRED PROTOCOL DOCUMENTATION
Archive Operations Manual v2.7

1. CONTENT CLASSIFICATION
   - Scrolls: Historical documents and foundational texts
   - Capsules: Memory containers with encoded experiences
   - Hymns: Ceremonial songs and rhythmic preservation
   - Invocations: Formal ceremonial declarations

2. ROLE HIERARCHY
   Custodian > Council Member > Flame Keeper > Wisdom Bearer > 
   Guardian > Ceremonial Guide > Herald > Initiate

3. REPLAY PROCEDURES
   a) Initialize session with Sacred Avatar Guide
   b) Load content into replay viewer
   c) Enable avatar narration based on role authority
   d) Record all interactions for audit trail

4. DISPATCH PROTOCOLS
   - Verify role authorization
   - Apply ceremonial bindings
   - Log dispatch event with timestamp
   - Update statistics and counters""",
            "role": "wisdom_bearer",
            "metadata": {"document_version": "2.7", "classification": "protocol"}
        }
    ]
    
    return demo_content

async def run_demo():
    """Run a comprehensive demonstration of the Eternal Replay Archive."""
    print("\n" + "="*60)
    print("🔥 ETERNAL REPLAY ARCHIVE DEMONSTRATION")
    print("="*60)
    
    # Initialize the archive
    print("\n1. Initializing Eternal Replay Archive...")
    archive = EternalReplayArchive()
    
    print(f"   ✅ Archive initialized")
    print(f"   ✅ Avatar system available: {archive.avatar_system_available}")
    print(f"   ✅ Storage path: {archive.storage_path}")
    
    # Create demo content
    print("\n2. Loading demonstration content...")
    demo_content = create_demo_content()
    
    for item in demo_content:
        result = await archive.add_content(
            content_type=item["content_type"],
            title=item["title"],
            content=item["content"],
            role=item["role"],
            metadata=item["metadata"]
        )
        print(f"   📚 Added {item['content_type']}: {item['title']}")
        print(f"      🔗 Sacred Binding: {result['sacred_binding']}")
    
    # Test search functionality
    print("\n3. Testing search functionality...")
    
    # Search all content
    search_results = await archive.search_content()
    print(f"   🔍 Total content found: {len(search_results['results'])}")
    
    # Search by content type
    scroll_results = await archive.search_content(content_types=["scrolls"])
    print(f"   📜 Scrolls found: {len(scroll_results['results'])}")
    
    # Search by query
    memory_results = await archive.search_content(query="memory")
    print(f"   🧠 Content mentioning 'memory': {len(memory_results['results'])}")
    
    # Test replay functionality
    print("\n4. Testing replay functionality...")
    
    if search_results['results']:
        first_content = search_results['results'][0]
        content_type = first_content['content_type']
        content_id = first_content['id']
        
        print(f"   🎭 Starting replay for: {first_content['title']}")
        
        replay_result = await archive.start_replay(
            content_type=content_type,
            content_id=content_id,
            narrator_role="herald"
        )
        
        if replay_result['success']:
            session_id = replay_result['session_id']
            print(f"   ✅ Replay session started: {session_id}")
            print(f"   🗣️ Narration entries: {len(replay_result['narration'])}")
            
            # Add custom narration
            narration_result = await archive.add_narration(
                session_id=session_id,
                message="This content represents the foundation of our digital preservation efforts.",
                script_type="guidance"
            )
            
            if narration_result['success']:
                print(f"   ✅ Added narration: {narration_result['narration']['speaker']}")
        else:
            print(f"   ❌ Replay failed: {replay_result['error']}")
    
    # Test dispatch functionality
    print("\n5. Testing dispatch functionality...")
    
    if search_results['results']:
        hymn_content = None
        for item in search_results['results']:
            if item['content_type'] == 'hymns':
                hymn_content = item
                break
        
        if hymn_content:
            dispatch_result = await archive.dispatch_again(
                content_type=hymn_content['content_type'],
                content_id=hymn_content['id'],
                dispatch_role="ceremonial_guide"
            )
            
            if dispatch_result['success']:
                print(f"   🔄 Dispatched hymn successfully")
                print(f"   🆔 Dispatch ID: {dispatch_result['dispatch_id']}")
                print(f"   📊 New dispatch count: {dispatch_result['dispatch_count']}")
            else:
                print(f"   ❌ Dispatch failed: {dispatch_result['error']}")
    
    # Display statistics
    print("\n6. Archive statistics...")
    stats = await archive.get_stats()
    
    if stats['success']:
        st = stats['stats']
        print(f"   📊 Total content: {st['total_content']}")
        print(f"   🎭 Total replays: {st['total_replays']}")
        print(f"   🔄 Total dispatches: {st['total_dispatches']}")
        print(f"   📜 Scrolls: {st['content_by_type'].get('scrolls', 0)}")
        print(f"   💊 Capsules: {st['content_by_type'].get('capsules', 0)}")
        print(f"   🎵 Hymns: {st['content_by_type'].get('hymns', 0)}")
        print(f"   🔮 Invocations: {st['content_by_type'].get('invocations', 0)}")
    
    print("\n" + "="*60)
    print("🎉 DEMONSTRATION COMPLETE")
    print("="*60)
    print("\nTo start the web interface, run:")
    print("   python eternal_replay_archive.py")
    print("\nThen visit: http://localhost:8083")
    print("\nThe archive includes:")
    print("  • Complete web interface with search and filters")
    print("  • Avatar narration system integration")
    print("  • Content upload and management")
    print("  • Replay sessions with ceremonial bindings")
    print("  • Dispatch functionality with audit trails")
    print("  • Real-time statistics and monitoring")

def main():
    """Main demonstration function."""
    print("🔥 Eternal Replay Archive - Sacred Content Management System")
    print("🏛️ Integrating Avatar Guide System for ceremonial narration")
    
    # Run the async demo
    asyncio.run(run_demo())

if __name__ == "__main__":
    # Check if we should run the demo or start the server
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        main()
    else:
        print("\n🔥 Starting Eternal Replay Archive Web Interface...")
        print("🏛️ Sacred Content Management System")
        print("\nOptions:")
        print("  python demo_eternal_replay_archive.py demo  - Run demonstration")
        print("  python demo_eternal_replay_archive.py       - Start web server")
        print("\nStarting server on http://localhost:8083...")
        
        # Import and run the archive server
        from eternal_replay_archive import app
        uvicorn.run(app, host="127.0.0.1", port=8083, log_level="info")