"""
Vault Diff Ritual
Compares two sigils in the vault and shows their differences
"""

from codex_alchemy.vault import restore
from codex_alchemy.utils import log

def diff_sigils(sigil_a, sigil_b):
    """Compare two sigils in the vault and show their differences"""
    try:
        glyphs_a = {g.name: g.vector for g in restore(sigil_a)}
        glyphs_b = {g.name: g.vector for g in restore(sigil_b)}
    except FileNotFoundError as e:
        log(f"❌ Error: {e}")
        return

    log(f"🔍 Comparing 🔮 '{sigil_a}' vs 🧿 '{sigil_b}'")
    log(f"📊 {sigil_a}: {len(glyphs_a)} glyphs")
    log(f"📊 {sigil_b}: {len(glyphs_b)} glyphs")
    
    only_in_a = set(glyphs_a) - set(glyphs_b)
    only_in_b = set(glyphs_b) - set(glyphs_a)
    common = set(glyphs_a) & set(glyphs_b)

    if only_in_a:
        log(f"🟥 Only in {sigil_a}: {sorted(only_in_a)}")
    if only_in_b:
        log(f"🟩 Only in {sigil_b}: {sorted(only_in_b)}")
    
    log(f"🔄 Common glyphs: {len(common)}")
    for name in sorted(common):
        if glyphs_a[name] != glyphs_b[name]:
            log(f"🟨 '{name}' differs")
        else:
            log(f"✅ '{name}' identical")
    
    if not only_in_a and not only_in_b and all(glyphs_a[name] == glyphs_b[name] for name in common):
        log("🎉 Sigils are identical!") 