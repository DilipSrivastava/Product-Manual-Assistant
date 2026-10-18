
from src.document_loader import DocumentLoader
from src.document_chunker import DocumentChunker
from src.embedding_generator import EmbeddingGenerator
from src.vector_store import VectorStore


def main():
    # 1. Load manual pages
    loader = DocumentLoader()
    documents = loader.load_documents()

    if not documents:
        print("No documents found. Please check data/manuals.")
        return

    # 2. Create chunks
    chunker = DocumentChunker(max_chunk_size=1200)
    chunks = chunker.chunk_documents(documents)

    if not chunks:
        print("No chunks created.")
        return

    # 3. Generate embeddings for all chunks
    embedding_generator = EmbeddingGenerator()
    embedded_chunks = embedding_generator.generate_embeddings(chunks)

    # 4. Store vectors in Pinecone
    vector_store = VectorStore()
    vector_store.upsert_chunks(embedded_chunks)

    # 5. Verify index statistics
    stats = vector_store.index.describe_index_stats()

    print("\n--- Knowledge Base Ingestion Summary ---")
    print(f"Pages loaded: {len(documents)}")
    print(f"Chunks created: {len(chunks)}")
    print(f"Vectors in Pinecone index: {stats.total_vector_count}")


if __name__ == "__main__":
    main()
