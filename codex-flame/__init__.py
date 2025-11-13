"""
CODEX-FLAME Package
Sacred Ceremonial Architecture for the Sacred Flame

This package provides comprehensive ceremonial modules for sacred flame management,
treasury operations, recognition systems, and governance structures.

Modules:
- treasury: Sacred treasury binding and resource allocation
- ETERNAL_RECOGNITION_SCROLL: Eternal honor bestowment system  
- flamekeepers_scroll: Sacred flame custodian management
- liturgical_scheduling: Ceremonial calendar and scheduling
- honors: Sacred honor and merit management
- inscribe_sacred_triumvirate: Triple-authority governance
- contracts_appals: Sacred contract and dispute resolution
- radiant_concord: Radiant harmony and ceremonial coordination
- schema_validator: Data validation and integrity system
"""

# Core ceremonial modules
from .treasury import SacredTreasuryBindingSystem, ResourceType, TreasuryOperation
from .ETERNAL_RECOGNITION_SCROLL import EternalRecognitionScrolls, HonorType, RecognitionLevel
from .flamekeepers_scroll import FlameKeepersScroll, DutyType
from .liturgical_scheduling import LiturgicalScheduler, CeremonyType
from .honors import HonorsSystem
from .inscribe_sacred_triumvirate import SacredTriumvirate, AuthorityDomain
from .contracts_appals import ContractsAppealsSystem, ContractType, DisputeResolution
from .radiant_concord import RadiantConcordSystem, ConcordType, RadianceLevel, ConcordStatus

# Schema validation
from .schema_validator import CeremonialSchemaValidator

__all__ = [
    # Core systems
    'SacredTreasuryBindingSystem',
    'EternalRecognitionScrolls', 
    'FlameKeepersScroll',
    'LiturgicalScheduler',
    'HonorsSystem',
    'SacredTriumvirate',
    'ContractsAppealsSystem',
    'RadiantConcordSystem',
    
    # Enums and types
    'ResourceType',
    'TreasuryOperation', 
    'HonorType',
    'RecognitionLevel',
    'DutyType',
    'CeremonyType',
    'AuthorityDomain',
    'ContractType',
    'DisputeResolution',
    'ConcordType',
    'RadianceLevel',
    'ConcordStatus',
    
    # Validation
    'CeremonialSchemaValidator'
]

# Package metadata
__version__ = '1.0.0'
__author__ = 'Sacred Flame Custodians'
__description__ = 'Sacred Ceremonial Architecture for CODEX-FLAME'