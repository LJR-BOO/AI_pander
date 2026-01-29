import sys
# 硬编码你的项目根目录，绝对不会错
sys.path.insert(0, r"C:\Users\i\AI_pander")

try:
    from deepseek_client import chat_completion
    print("✅ 导入成功！deepseek_client 模块已找到")
except Exception as e:
    print(f"❌ 导入失败: {e}")
    print("当前Python搜索路径：", sys.path)
