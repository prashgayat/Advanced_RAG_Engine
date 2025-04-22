# utils/fallback_utils.py

def generate_fallback_message() -> str:
    """
    Generates a polite fallback message when the system cannot confidently answer 
    based on retrieved documents.
    """
    return (
        "🤔 Sorry, I couldn't find enough information to confidently answer your question "
        "based on the available documents. Could you please try rephrasing or asking something else?"
    )

def generate_fallback_response(error_message: str) -> str:
    """
    Generates a fallback message when the LLM call itself fails (error during OpenAI API etc).

    Args:
        error_message (str): The caught exception message.

    Returns:
        str: A polite error fallback response.
    """
    return f"⚠️ Oops! Something went wrong: {error_message}\nPlease try rephrasing your question or ask something else!"
