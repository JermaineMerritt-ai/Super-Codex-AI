import unittest
import os
import tempfile
from backend.capsule_api import CodexAutomationCapsule

class TestCodexAutomationCapsule(unittest.TestCase):
    def setUp(self):
        # Use a temp file for logging
        self.tempdir = tempfile.TemporaryDirectory()
        self.log_path = os.path.join(self.tempdir.name, "capsule_events.log")
        CodexAutomationCapsule.LOG_PATH = self.log_path
        self.capsule = CodexAutomationCapsule("Jermaine of Waxhaw", "interstellar", "Founding Era")

    def test_initialization(self):
        self.assertEqual(self.capsule.custodian_id, "Jermaine of Waxhaw")
        self.assertEqual(self.capsule.sector, "interstellar")
        self.assertEqual(self.capsule.epoch, "Founding Era")
        self.assertEqual(len(self.capsule.replay_log), 0)

    def test_log_replay(self):
        self.capsule.log_replay()
        self.assertEqual(len(self.capsule.replay_log), 1)
        entry = self.capsule.replay_log[0]
        self.assertIn("custodian", entry)
        self.assertIn("timestamp", entry)

    def test_activation_flow(self):
        self.capsule.activate_capsule()
        # After activation, replay_log should have one entry
        self.assertEqual(len(self.capsule.replay_log), 1)

    def test_sectoral_invocation_valid(self):
        self.capsule.invoke_sector_key("finance")  # should trigger Ledger Flame
        self.capsule.invoke_sector_key("Education")  # case-insensitive

    def test_sectoral_invocation_invalid(self):
        self.capsule.invoke_sector_key("unknown")  # should print no key found

    def test_timestamp_format(self):
        ts = self.capsule.get_timestamp()
        self.assertTrue(ts.endswith("Z") or "T" in ts)  # ISO-like format

    def test_file_logging(self):
        self.capsule.log_replay()
        self.assertTrue(os.path.exists(self.log_path))
        with open(self.log_path, "r") as f:
            contents = f.read()
        self.assertIn("Jermaine of Waxhaw", contents)

    def tearDown(self):
        self.tempdir.cleanup()

if __name__ == "__main__":
    unittest.main()
