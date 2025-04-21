# Load environment variables automatically
from utils.env_loader import load_environment
load_environment()
import streamlit as st
from utils.file_utils import save_uploaded_file, load_file_content
from splitter.HybridTextSplitter import HybridTextSplitter
from retriever.retriever_utils import hybrid_retriever
from memory.memory_manager import MemoryManager
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Advanced Semantic RAG Engine", page_icon="🧠")
st.title("Welcome to the Advanced Semantic RAG Engine 🧠")
st.subheader("Built for robust ingestion and advanced semantic retrieval 🚀")

# --- Auto-adaptive keyword function ---
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

# --- Upload sidebar ---
st.sidebar.header("📄 Upload your documents")
if st.sidebar.button("🧹 Reset Conversation"):
    st.session_state.memory.clear()
    st.session_state.chunks = []
    st.sidebar.success("🧹 Conversation and chunks cleared!")

uploaded_files = st.sidebar.file_uploader(
    "Choose multiple files (PDF, DOCX, TXT, XLSX)", type=["pdf", "docx", "txt", "xlsx"], accept_multiple_files=True
)

# --- Initialize memory and chunks ---
if "memory" not in st.session_state:
    st.session_state.memory = MemoryManager()

if "chunks" not in st.session_state:
    st.session_state.chunks = []

# --- Handle file uploads ---
if uploaded_files:
    for uploaded_file in uploaded_files:
        try:
            file_path = save_uploaded_file(uploaded_file)
            file_content, _ = load_file_content(file_path)  # small fix here too

            # 🎯 Auto-adapt keywords based on filename
            your_keywords_list = infer_keywords_from_filename(uploaded_file.name)

            # 🧠 Create splitter with dynamic keywords
            splitter = HybridTextSplitter(keywords=your_keywords_list, chunk_size=500)

            chunks = splitter.split_text(file_content)
            st.session_state.chunks.extend(chunks)

            st.sidebar.success(f"✅ Uploaded {uploaded_file.name} ({len(chunks)} chunks)")
        except Exception as e:
            st.sidebar.error(f"❌ Failed to process {uploaded_file.name}: {str(e)}")

# --- Display conversation history ---
for role, content in st.session_state.memory.get_history():
    if role == "user":
        st.chat_message("user").markdown(content)
    else:
        st.chat_message("assistant").markdown(content)

# --- Chat input ---
user_query = st.chat_input("Ask a question about your documents...")

if user_query:
    st.session_state.memory.add_user_message(user_query)

    try:
        response = hybrid_retriever(
            query=user_query,
            chunks=st.session_state.chunks
        )
        answer = response if response else "🤔 Sorry, I could not find an exact answer in the uploaded documents."
    except Exception as e:
        answer = f"⚠️ An error occurred: {str(e)}"

    st.session_state.memory.add_assistant_message(answer)
    st.chat_message("assistant").markdown(answer)

# --- Footer ---
st.markdown("---")
st.caption("🔵 Engine ready for Semantic RAG - Unstructured Data, Zero Fear.")
