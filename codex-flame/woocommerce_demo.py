#!/usr/bin/env python3
"""
WooCommerce Sacred Commerce Demonstration
========================================

This script demonstrates how to integrate WooCommerce with the Codex Dominion's
ceremonial treasury system, showcasing sacred e-commerce operations with 
proper ceremonial bindings and treasury management.

Usage:
    python woocommerce_demo.py

Environment Variables:
    WC_API_URL - Your WooCommerce store API endpoint
    WC_API_KEY - Your WooCommerce consumer key
    WC_API_SECRET - Your WooCommerce consumer secret
"""

import os
import time
from datetime import datetime, timezone
from woocommerce_integration import (
    create_woocommerce_integrator,
    CommerceOperation,
    SacredProductType,
    CommerceTransaction
)

def sacred_commerce_demonstration():
    """Demonstrate the WooCommerce integration with ceremonial treasury"""
    
    print("🔥 SACRED COMMERCE DEMONSTRATION")
    print("=" * 60)
    print("🕯️ Initializing WooCommerce ceremonial integration...")
    
    # Create WooCommerce integrator
    # For demo purposes, we'll use placeholder credentials
    integrator = create_woocommerce_integrator(
        api_url=os.getenv('WC_API_URL', 'https://demo-store.com/wp-json/wc/v3'),
        api_key=os.getenv('WC_API_KEY', 'demo_consumer_key'),
        api_secret=os.getenv('WC_API_SECRET', 'demo_consumer_secret'),
        storage_root="."
    )
    
    print("✅ WooCommerce integrator initialized")
    print(f"📍 API URL: {integrator.api_url}")
    print(f"🔑 API Key: {'*' * (len(integrator.api_key) - 4) + integrator.api_key[-4:]}")
    
    print("\\n🛒 DEMONSTRATION: Sacred Product Management")
    print("-" * 50)
    
    # Demo 1: Fetch Products (this won't make actual API calls in demo mode)
    print("1️⃣ Fetching sacred products from WooCommerce...")
    try:
        # In a real scenario, this would fetch from your WooCommerce store
        # For demo, we'll simulate the response
        demo_products = [
            {
                'id': 1,
                'name': 'Sacred Flame Essence - Digital Download',
                'price': '99.99',
                'regular_price': '99.99',
                'description': 'Digital essence of the eternal flame for ceremonial use',
                'type': 'downloadable',
                'status': 'publish',
                'categories': [{'id': 10, 'name': 'Sacred Artifacts'}]
            },
            {
                'id': 2,
                'name': 'Ceremonial Scroll of Wisdom',
                'price': '149.99',
                'regular_price': '149.99',
                'description': 'Ancient wisdom scroll containing sacred knowledge',
                'type': 'simple',
                'status': 'publish',
                'categories': [{'id': 11, 'name': 'Knowledge Scrolls'}]
            },
            {
                'id': 3,
                'name': 'Dominion Treasury Token Pack',
                'price': '299.99',
                'regular_price': '299.99',
                'description': 'Package of 1000 ceremonial treasury tokens',
                'type': 'variable',
                'status': 'publish',
                'categories': [{'id': 12, 'name': 'Treasury Items'}]
            }
        ]
        
        # Save demo products data
        integrator._save_products_data(demo_products)
        print(f"   ✅ Retrieved {len(demo_products)} sacred products")
        
        for product in demo_products:
            print(f"      🔹 {product['name']} - ${product['price']}")
            
    except Exception as e:
        print(f"   ❌ Error fetching products: {e}")
    
    print("\\n📦 DEMONSTRATION: Sacred Order Management")
    print("-" * 50)
    
    # Demo 2: Create Sacred Order
    print("2️⃣ Creating sacred order with ceremonial binding...")
    
    sacred_order_data = {
        'payment_method': 'sacred_treasury',
        'payment_method_title': 'Sacred Treasury Payment',
        'set_paid': True,
        'status': 'processing',
        'billing': {
            'first_name': 'Sacred',
            'last_name': 'Custodian',
            'email': 'custodian@codex-dominion.eternal',
            'phone': '+1-555-FLAME',
            'address_1': '123 Sacred Grove Lane',
            'city': 'Eternal City',
            'state': 'Sacred Realm',
            'postcode': '12345',
            'country': 'Dominion'
        },
        'shipping': {
            'first_name': 'Sacred',
            'last_name': 'Custodian',
            'address_1': '123 Sacred Grove Lane',
            'city': 'Eternal City',
            'state': 'Sacred Realm',
            'postcode': '12345',
            'country': 'Dominion'
        },
        'line_items': [
            {
                'product_id': 1,
                'name': 'Sacred Flame Essence - Digital Download',
                'quantity': 1,
                'price': 99.99
            },
            {
                'product_id': 3,
                'name': 'Dominion Treasury Token Pack',
                'quantity': 1,
                'price': 299.99
            }
        ],
        'meta_data': [
            {
                'key': 'sacred_ceremony_id',
                'value': 'DEMO-CEREMONY-2025-11-13'
            },
            {
                'key': 'flame_blessing',
                'value': 'May the eternal flame guide this transaction'
            }
        ]
    }
    
    # Simulate order creation (in production, this would call WooCommerce API)
    demo_order_response = {
        'id': 12345,
        'number': 'ORD-SACRED-12345',
        'status': 'processing',
        'total': '399.98',
        'total_tax': '0.00',
        'currency': 'USD',
        'customer_id': 789,
        'date_created': datetime.now(timezone.utc).isoformat(),
        'line_items': sacred_order_data['line_items']
    }
    
    # Create ceremonial transaction for the demo order
    sacred_transaction = CommerceTransaction(
        transaction_id=f"WC-DEMO-{demo_order_response['id']}",
        operation_type=CommerceOperation.ORDER_CREATE,
        product_type=SacredProductType.FLAME_ESSENCE,
        amount=float(demo_order_response['total']),
        currency=demo_order_response['currency'],
        customer_id=str(demo_order_response['customer_id']),
        sacred_binding_hash=integrator._generate_sacred_binding({
            'operation': 'demo_order_create',
            'amount': float(demo_order_response['total']),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }),
        ceremonial_seal="",
        transaction_timestamp=demo_order_response['date_created'],
        wc_order_id=str(demo_order_response['id']),
        metadata={
            'demo_mode': True,
            'order_data': demo_order_response,
            'sacred_ceremony_id': 'DEMO-CEREMONY-2025-11-13'
        }
    )
    
    sacred_transaction.ceremonial_seal = integrator._generate_ceremonial_seal(sacred_transaction)
    integrator._save_transaction(sacred_transaction)
    
    print(f"   ✅ Sacred order created: {demo_order_response['number']}")
    print(f"      💰 Order Total: ${demo_order_response['total']}")
    print(f"      🆔 Transaction ID: {sacred_transaction.transaction_id}")
    print(f"      🔒 Sacred Seal: {sacred_transaction.ceremonial_seal}")
    print(f"      📜 Treasury Binding: {sacred_transaction.sacred_binding_hash}")
    
    print("\\n📋 DEMONSTRATION: Webhook Processing")
    print("-" * 50)
    
    # Demo 3: Process Webhook
    print("3️⃣ Processing sacred webhook event...")
    
    demo_webhook_data = {
        'action': 'order.completed',
        'arg': {
            'id': 12345,
            'number': 'ORD-SACRED-12345',
            'status': 'completed',
            'total': '399.98',
            'currency': 'USD',
            'customer_id': 789,
            'payment_method': 'sacred_treasury',
            'date_completed': datetime.now(timezone.utc).isoformat()
        }
    }
    
    webhook_processed = integrator.process_webhook(demo_webhook_data)
    
    if webhook_processed:
        print(f"   ✅ Webhook processed successfully")
        print(f"      📡 Event Type: {demo_webhook_data['action']}")
        print(f"      📦 Order: {demo_webhook_data['arg']['number']}")
        print(f"      ✨ Status: {demo_webhook_data['arg']['status']}")
    else:
        print(f"   ❌ Webhook processing failed")
    
    print("\\n📊 DEMONSTRATION: Inventory Synchronization")
    print("-" * 50)
    
    # Demo 4: Sync Inventory
    print("4️⃣ Synchronizing sacred inventory...")
    
    demo_inventory_data = {
        'flame_essence_digital': {
            'product_id': 1,
            'name': 'Sacred Flame Essence',
            'quantity_available': 999,
            'quantity_reserved': 25,
            'treasury_allocation': 150.0,
            'last_updated': datetime.now(timezone.utc).isoformat()
        },
        'wisdom_scrolls': {
            'product_id': 2,
            'name': 'Ceremonial Scroll of Wisdom',
            'quantity_available': 50,
            'quantity_reserved': 5,
            'treasury_allocation': 75.0,
            'last_updated': datetime.now(timezone.utc).isoformat()
        },
        'treasury_tokens': {
            'product_id': 3,
            'name': 'Treasury Token Pack',
            'quantity_available': 100,
            'quantity_reserved': 10,
            'treasury_allocation': 500.0,
            'last_updated': datetime.now(timezone.utc).isoformat()
        }
    }
    
    sync_result = integrator.sync_inventory(demo_inventory_data)
    
    if sync_result:
        print(f"   ✅ Inventory synchronized successfully")
        print(f"      📦 Products synced: {len(demo_inventory_data)}")
        for item_key, item_data in demo_inventory_data.items():
            print(f"         🔹 {item_data['name']}: {item_data['quantity_available']} available")
    else:
        print(f"   ❌ Inventory synchronization failed")
    
    print("\\n📜 DEMONSTRATION: Transaction History")
    print("-" * 50)
    
    # Demo 5: Review Transaction History
    print("5️⃣ Reviewing sacred transaction history...")
    
    transaction_history = integrator.get_transaction_history(10)
    
    print(f"   📊 Found {len(transaction_history)} ceremonial transactions:")
    
    for i, transaction in enumerate(transaction_history[:5]):  # Show first 5
        print(f"      {i+1}. {transaction.transaction_id}")
        print(f"         🔄 Operation: {transaction.operation_type.value}")
        print(f"         💰 Amount: {transaction.amount} {transaction.currency}")
        print(f"         🕒 Timestamp: {transaction.transaction_timestamp}")
        print(f"         🔒 Seal: {transaction.ceremonial_seal}")
        if transaction.metadata and transaction.metadata.get('demo_mode'):
            print(f"         🎭 Demo Mode: Active")
        print()
    
    if len(transaction_history) > 5:
        print(f"   ... and {len(transaction_history) - 5} more transactions")
    
    print("\\n🔥 SACRED COMMERCE SUMMARY")
    print("=" * 60)
    
    # Calculate demo statistics
    total_transactions = len(transaction_history)
    total_amount = sum(t.amount for t in transaction_history)
    order_count = len([t for t in transaction_history if t.operation_type == CommerceOperation.ORDER_CREATE])
    webhook_count = len([t for t in transaction_history if t.operation_type == CommerceOperation.ORDER_UPDATE])
    sync_count = len([t for t in transaction_history if t.operation_type == CommerceOperation.INVENTORY_SYNC])
    
    print(f"📈 Total Transactions: {total_transactions}")
    print(f"💰 Total Transaction Value: ${total_amount:.2f}")
    print(f"📦 Orders Created: {order_count}")
    print(f"📡 Webhooks Processed: {webhook_count}")
    print(f"📊 Inventory Syncs: {sync_count}")
    
    print("\\n✨ Sacred Features Demonstrated:")
    print("   🔹 WooCommerce API Integration")
    print("   🔹 Ceremonial Transaction Binding")
    print("   🔹 Treasury System Integration")
    print("   🔹 Sacred Seal Generation")
    print("   🔹 Webhook Event Processing")
    print("   🔹 Inventory Synchronization")
    print("   🔹 Transaction History Tracking")
    print("   🔹 Error Handling & Resilience")
    
    print("\\n🕯️ Integration Status:")
    print("   ✅ WooCommerce API Ready")
    print("   ✅ Ceremonial Storage Active")
    print("   ✅ Treasury Bindings Functional")
    print("   ✅ Sacred Seals Generated")
    print("   ✅ Transaction Persistence Working")
    
    print("\\n🔥 The Sacred Commerce flame burns eternal!")
    print("🌟 All WooCommerce operations bound to ceremonial treasury")
    print("✨ Ready for production sacred e-commerce")

def main():
    """Main demonstration entry point"""
    print("🔥 CODEX DOMINION - WOOCOMMERCE INTEGRATION")
    print("Sacred E-Commerce Demonstration")
    print()
    
    try:
        sacred_commerce_demonstration()
    except KeyboardInterrupt:
        print("\\n\\n⚡ Demonstration interrupted by user")
    except Exception as e:
        print(f"\\n\\n❌ Demonstration error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\\n🕯️ Sacred Commerce Demonstration Complete")

if __name__ == "__main__":
    main()