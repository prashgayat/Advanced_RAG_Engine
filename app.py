# app.py

from utils.env_loader import load_environment
load_environment()

import streamlit as st
from utils.file_utils import save_uploaded_file, load_file_content
from splitter.HybridTextSplitter import HybridTextSplitter
from retriever.retriever_utils import hybrid_retriever
from memory.memory_manager import MemoryManager
from dotenv import load_dotenv
from utils.fallback_utils import detect_no_retrieval, fallback_menu, execute_fallback_action
from llm_answer import llm_answer

load_dotenv()

st.set_page_config(page_title="Advanced Semantic RAG Engine", page_icon="🧠")
st.title("Welcome to the Advanced Semantic RAG Engine 🧠")
st.subheader("Built for robust ingestion and advanced semantic retrieval 🚀")

def infer_keywords_from_filename(filename: str) -> list:
    filename = filename.lower()
    if "insurance" in filename:
        return ["Policy", "Premium", "Coverage", "Risk", "Claim", "Underwriting", "Exclusions"]
    elif "real estate" in filename or "property" in filename:
        return ["Property", "Valuation", "Investment", "Rental", "Mortgage", "Ownership", "Lease"]
    elif "health" in filename or "medical" in filename:
        return ["Diagnosis", "Treatment", "Symptoms", "Prevention", "Medication", "Health Plan", "Procedure"]
    elif "business" in filename or "proposal" in filename:
        return ["Executive Summary", "Objectives", "Strategy", "Market Analysis", "Operations", "Financials", "Conclusion"]
    elif "academic" in filename or "research" in filename:
        return ["Abstract", "Introduction", "Methods", "Results", "Discussion", "Conclusion", "References"]
    else:
        return [
            "Introduction", "Summary", "Overview", "Conclusion", "Benefits",
            "Challenges", "Solutions", "Results", "Recommendations", "Future Work"
        ]

st.sidebar.header("📄 Upload your documents")
if st.sidebar.button("🧹 Reset Conversation"):
    st.session_state.memory.clear()
    st.session_state.chunks = []
    st.sidebar.success("🧹 Conversation and chunks cleared!")

uploaded_files = st.sidebar.file_uploader(
    "Choose multiple files (PDF, DOCX, TXT, XLSX)",
    type=["pdf", "docx", "txt", "xlsx"],
    accept_multiple_files=True
)

if "memory" not in st.session_state:
    st.session_state.memory = MemoryManager()

if "chunks" not in st.session_state:
    st.session_state.chunks = []

if uploaded_files:
    for uploaded_file in uploaded_files:
        try:
            file_path = save_uploaded_file(uploaded_file)
            file_content, _ = load_file_content(file_path)

            st.write(f"🔍 **Preview of uploaded content** (first 300 chars):\n\n```\n{file_content[:300]}\n```")

            your_keywords_list = infer_keywords_from_filename(uploaded_file.name)
            splitter = HybridTextSplitter(keywords=your_keywords_list, chunk_size=500)

            chunks = [chunk for chunk in splitter.split_text(file_content) if chunk.strip()]
            st.session_state.chunks.extend(chunks)

            st.sidebar.success(f"✅ Uploaded {uploaded_file.name} ({len(chunks)} usable chunks)")
        except Exception as e:
            st.sidebar.error(f"❌ Failed to process {uploaded_file.name}: {str(e)}")

# 🧠 Display chat history
st.markdown("### 🧠 Conversation History")
history = st.session_state.memory.get_history()

for i, (role, content) in enumerate(history, 1):
    if role == "user":
        st.chat_message("user").markdown(f"**User #{i}:** {content}")
    else:
        st.chat_message("assistant").markdown(f"**Assistant #{i}:** {content}")

st.markdown("---")

# 🧾 Input
user_query = st.chat_input("Ask a question about your documents...")
if user_query:
    st.write(f"[DEBUG] User asked: {user_query}")
    st.session_state.memory.add_user_message(user_query)

    try:
        retrieved_chunks = hybrid_retriever(
            query=user_query,
            chunks=st.session_state.chunks
        )

        st.write("🔍 **Retrieved Chunks (top 3):**", retrieved_chunks[:3])

        if detect_no_retrieval(retrieved_chunks):
            st.warning(fallback_menu(user_query))
            fallback_option = st.radio("Fallback options:", [
                "Retry your question",
                "Ask OpenAI directly",
                "Upload a new document"
            ])

            if st.button("Proceed with selected option"):
                fallback_response = execute_fallback_action(fallback_option, user_query, llm_answer)
                st.success(fallback_response)
                st.session_state.memory.add_assistant_message(fallback_response)
                st.chat_message("assistant").markdown(fallback_response)

        else:
            answer = llm_answer(
                question=user_query,
                documents=retrieved_chunks
            )

            # 🔍 Debug hooks
            st.write("🧠 [DEBUG] Assistant Raw Answer:")
            st.code(answer if answer.strip() else "❌ No answer returned", language="markdown")

            if answer and answer.strip():
                st.session_state.memory.add_assistant_message(answer)
                st.chat_message("assistant").markdown(answer)
            else:
                st.warning("⚠️ Assistant returned no answer.")

    except Exception as e:
        error_msg = f"⚠️ An error occurred: {str(e)}"
        st.session_state.memory.add_assistant_message(error_msg)
        st.chat_message("assistant").markdown(error_msg)

st.markdown("---")
st.caption("🔵 Engine ready for Semantic RAG - Built for robust debugging and mentor review.")
