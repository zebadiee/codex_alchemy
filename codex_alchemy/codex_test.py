# codex_test.py — Symbolic System Validator

import os
import json
from vault import Vault, Glyph

def test_vault_exists():
    assert os.path.exists("codex_vault.json"), "❌ Vault file is missing."

def test_vault_format():
    with open("codex_vault.json", "r") as f:
        data = json.load(f)
    assert isinstance(data, list), "❌ Vault format invalid."
    assert all("name" in g and "vector" in g for g in data), "❌ Missing glyph keys."
    assert all(isinstance(g["vector"], list) for g in data), "❌ Invalid vector format."

def test_vector_length():
    with open("codex_vault.json", "r") as f:
        data = json.load(f)
    lengths = set(len(g["vector"]) for g in data)
    assert len(lengths) == 1, f"❌ Inconsistent vector lengths: {lengths}"

def test_hash_consistency():
    v = Vault()
    glyphs = v.restore()
    for g in glyphs:
        h1 = v._hash(g)
        stored_hash = [e["hash"] for e in v.entries if e["name"] == g.name]
        assert stored_hash and h1 == stored_hash[0], f"❌ Hash mismatch: {g.name}"

def run_all():
    print("🔍 Running Codex Validation Suite...")
    test_vault_exists()
    test_vault_format()
    test_vector_length()
    test_hash_consistency()
    print("✅ All symbolic tests passed.")

if __name__ == "__main__":
    run_all()

