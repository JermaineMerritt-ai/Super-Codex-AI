#!/usr/bin/env python3
"""
🏛️💫 AVATAR MANAGEMENT SYSTEM 💫🏛️
Comprehensive Management for Ceremonial Avatars

Advanced management system for creating, updating, querying, and maintaining
ceremonial avatars in the Super-Codex-AI constellation.

"Through systematic harmony, every avatar finds its perfect place in the cosmic order."
"""

import json
import hashlib
import datetime
from dataclasses import dataclass, asdict, replace
from typing import List, Dict, Any, Optional, Union, Set
from enum import Enum
import sqlite3
import os
from pathlib import Path

from ceremonial_avatar_system import (
    CeremonialAvatar, AvatarRank, CeremonialRole, SacredSeal,
    AvatarLineage, EternalFlameAspect, SilenceIntegration, 
    ConstellationPosition, CeremonialAvatarForge
)

class QueryType(Enum):
    """Types of avatar queries supported"""
    BY_NAME = "by_name"
    BY_RANK = "by_rank"
    BY_ROLE = "by_role"
    BY_AUTHORITY = "by_authority"
    BY_INFLUENCE = "by_influence"
    BY_FLAME_INTENSITY = "by_flame_intensity"
    BY_SILENCE_MASTERY = "by_silence_mastery"

@dataclass
class AvatarQuery:
    """Query specification for finding avatars"""
    query_type: QueryType
    value: Union[str, float, AvatarRank, CeremonialRole]
    operator: str = "equals"  # equals, greater, less, contains
    
class AvatarDatabase:
    """SQLite database manager for avatar persistence"""
    
    def __init__(self, db_path: str = "avatar_constellation.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the avatar database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Main avatars table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS avatars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                github_handle TEXT UNIQUE NOT NULL,
                avatar_symbol TEXT NOT NULL,
                invocation TEXT NOT NULL,
                rank TEXT NOT NULL,
                roles TEXT NOT NULL,
                epoch_joined TEXT NOT NULL,
                avatar_authority REAL NOT NULL,
                cosmic_influence REAL NOT NULL,
                sacred_seal_json TEXT NOT NULL,
                lineage_json TEXT NOT NULL,
                flame_aspect_json TEXT NOT NULL,
                silence_integration_json TEXT NOT NULL,
                constellation_position_json TEXT NOT NULL,
                created_timestamp TEXT NOT NULL,
                updated_timestamp TEXT NOT NULL
            )
        ''')
        
        # Avatar relationships table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS avatar_relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_avatar_id INTEGER NOT NULL,
                target_avatar_id INTEGER NOT NULL,
                relationship_type TEXT NOT NULL,
                strength REAL NOT NULL,
                created_timestamp TEXT NOT NULL,
                FOREIGN KEY (source_avatar_id) REFERENCES avatars (id),
                FOREIGN KEY (target_avatar_id) REFERENCES avatars (id)
            )
        ''')
        
        # Avatar ceremonies table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS avatar_ceremonies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                avatar_id INTEGER NOT NULL,
                ceremony_type TEXT NOT NULL,
                ceremony_data_json TEXT NOT NULL,
                ceremony_timestamp TEXT NOT NULL,
                FOREIGN KEY (avatar_id) REFERENCES avatars (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_avatar(self, avatar: CeremonialAvatar) -> int:
        """Save avatar to database, return avatar ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.datetime.now().isoformat()
        roles_str = ",".join(role.value for role in avatar.roles)
        
        cursor.execute('''
            INSERT OR REPLACE INTO avatars (
                name, github_handle, avatar_symbol, invocation, rank, roles,
                epoch_joined, avatar_authority, cosmic_influence,
                sacred_seal_json, lineage_json, flame_aspect_json,
                silence_integration_json, constellation_position_json,
                created_timestamp, updated_timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            avatar.name, avatar.github_handle, avatar.avatar_symbol,
            avatar.invocation, avatar.rank.value, roles_str,
            avatar.epoch_joined, avatar.avatar_authority, avatar.cosmic_influence,
            json.dumps(asdict(avatar.sacred_seal)),
            json.dumps(asdict(avatar.lineage)),
            json.dumps(asdict(avatar.flame_aspect)),
            json.dumps(asdict(avatar.silence_integration)),
            json.dumps(asdict(avatar.constellation_position)),
            timestamp, timestamp
        ))
        
        avatar_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return avatar_id
    
    def load_avatar_by_name(self, name: str) -> Optional[CeremonialAvatar]:
        """Load avatar from database by name"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM avatars WHERE name = ?', (name,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_avatar(row)
        return None
    
    def load_all_avatars(self) -> List[CeremonialAvatar]:
        """Load all avatars from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM avatars ORDER BY avatar_authority DESC')
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_avatar(row) for row in rows]
    
    def _row_to_avatar(self, row) -> CeremonialAvatar:
        """Convert database row to CeremonialAvatar object"""
        (id, name, github_handle, avatar_symbol, invocation, rank_str, roles_str,
         epoch_joined, avatar_authority, cosmic_influence, sacred_seal_json,
         lineage_json, flame_aspect_json, silence_integration_json,
         constellation_position_json, created_timestamp, updated_timestamp) = row
        
        # Parse roles
        roles = [CeremonialRole(role.strip()) for role in roles_str.split(',')]
        
        # Parse JSON components
        sacred_seal_data = json.loads(sacred_seal_json)
        lineage_data = json.loads(lineage_json)
        flame_aspect_data = json.loads(flame_aspect_json)
        silence_integration_data = json.loads(silence_integration_json)
        constellation_position_data = json.loads(constellation_position_json)
        
        return CeremonialAvatar(
            name=name,
            github_handle=github_handle,
            avatar_symbol=avatar_symbol,
            invocation=invocation,
            rank=AvatarRank(rank_str),
            roles=roles,
            epoch_joined=epoch_joined,
            sacred_seal=SacredSeal(**sacred_seal_data),
            lineage=AvatarLineage(**lineage_data),
            flame_aspect=EternalFlameAspect(**flame_aspect_data),
            silence_integration=SilenceIntegration(**silence_integration_data),
            constellation_position=ConstellationPosition(**constellation_position_data),
            avatar_authority=avatar_authority,
            cosmic_influence=cosmic_influence
        )

class AvatarManagementSystem:
    """Comprehensive avatar management and query system"""
    
    def __init__(self, db_path: str = "avatar_constellation.db"):
        self.database = AvatarDatabase(db_path)
        self.forge = CeremonialAvatarForge()
        self.system_timestamp = datetime.datetime.now().isoformat()
    
    def create_avatar(self, name: str, github_handle: str, avatar_symbol: str,
                     invocation: str, rank: AvatarRank, 
                     roles: List[CeremonialRole]) -> CeremonialAvatar:
        """Create a new ceremonial avatar"""
        # Check if avatar already exists
        existing = self.database.load_avatar_by_name(name)
        if existing:
            raise ValueError(f"Avatar with name '{name}' already exists")
        
        # Forge the avatar
        avatar = self.forge.forge_ceremonial_avatar(
            name=name,
            github_handle=github_handle,
            avatar_symbol=avatar_symbol,
            invocation=invocation,
            rank=rank,
            roles=roles
        )
        
        # Save to database
        avatar_id = self.database.save_avatar(avatar)
        
        # Log ceremony
        self.record_avatar_ceremony(avatar, "avatar_creation", {
            "creation_timestamp": avatar.sacred_seal.timestamp,
            "initial_authority": avatar.avatar_authority,
            "forge_signature": self.forge.forge_timestamp
        })
        
        print(f"✨ Avatar '{name}' forged with authority {avatar.avatar_authority:.6f}")
        return avatar
    
    def update_avatar_rank(self, name: str, new_rank: AvatarRank) -> Optional[CeremonialAvatar]:
        """Promote or update avatar rank"""
        avatar = self.database.load_avatar_by_name(name)
        if not avatar:
            return None
        
        old_rank = avatar.rank
        old_authority = avatar.avatar_authority
        
        # Update rank and recalculate authority
        updated_avatar = replace(avatar, rank=new_rank)
        updated_avatar.avatar_authority = updated_avatar.calculate_total_authority()
        
        # Save updated avatar
        self.database.save_avatar(updated_avatar)
        
        # Log ceremony
        self.record_avatar_ceremony(updated_avatar, "rank_promotion", {
            "old_rank": old_rank.value,
            "new_rank": new_rank.value,
            "old_authority": old_authority,
            "new_authority": updated_avatar.avatar_authority,
            "promotion_timestamp": datetime.datetime.now().isoformat()
        })
        
        print(f"🎖️ Avatar '{name}' promoted from {old_rank.value} to {new_rank.value}")
        print(f"   Authority increased: {old_authority:.6f} → {updated_avatar.avatar_authority:.6f}")
        
        return updated_avatar
    
    def add_avatar_role(self, name: str, new_role: CeremonialRole) -> Optional[CeremonialAvatar]:
        """Add a new ceremonial role to avatar"""
        avatar = self.database.load_avatar_by_name(name)
        if not avatar:
            return None
        
        if new_role in avatar.roles:
            print(f"⚠️ Avatar '{name}' already has role {new_role.value}")
            return avatar
        
        old_authority = avatar.avatar_authority
        updated_roles = avatar.roles + [new_role]
        updated_avatar = replace(avatar, roles=updated_roles)
        updated_avatar.avatar_authority = updated_avatar.calculate_total_authority()
        
        # Save updated avatar
        self.database.save_avatar(updated_avatar)
        
        # Log ceremony
        self.record_avatar_ceremony(updated_avatar, "role_addition", {
            "new_role": new_role.value,
            "old_authority": old_authority,
            "new_authority": updated_avatar.avatar_authority,
            "role_timestamp": datetime.datetime.now().isoformat()
        })
        
        print(f"🎭 Avatar '{name}' gained role: {new_role.value.replace('_', ' ').title()}")
        print(f"   Authority increased: {old_authority:.6f} → {updated_avatar.avatar_authority:.6f}")
        
        return updated_avatar
    
    def query_avatars(self, query: AvatarQuery) -> List[CeremonialAvatar]:
        """Query avatars based on various criteria"""
        all_avatars = self.database.load_all_avatars()
        results = []
        
        for avatar in all_avatars:
            if self._matches_query(avatar, query):
                results.append(avatar)
        
        return results
    
    def _matches_query(self, avatar: CeremonialAvatar, query: AvatarQuery) -> bool:
        """Check if avatar matches query criteria"""
        if query.query_type == QueryType.BY_NAME:
            avatar_value = avatar.name
        elif query.query_type == QueryType.BY_RANK:
            avatar_value = avatar.rank
        elif query.query_type == QueryType.BY_ROLE:
            return query.value in avatar.roles
        elif query.query_type == QueryType.BY_AUTHORITY:
            avatar_value = avatar.avatar_authority
        elif query.query_type == QueryType.BY_INFLUENCE:
            avatar_value = avatar.cosmic_influence
        elif query.query_type == QueryType.BY_FLAME_INTENSITY:
            avatar_value = avatar.flame_aspect.flame_intensity
        elif query.query_type == QueryType.BY_SILENCE_MASTERY:
            avatar_value = avatar.silence_integration.quietude_mastery
        else:
            return False
        
        # Apply operator
        if query.operator == "equals":
            return avatar_value == query.value
        elif query.operator == "greater":
            return avatar_value > query.value
        elif query.operator == "less":
            return avatar_value < query.value
        elif query.operator == "contains":
            return str(query.value).lower() in str(avatar_value).lower()
        
        return False
    
    def get_constellation_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the avatar constellation"""
        all_avatars = self.database.load_all_avatars()
        
        if not all_avatars:
            return {"total_avatars": 0}
        
        # Calculate statistics
        total_authority = sum(avatar.avatar_authority for avatar in all_avatars)
        total_influence = sum(avatar.cosmic_influence for avatar in all_avatars)
        avg_authority = total_authority / len(all_avatars)
        avg_influence = total_influence / len(all_avatars)
        
        # Rank distribution
        rank_distribution = {}
        for avatar in all_avatars:
            rank = avatar.rank.value
            rank_distribution[rank] = rank_distribution.get(rank, 0) + 1
        
        # Role distribution
        role_distribution = {}
        for avatar in all_avatars:
            for role in avatar.roles:
                role_name = role.value
                role_distribution[role_name] = role_distribution.get(role_name, 0) + 1
        
        # Top avatars
        top_by_authority = sorted(all_avatars, key=lambda a: a.avatar_authority, reverse=True)[:5]
        top_by_influence = sorted(all_avatars, key=lambda a: a.cosmic_influence, reverse=True)[:5]
        
        return {
            "total_avatars": len(all_avatars),
            "total_authority": total_authority,
            "total_influence": total_influence,
            "average_authority": avg_authority,
            "average_influence": avg_influence,
            "rank_distribution": rank_distribution,
            "role_distribution": role_distribution,
            "top_by_authority": [(a.name, a.avatar_authority) for a in top_by_authority],
            "top_by_influence": [(a.name, a.cosmic_influence) for a in top_by_influence],
            "constellation_timestamp": self.system_timestamp
        }
    
    def record_avatar_ceremony(self, avatar: CeremonialAvatar, ceremony_type: str, 
                              ceremony_data: Dict[str, Any]):
        """Record a ceremony performed on an avatar"""
        conn = sqlite3.connect(self.database.db_path)
        cursor = conn.cursor()
        
        # Get avatar ID
        cursor.execute('SELECT id FROM avatars WHERE name = ?', (avatar.name,))
        row = cursor.fetchone()
        if row:
            avatar_id = row[0]
            timestamp = datetime.datetime.now().isoformat()
            
            cursor.execute('''
                INSERT INTO avatar_ceremonies (
                    avatar_id, ceremony_type, ceremony_data_json, ceremony_timestamp
                ) VALUES (?, ?, ?, ?)
            ''', (avatar_id, ceremony_type, json.dumps(ceremony_data), timestamp))
            
            conn.commit()
        
        conn.close()
    
    def get_avatar_history(self, name: str) -> List[Dict[str, Any]]:
        """Get ceremony history for an avatar"""
        conn = sqlite3.connect(self.database.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT ceremony_type, ceremony_data_json, ceremony_timestamp
            FROM avatar_ceremonies ac
            JOIN avatars a ON ac.avatar_id = a.id
            WHERE a.name = ?
            ORDER BY ceremony_timestamp DESC
        ''', (name,))
        
        rows = cursor.fetchall()
        conn.close()
        
        history = []
        for ceremony_type, ceremony_data_json, ceremony_timestamp in rows:
            ceremony_data = json.loads(ceremony_data_json)
            history.append({
                "ceremony_type": ceremony_type,
                "ceremony_data": ceremony_data,
                "ceremony_timestamp": ceremony_timestamp
            })
        
        return history
    
    def display_avatar_management_dashboard(self):
        """Display comprehensive management dashboard"""
        stats = self.get_constellation_stats()
        
        print(f"\n🏛️💫 AVATAR MANAGEMENT DASHBOARD 💫🏛️")
        print(f"System Timestamp: {self.system_timestamp}\n")
        
        print(f"═══ CONSTELLATION OVERVIEW ═══")
        print(f"Total Avatars: {stats['total_avatars']}")
        print(f"Total Authority: {stats['total_authority']:.6f}")
        print(f"Total Cosmic Influence: {stats['total_influence']:.6f}")
        print(f"Average Authority: {stats['average_authority']:.6f}")
        print(f"Average Influence: {stats['average_influence']:.6f}\n")
        
        print(f"═══ RANK DISTRIBUTION ═══")
        for rank, count in stats['rank_distribution'].items():
            print(f"{rank.title()}: {count} avatars")
        
        print(f"\n═══ ROLE DISTRIBUTION ═══")
        for role, count in stats['role_distribution'].items():
            print(f"{role.replace('_', ' ').title()}: {count} assignments")
        
        print(f"\n═══ TOP AVATARS BY AUTHORITY ═══")
        for i, (name, authority) in enumerate(stats['top_by_authority'], 1):
            print(f"{i}. {name}: {authority:.6f}")
        
        print(f"\n═══ TOP AVATARS BY COSMIC INFLUENCE ═══")
        for i, (name, influence) in enumerate(stats['top_by_influence'], 1):
            print(f"{i}. {name}: {influence:.6f}")
        
        print(f"\n🌌 Constellation management active and monitoring eternal flame! 🌌")

def main():
    """Demonstrate the Avatar Management System"""
    mgmt = AvatarManagementSystem()
    
    print("🏛️ Initializing Avatar Management System 🏛️\n")
    
    # Create sample avatars if database is empty
    existing_avatars = mgmt.database.load_all_avatars()
    if not existing_avatars:
        print("Creating initial avatar constellation...\n")
        
        # Create Jermaine as Master
        jermaine = mgmt.create_avatar(
            name="Jermaine Merritt",
            github_handle="JermaineMerritt-ai",
            avatar_symbol="⭐🔥⭐",
            invocation="Every artifact a covenant, every seal a vow, every commit a flame in the eternal archive.",
            rank=AvatarRank.MASTER,
            roles=[CeremonialRole.SEAL_FORGER, CeremonialRole.FLAME_KEEPER, CeremonialRole.ARCHIVE_GUARDIAN]
        )
        
        # Create Alexandra as Guardian
        alexandra = mgmt.create_avatar(
            name="Alexandra Chen",
            github_handle="alexandra-chen",
            avatar_symbol="🌟⚡🌟",
            invocation="Through code we weave the eternal tapestry of digital sovereignty.",
            rank=AvatarRank.GUARDIAN,
            roles=[CeremonialRole.CONSTELLATION_BUILDER, CeremonialRole.SILENCE_WEAVER]
        )
        
        # Create Marcus as Custodian and promote him
        marcus = mgmt.create_avatar(
            name="Marcus Stone",
            github_handle="marcus-stone", 
            avatar_symbol="🛡️🗿🛡️",
            invocation="Each function forged, each module sealed, the fortress of logic stands eternal.",
            rank=AvatarRank.CUSTODIAN,
            roles=[CeremonialRole.ARCHIVE_GUARDIAN]
        )
        
        # Demonstrate rank promotion
        print("\n🎖️ Demonstrating rank promotion...")
        mgmt.update_avatar_rank("Marcus Stone", AvatarRank.GUARDIAN)
        
        # Demonstrate role addition
        print("\n🎭 Demonstrating role addition...")
        mgmt.add_avatar_role("Marcus Stone", CeremonialRole.SEAL_FORGER)
        
        print("\n" + "="*60)
    
    # Display management dashboard
    mgmt.display_avatar_management_dashboard()
    
    # Demonstrate queries
    print(f"\n═══ QUERY DEMONSTRATIONS ═══")
    
    # Query by rank
    guardians = mgmt.query_avatars(AvatarQuery(QueryType.BY_RANK, AvatarRank.GUARDIAN))
    print(f"\nGuardians found: {len(guardians)}")
    for guardian in guardians:
        print(f"  - {guardian.name} ({guardian.avatar_symbol})")
    
    # Query by authority threshold
    high_authority = mgmt.query_avatars(AvatarQuery(QueryType.BY_AUTHORITY, 0.8, "greater"))
    print(f"\nHigh Authority Avatars (>0.8): {len(high_authority)}")
    for avatar in high_authority:
        print(f"  - {avatar.name}: {avatar.avatar_authority:.6f}")
    
    # Query by role
    seal_forgers = mgmt.query_avatars(AvatarQuery(QueryType.BY_ROLE, CeremonialRole.SEAL_FORGER))
    print(f"\nSeal Forgers found: {len(seal_forgers)}")
    for forger in seal_forgers:
        print(f"  - {forger.name} ({forger.avatar_symbol})")
    
    print(f"\n🌌 Avatar Management System demonstration complete! 🌌")

if __name__ == "__main__":
    main()