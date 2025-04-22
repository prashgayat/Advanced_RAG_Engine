# retriever/test_retriever_utils.py

from dotenv import load_dotenv
load_dotenv()

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from retriever.retriever_utils import HybridRetriever
from langchain.docstore.document import Document

print("\n🚀 Running HybridRetriever Unit Tests...")

# Sample documents
sample_documents = [
    Document(page_content="The insurance policy covers health benefits."),
    Document(page_content="Real estate investments require valuation."),
    Document(page_content="Medical treatment improves patient outcomes."),
]

# Initialize retriever
retriever = HybridRetriever(documents=sample_documents)
retriever.build_indexes([doc.page_content for doc in sample_documents])

# Perform a hybrid retrieval
query = "health insurance"
results = retriever.retrieve(query, top_k=2)

# Validate results
assert len(results) > 0, "No results retrieved!"
assert isinstance(results[0], Document), "Retrieved item is not a Document!"

print("🎯 All HybridRetriever unit tests passed successfully!")
