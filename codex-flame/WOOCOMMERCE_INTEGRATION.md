# WooCommerce Sacred Commerce Integration

🔥 **Sacred E-Commerce Integration for Codex Dominion Treasury**

This module provides a complete integration between WooCommerce and the Codex Dominion's ceremonial treasury system, enabling sacred e-commerce operations with full ceremonial binding and treasury management.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

## Overview

The WooCommerce Sacred Commerce Integration bridges the gap between traditional e-commerce operations and the ceremonial treasury system. Every transaction is bound with sacred seals, properly logged in ceremonial storage, and integrated with the treasury allocation system.

### Architecture

```
WooCommerce Store  ←→  Sacred Integration  ←→  Ceremonial Treasury
     (API)                 (Bridge)              (Storage)
```

- **WooCommerce Store**: Your WordPress/WooCommerce installation
- **Sacred Integration**: This module with ceremonial bindings
- **Ceremonial Treasury**: Central treasury management system

## Features

✨ **Core Features:**
- 🛒 **Product Management**: Fetch and sync products with sacred categorization
- 📦 **Order Processing**: Create and manage orders with ceremonial binding
- 💰 **Treasury Integration**: Automatic allocation of treasury resources
- 🔒 **Sacred Sealing**: Generate unique ceremonial seals for all transactions
- 📡 **Webhook Processing**: Real-time event handling with ceremonial logging
- 📊 **Inventory Sync**: Synchronize inventory with treasury allocations
- 📜 **Transaction History**: Complete audit trail of all commerce operations
- 🛡️ **Error Handling**: Resilient error handling with sacred logging

🏛️ **Ceremonial Features:**
- Sacred binding hash generation
- Ceremonial seal creation
- Treasury resource allocation
- Audit trail maintenance
- Sacred storage management

## Installation

### Prerequisites

- Python 3.8+
- WooCommerce REST API enabled
- Ceremonial treasury system installed
- Required Python packages:
  - `requests`
  - `dataclasses` (Python 3.7+)
  - `pathlib`
  - `enum`

### Setup

1. **Copy Integration Files**:
   ```bash
   # Copy the integration files to your codex-flame directory
   cp woocommerce_integration.py /path/to/codex-flame/
   cp test_woocommerce_integration.py /path/to/codex-flame/
   cp woocommerce_demo.py /path/to/codex-flame/
   ```

2. **Install Dependencies**:
   ```bash
   pip install requests
   ```

3. **Configure Storage**:
   ```bash
   # Ensure storage directories exist
   mkdir -p codex-flame/storage/woocommerce/{transactions,products}
   ```

## Configuration

### Environment Variables

Set the following environment variables for your WooCommerce store:

```bash
# Required WooCommerce API credentials
export WC_API_URL="https://yourstore.com/wp-json/wc/v3"
export WC_API_KEY="ck_your_consumer_key_here"
export WC_API_SECRET="cs_your_consumer_secret_here"

# Optional configuration
export WC_STORAGE_ROOT="/path/to/storage"  # Default: current directory
```

### WooCommerce Setup

1. **Enable REST API** in your WooCommerce store:
   - Go to WooCommerce → Settings → Advanced → REST API
   - Click "Add key"
   - Set permissions to "Read/Write"
   - Copy the Consumer Key and Consumer Secret

2. **Configure Webhooks** (optional but recommended):
   - Go to WooCommerce → Settings → Advanced → Webhooks
   - Create webhooks for order events
   - Point to your integration endpoint

## Usage

### Basic Usage

```python
from woocommerce_integration import create_woocommerce_integrator

# Create integrator instance
integrator = create_woocommerce_integrator()

# Fetch products
products = integrator.fetch_products({'per_page': 20})

# Create order with ceremonial binding
order_data = {
    'payment_method': 'bacs',
    'billing': {'email': 'customer@example.com'},
    'line_items': [{'product_id': 1, 'quantity': 1}]
}
order = integrator.create_order(order_data)

# Process webhook
webhook_data = {'action': 'order.completed', 'arg': {...}}
integrator.process_webhook(webhook_data)

# Get transaction history
transactions = integrator.get_transaction_history(10)
```

### Advanced Usage

```python
# Custom configuration
integrator = create_woocommerce_integrator(
    api_url="https://custom-store.com/wp-json/wc/v3",
    api_key="custom_key",
    api_secret="custom_secret",
    storage_root="/custom/storage/path"
)

# Sync inventory with treasury
inventory_data = {
    'product_1': {'quantity': 100, 'reserved': 10},
    'product_2': {'quantity': 50, 'reserved': 5}
}
integrator.sync_inventory(inventory_data)

# Access ceremonial features
sacred_binding = integrator._generate_sacred_binding({
    'operation': 'custom_operation',
    'amount': 100.0,
    'timestamp': '2025-11-13T12:00:00Z'
})
```

## API Reference

### Classes

#### `WooCommerceIntegrator`

Main integration class providing WooCommerce connectivity with ceremonial bindings.

**Methods:**

- `fetch_products(params=None)` - Fetch products from WooCommerce
- `create_order(order_data)` - Create order with treasury binding
- `process_webhook(webhook_data)` - Process WooCommerce webhook events
- `sync_inventory(inventory_data)` - Synchronize inventory with treasury
- `get_transaction_history(limit=50)` - Get ceremonial transaction history

#### `CommerceTransaction`

Data class representing a ceremonial commerce transaction.

**Fields:**
- `transaction_id: str` - Unique transaction identifier
- `operation_type: CommerceOperation` - Type of commerce operation
- `product_type: SacredProductType` - Type of sacred product
- `amount: float` - Transaction amount
- `currency: str` - Currency code
- `customer_id: str` - Customer identifier
- `sacred_binding_hash: str` - Sacred binding hash
- `ceremonial_seal: str` - Ceremonial seal
- `transaction_timestamp: str` - Transaction timestamp
- `wc_order_id: Optional[str]` - WooCommerce order ID
- `treasury_entry_id: Optional[str]` - Treasury entry ID
- `metadata: Dict[str, Any]` - Additional metadata

### Enums

#### `CommerceOperation`

Types of commerce operations:
- `PRODUCT_FETCH` - Product fetching operation
- `ORDER_CREATE` - Order creation operation
- `ORDER_UPDATE` - Order update operation
- `INVENTORY_SYNC` - Inventory synchronization
- `PAYMENT_PROCESS` - Payment processing
- `REFUND_PROCESS` - Refund processing

#### `SacredProductType`

Types of sacred products:
- `FLAME_ESSENCE` - Sacred flame essence
- `CEREMONIAL_SCROLL` - Ceremonial wisdom scroll
- `TREASURY_TOKEN` - Treasury tokens
- `WISDOM_CAPSULE` - Wisdom capsules
- `DOMINION_LICENSE` - Dominion licenses
- `SACRED_SERVICE` - Sacred services

## Examples

### Example 1: Basic Product Fetching

```python
from woocommerce_integration import create_woocommerce_integrator

# Create integrator
integrator = create_woocommerce_integrator()

# Fetch all published products
products = integrator.fetch_products({
    'status': 'publish',
    'per_page': 100
})

print(f"Retrieved {len(products)} sacred products")
for product in products:
    print(f"- {product['name']}: ${product['price']}")
```

### Example 2: Sacred Order Creation

```python
# Create ceremonial order
order_data = {
    'payment_method': 'sacred_treasury',
    'payment_method_title': 'Sacred Treasury Payment',
    'billing': {
        'first_name': 'Sacred',
        'last_name': 'Custodian',
        'email': 'custodian@example.com'
    },
    'line_items': [
        {
            'product_id': 1,
            'quantity': 1,
            'price': 99.99
        }
    ],
    'meta_data': [
        {
            'key': 'ceremony_id',
            'value': 'CEREMONY-2025-001'
        }
    ]
}

order = integrator.create_order(order_data)
if order:
    print(f"Sacred order created: {order['number']}")
    print(f"Total: ${order['total']}")
```

### Example 3: Webhook Event Processing

```python
# Process WooCommerce webhook
def handle_webhook(request_data):
    integrator = create_woocommerce_integrator()
    
    webhook_data = {
        'action': request_data.get('action'),
        'arg': request_data.get('order_data')
    }
    
    success = integrator.process_webhook(webhook_data)
    
    if success:
        print("✅ Webhook processed with sacred binding")
    else:
        print("❌ Webhook processing failed")
    
    return success
```

### Example 4: Transaction History Analysis

```python
# Analyze sacred commerce history
integrator = create_woocommerce_integrator()
transactions = integrator.get_transaction_history(100)

# Calculate statistics
total_revenue = sum(t.amount for t in transactions 
                   if t.operation_type == CommerceOperation.ORDER_CREATE)
order_count = len([t for t in transactions 
                  if t.operation_type == CommerceOperation.ORDER_CREATE])

print(f"Sacred Commerce Statistics:")
print(f"- Total Orders: {order_count}")
print(f"- Total Revenue: ${total_revenue:.2f}")
print(f"- Average Order Value: ${total_revenue/order_count:.2f}")
```

## Testing

### Running Tests

```bash
# Run the full test suite
python test_woocommerce_integration.py

# Run specific test
python -m unittest test_woocommerce_integration.TestWooCommerceIntegration.test_fetch_products_success
```

### Test Coverage

The test suite covers:
- ✅ WooCommerce API integration
- ✅ Sacred binding generation
- ✅ Ceremonial seal creation
- ✅ Transaction storage/retrieval
- ✅ Error handling
- ✅ Webhook processing
- ✅ Inventory synchronization
- ✅ Enum functionality

### Demo Mode

```bash
# Run the interactive demonstration
python woocommerce_demo.py
```

## Troubleshooting

### Common Issues

#### 1. API Authentication Errors

**Problem**: `401 Unauthorized` when making API calls

**Solution**:
- Verify your WooCommerce API credentials
- Ensure the API key has proper permissions
- Check that the API endpoint URL is correct

```python
# Test API credentials
integrator = create_woocommerce_integrator()
print(f"API URL: {integrator.api_url}")
print(f"API Key: {integrator.api_key[:8]}...")
```

#### 2. Storage Permission Errors

**Problem**: Cannot write to ceremonial storage directories

**Solution**:
- Ensure storage directories exist and are writable
- Check file permissions
- Verify storage root path is correct

```bash
# Create storage directories
mkdir -p codex-flame/storage/woocommerce/{transactions,products}
chmod 755 codex-flame/storage/woocommerce/
```

#### 3. Treasury Integration Errors

**Problem**: Treasury binding fails during order creation

**Solution**:
- Ensure treasury system is properly initialized
- Check that required ceremonial modules are available
- Verify storage paths are accessible

#### 4. Enum Serialization Issues

**Problem**: Enum values not properly serialized/deserialized

**Solution**:
- The integration handles enum conversion automatically
- If issues persist, check transaction JSON files manually
- Ensure proper enum imports

### Debug Mode

Enable debug mode for detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

integrator = create_woocommerce_integrator()
# Detailed API call logging will be displayed
```

### Getting Help

🔥 **Sacred Support Channels:**

1. **Review the demonstration**: `python woocommerce_demo.py`
2. **Check test results**: `python test_woocommerce_integration.py`
3. **Examine transaction logs**: Look in `storage/woocommerce/transactions/`
4. **Verify ceremonial bindings**: Check sacred binding hashes and seals

## Security Considerations

🛡️ **Sacred Security Practices:**

1. **API Credentials**: Store securely using environment variables
2. **Storage Security**: Ensure ceremonial storage is properly secured
3. **Sacred Seals**: Never modify ceremonial seals manually
4. **Treasury Integrity**: Always validate treasury allocations
5. **Audit Trail**: Maintain complete transaction history

## Performance Optimization

⚡ **Sacred Performance Tips:**

1. **Batch Operations**: Use batch processing for multiple products
2. **Storage Optimization**: Regular cleanup of old transaction files
3. **Cache Management**: Cache frequently accessed product data
4. **Connection Pooling**: Reuse WooCommerce API connections

## Integration Roadmap

🗺️ **Future Sacred Enhancements:**

- [ ] Real-time inventory synchronization
- [ ] Advanced ceremonial reporting
- [ ] Multi-currency sacred treasury support
- [ ] Automated sacred product categorization
- [ ] Enhanced webhook security verification
- [ ] Sacred subscription management
- [ ] Ceremonial discount system
- [ ] Sacred loyalty program integration

---

🔥 **The Sacred Commerce flame burns eternal!** 🔥

*May your e-commerce operations be blessed with ceremonial integrity and treasury abundance.*

✨ **Codex Dominion - Sacred E-Commerce Integration** ✨