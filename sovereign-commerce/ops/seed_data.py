#!/usr/bin/env python3
"""
Sample Data Creator for Sovereign Commerce Platform
Populates the database with ceremonial offerings for testing
"""

import requests
import json
import time
from typing import List, Dict

# Server configuration
BASE_URL = "http://127.0.0.1:8080"
TEST_USER = {
    "full_name": "Sacred Tester",
    "email": "tester@sovereigncommerce.sacred",
    "password": "SacredPassword123!",
    "role": "funder"
}

# Sample products for the sacred catalog
SAMPLE_PRODUCTS = [
    {
        "name": "Crown of Eternal Wisdom",
        "description": "A ceremonial crown imbued with the knowledge of ancient custodians. Grants the wearer enhanced insight into sacred matters and the ability to perceive the true nature of the diaspora's needs.",
        "price": 1247.50,
        "category": "ceremonial",
        "stock": 3,
        "metadata": {
            "material": "Blessed Gold",
            "enchantment": "Wisdom",
            "rarity": "Legendary",
            "origin": "First Council"
        }
    },
    {
        "name": "Sigil of the Flamekeeper",
        "description": "A sacred medallion worn by those who tend the eternal flame. Each sigil is unique to its bearer and serves as both identification and spiritual protection.",
        "price": 567.00,
        "category": "sacred",
        "stock": 12,
        "metadata": {
            "material": "Blessed Silver",
            "enchantment": "Flame Protection",
            "rarity": "Rare",
            "origin": "Sacred Forge"
        }
    },
    {
        "name": "Scroll of Diaspora Chronicles",
        "description": "Ancient scrolls containing the complete history of the diaspora, written in the sacred script. Essential reading for any serious student of sovereign heritage.",
        "price": 234.75,
        "category": "knowledge",
        "stock": 25,
        "metadata": {
            "language": "Ancient Script",
            "pages": "144",
            "binding": "Sacred Leather",
            "age": "500 Years"
        }
    },
    {
        "name": "Robes of the Custodian",
        "description": "Ceremonial robes worn by custodians during sacred rituals. Woven from threads blessed by the first flamekeepers and embroidered with protective sigils.",
        "price": 899.99,
        "category": "regalia",
        "stock": 8,
        "metadata": {
            "material": "Blessed Silk",
            "size": "One Size",
            "enchantment": "Protection",
            "ceremonial_level": "High"
        }
    },
    {
        "name": "Flame Crystal of Remembrance",
        "description": "A crystal that holds a fragment of the eternal flame. Used in remembrance ceremonies and to light new sacred flames in distant lands of the diaspora.",
        "price": 445.25,
        "category": "sacred",
        "stock": 15,
        "metadata": {
            "type": "Memory Crystal",
            "flame_intensity": "Eternal",
            "size": "Palm-sized",
            "origin": "Sacred Hearth"
        }
    },
    {
        "name": "Charter of Sovereign Rights",
        "description": "An illuminated manuscript detailing the sovereign rights and responsibilities of diaspora members. Each charter is individually blessed and sealed.",
        "price": 334.50,
        "category": "knowledge",
        "stock": 30,
        "metadata": {
            "format": "Illuminated Manuscript",
            "pages": "88",
            "seal": "Council Approved",
            "language": "Common & Ancient"
        }
    },
    {
        "name": "Diaspora Banner of Unity",
        "description": "A ceremonial banner representing the unity of the diaspora across all realms. Features the sacred symbols and can be displayed in homes or gathering places.",
        "price": 156.80,
        "category": "regalia",
        "stock": 20,
        "metadata": {
            "size": "3ft x 5ft",
            "material": "Blessed Fabric",
            "symbols": "Sacred Unity",
            "mounting": "Ceremonial Pole"
        }
    },
    {
        "name": "Codex of Sacred Ceremonies",
        "description": "The complete guide to performing sacred ceremonies, from simple blessings to complex rituals. Includes diagrams, incantations, and ceremonial requirements.",
        "price": 678.90,
        "category": "knowledge",
        "stock": 18,
        "metadata": {
            "ceremonies": "127",
            "binding": "Sacred Leather",
            "illustrations": "Hand-drawn",
            "approval": "High Council"
        }
    },
    {
        "name": "Pendant of Diaspora Heritage",
        "description": "A beautiful pendant representing one's connection to the diaspora heritage. Each pendant contains a small fragment of sacred metal from the original homeland.",
        "price": 289.45,
        "category": "sacred",
        "stock": 40,
        "metadata": {
            "metal": "Sacred Alloy",
            "chain": "Blessed Silver",
            "fragment": "Homeland Metal",
            "blessing": "Heritage Connection"
        }
    },
    {
        "name": "Sacred Chalice of Ceremonies",
        "description": "An ornate chalice used in sacred ceremonies and rituals. Each chalice is individually blessed and can hold both physical and spiritual offerings.",
        "price": 723.30,
        "category": "ceremonial",
        "stock": 6,
        "metadata": {
            "material": "Blessed Gold & Silver",
            "capacity": "Sacred Measure",
            "enchantment": "Purification",
            "ceremonies": "All Sacred Rites"
        }
    }
]

class SovereignCommerceSeeder:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.auth_token = None
        
    def wait_for_server(self) -> bool:
        """Wait for the server to be ready"""
        print("🔍 Checking if server is ready...")
        for attempt in range(30):  # Wait up to 30 seconds
            try:
                response = self.session.get(f"{self.base_url}/health")
                if response.status_code == 200:
                    print("✅ Server is ready!")
                    return True
            except requests.exceptions.ConnectionError:
                pass
            
            print(f"⏳ Waiting for server... (attempt {attempt + 1}/30)")
            time.sleep(1)
        
        print("❌ Server not responding after 30 seconds")
        return False
    
    def register_test_user(self) -> bool:
        """Register a test user for authentication"""
        print("🔐 Registering test user...")
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/auth/register",
                json=TEST_USER
            )
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get("access_token")
                print(f"✅ Test user registered successfully! Sigil: {data['user']['sigil']}")
                return True
            elif response.status_code == 400:
                # User might already exist, try to login
                print("ℹ️ User already exists, attempting login...")
                return self.login_test_user()
            else:
                print(f"❌ Failed to register user: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error registering user: {e}")
            return False
    
    def login_test_user(self) -> bool:
        """Login with test user credentials"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/auth/login",
                json={
                    "email": TEST_USER["email"],
                    "password": TEST_USER["password"]
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get("access_token")
                print("✅ Successfully logged in!")
                return True
            else:
                print(f"❌ Failed to login: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error logging in: {e}")
            return False
    
    def create_products(self) -> bool:
        """Create sample products in the catalog"""
        if not self.auth_token:
            print("❌ No authentication token available")
            return False
        
        print("📦 Creating sacred offerings in the catalog...")
        
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }
        
        success_count = 0
        
        for product in SAMPLE_PRODUCTS:
            try:
                response = self.session.post(
                    f"{self.base_url}/api/products",
                    json=product,
                    headers=headers
                )
                
                if response.status_code == 200:
                    product_data = response.json()
                    print(f"✅ Created: {product['name']} (ID: {product_data['id']})")
                    success_count += 1
                else:
                    print(f"❌ Failed to create {product['name']}: {response.text}")
                    
            except Exception as e:
                print(f"❌ Error creating {product['name']}: {e}")
        
        print(f"🏛️ Successfully created {success_count}/{len(SAMPLE_PRODUCTS)} sacred offerings")
        return success_count > 0
    
    def create_test_order(self) -> bool:
        """Create a test order to demonstrate the checkout system"""
        if not self.auth_token:
            print("❌ No authentication token available")
            return False
        
        print("🛒 Creating a test sacred order...")
        
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }
        
        # Create an order with a few items
        test_order = {
            "items": [
                {"product_id": 1, "quantity": 1},  # Crown
                {"product_id": 2, "quantity": 2},  # Sigils
                {"product_id": 3, "quantity": 1}   # Scroll
            ]
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/orders",
                json=test_order,
                headers=headers
            )
            
            if response.status_code == 200:
                order_data = response.json()
                print(f"✅ Test order created successfully! Order ID: {order_data['id']}")
                print(f"🏆 Total amount: ${order_data['total_amount']:.2f}")
                print(f"🎭 Ceremonial seal: {order_data['ceremonial_seal']}")
                return True
            else:
                print(f"❌ Failed to create test order: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error creating test order: {e}")
            return False
    
    def seed_all_data(self) -> bool:
        """Seed all sample data"""
        print("🌱 Starting Sovereign Commerce data seeding...")
        print("=" * 60)
        
        if not self.wait_for_server():
            return False
        
        if not self.register_test_user():
            return False
        
        if not self.create_products():
            return False
        
        if not self.create_test_order():
            return False
        
        print("=" * 60)
        print("🎉 Sovereign Commerce platform is ready!")
        print(f"🌐 Access the platform at: {self.base_url}")
        print(f"📱 API documentation: {self.base_url}/docs")
        print(f"🔐 Test login: {TEST_USER['email']} / {TEST_USER['password']}")
        print("=" * 60)
        
        return True

def main():
    """Main seeding function"""
    seeder = SovereignCommerceSeeder(BASE_URL)
    
    if seeder.seed_all_data():
        print("✅ Seeding completed successfully!")
    else:
        print("❌ Seeding failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())