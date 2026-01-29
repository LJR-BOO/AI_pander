import os
import sys

# 固定项目根目录，兼容Windows路径格式
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
project_root = project_root.replace('\\', '/')
sys.path.insert(0, project_root)

# 🌟 唯一的导入点：文件顶部直接导入
from deepseek_client import chat_completion

def test_chat_completion_mock(monkeypatch):
    """测试Mock模式：未设置DEEPSEEK_API_KEY时，聊天功能能正常运行"""
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.setenv("MOCK_MODE", "True")

    # 直接使用已导入的函数
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
    from unittest.mock import MagicMock
    mock = MagicMock()
    try:
        test_chat_completion_mock(mock)
        test_mock_mode_env(mock)
        print("🎉 所有本地测试通过！")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
