import os
import re
import tempfile
import shutil
import pytest
from backend.capsule_api import CodexAutomationCapsule

def test_initialization_and_identity():
    capsule = CodexAutomationCapsule("CustodianX", "sectorY", "epochZ")
    assert capsule.custodian_id == "CustodianX"
    assert capsule.sector == "sectorY"
    assert capsule.epoch == "epochZ"
    assert capsule.replay_log == []

def test_replay_logging_and_lineage(tmp_path, monkeypatch):
    log_path = tmp_path / "capsule_events.log"
    monkeypatch.setattr(CodexAutomationCapsule, "LOG_PATH", str(log_path))
    capsule = CodexAutomationCapsule("A", "B", "C")
    entry1 = capsule.log_replay()
    assert entry1["custodian"] == "A"
    assert entry1["sector"] == "B"
    assert entry1["epoch"] == "C"
    assert "timestamp" in entry1
    entry2 = capsule.log_replay()
    assert len(capsule.replay_log) == 2
    # Check log file
    with open(log_path) as f:
        lines = f.readlines()
    assert len(lines) == 2
    assert all("event': 'replay'" in l for l in lines)

def test_activation_flow_and_ceremonial(monkeypatch, tmp_path):
    log_path = tmp_path / "capsule_events.log"
    monkeypatch.setattr(CodexAutomationCapsule, "LOG_PATH", str(log_path))
    capsule = CodexAutomationCapsule("C1", "S1", "E1")
    result = capsule.activate_capsule()
    assert "log" in result and "modules" in result and "artifacts" in result and "oathstone" in result
    assert result["message"].startswith("Codex Capsule Activated")
    # Check log file for activation event
    with open(log_path) as f:
        lines = f.readlines()
    assert any("event': 'activation'" in l for l in lines)

def test_sectoral_invocation_keys(monkeypatch, tmp_path):
    log_path = tmp_path / "capsule_events.log"
    monkeypatch.setattr(CodexAutomationCapsule, "LOG_PATH", str(log_path))
    capsule = CodexAutomationCapsule("C2", "S2", "E2")
    assert "Ledger Flame" in capsule.invoke_sector_key("finance")
    assert "Scroll of Insight" in capsule.invoke_sector_key("EDUCATION")
    assert "No invocation key found" in capsule.invoke_sector_key("unknown")
    # Check log file for invocation event
    with open(log_path) as f:
        lines = f.readlines()
    assert any("event': 'invocation'" in l for l in lines)

def test_oathstone_binding():
    capsule = CodexAutomationCapsule("C3", "S3", "E3")
    assert "Oathstone Bound" in capsule.bind_oathstone()

def test_timestamp_integrity():
    capsule = CodexAutomationCapsule("C4", "S4", "E4")
    t1 = capsule.get_timestamp()
    t2 = capsule.get_timestamp()
    # ISO-8601 UTC format
    assert re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.*Z?", t1)
    assert t1 <= t2

def test_file_logging_integration(tmp_path, monkeypatch):
    log_path = tmp_path / "capsule_events.log"
    monkeypatch.setattr(CodexAutomationCapsule, "LOG_PATH", str(log_path))
    capsule = CodexAutomationCapsule("C5", "S5", "E5")
    for _ in range(3):
        capsule.activate_capsule()
    with open(log_path) as f:
        lines = f.readlines()
    assert len([l for l in lines if "event': 'activation'" in l]) == 3
    # Optional: test log rotation (simulate large file)
    with open(log_path, "a") as f:
        f.write("x" * 1024 * 1024)  # 1MB
    size = os.path.getsize(log_path)
    assert size > 1024 * 1024
    # (Rotation/archival logic would be tested here if implemented)
