#!/bin/bash

# Axiom Flame Health Check Script

API_URL="http://localhost:5000/api/registry"
TIMEOUT=10

echo "Checking Axiom Flame API health..."

# Check if API is responding
if curl -f -s --max-time $TIMEOUT "$API_URL" > /dev/null; then
    echo "✓ API is responding"
    api_status=0
else
    echo "✗ API is not responding"
    api_status=1
fi

# Check storage directories
storage_dirs=("./storage/ledger" "./storage/annals" "./storage/replays")
storage_status=0

for dir in "${storage_dirs[@]}"; do
    if [ -d "$dir" ] && [ -w "$dir" ]; then
        echo "✓ Storage directory $dir is accessible"
    else
        echo "✗ Storage directory $dir is not accessible"
        storage_status=1
    fi
done

# Check artifacts directories
artifact_dirs=("./artifacts/ceremonies" "./artifacts/honors" "./artifacts/registry")
artifact_status=0

for dir in "${artifact_dirs[@]}"; do
    if [ -d "$dir" ] && [ -w "$dir" ]; then
        echo "✓ Artifact directory $dir is accessible"
    else
        echo "✗ Artifact directory $dir is not accessible"
        artifact_status=1
    fi
done

# Overall status
if [ $api_status -eq 0 ] && [ $storage_status -eq 0 ] && [ $artifact_status -eq 0 ]; then
    echo "✓ All systems healthy"
    exit 0
else
    echo "✗ Some systems are unhealthy"
    exit 1
fi