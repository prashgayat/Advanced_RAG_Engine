# prompts/prompt_templates.py

def build_qa_prompt(query, context_chunks, chat_history):
    """
    Build a simple QA prompt by stitching together retrieved chunks and previous chat history.
    """
    context_text = "\n\n".join(context_chunks)
    history_text = "\n".join([f"User: {q}\nAssistant: {a}" for q, a in chat_history])

    prompt = f"""
You are a helpful assistant. Use the following context to answer the user's question.
If you don't know the answer, say you don't know.

Previous Conversation:
{history_text}

Context:
{context_text}

Question:
{query}

Answer:"""

    return prompt.strip()
