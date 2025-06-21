#!/usr/bin/env python3
import random, json
from datetime import datetime

glyphs = {
    "focus": "Directs energy toward a task or thought",
    "chaos": "Disturbs patterns to reveal hidden forms",
    "clarity": "Sharpens perception and understanding",
    "bind": "Links concepts or elements into unity",
    "echo": "Amplifies symbolic resonance",
    "shatter": "Breaks conceptual constructs to evolve",
    "seed": "Implants ideas that grow with time",
    "veil": "Conceals intention until readiness",
    "pulse": "Energizes dormant potential",
    "forge": "Combines symbols into structured meaning"
}

ritual_templates = [
    "Bind the glyph of {glyph} with intent to {intent}.",
    "Through chaos, channel {glyph} toward {intent}.",
    "Summon clarity by invoking {glyph}, manifesting {intent}.",
    "Forge the will of {intent} with the essence of {glyph}.",
    "Let {glyph} echo through the chamber of {intent}."
]

rarity_pool = {
    "common": 0.65,
    "non_common": 0.20,
    "rare": 0.10,
    "ultra_rare": 0.05
}

def draw_glyph():
    roll = random.random()
    cumulative = 0
    for rarity, prob in rarity_pool.items():
        cumulative += prob
        if roll <= cumulative:
            glyph = random.choice(list(glyphs.keys()))
            return {"name": glyph, "rarity": rarity, "description": glyphs[glyph]}
    return {"name": "unknown", "rarity": "unknown", "description": "error"}

def invoke_ritual(glyph):
    intent = random.choice(["transformation", "insight", "rebirth", "stability", "connection"])
    template = random.choice(ritual_templates)
    ritual = template.format(glyph=glyph["name"], intent=intent)
    return {"ritual": ritual, "glyph": glyph["name"], "intent": intent}

def generate_symbolic_algorithm():
    result = []
    for _ in range(5):
        glyph = draw_glyph()
        ritual = invoke_ritual(glyph)
        result.append(ritual)
    return result

def log_rituals(rituals):
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "algorithm": rituals
    }
    try:
        with open("ritual_log.json", "r") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []
    history.append(entry)
    with open("ritual_log.json", "w") as f:
        json.dump(history, f, indent=2)

if __name__ == "__main__":
    print("🧿 Invoking symbolic algorithm (glyphs + rituals)...\n")
    rituals = generate_symbolic_algorithm()
    for r in rituals:
        print(f"🔹 Glyph: {r['glyph']} [{r['intent']}]")
        print(f"   🔁 Ritual: {r['ritual']}\n")
    log_rituals(rituals)
    print("✅ Rituals logged in 'ritual_log.json'")
