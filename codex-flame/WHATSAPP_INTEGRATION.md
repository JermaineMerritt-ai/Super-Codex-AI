# WhatsApp Integration Documentation
## Sacred Messaging System for the Dominion

### Overview
The WhatsApp Integration provides a sacred messaging system that bridges the Dominion's ceremonial architecture with Twilio's WhatsApp Business API. This system enables ceremonial communication with role-based messaging, treasury cost tracking, and sacred binding verification.

### Architecture

#### Core Components
- **WhatsAppCeremonialMessenger**: Main messaging class with treasury integration
- **SacredMessage**: Dataclass for structured ceremonial messages
- **SacredContact**: Dataclass for contact management with roles
- **Ceremonial Treasury Integration**: Resource allocation and cost tracking
- **Sacred Binding System**: Cryptographic verification for message authenticity

#### File Structure
```
codex-flame/
├── whatsapp_integration.py      # Main integration module
├── test_whatsapp_integration.py # Comprehensive test suite
├── whatsapp_demo.py            # Interactive demonstration
└── debug_whatsapp.py           # Debug utilities
```

### Key Features

#### 🔥 Sacred Message Types
- **GREETING**: Welcome messages with flame blessings
- **CEREMONY_INVITATION**: Formal ceremonial invitations
- **TREASURY_NOTIFICATION**: Financial updates and balance reports  
- **FLAME_BLESSING**: Spiritual blessings and light ceremonies
- **DOMINION_ANNOUNCEMENT**: Official proclamations and decrees
- **WISDOM_SHARE**: Knowledge distribution and teaching content
- **EMERGENCY_ALERT**: Urgent notifications requiring immediate attention
- **RITUAL_REMINDER**: Sacred ceremony and ritual notifications

#### 👤 Contact Roles
- **CUSTODIAN**: Sacred guardians and administrators
- **COUNCIL_MEMBER**: Governing council representatives  
- **FLAME_KEEPER**: Spiritual guides and ceremony leaders
- **WISDOM_SEEKER**: Students and knowledge recipients
- **HERALD**: Message broadcasters and communicators
- **GUARDIAN**: Security and protection personnel

#### 📊 Message Priorities & Costs
- **LOW**: 0.02 Sacred Tokens - Basic notifications
- **NORMAL**: 0.05 Sacred Tokens - Standard communications  
- **HIGH**: 0.08 Sacred Tokens - Important announcements
- **URGENT**: 0.12 Sacred Tokens - Critical alerts
- **SACRED**: 0.15 Sacred Tokens - Ceremonial messages

### Installation & Setup

#### Prerequisites
```bash
# Install Twilio SDK for full functionality
pip install twilio

# Or use demo mode (no external dependencies)
# Demo mode automatically activates when Twilio is unavailable
```

#### Basic Configuration
```python
from whatsapp_integration import create_whatsapp_messenger

# With Twilio credentials (production)
messenger = create_whatsapp_messenger(
    account_sid="your_twilio_account_sid",
    auth_token="your_twilio_auth_token", 
    from_number="whatsapp:+1234567890",
    storage_root="/path/to/storage"
)

# Demo mode (development/testing)
messenger = create_whatsapp_messenger(
    storage_root="/path/to/storage"
)
```

### Usage Examples

#### Contact Management
```python
# Add ceremonial contact
custodian = messenger.add_contact(
    name="Sacred Custodian",
    phone_number="+1234567890",
    role=ContactRole.CUSTODIAN
)

# Load existing contact
contact = messenger.load_contact(custodian.contact_id)

# Get all contacts
all_contacts = messenger.load_all_contacts()
```

#### Sacred Messaging
```python
# Basic greeting
greeting = messenger.send_sacred_message(
    contact_id=contact.contact_id,
    message_type=MessageType.GREETING,
    priority=MessagePriority.NORMAL
)

# Custom message with template variables
blessing = messenger.send_sacred_message(
    contact_id=contact.contact_id,
    message_type=MessageType.FLAME_BLESSING,
    priority=MessagePriority.SACRED,
    template_vars={'blessing_text': 'May eternal light guide your path'}
)

# Custom message body
announcement = messenger.send_sacred_message(
    contact_id=contact.contact_id,
    message_type=MessageType.DOMINION_ANNOUNCEMENT,
    priority=MessagePriority.HIGH,
    custom_body="🏛️ New ceremonial protocols now in effect"
)
```

#### Broadcast Communications
```python
# Ceremony invitations to specific roles
invitations = messenger.send_ceremony_invitations(
    ceremony_name="Winter Solstice Renewal",
    ceremony_date="December 21, 2025",
    contact_roles=[ContactRole.CUSTODIAN, ContactRole.COUNCIL_MEMBER]
)

# Emergency alerts
alerts = messenger.send_emergency_alert(
    alert_message="Sacred flame requires immediate attention",
    target_roles=[ContactRole.CUSTODIAN, ContactRole.FLAME_KEEPER]
)

# Domain-wide announcements
broadcast = messenger.send_dominion_broadcast(
    announcement="Monthly ceremony completed successfully"
)
```

#### Treasury & Statistics
```python
# Get messaging statistics
stats = messenger.get_contact_statistics()
print(f"Total Messages: {stats['total_messages']}")
print(f"Treasury Cost: {stats['total_treasury_cost']} Sacred Tokens")
print(f"Success Rate: {stats['delivery_success_rate']}%")

# Message history
recent_messages = messenger.get_message_history(limit=10)
contact_messages = messenger.get_message_history(contact_id=contact.contact_id)
```

### Message Templates

The system includes built-in templates for each message type:

```python
# Template examples with variables
templates = {
    MessageType.GREETING: "🔥 The Dominion flame greets you, {name}!",
    MessageType.CEREMONY_INVITATION: "✨ Sacred Ceremony: {ceremony_name} on {date}",
    MessageType.TREASURY_NOTIFICATION: "💰 Treasury Update: {update_type}. Balance: {balance}",
    MessageType.FLAME_BLESSING: "🕯️ Flame Blessing: {blessing_text}",
    MessageType.EMERGENCY_ALERT: "🚨 Sacred Alert: {alert_message}",
    # ... additional templates
}
```

### Sacred Architecture

#### Ceremonial Binding
Each message includes cryptographic binding:
```python
sacred_binding = messenger._generate_sacred_binding({
    'type': message_type.value,
    'contact': contact_id,
    'timestamp': timestamp
})
```

#### Treasury Integration
Messages automatically deduct costs from ceremonial treasury:
```python
treasury_cost = messenger._calculate_message_cost(priority)
treasury.allocate_resources(
    resource_type=ResourceType.CEREMONIAL_TOKENS,
    amount=treasury_cost,
    actor="WhatsApp-Messenger",
    purpose=f"message_cost_{message_id}"
)
```

#### Flame Blessings
Each message receives a contextual blessing:
```python
blessing = messenger._generate_flame_blessing(message_type, priority)
# Example: "May the eternal flame illuminate your path"
```

### Testing

#### Running Tests
```bash
# Run comprehensive test suite
python test_whatsapp_integration.py

# Run specific test category
python -m unittest TestWhatsAppIntegration.test_send_sacred_message_demo_mode
```

#### Test Coverage
- ✅ Contact management (add, store, retrieve, formatting)
- ✅ Message sending (all types, priorities, custom content) 
- ✅ Template system and variable substitution
- ✅ Ceremonial binding and seal generation
- ✅ Treasury cost calculation and allocation
- ✅ Error handling and demo mode fallbacks
- ✅ Statistics and reporting functionality
- ✅ Broadcast communications
- ✅ Message history and persistence
- ✅ Enum serialization/deserialization

### Demo Mode

When Twilio SDK is unavailable, the system automatically operates in demo mode:

```
📱 Twilio SDK not installed - running in demo mode
   To enable full functionality, install with: pip install twilio

🎭 Demo: Sacred message to Contact Name
   📱 To: whatsapp:+1234567890
   💬 Message: [message content]
```

Demo mode provides:
- Full functionality testing without external dependencies
- Visual message preview and routing information
- Treasury cost tracking and ceremonial binding generation
- Contact management and statistics
- All ceremonial features except actual message delivery

### Error Handling

The system provides graceful error handling:

```python
try:
    message = messenger.send_sacred_message(contact_id, message_type, priority)
    if message:
        print(f"✅ Message sent: {message.message_id}")
    else:
        print("❌ Message failed to send")
except Exception as e:
    print(f"❌ Sacred messaging error: {e}")
```

Error scenarios handled:
- Missing Twilio SDK (demo mode activation)
- Invalid contact IDs
- Twilio API failures
- Network connectivity issues
- Invalid template variables
- Storage permissions

### Security Features

#### Sacred Binding Verification
Messages include SHA-256 based sacred binding for authenticity verification.

#### Ceremonial Seals
Each message receives a unique ceremonial seal combining:
- Message metadata
- Contact information  
- Timestamp
- Sacred binding hash

#### Role-Based Access
Contact roles determine:
- Message type permissions
- Priority level access
- Broadcast eligibility
- Emergency alert routing

### Performance Considerations

#### Storage Management
- Messages stored as individual JSON files
- Contacts cached in memory with persistent storage
- Treasury allocations logged for audit trails

#### Rate Limiting
- Built-in message cost system discourages spam
- Priority-based resource allocation
- Treasury balance enforcement

#### Scalability
- Stateless message sending
- Independent contact management
- Configurable storage paths
- Minimal memory footprint

### Troubleshooting

#### Common Issues
1. **Twilio Import Error**: Install Twilio SDK or use demo mode
2. **Template Variable Missing**: Provide all required template variables
3. **Contact Not Found**: Verify contact ID and storage permissions
4. **Storage Permission**: Ensure write access to storage directory

#### Debug Tools
```bash
# Run debug script for detailed analysis
python debug_whatsapp.py

# Enable verbose logging in messenger
messenger.enable_debug_logging = True
```

### Future Enhancements

#### Planned Features
- Message scheduling and delayed delivery
- Rich media support (images, documents)
- Group messaging for ceremonial circles
- Integration with external calendar systems
- Advanced analytics and reporting
- Message encryption for sensitive communications

### Integration Points

#### Treasury System
Automatic integration with ceremonial treasury for:
- Resource allocation tracking
- Cost management
- Audit trail generation

#### Sacred Storage
Persistent storage using:
- JSON-based message archives
- Contact database management  
- Ceremonial binding verification
- Audit log maintenance

### Support & Documentation

For additional support:
- Review test files for usage examples
- Run demo script for interactive exploration
- Check debug output for troubleshooting
- Examine source code for detailed implementation

May the eternal flame illuminate all sacred communications! 🔥🕯️