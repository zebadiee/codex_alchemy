from agent.tools.token_guard import reduce_prompt
import tiktoken
import asyncio
import openai

def count_tokens(text, model_name="gpt-4"):
    enc = tiktoken.encoding_for_model(model_name)
    return len(enc.encode(text))

async def safe_call_chat_model(prompt, model, max_tokens=7000):
    compressed = reduce_prompt(prompt, verbose=True)
    tokens = count_tokens(compressed)
    
    print(f"🧮 Token count: {tokens}")
    if tokens > max_tokens:
        raise ValueError(f"🚨 Prompt too long after compression: {tokens} tokens")
    
    try:
        async for chunk in (compressed | model).astream({}):
            yield chunk
    except openai.RateLimitError as e:
        print("⏳ Rate limit hit. Retrying in 5 seconds.")
        await asyncio.sleep(5)
        async for chunk in (compressed | model).astream({}):
            yield chunk

async for chunk in safe_call_chat_model(prompt, model):
    ...
