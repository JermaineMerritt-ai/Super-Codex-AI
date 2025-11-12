#!/usr/bin/env bash
# AXIOM CLI Shell Wrapper
# Activates virtual environment and runs the Python CLI

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment
source .venv/bin/activate

# Run the CLI with all arguments
python cli/axiom_cli.py "$@"