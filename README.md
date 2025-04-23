# 📃 Advanced Semantic RAG Engine

## 🚀 Features

- **Multi-format Upload**: Supports PDF, DOCX, TXT, XLSX
- **Hybrid Chunking**: Combines keyword rules + semantic splitting
- **Auto Keyword Detection**: Learns keyword types from filenames
- **Conversation Memory**: Multi-turn interactions persist during session
- **Environment Security**: Auto-load `.env` for API key management
- **Strict Mode Fallbacks**: Guarantees hallucination control
- **Modular Codebase**: Built with clean, extensible Python modules

---

## 🔰 Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/Advanced_RAG_Engine.git
    cd Advanced_RAG_Engine
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Add your API key to `.env`**:
    ```bash
    touch .env
    ```

    Inside `.env`:
    ```env
    OPENAI_API_KEY=your-openai-api-key-here
    STRICT_MODE=True
    ```

4. **Run the app**:
    ```bash
    streamlit run app.py
    ```

---

## 🧪 Streamlit Test Example (Mentor-Ready)

This simulates a **Postman-style test case** for Streamlit-based flows:

> Upload: `project-consortium-agreement-template.docx`  
> Ask: `What are the responsibilities of the PCC?`  

Expected Output:
> "The responsibilities of the PCC in the consortium agreement include ensuring that the work identified in Annex A can be carried out by the Parties, identifying subcontracted elements in the Full Proposal..."

---

## 🗂️ Test Documentation

All evaluation snapshots and result trails are organized under:

```
test_results/
├── RAG testing 3.pdf
├── RAG testing edge case.pdf
├── Stephen-TheSevenHabitsOfHighlyEffectivePeople.pdf
└── project-consortium-agreement-template.docx
```

This includes ground-truth verification and hallucination failure cases with debug logs.

---

## 📂 Project Structure

```
Advanced_RAG_Engine/
│
├── app.py                      # Main Streamlit UI logic
├── .env                        # 🔐 API keys & flags (local only)
├── test_results/               # 📊 Real-time mentor test snapshots
│
├── utils/
│   ├── env_loader.py           # Auto environment loader
│   └── file_utils.py           # File handling utilities
│
├── splitter/
│   └── HybridTextSplitter.py   # Semantic + keyword chunker
│
├── retriever/
│   └── retriever_utils.py      # TF-IDF + FAISS hybrid retriever
│
├── memory/
│   └── memory_manager.py       # Persistent conversation memory
│
├── prompts/
│   └── prompt_templates.py     # Structured context prompt templates
```

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 🙌 Acknowledgements

- [Streamlit](https://streamlit.io/)
- [OpenAI API](https://platform.openai.com/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [Scikit-Learn](https://scikit-learn.org/)
- [Semantic Text Splitter](https://github.com/jerryjliu/semantic-text-splitter)
