import re

def reduce_prompt(prompt: str, verbose=False) -> str:
    original = prompt
    compressed = prompt

    # Common phrase reductions
    substitutions = [
        (r"(?i)\bplease\s+(can you|could you)\b", "🧾"),
        (r"(?i)\bplease\s+(summarize|list|explain)\b", r"\1"),
        (r"(?i)\bwhat is the\b", ""),  # remove redundant questions
        (r"(?i)\bi want you to\b", ""),
        (r"(?i)\bit is important to\b", ""),
        (r"(?i)\bin the context of\b", ""),
        (r"(?i)\bmake sure to\b", "ensure"),
        (r"(?i)\bI would like to\b", "want to"),
        (r"(?i)\bplease\b", "⤵️"),
        (r"(?i)\bthank you\b", "🙏"),
    ]

    # Apply substitutions
    for pattern, repl in substitutions:
        compressed = re.sub(pattern, repl, compressed)

    # Collapse repeated newlines and whitespace
    compressed = re.sub(r"\n\s*\n", "\n", compressed)
    compressed = re.sub(r"\s+", " ", compressed).strip()

    # Compress lists and patterns
    compressed = re.sub(r"(?i)(-|\*)\s+(.*?)\s*(?=\n|$)", r"• \2", compressed)
    compressed = re.sub(r"\b(step|phase|part)\s*\d+\b", "↪️", compressed)

    if verbose:
        print("🔻 Prompt Compression Applied")
        print(f"🔠 Original Length: {len(original)} → {len(compressed)} chars")

    return compressed
