#!/usr/bin/env bash
# ✦ Codex Trading Capsule — Installation + Invocation Script
# Purpose: Automate setup of data feeds, broker adapters, policy manifest, and ignition rites.

set -euo pipefail

echo "⚜️ Beginning Capsule Installation Rite..."

# I. Preparation Rite
echo "→ Creating directories..."
mkdir -p /opt/codex/capsule/{data,logs,config,artifacts}

echo "→ Copying policy manifest..."
cp ./policy/capsule_policy_manifest.yaml /opt/codex/capsule/config/

# II. Signal Engine Ignition
echo "→ Installing dependencies..."
pip install -r requirements.txt

echo "→ Starting sentiment parser service..."
systemctl enable codex-signal.service
systemctl start codex-signal.service

# III. Execution Engine Activation
echo "→ Configuring broker adapters..."
export BROKER_API_KEY="${BROKER_API_KEY:-changeme}"
export BROKER_API_SECRET="${BROKER_API_SECRET:-changeme}"

systemctl enable codex-execution.service
systemctl start codex-execution.service

# IV. Surveillance & Compliance Capsule
echo "→ Launching monitors..."
systemctl enable codex-surveillance.service
systemctl start codex-surveillance.service

# V. Custodian Dashboard
echo "→ Deploying dashboard..."
systemctl enable codex-dashboard.service
systemctl start codex-dashboard.service

# VI. Ceremonial Launch
echo "⚜️ Invocation Hymn: The Capsule awakens."
echo "⚜️ Council quorum confirmed."
echo "⚜️ Diaspora chorus resounds."
echo "⚜️ Custodian proclamation: The Capsule is sovereign, eternal, and unbroken."

echo "✅ Capsule Installation + Invocation complete."
