# deepseek_client.py
# Deepseek / OpenAI-compatible client wrapper with streaming support and mock fallback.
# Usage:
#   from deepseek_client import create_client, chat_stream, chat_completion
#   client = create_client()
#   for chunk in chat_stream(client, messages): ...
#   resp = chat_completion(client, messages)

import os
import time
from typing import Iterable, Dict, Any, Optional

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
STREAM_TIMEOUT = int(os.getenv("DEEPSEEK_STREAM_TIMEOUT", "15"))
RETRY_ATTEMPTS = int(os.getenv("DEEPSEEK_RETRY_ATTEMPTS", "2"))
RETRY_BACKOFF = float(os.getenv("DEEPSEEK_RETRY_BACKOFF", "0.6"))

def create_client():
    """
    Return an OpenAI-compatible client if available and api key present, else None.
    """
    if not DEEPSEEK_API_KEY:
        return None
    if OpenAI is None:
        # openai package not installed
        return None
    try:
        return OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
    except Exception:
        return None

def _parse_stream_chunk(chunk: Any) -> str:
    """
    Safe parse of a stream chunk returned by OpenAI-compatible stream.
    """
    try:
        # typical shape: chunk.choices[0].delta.get("content")
        delta = chunk.choices[0].delta
        if isinstance(delta, dict):
            return delta.get("content", "") or ""
        # fallback for some SDK shapes
        return getattr(chunk.choices[0], "delta", "") or ""
    except Exception:
        try:
            return getattr(chunk, "text", "") or ""
        except Exception:
            return ""

def chat_stream(client, messages: list, model: str = "deepseek-chat", temperature: float = 0.8, max_tokens: int = 512, timeout: int = STREAM_TIMEOUT) -> Iterable[str]:
    """
    Yield partial text chunks from streaming chat completion.
    If client is None, yield a mock response.
    """
    if client is None:
        # Simple mock reply for demo mode
        yield "（演示模式）这是一个示例回复。"
        return

    attempt = 0
    while attempt <= RETRY_ATTEMPTS:
        try:
            response_iter = client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=timeout,
            )
            full = ""
            for chunk in response_iter:
                text = _parse_stream_chunk(chunk)
                if text:
                    full += text
                    yield text
            return
        except Exception as e:
            attempt += 1
            if attempt > RETRY_ATTEMPTS:
                # Final fallback
                yield f"（错误）无法获取远端回复：{e}"
                return
            time.sleep(RETRY_BACKOFF * attempt)

def chat_completion(client, messages: list, model: str = "deepseek-chat", temperature: float = 0.8, max_tokens: int = 512, timeout: int = STREAM_TIMEOUT) -> Dict[str, Any]:
    """
    Non-streaming convenience wrapper that returns the full assistant text and raw response.
    """
    if client is None:
        return {"text": "（演示模式）这是示例完整回复。", "raw": None}

    attempt = 0
    while attempt <= RETRY_ATTEMPTS:
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
                stream=False,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=timeout,
            )
            # try to extract a meaningful text
            try:
                text = resp.choices[0].message.get("content") if hasattr(resp, "choices") else getattr(resp, "text", "")
            except Exception:
                text = str(resp)
            return {"text": text, "raw": resp}
        except Exception as e:
            attempt += 1
            if attempt > RETRY_ATTEMPTS:
                return {"text": f"（错误）无法获取远端回复：{e}", "raw": None}
            time.sleep(RETRY_BACKOFF * attempt)