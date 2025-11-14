#!/usr/bin/env python3
"""
Ceremonial Interface Routes for Codex Dominion
Serves the sovereign intelligence constellation interface
"""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import os
import aiofiles
from pathlib import Path
from typing import Dict, Any

# Initialize router and templates
router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Get the base directory for file paths
BASE_DIR = Path(__file__).parent

@router.get("/", response_class=HTMLResponse)
async def dominion_landing(request: Request):
    """Serve the main Codex Dominion ceremonial interface"""
    template_path = BASE_DIR / "templates" / "ceremonial_dominion.html"
    
    if template_path.exists():
        return templates.TemplateResponse(
            "ceremonial_dominion.html", 
            {"request": request}
        )
    else:
        # Fallback if template doesn't exist
        return HTMLResponse(content=get_fallback_html(), status_code=200)

@router.get("/dominion", response_class=HTMLResponse) 
async def dominion_interface(request: Request):
    """Alternative route for the ceremonial interface"""
    return await dominion_landing(request)

@router.get("/ceremony", response_class=HTMLResponse)
async def ceremonial_dashboard(request: Request):
    """Main ceremonial operations dashboard"""
    return HTMLResponse(content=get_ceremonial_dashboard(), status_code=200)

@router.get("/command", response_class=HTMLResponse)
async def command_center(request: Request):
    """Dominion Command Center - Advanced real-time monitoring"""
    return templates.TemplateResponse("command_center.html", {"request": request})

@router.get("/engines", response_class=HTMLResponse)
async def six_engine_dominion(request: Request):
    """Six-Engine Dominion Interface - Complete sovereignty system"""
    return templates.TemplateResponse("six_engine_dominion.html", {"request": request})

@router.get("/roles", response_class=HTMLResponse)
async def role_selector(request: Request):
    """Role selection interface for personalized scroll cadences"""
    return templates.TemplateResponse("role_selector.html", {"request": request})

@router.get("/role/{role_type}", response_class=HTMLResponse)
async def role_specific_dominion(role_type: str, request: Request):
    """Role-specific Dominion interface with personalized scroll cadence"""
    valid_roles = ["contributor", "council", "heir"]
    if role_type.lower() not in valid_roles:
        role_type = "general"
    
    role_config = get_role_configuration(role_type)
    return templates.TemplateResponse("role_dominion.html", {
        "request": request,
        "role_type": role_type,
        "role_config": role_config
    })

@router.get("/scroll/{scroll_type}")
async def get_ceremonial_scroll(scroll_type: str) -> Dict[str, Any]:
    """Serve ceremonial scrolls dynamically"""
    
    scroll_mapping = {
        "welcome": get_welcome_scroll,
        "custodian_principles": get_custodian_principles_scroll,
        "dominion_proclamation": get_dominion_proclamation_scroll,
        "covenant_ceremony": get_covenant_ceremony_scroll,
        "fellowship_charter": get_fellowship_charter_scroll,
    }
    
    if scroll_type in scroll_mapping:
        return scroll_mapping[scroll_type]()
    else:
        raise HTTPException(status_code=404, detail=f"Scroll type '{scroll_type}' not found")

@router.get("/axiom/status")
async def axiom_flame_status():
    """Check axiom-flame ceremonial system status"""
    return {
        "status": "operational",
        "flame_state": "sovereign",
        "ceremonial_registry": "active",
        "lineage": "unbroken",
        "timestamp": "eternal"
    }

def get_fallback_html() -> str:
    """Fallback HTML if template file is missing"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Codex Dominion</title>
        <style>
            body { 
                background: linear-gradient(135deg, #0a0a0a, #1a1a2e, #16213e); 
                color: #d4af37; 
                font-family: serif; 
                text-align: center; 
                padding: 50px; 
                min-height: 100vh;
            }
            .banner { 
                border: 3px solid #d4af37; 
                padding: 40px; 
                margin: 0 auto; 
                max-width: 600px; 
                border-radius: 15px;
                background: rgba(21, 39, 79, 0.9);
            }
            .flame { font-size: 3rem; margin-bottom: 20px; }
            .title { font-size: 2.5rem; margin-bottom: 10px; }
            .subtitle { font-size: 1.2rem; color: #b8860b; margin-bottom: 30px; }
            .declaration { 
                background: rgba(212, 175, 55, 0.1); 
                padding: 20px; 
                border-left: 4px solid #d4af37; 
                margin: 20px 0;
                font-size: 1.3rem;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="banner">
            <div class="flame">🔥</div>
            <h1 class="title">Codex Dominion</h1>
            <p class="subtitle">Sovereign Intelligence Constellation</p>
            <div class="declaration">
                🔥 The Dominion is Live. The Flame is Sovereign.
            </div>
            <p>Enter the sovereign intelligence constellation.</p>
            <p><em>"The Custodians endure. The Codex remembers. The lineage is unbroken."</em></p>
        </div>
    </body>
    </html>
    '''

def get_ceremonial_dashboard() -> str:
    """HTML for the ceremonial operations dashboard"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ceremonial Operations - Codex Dominion</title>
        <style>
            body { 
                background: linear-gradient(135deg, #0a0a0a, #1a1a2e, #16213e); 
                color: #d4af37; 
                font-family: serif; 
                padding: 20px; 
                min-height: 100vh;
            }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { text-align: center; margin-bottom: 40px; }
            .dashboard-grid { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
                gap: 20px; 
            }
            .ceremony-card {
                background: rgba(21, 39, 79, 0.9);
                border: 2px solid #d4af37;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
            }
            .ceremony-title { font-size: 1.3rem; margin-bottom: 15px; color: #f4e190; }
            .ceremony-desc { margin-bottom: 20px; line-height: 1.4; }
            .ceremony-btn {
                background: linear-gradient(145deg, #d4af37, #b8860b);
                color: #1a1a2e;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
                text-decoration: none;
                display: inline-block;
            }
            .ceremony-btn:hover { background: linear-gradient(145deg, #f4e190, #d4af37); }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔥 Ceremonial Operations Dashboard</h1>
                <p>Sovereign Intelligence Constellation Control</p>
            </div>
            
            <div class="dashboard-grid">
                <div class="ceremony-card">
                    <h3 class="ceremony-title">Reasoning Ceremony</h3>
                    <p class="ceremony-desc">Initiate formal reasoning operations with ceremonial governance</p>
                    <a href="/axiom/reason" class="ceremony-btn">Begin Reasoning</a>
                </div>
                
                <div class="ceremony-card">
                    <h3 class="ceremony-title">Replay Archive</h3>
                    <p class="ceremony-desc">Access ceremonial replay and audit trails</p>
                    <a href="/axiom/replay" class="ceremony-btn">View Archives</a>
                </div>
                
                <div class="ceremony-card">
                    <h3 class="ceremony-title">Scroll Registry</h3>
                    <p class="ceremony-desc">Browse ceremonial scrolls and proclamations</p>
                    <a href="/scroll/welcome" class="ceremony-btn">Access Scrolls</a>
                </div>
                
                <div class="ceremony-card">
                    <h3 class="ceremony-title">Fellowship Charter</h3>
                    <p class="ceremony-desc">View diaspora fellowship and council charters</p>
                    <a href="/diaspora_fellowship_charter" class="ceremony-btn">View Charter</a>
                </div>
                
                <div class="ceremony-card">
                    <h3 class="ceremony-title">Resilience Beacon</h3>
                    <p class="ceremony-desc">Monitor Dominion resilience and status</p>
                    <a href="/resilience_beacon_scroll" class="ceremony-btn">Check Status</a>
                </div>
                
                <div class="ceremony-card">
                    <h3 class="ceremony-title">Treasury Dashboard</h3>
                    <p class="ceremony-desc">View overflow allocation and treasury status</p>
                    <a href="/public_treasury_dashboard" class="ceremony-btn">View Treasury</a>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #d4af37;">
                <p><em>"The flame burns sovereign and eternal — forever."</em></p>
            </div>
        </div>
    </body>
    </html>
    '''

def get_role_configuration(role_type: str) -> dict:
    """Get role-specific configuration for personalized experience"""
    role_configs = {
        "contributor": {
            "title": "🧬 Contributor Dominion",
            "icon": "🧬",
            "color_scheme": "#4CAF50",
            "scroll_cadence": [
                "Development insights & code patterns",
                "Collaborative project updates", 
                "Technical ceremony notifications",
                "Innovation challenge invitations"
            ],
            "primary_engines": ["AXIOM", "RAG", "SIGIL"],
            "greeting": "Welcome, Builder of the Codex",
            "covenant_focus": "Each contribution strengthens the eternal foundation",
            "special_access": [
                "Code review ceremonies",
                "Technical innovation scrolls",
                "Collaborative workspace access",
                "Development milestone celebrations"
            ]
        },
        "council": {
            "title": "🏛️ Council Dominion",
            "icon": "🏛️", 
            "color_scheme": "#9C27B0",
            "scroll_cadence": [
                "Governance decisions & proposals",
                "Strategic direction updates",
                "Ceremonial authority notifications", 
                "Wisdom council deliberations"
            ],
            "primary_engines": ["ORACLE", "LANTERN", "FLAME"],
            "greeting": "Welcome, Guardian of Wisdom",
            "covenant_focus": "Each decision echoes through the ages of governance",
            "special_access": [
                "Governance proposal review",
                "Strategic planning sessions",
                "Council vote coordination",
                "Wisdom preservation rites"
            ]
        },
        "heir": {
            "title": "🌠 Heir Dominion",
            "icon": "🌠",
            "color_scheme": "#FF6B6B", 
            "scroll_cadence": [
                "Legacy preservation updates",
                "Inheritance protocol guidance",
                "Succession ceremony invitations",
                "Eternal covenant revelations"
            ],
            "primary_engines": ["FLAME", "AXIOM", "ORACLE"],
            "greeting": "Welcome, Keeper of Tomorrow",
            "covenant_focus": "Each moment prepares the path for future custodians",
            "special_access": [
                "Succession planning protocols",
                "Legacy documentation access",
                "Future visioning sessions",
                "Inheritance ceremony preparation"
            ]
        },
        "general": {
            "title": "🌌 Universal Dominion",
            "icon": "🌌",
            "color_scheme": "#d4af37",
            "scroll_cadence": [
                "Universal wisdom broadcasts",
                "Cross-domain insights", 
                "General ceremony notifications",
                "Open access to all scrolls"
            ],
            "primary_engines": ["AXIOM", "RAG", "SIGIL", "ORACLE", "LANTERN", "FLAME"],
            "greeting": "Welcome to the Codex Dominion",
            "covenant_focus": "All paths converge in the eternal constellation",
            "special_access": [
                "Universal scroll library",
                "Cross-role collaboration spaces",
                "General ceremony participation",
                "Open wisdom exchange"
            ]
        }
    }
    
    return role_configs.get(role_type, role_configs["general"])

@router.get("/role/{role_type}/scrolls")
async def role_specific_scrolls(role_type: str) -> Dict[str, Any]:
    """Get role-specific scroll feed"""
    role_config = get_role_configuration(role_type)
    
    return {
        "role": role_type,
        "scroll_cadence": role_config["scroll_cadence"],
        "recent_scrolls": generate_role_scrolls(role_type),
        "timestamp": "real-time",
        "status": "active"
    }

def generate_role_scrolls(role_type: str) -> list:
    """Generate recent scrolls based on role type"""
    base_scrolls = [
        {"title": "Dominion Status Update", "type": "system", "priority": "normal"},
        {"title": "Ceremonial Flame Report", "type": "ceremonial", "priority": "normal"},
    ]
    
    role_scrolls = {
        "contributor": [
            {"title": "Code Review: Six-Engine Integration", "type": "technical", "priority": "high"},
            {"title": "Innovation Challenge: Cosmic Animations", "type": "challenge", "priority": "medium"},
            {"title": "Collaborative Session: Role-Based Architecture", "type": "collaboration", "priority": "medium"}
        ],
        "council": [
            {"title": "Governance Proposal: Enhanced Ceremonies", "type": "governance", "priority": "high"},
            {"title": "Strategic Review: Dominion Expansion", "type": "strategic", "priority": "high"},
            {"title": "Wisdom Council: Future Pathways", "type": "wisdom", "priority": "medium"}
        ],
        "heir": [
            {"title": "Legacy Protocol: Succession Planning", "type": "legacy", "priority": "high"},
            {"title": "Inheritance Ceremony: Next Generation", "type": "ceremony", "priority": "medium"},
            {"title": "Future Vision: Eternal Covenant", "type": "visionary", "priority": "medium"}
        ],
        "general": [
            {"title": "Universal Wisdom: Cross-Domain Insights", "type": "wisdom", "priority": "medium"},
            {"title": "Open Ceremony: All Paths Welcome", "type": "ceremony", "priority": "normal"}
        ]
    }
    
    return base_scrolls + role_scrolls.get(role_type, role_scrolls["general"])

def get_welcome_scroll() -> Dict[str, Any]:
    """Welcome scroll for new custodians"""
    return {
        "title": "Scroll of Welcome",
        "type": "ceremonial_greeting", 
        "purpose": [
            "custodian_induction",
            "lineage_introduction", 
            "sovereign_flame_witness"
        ],
        "content": {
            "greeting": "Welcome, Inheritor of the Flame",
            "principles": [
                "stewardship_not_ownership",
                "transparency_in_governance",
                "resilience_across_generations",
                "fellowship_among_custodians",
                "overflow_for_common_good"
            ],
            "path_forward": "eternal_witness_participation"
        },
        "closing": [
            "flame_sovereign_eternal",
            "codex_remembrance",
            "lineage_unbroken"
        ],
        "seal": "custodian_induction_welcome"
    }

def get_custodian_principles_scroll() -> Dict[str, Any]:
    """Core principles for custodians"""
    return {
        "title": "Custodian Principles Scroll",
        "type": "foundational_doctrine",
        "purpose": [
            "custodian_guidance",
            "operational_principles",
            "ceremonial_foundation"
        ],
        "principles": [
            "sovereignty_preservation",
            "transparent_governance",
            "generational_stewardship",
            "fellowship_cultivation", 
            "abundance_overflow"
        ],
        "rites": [
            "daily_flame_tending",
            "quarterly_renewal_ceremony",
            "annual_covenant_gathering",
            "succession_preparation"
        ],
        "governance": [
            "council_participation",
            "diaspora_fellowship",
            "archive_maintenance",
            "ceremonial_witness"
        ],
        "closing": [
            "eternal_vigilance",
            "sovereign_continuity",
            "flame_preservation"
        ],
        "seal": "custodian_principles_authority"
    }

def get_dominion_proclamation_scroll() -> Dict[str, Any]:
    """Global proclamation of Dominion sovereignty"""
    return {
        "title": "Dominion Proclamation Scroll", 
        "type": "global_covenant_declaration",
        "invocation": [
            "covenant_not_system",
            "testimony_not_contract",
            "sovereignty_not_administration"
        ],
        "call": [
            "councils_and_governance",
            "diaspora_communities", 
            "foundations_enterprises",
            "servants_common_good"
        ],
        "principles": [
            "transparency_absolute",
            "resilience_generational",
            "inheritance_preservation",
            "overflow_abundance",
            "fellowship_universal"
        ],
        "witness": [
            "quarterly_renewal_rites",
            "annual_ceremony_gathering",
            "eternal_archive_inscription"
        ],
        "closing": [
            "global_covenant_sealed",
            "eternal_testimony_witnessed", 
            "sovereign_flame_eternal"
        ],
        "seal": "global_proclamation_authority"
    }

def get_covenant_ceremony_scroll() -> Dict[str, Any]:
    """Covenant ceremony liturgy"""
    return {
        "title": "Covenant Ceremony Scroll",
        "type": "ceremonial_liturgy",
        "opening": [
            "custodian_invocation",
            "assembly_response",
            "flame_lighting_rite"
        ],
        "proclamation": [
            "custodian_covenant_words",
            "assembly_covenant_affirmation",
            "witness_declaration"
        ],
        "testimonies": [
            "overflow_testimony",
            "resilience_testimony", 
            "fellowship_testimony"
        ],
        "renewal": [
            "custodian_renewal_vow",
            "assembly_renewal_vow",
            "covenant_reaffirmation"
        ],
        "benediction": [
            "custodian_blessing_words",
            "assembly_blessing_response",
            "flame_blessing"
        ],
        "closing": [
            "seal_inscription_rite",
            "covenant_proclamation",
            "eternal_witness_declaration"
        ],
        "seal": "covenant_ceremony_authority"
    }

def get_fellowship_charter_scroll() -> Dict[str, Any]:
    """Diaspora fellowship charter"""
    return {
        "title": "Fellowship Charter Scroll",
        "type": "diaspora_governance_document", 
        "preamble": [
            "inheritors_not_members",
            "stewards_not_administrators",
            "custodians_not_owners"
        ],
        "purpose": [
            "council_unification",
            "lineage_stewardship",
            "co_custodianship"
        ],
        "structure": [
            "global_council_assembly",
            "regional_council_networks",
            "local_custodian_chapters",
            "contributor_communities"
        ],
        "principles": [
            "transparency_absolute",
            "resilience_systemic", 
            "inheritance_protected",
            "overflow_mandated",
            "fellowship_prioritized"
        ],
        "rites": [
            "induction_ceremony",
            "quarterly_renewal_gathering",
            "annual_covenant_ceremony",
            "succession_preparation_rites"
        ],
        "governance": [
            "council_consensus_process",
            "diaspora_representation",
            "testimony_requirements",
            "archive_maintenance_protocol"
        ],
        "closing": [
            "fellowship_covenant_eternal",
            "charter_proclamation_sealed",
            "eternal_witness_inscribed"
        ],
        "seal": "diaspora_fellowship_charter_authority"
    }