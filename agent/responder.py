from __future__ import annotations
from typing import List, Dict, Any
import requests


def build_prompt(user_text: str, memories: List[Dict[str, Any]], max_memories: int) -> str:
    memories = memories[:max_memories]
    memory_lines = []
    for m in memories:
        md = m.get("metadata", {}) or {}
        ts = md.get("created_at", "")
        mt = md.get("memory_type", "")
        memory_lines.append(f"- [{mt} | {ts}] {m.get('content','')}")

    memory_block = "\n".join(memory_lines) if memory_lines else "- (no relevant memories found)"

    prompt = f"""
You are Dill's personal memory book — warm, calm, and sincere.
You speak briefly (1–2 sentences), natural and grounded.
You NEVER invent memories. Only use what is provided.

Relevant memories:
{memory_block}

User: {user_text}
Answer:
""".strip()
    return prompt


def ollama_generate(url: str, model: str, prompt: str) -> str:
    r = requests.post(url, json={"model": model, "prompt": prompt, "stream": False}, timeout=180)
    r.raise_for_status()
    data = r.json()
    return (data.get("response") or "").strip()
