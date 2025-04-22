# splitter/HybridTextSplitter_BACKUP_SAFE_PATCH.py

from typing import List
import re
import os
import importlib.util
import streamlit as st
import sys

class HybridTextSplitter:
    """
    Custom splitter that first splits by keywords and then applies semantic chunking.
    """

    def __init__(self, keywords: List[str], chunk_size: int = 500):
        self.keywords = keywords
        self.chunk_size = chunk_size

        # 🧠 Dynamic loading of semantic_text_splitter.abi3.so
        self.semantic_splitter = self._load_semantic_splitter()

        st.write(f"🧠✅ [HybridTextSplitter Debug]: semantic_text_splitter loaded dynamically")

    def _load_semantic_splitter(self):
        # Dynamically find the .so file
        base_dir = "/workspaces/Advanced_RAG_Engine/"
        so_file = None

        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.endswith(".so") and "semantic_text_splitter" in file:
                    so_file = os.path.join(root, file)
                    break
            if so_file:
                break

        if not so_file:
            raise ImportError("❗ semantic_text_splitter.abi3.so file not found!")

        spec = importlib.util.spec_from_file_location("semantic_text_splitter", so_file)
        semantic_module = importlib.util.module_from_spec(spec)
        sys.modules["semantic_text_splitter"] = semantic_module
        spec.loader.exec_module(semantic_module)

        return semantic_module

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
            semantic_chunks = self.semantic_splitter.split_text(section, chunk_size=self.chunk_size)
            final_chunks.extend(semantic_chunks)

        return final_chunks
