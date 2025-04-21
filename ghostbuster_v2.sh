#!/bin/bash

echo "🧹 Starting Ghostbuster v2 script..."

# Step 1: Activate venv
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    exit 1
fi

echo "⚡ Activating virtual environment..."
source .venv/bin/activate

# Step 2: Set PYTHONPATH
export PYTHONPATH=/workspaces/Advanced_RAG_Engine

# Step 3: Rebuild semantic-text-splitter if needed
echo "🔨 Rebuilding semantic-text-splitter from source..."
cd semantic_text_splitter_src || { echo "❌ semantic_text_splitter_src not found"; exit 1; }
maturin develop --release
cd ..

# Step 4: Hotfix HybridTextSplitter.py import
echo "🛠 Patching HybridTextSplitter.py import statement..."
HYBRID_SPLITTER="splitter/HybridTextSplitter.py"

if grep -q "from semantic_text_splitter import TextSplitter" "$HYBRID_SPLITTER"; then
    sed -i 's/from semantic_text_splitter import TextSplitter/from semantic_text_splitter import SemanticTextSplitter as TextSplitter/' "$HYBRID_SPLITTER"
    echo "✅ HybridTextSplitter.py import fixed!"
else
    echo "⚠️ No need to patch, already correct."
fi

# Step 5: Launch Streamlit
echo "🚀 Launching Streamlit app..."
streamlit run ADVANCED_RAG_ENGINE/app.py
