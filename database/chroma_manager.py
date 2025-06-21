import chromadb
from typing import Dict, Optional

class ChromaManager:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=".chromadb")
        self.collection = self.client.get_or_create_collection("book_chapters")
        
    def save_version(self, content: str, metadata: Dict, version_id: Optional[str] = None) -> str:
        if not version_id:
            version_id = f"ver_{len(self.collection.get()['ids'])+1}"
            
        self.collection.upsert(
            documents=[content],
            metadatas=[metadata],
            ids=[version_id]
        )
        return version_id
        
    def get_version(self, version_id: str) -> Dict:
        return self.collection.get(ids=[version_id])
        
    def search_versions(self, query: str, n_results: int = 3) -> Dict:
        return self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
