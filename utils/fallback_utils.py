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


def generate_fallback_response(no_docs=False, error=False, error_message="") -> str:
    """
    Generates a fallback response for missing documents or LLM call errors.

    Args:
        no_docs (bool): No documents were retrieved.
        error (bool): OpenAI API or LLM call failed.
        error_message (str): Detailed error if available.

    Returns:
        str: A polite fallback response message.
    """
    if no_docs:
        return (
            "🤔 Sorry, I couldn't find enough information to confidently answer your question "
            "based on the available documents. Could you please try rephrasing or asking something else?"
        )
    if error:
        return f"⚠️ Oops! Something went wrong: {error_message}\nPlease try rephrasing your question or ask something else!"

    return "⚠️ An unexpected error occurred. Please try again."
