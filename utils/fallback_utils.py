# utils/fallback_utils.py

def detect_no_retrieval(chunks):
    """
    Returns True if no chunks were retrieved.
    """
    return not chunks or len(chunks) == 0


def fallback_menu(user_query):
    """
    Returns a user-friendly fallback prompt when no data is retrieved.
    """
    return f"""
⚠️ I couldn’t find any relevant information in the uploaded documents for:

**"{user_query}"**

You can:
- 🔁 Retry your question
- 💡 Ask OpenAI directly (might hallucinate)
- 📂 Upload a new document to assist me

Choose from below to proceed:
    """


def execute_fallback_action(option, user_query, llm):
    """
    Executes fallback behavior based on selected option.
    """
    if option == "Retry your question":
        return "🔁 Please rephrase and try your question again."

    elif option == "Ask OpenAI directly":
        openai_response = llm(question=user_query, documents=None)  # No documents passed
        return f"💡 OpenAI suggests:\n\n{openai_response}"

    elif option == "Upload a new document":
        return "📂 Please upload a document and try your question again."

    else:
        return "❓ Unknown option selected. Please choose again."
