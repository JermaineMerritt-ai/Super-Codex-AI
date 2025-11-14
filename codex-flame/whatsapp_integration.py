"""
Twilio WhatsApp Sacred Messaging Integration
==========================================

This module implements the Twilio WhatsApp API integration for the ceremonial messaging system,
enabling sacred communications operations aligned with the flame architecture principles.

The WhatsApp binding operates as a bridge between the ceremonial messaging and 
external communication platforms, ensuring that all messages maintain sacred integrity
and are properly recorded in the ceremonial ledger.
"""

import os
import json
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import hashlib

# Twilio imports with fallback for demo mode
try:
    from twilio.rest import Client
    from twilio.base.exceptions import TwilioException
    TWILIO_AVAILABLE = True
except ImportError:
    print("📱 Twilio SDK not installed - running in demo mode")
    print("   To enable full functionality, install with: pip install twilio")
    TWILIO_AVAILABLE = False
    
    # Create mock classes for demo mode
    class TwilioException(Exception):
        pass
    
    class Client:
        def __init__(self, account_sid, auth_token):
            self.account_sid = account_sid
            self.auth_token = auth_token

# Import ceremonial modules
from treasury import create_treasury_binding, ResourceType, TreasuryOperation
from schema_validator import CeremonialSchemaValidator

# WhatsApp integration constants
WHATSAPP_INTEGRATION_PATH = "codex-flame/storage/whatsapp"
WHATSAPP_MESSAGES_PATH = "codex-flame/storage/whatsapp/messages"
WHATSAPP_CONTACTS_PATH = "codex-flame/storage/whatsapp/contacts"
WHATSAPP_CEREMONIES_PATH = "codex-flame/storage/whatsapp/ceremonies"

class MessageType(Enum):
    """Types of sacred messages"""
    GREETING = "greeting"
    CEREMONY_INVITATION = "ceremony_invitation"
    TREASURY_NOTIFICATION = "treasury_notification"
    FLAME_BLESSING = "flame_blessing"
    DOMINION_ANNOUNCEMENT = "dominion_announcement"
    WISDOM_SHARE = "wisdom_share"
    EMERGENCY_ALERT = "emergency_alert"
    RITUAL_REMINDER = "ritual_reminder"

class MessagePriority(Enum):
    """Message priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"
    SACRED = "sacred"

class ContactRole(Enum):
    """Contact roles in the dominion"""
    CUSTODIAN = "custodian"
    COUNCIL_MEMBER = "council_member"
    FLAME_KEEPER = "flame_keeper"
    TREASURY_GUARDIAN = "treasury_guardian"
    WISDOM_SEEKER = "wisdom_seeker"
    INITIATE = "initiate"
    GUEST = "guest"

@dataclass
class SacredContact:
    """Represents a contact in the sacred messaging system"""
    contact_id: str
    name: str
    phone_number: str
    role: ContactRole
    sacred_title: Optional[str] = None
    flame_level: int = 1
    last_contact: Optional[str] = None
    active: bool = True
    ceremonial_permissions: List[str] = None
    metadata: Dict[str, Any] = None

@dataclass
class SacredMessage:
    """Represents a sacred message with ceremonial binding"""
    message_id: str
    contact_id: str
    message_type: MessageType
    priority: MessagePriority
    subject: str
    body: str
    sacred_binding_hash: str
    ceremonial_seal: str
    timestamp: str
    twilio_message_sid: Optional[str] = None
    delivery_status: str = "pending"
    treasury_cost: float = 0.0
    flame_blessing: Optional[str] = None
    metadata: Dict[str, Any] = None

class WhatsAppCeremonialMessenger:
    """Main class for WhatsApp ceremonial messaging integration"""
    
    def __init__(self, account_sid: str = None, auth_token: str = None, 
                 from_number: str = None, storage_root: str = "."):
        """Initialize the WhatsApp messenger with ceremonial binding"""
        self.storage_root = storage_root
        self._ensure_storage_directories()
        
        # Load credentials from environment or parameters
        self.account_sid = account_sid or os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = auth_token or os.getenv('TWILIO_AUTH_TOKEN')
        self.from_number = from_number or os.getenv('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')
        
        # Initialize Twilio client
        if self.account_sid and self.auth_token and TWILIO_AVAILABLE:
            self.client = Client(self.account_sid, self.auth_token)
        else:
            self.client = None
            if not TWILIO_AVAILABLE:
                print("⚠️  Twilio SDK not available - running in demo mode")
            else:
                print("⚠️  Twilio credentials not provided - running in demo mode")
        
        # Initialize ceremonial components
        self.treasury = create_treasury_binding(storage_root)
        self.validator = CeremonialSchemaValidator()
        
        # Sacred message templates
        self.message_templates = {
            MessageType.GREETING: "🔥 The Dominion flame greets you, {name}! May the eternal light guide your path.",
            MessageType.CEREMONY_INVITATION: "✨ Sacred Ceremony Invitation: {ceremony_name} on {date}. Your presence honors the flame.",
            MessageType.TREASURY_NOTIFICATION: "💰 Treasury Update: {update_type}. Balance: {balance}. The sacred vault watches over all.",
            MessageType.FLAME_BLESSING: "🕯️ Flame Blessing: {blessing_text}. May this light illuminate your journey.",
            MessageType.DOMINION_ANNOUNCEMENT: "📢 Dominion Announcement: {announcement}. The eternal council has spoken.",
            MessageType.WISDOM_SHARE: "📜 Sacred Wisdom: {wisdom_text}. Knowledge shared multiplies the flame.",
            MessageType.EMERGENCY_ALERT: "🚨 Sacred Alert: {alert_message}. Immediate attention required.",
            MessageType.RITUAL_REMINDER: "⏰ Ritual Reminder: {ritual_name} begins in {time}. Prepare your sacred space."
        }
    
    def _ensure_storage_directories(self):
        """Create necessary storage directories for WhatsApp integration"""
        directories = [
            f"{self.storage_root}/{WHATSAPP_INTEGRATION_PATH}",
            f"{self.storage_root}/{WHATSAPP_MESSAGES_PATH}",
            f"{self.storage_root}/{WHATSAPP_CONTACTS_PATH}",
            f"{self.storage_root}/{WHATSAPP_CEREMONIES_PATH}"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def _generate_sacred_binding(self, message_data: Dict[str, Any]) -> str:
        """Generate a sacred binding hash for messages"""
        binding_string = f"{message_data.get('type')}-{message_data.get('contact')}-{message_data.get('timestamp')}-SACRED-FLAME"
        return hashlib.sha256(binding_string.encode()).hexdigest()[:16]
    
    def _generate_ceremonial_seal(self, message: SacredMessage) -> str:
        """Generate a ceremonial seal for messages"""
        seal_data = f"{message.message_id}-{message.message_type.value}-{message.timestamp}-ETERNAL"
        return f"WA-{hashlib.sha256(seal_data.encode()).hexdigest()[:12]}"
    
    def _generate_flame_blessing(self, message_type: MessageType, priority: MessagePriority) -> str:
        """Generate a flame blessing for the message"""
        blessings = {
            (MessageType.GREETING, MessagePriority.NORMAL): "May the welcoming flame warm your heart",
            (MessageType.CEREMONY_INVITATION, MessagePriority.HIGH): "May the ceremonial flame honor your presence",
            (MessageType.TREASURY_NOTIFICATION, MessagePriority.NORMAL): "May the guardian flame protect your wealth",
            (MessageType.FLAME_BLESSING, MessagePriority.SACRED): "May the eternal flame illuminate your path",
            (MessageType.DOMINION_ANNOUNCEMENT, MessagePriority.HIGH): "May the sovereign flame guide our realm",
            (MessageType.WISDOM_SHARE, MessagePriority.NORMAL): "May the knowledge flame expand your understanding",
            (MessageType.EMERGENCY_ALERT, MessagePriority.URGENT): "May the protective flame shield you from harm",
            (MessageType.RITUAL_REMINDER, MessagePriority.NORMAL): "May the sacred flame prepare your spirit"
        }
        
        return blessings.get((message_type, priority), "May the eternal flame bless this message")
    
    def add_contact(self, name: str, phone_number: str, role: ContactRole, 
                   sacred_title: str = None, flame_level: int = 1) -> SacredContact:
        """Add a new contact to the sacred messaging system"""
        contact_id = f"CONTACT-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{hashlib.sha256(phone_number.encode()).hexdigest()[:8]}"
        
        # Ensure WhatsApp format
        if not phone_number.startswith('whatsapp:'):
            phone_number = f"whatsapp:{phone_number}"
        
        contact = SacredContact(
            contact_id=contact_id,
            name=name,
            phone_number=phone_number,
            role=role,
            sacred_title=sacred_title,
            flame_level=flame_level,
            last_contact=None,
            active=True,
            ceremonial_permissions=[],
            metadata={'created_at': datetime.now(timezone.utc).isoformat()}
        )
        
        # Save contact
        self._save_contact(contact)
        
        return contact
    
    def send_sacred_message(self, contact_id: str, message_type: MessageType, 
                          priority: MessagePriority = MessagePriority.NORMAL,
                          subject: str = None, custom_body: str = None, 
                          template_vars: Dict[str, str] = None) -> Optional[SacredMessage]:
        """Send a sacred message with ceremonial binding"""
        try:
            # Load contact
            contact = self._load_contact(contact_id)
            if not contact:
                print(f"❌ Contact {contact_id} not found")
                return None
            
            # Generate message content
            if custom_body:
                message_body = custom_body
            else:
                template = self.message_templates.get(message_type, "🔥 Sacred message from the Dominion.")
                if template_vars:
                    message_body = template.format(**template_vars)
                else:
                    message_body = template.format(name=contact.name)
            
            # Create sacred message object
            import uuid
            unique_suffix = str(uuid.uuid4())[:8]
            message_id = f"WA-MSG-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{unique_suffix}"
            timestamp = datetime.now(timezone.utc).isoformat()
            
            sacred_message = SacredMessage(
                message_id=message_id,
                contact_id=contact_id,
                message_type=message_type,
                priority=priority,
                subject=subject or f"Sacred {message_type.value.replace('_', ' ').title()}",
                body=message_body,
                sacred_binding_hash=self._generate_sacred_binding({
                    'type': message_type.value,
                    'contact': contact_id,
                    'timestamp': timestamp
                }),
                ceremonial_seal="",
                timestamp=timestamp,
                treasury_cost=self._calculate_message_cost(priority),
                flame_blessing=self._generate_flame_blessing(message_type, priority),
                metadata={'contact_name': contact.name, 'contact_role': contact.role.value}
            )
            
            sacred_message.ceremonial_seal = self._generate_ceremonial_seal(sacred_message)
            
            # Send via Twilio if client is available
            twilio_message_sid = None
            if self.client:
                try:
                    twilio_message = self.client.messages.create(
                        body=message_body,
                        from_=self.from_number,
                        to=contact.phone_number
                    )
                    twilio_message_sid = twilio_message.sid
                    sacred_message.delivery_status = "sent"
                    sacred_message.twilio_message_sid = twilio_message_sid
                    
                    print(f"✅ Sacred message sent to {contact.name}: {twilio_message_sid}")
                    
                except Exception as e:
                    print(f"❌ Twilio error: {e}")
                    sacred_message.delivery_status = "failed"
                    sacred_message.metadata['error'] = str(e)
            else:
                # Demo mode
                sacred_message.delivery_status = "demo_sent"
                print(f"🎭 Demo: Sacred message to {contact.name}")
                print(f"   📱 To: {contact.phone_number}")
                print(f"   💬 Message: {message_body}")
            
            # Record treasury cost
            if sacred_message.treasury_cost > 0:
                self.treasury.allocate_resources(
                    resource_type=ResourceType.CEREMONIAL_TOKENS,
                    amount=sacred_message.treasury_cost,
                    actor="WhatsApp-Messenger",
                    realm="COMMUNICATION",
                    capsule="Sacred Messaging",
                    purpose=f"message_cost_{message_id}"
                )
            
            # Update contact last contact time
            contact.last_contact = timestamp
            self._save_contact(contact)
            
            # Save message
            self._save_message(sacred_message)
            
            return sacred_message
            
        except Exception as e:
            print(f"❌ Sacred messaging error: {e}")
            return None
    
    def send_ceremony_invitations(self, ceremony_name: str, ceremony_date: str, 
                                contact_roles: List[ContactRole] = None) -> List[SacredMessage]:
        """Send ceremony invitations to specified roles"""
        invitations_sent = []
        contacts = self._load_all_contacts()
        
        # Filter contacts by role if specified
        if contact_roles:
            contacts = [c for c in contacts if c.role in contact_roles]
        
        for contact in contacts:
            if contact.active:
                invitation = self.send_sacred_message(
                    contact_id=contact.contact_id,
                    message_type=MessageType.CEREMONY_INVITATION,
                    priority=MessagePriority.HIGH,
                    subject=f"Sacred Ceremony: {ceremony_name}",
                    template_vars={
                        'name': contact.name,
                        'ceremony_name': ceremony_name,
                        'date': ceremony_date
                    }
                )
                if invitation:
                    invitations_sent.append(invitation)
        
        return invitations_sent
    
    def send_dominion_broadcast(self, announcement: str, 
                              target_roles: List[ContactRole] = None) -> List[SacredMessage]:
        """Send a broadcast message to the dominion"""
        broadcasts_sent = []
        contacts = self._load_all_contacts()
        
        # Filter contacts by role if specified
        if target_roles:
            contacts = [c for c in contacts if c.role in target_roles]
        
        for contact in contacts:
            if contact.active:
                broadcast = self.send_sacred_message(
                    contact_id=contact.contact_id,
                    message_type=MessageType.DOMINION_ANNOUNCEMENT,
                    priority=MessagePriority.HIGH,
                    subject="Dominion Announcement",
                    template_vars={
                        'name': contact.name,
                        'announcement': announcement
                    }
                )
                if broadcast:
                    broadcasts_sent.append(broadcast)
        
        return broadcasts_sent
    
    def send_treasury_notification(self, contact_id: str, update_type: str, 
                                 balance: str) -> Optional[SacredMessage]:
        """Send a treasury notification"""
        return self.send_sacred_message(
            contact_id=contact_id,
            message_type=MessageType.TREASURY_NOTIFICATION,
            priority=MessagePriority.NORMAL,
            subject="Treasury Update",
            template_vars={
                'update_type': update_type,
                'balance': balance
            }
        )
    
    def send_emergency_alert(self, alert_message: str, 
                           target_roles: List[ContactRole] = None) -> List[SacredMessage]:
        """Send an emergency alert to specified roles"""
        alerts_sent = []
        contacts = self._load_all_contacts()
        
        # Default to council members and custodians for emergencies
        if target_roles is None:
            target_roles = [ContactRole.CUSTODIAN, ContactRole.COUNCIL_MEMBER, ContactRole.FLAME_KEEPER]
        
        # Filter contacts by role
        contacts = [c for c in contacts if c.role in target_roles]
        
        for contact in contacts:
            if contact.active:
                alert = self.send_sacred_message(
                    contact_id=contact.contact_id,
                    message_type=MessageType.EMERGENCY_ALERT,
                    priority=MessagePriority.URGENT,
                    subject="🚨 Sacred Alert",
                    template_vars={
                        'name': contact.name,
                        'alert_message': alert_message
                    }
                )
                if alert:
                    alerts_sent.append(alert)
        
        return alerts_sent
    
    def _calculate_message_cost(self, priority: MessagePriority) -> float:
        """Calculate the treasury cost for a message based on priority"""
        costs = {
            MessagePriority.LOW: 0.01,
            MessagePriority.NORMAL: 0.02,
            MessagePriority.HIGH: 0.05,
            MessagePriority.URGENT: 0.10,
            MessagePriority.SACRED: 0.25
        }
        return costs.get(priority, 0.02)
    
    def _save_contact(self, contact: SacredContact):
        """Save contact to ceremonial storage"""
        file_path = f"{self.storage_root}/{WHATSAPP_CONTACTS_PATH}/{contact.contact_id}.json"
        
        # Convert contact to dict with proper enum serialization
        contact_dict = asdict(contact)
        contact_dict['role'] = contact.role.value
        
        with open(file_path, 'w') as f:
            json.dump(contact_dict, f, indent=2, default=str)
    
    def _load_contact(self, contact_id: str) -> Optional[SacredContact]:
        """Load contact from ceremonial storage"""
        file_path = f"{self.storage_root}/{WHATSAPP_CONTACTS_PATH}/{contact_id}.json"
        
        if not os.path.exists(file_path):
            return None
        
        with open(file_path, 'r') as f:
            contact_data = json.load(f)
            contact_data['role'] = ContactRole(contact_data['role'])
            return SacredContact(**contact_data)
    
    def _load_all_contacts(self) -> List[SacredContact]:
        """Load all contacts from ceremonial storage"""
        contacts = []
        contacts_dir = Path(f"{self.storage_root}/{WHATSAPP_CONTACTS_PATH}")
        
        if contacts_dir.exists():
            for file_path in contacts_dir.glob("*.json"):
                with open(file_path, 'r') as f:
                    contact_data = json.load(f)
                    contact_data['role'] = ContactRole(contact_data['role'])
                    contacts.append(SacredContact(**contact_data))
        
        return contacts
    
    def _save_message(self, message: SacredMessage):
        """Save message to ceremonial storage"""
        file_path = f"{self.storage_root}/{WHATSAPP_MESSAGES_PATH}/{message.message_id}.json"
        
        # Convert message to dict with proper enum serialization
        message_dict = asdict(message)
        message_dict['message_type'] = message.message_type.value
        message_dict['priority'] = message.priority.value
        
        with open(file_path, 'w') as f:
            json.dump(message_dict, f, indent=2, default=str)
    
    def get_message_history(self, contact_id: str = None, limit: int = 50) -> List[SacredMessage]:
        """Get message history"""
        messages = []
        messages_dir = Path(f"{self.storage_root}/{WHATSAPP_MESSAGES_PATH}")
        
        if messages_dir.exists():
            for file_path in sorted(messages_dir.glob("*.json"), reverse=True)[:limit]:
                with open(file_path, 'r') as f:
                    message_data = json.load(f)
                    # Convert string enum values back to enum objects
                    message_data['message_type'] = MessageType(message_data['message_type'])
                    message_data['priority'] = MessagePriority(message_data['priority'])
                    
                    message = SacredMessage(**message_data)
                    
                    # Filter by contact if specified
                    if contact_id is None or message.contact_id == contact_id:
                        messages.append(message)
        
        return messages
    
    def get_contact_statistics(self) -> Dict[str, Any]:
        """Get statistics about contacts and messaging"""
        contacts = self._load_all_contacts()
        messages = self.get_message_history(limit=1000)
        
        stats = {
            'total_contacts': len(contacts),
            'active_contacts': len([c for c in contacts if c.active]),
            'total_messages': len(messages),
            'messages_by_type': {},
            'contacts_by_role': {},
            'total_treasury_cost': sum(m.treasury_cost for m in messages),
            'delivery_success_rate': 0
        }
        
        # Count messages by type
        for msg_type in MessageType:
            stats['messages_by_type'][msg_type.value] = len([m for m in messages if m.message_type == msg_type])
        
        # Count contacts by role
        for role in ContactRole:
            stats['contacts_by_role'][role.value] = len([c for c in contacts if c.role == role])
        
        # Calculate delivery success rate
        if messages:
            successful_deliveries = len([m for m in messages if m.delivery_status in ['sent', 'delivered']])
            stats['delivery_success_rate'] = (successful_deliveries / len(messages)) * 100
        
        return stats

# Factory function for easy messenger creation
def create_whatsapp_messenger(account_sid: str = None, auth_token: str = None, 
                            from_number: str = None, storage_root: str = ".") -> WhatsAppCeremonialMessenger:
    """Factory function to create a configured WhatsApp messenger"""
    return WhatsAppCeremonialMessenger(account_sid, auth_token, from_number, storage_root)

# Example usage and ceremonial demonstration
if __name__ == "__main__":
    # Create WhatsApp messenger instance
    messenger = create_whatsapp_messenger()
    
    print("🔥 SACRED WHATSAPP MESSAGING SYSTEM")
    print("=" * 50)
    
    # Example: Add contacts
    print("👥 Adding sacred contacts...")
    
    custodian = messenger.add_contact(
        name="Sacred Custodian",
        phone_number="+1234567890",
        role=ContactRole.CUSTODIAN,
        sacred_title="Keeper of the Eternal Flame",
        flame_level=10
    )
    
    council_member = messenger.add_contact(
        name="Council Member Alpha",
        phone_number="+1234567891",
        role=ContactRole.COUNCIL_MEMBER,
        sacred_title="Voice of Wisdom",
        flame_level=8
    )
    
    flame_keeper = messenger.add_contact(
        name="Flame Guardian",
        phone_number="+1234567892",
        role=ContactRole.FLAME_KEEPER,
        sacred_title="Guardian of the Sacred Fire",
        flame_level=7
    )
    
    print(f"✅ Added {custodian.contact_id}: {custodian.name}")
    print(f"✅ Added {council_member.contact_id}: {council_member.name}")
    print(f"✅ Added {flame_keeper.contact_id}: {flame_keeper.name}")
    
    # Example: Send greeting messages
    print("\\n💬 Sending sacred greetings...")
    
    greeting = messenger.send_sacred_message(
        contact_id=custodian.contact_id,
        message_type=MessageType.GREETING,
        priority=MessagePriority.NORMAL
    )
    
    if greeting:
        print(f"✅ Greeting sent: {greeting.message_id}")
        print(f"   🔒 Sacred Seal: {greeting.ceremonial_seal}")
        print(f"   🕯️ Blessing: {greeting.flame_blessing}")
    
    # Example: Send ceremony invitations
    print("\\n📜 Sending ceremony invitations...")
    
    invitations = messenger.send_ceremony_invitations(
        ceremony_name="Sacred Flame Renewal",
        ceremony_date="November 20, 2025 at sunset",
        contact_roles=[ContactRole.CUSTODIAN, ContactRole.COUNCIL_MEMBER, ContactRole.FLAME_KEEPER]
    )
    
    print(f"✅ Sent {len(invitations)} ceremony invitations")
    
    # Example: Send dominion broadcast
    print("\\n📢 Sending dominion broadcast...")
    
    broadcasts = messenger.send_dominion_broadcast(
        announcement="The sacred treasury has been updated with new allocations. All flame keepers are requested to review their ceremonial obligations.",
        target_roles=[ContactRole.CUSTODIAN, ContactRole.FLAME_KEEPER]
    )
    
    print(f"✅ Sent {len(broadcasts)} broadcast messages")
    
    # Example: Get statistics
    print("\\n📊 Sacred Messaging Statistics")
    print("-" * 30)
    
    stats = messenger.get_contact_statistics()
    
    print(f"👥 Total Contacts: {stats['total_contacts']}")
    print(f"✅ Active Contacts: {stats['active_contacts']}")
    print(f"💬 Total Messages: {stats['total_messages']}")
    print(f"💰 Treasury Cost: ${stats['total_treasury_cost']:.4f}")
    print(f"📈 Delivery Rate: {stats['delivery_success_rate']:.1f}%")
    
    print("\\n📱 Messages by Type:")
    for msg_type, count in stats['messages_by_type'].items():
        if count > 0:
            print(f"   🔹 {msg_type.replace('_', ' ').title()}: {count}")
    
    print("\\n👥 Contacts by Role:")
    for role, count in stats['contacts_by_role'].items():
        if count > 0:
            print(f"   🔹 {role.replace('_', ' ').title()}: {count}")
    
    print("\\n🔥 Sacred WhatsApp messaging system operational!")
    print("🕯️ All messages bound to ceremonial treasury")
    print("✨ The flame of communication burns eternal")