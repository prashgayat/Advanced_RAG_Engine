# test_llm_answer.py

from llm_answer import llm_answer

# Example question and example retrieved documents
question = "What is the importance of being proactive?"
documents = [
    "Being proactive means taking responsibility for your life. You cannot keep blaming everything on your parents or circumstances."
]

# Call llm_answer
response = llm_answer(question, documents)

# Print the output
print("\n🔵 LLM Response:")
print(response)
