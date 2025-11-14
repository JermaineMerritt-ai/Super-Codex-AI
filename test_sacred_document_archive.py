#!/usr/bin/env python3
"""
Sacred Document Archive Test Suite
Comprehensive testing for document upload and archival system
"""

import unittest
import asyncio
import tempfile
import shutil
import json
import hashlib
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch
from io import BytesIO

import pytest
from fastapi.testclient import TestClient
from fastapi import UploadFile

# Import the sacred document archive
from sacred_document_archive import (
    SacredDocumentArchive, SacredDocument, DocumentType, 
    DocumentStatus, SacredPriority, app, create_sacred_archive
)


class TestSacredDocumentArchive(unittest.TestCase):
    """Test suite for Sacred Document Archive system"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()
        self.archive = SacredDocumentArchive(storage_root=self.temp_dir)
        
        # Create test files
        self.test_content = b"Sacred ceremonial content for testing the eternal flame archive"
        self.test_filename = "test_ceremonial_scroll.txt"
        
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_archive_initialization(self):
        """Test sacred archive initialization"""
        self.assertTrue(self.archive.storage_root.exists())
        self.assertEqual(len(self.archive.archive_costs), 5)  # 5 priority levels
        
        # Check directory structure
        expected_dirs = [
            "documents", "metadata", "bindings", "sealed_archives"
        ]
        for directory in expected_dirs:
            self.assertTrue((self.archive.storage_root / directory).exists())
    
    def test_document_type_detection(self):
        """Test automatic document type detection"""
        test_cases = [
            ("sacred_scroll.pdf", DocumentType.CEREMONIAL_SCROLL),
            ("binding_contract.doc", DocumentType.SACRED_CONTRACT),
            ("flame_blessing.txt", DocumentType.FLAME_BLESSING),
            ("liturgy_service.pdf", DocumentType.LITURGICAL_TEXT),
            ("treasury_report.xlsx", DocumentType.TREASURY_RECORD),
            ("council_decree.pdf", DocumentType.COUNCIL_DECREE),
            ("wisdom_codex.epub", DocumentType.WISDOM_CODEX),
            ("honor_citation.doc", DocumentType.HONOR_CITATION),
            ("sacred_oath.pdf", DocumentType.BINDING_OATH),
            ("random_file.txt", DocumentType.ARCHIVE_DOCUMENT)
        ]
        
        for filename, expected_type in test_cases:
            detected = self.archive._determine_document_type(filename, "text/plain")
            self.assertEqual(detected, expected_type, 
                           f"Failed to detect {expected_type.value} for {filename}")
    
    def test_priority_determination(self):
        """Test document priority determination"""
        # Test priority by document type
        priority = self.archive._determine_priority(DocumentType.CEREMONIAL_SCROLL, 1024)
        self.assertEqual(priority, SacredPriority.SACRED)
        
        priority = self.archive._determine_priority(DocumentType.SACRED_CONTRACT, 1024)
        self.assertEqual(priority, SacredPriority.DIVINE)
        
        priority = self.archive._determine_priority(DocumentType.ARCHIVE_DOCUMENT, 1024)
        self.assertEqual(priority, SacredPriority.MUNDANE)
        
        # Test large file priority elevation
        large_file_size = 15 * 1024 * 1024  # 15MB
        priority = self.archive._determine_priority(DocumentType.ARCHIVE_DOCUMENT, large_file_size)
        self.assertEqual(priority, SacredPriority.IMPORTANT)
    
    def test_sacred_binding_generation(self):
        """Test sacred binding hash generation"""
        document_data = {
            'filename': 'test.txt',
            'content_hash': 'abcd1234',
            'upload_timestamp': '2025-11-13T12:00:00Z',
            'file_size': 1024
        }
        
        binding1 = self.archive._generate_sacred_binding(document_data)
        binding2 = self.archive._generate_sacred_binding(document_data)
        
        # Same data should produce same binding
        self.assertEqual(binding1, binding2)
        self.assertEqual(len(binding1), 32)  # 32 character hash
        
        # Different data should produce different binding
        document_data['filename'] = 'different.txt'
        binding3 = self.archive._generate_sacred_binding(document_data)
        self.assertNotEqual(binding1, binding3)
    
    def test_ceremonial_seal_generation(self):
        """Test ceremonial seal generation"""
        sacred_doc = SacredDocument(
            document_id="TEST-001",
            filename="test.txt",
            original_name="test.txt",
            file_size=1024,
            content_hash="abcd1234",
            mime_type="text/plain",
            document_type=DocumentType.CEREMONIAL_SCROLL,
            priority=SacredPriority.SACRED,
            status=DocumentStatus.RECEIVED,
            upload_timestamp="2025-11-13T12:00:00Z",
            sacred_binding="test_binding",
            ceremonial_seal="",
            uploader_id="test_user",
            storage_path="test/path",
            metadata={},
            treasury_cost=0.15,
            flame_blessing="test blessing"
        )
        
        seal = self.archive._generate_ceremonial_seal(sacred_doc)
        self.assertEqual(len(seal), 16)  # 16 character seal
        self.assertTrue(seal.isupper())  # Should be uppercase
    
    def test_flame_blessing_generation(self):
        """Test contextual flame blessing generation"""
        blessing = self.archive._generate_flame_blessing(
            DocumentType.CEREMONIAL_SCROLL, SacredPriority.SACRED
        )
        self.assertIn("eternal flame", blessing)
        
        blessing = self.archive._generate_flame_blessing(
            DocumentType.SACRED_CONTRACT, SacredPriority.DIVINE
        )
        self.assertIn("binding flame", blessing)
    
    def test_cost_calculation(self):
        """Test treasury cost calculation"""
        # Test base costs
        cost = self.archive._calculate_archive_cost(SacredPriority.MUNDANE, 1024)
        self.assertAlmostEqual(cost, 0.01, places=4)
        
        cost = self.archive._calculate_archive_cost(SacredPriority.ETERNAL, 1024)
        self.assertAlmostEqual(cost, 1.0, places=4)
        
        # Test size-based cost addition
        large_file = 10 * 1024 * 1024  # 10MB
        cost = self.archive._calculate_archive_cost(SacredPriority.MUNDANE, large_file)
        expected_cost = 0.01 + (10 * 0.001)  # Base + size cost
        self.assertAlmostEqual(cost, expected_cost, places=6)
    
    def test_storage_path_generation(self):
        """Test storage path generation"""
        path = self.archive._get_storage_path(
            DocumentType.CEREMONIAL_SCROLL, "DOC-001", "test.pdf"
        )
        self.assertTrue(path.startswith("documents/ceremonial_scrolls/"))
        self.assertTrue(path.endswith(".pdf"))
        
        path = self.archive._get_storage_path(
            DocumentType.TREASURY_RECORD, "DOC-002", "budget.xlsx"
        )
        self.assertTrue(path.startswith("documents/treasury_records/"))
        self.assertTrue(path.endswith(".xlsx"))
    
    @patch('sacred_document_archive.aiofiles')
    async def test_metadata_file_saving(self, mock_aiofiles):
        """Test metadata file saving"""
        mock_file = AsyncMock()
        mock_aiofiles.open.return_value.__aenter__.return_value = mock_file
        
        sacred_doc = SacredDocument(
            document_id="TEST-001",
            filename="test.txt",
            original_name="test.txt", 
            file_size=1024,
            content_hash="abcd1234",
            mime_type="text/plain",
            document_type=DocumentType.CEREMONIAL_SCROLL,
            priority=SacredPriority.SACRED,
            status=DocumentStatus.RECEIVED,
            upload_timestamp="2025-11-13T12:00:00Z",
            sacred_binding="test_binding",
            ceremonial_seal="TEST_SEAL",
            uploader_id="test_user",
            storage_path="test/path",
            metadata={},
            treasury_cost=0.15,
            flame_blessing="test blessing"
        )
        
        result = await self.archive._save_metadata_file(sacred_doc)
        self.assertTrue(result)
        mock_file.write.assert_called_once()
    
    @patch('sacred_document_archive.aiofiles')
    async def test_binding_record_saving(self, mock_aiofiles):
        """Test sacred binding record saving"""
        mock_file = AsyncMock()
        mock_aiofiles.open.return_value.__aenter__.return_value = mock_file
        
        sacred_doc = SacredDocument(
            document_id="TEST-001",
            filename="test.txt",
            original_name="test.txt",
            file_size=1024,
            content_hash="abcd1234",
            mime_type="text/plain",
            document_type=DocumentType.CEREMONIAL_SCROLL,
            priority=SacredPriority.SACRED,
            status=DocumentStatus.RECEIVED,
            upload_timestamp="2025-11-13T12:00:00Z",
            sacred_binding="test_binding",
            ceremonial_seal="TEST_SEAL",
            uploader_id="test_user",
            storage_path="test/path",
            metadata={},
            treasury_cost=0.15,
            flame_blessing="test blessing"
        )
        
        result = await self.archive._save_binding_record(sacred_doc)
        self.assertTrue(result)
        mock_file.write.assert_called_once()
    
    def test_enum_values(self):
        """Test all enum values are properly defined"""
        # Test DocumentType enum
        self.assertEqual(len(list(DocumentType)), 10)
        self.assertIn(DocumentType.CEREMONIAL_SCROLL, DocumentType)
        self.assertIn(DocumentType.SACRED_CONTRACT, DocumentType)
        
        # Test SacredPriority enum
        self.assertEqual(len(list(SacredPriority)), 5)
        self.assertIn(SacredPriority.MUNDANE, SacredPriority)
        self.assertIn(SacredPriority.ETERNAL, SacredPriority)
        
        # Test DocumentStatus enum
        self.assertEqual(len(list(DocumentStatus)), 7)
        self.assertIn(DocumentStatus.RECEIVED, DocumentStatus)
        self.assertIn(DocumentStatus.ARCHIVED, DocumentStatus)


class TestSacredDocumentAPI(unittest.TestCase):
    """Test suite for FastAPI endpoints"""
    
    def setUp(self):
        """Set up test client"""
        self.client = TestClient(app)
        self.temp_dir = tempfile.mkdtemp()

        # Create a test archive instance
        from sacred_document_archive import create_sacred_archive
        global archive
        archive = create_sacred_archive(storage_root=self.temp_dir)
        archive._ensure_sacred_directories()
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data['status'], 'sacred_flame_burning')
        self.assertEqual(data['archive_system'], 'operational')
    
    def test_document_types_endpoint(self):
        """Test document types endpoint"""
        response = self.client.get("/docs/types")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('document_types', data)
        self.assertIn('priority_levels', data)
        self.assertIn('status_states', data)
        
        # Check all document types are included
        self.assertEqual(len(data['document_types']), 10)
        self.assertIn('ceremonial_scroll', data['document_types'])
    
    @patch('sacred_document_archive.archive.archive_document')
    def test_upload_docs_endpoint(self, mock_archive):
        """Test document upload endpoint"""
        # Mock the archive_document method
        mock_doc = SacredDocument(
            document_id="DOC-TEST-001",
            filename="test.txt",
            original_name="test_document.txt",
            file_size=1024,
            content_hash="abcd1234",
            mime_type="text/plain",
            document_type=DocumentType.CEREMONIAL_SCROLL,
            priority=SacredPriority.SACRED,
            status=DocumentStatus.ARCHIVED,
            upload_timestamp="2025-11-13T12:00:00Z",
            sacred_binding="test_binding",
            ceremonial_seal="TEST_SEAL",
            uploader_id="test_user",
            storage_path="test/path",
            metadata={},
            treasury_cost=0.15,
            flame_blessing="May the eternal flame preserve this knowledge"
        )
        
        mock_archive.return_value = mock_doc
        
        # Create test file
        test_file_content = b"Sacred test document content"
        files = {"file": ("test_document.txt", BytesIO(test_file_content), "text/plain")}
        
        # Test upload without auth (should work with anonymous user)
        response = self.client.post("/upload/docs", files=files)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data['document_id'], "DOC-TEST-001")
        self.assertEqual(data['status'], 'archived')
        self.assertIn('sacred_binding', data)
        self.assertIn('ceremonial_seal', data)
        self.assertIn('flame_blessing', data)
    
    @patch('sacred_document_archive.archive.archive_document')
    def test_upload_with_parameters(self, mock_archive):
        """Test document upload with type and priority parameters"""
        mock_doc = SacredDocument(
            document_id="DOC-TEST-002",
            filename="contract.pdf",
            original_name="sacred_contract.pdf",
            file_size=2048,
            content_hash="efgh5678",
            mime_type="application/pdf",
            document_type=DocumentType.SACRED_CONTRACT,
            priority=SacredPriority.DIVINE,
            status=DocumentStatus.ARCHIVED,
            upload_timestamp="2025-11-13T12:00:00Z",
            sacred_binding="contract_binding",
            ceremonial_seal="CONTRACT_SEAL",
            uploader_id="test_user",
            storage_path="contracts/path",
            metadata={},
            treasury_cost=0.30,
            flame_blessing="May the binding flame witness these oaths"
        )
        
        mock_archive.return_value = mock_doc
        
        # Create test file
        test_file_content = b"Sacred contract content"
        files = {"file": ("sacred_contract.pdf", BytesIO(test_file_content), "application/pdf")}
        data = {
            "document_type": "sacred_contract",
            "priority": "divine"
        }
        
        response = self.client.post("/upload/docs", files=files, data=data)
        self.assertEqual(response.status_code, 200)
        
        result = response.json()
        self.assertEqual(result['document_type'], 'sacred_contract')
        self.assertEqual(result['priority'], 'divine')
    
    def test_upload_invalid_type(self):
        """Test upload with invalid document type"""
        test_file_content = b"Test content"
        files = {"file": ("test.txt", BytesIO(test_file_content), "text/plain")}
        data = {"document_type": "invalid_type"}
        
        response = self.client.post("/upload/docs", files=files, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid document type", response.json()['detail'])
    
    def test_upload_invalid_priority(self):
        """Test upload with invalid priority"""
        test_file_content = b"Test content"
        files = {"file": ("test.txt", BytesIO(test_file_content), "text/plain")}
        data = {"priority": "invalid_priority"}
        
        response = self.client.post("/upload/docs", files=files, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid priority", response.json()['detail'])
    
    @patch('sacred_document_archive.archive.get_document')
    def test_get_document_info(self, mock_get):
        """Test document info retrieval"""
        mock_doc = SacredDocument(
            document_id="DOC-TEST-003",
            filename="info_test.txt",
            original_name="info_test_document.txt",
            file_size=512,
            content_hash="ijkl9012",
            mime_type="text/plain",
            document_type=DocumentType.WISDOM_CODEX,
            priority=SacredPriority.ETERNAL,
            status=DocumentStatus.BLESSED,
            upload_timestamp="2025-11-13T12:00:00Z",
            sacred_binding="wisdom_binding",
            ceremonial_seal="WISDOM_SEAL",
            uploader_id="test_user",
            storage_path="wisdom/path",
            metadata={"category": "ancient_knowledge"},
            treasury_cost=1.00,
            flame_blessing="May the ancient flame kindle wisdom"
        )
        
        mock_get.return_value = mock_doc
        
        response = self.client.get("/docs/DOC-TEST-003")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data['document_id'], "DOC-TEST-003")
        self.assertEqual(data['document_type'], 'wisdom_codex')
        self.assertEqual(data['status'], 'blessed')
    
    @patch('sacred_document_archive.archive.get_document')
    def test_get_document_not_found(self, mock_get):
        """Test document info retrieval for non-existent document"""
        mock_get.return_value = None
        
        response = self.client.get("/docs/NONEXISTENT")
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json()['detail'])
    
    @patch('sacred_document_archive.archive.get_document_statistics')
    def test_archive_statistics(self, mock_stats):
        """Test archive statistics endpoint"""
        mock_stats.return_value = {
            'total_documents': 42,
            'total_size_bytes': 1024000,
            'documents_by_type': {'ceremonial_scroll': 10, 'sacred_contract': 5},
            'documents_by_priority': {'sacred': 15, 'divine': 10},
            'total_treasury_cost': 15.75,
            'archive_health': 'excellent'
        }
        
        response = self.client.get("/docs/stats")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('sacred_archive_statistics', data)
        self.assertEqual(data['eternal_flame_status'], 'burning_bright')
        self.assertEqual(data['sacred_archive_statistics']['total_documents'], 42)


class TestFactoryFunction(unittest.TestCase):
    """Test suite for factory function"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_create_sacred_archive(self):
        """Test factory function"""
        archive = create_sacred_archive(storage_root=self.temp_dir)
        
        self.assertIsInstance(archive, SacredDocumentArchive)
        self.assertEqual(str(archive.storage_root), self.temp_dir)
        self.assertTrue(archive.storage_root.exists())
    
    def test_create_archive_with_postgres(self):
        """Test factory function with PostgreSQL URL"""
        postgres_url = "postgresql://user:pass@localhost/testdb"
        archive = create_sacred_archive(
            storage_root=self.temp_dir,
            postgres_url=postgres_url
        )
        
        self.assertEqual(archive.postgres_url, postgres_url)


async def run_async_tests():
    """Run asynchronous tests"""
    print("🔥 Running Sacred Document Archive Tests...")
    
    # Create test instance
    temp_dir = tempfile.mkdtemp()
    archive = SacredDocumentArchive(storage_root=temp_dir)
    
    try:
        # Test async document archival
        print("   📜 Testing document archival...")
        
        # Create mock UploadFile
        test_content = b"Sacred ceremonial content for async testing"
        
        class MockUploadFile:
            def __init__(self, filename, content, content_type):
                self.filename = filename
                self.content = content
                self.content_type = content_type
            
            async def read(self):
                return self.content
        
        mock_file = MockUploadFile(
            "test_ceremonial_scroll.txt",
            test_content,
            "text/plain"
        )
        
        # Archive the document
        sacred_doc = await archive.archive_document(mock_file, "test_user")
        
        print(f"   ✅ Document archived: {sacred_doc.document_id}")
        print(f"   🔐 Sacred binding: {sacred_doc.sacred_binding}")
        print(f"   🏺 Ceremonial seal: {sacred_doc.ceremonial_seal}")
        print(f"   💰 Treasury cost: {sacred_doc.treasury_cost}")
        
        # Test document retrieval
        print("   📚 Testing document retrieval...")
        retrieved_doc = await archive.get_document(sacred_doc.document_id)
        
        assert retrieved_doc is not None
        assert retrieved_doc.document_id == sacred_doc.document_id
        print(f"   ✅ Document retrieved: {retrieved_doc.original_name}")
        
        # Test statistics
        print("   📊 Testing statistics...")
        stats = await archive.get_document_statistics()
        
        assert stats['total_documents'] >= 1
        assert stats['total_treasury_cost'] > 0
        print(f"   ✅ Statistics: {stats['total_documents']} documents, {stats['total_treasury_cost']} tokens")
        
        print("   🕯️ All async tests passed!")
        
    except Exception as e:
        print(f"   ❌ Async test error: {e}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    print("🔥" + "="*60 + "🔥")
    print("   SACRED DOCUMENT ARCHIVE TEST SUITE")
    print("   Testing ceremonial document storage")
    print("🔥" + "="*60 + "🔥\n")
    
    # Run synchronous unit tests
    print("📋 Running Unit Tests...")
    unittest.main(verbosity=2, exit=False)
    
    # Run asynchronous tests
    print("\n🔄 Running Async Tests...")
    asyncio.run(run_async_tests())
    
    print("\n🕯️ Sacred Document Archive Testing Complete")
    print("   May the eternal flame preserve all sacred knowledge!")