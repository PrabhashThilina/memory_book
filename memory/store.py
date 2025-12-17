from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
import uuid
from typing import Dict, Any, Optional


@dataclass
class MemoryItem:
    id: str
    content: str
    created_at: str
    memory_type: str  # e.g., "event", "feeling", "reflection"
    tags: Optional[str] = None  # comma-separated tags (optional)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_memory(content: str, memory_type: str, tags: Optional[str] = None) -> MemoryItem:
    return MemoryItem(
        id=f"mem-{uuid.uuid4().hex[:12]}",
        content=content.strip(),
        created_at=utc_now_iso(),
        memory_type=memory_type,
        tags=tags
    )


def memory_metadata(m: MemoryItem) -> Dict[str, Any]:
    md = {
        "created_at": m.created_at,
        "memory_type": m.memory_type,
    }
    if m.tags:
        md["tags"] = m.tags
    return md
