# test_hybrid_splitter.py

from splitter.HybridTextSplitter import HybridTextSplitter

def test_hybrid_splitter():
    print("\n🚀 Running HybridTextSplitter Unit Tests...")

    # Sample test input
    text = """
    Introduction: This document explains the health benefits.
    Diagnosis: Health issues can be identified early.
    Treatment: Medicines and therapy help patients recover.
    Conclusion: Preventive care is crucial.
    """

    # Keywords we want to split on
    keywords = ["Introduction", "Diagnosis", "Treatment", "Conclusion"]

    # Initialize HybridTextSplitter
    splitter = HybridTextSplitter(keywords=keywords, chunk_size=50)

    # Perform split
    chunks = splitter.split_text(text)

    # Assertions
    assert isinstance(chunks, list), "Chunks should be a list."
    assert len(chunks) > 0, "Chunks should not be empty."
    assert all(isinstance(chunk, str) for chunk in chunks), "Each chunk should be a string."

    print("✅ Chunks created:", chunks)
    print("🎯 All HybridTextSplitter tests passed successfully!")

if __name__ == "__main__":
    test_hybrid_splitter()
