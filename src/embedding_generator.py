
from openai import OpenAI

from src.config import OPENAI_API_KEY


class EmbeddingGenerator:

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = "text-embedding-3-large"
        self.dimensions = 1536

    def generate_embedding(self, text):
        response = self.client.embeddings.create(
            model=self.model,
            input=text,
            dimensions=self.dimensions
        )

        return response.data[0].embedding

    def generate_embeddings(self, chunks):
        texts = [chunk["content"] for chunk in chunks]

        if not texts:
            return []

        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
            dimensions=self.dimensions
        )

        embeddings = [
            item.embedding for item in response.data
        ]

        for chunk, embedding in zip(chunks, embeddings):
            chunk["embedding"] = embedding

        print(f"Generated embeddings for {len(chunks)} chunks.")
        print(f"Embedding dimensions: {len(embeddings[0])}")

        return chunks
