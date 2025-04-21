# splitter/HybridTextSplitter.py

from typing import List
import re
import streamlit as st
from semantic_text_splitter import split_text as semantic_split_text  # ✅ correct import

class HybridTextSplitter:
    """
    Custom splitter that first splits by keywords and then applies semantic chunking.
    """

    def __init__(self, keywords: List[str], chunk_size: int = 500):
        self.keywords = keywords
        self.chunk_size = chunk_size

        st.write(f"🧠✅ [HybridTextSplitter Debug]: Using semantic_split_text function directly")

    def split_text(self, text: str) -> List[str]:
        """
        Splits text first by keywords, then semantically.
        """
        if not text:
            return []

        # Step 1: Keyword-based rough splitting
        keyword_pattern = '|'.join([re.escape(kw) for kw in self.keywords])
        keyword_sections = re.split(f"(?i)({keyword_pattern})", text)

        merged_sections = []
        current_section = ""

        for part in keyword_sections:
            if part.strip():
                if re.match(f"(?i)({keyword_pattern})", part):
                    if current_section:
                        merged_sections.append(current_section)
                        current_section = ""
                current_section += part
        if current_section:
            merged_sections.append(current_section)

        # Step 2: Semantic fine-splitting on each section
        final_chunks = []
        for section in merged_sections:
            semantic_chunks = semantic_split_text(section, chunk_size=self.chunk_size)  # ✅ only chunk_size
            final_chunks.extend(semantic_chunks)

        return final_chunks
