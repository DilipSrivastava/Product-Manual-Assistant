
import streamlit as st

from src.document_loader import DocumentLoader
from src.document_chunker import DocumentChunker
from src.vector_retriever import VectorRetriever
from src.answer_generator import AnswerGenerator


st.set_page_config(
    page_title="Product Manual Assistant",
    page_icon="📘",
    layout="wide"
)


@st.cache_resource
def initialize_assistant():
    loader = DocumentLoader()
    documents = loader.load_documents()

    chunker = DocumentChunker(max_chunk_size=1200)
    chunks = chunker.chunk_documents(documents)

    retriever = VectorRetriever()

    answer_generator = AnswerGenerator()

    return retriever, answer_generator, len(documents), len(chunks)


st.title("📘 Product Manual Assistant")
st.write(
    "Ask questions about your product manual. "
    "Answers are generated using retrieved manual content."
)

try:
    retriever, answer_generator, page_count, chunk_count = (
        initialize_assistant()
    )

    with st.sidebar:
        st.subheader("Knowledge Base")
        st.write(f"Pages loaded: {page_count}")
        st.write(f"Chunks indexed: {chunk_count}")
        st.write("Vector database: Pinecone")
  
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input(
        "Ask a question about your washing machine..."
    )

    if question:
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching the manual and preparing an answer..."):
                retrieved_chunks = retriever.search(
                    question,
                    top_k=5
                )

                answer = answer_generator.generate_answer(
                    question,
                    retrieved_chunks
                )

            st.markdown(answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

except Exception as exc:
    st.error("Unable to initialize the Product Manual Assistant.")
    st.exception(exc)
