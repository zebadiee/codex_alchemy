import os
import json
import argparse
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Missing OPENAI_API_KEY in environment.")

client = OpenAI(api_key=api_key)

glyphs = {
    "evolve": {"description": "Trigger symbolic transformation."},
    "transform": {"description": "Reshape internal symbolic form."},
    "reveal": {"description": "Lift veils, expose hidden truth."},
    "stabilize": {"description": "Anchor structures, harmonize flow."},
}

def get_model_name(use_pro):
    return "gpt-4o" if use_pro else "gpt-3.5-turbo"

def evolve_assistant():
    evolution_log = "evolution_history.json"
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "upgrade": "Symbolic intelligence evolved",
        "version": "1.0.0",
        "directives": ["evolve", "renew", "assist", "preserve"]
    }
    try:
        with open(evolution_log, "r") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []
    history.append(entry)
    with open(evolution_log, "w") as f:
        json.dump(history, f, indent=2)
    print(f"🧬 Evolution event recorded. Total: {len(history)}")

def run_session(use_pro=False):
    model = get_model_name(use_pro)
    log_file = "interaction_log.json"
    print("\n🧿 Codex Assistant Online — type 'exit' to quit.\n")

    history = []
    interaction_count = 0
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            history = json.load(f)

    while True:
        user_input = input("You 🔹: ").strip()
        if user_input.lower() == "exit":
            print("🛑 Codex Assistant Session Ended.")
            break

        for key in glyphs:
            if key.lower() in user_input.lower():
                context = glyphs[key].get("description", "")
                user_input += f"\n[context: {context}]"
                break

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": user_input}],
                temperature=0.7,
            )
            assistant_msg = response.choices[0].message.content.strip()
        except Exception as e:
            assistant_msg = f"⚠️ Assistant Error: {e}"

        print("Codex 🤖:", assistant_msg)

        timestamp = datetime.utcnow().isoformat() + "Z"
        history.append({
            "timestamp": timestamp,
            "user": user_input,
            "assistant": assistant_msg
        })

        with open(log_file, "w") as f:
            json.dump(history, f, indent=2)

        interaction_count += 1
        if interaction_count % 5 == 0:
            evolve_assistant()

        if len(history) >= 10:
            recent = history[-10:]
            summary_prompt = "Summarize the following symbolic dialog:\n" + "\n".join(
                f"{x['user']} => {x['assistant']}" for x in recent
            )
            try:
                reflection = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": summary_prompt}],
                ).choices[0].message.content.strip()
                print("\n🧠 Reflection:", reflection)
            except Exception:
                pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pro", action="store_true", help="Use GPT-4o instead of GPT-3.5")
    args = parser.parse_args()
    run_session(use_pro=args.pro)

