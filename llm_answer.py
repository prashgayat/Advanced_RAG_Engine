# llm_answer.py

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI Client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def llm_answer(question: str, documents: list) -> str:
    """
    Generates an answer using retrieved document chunks and the OpenAI model.

    Args:
        question (str): The user's question.
        documents (list): List of context text chunks retrieved.

    Returns:
        str: The generated answer or fallback message.
    """
    if not documents:
        return "🤔 Sorry, I could not find relevant information to answer your question."

    # Prepare context from retrieved documents
    context = "\n\n".join(documents)

    # Prepare prompt
    prompt = f"""You are an expert knowledge assistant.

Answer the following question based **only** on the given context.

Context:
{context}

Question:
{question}

Answer:"""

    try:
        # Call the OpenAI model
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant specialized in answering based strictly on provided context."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=600,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"❗ Error generating answer: {e}")
        return "⚠️ Sorry, something went wrong while generating the answer."
