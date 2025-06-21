import asyncio
import json
import os
from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
from agent.tools.token_guard import reduce_prompt
import tiktoken
import openai
from langchain_core.runnables.base import Runnable
from langchain_openai import ChatOpenAI

# === Config ===
CONFIG_PATH = Path.home() / "codex_alchemy" / "agent_config.json"
if CONFIG_PATH.exists():
    with open(CONFIG_PATH) as f:
        config = json.load(f)
else:
    config = {}

USE_TOKEN_GUARD = config.get("token_guard", True)
MAX_TOKENS = config.get("max_tokens", 7000)
MODEL_NAME = config.get("model", "gpt-4")

# === Token Counting ===
def count_tokens(text: str, model_name: str = MODEL_NAME) -> int:
    enc = tiktoken.encoding_for_model(model_name)
    return len(enc.encode(text))

# === Ritual Logger ===
def log_ritual_event(mode: str, prompt: str, output: str):
    log_path = Path.home() / "codex_alchemy" / "vault" / "ritual_log.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a") as f:
        f.write(json.dumps({
            "mode": mode,
            "prompt": prompt,
            "output": output,
        }) + "\n")

# === Safe Model Call ===
async def safe_call_chat_model(prompt: str, model: Runnable):
    if USE_TOKEN_GUARD:
        prompt = reduce_prompt(prompt, verbose=True)

    print("🔻 Prompt Compression Applied")
    tokens = count_tokens(prompt)
    print(f"🧮 Token Count: {tokens}")

    if tokens > MAX_TOKENS:
        raise ValueError(f"🚨 Compressed prompt still exceeds max tokens: {tokens} > {MAX_TOKENS}")

    try:
        async for chunk in model.astream(prompt):  # 🛠️ Fixed input format here
            yield chunk
    except openai.RateLimitError:
        print("⏳ Rate limit hit. Retrying in 5 seconds...")
        await asyncio.sleep(5)
        async for chunk in model.astream(prompt):
            yield chunk

# === Agent Monologue Entry ===
async def monologue(prompt: str, mode: str = "reflect"):
    model = ChatOpenAI(model_name=MODEL_NAME, streaming=True)

    print("📡 Running Gene...\n")
    print(f"💭 Mode: {mode.upper()}")
    print(f"🔮 {prompt} ✨\n")

    output = ""
    async for chunk in safe_call_chat_model(prompt, model):
        output += chunk.content
        print(chunk.content, end="", flush=True)

    log_ritual_event(mode, prompt, output)

# === CLI Entry Point ===
if __name__ == "__main__":
    import sys

    args = sys.argv[1:]
    instruction = args[0] if len(args) > 0 else "Hello from Gene"
    mode = args[2] if "--mode" in args else "reflect"

    asyncio.run(monologue(instruction, mode))
