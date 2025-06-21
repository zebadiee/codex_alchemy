def refine_script(script: str, feedback: dict) -> str:
    rating = feedback.get("rating", 0)
    comments = feedback.get("comments", "")
    improvements = []

    if rating <= 2:
        improvements.append("# ⚠️ Suggestion: Add error handling or break down logic")
    if "doc" in comments.lower():
        improvements.append("# 📚 Add inline documentation or usage comments")
    if "perf" in comments.lower() or "slow" in comments.lower():
        improvements.append("# ⚡ Consider optimizing loop or I/O operations")
    if "security" in comments.lower():
        improvements.append("# 🔐 Add input validation or sanitize user input")

    return script + "\n\n" + "\n".join(improvements) 