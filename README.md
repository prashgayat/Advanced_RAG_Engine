
# 📃 Advanced Semantic RAG Engine

## 🚀 Features

- **Multi-format Upload**: PDF, DOCX, TXT, XLSX
- **Hybrid Chunking**: Keyword + Semantic splitting
- **Auto Keyword Adaptation**: Intelligent keyword inference based on document type
- **Memory Support**: Multi-turn conversation memory
- **Environment Security**: Auto-load `.env` securely
- **Modular Codebase**: Clean, extensible Python modules

---

## 🔰 Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/Advanced_RAG_Engine.git
    cd Advanced_RAG_Engine
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the project root:
    ```bash
    touch .env
    ```

4. Add your API key to `.env`:
    ```
    OPENAI_API_KEY=your-openai-api-key-here
    ```

5. Run the app:
    ```bash
    streamlit run app.py
    ```

---

## 📂 Project Structure

```
Advanced_RAG_Engine/
│
├── app.py                  # Main Streamlit application
├── utils/
│   ├── env_loader.py        # Auto environment variable loader
│   └── file_utils.py        # File saving and text extraction utilities
│
├── splitter/
│   └── HybridTextSplitter.py # Hybrid keyword + semantic text splitter
│
├── retriever/
│   └── retriever_utils.py   # FAISS + TF-IDF hybrid retriever
│
├── memory/
│   └── memory_manager.py    # Conversation memory manager
│
└── .env                     # (local) API keys (NOT committed)
```

---

## 💬 Example Usage

> Upload your document → Ask questions → Get precise, chunk-based semantic answers 🔥.

---

## 📜 License

This project is licensed under the MIT License.

---

## 🙌 Acknowledgements

- Streamlit
- OpenAI API
- FAISS
- Scikit-Learn (TF-IDF)
- Semantic Text Splitter

