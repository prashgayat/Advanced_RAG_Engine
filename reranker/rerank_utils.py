# reranker/rerank_utils.py

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI Client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def rerank_chunks(query: str, chunks: list, top_k: int = 5) -> list:
    """
    Rerank retrieved chunks based on relevance to the query using OpenAI.

    Args:
        query (str): The original user question.
        chunks (list): List of retrieved document chunks.
        top_k (int, optional): Number of top-ranked chunks to return. Defaults to 5.

    Returns:
        list: Top K most relevant chunks (reranked).
    """
    if not chunks:
        return []

    # Prepare formatted chunks
    formatted_chunks = "\n\n".join(
        [f"Chunk {i+1}:\n{chunk}" for i, chunk in enumerate(chunks)]
    )

    rerank_prompt = f"""You are a ranking assistant.

Given the following user question and document chunks, rank the chunks by how relevant they are to answering the question.

User Question:
{query}

Document Chunks:
{formatted_chunks}

Return the top {top_k} most relevant chunks as a numbered list, only returning the chunk text without any explanations.
"""

    try:
        # OpenAI API call
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that ranks content relevance."},
                {"role": "user", "content": rerank_prompt}
            ],
            temperature=0.0,
            max_tokens=1000,
        )

        reranked_text = response.choices[0].message.content.strip()

        # Debug print
        #print("\n🔵 Raw Reranked Text from OpenAI:")
        #print(reranked_text)

        # Safely parse both "1. text" and "1: text" formats
        reranked_chunks = [line.strip() for line in reranked_text.splitlines() if line.strip()]
        cleaned_chunks = []

        for chunk in reranked_chunks:
            if "." in chunk:
                parts = chunk.split(".", 1)
                cleaned_chunks.append(parts[1].strip())
            elif ":" in chunk:
                parts = chunk.split(":", 1)
                cleaned_chunks.append(parts[1].strip())
            else:
                cleaned_chunks.append(chunk.strip())

        return cleaned_chunks[:top_k]

    except Exception as e:
        print(f"❗ Error during reranking: {e}")
        return chunks[:top_k]
