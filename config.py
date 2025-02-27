import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Stytch configuration
STYTCH_SECRET = os.getenv("STYTCH_SECRET")
STYTCH_PROJECT_ID = os.getenv("STYTCH_PROJECT_ID")

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_KEY")
