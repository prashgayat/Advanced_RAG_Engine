#!/bin/bash

echo "🧹 Starting Ghostbuster v3 script..."

# Activate venv
echo "⚡ Activating virtual environment..."
source .venv/bin/activate

# Rebuild semantic-text-splitter
echo "🔨 Rebuilding semantic-text-splitter from source..."
cd semantic_text_splitter_src
maturin develop --release
cd ..

# Patch HybridTextSplitter if needed (already correct mostly)
echo "🛠 Patching HybridTextSplitter.py import statement if needed..."
sed -i 's/from semantic_text_splitter import TextSplitter/from semantic_text_splitter import split_text as semantic_split_text/' splitter/HybridTextSplitter.py || true
echo "✅ No patch needed. Already correct."

# Run Streamlit App
echo "🚀 Launching Streamlit app..."
streamlit run app.py
