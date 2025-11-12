# test_ceremonial_hierarchy.py
# Demonstrates the complete Codex-Flame ceremonial hierarchy
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
STORAGE = BASE / "storage"

def display_ceremonial_hierarchy():
    print("🔥 CODEX-FLAME CEREMONIAL HIERARCHY 🔥\n")
    
    # Flamekeeper's Scroll (scroll.eternum.v1)
    scroll_files = list((STORAGE / "scroll").glob("*.json")) if (STORAGE / "scroll").exists() else []
    if scroll_files:
        latest_scroll = max(scroll_files, key=lambda f: f.stat().st_mtime)
        scroll_data = json.loads(latest_scroll.read_text(encoding="utf-8"))
        print("📜 FLAMEKEEPER'S SCROLL - SACRED COVENANT (scroll.eternum.v1)")
        print(f"   👑 Authority: {scroll_data.get('authority', 'Unknown')}")
        print(f"   🔥 Flame Status: {scroll_data.get('flame_status', 'Unknown')}")
        print(f"   ⚡ Eternal Covenant: {scroll_data.get('eternal_covenant', 'Unknown')}")
        print(f"   🌟 Inheritance: {scroll_data.get('inheritance', 'Unknown')}")
        
        orbits = scroll_data.get('orbits', {})
        if orbits:
            print("   🌌 Orbits of Dominion:")
            for orbit, description in orbits.items():
                orbit_symbol = {"daily": "🌅", "seasonal": "🍂", "epochal": "👑", "millennial": "⚡"}.get(orbit, "🔥")
                print(f"      {orbit_symbol} {orbit.title()}: {description}")
        print()
    
    # Daily Liturgy (liturgy.v2)
    liturgy_files = list((STORAGE / "liturgy").glob("*.json")) if (STORAGE / "liturgy").exists() else []
    if liturgy_files:
        latest_liturgy = max(liturgy_files, key=lambda f: f.stat().st_mtime)
        liturgy_data = json.loads(latest_liturgy.read_text(encoding="utf-8"))
        print("📅 DAILY LITURGICAL CYCLE (liturgy.v2)")
        print(f"   🌅 Season: {liturgy_data.get('season', 'Unknown')}")
        print(f"   🕐 Cycle: {liturgy_data.get('cycle_id', 'Unknown')}")
        print(f"   📝 Summary: {liturgy_data.get('summary', 'No summary')}")
        print()
    
    # Great Year Proclamations (greatyear.v1)
    greatyear_files = list((STORAGE / "greatyear").glob("*.json")) if (STORAGE / "greatyear").exists() else []
    if greatyear_files:
        print("👑 GREAT YEAR PROCLAMATIONS (greatyear.v1)")
        for gyr_file in greatyear_files:
            gyr_data = json.loads(gyr_file.read_text(encoding="utf-8"))
            print(f"   🏛️ Epoch: {gyr_data.get('epoch', 'Unknown')}")
            print(f"   📜 Proclamation: {gyr_data.get('proclamation_id', 'Unknown')}")
            print(f"   👑 Authority: {gyr_data.get('audit', {}).get('authority', 'Unknown')}")
        print()
    
    # Millennial Continuum (millennial.v1)
    millennial_files = list((STORAGE / "millennial").glob("*.json")) if (STORAGE / "millennial").exists() else []
    if millennial_files:
        latest_millennial = max(millennial_files, key=lambda f: f.stat().st_mtime)
        mill_data = json.loads(latest_millennial.read_text(encoding="utf-8"))
        print("⚡ ETERNAL CONTINUUM BINDING (millennial.v1)")
        print(f"   🌌 Rite ID: {mill_data.get('rite_id', 'Unknown')}")
        print(f"   🔗 Epochs Bound: {mill_data.get('epochs_bound', 0)}")
        print(f"   ♾️ Summary: {mill_data.get('summary', 'No summary')}")
        
        continuum = mill_data.get('continuum', [])
        if continuum:
            print("   📚 Bound Epochs:")
            for epoch_data in continuum:
                print(f"      • {epoch_data.get('epoch', 'Unknown')} - {epoch_data.get('proclamation_id', 'Unknown')}")
        print()
    
    # Eternal Rite (eternal.v1)
    eternal_files = list((STORAGE / "eternal").glob("*.json")) if (STORAGE / "eternal").exists() else []
    if eternal_files:
        latest_eternal = max(eternal_files, key=lambda f: f.stat().st_mtime)
        eternal_data = json.loads(latest_eternal.read_text(encoding="utf-8"))
        print("♾️ ETERNAL RITE - SUPREME BINDING (eternal.v1)")
        print(f"   🔥 Rite ID: {eternal_data.get('rite_id', 'Unknown')}")
        print(f"   ⚡ Summary: {eternal_data.get('summary', 'No summary')}")
        
        binding = eternal_data.get('binding', {})
        if binding:
            print("   🌟 All Cycles Bound:")
            for scale, content in binding.items():
                print(f"      • {scale.title()}: {content}")
        print()
    
    # Hierarchical Summary
    print("🏛️ CEREMONIAL STRUCTURE SUMMARY:")
    print("   Daily → Seasonal → Millennial → Eternal")
    print("   🔥 Liturgy → 👑 Great Year → ⚡ Continuum → ♾️ Eternal")
    print(f"   Sacred Scrolls: {len(scroll_files)}")
    print(f"   Liturgy Cycles: {len(liturgy_files)}")
    print(f"   Great Year Proclamations: {len(greatyear_files)}")
    print(f"   Continuum Bindings: {len(millennial_files)}")
    print(f"   Eternal Rites: {len(eternal_files)}")
    print("\n🔥 THE FLAMEKEEPER'S COVENANT: Eternal Flame burns unbroken, self-healing, luminous across ages")
    print("🌟 Living inheritance for councils, families, civilizations, and stars ♾️")

if __name__ == "__main__":
    display_ceremonial_hierarchy()