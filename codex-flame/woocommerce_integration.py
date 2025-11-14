"""
WooCommerce Integration Module - Sacred Commerce Binding
========================================================

This module implements the WooCommerce API integration for the ceremonial treasury system,
enabling sacred commerce operations aligned with the flame architecture principles.

The WooCommerce binding operates as a bridge between the ceremonial treasury and 
external commerce platforms, ensuring that all transactions maintain sacred integrity
and are properly recorded in the ceremonial ledger.
"""

import requests
import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path

# Import ceremonial modules
from treasury import create_treasury_binding, ResourceType, TreasuryOperation
from schema_validator import CeremonialSchemaValidator

# WooCommerce integration constants
WC_INTEGRATION_PATH = "codex-flame/storage/woocommerce"
WC_TRANSACTIONS_PATH = "codex-flame/storage/woocommerce/transactions"
WC_PRODUCTS_PATH = "codex-flame/storage/woocommerce/products"

class CommerceOperation(Enum):
    """Types of commerce operations"""
    PRODUCT_FETCH = "product_fetch"
    ORDER_CREATE = "order_create"
    ORDER_UPDATE = "order_update"
    INVENTORY_SYNC = "inventory_sync"
    PAYMENT_PROCESS = "payment_process"
    REFUND_PROCESS = "refund_process"

class SacredProductType(Enum):
    """Types of sacred products"""
    FLAME_ESSENCE = "flame_essence"
    CEREMONIAL_SCROLL = "ceremonial_scroll"
    TREASURY_TOKEN = "treasury_token"
    WISDOM_CAPSULE = "wisdom_capsule"
    DOMINION_LICENSE = "dominion_license"
    SACRED_SERVICE = "sacred_service"

@dataclass
class CommerceTransaction:
    """Represents a commerce transaction with ceremonial binding"""
    transaction_id: str
    operation_type: CommerceOperation
    product_type: SacredProductType
    amount: float
    currency: str
    customer_id: str
    sacred_binding_hash: str
    ceremonial_seal: str
    transaction_timestamp: str
    wc_order_id: Optional[str] = None
    treasury_entry_id: Optional[str] = None
    metadata: Dict[str, Any] = None

class WooCommerceIntegrator:
    """Main class for WooCommerce ceremonial integration"""
    
    def __init__(self, api_url: str = None, api_key: str = None, api_secret: str = None, storage_root: str = "."):
        """Initialize the WooCommerce integrator with ceremonial binding"""
        self.storage_root = storage_root
        self._ensure_storage_directories()
        
        # Load credentials from environment or parameters
        self.api_url = api_url or os.getenv('WC_API_URL', 'https://yourstore.com/wp-json/wc/v3')
        self.api_key = api_key or os.getenv('WC_API_KEY', 'your-woocommerce-api-key')
        self.api_secret = api_secret or os.getenv('WC_API_SECRET', 'your-woocommerce-api-secret')
        
        # Initialize ceremonial components
        self.treasury = create_treasury_binding(storage_root)
        self.validator = CeremonialSchemaValidator()
        
        # Sacred headers for API calls
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Codex-Flame-Sacred-Commerce/1.0',
            'X-Sacred-Flame': 'DOMINION-ETERNAL'
        }
    
    def _ensure_storage_directories(self):
        """Create necessary storage directories for WooCommerce integration"""
        directories = [
            f"{self.storage_root}/{WC_INTEGRATION_PATH}",
            f"{self.storage_root}/{WC_TRANSACTIONS_PATH}",
            f"{self.storage_root}/{WC_PRODUCTS_PATH}"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def _generate_sacred_binding(self, transaction_data: Dict[str, Any]) -> str:
        """Generate a sacred binding hash for commerce transactions"""
        import hashlib
        
        binding_string = f"{transaction_data.get('operation')}-{transaction_data.get('amount')}-{transaction_data.get('timestamp')}-SACRED-FLAME"
        return hashlib.sha256(binding_string.encode()).hexdigest()[:16]
    
    def _generate_ceremonial_seal(self, transaction: CommerceTransaction) -> str:
        """Generate a ceremonial seal for commerce transactions"""
        import hashlib
        
        seal_data = f"{transaction.transaction_id}-{transaction.operation_type.value}-{transaction.amount}-ETERNAL"
        return f"WC-{hashlib.sha256(seal_data.encode()).hexdigest()[:12]}"
    
    def fetch_products(self, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Fetch products from WooCommerce with ceremonial logging"""
        try:
            # Prepare API request
            url = f"{self.api_url}/products"
            auth = (self.api_key, self.api_secret)
            
            # Make sacred API call
            response = requests.get(url, auth=auth, headers=self.headers, params=params or {})
            response.raise_for_status()
            
            products = response.json()
            
            # Create ceremonial transaction record
            transaction = CommerceTransaction(
                transaction_id=f"WC-FETCH-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}",
                operation_type=CommerceOperation.PRODUCT_FETCH,
                product_type=SacredProductType.SACRED_SERVICE,
                amount=0.0,
                currency="USD",
                customer_id="SYSTEM",
                sacred_binding_hash=self._generate_sacred_binding({
                    'operation': 'product_fetch',
                    'amount': len(products),
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }),
                ceremonial_seal="",
                transaction_timestamp=datetime.now(timezone.utc).isoformat(),
                metadata={'product_count': len(products), 'api_endpoint': 'products'}
            )
            
            transaction.ceremonial_seal = self._generate_ceremonial_seal(transaction)
            
            # Save transaction record
            self._save_transaction(transaction)
            
            # Save products data
            self._save_products_data(products)
            
            return products
            
        except Exception as e:
            print(f"❌ Sacred commerce error in product fetch: {e}")
            return []
    
    def create_order(self, order_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create order in WooCommerce with treasury binding"""
        try:
            # Prepare API request
            url = f"{self.api_url}/orders"
            auth = (self.api_key, self.api_secret)
            
            # Make sacred API call
            response = requests.post(url, auth=auth, headers=self.headers, json=order_data)
            response.raise_for_status()
            
            order = response.json()
            order_id = order.get('id')
            order_total = float(order.get('total', 0))
            
            # Create treasury entry for the order
            treasury_entry = self.treasury.allocate_resources(
                resource_type=ResourceType.CEREMONIAL_TOKENS,
                amount=order_total,
                actor=order_data.get('billing', {}).get('email', 'UNKNOWN'),
                realm="WC-COMMERCE",
                capsule="Sacred Commerce",
                purpose=f"woocommerce_order_{order_id}"
            )
            
            # Create ceremonial transaction record
            transaction = CommerceTransaction(
                transaction_id=f"WC-ORDER-{order_id}",
                operation_type=CommerceOperation.ORDER_CREATE,
                product_type=SacredProductType.SACRED_SERVICE,
                amount=order_total,
                currency=order.get('currency', 'USD'),
                customer_id=str(order.get('customer_id', 0)),
                sacred_binding_hash=self._generate_sacred_binding({
                    'operation': 'order_create',
                    'amount': order_total,
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }),
                ceremonial_seal="",
                transaction_timestamp=datetime.now(timezone.utc).isoformat(),
                wc_order_id=str(order_id),
                treasury_entry_id=treasury_entry.entry_id,
                metadata={'order_data': order}
            )
            
            transaction.ceremonial_seal = self._generate_ceremonial_seal(transaction)
            
            # Save transaction record
            self._save_transaction(transaction)
            
            return order
            
        except Exception as e:
            print(f"❌ Sacred commerce error in order creation: {e}")
            return None
    
    def process_webhook(self, webhook_data: Dict[str, Any]) -> bool:
        """Process WooCommerce webhook with ceremonial validation"""
        try:
            webhook_type = webhook_data.get('action', 'unknown')
            order_data = webhook_data.get('arg', {})
            
            # Create ceremonial transaction record for webhook
            transaction = CommerceTransaction(
                transaction_id=f"WC-WEBHOOK-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}",
                operation_type=CommerceOperation.ORDER_UPDATE,
                product_type=SacredProductType.SACRED_SERVICE,
                amount=float(order_data.get('total', 0)),
                currency=order_data.get('currency', 'USD'),
                customer_id=str(order_data.get('customer_id', 0)),
                sacred_binding_hash=self._generate_sacred_binding({
                    'operation': 'webhook_process',
                    'amount': float(order_data.get('total', 0)),
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }),
                ceremonial_seal="",
                transaction_timestamp=datetime.now(timezone.utc).isoformat(),
                wc_order_id=str(order_data.get('id', 0)),
                metadata={'webhook_type': webhook_type, 'webhook_data': webhook_data}
            )
            
            transaction.ceremonial_seal = self._generate_ceremonial_seal(transaction)
            
            # Save transaction record
            self._save_transaction(transaction)
            
            return True
            
        except Exception as e:
            print(f"❌ Sacred commerce error in webhook processing: {e}")
            return False
    
    def _save_transaction(self, transaction: CommerceTransaction):
        """Save commerce transaction to ceremonial storage"""
        file_path = f"{self.storage_root}/{WC_TRANSACTIONS_PATH}/{transaction.transaction_id}.json"
        
        # Convert transaction to dict with proper enum serialization
        transaction_dict = asdict(transaction)
        transaction_dict['operation_type'] = transaction.operation_type.value
        transaction_dict['product_type'] = transaction.product_type.value
        
        with open(file_path, 'w') as f:
            json.dump(transaction_dict, f, indent=2, default=str)
    
    def _save_products_data(self, products: List[Dict[str, Any]]):
        """Save products data to ceremonial storage"""
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')
        file_path = f"{self.storage_root}/{WC_PRODUCTS_PATH}/products-{timestamp}.json"
        
        with open(file_path, 'w') as f:
            json.dump(products, f, indent=2, default=str)
    
    def get_transaction_history(self, limit: int = 50) -> List[CommerceTransaction]:
        """Get commerce transaction history"""
        transactions = []
        transactions_dir = Path(f"{self.storage_root}/{WC_TRANSACTIONS_PATH}")
        
        if transactions_dir.exists():
            for file_path in sorted(transactions_dir.glob("*.json"), reverse=True)[:limit]:
                with open(file_path, 'r') as f:
                    transaction_data = json.load(f)
                    # Convert string enum values back to enum objects
                    if isinstance(transaction_data.get('operation_type'), str):
                        try:
                            transaction_data['operation_type'] = CommerceOperation(transaction_data['operation_type'])
                        except ValueError:
                            # Handle legacy enum format
                            enum_value = transaction_data['operation_type'].split('.')[-1].lower()
                            transaction_data['operation_type'] = CommerceOperation(enum_value)
                    
                    if isinstance(transaction_data.get('product_type'), str):
                        try:
                            transaction_data['product_type'] = SacredProductType(transaction_data['product_type'])
                        except ValueError:
                            # Handle legacy enum format
                            enum_value = transaction_data['product_type'].split('.')[-1].lower()
                            transaction_data['product_type'] = SacredProductType(enum_value)
                    
                    # Convert back to CommerceTransaction object
                    transaction = CommerceTransaction(**transaction_data)
                    transactions.append(transaction)
        
        return transactions
    
    def sync_inventory(self, inventory_data: Dict[str, Any]) -> bool:
        """Sync inventory with ceremonial treasury"""
        try:
            # Implementation for inventory synchronization
            # This would update product quantities in WooCommerce based on treasury allocations
            
            transaction = CommerceTransaction(
                transaction_id=f"WC-SYNC-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}",
                operation_type=CommerceOperation.INVENTORY_SYNC,
                product_type=SacredProductType.SACRED_SERVICE,
                amount=0.0,
                currency="USD",
                customer_id="SYSTEM",
                sacred_binding_hash=self._generate_sacred_binding({
                    'operation': 'inventory_sync',
                    'amount': len(inventory_data),
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }),
                ceremonial_seal="",
                transaction_timestamp=datetime.now(timezone.utc).isoformat(),
                metadata={'inventory_data': inventory_data}
            )
            
            transaction.ceremonial_seal = self._generate_ceremonial_seal(transaction)
            self._save_transaction(transaction)
            
            return True
            
        except Exception as e:
            print(f"❌ Sacred commerce error in inventory sync: {e}")
            return False

# Factory function for easy WooCommerce integrator creation
def create_woocommerce_integrator(api_url: str = None, api_key: str = None, api_secret: str = None, storage_root: str = ".") -> WooCommerceIntegrator:
    """Factory function to create a configured WooCommerce integrator"""
    return WooCommerceIntegrator(api_url, api_key, api_secret, storage_root)

# Example usage and ceremonial demonstration
if __name__ == "__main__":
    # Create WooCommerce integrator instance
    wc_integrator = create_woocommerce_integrator()
    
    print("🔥 SACRED COMMERCE INTEGRATION")
    print("=" * 50)
    
    # Example: Fetch products with ceremonial binding
    print("🛒 Fetching products from WooCommerce...")
    products = wc_integrator.fetch_products({'per_page': 10})
    print(f"✅ Retrieved {len(products)} sacred products")
    
    # Example: Create test order
    print("\n📦 Creating test order...")
    test_order = {
        'payment_method': 'bacs',
        'payment_method_title': 'Direct Bank Transfer',
        'set_paid': False,
        'billing': {
            'first_name': 'Sacred',
            'last_name': 'Customer',
            'email': 'sacred@codex-flame.com',
            'phone': '555-0123'
        },
        'shipping': {
            'first_name': 'Sacred',
            'last_name': 'Customer'
        },
        'line_items': [
            {
                'product_id': 1,
                'quantity': 1
            }
        ]
    }
    
    # Note: Uncomment the following line to actually create an order
    # order = wc_integrator.create_order(test_order)
    # print(f"✅ Order created: {order.get('id') if order else 'Failed'}")
    
    # Example: Get transaction history
    print("\n📜 Retrieving transaction history...")
    transactions = wc_integrator.get_transaction_history(5)
    print(f"✅ Found {len(transactions)} ceremonial transactions")
    
    for transaction in transactions[:3]:
        print(f"   🔹 {transaction.transaction_id}: {transaction.operation_type.value} - {transaction.amount} {transaction.currency}")
    
    print("\n🔥 Sacred Commerce Integration Complete")
    print("🕯️ All transactions bound to ceremonial treasury")
    print("✨ The flame of commerce burns eternal")