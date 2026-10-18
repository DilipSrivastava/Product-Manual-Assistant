
from openai import OpenAI

from src.config import OPENAI_API_KEY


class AnswerGenerator:

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = "gpt-4o-mini"

    def generate_answer(self, question, retrieved_chunks):
        if not retrieved_chunks:
            return (
                "I couldn't find relevant information in the "
                "available product manual."
            )

        context_parts = []

        for chunk in retrieved_chunks:
            context_parts.append(
                f"Source: {chunk['source']}, "
                f"Page: {chunk['page']}\n"
                f"Content:\n{chunk['content']}"
            )

        context = "\n\n---\n\n".join(context_parts)

        system_prompt = """
You are a helpful product manual assistant.

Answer the user's question using only the supplied manual excerpts.

Rules:
1. Do not invent instructions or product specifications.
2. If the excerpts do not contain enough information, say so clearly.
3. Keep the answer clear and easy to follow.
4. Cite supporting information using the format [Source: filename, Page: N].
5. Include citations next to the relevant instructions.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": (
                        f"Manual excerpts:\n{context}\n\n"
                        f"Question: {question}"
                    )
                }
            ],
            temperature=0
        )

        return response.choices[0].message.content
