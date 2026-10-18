
from pinecone import Pinecone, ServerlessSpec

from src.config import PINECONE_API_KEY, PINECONE_INDEX_NAME


class VectorStore:

    def __init__(self):
        self.client = Pinecone(api_key=PINECONE_API_KEY)

        existing_indexes = self.client.list_indexes().names()

        if PINECONE_INDEX_NAME not in existing_indexes:
            self.client.create_index(
                name=PINECONE_INDEX_NAME,
                dimension=1536,
                metric="dotproduct",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )

        self.index = self.client.Index(PINECONE_INDEX_NAME)

    def upsert_chunks(self, chunks):
        vectors = []

        for chunk in chunks:
            if "embedding" not in chunk:
                raise ValueError(
                    f"Missing embedding for chunk: {chunk['chunk_id']}"
                )

            vectors.append({
                "id": chunk["chunk_id"],
                "values": chunk["embedding"],
                "metadata": {
                    "source": chunk["source"],
                    "page": chunk["page"],
                    "content": chunk["content"]
                }
            })

        if vectors:
            # Pinecone accepts batches; keep each request manageable.
            for start in range(0, len(vectors), 100):
                batch = vectors[start:start + 100]
                self.index.upsert(vectors=batch)

        print(f"Upserted {len(vectors)} vectors into Pinecone.")

    def search(self, query_embedding, top_k=5):
        response = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )

        return response.matches
