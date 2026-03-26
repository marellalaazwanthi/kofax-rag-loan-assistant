import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = "sqlite:///./test.db"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
USE_OPENAI = os.getenv("USE_OPENAI", "false").lower() == "true"
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
