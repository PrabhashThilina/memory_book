import chromadb


def get_client(chroma_path: str) -> chromadb.PersistentClient:
    return chromadb.PersistentClient(path=chroma_path)


def get_collection(client: chromadb.PersistentClient, name: str):
    return client.get_or_create_collection(name=name)
