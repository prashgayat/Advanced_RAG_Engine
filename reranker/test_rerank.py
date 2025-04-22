# reranker/test_rerank.py

from reranker.rerank_utils import rerank_chunks

# Sample question
question = "What is the importance of being proactive?"

# Sample retrieved document chunks
retrieved_chunks = [
    "Proactivity means taking responsibility for your reactions, emotions, and actions.",
    "Proactive people blame circumstances and genetics for their behavior.",
    "Taking initiative is a hallmark of being proactive and creating positive change.",
    "Being reactive is responding to situations based on emotions and immediate conditions.",
    "Proactivity leads to better long-term career growth and life satisfaction."
]

# Call the reranker
top_chunks = rerank_chunks(query=question, chunks=retrieved_chunks, top_k=3)

# Print the reranked top chunks
print("\n🔵 Top Reranked Chunks:")
for idx, chunk in enumerate(top_chunks, start=1):
    print(f"{idx}. {chunk}")
