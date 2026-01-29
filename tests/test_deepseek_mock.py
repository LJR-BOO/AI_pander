import os
import importlib
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_chat_completion_mock(monkeypatch):
    # Ensure DEEPSEEK_API_KEY is unset
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    # Reload module to pick up env change if needed
    deepseek_client = importlib.import_module("deepseek_client")
    # create_client should return None in mock mode
    client = deepseek_client.create_client()
    assert client is None
    # call chat_completion in mock mode
    resp = deepseek_client.chat_completion(client, messages=[{"role":"user","content":"Hello"}])
    assert isinstance(resp, dict)
    assert "text" in resp
    assert isinstance(resp["text"], str)
    assert "演示模式" in resp["text"] or "示例" in resp["text"]
