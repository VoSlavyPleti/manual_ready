from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "")

def get_llm(max_completion_tokens: int = 50000):

    return ChatOpenAI(
        model=DEEPSEEK_MODEL,
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL,
        max_retries=3,
        timeout=300,
        temperature=0.0,
        max_completion_tokens=max_completion_tokens,
        extra_body={
            "thinking": {"type": "disabled"},
            "max_tokens": 50000
            }
    )

__all__ = ["get_llm"]
