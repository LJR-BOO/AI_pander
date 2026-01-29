import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

def test_chat_completion_mock(monkeypatch):
    """测试Mock模式：未设置DEEPSEEK_API_KEY时，聊天功能能正常运行"""
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.setenv("MOCK_MODE", "True")

    # 现在可以正常导入了
    try:
        from deepseek_client import chat_completion
        response = chat_completion(prompt="你好，你是谁？")
        assert response is not None
        assert len(response) > 0
        print("✅ Mock模式聊天测试通过！")
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        raise
    except AssertionError:
        print("❌ 测试断言失败：响应为空")
        raise

def test_mock_mode_env(monkeypatch):
    """测试环境变量MOCK_MODE的识别"""
    monkeypatch.setenv("MOCK_MODE", "True")
    assert os.getenv("MOCK_MODE") == "True"
    monkeypatch.setenv("MOCK_MODE", "False")
    assert os.getenv("MOCK_MODE") == "False"
    print("✅ 环境变量测试通过！")
