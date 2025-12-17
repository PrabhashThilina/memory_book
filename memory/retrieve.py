from __future__ import annotations
from typing import List, Dict, Any


def retrieve(collection, query_embedding: list, n_results: int) -> List[Dict[str, Any]]:
    res = collection.query(query_embeddings=[query_embedding], n_results=n_results)

    docs = res.get("documents", [[]])[0] if res.get("documents") else []
    metas = res.get("metadatas", [[]])[0] if res.get("metadatas") else []
    ids = res.get("ids", [[]])[0] if res.get("ids") else []
    dists = res.get("distances", [[]])[0] if res.get("distances") else []

    out = []
    for i in range(len(docs)):
        out.append({
            "id": ids[i] if i < len(ids) else None,
            "content": docs[i],
            "metadata": metas[i] if i < len(metas) else {},
            "distance": dists[i] if i < len(dists) else None,
        })
    return out
