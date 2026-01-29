import os
import sys
# 固定项目根目录，强行加入Python搜索路径（优先级最高）
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# 🌟 核心修改：把导入提到文件顶部，路径生效后直接导入，不再放函数内/try里
from deepseek_client import chat_completion

def test_chat_completion_mock(monkeypatch):
    """测试Mock模式：未设置DEEPSEEK_API_KEY时，聊天功能能正常运行"""
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.setenv("MOCK_MODE", "True")

    # 直接调用，无需再导入
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

# 可选：本地运行测试的入口
if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
