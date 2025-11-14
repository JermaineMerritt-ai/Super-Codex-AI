#!/usr/bin/env python3
"""
WhatsApp Integration Demonstration
Sacred Messaging System for the Dominion
"""

import tempfile
import shutil
from whatsapp_integration import (
    create_whatsapp_messenger, ContactRole, MessageType, MessagePriority
)


def whatsapp_sacred_demonstration():
    """Demonstrate the WhatsApp sacred messaging integration"""
    
    print("🔥" + "="*60 + "🔥")
    print("   SACRED WHATSAPP MESSAGING DEMONSTRATION")
    print("   Ceremonial Communication for the Dominion")
    print("🔥" + "="*60 + "🔥\n")
    
    # Create temporary storage for demo
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Create WhatsApp messenger instance
        print("🌟 Initializing Sacred WhatsApp Messenger...")
        messenger = create_whatsapp_messenger(storage_root=temp_dir)
        print("✅ WhatsApp messenger initialized with ceremonial treasury\n")
        
        # Add ceremonial contacts
        print("📋 Adding Sacred Contacts...")
        custodian = messenger.add_contact(
            name="Sacred Custodian",
            phone_number="+1234567890",
            role=ContactRole.CUSTODIAN
        )
        print(f"   ✅ {custodian.name} added (Role: {custodian.role.value})")
        
        council_member = messenger.add_contact(
            name="Council Elder",
            phone_number="+1987654321", 
            role=ContactRole.COUNCIL_MEMBER
        )
        print(f"   ✅ {council_member.name} added (Role: {council_member.role.value})")
        
        flame_keeper = messenger.add_contact(
            name="Flame Keeper Aria",
            phone_number="+1555123456",
            role=ContactRole.FLAME_KEEPER
        )
        print(f"   ✅ {flame_keeper.name} added (Role: {flame_keeper.role.value})")
        
        wisdom_seeker = messenger.add_contact(
            name="Wisdom Seeker Neo",
            phone_number="+1333444555",
            role=ContactRole.WISDOM_SEEKER
        )
        print(f"   ✅ {wisdom_seeker.name} added (Role: {wisdom_seeker.role.value})\n")
        
        # Demonstrate different message types
        print("💬 Demonstrating Sacred Message Types...")
        
        # 1. Greeting message
        print("\n   🔥 GREETING MESSAGE:")
        greeting = messenger.send_sacred_message(
            contact_id=custodian.contact_id,
            message_type=MessageType.GREETING,
            priority=MessagePriority.NORMAL
        )
        
        # 2. Flame blessing with custom content
        print("\n   🕯️  FLAME BLESSING:")
        blessing = messenger.send_sacred_message(
            contact_id=flame_keeper.contact_id,
            message_type=MessageType.FLAME_BLESSING,
            priority=MessagePriority.SACRED,
            template_vars={'blessing_text': 'May the eternal flame illuminate your noble path of service'}
        )
        
        # 3. Treasury notification
        print("\n   💰 TREASURY NOTIFICATION:")
        treasury_update = messenger.send_sacred_message(
            contact_id=council_member.contact_id,
            message_type=MessageType.TREASURY_NOTIFICATION,
            priority=MessagePriority.HIGH,
            template_vars={'update_type': 'Monthly Report', 'balance': '15,250.75 Sacred Tokens'}
        )
        
        # 4. Wisdom sharing
        print("\n   📜 WISDOM SHARE:")
        wisdom = messenger.send_sacred_message(
            contact_id=wisdom_seeker.contact_id,
            message_type=MessageType.WISDOM_SHARE,
            priority=MessagePriority.NORMAL,
            template_vars={'wisdom_text': 'The flame burns brightest when shared among many hearts'}
        )
        
        # 5. Custom message body
        print("\n   🎭 CUSTOM MESSAGE:")
        custom = messenger.send_sacred_message(
            contact_id=custodian.contact_id,
            message_type=MessageType.DOMINION_ANNOUNCEMENT,
            priority=MessagePriority.HIGH,
            custom_body="🏛️ The Dominion Council announces: New ceremonial protocols are now in effect. All rituals must include the sacred flame blessing. May the eternal light guide our path."
        )
        
        # Demonstrate ceremony invitations
        print("\n\n📨 CEREMONY INVITATION BROADCAST:")
        invitations = messenger.send_ceremony_invitations(
            ceremony_name="Winter Solstice Sacred Flame Renewal",
            ceremony_date="December 21, 2025",
            contact_roles=[ContactRole.CUSTODIAN, ContactRole.COUNCIL_MEMBER, ContactRole.FLAME_KEEPER]
        )
        print(f"   📤 Sent {len(invitations)} ceremonial invitations")
        
        # Demonstrate emergency alert
        print("\n\n🚨 EMERGENCY ALERT SYSTEM:")
        emergency_contacts = messenger.send_emergency_alert(
            alert_message="Sacred flame requires immediate tending - gather at the central sanctum",
            target_roles=[ContactRole.CUSTODIAN, ContactRole.FLAME_KEEPER]
        )
        print(f"   🚨 Emergency alert sent to {len(emergency_contacts)} essential personnel")
        
        # Demonstrate dominion broadcast
        print("\n\n📢 DOMINION WIDE BROADCAST:")
        broadcast_results = messenger.send_dominion_broadcast(
            announcement="Monthly sacred flame ceremony completed successfully. Next gathering: New Moon cycle."
        )
        print(f"   📡 Broadcast sent to all {len(broadcast_results)} contacts")
        
        # Display statistics
        print("\n\n📊 SACRED MESSAGING STATISTICS:")
        stats = messenger.get_contact_statistics()
        print(f"   👥 Total Contacts: {stats['total_contacts']}")
        print(f"   📱 Active Contacts: {stats['active_contacts']}")
        print(f"   💬 Total Messages: {stats['total_messages']}")
        print(f"   💰 Treasury Cost: {stats['total_treasury_cost']:.2f} Sacred Tokens")
        print(f"   📈 Delivery Success Rate: {stats['delivery_success_rate']:.1f}%")
        
        print("\n   📋 Messages by Type:")
        for msg_type, count in stats['messages_by_type'].items():
            if count > 0:
                print(f"      {msg_type.replace('_', ' ').title()}: {count}")
        
        print("\n   👤 Contacts by Role:")
        for role, count in stats['contacts_by_role'].items():
            if count > 0:
                print(f"      {role.replace('_', ' ').title()}: {count}")
        
        # Display recent message history
        print("\n\n📚 RECENT MESSAGE HISTORY:")
        recent_messages = messenger.get_message_history(limit=5)
        for i, msg in enumerate(recent_messages[:3]):  # Show first 3
            print(f"   📝 Message {i+1}: {msg.message_type.value} to contact {msg.contact_id[:8]}...")
            print(f"      Status: {msg.delivery_status} | Cost: {msg.treasury_cost} tokens")
            print(f"      Blessing: {msg.flame_blessing}")
        
        if len(recent_messages) > 3:
            print(f"   ... and {len(recent_messages) - 3} more messages")
        
        print("\n" + "🕯️" + "="*60 + "🕯️")
        print("   SACRED WHATSAPP DEMONSTRATION COMPLETE")
        print("   May the eternal flame illuminate all communications")
        print("🕯️" + "="*60 + "🕯️")
        
    except Exception as e:
        print(f"❌ Sacred messaging error: {e}")
        
    finally:
        # Cleanup temporary files
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    whatsapp_sacred_demonstration()