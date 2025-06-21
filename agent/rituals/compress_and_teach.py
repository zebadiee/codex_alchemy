from agent.tools.token_guard import reduce_prompt
from agent.tools.ledger_utils import log_to_ledger

def compress_and_teach(text, label="manual-teach"):
    compressed = reduce_prompt(text, verbose=True)
    log_to_ledger({
        "original": text,
        "compressed": compressed,
        "label": label
    }, mode="train")
    return compressed
