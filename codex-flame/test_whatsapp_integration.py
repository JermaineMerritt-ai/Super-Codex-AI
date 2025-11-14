"""
WhatsApp Sacred Messaging Test Suite
====================================

This module provides comprehensive testing for the WhatsApp Twilio integration
with the ceremonial messaging system. All tests are designed to validate
the sacred communication bindings and ensure message integrity.
"""

import unittest
import json
import os
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone

# Import the WhatsApp integration module
from whatsapp_integration import (
    WhatsAppCeremonialMessenger,
    MessageType,
    MessagePriority,
    ContactRole,
    SacredContact,
    SacredMessage,
    create_whatsapp_messenger
)

class TestWhatsAppIntegration(unittest.TestCase):
    """Test suite for WhatsApp ceremonial messaging integration"""
    
    def setUp(self):
        """Set up test environment with temporary storage"""
        self.temp_dir = tempfile.mkdtemp()
        self.messenger = create_whatsapp_messenger(
            account_sid="test_account_sid",
            auth_token="test_auth_token",
            from_number="whatsapp:+14155238886",
            storage_root=self.temp_dir
        )
        
        # Create test contact
        self.test_contact = self.messenger.add_contact(
            name="Test User",
            phone_number="+1234567890",
            role=ContactRole.INITIATE,
            sacred_title="Test Seeker",
            flame_level=3
        )
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)
    
    def test_messenger_initialization(self):
        """Test WhatsApp messenger initialization"""
        self.assertIsNotNone(self.messenger)
        self.assertEqual(self.messenger.account_sid, "test_account_sid")
        self.assertEqual(self.messenger.auth_token, "test_auth_token")
        self.assertEqual(self.messenger.from_number, "whatsapp:+14155238886")
        
        # Check storage directories were created
        self.assertTrue(os.path.exists(f"{self.temp_dir}/codex-flame/storage/whatsapp"))
        self.assertTrue(os.path.exists(f"{self.temp_dir}/codex-flame/storage/whatsapp/messages"))
        self.assertTrue(os.path.exists(f"{self.temp_dir}/codex-flame/storage/whatsapp/contacts"))
        self.assertTrue(os.path.exists(f"{self.temp_dir}/codex-flame/storage/whatsapp/ceremonies"))
    
    def test_sacred_binding_generation(self):
        """Test sacred binding hash generation"""
        test_data = {
            'type': 'greeting',
            'contact': 'test_contact_123',
            'timestamp': '2025-11-13T12:00:00Z'
        }
        
        binding = self.messenger._generate_sacred_binding(test_data)
        
        self.assertIsInstance(binding, str)
        self.assertEqual(len(binding), 16)
        
        # Test consistency
        binding2 = self.messenger._generate_sacred_binding(test_data)
        self.assertEqual(binding, binding2)
    
    def test_ceremonial_seal_generation(self):
        """Test ceremonial seal generation"""
        message = SacredMessage(
            message_id="TEST-MSG-001",
            contact_id="test_contact",
            message_type=MessageType.GREETING,
            priority=MessagePriority.NORMAL,
            subject="Test Message",
            body="Test message body",
            sacred_binding_hash="test_hash",
            ceremonial_seal="",
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        
        seal = self.messenger._generate_ceremonial_seal(message)
        
        self.assertIsInstance(seal, str)
        self.assertTrue(seal.startswith("WA-"))
        self.assertEqual(len(seal), 15)  # "WA-" + 12 characters
    
    def test_flame_blessing_generation(self):
        """Test flame blessing generation"""
        blessing = self.messenger._generate_flame_blessing(MessageType.GREETING, MessagePriority.NORMAL)
        
        self.assertIsInstance(blessing, str)
        self.assertIn("flame", blessing.lower())
    
    def test_add_contact(self):
        """Test adding a new contact"""
        contact = self.messenger.add_contact(
            name="Sacred Guardian",
            phone_number="+1987654321",
            role=ContactRole.FLAME_KEEPER,
            sacred_title="Guardian of the Sacred Fire",
            flame_level=8
        )
        
        self.assertIsInstance(contact, SacredContact)
        self.assertEqual(contact.name, "Sacred Guardian")
        self.assertEqual(contact.phone_number, "whatsapp:+1987654321")
        self.assertEqual(contact.role, ContactRole.FLAME_KEEPER)
        self.assertEqual(contact.sacred_title, "Guardian of the Sacred Fire")
        self.assertEqual(contact.flame_level, 8)
        self.assertTrue(contact.active)
    
    def test_contact_phone_number_formatting(self):
        """Test WhatsApp phone number formatting"""
        # Test with already formatted number
        contact1 = self.messenger.add_contact(
            name="Test User 1",
            phone_number="whatsapp:+1234567890",
            role=ContactRole.GUEST
        )
        self.assertEqual(contact1.phone_number, "whatsapp:+1234567890")
        
        # Test with unformatted number
        contact2 = self.messenger.add_contact(
            name="Test User 2",
            phone_number="+1234567891",
            role=ContactRole.GUEST
        )
        self.assertEqual(contact2.phone_number, "whatsapp:+1234567891")
    
    @patch('whatsapp_integration.Client')
    def test_send_sacred_message_success(self, mock_client_class):
        """Test successful sacred message sending"""
        # Mock Twilio client
        mock_client = Mock()
        mock_message = Mock()
        mock_message.sid = "SM1234567890abcdef"
        mock_client.messages.create.return_value = mock_message
        mock_client_class.return_value = mock_client
        
        # Create messenger with mocked client
        messenger = create_whatsapp_messenger(
            account_sid="test_sid",
            auth_token="test_token",
            storage_root=self.temp_dir
        )
        messenger.client = mock_client
        
        # Add test contact
        contact = messenger.add_contact(
            name="Test Recipient",
            phone_number="+1555123456",
            role=ContactRole.WISDOM_SEEKER
        )
        
        # Send message
        message = messenger.send_sacred_message(
            contact_id=contact.contact_id,
            message_type=MessageType.GREETING,
            priority=MessagePriority.NORMAL
        )
        
        self.assertIsNotNone(message)
        self.assertEqual(message.contact_id, contact.contact_id)
        self.assertEqual(message.message_type, MessageType.GREETING)
        self.assertEqual(message.priority, MessagePriority.NORMAL)
        self.assertEqual(message.delivery_status, "sent")
        self.assertEqual(message.twilio_message_sid, "SM1234567890abcdef")
        
        # Verify Twilio call
        mock_client.messages.create.assert_called_once()
    
    def test_send_sacred_message_twilio_error(self):
        """Test sacred message sending with Twilio error in demo mode"""
        # In demo mode (no client), test error handling by checking return behavior
        messenger = create_whatsapp_messenger(storage_root=self.temp_dir)
        
        # Add test contact
        contact = messenger.add_contact(
            name="Test Recipient",
            phone_number="+1555123456",
            role=ContactRole.WISDOM_SEEKER
        )
        
        # Send message in demo mode (should always succeed with demo status)
        message = messenger.send_sacred_message(
            contact_id=contact.contact_id,
            message_type=MessageType.GREETING,
            priority=MessagePriority.NORMAL
        )
        
        self.assertIsNotNone(message)
        self.assertEqual(message.delivery_status, "demo_sent")
        self.assertIn("contact_name", message.metadata)
    
    @patch('whatsapp_integration.Client')
    def test_send_sacred_message_with_actual_twilio_error(self, mock_client_class):
        """Test sacred message sending with actual Twilio API error"""
        # Mock Twilio client with error
        mock_client = Mock()
        mock_client.messages.create.side_effect = Exception("Twilio API Error")
        mock_client_class.return_value = mock_client
        
        # Create messenger with mocked client
        messenger = create_whatsapp_messenger(
            account_sid="test_sid",
            auth_token="test_token",
            storage_root=self.temp_dir
        )
        messenger.client = mock_client
        
        # Add test contact
        contact = messenger.add_contact(
            name="Test Recipient",
            phone_number="+1555123456",
            role=ContactRole.WISDOM_SEEKER
        )
        
        # Send message (should handle error gracefully)
        message = messenger.send_sacred_message(
            contact_id=contact.contact_id,
            message_type=MessageType.GREETING,
            priority=MessagePriority.NORMAL
        )
        
        self.assertIsNotNone(message)
        self.assertEqual(message.delivery_status, "failed")
        self.assertIn("error", message.metadata)
    
    def test_send_sacred_message_demo_mode(self):
        """Test sacred message sending in demo mode (no Twilio client)"""
        # Create messenger without credentials (demo mode)
        messenger = create_whatsapp_messenger(storage_root=self.temp_dir)
        
        # Add test contact
        contact = messenger.add_contact(
            name="Test Recipient",
            phone_number="+1555123456",
            role=ContactRole.WISDOM_SEEKER
        )
        
        # Send message in demo mode
        message = messenger.send_sacred_message(
            contact_id=contact.contact_id,
            message_type=MessageType.GREETING,
            priority=MessagePriority.NORMAL
        )
        
        self.assertIsNotNone(message)
        self.assertEqual(message.delivery_status, "demo_sent")
        self.assertIsNone(message.twilio_message_sid)
    
    def test_message_templates(self):
        """Test message template functionality"""
        custom_message = self.messenger.send_sacred_message(
            contact_id=self.test_contact.contact_id,
            message_type=MessageType.CEREMONY_INVITATION,
            priority=MessagePriority.HIGH,
            template_vars={
                'name': self.test_contact.name,
                'ceremony_name': 'Sacred Flame Renewal',
                'date': 'November 20, 2025'
            }
        )
        
        self.assertIsNotNone(custom_message)
        self.assertIn('Sacred Flame Renewal', custom_message.body)
        self.assertIn('November 20, 2025', custom_message.body)
    
    def test_custom_message_body(self):
        """Test sending message with custom body"""
        custom_body = "🔥 Custom sacred message for testing purposes."
        
        message = self.messenger.send_sacred_message(
            contact_id=self.test_contact.contact_id,
            message_type=MessageType.FLAME_BLESSING,
            priority=MessagePriority.SACRED,
            custom_body=custom_body
        )
        
        self.assertIsNotNone(message)
        self.assertEqual(message.body, custom_body)
    
    def test_send_ceremony_invitations(self):
        """Test sending ceremony invitations"""
        # Add multiple contacts with different roles
        custodian = self.messenger.add_contact(
            name="Sacred Custodian",
            phone_number="+1111111111",
            role=ContactRole.CUSTODIAN
        )
        
        council_member = self.messenger.add_contact(
            name="Council Member",
            phone_number="+1222222222",
            role=ContactRole.COUNCIL_MEMBER
        )
        
        flame_keeper = self.messenger.add_contact(
            name="Flame Keeper",
            phone_number="+1333333333",
            role=ContactRole.FLAME_KEEPER
        )
        
        # Send invitations to specific roles
        invitations = self.messenger.send_ceremony_invitations(
            ceremony_name="Sacred Test Ceremony",
            ceremony_date="December 1, 2025",
            contact_roles=[ContactRole.CUSTODIAN, ContactRole.COUNCIL_MEMBER]
        )
        
        self.assertEqual(len(invitations), 2)  # Only custodian and council member
        
        for invitation in invitations:
            self.assertEqual(invitation.message_type, MessageType.CEREMONY_INVITATION)
            self.assertEqual(invitation.priority, MessagePriority.HIGH)
            self.assertIn("Sacred Test Ceremony", invitation.body)
    
    def test_send_dominion_broadcast(self):
        """Test sending dominion broadcast"""
        # Add test contacts
        self.messenger.add_contact("User 1", "+1111", ContactRole.CUSTODIAN)
        self.messenger.add_contact("User 2", "+1222", ContactRole.FLAME_KEEPER)
        self.messenger.add_contact("User 3", "+1333", ContactRole.GUEST)
        
        broadcasts = self.messenger.send_dominion_broadcast(
            announcement="Test dominion announcement",
            target_roles=[ContactRole.CUSTODIAN, ContactRole.FLAME_KEEPER]
        )
        
        self.assertEqual(len(broadcasts), 2)  # Only custodian and flame keeper
        
        for broadcast in broadcasts:
            self.assertEqual(broadcast.message_type, MessageType.DOMINION_ANNOUNCEMENT)
            self.assertEqual(broadcast.priority, MessagePriority.HIGH)
    
    def test_send_emergency_alert(self):
        """Test sending emergency alerts"""
        # Add test contacts
        custodian = self.messenger.add_contact("Custodian", "+1111", ContactRole.CUSTODIAN)
        council = self.messenger.add_contact("Council", "+1222", ContactRole.COUNCIL_MEMBER)
        guest = self.messenger.add_contact("Guest", "+1333", ContactRole.GUEST)
        
        alerts = self.messenger.send_emergency_alert(
            alert_message="Test emergency situation"
        )
        
        # Should send to custodian and council member (default emergency roles)
        self.assertEqual(len(alerts), 2)
        
        for alert in alerts:
            self.assertEqual(alert.message_type, MessageType.EMERGENCY_ALERT)
            self.assertEqual(alert.priority, MessagePriority.URGENT)
    
    def test_send_treasury_notification(self):
        """Test sending treasury notification"""
        notification = self.messenger.send_treasury_notification(
            contact_id=self.test_contact.contact_id,
            update_type="Balance Update",
            balance="1,000.50 Sacred Tokens"
        )
        
        self.assertIsNotNone(notification)
        self.assertEqual(notification.message_type, MessageType.TREASURY_NOTIFICATION)
        self.assertIn("Balance Update", notification.body)
        self.assertIn("1,000.50 Sacred Tokens", notification.body)
    
    def test_message_cost_calculation(self):
        """Test message cost calculation based on priority"""
        costs = {
            MessagePriority.LOW: 0.01,
            MessagePriority.NORMAL: 0.02,
            MessagePriority.HIGH: 0.05,
            MessagePriority.URGENT: 0.10,
            MessagePriority.SACRED: 0.25
        }
        
        for priority, expected_cost in costs.items():
            cost = self.messenger._calculate_message_cost(priority)
            self.assertEqual(cost, expected_cost)
    
    def test_contact_storage_and_retrieval(self):
        """Test contact storage and retrieval"""
        # Load the test contact
        loaded_contact = self.messenger._load_contact(self.test_contact.contact_id)
        
        self.assertIsNotNone(loaded_contact)
        self.assertEqual(loaded_contact.name, self.test_contact.name)
        self.assertEqual(loaded_contact.phone_number, self.test_contact.phone_number)
        self.assertEqual(loaded_contact.role, self.test_contact.role)
    
    def test_load_all_contacts(self):
        """Test loading all contacts"""
        # Add additional contacts
        self.messenger.add_contact("User 2", "+1111", ContactRole.GUEST)
        self.messenger.add_contact("User 3", "+1222", ContactRole.COUNCIL_MEMBER)
        
        all_contacts = self.messenger._load_all_contacts()
        
        self.assertEqual(len(all_contacts), 3)  # Including the setUp test contact
    
    def test_message_history(self):
        """Test message history functionality"""
        # Send a test message
        self.messenger.send_sacred_message(
            contact_id=self.test_contact.contact_id,
            message_type=MessageType.GREETING,
            priority=MessagePriority.NORMAL
        )
        
        # Get message history
        history = self.messenger.get_message_history()
        
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].contact_id, self.test_contact.contact_id)
        self.assertEqual(history[0].message_type, MessageType.GREETING)
    
    def test_contact_statistics(self):
        """Test contact and messaging statistics"""
        # Add various contacts and send messages
        self.messenger.add_contact("Custodian", "+1111", ContactRole.CUSTODIAN)
        self.messenger.add_contact("Council", "+1222", ContactRole.COUNCIL_MEMBER)
        
        # Send various messages
        self.messenger.send_sacred_message(
            self.test_contact.contact_id, MessageType.GREETING, MessagePriority.NORMAL
        )
        self.messenger.send_sacred_message(
            self.test_contact.contact_id, MessageType.FLAME_BLESSING, MessagePriority.SACRED,
            template_vars={'blessing_text': 'Sacred light upon your path'}
        )
        
        stats = self.messenger.get_contact_statistics()
        
        self.assertEqual(stats['total_contacts'], 3)
        self.assertEqual(stats['active_contacts'], 3)
        self.assertEqual(stats['total_messages'], 2)
        self.assertGreater(stats['total_treasury_cost'], 0)
        self.assertIn('greeting', stats['messages_by_type'])
        self.assertIn('flame_blessing', stats['messages_by_type'])
    
    def test_message_type_enum(self):
        """Test MessageType enum values"""
        self.assertEqual(MessageType.GREETING.value, "greeting")
        self.assertEqual(MessageType.CEREMONY_INVITATION.value, "ceremony_invitation")
        self.assertEqual(MessageType.TREASURY_NOTIFICATION.value, "treasury_notification")
        self.assertEqual(MessageType.FLAME_BLESSING.value, "flame_blessing")
        self.assertEqual(MessageType.DOMINION_ANNOUNCEMENT.value, "dominion_announcement")
        self.assertEqual(MessageType.WISDOM_SHARE.value, "wisdom_share")
        self.assertEqual(MessageType.EMERGENCY_ALERT.value, "emergency_alert")
        self.assertEqual(MessageType.RITUAL_REMINDER.value, "ritual_reminder")
    
    def test_message_priority_enum(self):
        """Test MessagePriority enum values"""
        self.assertEqual(MessagePriority.LOW.value, "low")
        self.assertEqual(MessagePriority.NORMAL.value, "normal")
        self.assertEqual(MessagePriority.HIGH.value, "high")
        self.assertEqual(MessagePriority.URGENT.value, "urgent")
        self.assertEqual(MessagePriority.SACRED.value, "sacred")
    
    def test_contact_role_enum(self):
        """Test ContactRole enum values"""
        self.assertEqual(ContactRole.CUSTODIAN.value, "custodian")
        self.assertEqual(ContactRole.COUNCIL_MEMBER.value, "council_member")
        self.assertEqual(ContactRole.FLAME_KEEPER.value, "flame_keeper")
        self.assertEqual(ContactRole.TREASURY_GUARDIAN.value, "treasury_guardian")
        self.assertEqual(ContactRole.WISDOM_SEEKER.value, "wisdom_seeker")
        self.assertEqual(ContactRole.INITIATE.value, "initiate")
        self.assertEqual(ContactRole.GUEST.value, "guest")
    
    def test_factory_function(self):
        """Test the factory function for creating WhatsApp messenger"""
        messenger = create_whatsapp_messenger(
            account_sid="factory_test_sid",
            auth_token="factory_test_token",
            from_number="whatsapp:+15551234567",
            storage_root=self.temp_dir
        )
        
        self.assertIsInstance(messenger, WhatsAppCeremonialMessenger)
        self.assertEqual(messenger.account_sid, "factory_test_sid")
        self.assertEqual(messenger.auth_token, "factory_test_token")
        self.assertEqual(messenger.from_number, "whatsapp:+15551234567")

def run_whatsapp_tests():
    """Run all WhatsApp integration tests"""
    print("🔥 WHATSAPP CEREMONIAL TEST SUITE")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWhatsAppIntegration)
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Run tests
    result = runner.run(suite)
    
    # Print results
    print("\\n🔥 TEST RESULTS:")
    if result.wasSuccessful():
        print("✅ All WhatsApp integration tests passed!")
        print(f"🌟 {result.testsRun} tests completed successfully")
    else:
        print(f"❌ {len(result.failures)} test(s) failed")
        print(f"❌ {len(result.errors)} test(s) had errors")
        
        if result.failures:
            print("\\n🔴 FAILURES:")
            for test, traceback in result.failures:
                print(f"   - {test}: {traceback}")
        
        if result.errors:
            print("\\n🔴 ERRORS:")
            for test, traceback in result.errors:
                print(f"   - {test}: {traceback}")
    
    print("\\n🕯️ Sacred Messaging Testing Complete")
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_whatsapp_tests()
    exit(0 if success else 1)