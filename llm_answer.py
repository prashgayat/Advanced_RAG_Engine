# llm_answer.py

import os
from openai import OpenAI
from dotenv import load_dotenv
from prompts.prompt_templates import context_qa_prompt_template
from utils.fallback_utils import generate_fallback_response  # ✅ added fallback import

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
        return generate_fallback_response(no_docs=True)

    context = "\n\n".join(documents).strip()
    word_count = len(context.split())

    # 🔍 Check for truly meaningful context
    print(f"[DEBUG] Context word count: {word_count}")
    print(f"[DEBUG] Context preview (first 300 chars):\n{context[:300]}")

    if word_count < 20:
        return generate_fallback_response(no_docs=True)

    prompt = context_qa_prompt_template.format(context=context, question=question)

    try:
        print(f"[DEBUG] Prompt Preview:\n{prompt[:300]}...")
        print(f"[DEBUG] Using max_tokens=1000, temperature=0.3")

        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Answer only from the provided context."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"❗ Error generating answer: {e}")
        return generate_fallback_response(error=True)
