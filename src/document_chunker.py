
import re

#structure-based chunking strategy with a maximum character limit.
#Here I have implemented two main techniques
#1. Structure-based chunking
#2. Fixed-size chunking as a fallback
class DocumentChunker:

    def __init__(self, max_chunk_size=1200, min_chunk_size=50):
        self.max_chunk_size = max_chunk_size
        self.min_chunk_size = min_chunk_size

    def chunk_documents(self, documents):
        chunks = []

        for document in documents:
            content = document["content"]
            #1. Structure-based chunking
            sections = re.split(
                r"\n\s*\n|(?=^[A-Z][A-Z0-9 /&(),:-]{3,}$)", #This finds a blank line and splits the text there.
                content,
                flags=re.MULTILINE
            )

            sections = [
                section.strip()
                for section in sections
                if section.strip()
            ]

            # Split any section that exceeds the maximum size 1200.
            split_sections = []

            for section in sections:
                while len(section) > self.max_chunk_size:
                    split_at = section.rfind(
                        " ", 0, self.max_chunk_size + 1
                    )

                    if split_at <= 0:
                        split_at = self.max_chunk_size

                    split_sections.append(section[:split_at].strip())
                    section = section[split_at:].strip()

                if section:
                    split_sections.append(section)

            # Combine sections into chunks without exceeding the limit.
            current_chunk = ""

            for section in split_sections:
                candidate = (
                    f"{current_chunk}\n{section}"
                    if current_chunk else section
                )

                if len(candidate) <= self.max_chunk_size:
                    current_chunk = candidate
                else:
                    if current_chunk:
                        chunks.append({
                            "chunk_id": (
                                f"{document['source']}_"
                                f"page{document['page']}_"
                                f"{len(chunks)}"
                            ),
                            "source": document["source"],
                            "page": document["page"],
                            "content": current_chunk
                        })

                    current_chunk = section

            if current_chunk:
                chunks.append({
                    "chunk_id": (
                        f"{document['source']}_"
                        f"page{document['page']}_"
                        f"{len(chunks)}"
                    ),
                    "source": document["source"],
                    "page": document["page"],
                    "content": current_chunk
                })

        print(f"Total chunks created: {len(chunks)}")
        return chunks
