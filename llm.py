from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "")

PROJECT_ROOT = Path(__file__).resolve().parent
REASONING_DIR = PROJECT_ROOT / "run_logs" / "reasoning"


def _extract_reasoning(value: Any) -> list[str]:
    chunks: list[str] = []

    if isinstance(value, str) and value.strip():
        chunks.append(value.strip())
    elif isinstance(value, dict):
        for key in (
            "reasoning_content",
            "reasoning",
            "reasoning_text",
            "thinking",
            "thoughts",
        ):
            chunks.extend(_extract_reasoning(value.get(key)))
        for item in value.get("content", []) if isinstance(value.get("content"), list) else []:
            chunks.extend(_extract_reasoning(item))
    elif isinstance(value, list):
        for item in value:
            chunks.extend(_extract_reasoning(item))

    return chunks


def _log_reasoning(result: Any) -> None:
    chunks: list[str] = []
    for generation_group in getattr(result, "generations", []) or []:
        generations = generation_group if isinstance(generation_group, list) else [generation_group]
        for generation in generations:
            message = getattr(generation, "message", None)
            if message is None:
                continue
            chunks.extend(_extract_reasoning(getattr(message, "additional_kwargs", {})))
            chunks.extend(_extract_reasoning(getattr(message, "response_metadata", {})))

    if not chunks:
        return

    REASONING_DIR.mkdir(parents=True, exist_ok=True)
    path = REASONING_DIR / f"reasoning_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with path.open("a", encoding="utf-8") as handle:
        for index, chunk in enumerate(chunks, 1):
            handle.write(f"--- reasoning chunk {index} ---\n")
            handle.write(chunk)
            handle.write("\n\n")


class _ReasoningSafeChatOpenAI(ChatOpenAI):
    def _generate(self, *args: Any, **kwargs: Any) -> Any:
        result = super()._generate(*args, **kwargs)
        _log_reasoning(result)
        return result

    async def _agenerate(self, *args: Any, **kwargs: Any) -> Any:
        result = await super()._agenerate(*args, **kwargs)
        _log_reasoning(result)
        return result


def get_llm(
    max_completion_tokens: int = 250000,
    thinking: bool = False,
    reasoning_effort: str | None = None,
) -> ChatOpenAI:
    kwargs: dict[str, Any] = {
        "model": DEEPSEEK_MODEL,
        "api_key": DEEPSEEK_API_KEY,
        "base_url": DEEPSEEK_BASE_URL,
        "max_retries": 3,
        "timeout": 300,
        "temperature": 0.0,
        "max_completion_tokens": max_completion_tokens,
        "extra_body": {
            "thinking": {"type": "enabled" if thinking else "disabled"},
            "max_tokens": max_completion_tokens,
        },
    }
    if thinking and reasoning_effort:
        kwargs["reasoning_effort"] = reasoning_effort
    return _ReasoningSafeChatOpenAI(**kwargs)


__all__ = ["get_llm"]
