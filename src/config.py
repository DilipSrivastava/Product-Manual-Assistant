import os
from dotenv import load_dotenv

# Load environment variables from the project root .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv(
    "PINECONE_INDEX_NAME",
    "product-manual-index"
)

# Validate required configuration
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing in .env")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY is missing in .env")

print("Configuration loaded successfully.")
print(f"Pinecone index name: {PINECONE_INDEX_NAME}")
