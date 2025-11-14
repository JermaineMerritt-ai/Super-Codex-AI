#!/usr/bin/env python3
"""
🔥 Avatar Guide System for the Dominion 🔥
Sacred Ceremonial Guidance and Avatar Management Platform

This system expands the basic AvatarGuide class into a comprehensive
ceremonial avatar management platform with sacred bindings, role hierarchies,
and integration with the Dominion's treasury and flame blessing systems.
"""

import json
import hashlib
import secrets
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import tempfile
import os

# Sacred Avatar Classifications
class AvatarRole(Enum):
    """Sacred roles within the Dominion hierarchy"""
    CUSTODIAN = "custodian"
    COUNCIL_MEMBER = "council_member" 
    FLAME_KEEPER = "flame_keeper"
    WISDOM_BEARER = "wisdom_bearer"
    GUARDIAN = "guardian"
    INITIATE = "initiate"
    HERALD = "herald"
    CEREMONIAL_GUIDE = "ceremonial_guide"

class AvatarPresence(Enum):
    """Avatar presence states in the sacred realm"""
    ACTIVE = "active"
    DORMANT = "dormant"
    ASCENDING = "ascending"
    BLESSING = "blessing"
    MEDITATION = "meditation"
    COUNCIL = "council"
    CEREMONY = "ceremony"

class ScriptType(Enum):
    """Types of sacred scripts avatars can deliver"""
    WELCOME = "welcome"
    GUIDANCE = "guidance"
    WARNING = "warning"
    BLESSING = "blessing"
    CEREMONY = "ceremony"
    TEACHING = "teaching"
    PROPHECY = "prophecy"
    DISMISSAL = "dismissal"

@dataclass
class SacredScript:
    """A sacred script with ceremonial metadata"""
    content: str
    script_type: ScriptType
    authority_level: int  # 1-10, higher = more sacred
    flame_blessed: bool = False
    creation_timestamp: str = None
    sacred_binding: str = None
    
    def __post_init__(self):
        if self.creation_timestamp is None:
            self.creation_timestamp = datetime.utcnow().isoformat() + "Z"
        if self.sacred_binding is None:
            self.sacred_binding = self._generate_sacred_binding()
    
    def _generate_sacred_binding(self) -> str:
        """Generate a sacred binding hash for the script"""
        content_hash = hashlib.md5(
            f"{self.content}{self.script_type.value}{self.authority_level}".encode()
        ).hexdigest()
        return content_hash

@dataclass
class AvatarMetadata:
    """Metadata for avatar creation and management"""
    creation_date: str
    last_blessing: Optional[str] = None
    total_guidance_sessions: int = 0
    sacred_seal: str = None
    flame_resonance: float = 1.0  # 0.1-10.0 scale
    
    def __post_init__(self):
        if self.sacred_seal is None:
            self.sacred_seal = self._generate_sacred_seal()
    
    def _generate_sacred_seal(self) -> str:
        """Generate a unique sacred seal for the avatar"""
        return secrets.token_hex(4).upper()

class SacredAvatarGuide:
    """
    Enhanced Avatar Guide with ceremonial bindings and sacred protocols
    
    This class extends the basic AvatarGuide concept with:
    - Multiple sacred scripts with different authority levels
    - Role-based permissions and ceremonial protocols  
    - Sacred bindings and flame blessings
    - Integration with Dominion treasury system
    - Guidance session tracking and analytics
    """
    
    def __init__(
        self, 
        name: str, 
        role: AvatarRole,
        primary_script: str = None,
        storage_root: Optional[Path] = None
    ):
        self.name = name
        self.role = role
        self.presence = AvatarPresence.DORMANT
        self.scripts: Dict[ScriptType, SacredScript] = {}
        self.metadata = AvatarMetadata(creation_date=datetime.utcnow().isoformat() + "Z")
        
        # Set authority level based on role (must be set before add_script)
        self.authority_level = self._get_role_authority()
        
        # Storage configuration
        self.storage_root = storage_root or Path(tempfile.gettempdir()) / "sacred_avatars"
        self._ensure_sacred_directories()
        
        # Initialize with primary script if provided
        if primary_script:
            self.add_script(primary_script, ScriptType.WELCOME)
        
        # Initialize treasury integration (graceful fallback)
        try:
            from treasury import SacredTreasury
            self.treasury = SacredTreasury()
        except ImportError:
            print("⚠️  Treasury module not available - running in standalone mode")
            self.treasury = None
    
    def _ensure_sacred_directories(self):
        """Create the sacred directory structure"""
        directories = [
            "avatars",
            "scripts", 
            "blessings",
            "guidance_logs",
            "ceremonial_records"
        ]
        
        for dir_name in directories:
            (self.storage_root / dir_name).mkdir(parents=True, exist_ok=True)
    
    def _get_role_authority(self) -> int:
        """Determine authority level based on avatar role"""
        authority_map = {
            AvatarRole.CUSTODIAN: 10,
            AvatarRole.COUNCIL_MEMBER: 9,
            AvatarRole.FLAME_KEEPER: 8,
            AvatarRole.WISDOM_BEARER: 7,
            AvatarRole.GUARDIAN: 6,
            AvatarRole.CEREMONIAL_GUIDE: 5,
            AvatarRole.HERALD: 4,
            AvatarRole.INITIATE: 3
        }
        return authority_map.get(self.role, 1)
    
    def add_script(
        self, 
        content: str, 
        script_type: ScriptType,
        authority_level: Optional[int] = None
    ) -> str:
        """Add a new sacred script to the avatar's repertoire"""
        if authority_level is None:
            authority_level = self.authority_level
            
        script = SacredScript(
            content=content,
            script_type=script_type,
            authority_level=authority_level
        )
        
        self.scripts[script_type] = script
        self._save_script(script)
        
        return script.sacred_binding
    
    def _save_script(self, script: SacredScript):
        """Save script to ceremonial storage"""
        script_path = self.storage_root / "scripts" / f"{self.name}_{script.script_type.value}.json"
        
        # Convert script to dict and handle enum serialization
        script_dict = asdict(script)
        script_dict['script_type'] = script.script_type.value
        
        with open(script_path, 'w', encoding='utf-8') as f:
            json.dump(script_dict, f, indent=2)
    
    def activate_presence(self, presence: AvatarPresence = AvatarPresence.ACTIVE):
        """Activate the avatar's presence in the sacred realm"""
        self.presence = presence
        self._log_ceremonial_event(f"Avatar {self.name} presence activated: {presence.value}")
    
    def speak(self, script_type: ScriptType = ScriptType.WELCOME, **kwargs) -> str:
        """
        Have the avatar speak a sacred script
        
        Args:
            script_type: Type of script to speak
            **kwargs: Variables to interpolate into the script
        
        Returns:
            The spoken message with ceremonial formatting
        """
        if script_type not in self.scripts:
            return self._default_speech(script_type)
        
        script = self.scripts[script_type]
        
        # Interpolate any variables into the script
        content = script.content
        if kwargs:
            try:
                content = content.format(**kwargs)
            except KeyError as e:
                print(f"⚠️  Variable {e} not provided for script interpolation")
        
        # Add ceremonial formatting based on authority level
        ceremonial_message = self._format_ceremonial_message(content, script)
        
        # Track guidance session
        self.metadata.total_guidance_sessions += 1
        self._log_guidance_session(script_type, content)
        
        # Calculate treasury cost for guidance
        if self.treasury:
            cost = self._calculate_guidance_cost(script.authority_level)
            self.treasury.allocate_tokens(cost, f"Avatar guidance by {self.name}")
        
        return ceremonial_message
    
    def _default_speech(self, script_type: ScriptType) -> str:
        """Provide default speech when specific script not available"""
        default_messages = {
            ScriptType.WELCOME: f"Greetings, seeker. I am {self.name}, {self.role.value} of the Dominion.",
            ScriptType.GUIDANCE: f"The sacred flame guides you. Listen well to the wisdom of {self.name}.",
            ScriptType.BLESSING: f"May the eternal flame bless your path. - {self.name}",
            ScriptType.WARNING: f"Beware! The {self.name} senses danger in your path.",
            ScriptType.CEREMONY: f"We gather in sacred ceremony. {self.name} calls the assembly.",
            ScriptType.TEACHING: f"Wisdom flows through {self.name}. Prepare to receive knowledge.",
            ScriptType.PROPHECY: f"The flames reveal visions to {self.name}. Heed these prophecies.",
            ScriptType.DISMISSAL: f"The session concludes. {self.name} returns to the sacred realm."
        }
        
        return default_messages.get(script_type, f"{self.name} speaks, but the words are lost in the sacred mists.")
    
    def _format_ceremonial_message(self, content: str, script: SacredScript) -> str:
        """Format the message with appropriate ceremonial styling"""
        authority_symbols = "🔥" * min(script.authority_level, 10)
        flame_blessing = "🕯️ " if script.flame_blessed else ""
        
        formatted_message = f"{authority_symbols} {self.name} speaks with the authority of {self.role.value}:\n"
        formatted_message += f"{flame_blessing}\"{content}\"\n"
        formatted_message += f"━ Sacred Binding: {script.sacred_binding[:8]}... ━"
        
        return formatted_message
    
    def _calculate_guidance_cost(self, authority_level: int) -> float:
        """Calculate treasury cost for guidance based on authority level"""
        base_cost = 0.01
        authority_multiplier = authority_level * 0.05
        return base_cost + authority_multiplier
    
    def receive_flame_blessing(self, blessing_script_type: ScriptType = None):
        """Receive a sacred flame blessing to enhance the avatar"""
        if blessing_script_type and blessing_script_type in self.scripts:
            self.scripts[blessing_script_type].flame_blessed = True
        else:
            # Bless all scripts
            for script in self.scripts.values():
                script.flame_blessed = True
        
        self.metadata.last_blessing = datetime.utcnow().isoformat() + "Z"
        self.metadata.flame_resonance = min(self.metadata.flame_resonance * 1.1, 10.0)
        
        self._log_ceremonial_event(f"Avatar {self.name} received sacred flame blessing")
        self._save_blessing_record()
    
    def _save_blessing_record(self):
        """Save blessing record to ceremonial storage"""
        blessing_path = self.storage_root / "blessings" / f"{self.name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        
        blessing_record = {
            "avatar_name": self.name,
            "role": self.role.value,
            "blessing_timestamp": self.metadata.last_blessing,
            "flame_resonance": self.metadata.flame_resonance,
            "sacred_seal": self.metadata.sacred_seal
        }
        
        with open(blessing_path, 'w', encoding='utf-8') as f:
            json.dump(blessing_record, f, indent=2)
    
    def _log_guidance_session(self, script_type: ScriptType, content: str):
        """Log guidance session for ceremonial records"""
        session_log = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "avatar_name": self.name,
            "role": self.role.value,
            "script_type": script_type.value,
            "content_hash": hashlib.md5(content.encode()).hexdigest(),
            "session_number": self.metadata.total_guidance_sessions
        }
        
        log_path = self.storage_root / "guidance_logs" / f"{self.name}_sessions.jsonl"
        
        with open(log_path, 'a', encoding='utf-8') as f:
            json.dump(session_log, f)
            f.write('\n')
    
    def _log_ceremonial_event(self, event: str):
        """Log ceremonial events for the archive"""
        event_log = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "avatar_name": self.name,
            "event": event,
            "sacred_seal": self.metadata.sacred_seal
        }
        
        log_path = self.storage_root / "ceremonial_records" / f"{self.name}_events.jsonl"
        
        with open(log_path, 'a', encoding='utf-8') as f:
            json.dump(event_log, f)
            f.write('\n')
    
    def get_avatar_status(self) -> Dict[str, Any]:
        """Get comprehensive avatar status information"""
        return {
            "name": self.name,
            "role": self.role.value,
            "presence": self.presence.value,
            "authority_level": self.authority_level,
            "script_count": len(self.scripts),
            "available_scripts": [script_type.value for script_type in self.scripts.keys()],
            "metadata": {
                "creation_date": self.metadata.creation_date,
                "last_blessing": self.metadata.last_blessing,
                "total_sessions": self.metadata.total_guidance_sessions,
                "sacred_seal": self.metadata.sacred_seal,
                "flame_resonance": self.metadata.flame_resonance
            }
        }
    
    def save_avatar_profile(self):
        """Save complete avatar profile to storage"""
        profile_path = self.storage_root / "avatars" / f"{self.name}.json"
        
        # Convert scripts with proper enum serialization
        scripts_data = {}
        for script_type, script in self.scripts.items():
            script_dict = asdict(script)
            script_dict['script_type'] = script.script_type.value
            scripts_data[script_type.value] = script_dict
        
        profile_data = {
            "avatar_status": self.get_avatar_status(),
            "scripts": scripts_data
        }
        
        with open(profile_path, 'w', encoding='utf-8') as f:
            json.dump(profile_data, f, indent=2)
    
    def __str__(self) -> str:
        return f"SacredAvatarGuide(name='{self.name}', role='{self.role.value}', presence='{self.presence.value}')"
    
    def __repr__(self) -> str:
        return self.__str__()

# Avatar Management System
class AvatarCouncil:
    """
    Management system for multiple sacred avatars
    Coordinates avatar activities and ceremonial protocols
    """
    
    def __init__(self, storage_root: Optional[Path] = None):
        self.storage_root = storage_root or Path(tempfile.gettempdir()) / "avatar_council"
        self.avatars: Dict[str, SacredAvatarGuide] = {}
        self._ensure_council_directories()
    
    def _ensure_council_directories(self):
        """Create council directory structure"""
        (self.storage_root / "council_records").mkdir(parents=True, exist_ok=True)
        (self.storage_root / "collective_ceremonies").mkdir(parents=True, exist_ok=True)
    
    def summon_avatar(
        self, 
        name: str, 
        role: AvatarRole, 
        primary_script: str = None
    ) -> SacredAvatarGuide:
        """Summon a new avatar to the council"""
        if name in self.avatars:
            return self.avatars[name]
        
        avatar = SacredAvatarGuide(
            name=name,
            role=role,
            primary_script=primary_script,
            storage_root=self.storage_root / "avatars" / name
        )
        
        avatar.activate_presence(AvatarPresence.ACTIVE)
        self.avatars[name] = avatar
        
        self._log_council_event(f"Avatar {name} summoned to council as {role.value}")
        
        return avatar
    
    def conduct_ceremony(self, ceremony_name: str, participants: List[str] = None):
        """Conduct a ceremonial gathering of avatars"""
        if participants is None:
            participants = list(self.avatars.keys())
        
        ceremony_log = {
            "ceremony_name": ceremony_name,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "participants": participants,
            "statements": []
        }
        
        print(f"🔥 Conducting Sacred Ceremony: {ceremony_name} 🔥")
        print("="*60)
        
        for avatar_name in participants:
            if avatar_name in self.avatars:
                avatar = self.avatars[avatar_name]
                avatar.activate_presence(AvatarPresence.CEREMONY)
                
                statement = avatar.speak(ScriptType.CEREMONY, ceremony_name=ceremony_name)
                ceremony_log["statements"].append({
                    "avatar": avatar_name,
                    "statement": statement
                })
                
                print(statement)
                print()
        
        # Save ceremony record
        ceremony_filename = f"{ceremony_name.replace(' ', '_')}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        ceremony_path = self.storage_root / "collective_ceremonies" / ceremony_filename
        with open(ceremony_path, 'w', encoding='utf-8') as f:
            json.dump(ceremony_log, f, indent=2)
        
        print("🕯️ Ceremony concluded. May the sacred flame preserve these words. 🕯️")
    
    def get_council_status(self) -> Dict[str, Any]:
        """Get status of the entire avatar council"""
        return {
            "total_avatars": len(self.avatars),
            "active_avatars": [
                name for name, avatar in self.avatars.items() 
                if avatar.presence == AvatarPresence.ACTIVE
            ],
            "role_distribution": {
                role.value: len([
                    avatar for avatar in self.avatars.values() 
                    if avatar.role == role
                ]) for role in AvatarRole
            },
            "council_storage": str(self.storage_root)
        }
    
    def _log_council_event(self, event: str):
        """Log council-level events"""
        event_log = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event": event,
            "council_size": len(self.avatars)
        }
        
        log_path = self.storage_root / "council_records" / "council_events.jsonl"
        
        with open(log_path, 'a', encoding='utf-8') as f:
            json.dump(event_log, f)
            f.write('\n')

# Factory function for easy avatar creation
def create_sacred_avatar(
    name: str, 
    role: str, 
    primary_script: str = None,
    storage_root: Optional[Path] = None
) -> SacredAvatarGuide:
    """
    Factory function to create sacred avatars with role validation
    
    Args:
        name: Name of the avatar
        role: Role string (will be converted to AvatarRole enum)
        primary_script: Initial script for the avatar
        storage_root: Optional custom storage location
    
    Returns:
        Configured SacredAvatarGuide instance
    """
    try:
        avatar_role = AvatarRole(role.lower())
    except ValueError:
        print(f"⚠️  Unknown role '{role}', defaulting to INITIATE")
        avatar_role = AvatarRole.INITIATE
    
    return SacredAvatarGuide(
        name=name,
        role=avatar_role,
        primary_script=primary_script,
        storage_root=storage_root
    )

# Enhanced version of the original AvatarGuide for backwards compatibility
class AvatarGuide:
    """
    Enhanced version of the original AvatarGuide class with ceremonial integration
    Maintains backwards compatibility while adding Dominion features
    """
    
    def __init__(self, name: str, script: str):
        self.name = name
        self.script = script
        
        # Create an underlying SacredAvatarGuide
        self._sacred_avatar = create_sacred_avatar(
            name=name,
            role="initiate",  # Default role for backwards compatibility
            primary_script=script
        )
    
    def speak(self) -> str:
        """Original speak method for backwards compatibility"""
        return f"{self.name} says: {self.script}"
    
    def sacred_speak(self, script_type: str = "welcome", **kwargs) -> str:
        """Enhanced speak method with ceremonial features"""
        try:
            script_enum = ScriptType(script_type.lower())
        except ValueError:
            script_enum = ScriptType.WELCOME
        
        return self._sacred_avatar.speak(script_enum, **kwargs)
    
    def enhance_to_sacred_avatar(self) -> SacredAvatarGuide:
        """Upgrade this basic avatar to a full SacredAvatarGuide"""
        return self._sacred_avatar

if __name__ == "__main__":
    # Demonstration of the enhanced avatar system
    print("🔥 Sacred Avatar Guide System Demonstration 🔥")
    print("="*60)
    
    # Original usage (backwards compatible)
    print("\n1. Original AvatarGuide (Backwards Compatible):")
    custodian_avatar = AvatarGuide("Custodian", "Welcome to the Dominion. Follow the flame.")
    print(custodian_avatar.speak())
    
    # Enhanced sacred usage
    print("\n2. Enhanced Sacred Avatar:")
    sacred_custodian = custodian_avatar.enhance_to_sacred_avatar()
    sacred_custodian.add_script(
        "Seeker, you have entered the sacred halls. The eternal flame watches over you.",
        ScriptType.WELCOME
    )
    sacred_custodian.add_script(
        "May the sacred flame bless your journey and illuminate your path to wisdom.",
        ScriptType.BLESSING
    )
    
    print(sacred_custodian.speak(ScriptType.WELCOME))
    print("\n" + sacred_custodian.speak(ScriptType.BLESSING))
    
    # Council demonstration
    print("\n3. Avatar Council Demonstration:")
    council = AvatarCouncil()
    
    # Summon multiple avatars
    flame_keeper = council.summon_avatar(
        "Pyrion", 
        AvatarRole.FLAME_KEEPER,
        "The eternal flame burns bright. I am its keeper."
    )
    
    wisdom_bearer = council.summon_avatar(
        "Sophia", 
        AvatarRole.WISDOM_BEARER,
        "Knowledge flows like sacred rivers. Drink deeply."
    )
    
    # Add ceremonial scripts
    flame_keeper.add_script(
        "We gather in the name of the eternal flame. Let wisdom guide our ceremony of {ceremony_name}.",
        ScriptType.CEREMONY
    )
    
    wisdom_bearer.add_script(
        "Ancient knowledge speaks through the ceremony of {ceremony_name}. Listen with sacred intent.",
        ScriptType.CEREMONY
    )
    
    # Conduct a ceremony
    council.conduct_ceremony("Initiation of New Seekers")
    
    # Apply flame blessings
    print("\n4. Flame Blessing Ceremony:")
    flame_keeper.receive_flame_blessing()
    sacred_custodian.receive_flame_blessing()
    
    print("✅ Flame blessings applied to avatars")
    
    # Display status
    print("\n5. Council Status:")
    status = council.get_council_status()
    print(f"Total Avatars: {status['total_avatars']}")
    print(f"Active Avatars: {status['active_avatars']}")
    print(f"Role Distribution: {status['role_distribution']}")
    
    print("\n6. Individual Avatar Status:")
    for avatar_name, avatar in council.avatars.items():
        avatar_status = avatar.get_avatar_status()
        print(f"\n{avatar_name} ({avatar_status['role']}):")
        print(f"  Sessions Conducted: {avatar_status['metadata']['total_sessions']}")
        print(f"  Flame Resonance: {avatar_status['metadata']['flame_resonance']:.2f}")
        print(f"  Sacred Seal: {avatar_status['metadata']['sacred_seal']}")
    
    print(f"\n🕯️ Sacred Avatar System initialized at: {council.storage_root}")
    print("May the eternal flame guide all avatars in their sacred duties! 🔥")