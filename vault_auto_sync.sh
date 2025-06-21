#!/bin/bash

# Vault Auto-Sync Ritual
# Runs vault synchronization every 5 minutes

echo "🔄 Starting Vault Auto-Sync Ritual..."
echo "📁 Sync interval: 5 minutes"
echo "📊 Log file: sync_logs/auto_sync.out"
echo "⏰ Started at: $(date)"

while true; do
    echo "🔄 [$(date)] Running vault sync..."
    python unified_cli.py sync
    echo "✅ [$(date)] Sync completed, sleeping for 5 minutes..."
    sleep 300
done 