import os
import glob
import pytest
from backend.logging_utils import log_capsule_event, seal_log_with_checksum, logger

LOG_DIR = "backend/logs"

@pytest.fixture(autouse=True)
def clean_logs():
    # Close and remove all handlers before deleting log files
    handlers = logger.handlers[:]
    for handler in handlers:
        handler.close()
        logger.removeHandler(handler)
    for f in glob.glob(os.path.join(LOG_DIR, "capsule_events*")):
        try:
            os.remove(f)
        except PermissionError:
            pass
    # Re-add the handler so logging works in tests
    from backend.logging_utils import ChecksumTimedRotatingFileHandler
    import logging
    log_file = os.path.join(LOG_DIR, "capsule_events.log")
    handler = ChecksumTimedRotatingFileHandler(
        log_file, when="midnight", interval=1, backupCount=30, utc=True
    )
    formatter = logging.Formatter("%(asctime)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    yield
    # Repeat after test
    handlers = logger.handlers[:]
    for handler in handlers:
        handler.close()
        logger.removeHandler(handler)
    for f in glob.glob(os.path.join(LOG_DIR, "capsule_events*")):
        try:
            os.remove(f)
        except PermissionError:
            pass

def test_log_and_checksum_creation():
    # Write an event to create the log
    log_capsule_event("Checksum test entry")

    # Seal the log with checksum
    log_file = os.path.join(LOG_DIR, "capsule_events.log")
    checksum_file = seal_log_with_checksum(log_file)

    assert os.path.exists(log_file)
    assert os.path.exists(checksum_file)

    # Verify checksum contents include both hash and filename
    with open(checksum_file) as f:
        contents = f.read().strip()
    assert "capsule_events.log" in contents
    assert len(contents.split()[0]) == 64  # SHA256 length

def test_rotation_and_auto_checksum(tmp_path):
    # Force rollover
    handler = logger.handlers[0]
    log_capsule_event("Before rollover")
    handler.doRollover()
    log_capsule_event("After rollover")

    # Collect rotated logs and checksum files
    logs = glob.glob(os.path.join(LOG_DIR, "capsule_events*"))
    sha_files = [f for f in logs if f.endswith(".sha256")]
    log_files = [f for f in logs if not f.endswith(".sha256")]

    # Ensure at least one rotated log and its checksum exist
    assert len(log_files) >= 2
    assert len(sha_files) >= 1

    # Verify that each checksum file references its log
    for sha in sha_files:
        with open(sha) as f:
            contents = f.read().strip()
        filename = contents.split()[1]
        assert os.path.exists(os.path.join(LOG_DIR, filename))
