"""
WooCommerce Ceremonial Test Suite
================================

This module provides comprehensive testing for the WooCommerce integration
with the ceremonial treasury system. All tests are designed to validate
the sacred commerce bindings and ensure transactional integrity.
"""

import unittest
import json
import os
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone

# Import the WooCommerce integration module
from woocommerce_integration import (
    WooCommerceIntegrator,
    CommerceOperation,
    SacredProductType,
    CommerceTransaction,
    create_woocommerce_integrator
)

class TestWooCommerceIntegration(unittest.TestCase):
    """Test suite for WooCommerce ceremonial integration"""
    
    def setUp(self):
        """Set up test environment with temporary storage"""
        self.temp_dir = tempfile.mkdtemp()
        self.integrator = create_woocommerce_integrator(
            api_url="https://test-store.com/wp-json/wc/v3",
            api_key="test_key_123",
            api_secret="test_secret_456",
            storage_root=self.temp_dir
        )
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)
    
    def test_woocommerce_integrator_initialization(self):
        """Test WooCommerce integrator initialization"""
        self.assertIsNotNone(self.integrator)
        self.assertEqual(self.integrator.api_url, "https://test-store.com/wp-json/wc/v3")
        self.assertEqual(self.integrator.api_key, "test_key_123")
        self.assertEqual(self.integrator.api_secret, "test_secret_456")
        
        # Check storage directories were created
        self.assertTrue(os.path.exists(f"{self.temp_dir}/codex-flame/storage/woocommerce"))
        self.assertTrue(os.path.exists(f"{self.temp_dir}/codex-flame/storage/woocommerce/transactions"))
        self.assertTrue(os.path.exists(f"{self.temp_dir}/codex-flame/storage/woocommerce/products"))
    
    def test_sacred_binding_generation(self):
        """Test sacred binding hash generation"""
        test_data = {
            'operation': 'test_operation',
            'amount': 100.0,
            'timestamp': '2025-11-13T12:00:00Z'
        }
        
        binding = self.integrator._generate_sacred_binding(test_data)
        
        self.assertIsInstance(binding, str)
        self.assertEqual(len(binding), 16)
        
        # Test consistency
        binding2 = self.integrator._generate_sacred_binding(test_data)
        self.assertEqual(binding, binding2)
    
    def test_ceremonial_seal_generation(self):
        """Test ceremonial seal generation"""
        transaction = CommerceTransaction(
            transaction_id="TEST-001",
            operation_type=CommerceOperation.PRODUCT_FETCH,
            product_type=SacredProductType.FLAME_ESSENCE,
            amount=50.0,
            currency="USD",
            customer_id="test_customer",
            sacred_binding_hash="test_hash",
            ceremonial_seal="",
            transaction_timestamp=datetime.now(timezone.utc).isoformat()
        )
        
        seal = self.integrator._generate_ceremonial_seal(transaction)
        
        self.assertIsInstance(seal, str)
        self.assertTrue(seal.startswith("WC-"))
        self.assertEqual(len(seal), 15)  # "WC-" + 12 characters
    
    @patch('woocommerce_integration.requests.get')
    def test_fetch_products_success(self, mock_get):
        """Test successful product fetching"""
        # Mock API response
        mock_response = Mock()
        mock_response.json.return_value = [
            {'id': 1, 'name': 'Sacred Flame Essence', 'price': '99.99'},
            {'id': 2, 'name': 'Ceremonial Scroll', 'price': '149.99'}
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Test product fetching
        products = self.integrator.fetch_products({'per_page': 10})
        
        self.assertEqual(len(products), 2)
        self.assertEqual(products[0]['name'], 'Sacred Flame Essence')
        
        # Verify API call was made correctly
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        self.assertEqual(call_args[1]['auth'], ('test_key_123', 'test_secret_456'))
        self.assertEqual(call_args[1]['params'], {'per_page': 10})
    
    @patch('woocommerce_integration.requests.get')
    def test_fetch_products_failure(self, mock_get):
        """Test product fetching failure handling"""
        # Mock API failure
        mock_get.side_effect = Exception("API Error")
        
        # Test product fetching with error
        products = self.integrator.fetch_products()
        
        self.assertEqual(products, [])
    
    @patch('woocommerce_integration.requests.post')
    def test_create_order_success(self, mock_post):
        """Test successful order creation"""
        # Mock API response
        mock_response = Mock()
        mock_response.json.return_value = {
            'id': 123,
            'total': '199.98',
            'currency': 'USD',
            'customer_id': 456
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Test order creation
        order_data = {
            'billing': {'email': 'test@example.com'},
            'line_items': [{'product_id': 1, 'quantity': 2}]
        }
        
        order = self.integrator.create_order(order_data)
        
        self.assertIsNotNone(order)
        self.assertEqual(order['id'], 123)
        self.assertEqual(order['total'], '199.98')
        
        # Verify API call was made correctly
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertEqual(call_args[1]['auth'], ('test_key_123', 'test_secret_456'))
        self.assertEqual(call_args[1]['json'], order_data)
    
    @patch('woocommerce_integration.requests.post')
    def test_create_order_failure(self, mock_post):
        """Test order creation failure handling"""
        # Mock API failure
        mock_post.side_effect = Exception("Order creation failed")
        
        # Test order creation with error
        order_data = {'billing': {'email': 'test@example.com'}}
        order = self.integrator.create_order(order_data)
        
        self.assertIsNone(order)
    
    def test_process_webhook(self):
        """Test webhook processing"""
        webhook_data = {
            'action': 'order.updated',
            'arg': {
                'id': 123,
                'total': '99.99',
                'currency': 'USD',
                'customer_id': 456
            }
        }
        
        result = self.integrator.process_webhook(webhook_data)
        
        self.assertTrue(result)
        
        # Check transaction was saved
        transactions = self.integrator.get_transaction_history(1)
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].operation_type, CommerceOperation.ORDER_UPDATE)
    
    def test_transaction_storage_and_retrieval(self):
        """Test transaction storage and retrieval"""
        # Create test transaction
        transaction = CommerceTransaction(
            transaction_id="TEST-STORAGE-001",
            operation_type=CommerceOperation.PRODUCT_FETCH,
            product_type=SacredProductType.CEREMONIAL_SCROLL,
            amount=75.0,
            currency="USD",
            customer_id="test_user",
            sacred_binding_hash="test_hash_123",
            ceremonial_seal="WC-test_seal_456",
            transaction_timestamp=datetime.now(timezone.utc).isoformat(),
            metadata={'test': True}
        )
        
        # Save transaction
        self.integrator._save_transaction(transaction)
        
        # Retrieve and verify
        retrieved_transactions = self.integrator.get_transaction_history(5)
        self.assertEqual(len(retrieved_transactions), 1)
        
        retrieved = retrieved_transactions[0]
        self.assertEqual(retrieved.transaction_id, "TEST-STORAGE-001")
        self.assertEqual(retrieved.operation_type, CommerceOperation.PRODUCT_FETCH)
        self.assertEqual(retrieved.amount, 75.0)
    
    def test_sync_inventory(self):
        """Test inventory synchronization"""
        inventory_data = {
            'product_1': {'quantity': 100, 'reserved': 10},
            'product_2': {'quantity': 50, 'reserved': 5}
        }
        
        result = self.integrator.sync_inventory(inventory_data)
        
        self.assertTrue(result)
        
        # Check transaction was created
        transactions = self.integrator.get_transaction_history(1)
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].operation_type, CommerceOperation.INVENTORY_SYNC)
    
    def test_commerce_operation_enum(self):
        """Test CommerceOperation enum values"""
        self.assertEqual(CommerceOperation.PRODUCT_FETCH.value, "product_fetch")
        self.assertEqual(CommerceOperation.ORDER_CREATE.value, "order_create")
        self.assertEqual(CommerceOperation.ORDER_UPDATE.value, "order_update")
        self.assertEqual(CommerceOperation.INVENTORY_SYNC.value, "inventory_sync")
        self.assertEqual(CommerceOperation.PAYMENT_PROCESS.value, "payment_process")
        self.assertEqual(CommerceOperation.REFUND_PROCESS.value, "refund_process")
    
    def test_sacred_product_type_enum(self):
        """Test SacredProductType enum values"""
        self.assertEqual(SacredProductType.FLAME_ESSENCE.value, "flame_essence")
        self.assertEqual(SacredProductType.CEREMONIAL_SCROLL.value, "ceremonial_scroll")
        self.assertEqual(SacredProductType.TREASURY_TOKEN.value, "treasury_token")
        self.assertEqual(SacredProductType.WISDOM_CAPSULE.value, "wisdom_capsule")
        self.assertEqual(SacredProductType.DOMINION_LICENSE.value, "dominion_license")
        self.assertEqual(SacredProductType.SACRED_SERVICE.value, "sacred_service")
    
    def test_commerce_transaction_dataclass(self):
        """Test CommerceTransaction dataclass functionality"""
        transaction = CommerceTransaction(
            transaction_id="TEST-002",
            operation_type=CommerceOperation.ORDER_CREATE,
            product_type=SacredProductType.WISDOM_CAPSULE,
            amount=125.50,
            currency="EUR",
            customer_id="cust_456",
            sacred_binding_hash="hash_abc123",
            ceremonial_seal="WC-seal_def456",
            transaction_timestamp="2025-11-13T15:30:00Z",
            wc_order_id="789",
            treasury_entry_id="TRE-001",
            metadata={'source': 'test'}
        )
        
        self.assertEqual(transaction.transaction_id, "TEST-002")
        self.assertEqual(transaction.operation_type, CommerceOperation.ORDER_CREATE)
        self.assertEqual(transaction.product_type, SacredProductType.WISDOM_CAPSULE)
        self.assertEqual(transaction.amount, 125.50)
        self.assertEqual(transaction.currency, "EUR")
        self.assertEqual(transaction.customer_id, "cust_456")
        self.assertEqual(transaction.wc_order_id, "789")
        self.assertEqual(transaction.treasury_entry_id, "TRE-001")
        self.assertIsNotNone(transaction.metadata)
    
    def test_factory_function(self):
        """Test the factory function for creating WooCommerce integrator"""
        integrator = create_woocommerce_integrator(
            api_url="https://factory-test.com/wp-json/wc/v3",
            api_key="factory_key",
            api_secret="factory_secret",
            storage_root=self.temp_dir
        )
        
        self.assertIsInstance(integrator, WooCommerceIntegrator)
        self.assertEqual(integrator.api_url, "https://factory-test.com/wp-json/wc/v3")
        self.assertEqual(integrator.api_key, "factory_key")
        self.assertEqual(integrator.api_secret, "factory_secret")

def run_woocommerce_tests():
    """Run all WooCommerce integration tests"""
    print("🔥 WOOCOMMERCE CEREMONIAL TEST SUITE")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWooCommerceIntegration)
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Run tests
    result = runner.run(suite)
    
    # Print results
    print("\n🔥 TEST RESULTS:")
    if result.wasSuccessful():
        print("✅ All WooCommerce integration tests passed!")
        print(f"🌟 {result.testsRun} tests completed successfully")
    else:
        print(f"❌ {len(result.failures)} test(s) failed")
        print(f"❌ {len(result.errors)} test(s) had errors")
        
        if result.failures:
            print("\n🔴 FAILURES:")
            for test, traceback in result.failures:
                print(f"   - {test}: {traceback}")
        
        if result.errors:
            print("\n🔴 ERRORS:")
            for test, traceback in result.errors:
                print(f"   - {test}: {traceback}")
    
    print("\n🕯️ Sacred Commerce Testing Complete")
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_woocommerce_tests()
    exit(0 if success else 1)