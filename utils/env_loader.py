import os
from dotenv import load_dotenv

def load_environment():
    """Auto-load .env if not already loaded."""
    env_path = os.path.join(os.getcwd(), ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
        print("✅ Environment variables loaded from .env")
    else:
        print("⚠️ .env file not found. Proceeding without loading environment variables.")
