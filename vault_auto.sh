#!/bin/bash

SIGIL="AutoSigil_$(date +%s)"
LOGFILE="vault_auto.log"

echo "🚀 Starting Vault Automation for sigil: $SIGIL" | tee -a "$LOGFILE"

echo -e "\n🔁 [1] Preserving glyphs under sigil: $SIGIL" | tee -a "$LOGFILE"
python3 vault.py preserve "$SIGIL" 2>&1 | tee -a "$LOGFILE"

echo -e "\n📜 [2] Listing all saved vaults:" | tee -a "$LOGFILE"
python3 vault.py list 2>&1 | tee -a "$LOGFILE"

echo -e "\n♻️ [3] Restoring vault from sigil: $SIGIL" | tee -a "$LOGFILE"
python3 vault.py restore "$SIGIL" 2>&1 | tee -a "$LOGFILE"

echo -e "\n📊 [4] Vault Statistics:" | tee -a "$LOGFILE"
python3 vault.py stats 2>&1 | tee -a "$LOGFILE"

echo -e "\n✅ Vault automation completed for: $SIGIL" | tee -a "$LOGFILE"

