import pytest
import os
import tempfile
from backend.capsule_api import CodexAutomationCapsule

@pytest.fixture
def capsule(tmp_path, monkeypatch):
    log_path = tmp_path / "capsule_events.log"
    monkeypatch.setattr(CodexAutomationCapsule, "LOG_PATH", str(log_path))
    return CodexAutomationCapsule("Jermaine of Waxhaw", "interstellar", "Founding Era")

def test_initialization(capsule):
    assert capsule.custodian_id == "Jermaine of Waxhaw"
    assert capsule.sector == "interstellar"
    assert capsule.epoch == "Founding Era"
    assert capsule.replay_log == []

def test_log_replay(capsule):
    capsule.log_replay()
    assert len(capsule.replay_log) == 1
    entry = capsule.replay_log[0]
    assert "custodian" in entry
    assert "timestamp" in entry
    assert os.path.exists(CodexAutomationCapsule.LOG_PATH)

@pytest.mark.parametrize("domain,expected", [
    ("finance", "Invoke Ledger Flame"),
    ("education", "Invoke Scroll of Insight"),
    ("diaspora", "Invoke Ancestral Dispatch"),
    ("governance", "Invoke Seal of Accord"),
])
def test_sectoral_invocation_valid(capsule, domain, expected):
    result = capsule.invoke_sector_key(domain)
    assert expected in result

def test_sectoral_invocation_invalid(capsule):
    result = capsule.invoke_sector_key("unknown")
    assert "No invocation key found" in result

def test_activation_flow(capsule):
    capsule.activate_capsule()
    assert len(capsule.replay_log) == 1

def test_timestamp_format(capsule):
    ts = capsule.get_timestamp()
    assert "T" in ts  # ISO-like format
