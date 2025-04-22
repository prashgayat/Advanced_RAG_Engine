# fallback_utils.py

def generate_fallback_message() -> str:
    """
    Generates a polite fallback message when the system cannot confidently answer 
    based on retrieved documents.

    Returns:
        str: A fallback response for the user encouraging rephrasing or retrying.
    """
    return (
        "🤔 Sorry, I couldn't find enough information to confidently answer your question "
        "based on the available documents. Could you please try rephrasing or asking something else?"
    )
