
from src.embedding_generator import EmbeddingGenerator
from src.vector_store import VectorStore


class VectorRetriever:

    def __init__(self):
        self.embedding_generator = EmbeddingGenerator()
        self.vector_store = VectorStore()

    def search(self, query, top_k=5):
        # 1. Convert the user's question into an embedding
        query_embedding = (
            self.embedding_generator.generate_embedding(query)
        )

        # 2. Search Pinecone for similar chunks
        matches = self.vector_store.search(
            query_embedding,
            top_k=top_k
        )

        # 3. Return the matching chunks
        results = []

        for match in matches:
            results.append({
                "chunk_id": match.id,
                "source": match.metadata.get("source", "Unknown"),
                "page": match.metadata.get("page"),
                "content": match.metadata.get("content", ""),
                "vector_score": float(match.score)
            })

        return results
