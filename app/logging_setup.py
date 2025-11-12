# app/logging_setup.py
import logging, sys
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s :: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("codex")

# usage: logger.info("Workflow started %s", wid)