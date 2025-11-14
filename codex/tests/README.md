# Super-Codex-AI Testing Framework

Comprehensive test suite for the Super-Codex-AI system, covering all major components including RAG functionality, scroll generation, real-time operations, and system integration.

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── pytest.ini              # Pytest configuration
├── run_tests.py            # Test runner script
├── test_rag.py              # RAG system tests
├── test_scrolls.py          # Scroll system tests
├── test_integration.py      # Integration tests
└── README.md               # This file
```

## Running Tests

### Quick Start

```powershell
# Run all tests
python tests/run_tests.py

# Run specific test suites
python tests/run_tests.py --unit
python tests/run_tests.py --integration
python tests/run_tests.py --performance

# Run with coverage
python tests/run_tests.py --coverage --html-coverage
```

### Direct Pytest Usage

```powershell
# From the codex/ directory
pytest tests/ -v

# Run specific test file
pytest tests/test_rag.py -v

# Run specific test
pytest tests/test_rag.py::TestMockEmbeddingModel::test_embed_single_text -v

# Run with markers
pytest tests/ -m "integration" -v
pytest tests/ -m "not slow" -v
```

## Test Categories

### Unit Tests

Test individual components in isolation:

- **RAG Components** (`test_rag.py`)
  - MockEmbeddingModel functionality
  - VectorStore operations
  - TextSplitter behavior
  - CodexRAG system
  - Document processors

- **Scroll Components** (`test_scrolls.py`)
  - CeremonialContext management
  - CapsuleDefinition and registry
  - PromptTemplate system
  - ScrollGenerator functionality
  - Real-time event handling

### Integration Tests

Test complete workflows and component interactions:

- **Document Ingestion Workflow** 
  - End-to-end document processing
  - Multi-format document support
  - Batch ingestion operations

- **Scroll Generation Workflow**
  - Complete scroll creation process
  - Template rendering with context
  - Ceremonial protocol integration

- **Real-time Workflow**
  - WebSocket session management
  - Live progress updates
  - Event broadcasting

- **Full Engine Workflow**
  - Complete system integration
  - API endpoint testing
  - Error handling scenarios

### Performance Tests

Test system performance under various conditions:

- **Batch Ingestion Performance**
  - Multiple document processing
  - Processing time measurements
  - Memory usage optimization

- **Concurrent Query Performance**
  - Multiple simultaneous queries
  - Response time consistency
  - System resource utilization

### Resilience Tests

Test system behavior under adverse conditions:

- **Graceful Degradation**
  - Empty corpus handling
  - Invalid input processing
  - Network failure scenarios

- **Cleanup and Recovery**
  - System restart capability
  - Data persistence validation
  - Resource cleanup verification

## Test Markers

Tests are marked for easy filtering:

- `unit`: Unit tests (default)
- `integration`: Integration tests
- `performance`: Performance tests
- `slow`: Tests that take longer to run
- `rag`: RAG-specific tests
- `scrolls`: Scroll-specific tests
- `realtime`: Real-time functionality tests
- `audit`: Audit and logging tests

### Using Markers

```powershell
# Run only fast tests
pytest tests/ -m "not slow" -v

# Run RAG and scroll tests
pytest tests/ -m "rag or scrolls" -v

# Run everything except performance tests
pytest tests/ -m "not performance" -v
```

## Test Configuration

### Environment Setup

Tests use temporary directories and mock configurations to avoid affecting the main system:

```python
# Automatic temporary workspace creation
temp_workspace = temp_directory fixture

# Mock configuration with test paths
mock_config = mock_config fixture

# Sample test data
sample_documents = sample_documents fixture
```

### Fixtures Available

#### Core Fixtures
- `temp_directory`: Temporary directory for test files
- `mock_config`: Test configuration with temp paths
- `sample_documents`: Pre-created test documents
- `ceremonial_context`: Sample ceremonial context
- `user_context`: Sample user context

#### System Fixtures
- `mock_rag_system`: Configured mock RAG system
- `mock_capsule_registry`: Mock capsule registry
- `mock_prompt_manager`: Mock prompt manager
- `mock_embedding_model`: Mock embedding model

#### Data Fixtures
- `sample_embeddings`: Pre-generated test embeddings
- `sample_query_data`: Common test queries
- `sample_rag_responses`: Expected response formats
- `sample_scroll_template`: Test Jinja template

## Writing New Tests

### Test File Structure

```python
"""
Test module description
"""

import pytest
import asyncio
from pathlib import Path
from unittest.mock import Mock, AsyncMock

# Import system under test
from engine.component import ComponentToTest

class TestComponentToTest:
    """Test class for ComponentToTest"""
    
    def test_basic_functionality(self):
        """Test basic component functionality"""
        component = ComponentToTest()
        result = component.basic_method()
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_async_functionality(self):
        """Test async component functionality"""
        component = ComponentToTest()
        result = await component.async_method()
        assert result["success"] is True
```

### Best Practices

1. **Use Descriptive Names**
   ```python
   def test_rag_query_with_valid_input_returns_sources()
   def test_scroll_generation_with_insufficient_access_fails()
   ```

2. **Test Both Success and Failure Cases**
   ```python
   def test_successful_operation(self):
       # Test normal operation
   
   def test_operation_with_invalid_input(self):
       # Test error handling
   ```

3. **Use Fixtures for Setup**
   ```python
   def test_with_setup(self, mock_config, sample_documents):
       # Use provided fixtures instead of manual setup
   ```

4. **Mark Tests Appropriately**
   ```python
   @pytest.mark.integration
   @pytest.mark.slow
   async def test_full_system_workflow(self):
       # Long-running integration test
   ```

5. **Clean Assertions**
   ```python
   # Good
   assert result["success"] is True
   assert len(result["sources"]) > 0
   assert "expected_content" in result["content"]
   
   # Avoid
   assert result  # Too generic
   ```

## Coverage Reports

Generate coverage reports to track test completeness:

```powershell
# Generate terminal coverage report
python tests/run_tests.py --coverage

# Generate HTML coverage report
python tests/run_tests.py --html-coverage

# View HTML report (generated in htmlcov/)
Start-Process htmlcov/index.html
```

## Continuous Integration

For CI/CD pipelines:

```powershell
# Fast test suite for quick feedback
python tests/run_tests.py --fast --quiet

# Full test suite with coverage
python tests/run_tests.py --coverage --failfast

# Performance benchmarking
python tests/run_tests.py --performance --verbose
```

## Debugging Tests

### Verbose Output
```powershell
python tests/run_tests.py --verbose
```

### Debug on Failure
```powershell
python tests/run_tests.py --pdb
```

### Run Specific Failing Test
```powershell
python tests/run_tests.py --file test_rag.py --function test_specific_function
```

### Check Test Dependencies
```powershell
# Verify required packages
pip install pytest pytest-asyncio pytest-mock

# Optional for enhanced features
pip install pytest-cov pytest-xdist pytest-timeout
```

## Contributing

When adding new features:

1. **Add corresponding tests** for new functionality
2. **Update existing tests** if behavior changes
3. **Add new fixtures** for reusable test components
4. **Document test scenarios** in docstrings
5. **Run full test suite** before committing

```powershell
# Pre-commit test check
python tests/run_tests.py --fast
python tests/run_tests.py --integration
```

The testing framework ensures the Super-Codex-AI system maintains high quality, reliability, and performance across all components and workflows.