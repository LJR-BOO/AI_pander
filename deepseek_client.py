# deepseek_client.py (占位实现)
# 如果你需要把远端检索/QA 从 app 中抽离，可在此实现真实请求逻辑。
import os
import requests

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

def simple_search(query, top_k=5):
    """
    占位：若未配置 DEEPSEEK_API_KEY，则返回空列表。
    若配置了真实 Deepseek REST 接口，请根据官方文档实现请求并返回统一格式：
    [ {"file": "...", "chunk_index":0, "text":"...", "similarity":0.9}, ... ]
    """
    if not DEEPSEEK_API_KEY:
        return []
    # TODO: implement real request per Deepseek API
    return []
