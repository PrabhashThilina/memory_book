import yaml
from sentence_transformers import SentenceTransformer

from memory.db import get_client, get_collection
from memory.store import new_memory, memory_metadata
from memory.retrieve import retrieve
from agent.classifier import classify
from agent.responder import build_prompt, ollama_generate


def load_settings():
    with open("config/settings.yaml", "r") as f:
        return yaml.safe_load(f)


def main():
    cfg = load_settings()

    embedder = SentenceTransformer(cfg["embedding_model"])

    client = get_client(cfg["chroma_path"])
    collection = get_collection(client, cfg["collection_name"])

    print("\n📘 Personal Memory Book (text-only)")
    print("Type your message. Type 'exit' to quit.\n")

    while True:
        user_text = input("You: ").strip()
        if not user_text:
            continue

        kind = classify(user_text)

        if kind == "exit":
            print("Memory Book: See you.")
            break

        if kind == "memory":
            cleaned = user_text.split(":", 1)[-1].strip()
            m = new_memory(cleaned, "reflection")

            emb = embedder.encode([m.content])[0].tolist()
            collection.add(
                ids=[m.id],
                documents=[m.content],
                embeddings=[emb],
                metadatas=[memory_metadata(m)]
            )

            print("Memory Book: I’ll remember that.\n")
            continue

        # Chat
        q_emb = embedder.encode([user_text])[0].tolist()
        memories = retrieve(collection, q_emb, cfg["retrieval"]["n_results"])

        prompt = build_prompt(
            user_text,
            memories,
            cfg["agent"]["max_memories_in_prompt"]
        )

        reply = ollama_generate(
            cfg["ollama"]["url"],
            cfg["ollama"]["model"],
            prompt
        )

        print(f"Memory Book: {reply}\n")


if __name__ == "__main__":
    main()
