# llm_answer.py

import os
from openai import OpenAI
from dotenv import load_dotenv
from prompts.prompt_templates import context_qa_prompt_template
from utils.fallback_utils import generate_fallback_response

# Load environment variables
load_dotenv()

# Initialize OpenAI Client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
STRICT_MODE = os.getenv("STRICT_MODE", "False").lower() == "true"

def llm_answer(question: str, documents: list) -> str:
    """
    Generates an answer using retrieved document chunks and the OpenAI model.
    Applies strict fallback if STRICT_MODE is enabled and grounding is weak.
    Appends a response tag to clarify whether content is grounded or fallback.
    """

    context = "\n\n".join(documents).strip()
    word_count = len(context.split())
    print(f"[DEBUG] Context word count: {word_count}")
    print(f"[DEBUG] Context preview (first 300 chars):\n{context[:300]}")

    # 🔐 Strict fallback enforcement
    if not documents or word_count < 20:
        if STRICT_MODE:
            print("[DEBUG - STRICT MODE] Context missing or too short. Triggering fallback.")
            fallback = generate_fallback_response(no_docs=True)
            return f"{fallback}\n\n[⚠️ Fallback: No matching document content.]"
        else:
            print("[DEBUG] Weak context, but STRICT_MODE is OFF.")

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

        final_answer = response.choices[0].message.content.strip()

        # 🧠 Detect polite fallback-style refusals from LLM output
        fallback_phrases = [
            "not provided in the context",
            "not found in the context",
            "couldn't find enough information",
            "does not contain relevant information",
            "context does not include",
            "information is missing from the document",
            "unable to answer based on the provided documents"
        ]

        if any(phrase in final_answer.lower() for phrase in fallback_phrases):
            return f"{final_answer}\n\n[⚠️ Fallback: No matching document content.]"

        return f"{final_answer}\n\n[✔️ Answer based on uploaded document.]"

    except Exception as e:
        print(f"❗ Error generating answer: {e}")
        fallback = generate_fallback_response(error=True)
        return f"{fallback}\n\n[⚠️ Fallback: LLM error occurred.]"
