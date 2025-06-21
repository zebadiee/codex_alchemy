import json

filename = "codex_vault.json"

with open(filename, "r") as f:
    data = json.load(f)

if isinstance(data, list):
    print("⚠️ Vault is a list — converting to dict with 'RecoveredSigil'")
    new_data = {"RecoveredSigil": data}
    with open(filename, "w") as f:
        json.dump(new_data, f, indent=2)
    print("✅ Vault repaired. All entries now under 'RecoveredSigil'.")
elif isinstance(data, dict):
    print("✅ Vault format looks good.")
else:
    print("❌ Unknown vault format. Manual intervention needed.")

