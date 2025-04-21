#!/bin/bash

echo "🧹 Starting the ghostbuster script..."

# 1. Activate venv
echo "⚡ Activating virtual environment..."
source .venv/bin/activate

# 2. Install semantic-text-splitter inside venv
echo "🔨 Rebuilding semantic-text-splitter from source..."
cd /workspaces/Advanced_RAG_Engine/semantic_text_splitter_src
maturin develop --release

# 3. Go back to project root
cd /workspaces/Advanced_RAG_Engine

# 4. Run Streamlit
echo "🚀 Launching Streamlit app..."
PYTHONPATH=/workspaces/Advanced_RAG_Engine streamlit run ADVANCED_RAG_ENGINE/app.py
