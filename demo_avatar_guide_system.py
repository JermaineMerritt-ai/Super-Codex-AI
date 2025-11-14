#!/usr/bin/env python3
"""
🔥 Sacred Avatar Guide System - Complete Demonstration 🔥

This demonstration showcases the complete functionality of the enhanced
Avatar Guide system, from basic avatar creation to complex ceremonial interactions.

The Sacred Avatar Guide system provides:
- Backwards-compatible AvatarGuide class 
- Full-featured SacredAvatarGuide with ceremonial protocols
- AvatarCouncil management for coordinating multiple avatars
- Sacred script system with authority levels and flame blessings
- Persistent storage with hierarchical organization
- Treasury integration with graceful fallback
"""

import tempfile
import time
from pathlib import Path
from avatar_guide_system import (
    AvatarGuide, SacredAvatarGuide, AvatarCouncil, create_sacred_avatar,
    AvatarRole, AvatarPresence, ScriptType
)

def demonstrate_basic_avatar():
    """Demonstrate backwards-compatible AvatarGuide usage"""
    print("🌟 === Demonstrating Basic Avatar Guide (Backwards Compatible) === 🌟")
    print()
    
    # Create a basic avatar (automatically enhanced internally)
    avatar = AvatarGuide("Welcome Guardian", "Greetings, traveler! Welcome to our sacred realm.")
    
    # Use the original simple API
    print("Original speak method:")
    print(avatar.speak())
    print()
    
    # Access enhanced sacred features
    print("Enhanced sacred speak method:")
    print(avatar.sacred_speak())
    print()
    
    # Upgrade to full SacredAvatarGuide functionality
    sacred = avatar.enhance_to_sacred_avatar()
    print(f"Enhanced to: {sacred}")
    print()

def demonstrate_sacred_avatar():
    """Demonstrate full SacredAvatarGuide functionality"""
    print("🔥 === Demonstrating Sacred Avatar Guide === 🔥")
    print()
    
    # Create a temporary directory for demonstration
    demo_dir = Path(tempfile.mkdtemp()) / "sacred_demo"
    
    # Create a sacred avatar with high authority
    custodian = SacredAvatarGuide(
        name="Flame Keeper Aethon",
        role=AvatarRole.CUSTODIAN,
        primary_script="Welcome, seeker of wisdom. I guard the eternal flame.",
        storage_root=demo_dir
    )
    
    print(f"Created: {custodian}")
    print()
    
    # Add various types of scripts
    print("Adding sacred scripts...")
    custodian.add_script(
        "The path to enlightenment requires dedication, {seeker_name}. Walk carefully.",
        ScriptType.GUIDANCE
    )
    
    custodian.add_script(
        "🕯️ May the eternal flame illuminate your journey and bless your endeavors. 🕯️",
        ScriptType.BLESSING
    )
    
    custodian.add_script(
        "Danger approaches, {seeker_name}! The shadows gather. Seek shelter immediately!",
        ScriptType.WARNING
    )
    
    custodian.add_script(
        "In the time of the Fifth Expansion, when {prophecy_element} aligns with {cosmic_force}, great change shall come.",
        ScriptType.PROPHECY
    )
    print("Scripts added successfully!")
    print()
    
    # Activate the avatar
    custodian.activate_presence(AvatarPresence.ACTIVE)
    print(f"Avatar presence activated: {custodian.presence.value}")
    print()
    
    # Demonstrate different speech types
    print("=== Avatar Speech Demonstrations ===")
    
    print("Welcome message:")
    print(custodian.speak(ScriptType.WELCOME))
    print()
    
    print("Personalized guidance:")
    print(custodian.speak(ScriptType.GUIDANCE, seeker_name="Initiate Marcus"))
    print()
    
    print("Sacred blessing:")
    print(custodian.speak(ScriptType.BLESSING))
    print()
    
    print("Warning message:")
    print(custodian.speak(ScriptType.WARNING, seeker_name="Brave Soul"))
    print()
    
    print("Prophetic vision:")
    print(custodian.speak(ScriptType.PROPHECY, prophecy_element="the crimson star", cosmic_force="the sacred flame"))
    print()
    
    # Demonstrate flame blessings
    print("=== Flame Blessing Demonstration ===")
    custodian.receive_flame_blessing(ScriptType.BLESSING)
    
    print("After receiving flame blessing:")
    print(custodian.speak(ScriptType.BLESSING))
    print()
    
    # Show avatar status
    status = custodian.get_avatar_status()
    print("=== Avatar Status ===")
    for key, value in status.items():
        print(f"{key}: {value}")
    print()
    
    # Save the avatar profile
    custodian.save_avatar_profile()
    print(f"Avatar profile saved to: {custodian.storage_root / 'avatars' / f'{custodian.name}.json'}")
    print()

def demonstrate_avatar_council():
    """Demonstrate AvatarCouncil management"""
    print("🏛️ === Demonstrating Avatar Council Management === 🏛️")
    print()
    
    # Create council with temporary storage
    council_dir = Path(tempfile.mkdtemp()) / "council_demo"
    council = AvatarCouncil(storage_root=council_dir)
    
    print("Council established!")
    print()
    
    # Summon avatars with different roles
    print("Summoning council members...")
    
    keeper = council.summon_avatar(
        "Pyrion the Eternal",
        AvatarRole.FLAME_KEEPER,
        "The eternal flame burns bright in my keeping."
    )
    
    guardian = council.summon_avatar(
        "Valeria Storm-Shield", 
        AvatarRole.GUARDIAN,
        "I stand watch over the sacred grounds."
    )
    
    sage = council.summon_avatar(
        "Elder Theron",
        AvatarRole.WISDOM_BEARER,
        "Wisdom flows through the ages, and I am its vessel."
    )
    
    council_member = council.summon_avatar(
        "Council Speaker Lyra",
        AvatarRole.COUNCIL_MEMBER,
        "I speak with the voice of the assembled council."
    )
    
    print(f"Summoned {len(council.avatars)} avatars to the council")
    print()
    
    # Add ceremonial scripts to avatars
    print("Preparing ceremonial scripts...")
    for avatar in council.avatars.values():
        avatar.add_script(
            f"I, {avatar.name}, participate in this {'{ceremony_name}'} with sacred intent.",
            ScriptType.CEREMONY
        )
        avatar.add_script(
            f"As {avatar.role.value}, I offer this blessing for {'{blessing_target}'}.",
            ScriptType.BLESSING
        )
    print("Ceremonial scripts prepared!")
    print()
    
    # Conduct a sacred ceremony
    print("=== Conducting Sacred Ceremony ===")
    ceremony_name = "Blessing of the New Initiates"
    council.conduct_ceremony(ceremony_name)
    print()
    
    # Apply flame blessings to the ceremonial scripts
    print("=== Applying Flame Blessings ===")
    for avatar in council.avatars.values():
        avatar.receive_flame_blessing(ScriptType.CEREMONY)
        print(f"✨ {avatar.name} received ceremonial flame blessing")
    print()
    
    # Show council status
    status = council.get_council_status()
    print("=== Council Status ===")
    print(f"Total Avatars: {status['total_avatars']}")
    print(f"Council Storage: {status['council_storage']}")
    print("Role Distribution:")
    for role, count in status['role_distribution'].items():
        if count > 0:
            print(f"  {role}: {count}")
    print()
    
    # Save all avatar profiles
    print("Saving council member profiles...")
    for avatar in council.avatars.values():
        avatar.save_avatar_profile()
    print("All profiles saved!")
    print()

def demonstrate_factory_function():
    """Demonstrate the factory function for creating avatars"""
    print("🏭 === Demonstrating Avatar Factory Function === 🏭")
    print()
    
    # Create various avatars using the factory function
    demo_dir = Path(tempfile.mkdtemp()) / "factory_demo"
    
    avatars = []
    
    # Valid roles
    valid_configs = [
        ("Herald Magnus", "herald", "Hear ye! I bring tidings from the sacred council."),
        ("Guardian Sentinel", "guardian", "None shall pass without proper authorization."),
        ("Initiate Luna", "initiate", "I am new to the sacred ways. Please guide me."),
        ("Flame Keeper Ignis", "flame_keeper", "The sacred flame never dies while I tend it.")
    ]
    
    print("Creating avatars with various roles:")
    for name, role, script in valid_configs:
        avatar = create_sacred_avatar(name, role, script, storage_root=demo_dir)
        avatars.append(avatar)
        print(f"✅ Created: {name} as {role}")
    
    # Invalid role (demonstrates fallback)
    print("\nTesting invalid role fallback:")
    invalid_avatar = create_sacred_avatar(
        "Test Avatar",
        "invalid_role_name",
        "This will default to initiate role.",
        storage_root=demo_dir
    )
    print(f"✅ Invalid role defaulted to: {invalid_avatar.role.value}")
    print()
    
    # Demonstrate each avatar
    print("=== Factory-Created Avatar Demonstrations ===")
    for avatar in avatars:
        print(f"\n{avatar.name} ({avatar.role.value}) speaks:")
        print(avatar.speak(ScriptType.WELCOME))

def demonstrate_advanced_features():
    """Demonstrate advanced ceremonial features"""
    print("⚡ === Demonstrating Advanced Ceremonial Features === ⚡")
    print()
    
    # Create a high-authority avatar
    demo_dir = Path(tempfile.mkdtemp()) / "advanced_demo"
    master = SacredAvatarGuide(
        name="Grand Master Solarius",
        role=AvatarRole.CUSTODIAN,
        primary_script="I am the keeper of the highest mysteries.",
        storage_root=demo_dir
    )
    
    # Add scripts with different authority levels
    print("Creating scripts with various authority levels...")
    
    master.add_script("Welcome, traveler.", ScriptType.WELCOME, authority_level=3)
    master.add_script("Seek the wisdom within.", ScriptType.GUIDANCE, authority_level=7)
    master.add_script("By the power of the eternal flame, be blessed!", ScriptType.BLESSING, authority_level=10)
    
    # Show how authority affects presentation
    print("\n=== Authority Level Demonstrations ===")
    print("Low authority welcome:")
    print(master.speak(ScriptType.WELCOME))
    print()
    
    print("Medium authority guidance:")
    print(master.speak(ScriptType.GUIDANCE))
    print()
    
    print("High authority blessing:")
    print(master.speak(ScriptType.BLESSING))
    print()
    
    # Demonstrate presence state changes
    print("=== Presence State Demonstrations ===")
    states_to_demo = [AvatarPresence.MEDITATION, AvatarPresence.BLESSING, AvatarPresence.ASCENDING]
    
    for state in states_to_demo:
        master.activate_presence(state)
        print(f"Avatar presence: {state.value}")
        print(f"Status: {master.get_avatar_status()['presence']}")
        print()

def main():
    """Run the complete demonstration"""
    print("🔥" * 60)
    print("🔥" + " " * 16 + "SACRED AVATAR GUIDE SYSTEM" + " " * 16 + "🔥")
    print("🔥" + " " * 19 + "COMPLETE DEMONSTRATION" + " " * 19 + "🔥")
    print("🔥" * 60)
    print()
    
    try:
        # Run all demonstrations
        demonstrate_basic_avatar()
        print("─" * 80)
        
        demonstrate_sacred_avatar()
        print("─" * 80)
        
        demonstrate_avatar_council()
        print("─" * 80)
        
        demonstrate_factory_function()
        print("─" * 80)
        
        demonstrate_advanced_features()
        print("─" * 80)
        
        print("🎉" * 20)
        print("🎉" + " " * 16 + "DEMONSTRATION COMPLETE!" + " " * 17 + "🎉")
        print("🎉" + " " * 14 + "The Sacred Avatar System Lives!" + " " * 14 + "🎉")
        print("🎉" * 20)
        print()
        print("✨ All features demonstrated successfully! ✨")
        print("The eternal flame burns bright in the Sacred Avatar Guide system.")
        print()
        
    except Exception as e:
        print(f"❌ Demonstration encountered an error: {e}")
        raise

if __name__ == "__main__":
    main()