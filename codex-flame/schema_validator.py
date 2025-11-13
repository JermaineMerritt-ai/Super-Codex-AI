"""
CODEX-FLAME Schema Validator
Sacred JSON schema validation for ceremonial data integrity

This module provides schema validation for all ceremonial data structures
to ensure data integrity and consistency across the Sacred Flame Architecture.
"""

import json
import os
from typing import Dict, Any, List, Union
from datetime import datetime, timezone
import jsonschema
from pathlib import Path

class CeremonialSchemaValidator:
    """Validates ceremonial data against sacred schemas"""
    
    def __init__(self):
        self.schema_dir = Path(__file__).parent / "schemas"
        self.schemas = self._load_schemas()
    
    def _load_schemas(self) -> Dict[str, Any]:
        """Load all ceremonial schemas"""
        schema_file = self.schema_dir / "ceremonial_schemas.json"
        
        if not schema_file.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_file}")
        
        with open(schema_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def validate_treasury_binding(self, data: Dict[str, Any]) -> bool:
        """Validate treasury binding data"""
        try:
            jsonschema.validate(data, self.schemas["definitions"]["treasuryBinding"])
            return True
        except jsonschema.ValidationError as e:
            print(f"🔥 Treasury binding validation failed: {e.message}")
            return False
    
    def validate_eternal_recognition(self, data: Dict[str, Any]) -> bool:
        """Validate eternal recognition data"""
        try:
            jsonschema.validate(data, self.schemas["definitions"]["eternalRecognition"])
            return True
        except jsonschema.ValidationError as e:
            print(f"🔥 Eternal recognition validation failed: {e.message}")
            return False
    
    def validate_flame_keeper(self, data: Dict[str, Any]) -> bool:
        """Validate flame keeper data"""
        try:
            jsonschema.validate(data, self.schemas["definitions"]["flameKeeper"])
            return True
        except jsonschema.ValidationError as e:
            print(f"🔥 Flame keeper validation failed: {e.message}")
            return False
    
    def validate_liturgical_ceremony(self, data: Dict[str, Any]) -> bool:
        """Validate liturgical ceremony data"""
        try:
            jsonschema.validate(data, self.schemas["definitions"]["liturgicalCeremony"])
            return True
        except jsonschema.ValidationError as e:
            print(f"🔥 Liturgical ceremony validation failed: {e.message}")
            return False
    
    def validate_sacred_honor(self, data: Dict[str, Any]) -> bool:
        """Validate sacred honor data"""
        try:
            jsonschema.validate(data, self.schemas["definitions"]["sacredHonor"])
            return True
        except jsonschema.ValidationError as e:
            print(f"🔥 Sacred honor validation failed: {e.message}")
            return False
    
    def validate_triumvirate_member(self, data: Dict[str, Any]) -> bool:
        """Validate triumvirate member data"""
        try:
            jsonschema.validate(data, self.schemas["definitions"]["triumvirateMember"])
            return True
        except jsonschema.ValidationError as e:
            print(f"🔥 Triumvirate member validation failed: {e.message}")
            return False
    
    def validate_sacred_contract(self, data: Dict[str, Any]) -> bool:
        """Validate sacred contract data"""
        try:
            jsonschema.validate(data, self.schemas["definitions"]["sacredContract"])
            return True
        except jsonschema.ValidationError as e:
            print(f"🔥 Sacred contract validation failed: {e.message}")
            return False
    
    def validate_ceremonial_manifest(self, data: Dict[str, Any]) -> bool:
        """Validate ceremonial manifest data"""
        try:
            jsonschema.validate(data, self.schemas["ceremonialManifest"])
            return True
        except jsonschema.ValidationError as e:
            print(f"🔥 Ceremonial manifest validation failed: {e.message}")
            return False
    
    def validate_any_ceremonial_data(self, data: Dict[str, Any], data_type: str) -> bool:
        """Validate any ceremonial data by type"""
        validators = {
            "treasury": self.validate_treasury_binding,
            "recognition": self.validate_eternal_recognition,
            "keeper": self.validate_flame_keeper,
            "ceremony": self.validate_liturgical_ceremony,
            "honor": self.validate_sacred_honor,
            "triumvirate": self.validate_triumvirate_member,
            "contract": self.validate_sacred_contract,
            "manifest": self.validate_ceremonial_manifest
        }
        
        validator = validators.get(data_type.lower())
        if not validator:
            print(f"🔥 Unknown data type for validation: {data_type}")
            return False
        
        return validator(data)
    
    def generate_validation_report(self, ceremonial_data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Generate comprehensive validation report for all ceremonial data"""
        report = {
            "validation_timestamp": datetime.now(timezone.utc).isoformat(),
            "total_records": 0,
            "valid_records": 0,
            "invalid_records": 0,
            "validation_results": {},
            "errors": []
        }
        
        for data_type, records in ceremonial_data.items():
            type_results = {
                "total": len(records),
                "valid": 0,
                "invalid": 0,
                "errors": []
            }
            
            for record in records:
                try:
                    if self.validate_any_ceremonial_data(record, data_type):
                        type_results["valid"] += 1
                        report["valid_records"] += 1
                    else:
                        type_results["invalid"] += 1
                        report["invalid_records"] += 1
                except Exception as e:
                    type_results["invalid"] += 1
                    report["invalid_records"] += 1
                    type_results["errors"].append(str(e))
                    report["errors"].append(f"{data_type}: {str(e)}")
                
                report["total_records"] += 1
            
            report["validation_results"][data_type] = type_results
        
        return report

def create_sample_ceremonial_data() -> Dict[str, List[Dict[str, Any]]]:
    """Create sample data for validation testing"""
    now = datetime.now(timezone.utc).isoformat()
    
    return {
        "treasury": [{
            "binding_id": "TRE-2025-11-12-ABCDEF01",
            "timestamp": now,
            "resource_type": "SACRED_COINS",
            "amount": 1000,
            "operation": "ALLOCATION",
            "custodian": "Master Treasurer",
            "purpose": "Ceremonial preparations",
            "sacred_seal": "🔱⚡🔥"
        }],
        "recognition": [{
            "recognition_id": "ERS-2025-11-12-ABCDEF01",
            "timestamp": now,
            "honoree": "Sacred Keeper",
            "honor_type": "VALOR",
            "recognition_level": "GOLD",
            "deed_description": "Heroic defense of the Sacred Flame",
            "lineage_reference": "Ancient Line of Guardians",
            "eternal_seal": "🌟👑🔥"
        }],
        "keeper": [{
            "keeper_id": "FKP-2025-11-12-ABCDEF01",
            "timestamp": now,
            "keeper_name": "Guardian Prime",
            "flame_assignment": "Central Sacred Flame",
            "duty_type": "PRIMARY_GUARDIAN",
            "sacred_vows": "To tend the flame eternally",
            "ordination_seal": "🔥🛡️⚔️"
        }]
    }

def main():
    """Test the validation system"""
    print("🔥🔥🔥 CODEX-FLAME SCHEMA VALIDATION TEST 🔥🔥🔥")
    print("=" * 60)
    
    try:
        validator = CeremonialSchemaValidator()
        sample_data = create_sample_ceremonial_data()
        
        # Test individual validations
        print("🔥 Testing individual validations...")
        for data_type, records in sample_data.items():
            for record in records:
                is_valid = validator.validate_any_ceremonial_data(record, data_type)
                status = "✅ VALID" if is_valid else "❌ INVALID"
                print(f"   {data_type.upper()}: {status}")
        
        print("\n🔥 Generating comprehensive validation report...")
        report = validator.generate_validation_report(sample_data)
        
        print(f"   Total Records: {report['total_records']}")
        print(f"   Valid Records: {report['valid_records']}")
        print(f"   Invalid Records: {report['invalid_records']}")
        
        if report['errors']:
            print(f"   Errors: {len(report['errors'])}")
            for error in report['errors'][:3]:  # Show first 3 errors
                print(f"     - {error}")
        
        print("\n🌟 Schema validation system operational! 🌟")
        
    except Exception as e:
        print(f"❌ Schema validation test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()