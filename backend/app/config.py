import os
from dotenv import load_dotenv

load_dotenv()

ANYTHINGLLM_BASE_URL = os.getenv("ANYTHINGLLM_BASE_URL", "http://localhost:3001")
ANYTHINGLLM_API_KEY = os.getenv("ANYTHINGLLM_API_KEY", "")

EBAY_APP_ID = os.getenv("EBAY_APP_ID", "")
EBAY_CLIENT_ID = os.getenv("EBAY_CLIENT_ID", "")
EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET", "")
EBAY_ENV = os.getenv("EBAY_ENV", "production")
