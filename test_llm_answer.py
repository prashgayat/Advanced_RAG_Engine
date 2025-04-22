# test_llm_answer.py

from llm_answer import llm_answer

def test_llm_answer_success():
    sample_question = "What are the benefits of having health insurance?"
    sample_documents = [
        "Health insurance provides financial protection against high medical costs.",
        "It ensures access to a network of healthcare providers at negotiated rates."
    ]

    answer = llm_answer(sample_question, sample_documents)
    print("\n✅ Test 1 - Successful Answer:")
    print(answer)

    assert isinstance(answer, str), "Answer should be a string."
    assert len(answer) > 0, "Answer should not be empty."
    assert "health" in answer.lower() or "insurance" in answer.lower(), "Answer should be relevant to the question."

def test_llm_answer_no_documents():
    sample_question = "What is the meaning of mortgage insurance?"
    sample_documents = []  # Simulating no retrieval

    answer = llm_answer(sample_question, sample_documents)
    print("\n✅ Test 2 - No Documents Retrieved:")
    print(answer)

    assert isinstance(answer, str), "Fallback answer should be a string."
    assert "sorry" in answer.lower(), "Fallback answer should apologize for missing information."

if __name__ == "__main__":
    print("\n🚀 Running llm_answer.py Unit Tests...")
    try:
        test_llm_answer_success()
        test_llm_answer_no_documents()
        print("\n🎯 All tests passed successfully!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
