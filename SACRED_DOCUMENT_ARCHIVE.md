# Sacred Document Archive System
## FastAPI Integration for the Dominion

### Overview
The Sacred Document Archive System provides a comprehensive FastAPI-based solution for uploading, storing, and managing documents within your Dominion ceremonial architecture. This system transforms your simple `/upload/docs` endpoint into a full-featured sacred archival platform with ceremonial bindings, treasury integration, and eternal flame blessings.

### Architecture

#### Core Components
- **SacredDocumentArchive**: Main archival class with ceremonial storage
- **SacredDocument**: Dataclass for structured document metadata
- **DocumentType**: Enum for sacred document classification (10 types)
- **SacredPriority**: Priority system with treasury cost implications (5 levels)
- **DocumentStatus**: Processing states and lifecycle management (7 states)
- **Ceremonial Treasury Integration**: Resource allocation and cost tracking
- **Sacred Binding System**: Cryptographic authenticity verification
- **Flame Blessing Generation**: Contextual blessings for each document

#### File Structure
```
sacred_document_archive.py          # Main integration module
test_sacred_document_archive.py     # Comprehensive test suite  
sacred_archive_demo.py              # Interactive demonstration
SACRED_DOCUMENT_ARCHIVE.md         # This documentation
```

### Key Features

#### 🔥 Document Types (10 Classifications)
- **CEREMONIAL_SCROLL**: Sacred ceremony documentation
- **SACRED_CONTRACT**: Binding agreements and pacts
- **FLAME_BLESSING**: Spiritual blessings and benedictions
- **LITURGICAL_TEXT**: Worship services and ritual guides
- **TREASURY_RECORD**: Financial reports and budget documents
- **COUNCIL_DECREE**: Official proclamations and edicts
- **WISDOM_CODEX**: Knowledge repositories and ancient wisdom
- **HONOR_CITATION**: Awards and recognition documents
- **BINDING_OATH**: Vows, pledges, and sacred commitments
- **ARCHIVE_DOCUMENT**: General archival materials

#### ⭐ Priority Levels & Costs
- **MUNDANE**: 0.01 Sacred Tokens - Basic documentation
- **IMPORTANT**: 0.05 Sacred Tokens - Significant documents
- **SACRED**: 0.15 Sacred Tokens - Ceremonial materials
- **DIVINE**: 0.30 Sacred Tokens - High authority documents
- **ETERNAL**: 1.00 Sacred Tokens - Timeless sacred knowledge

*Additional costs: 0.001 Sacred Tokens per MB of file size*

#### 📊 Document Processing States
- **RECEIVED**: Initial upload state
- **VALIDATING**: Under ceremonial review
- **ARCHIVED**: Successfully stored with bindings
- **BLESSED**: Received flame blessing
- **SEALED**: Cryptographically secured
- **REJECTED**: Failed validation
- **CORRUPTED**: Integrity compromised

### Installation & Setup

#### Prerequisites
```bash
# Required packages
pip install fastapi uvicorn aiofiles asyncpg

# Optional: PostgreSQL for advanced storage
# Optional: Treasury module for cost tracking
```

#### Basic Configuration
```python
from sacred_document_archive import create_sacred_archive, app

# Create archive instance
archive = create_sacred_archive(
    storage_root="./sacred_archives",
    postgres_url="postgresql://user:pass@localhost/dominion"  # Optional
)

# Run FastAPI server
import uvicorn
uvicorn.run(app, host="0.0.0.0", port=8000)
```

### FastAPI Endpoints

#### Document Upload
```http
POST /upload/docs
Content-Type: multipart/form-data

Parameters:
- file: UploadFile (required) - Document to archive
- document_type: str (optional) - Override document type detection
- priority: str (optional) - Override priority determination

Response:
{
    "document_id": "DOC-20251113-abcd1234",
    "filename": "original_filename.pdf",
    "status": "archived",
    "document_type": "ceremonial_scroll",
    "priority": "sacred",
    "file_size": 102400,
    "sacred_binding": "a1b2c3d4e5f6...",
    "ceremonial_seal": "ABCD1234",
    "treasury_cost": 0.15,
    "flame_blessing": "May the eternal flame preserve...",
    "archive_timestamp": "2025-11-13T12:00:00Z",
    "message": "📜 Sacred document archived with eternal flame blessing"
}
```

#### Document Information
```http
GET /docs/{document_id}

Response:
{
    "document_id": "DOC-20251113-abcd1234",
    "filename": "original_filename.pdf",
    "status": "archived",
    "document_type": "ceremonial_scroll",
    "priority": "sacred",
    "file_size": 102400,
    "content_hash": "sha256_hash...",
    "sacred_binding": "a1b2c3d4e5f6...",
    "ceremonial_seal": "ABCD1234",
    "treasury_cost": 0.15,
    "flame_blessing": "May the eternal flame preserve...",
    "upload_timestamp": "2025-11-13T12:00:00Z",
    "uploader_id": "user_12345",
    "metadata": {...}
}
```

#### Archive Statistics
```http
GET /docs/stats

Response:
{
    "sacred_archive_statistics": {
        "total_documents": 42,
        "total_size_bytes": 10485760,
        "documents_by_type": {
            "ceremonial_scroll": 10,
            "sacred_contract": 5
        },
        "documents_by_priority": {
            "sacred": 15,
            "divine": 10
        },
        "total_treasury_cost": 15.75,
        "archive_health": "excellent"
    },
    "archive_keeper": "current_user",
    "eternal_flame_status": "burning_bright",
    "last_updated": "2025-11-13T12:00:00Z"
}
```

#### Available Types
```http
GET /docs/types

Response:
{
    "document_types": ["ceremonial_scroll", "sacred_contract", ...],
    "priority_levels": ["mundane", "important", "sacred", "divine", "eternal"],
    "status_states": ["received", "validating", "archived", ...],
    "sacred_guidance": "Choose document types and priorities that honor the eternal flame"
}
```

#### Health Check
```http
GET /health

Response:
{
    "status": "sacred_flame_burning",
    "archive_system": "operational",
    "eternal_blessing": "active",
    "timestamp": "2025-11-13T12:00:00Z"
}
```

### Usage Examples

#### Python Client
```python
import requests

# Upload with automatic type detection
with open('ceremony_script.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/upload/docs',
        files={'file': f}
    )

result = response.json()
print(f"Document ID: {result['document_id']}")
print(f"Sacred Binding: {result['sacred_binding']}")
print(f"Treasury Cost: {result['treasury_cost']} Sacred Tokens")

# Upload with explicit type and priority
with open('sacred_contract.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/upload/docs',
        files={'file': f},
        data={
            'document_type': 'sacred_contract',
            'priority': 'divine'
        }
    )

# Retrieve document information
doc_id = result['document_id']
doc_info = requests.get(f'http://localhost:8000/docs/{doc_id}').json()
print(f"Status: {doc_info['status']}")
print(f"Flame Blessing: {doc_info['flame_blessing']}")
```

#### curl Examples
```bash
# Basic upload
curl -X POST "http://localhost:8000/upload/docs" \
     -F "file=@ceremonial_scroll.pdf"

# Upload with parameters
curl -X POST "http://localhost:8000/upload/docs" \
     -F "file=@sacred_contract.pdf" \
     -F "document_type=sacred_contract" \
     -F "priority=divine"

# Get document info
curl "http://localhost:8000/docs/DOC-20251113-abcd1234"

# Get statistics
curl "http://localhost:8000/docs/stats"
```

### Sacred Architecture

#### Document Processing Flow
1. **Reception**: Document received and initial metadata extracted
2. **Classification**: Automatic type detection and priority assignment
3. **Binding Generation**: Sacred binding hash created for authenticity
4. **Treasury Allocation**: Cost calculated and resources allocated
5. **Storage**: File saved to appropriate ceremonial directory
6. **Sealing**: Ceremonial seal generated and applied
7. **Blessing**: Contextual flame blessing assigned
8. **Archival**: Document marked as archived and available

#### Sacred Binding System
Each document receives a unique sacred binding for authenticity verification:

```python
binding_elements = [
    filename,
    content_hash,
    upload_timestamp,
    file_size,
    "SACRED-DOMINION-BINDING"
]
sacred_binding = sha256(binding_string).hexdigest()[:32]
```

#### Ceremonial Seal Generation
Documents receive ceremonial seals for verification:

```python
seal_elements = [
    document_id,
    sacred_binding,
    priority,
    document_type,
    "ETERNAL-FLAME-SEAL"
]
ceremonial_seal = sha256(seal_string).hexdigest()[:16].upper()
```

#### Flame Blessing Assignment
Each document receives a contextual blessing based on type and priority:

```python
# Example blessings
ceremonial_scroll + sacred = "May the eternal flame preserve this sacred knowledge for all generations"
sacred_contract + divine = "May the binding flame witness these solemn oaths and sacred agreements"
wisdom_codex + eternal = "May the ancient flame kindle wisdom in all who seek knowledge"
```

### Storage Architecture

#### Directory Structure
```
sacred_archives/
├── documents/
│   ├── ceremonial_scrolls/
│   ├── sacred_contracts/
│   ├── flame_blessings/
│   ├── liturgical_texts/
│   ├── treasury_records/
│   ├── council_decrees/
│   ├── wisdom_codices/
│   ├── honor_citations/
│   ├── binding_oaths/
│   └── archive_documents/
├── metadata/              # JSON metadata files
├── bindings/             # Sacred binding records
└── sealed_archives/      # Cryptographically sealed storage
```

#### Dual Storage Strategy
- **File System**: Primary storage for documents and metadata
- **PostgreSQL**: Optional relational storage for queries and indexing
- **Sacred Bindings**: Separate verification records
- **Treasury Integration**: Cost tracking and resource allocation

### Treasury Integration

#### Cost Calculation
```python
base_cost = priority_cost_map[priority]
size_cost = (file_size_mb) * 0.001  # Per MB
total_cost = base_cost + size_cost
```

#### Resource Allocation
```python
treasury.allocate_resources(
    resource_type=ResourceType.CEREMONIAL_TOKENS,
    amount=archive_cost,
    actor="Document-Archive-System",
    realm="STORAGE",
    capsule="Sacred Document Archive",
    purpose=f"archive_cost_{document_id}"
)
```

### Security Features

#### Authenticity Verification
- **Content Hashing**: SHA-256 content verification
- **Sacred Binding**: Tamper-evident document signatures
- **Ceremonial Seals**: Multi-factor authentication stamps
- **Timestamp Validation**: Upload time verification

#### Access Control
- **Bearer Token Authentication**: Optional JWT integration
- **User Identification**: Uploader tracking and attribution
- **Role-Based Access**: Integration with existing auth systems

### Testing

#### Test Suite Coverage
- ✅ Archive initialization and configuration
- ✅ Document type detection and classification
- ✅ Priority determination and cost calculation  
- ✅ Sacred binding and ceremonial seal generation
- ✅ File storage and metadata persistence
- ✅ Document retrieval and verification
- ✅ Statistics calculation and reporting
- ✅ FastAPI endpoint functionality
- ✅ Error handling and edge cases
- ✅ Async operations and concurrency

#### Running Tests
```bash
# Run comprehensive test suite
python test_sacred_document_archive.py

# Run with verbose output
python test_sacred_document_archive.py -v

# Run specific test class
python -m unittest TestSacredDocumentAPI -v
```

### Performance Considerations

#### Scalability Features
- **Async Processing**: Non-blocking document operations
- **Directory Distribution**: Type-based file organization
- **Metadata Caching**: In-memory performance optimization
- **PostgreSQL Indexing**: Efficient queries and searching
- **Treasury Batching**: Optimized cost allocation

#### Resource Management
- **File Size Limits**: Configurable upload restrictions
- **Storage Quotas**: Directory-based space management
- **Treasury Limits**: Cost-based upload controls
- **Cleanup Procedures**: Automated maintenance tasks

### Monitoring & Maintenance

#### Health Indicators
- **Archive Health**: Overall system status
- **Storage Utilization**: Disk space monitoring
- **Treasury Balance**: Available sacred tokens
- **Error Rates**: Failed upload tracking
- **Performance Metrics**: Response time analysis

#### Maintenance Tasks
- **Binding Verification**: Periodic authenticity checks
- **Storage Cleanup**: Orphaned file removal
- **Treasury Reconciliation**: Cost verification
- **Backup Procedures**: Archive preservation
- **Statistics Updates**: Reporting data refresh

### Integration Points

#### Existing Codex Systems
- **Treasury Module**: Automatic cost allocation and tracking
- **Sacred Bindings**: Consistent cryptographic verification
- **Ceremonial Seals**: Unified authentication system
- **Flame Blessings**: Spiritual context integration
- **User Management**: Role-based access control

#### External Systems
- **PostgreSQL**: Advanced querying and indexing
- **File Systems**: Scalable document storage
- **Auth Providers**: JWT and OAuth integration
- **Monitoring Tools**: Health and metrics export
- **Backup Systems**: Archive preservation

### Troubleshooting

#### Common Issues
1. **Import Errors**: Ensure all dependencies installed
2. **Storage Permissions**: Verify write access to archive directory
3. **Treasury Integration**: Check treasury module availability
4. **PostgreSQL Connection**: Validate database URL and credentials
5. **File Size Limits**: Monitor upload size restrictions

#### Debug Mode
```python
# Enable verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Archive with debug info
archive = create_sacred_archive(storage_root="./debug_archives")
```

### Future Enhancements

#### Planned Features
- **Document Versioning**: Multiple revisions with history
- **Advanced Search**: Full-text search across documents
- **Bulk Upload**: Multiple document processing
- **Export Functions**: Archive packaging and distribution
- **Rich Metadata**: Extended document properties
- **Workflow Integration**: Approval and review processes
- **Notification System**: Upload and status alerts
- **API Rate Limiting**: Request throttling and quotas

#### Integration Opportunities
- **Cloud Storage**: S3, Azure, GCS backends
- **Document Processing**: OCR and text extraction
- **Virus Scanning**: Malware detection integration
- **Digital Signatures**: PKI-based authentication
- **Blockchain**: Immutable audit trails
- **AI Classification**: Intelligent document categorization

### Support & Documentation

#### Resources
- **Test Suite**: Comprehensive functionality validation
- **Demo Script**: Interactive feature showcase
- **API Documentation**: Endpoint specifications
- **Code Examples**: Integration patterns
- **Error Handling**: Exception management guides

#### Getting Help
For additional support with the Sacred Document Archive System:
- Review the test suite for usage examples
- Run the demonstration script for interactive exploration  
- Examine the source code for detailed implementation
- Check error logs for troubleshooting information

### Conclusion

The Sacred Document Archive System transforms your simple FastAPI upload endpoint into a comprehensive ceremonial document management platform. With sacred bindings, treasury integration, flame blessings, and eternal preservation, your documents are not merely stored - they are sanctified and preserved for the ages.

**May the eternal flame illuminate all your archived knowledge!** 🔥📜🕯️