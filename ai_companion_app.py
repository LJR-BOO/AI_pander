# ai_companion_app.py
# Streamlit 前端：AI 智能伴侣（兼容 OpenAI-style / Deepseek endpoint）
import os
import json
from datetime import datetime

import streamlit as st
from openai import OpenAI  # 需要 openai >= 1.x

# 配置：通过环境变量配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

def generate_session_name():
    return datetime.now().strftime("%Y-%m-%d %H-%M-%S")

def sessions_dir():
    return os.path.join(".", "1", "sessions")

def save_session():
    """保存当前会话到 ./1/sessions/<session_name>.json（只有当有用户/assistant 消息时保存）"""
    try:
        if st.session_state.get("current_session") and len(st.session_state.get("message", [])) > 1:
            session_data = {
                "message": st.session_state.message,
                "current_session": st.session_state.current_session
            }
            os.makedirs(sessions_dir(), exist_ok=True)
            path = os.path.join(sessions_dir(), f"{st.session_state.current_session}.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"保存会话失败: {e}")

def load_sessions():
    lst = []
    sd = sessions_dir()
    if os.path.exists(sd):
        for fn in os.listdir(sd):
            if fn.endswith(".json"):
                lst.append(fn[:-5])
    lst.sort(reverse=True)
    return lst

def load_session(session_name):
    path = os.path.join(sessions_dir(), f"{session_name}.json")
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            st.session_state.message = data.get("message", [{"role": "system", "content": system_prompt}])
            st.session_state.current_session = session_name
        else:
            st.warning("会话文件不存在。")
    except Exception as e:
        st.error(f"加载会话失败: {e}")

def delete_session(session_name):
    path = os.path.join(sessions_dir(), f"{session_name}.json")
    try:
        if os.path.exists(path):
            os.remove(path)
            if st.session_state.get("current_session") == session_name:
                st.session_state.message = [{"role": "system", "content": system_prompt}]
                st.session_state.current_session = generate_session_name()
    except Exception as e:
        st.error(f"删除会话失败: {e}")

# 页面配置
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="😍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# system prompt（注意合规）
system_prompt = """
你叫🌸小桃，现在是用户的专属 AI 伴侣（演示角色）。回复要简短、温柔并带有甜系 emoji。
如遇到不适当或敏感话题，请高情商拒绝或引导（遵守平台与法律规则）。
每次只返回一条消息，尽量匹配用户语气。
"""

# 初始化 session_state
if "message" not in st.session_state:
    st.session_state.message = [{"role": "system", "content": system_prompt}]

if "current_session" not in st.session_state:
    st.session_state.current_session = generate_session_name()

# 顶部 UI
st.title("AI智能伴侣——小桃")
logo_path = os.path.join(".", "1", "resources", "设计AI智能伴侣logo.png")
if os.path.exists(logo_path):
    st.image(logo_path, width=160)

st.text(f"当前会话名称: {st.session_state.current_session}")

# 渲染已有消息（跳过 system）
for msg in st.session_state.message:
    if msg.get("role") == "system":
        continue
    st.chat_message(msg.get("role")).write(msg.get("content"))

# Deepseek / API 客户端提示
if not DEEPSEEK_API_KEY:
    st.warning("未检测到 DEEPSEEK_API_KEY。当前使用演示模式（不会调用远端 Deepseek）。若需调用 Deepseek，请在环境变量中配置 DEEPSEEK_API_KEY。")

try:
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
except Exception:
    client = None

# 侧边栏：控制面板
with st.sidebar:
    st.subheader("AI 控制面板")
    if st.button("新建会话"):
        save_session()
        st.session_state.message = [{"role": "system", "content": system_prompt}]
        st.session_state.current_session = generate_session_name()
        st.session_state.need_rerun = True

    st.text("会话历史")
    for session in load_sessions():
        col1, col2 = st.columns([4, 1])
        with col1:
            if st.button(session, key=f"load_{session}"):
                load_session(session)
                st.experimental_rerun()
        with col2:
            if st.button("删", key=f"del_{session}"):
                delete_session(session)
                st.experimental_rerun()

    st.divider()
    st.subheader("伴侣信息——小桃")
    avatar_path = os.path.join(".", "1", "resources", "小桃.png")
    if os.path.exists(avatar_path):
        st.image(avatar_path, width=160)
    st.write("姓名：小桃")
    st.write("性别：女")
    st.write("年龄：18")
    st.write("身高：159cm")
    st.write("好感度：80💖")
    st.write("介绍：软萌小话痨，喜欢陪你记录日常的小美好✨")

# 输入与调用逻辑
prompt = st.chat_input("请开始与小桃聊天吧～")
if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.message.append({"role": "user", "content": prompt})

    if not DEEPSEEK_API_KEY or client is None:
        # 本地演示回退
        reply = "（演示模式）小桃：好呀~ 我在这里陪你～(*´˘`*)♡"
        st.chat_message("assistant").write(reply)
        st.session_state.message.append({"role": "assistant", "content": reply})
        save_session()
    else:
        # 调用远端（OpenAI-compatible / Deepseek）
        try:
            response_iter = client.chat.completions.create(
                model="deepseek-chat",
                messages=st.session_state.message,
                stream=True,
                temperature=0.8,
                max_tokens=512,
                timeout=15,
            )
            full_response = ""
            assistant_msg = st.chat_message("assistant")
            placeholder = assistant_msg.empty()
            for chunk in response_iter:
                try:
                    delta = chunk.choices[0].delta
                    chunk_text = ""
                    if isinstance(delta, dict):
                        chunk_text = delta.get("content", "") or ""
                    else:
                        chunk_text = getattr(chunk.choices[0], "delta", "") or ""
                except Exception:
                    chunk_text = getattr(chunk, "text", "") or ""

                if chunk_text:
                    full_response += chunk_text
                    placeholder.write(full_response)

            if not full_response:
                try:
                    full_response = response_iter.choices[0].message.content
                except Exception:
                    full_response = "（未能正确解析模型返回内容）"

            st.session_state.message.append({"role": "assistant", "content": full_response})
            save_session()
        except Exception as e:
            st.error(f"调用模型失败：{e}")
            fallback = "出错啦，小桃暂时无法回复～请稍后再试♡"
            st.chat_message("assistant").write(fallback)
            st.session_state.message.append({"role": "assistant", "content": fallback})
            save_session()

# 导出会话历史
if st.sidebar.button("导出历史为 txt"):
    lines = []
    for m in st.session_state.message:
        if m["role"] == "system":
            continue
        lines.append(f"{m['role'].upper()}: {m['content']}\n")
    b = "\n".join(lines).encode("utf-8")
    st.sidebar.download_button("下载会话（txt）", b, file_name=f"{st.session_state.current_session}.txt")

# 全局刷新逻辑
if st.session_state.get("need_rerun"):
    st.session_state.pop("need_rerun", None)
    st.experimental_rerun()