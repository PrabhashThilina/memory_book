from __future__ import annotations


MEMORY_PREFIXES = (
    "i feel", "i am", "i was", "today", "yesterday", "i did", "i went",
    "i met", "i saw", "i learned", "i realized", "i miss", "i love", "i hate"
)

def classify(text: str) -> str:
    t = text.strip().lower()

    # commands
    if t in ("exit", "quit", "stop"):
        return "exit"

    # explicit store
    if t.startswith("remember:") or t.startswith("store:"):
        return "memory"

    # memory-like statements
    if t.startswith(MEMORY_PREFIXES):
        return "memory"

    # questions default to chat
    if "?" in t:
        return "chat"

    # fallback
    return "chat"
