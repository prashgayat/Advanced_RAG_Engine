import streamlit as st
from utils.file_utils import save_uploaded_file, load_file_content
from splitter.HybridTextSplitter import HybridTextSplitter  # Import this

st.set_page_config(page_title="Advanced Semantic RAG Engine 🚀", page_icon="🧠")

# Sidebar
st.sidebar.title("📚 Upload your documents")
uploaded_files = st.sidebar.file_uploader(
    "Choose multiple files (PDF, DOCX, TXT, XLSX)",
    accept_multiple_files=True,
    type=["pdf", "docx", "txt", "xlsx"]
)

# Main page content
st.title("Welcome to the Advanced Semantic RAG Engine 🧠")
st.subheader("Built for robust ingestion and advanced semantic retrieval 🚀")

# Divider
st.markdown("---")

# If files are uploaded
if uploaded_files:
    st.success(f"{len(uploaded_files)} file(s) uploaded successfully!")
    for uploaded_file in uploaded_files:
        st.write(f"✅ {uploaded_file.name}")

        # Save the uploaded file
        saved_path = save_uploaded_file(uploaded_file)

        # Load the file content
        try:
            file_content, file_type = load_file_content(saved_path)
            st.info(f"📄 Loaded {file_type.upper()} file successfully! ({len(file_content)} characters)")

            # ✨ Now split using HybridTextSplitter
            splitter = HybridTextSplitter(
                keywords=["Introduction", "Chapter", "Section", "Summary"],  # Customize as needed
                chunk_size=500
            )
            chunks = splitter.split_text(file_content)
            st.success(f"🔵 Text split into {len(chunks)} semantic+keyword chunks.")

        except Exception as e:
            st.error(f"❌ Failed to process {uploaded_file.name}: {str(e)}")

else:
    st.info("👈 Please upload documents from the sidebar to proceed.")

# Footer
st.markdown("---")
st.caption("🔵 Engine ready for Semantic RAG - Unstructured Data, Zero Fear.")
