#!/usr/bin/env python3
"""
🧪 Test Suite for Sacred Avatar Guide System 🧪
Comprehensive testing for avatar management and ceremonial protocols

This test suite validates all aspects of the Avatar Guide system including:
- Basic avatar creation and management
- Sacred script management and delivery
- Ceremonial protocols and council operations
- Storage and persistence systems
- Treasury integration and flame blessings
"""

import unittest
import tempfile
import shutil
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

from avatar_guide_system import (
    AvatarGuide, SacredAvatarGuide, AvatarCouncil, create_sacred_avatar,
    AvatarRole, AvatarPresence, ScriptType, SacredScript, AvatarMetadata
)

class TestBasicAvatarGuide(unittest.TestCase):
    """Test the backwards-compatible AvatarGuide class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.avatar = AvatarGuide("TestAvatar", "Hello, welcome to our test realm.")
    
    def test_avatar_creation(self):
        """Test basic avatar creation"""
        self.assertEqual(self.avatar.name, "TestAvatar")
        self.assertEqual(self.avatar.script, "Hello, welcome to our test realm.")
    
    def test_basic_speak(self):
        """Test the original speak method"""
        expected = "TestAvatar says: Hello, welcome to our test realm."
        self.assertEqual(self.avatar.speak(), expected)
    
    def test_sacred_speak(self):
        """Test the enhanced sacred speak method"""
        result = self.avatar.sacred_speak()
        self.assertIn("TestAvatar", result)
        self.assertIn("authority", result)
    
    def test_enhancement_to_sacred(self):
        """Test upgrading to SacredAvatarGuide"""
        sacred = self.avatar.enhance_to_sacred_avatar()
        self.assertIsInstance(sacred, SacredAvatarGuide)
        self.assertEqual(sacred.name, "TestAvatar")
        self.assertEqual(sacred.role, AvatarRole.INITIATE)

class TestSacredScript(unittest.TestCase):
    """Test the SacredScript data class"""
    
    def test_script_creation(self):
        """Test creating a sacred script"""
        script = SacredScript(
            content="Test sacred content",
            script_type=ScriptType.WELCOME,
            authority_level=5
        )
        
        self.assertEqual(script.content, "Test sacred content")
        self.assertEqual(script.script_type, ScriptType.WELCOME)
        self.assertEqual(script.authority_level, 5)
        self.assertIsNotNone(script.creation_timestamp)
        self.assertIsNotNone(script.sacred_binding)
    
    def test_sacred_binding_generation(self):
        """Test sacred binding hash generation"""
        script1 = SacredScript("Content", ScriptType.WELCOME, 5)
        script2 = SacredScript("Content", ScriptType.WELCOME, 5)
        script3 = SacredScript("Different", ScriptType.WELCOME, 5)
        
        # Same content should generate same binding
        self.assertEqual(script1.sacred_binding, script2.sacred_binding)
        # Different content should generate different binding
        self.assertNotEqual(script1.sacred_binding, script3.sacred_binding)

class TestSacredAvatarGuide(unittest.TestCase):
    """Test the SacredAvatarGuide class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.avatar = SacredAvatarGuide(
            name="TestSacredAvatar",
            role=AvatarRole.CUSTODIAN,
            primary_script="Sacred greetings, seeker.",
            storage_root=self.temp_dir
        )
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_avatar_creation(self):
        """Test sacred avatar creation"""
        self.assertEqual(self.avatar.name, "TestSacredAvatar")
        self.assertEqual(self.avatar.role, AvatarRole.CUSTODIAN)
        self.assertEqual(self.avatar.presence, AvatarPresence.DORMANT)
        self.assertEqual(self.avatar.authority_level, 10)  # Custodian has max authority
    
    def test_directory_creation(self):
        """Test sacred directory structure creation"""
        expected_dirs = ["avatars", "scripts", "blessings", "guidance_logs", "ceremonial_records"]
        
        for dir_name in expected_dirs:
            self.assertTrue((self.temp_dir / dir_name).exists())
    
    def test_script_addition(self):
        """Test adding sacred scripts"""
        binding = self.avatar.add_script(
            "Test blessing content",
            ScriptType.BLESSING,
            authority_level=8
        )
        
        self.assertIn(ScriptType.BLESSING, self.avatar.scripts)
        self.assertIsNotNone(binding)
        
        # Check script file was saved
        script_file = self.temp_dir / "scripts" / f"{self.avatar.name}_blessing.json"
        self.assertTrue(script_file.exists())
    
    def test_presence_activation(self):
        """Test avatar presence activation"""
        self.avatar.activate_presence(AvatarPresence.ACTIVE)
        self.assertEqual(self.avatar.presence, AvatarPresence.ACTIVE)
    
    def test_speak_functionality(self):
        """Test avatar speaking with different script types"""
        # Test default speech when script not available
        result = self.avatar.speak(ScriptType.WARNING)
        self.assertIn("TestSacredAvatar", result)
        self.assertIn("danger", result)
        
        # Add custom script and test
        self.avatar.add_script("Custom warning message", ScriptType.WARNING)
        result = self.avatar.speak(ScriptType.WARNING)
        self.assertIn("Custom warning message", result)
        self.assertIn("🔥", result)  # Authority symbols
    
    def test_script_interpolation(self):
        """Test variable interpolation in scripts"""
        self.avatar.add_script(
            "Welcome, {visitor_name}, to the realm of {realm}",
            ScriptType.WELCOME
        )
        
        result = self.avatar.speak(
            ScriptType.WELCOME,
            visitor_name="Seeker",
            realm="Sacred Knowledge"
        )
        
        self.assertIn("Seeker", result)
        self.assertIn("Sacred Knowledge", result)
    
    def test_flame_blessing(self):
        """Test flame blessing functionality"""
        self.avatar.add_script("Test content", ScriptType.BLESSING)
        
        initial_resonance = self.avatar.metadata.flame_resonance
        self.assertIsNone(self.avatar.metadata.last_blessing)
        
        self.avatar.receive_flame_blessing(ScriptType.BLESSING)
        
        self.assertTrue(self.avatar.scripts[ScriptType.BLESSING].flame_blessed)
        self.assertIsNotNone(self.avatar.metadata.last_blessing)
        self.assertGreater(self.avatar.metadata.flame_resonance, initial_resonance)
    
    def test_avatar_status(self):
        """Test avatar status reporting"""
        self.avatar.add_script("Test", ScriptType.GUIDANCE)
        status = self.avatar.get_avatar_status()
        
        self.assertEqual(status["name"], "TestSacredAvatar")
        self.assertEqual(status["role"], "custodian")
        self.assertEqual(status["script_count"], 2)  # Primary + added script
        self.assertIn("guidance", status["available_scripts"])
    
    def test_profile_saving(self):
        """Test avatar profile persistence"""
        self.avatar.add_script("Test script", ScriptType.TEACHING)
        self.avatar.save_avatar_profile()
        
        profile_file = self.temp_dir / "avatars" / f"{self.avatar.name}.json"
        self.assertTrue(profile_file.exists())
        
        with open(profile_file, 'r') as f:
            profile_data = json.load(f)
        
        self.assertEqual(profile_data["avatar_status"]["name"], "TestSacredAvatar")
        self.assertIn("teaching", profile_data["scripts"])

class TestAvatarCouncil(unittest.TestCase):
    """Test the AvatarCouncil management system"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.council = AvatarCouncil(storage_root=self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_council_creation(self):
        """Test council initialization"""
        self.assertEqual(len(self.council.avatars), 0)
        
        # Check council directories
        self.assertTrue((self.temp_dir / "council_records").exists())
        self.assertTrue((self.temp_dir / "collective_ceremonies").exists())
    
    def test_avatar_summoning(self):
        """Test summoning avatars to the council"""
        avatar = self.council.summon_avatar(
            "CouncilAvatar",
            AvatarRole.COUNCIL_MEMBER,
            "I speak for the council."
        )
        
        self.assertIn("CouncilAvatar", self.council.avatars)
        self.assertEqual(avatar.role, AvatarRole.COUNCIL_MEMBER)
        self.assertEqual(avatar.presence, AvatarPresence.ACTIVE)
    
    def test_duplicate_summoning(self):
        """Test that summoning same avatar returns existing instance"""
        avatar1 = self.council.summon_avatar("TestAvatar", AvatarRole.GUARDIAN)
        avatar2 = self.council.summon_avatar("TestAvatar", AvatarRole.FLAME_KEEPER)
        
        self.assertIs(avatar1, avatar2)
        self.assertEqual(len(self.council.avatars), 1)
    
    def test_ceremony_conduction(self):
        """Test conducting ceremonial gatherings"""
        # Summon avatars
        self.council.summon_avatar("Avatar1", AvatarRole.CUSTODIAN)
        self.council.summon_avatar("Avatar2", AvatarRole.FLAME_KEEPER)
        
        # Add ceremony scripts
        for avatar in self.council.avatars.values():
            avatar.add_script(
                "We gather for sacred {ceremony_name}",
                ScriptType.CEREMONY
            )
        
        # Conduct ceremony
        self.council.conduct_ceremony("Test Ceremony")
        
        # Check ceremony record was saved
        ceremony_files = list((self.temp_dir / "collective_ceremonies").glob("Test_Ceremony_*.json"))
        self.assertTrue(len(ceremony_files) > 0)
    
    def test_council_status(self):
        """Test council status reporting"""
        self.council.summon_avatar("Avatar1", AvatarRole.CUSTODIAN)
        self.council.summon_avatar("Avatar2", AvatarRole.GUARDIAN)
        self.council.summon_avatar("Avatar3", AvatarRole.GUARDIAN)
        
        status = self.council.get_council_status()
        
        self.assertEqual(status["total_avatars"], 3)
        self.assertEqual(len(status["active_avatars"]), 3)
        self.assertEqual(status["role_distribution"]["guardian"], 2)
        self.assertEqual(status["role_distribution"]["custodian"], 1)

class TestFactoryFunction(unittest.TestCase):
    """Test the create_sacred_avatar factory function"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_valid_role_creation(self):
        """Test creating avatar with valid role"""
        avatar = create_sacred_avatar(
            "FactoryAvatar",
            "flame_keeper",
            "The flame guides us",
            storage_root=self.temp_dir
        )
        
        self.assertEqual(avatar.name, "FactoryAvatar")
        self.assertEqual(avatar.role, AvatarRole.FLAME_KEEPER)
        self.assertIn(ScriptType.WELCOME, avatar.scripts)
    
    def test_invalid_role_fallback(self):
        """Test fallback for invalid role"""
        with patch('builtins.print') as mock_print:
            avatar = create_sacred_avatar(
                "InvalidRoleAvatar",
                "invalid_role",
                storage_root=self.temp_dir
            )
            
            self.assertEqual(avatar.role, AvatarRole.INITIATE)
            
            # Check that the role error message was printed
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            self.assertIn("⚠️  Unknown role 'invalid_role', defaulting to INITIATE", print_calls)
    
    def test_role_case_insensitive(self):
        """Test that role matching is case-insensitive"""
        avatar = create_sacred_avatar(
            "CaseTestAvatar",
            "COUNCIL_MEMBER",
            storage_root=self.temp_dir
        )
        
        self.assertEqual(avatar.role, AvatarRole.COUNCIL_MEMBER)

class TestIntegration(unittest.TestCase):
    """Integration tests for the complete avatar system"""
    
    def setUp(self):
        """Set up integration test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up integration test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('avatar_guide_system.print')
    def test_treasury_integration(self, mock_print):
        """Test integration with treasury system (graceful degradation)"""
        avatar = SacredAvatarGuide(
            "TreasuryAvatar",
            AvatarRole.CUSTODIAN,
            storage_root=self.temp_dir
        )
        
        avatar.speak(ScriptType.WELCOME)
        
        # Verify treasury warning was printed (since treasury not available)
        mock_print.assert_called_with("⚠️  Treasury module not available - running in standalone mode")
    
    def test_complete_workflow(self):
        """Test a complete workflow from creation to ceremony"""
        # Create council
        council = AvatarCouncil(storage_root=self.temp_dir)
        
        # Summon avatars with different roles
        custodian = council.summon_avatar("Keeper", AvatarRole.CUSTODIAN, "I guard the sacred halls.")
        flame_keeper = council.summon_avatar("Pyrion", AvatarRole.FLAME_KEEPER, "The flame is eternal.")
        
        # Add various scripts
        custodian.add_script("Ceremony begins with sacred intent", ScriptType.CEREMONY)
        flame_keeper.add_script("The eternal flame blesses this gathering", ScriptType.BLESSING)
        
        # Apply flame blessings
        custodian.receive_flame_blessing()
        flame_keeper.receive_flame_blessing()
        
        # Conduct ceremony
        council.conduct_ceremony("Integration Test Ceremony")
        
        # Save profiles
        for avatar in council.avatars.values():
            avatar.save_avatar_profile()
        
        # Verify all files were created (avatars are in subdirectories under council structure)
        self.assertTrue((self.temp_dir / "avatars" / "Keeper" / "avatars" / "Keeper.json").exists())
        self.assertTrue((self.temp_dir / "avatars" / "Pyrion" / "avatars" / "Pyrion.json").exists())
        
        ceremony_files = list((self.temp_dir / "collective_ceremonies").glob("*.json"))
        self.assertTrue(len(ceremony_files) > 0)
        
        # Check final status (avatars will be in ceremony state after the ceremony)
        status = council.get_council_status()
        self.assertEqual(status["total_avatars"], 2)
        # Note: avatars are in ceremony state after the ceremony, not active
        # Check that all avatars exist regardless of presence state
        all_avatars = list(council.avatars.keys())
        self.assertEqual(len(all_avatars), 2)
        self.assertIn("Keeper", all_avatars)
        self.assertIn("Pyrion", all_avatars)

if __name__ == '__main__':
    # Run the comprehensive test suite
    print("🧪 Running Sacred Avatar Guide System Tests 🧪")
    print("="*60)
    
    # Create test loader and runner
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestBasicAvatarGuide,
        TestSacredScript,
        TestSacredAvatarGuide,
        TestAvatarCouncil,
        TestFactoryFunction,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n🔥 Test Results Summary 🔥")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("✅ All tests passed! The Sacred Avatar System is blessed by the eternal flame! 🕯️")
    else:
        print("❌ Some tests failed. The sacred flame requires attention to these matters.")
    
    # Exit with appropriate code
    exit_code = 0 if result.wasSuccessful() else 1
    exit(exit_code)