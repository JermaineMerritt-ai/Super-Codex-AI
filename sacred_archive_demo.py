#!/usr/bin/env python3
"""
Sacred Document Archive Demonstration
Interactive showcase of ceremonial document storage
"""

import asyncio
import tempfile
import shutil
from pathlib import Path
from io import BytesIO

from sacred_document_archive import (
    create_sacred_archive, SacredDocumentArchive, DocumentType, 
    SacredPriority, DocumentStatus
)


class MockUploadFile:
    """Mock UploadFile for demonstration"""
    
    def __init__(self, filename: str, content: bytes, content_type: str = "text/plain"):
        self.filename = filename
        self.content = content
        self.content_type = content_type
    
    async def read(self):
        return self.content


async def sacred_archive_demonstration():
    """Demonstrate the sacred document archive system"""
    
    print("🔥" + "="*70 + "🔥")
    print("   SACRED DOCUMENT ARCHIVE DEMONSTRATION")
    print("   Ceremonial Storage System for the Dominion")
    print("🔥" + "="*70 + "🔥\n")
    
    # Create temporary storage for demo
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Initialize sacred archive
        print("🌟 Initializing Sacred Document Archive...")
        archive = create_sacred_archive(storage_root=temp_dir)
        print("✅ Archive initialized with ceremonial treasury integration\n")
        
        # Display archive configuration
        print("📋 Archive Configuration:")
        print(f"   📁 Storage Root: {archive.storage_root}")
        print(f"   💰 Treasury Integration: {'Active' if archive.treasury else 'Standalone Mode'}")
        print(f"   🔐 Sacred Binding System: Active")
        print(f"   🏺 Ceremonial Seals: Active")
        print()
        
        # Create sample documents
        sample_docs = [
            {
                'filename': 'winter_solstice_ceremony.txt',
                'content': b"""SACRED CEREMONIAL SCROLL
Winter Solstice Flame Renewal Ceremony

By the authority of the Eternal Flame and the Sacred Council,
let it be known that the Winter Solstice Ceremony shall commence
at the sacred grove when the moon reaches its highest point.

All Custodians, Flame Keepers, and Council Members are summoned
to witness the renewal of the sacred flame and the blessing of
the coming year.

May the eternal light guide our path through the darkest night.

Sealed by the Sacred Council
With the blessing of the Eternal Flame""",
                'type': DocumentType.CEREMONIAL_SCROLL,
                'priority': SacredPriority.SACRED
            },
            {
                'filename': 'binding_oath_of_service.pdf',
                'content': b"""SACRED BINDING OATH

I, [Name], do solemnly swear by the eternal flame that burns
in the heart of the Dominion, to serve with honor, wisdom,
and unwavering dedication.

I pledge to:
- Protect the sacred knowledge entrusted to me
- Uphold the principles of the Eternal Flame  
- Serve the Dominion with integrity and courage
- Guard the ceremonial traditions for future generations

This oath I swear, witnessed by the eternal flame,
sealed with my sacred binding, and blessed by
the light that never dies.

Sealed in sacred fire,
[Signature and Sacred Binding]""",
                'type': DocumentType.BINDING_OATH,
                'priority': SacredPriority.DIVINE
            },
            {
                'filename': 'treasury_quarterly_report.xlsx',
                'content': b"""SACRED TREASURY QUARTERLY REPORT
Q4 2025 Financial Summary

Sacred Token Reserves: 15,847.23 ST
Ceremonial Asset Value: 42,156.89 ST
Active Allocations: 8,234.45 ST
Reserved for Ceremonies: 5,000.00 ST

Revenue Sources:
- Ceremonial Services: 12,450.00 ST
- Sacred Bindings: 3,280.50 ST
- Flame Blessings: 1,890.25 ST
- Archive Storage: 567.89 ST

Expenditures:
- Facility Maintenance: 4,200.00 ST
- Sacred Materials: 2,850.00 ST
- Staff Compensation: 6,500.00 ST
- Emergency Reserve: 1,000.00 ST

The treasury remains healthy and blessed by the eternal flame.
All allocations are properly recorded and sealed.

Verified by the Sacred Treasury
Blessed by the Eternal Flame""",
                'type': DocumentType.TREASURY_RECORD,
                'priority': SacredPriority.IMPORTANT
            },
            {
                'filename': 'council_decree_001.doc',
                'content': b"""DECREE OF THE ETERNAL COUNCIL
Decree Number: EDC-2025-001
Date: November 13, 2025

By the power vested in us by the Sacred Charter and the
blessing of the Eternal Flame, the Council hereby decrees:

NEW CEREMONIAL PROTOCOLS

1. All sacred ceremonies must now include the Flame Blessing
2. Document archives require ceremonial seals for authenticity
3. Treasury allocations above 100 Sacred Tokens need Council approval
4. Emergency alerts must be sent via sacred messaging systems

These protocols take effect immediately and shall be observed
by all members of the Dominion. Violation of these protocols
will result in ceremonial review and possible sanctions.

This decree is sealed with the authority of the Eternal Council
and blessed by the Sacred Flame.

May the eternal light guide our governance.

[Council Signatures and Sacred Seals]
Witnessed by the Eternal Flame""",
                'type': DocumentType.COUNCIL_DECREE,
                'priority': SacredPriority.DIVINE
            },
            {
                'filename': 'ancient_wisdom_codex.epub',
                'content': b"""THE CODEX OF ETERNAL WISDOM
Ancient Knowledge for Modern Flame Keepers

Chapter 1: The Nature of Sacred Fire

The eternal flame that burns at the heart of our realm is more
than mere fire - it is the manifestation of divine will, the
source of all sacred power, and the guardian of cosmic balance.

Ancient Principle #1: The Flame of Unity
All flames are connected. When we light a candle from another,
we do not diminish the source - we multiply the light. So too
with wisdom, love, and sacred knowledge.

Ancient Principle #2: The Binding of Oaths
Words spoken before the sacred flame become bonds that transcend
the physical realm. They are witnessed by forces beyond our
understanding and sealed with cosmic authority.

Ancient Principle #3: The Treasury of Souls
True wealth is not measured in gold or tokens, but in the
strength of community, the depth of wisdom, and the purity
of intention. Sacred tokens are merely symbols of this deeper
abundance.

Chapter 2: Ceremonial Practices...

[The codex continues with ancient wisdom and modern applications]

May this knowledge illuminate the path for all who seek truth.

Compiled by the Flame Keepers
Blessed by the Eternal Light""",
                'type': DocumentType.WISDOM_CODEX,
                'priority': SacredPriority.ETERNAL
            }
        ]
        
        print("📜 Archiving Sacred Documents...")
        archived_docs = []
        
        for doc_info in sample_docs:
            print(f"\n   🔥 Processing: {doc_info['filename']}")
            
            # Create mock upload file
            mock_file = MockUploadFile(
                filename=doc_info['filename'],
                content=doc_info['content'],
                content_type="application/octet-stream"
            )
            
            # Archive the document
            sacred_doc = await archive.archive_document(
                file=mock_file,
                uploader_id="demo_custodian",
                document_type=doc_info['type'],
                priority=doc_info['priority']
            )
            
            archived_docs.append(sacred_doc)
            
            print(f"      📋 Document ID: {sacred_doc.document_id}")
            print(f"      📂 Type: {sacred_doc.document_type.value}")
            print(f"      ⭐ Priority: {sacred_doc.priority.value}")
            print(f"      💾 Size: {sacred_doc.file_size:,} bytes")
            print(f"      🔐 Sacred Binding: {sacred_doc.sacred_binding}")
            print(f"      🏺 Ceremonial Seal: {sacred_doc.ceremonial_seal}")
            print(f"      💰 Treasury Cost: {sacred_doc.treasury_cost} Sacred Tokens")
            print(f"      🕯️ Flame Blessing: {sacred_doc.flame_blessing}")
        
        print(f"\n✅ Successfully archived {len(archived_docs)} sacred documents")
        
        # Demonstrate document retrieval
        print("\n📚 Document Retrieval Demonstration:")
        for i, doc in enumerate(archived_docs[:2]):  # Show first 2
            print(f"\n   🔍 Retrieving: {doc.original_name}")
            
            retrieved = await archive.get_document(doc.document_id)
            if retrieved:
                print(f"      ✅ Successfully retrieved document")
                print(f"      📄 Original Name: {retrieved.original_name}")
                print(f"      📊 Status: {retrieved.status.value}")
                print(f"      🔍 Content Hash: {retrieved.content_hash}")
                print(f"      📅 Uploaded: {retrieved.upload_timestamp}")
            else:
                print(f"      ❌ Failed to retrieve document")
        
        # Display archive statistics
        print("\n📊 Sacred Archive Statistics:")
        stats = await archive.get_document_statistics()
        
        print(f"   📜 Total Documents: {stats['total_documents']}")
        print(f"   💾 Total Storage Size: {stats['total_size_bytes']:,} bytes")
        print(f"   💰 Total Treasury Cost: {stats['total_treasury_cost']:.6f} Sacred Tokens")
        print(f"   🏥 Archive Health: {stats['archive_health']}")
        
        if stats['documents_by_type']:
            print("\n   📋 Documents by Type:")
            for doc_type, count in stats['documents_by_type'].items():
                if count > 0:
                    print(f"      {doc_type.replace('_', ' ').title()}: {count}")
        
        if stats['documents_by_priority']:
            print("\n   ⭐ Documents by Priority:")
            for priority, count in stats['documents_by_priority'].items():
                if count > 0:
                    print(f"      {priority.replace('_', ' ').title()}: {count}")
        
        if stats['storage_locations']:
            print("\n   📁 Storage Distribution:")
            for location, count in stats['storage_locations'].items():
                print(f"      {location.replace('_', ' ').title()}: {count} documents")
        
        # Show storage directory structure
        print("\n📁 Sacred Archive Directory Structure:")
        def show_directory_tree(path, indent=""):
            items = list(path.iterdir()) if path.exists() else []
            items.sort(key=lambda x: (x.is_file(), x.name))
            
            for item in items[:10]:  # Limit to first 10 items
                if item.is_dir():
                    print(f"{indent}📁 {item.name}/")
                    if len(list(item.iterdir())) > 0:
                        show_directory_tree(item, indent + "   ")
                else:
                    size = item.stat().st_size if item.exists() else 0
                    print(f"{indent}📄 {item.name} ({size:,} bytes)")
        
        show_directory_tree(archive.storage_root)
        
        # Demonstration of different document priorities and costs
        print("\n💰 Treasury Cost Analysis:")
        print("   Priority Level → Base Cost per Document")
        for priority in SacredPriority:
            base_cost = archive.archive_costs[priority]
            print(f"   {priority.value.replace('_', ' ').title():>12} → {base_cost:.3f} Sacred Tokens")
        
        print("\n   💡 Additional costs apply based on file size (0.001 ST per MB)")
        
        # Show ceremonial binding verification
        print("\n🔐 Sacred Binding Verification:")
        sample_doc = archived_docs[0]
        
        # Regenerate binding to verify authenticity
        original_binding = sample_doc.sacred_binding
        verification_data = {
            'filename': sample_doc.original_name,
            'content_hash': sample_doc.content_hash,
            'upload_timestamp': sample_doc.upload_timestamp,
            'file_size': sample_doc.file_size
        }
        
        regenerated_binding = archive._generate_sacred_binding(verification_data)
        
        print(f"   📄 Document: {sample_doc.original_name}")
        print(f"   🔐 Original Binding: {original_binding}")
        print(f"   🔍 Verification Binding: {regenerated_binding}")
        print(f"   ✅ Authenticity: {'VERIFIED' if original_binding == regenerated_binding else 'CORRUPTED'}")
        
        print("\n" + "🕯️" + "="*70 + "🕯️")
        print("   SACRED DOCUMENT ARCHIVE DEMONSTRATION COMPLETE")
        print("   All documents safely archived with eternal flame blessing")
        print("   May the sacred knowledge be preserved for all generations")
        print("🕯️" + "="*70 + "🕯️")
        
    except Exception as e:
        print(f"❌ Demonstration error: {e}")
        
    finally:
        # Cleanup temporary files
        shutil.rmtree(temp_dir, ignore_errors=True)


def show_api_examples():
    """Show FastAPI usage examples"""
    
    print("\n🔗 FastAPI Usage Examples:")
    print("="*50)
    
    print("""
# Start the sacred archive server
python sacred_document_archive.py

# Basic document upload (curl)
curl -X POST "http://localhost:8000/upload/docs" \\
     -F "file=@ceremonial_scroll.pdf"

# Upload with document type and priority
curl -X POST "http://localhost:8000/upload/docs" \\
     -F "file=@sacred_contract.pdf" \\
     -F "document_type=sacred_contract" \\
     -F "priority=divine"

# Get document information
curl "http://localhost:8000/docs/{document_id}"

# Get archive statistics
curl "http://localhost:8000/docs/stats"

# Get available document types
curl "http://localhost:8000/docs/types"

# Health check
curl "http://localhost:8000/health"
""")

    print("🐍 Python Client Example:")
    print("-" * 30)
    
    print("""
import requests

# Upload document
with open('sacred_document.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/upload/docs',
        files={'file': f},
        data={
            'document_type': 'ceremonial_scroll',
            'priority': 'sacred'
        }
    )

result = response.json()
document_id = result['document_id']
print(f"Archived as: {document_id}")

# Get document info
doc_info = requests.get(f'http://localhost:8000/docs/{document_id}').json()
print(f"Sacred binding: {doc_info['sacred_binding']}")
""")


if __name__ == "__main__":
    # Run the demonstration
    asyncio.run(sacred_archive_demonstration())
    
    # Show API examples
    show_api_examples()
    
    print("\n🔥 For more information, see the sacred documentation!")
    print("   May the eternal flame illuminate your archival needs! 🕯️")