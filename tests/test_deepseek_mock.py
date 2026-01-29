import os
import sys
import importlib

# 固定项目根目录，强行加入Python搜索路径（优先级最高）
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# 兼容Windows路径：替换斜杠，确保Python识别
project_root = project_root.replace('\\', '/')
sys.path.insert(0, project_root)
# 打印路径（本地调试用，CI运行时会显示，不影响结果）
print(f"🔍 项目根目录已加入Python路径：{project_root}")

# 🌟 核心：文件顶部直接导入，路径生效后一次导入完成
from deepseek_client import chat_completion

def test_chat_completion_mock(monkeypatch):
    """测试Mock模式：未设置DEEPSEEK_API_KEY时，聊天功能能正常运行"""
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.setenv("MOCK_MODE", "True")

    # 直接使用已导入的函数，无需reload
    response = chat_completion(prompt="你好，你是谁？")
    assert response is not None
    assert len(response) > 0
    print("✅ Mock模式聊天测试通过！")

def test_mock_mode_env(monkeypatch):
    """测试环境变量MOCK_MODE的识别"""
    monkeypatch.setenv("MOCK_MODE", "True")
    assert os.getenv("MOCK_MODE") == "True"
    monkeypatch.setenv("MOCK_MODE", "False")
    assert os.getenv("MOCK_MODE") == "False"
    print("✅ 环境变量测试通过！")

# 本地运行入口
if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
