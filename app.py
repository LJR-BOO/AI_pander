import os
import streamlit as st
from deepseek_client import search_and_answer
from pathlib import Path

st.set_page_config(page_title="Campus Knowledge Search", layout="wide")

if "history" not in st.session_state:
    st.session_state.history = []

st.title("Campus Knowledge Search — Demo")
st.markdown("上传或选择示例文档，输入问题，查看检索片段与答案（演示用）")

# 左侧：上传 / 示例选择
with st.sidebar:
    st.header("文档来源")
    uploaded = st.file_uploader("上传文本文件（.txt）", accept_multiple_files=True, type=["txt"])
    use_examples = st.checkbox("使用示例文档", value=True)

# 读取示例文档
docs = {}
if use_examples:
    examples_dir = Path("examples")
    if examples_dir.exists():
        for f in examples_dir.glob("*.txt"):
            docs[f.name] = f.read_text(encoding="utf-8")

# 读取上传的文件
if uploaded:
    for uf in uploaded:
        try:
            content = uf.getvalue().decode("utf-8")
        except Exception:
            content = uf.getvalue().decode("latin-1")
        docs[uf.name] = content

st.write(f"已加载文档数量：{len(docs)}")

# 问题输入
question = st.text_input("请输入你的问题：")
top_k = st.slider("检索返回片段数 (top_k)", 1, 8, 3)

if st.button("检索并回答"):
    if not question.strip():
        st.warning("请先输入问题")
    elif len(docs) == 0:
        st.warning("请上传或启用示例文档")
    else:
        with st.spinner("检索中..."):
            t0 = st.time()
            result = search_and_answer(question, docs, top_k=top_k)
            latency = st.time() - t0

        # 保存历史
        entry = {
            "question": question,
            "answer": result["answer"],
            "evidence": result["evidence"],
            "latency_s": latency
        }
        st.session_state.history.append(entry)

        # 显示答案
        st.subheader("回答（演示）")
        st.write(result["answer"])
        st.caption(f"耗时：{latency:.2f}s")

        # 显示证据
        st.subheader("证据片段（按相似度）")
        for ev in result["evidence"]:
            st.markdown(f"**文件**: {ev.get('file')} — **相似度**: {ev.get('similarity'):.3f}")
            st.write(ev.get("text")[:1000])
            st.markdown("---")

# 会话历史与导出
st.sidebar.header("会话历史")
for i, h in enumerate(reversed(st.session_state.history[-20:])):
    st.sidebar.markdown(f"**Q{i+1}**: {h['question'][:60]}")
if st.sidebar.button("导出历史为 txt"):
    lines = []
    for h in st.session_state.history:
        lines.append(f"Q: {h['question']}\nA: {h['answer']}\n---\n")
    b = "\n".join(lines).encode("utf-8")
    st.sidebar.download_button("下载会话（txt）", b, file_name="session_history.txt")