#!/bin/bash

echo "🧹 Starting Ghostbuster v3 script..."

# Move to project root
cd /workspaces/Advanced_RAG_Engine || { echo "❌ Failed to cd to project."; exit 1; }

# Activate virtual environment
echo "⚡ Activating virtual environment..."
if [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
else
  echo "❌ Virtual environment not found. Exiting."
  exit 1
fi

# Set PYTHONPATH correctly
export PYTHONPATH=/workspaces/Advanced_RAG_Engine

# Rebuild semantic-text-splitter
echo "🔨 Rebuilding semantic-text-splitter from source..."
cd semantic_text_splitter_src || { echo "❌ semantic_text_splitter_src not found. Exiting."; exit 1; }
maturin develop --release

# Go back to project root
cd ..

# Patch HybridTextSplitter import if needed
echo "🛠 Patching HybridTextSplitter.py import statement if needed..."
HYBRID_SPLITTER_FILE="splitter/HybridTextSplitter.py"
if grep -q "from semantic_text_splitter import SemanticTextSplitter" "$HYBRID_SPLITTER_FILE"; then
  echo "⚠️ Wrong import found. Fixing..."
  sed -i 's/from semantic_text_splitter import SemanticTextSplitter.*/from semantic_text_splitter import TextSplitter/' "$HYBRID_SPLITTER_FILE"
  echo "✅ Patched HybridTextSplitter import correctly."
else
  echo "✅ No patch needed. Already correct."
fi

# Launch Streamlit app
echo "🚀 Launching Streamlit app..."
streamlit run ADVANCED_RAG_ENGINE/app.py
