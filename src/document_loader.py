from pathlib import Path
from pypdf import PdfReader


class DocumentLoader:

    def __init__(self, manuals_directory="data/manuals"):
        self.manuals_directory = Path(manuals_directory)

    def load_documents(self):
        documents = []

        pdf_files = list(self.manuals_directory.glob("*.pdf"))

        if not pdf_files:
            print("No PDF manuals found.")
            return documents

        for pdf_file in pdf_files:
            print(f"\nLoading manual: {pdf_file.name}")

            reader = PdfReader(str(pdf_file))

            for page_number, page in enumerate(reader.pages, start=1):
                content = page.extract_text() or ""

                if not content.strip():
                    print(f"Skipping page {page_number}: no extractable text")
                    continue

                documents.append({
                    "source": pdf_file.name,
                    "page": page_number,
                    "content": content.strip()
                })

        print(f"\nTotal pages loaded: {len(documents)}")
        return documents
