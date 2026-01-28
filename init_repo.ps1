# PowerShell 脚本：init_repo.ps1
# 用法：在已克隆的仓库目录运行 `.\init_repo.ps1`
$ErrorActionPreference = "Stop"

function Write-UTF8File($path, $content) {
    $dir = Split-Path $path -Parent
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    $content | Out-File -FilePath $path -Encoding utf8 -Force
}

# ai_companion_app.py
$ai = @'
# ai_companion_app.py
# Streamlit 前端：AI 智能伴侣（Deepseek / OpenAI-compatible endpoint）
import os
import json
from datetime import datetime

import streamlit as st
from openai import OpenAI  # 需要 openai >= 1.x

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

def generate_session_name():
    return datetime.now().strftime("%Y-%m-%d %H-%M-%S")

def sessions_dir():
    return os.path.join(".", "1", "sessions")

def save_session():
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

st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="😍",
    layout="wide",
    initial_sidebar_state="expanded",
)

system_prompt = """
你叫🌸小桃，现在是用户的专属 AI 伴侣（演示角色）。回复要简短、温柔并带有甜系 emoji。
如遇到不适当或敏感话题，请高情商拒绝或引导（遵守平台与法律规则）。
每次只返回一条消息，尽量匹配用户语气。
"""

if "message" not in st.session_state:
    st.session_state.message = [{"role": "system", "content": system_prompt}]

if "current_session" not in st.session_state:
    st.session_state.current_session = generate_session_name()

st.title("AI智能伴侣——小桃")
logo_path = os.path.join(".", "1", "resources", "设计AI智能伴侣logo.png")
if os.path.exists(logo_path):
    st.image(logo_path, width=160)

st.text(f"当前会话名称: {st.session_state.current_session}")

for msg in st.session_state.message:
    if msg.get("role") == "system":
        continue
    st.chat_message(msg.get("role")).write(msg.get("content"))

if not DEEPSEEK_API_KEY:
    st.warning("未检测到 DEEPSEEK_API_KEY。当前使用演示模式（不会调用远端 Deepseek）。若需调用 Deepseek，请在环境变量中配置 DEEPSEEK_API_KEY。")

try:
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
except Exception:
    client = None

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

prompt = st.chat_input("请开始与小桃聊天吧～")
if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.message.append({"role": "user", "content": prompt})

    if not DEEPSEEK_API_KEY or client is None:
        reply = "（演示模式）小桃：好呀~ 我在这里陪你～(*´˘`*)♡"
        st.chat_message("assistant").write(reply)
        st.session_state.message.append({"role": "assistant", "content": reply})
        save_session()
    else:
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

if st.sidebar.button("导出历史为 txt"):
    lines = []
    for m in st.session_state.message:
        if m["role"] == "system":
            continue
        lines.append(f"{m['role'].upper()}: {m['content']}\n")
    b = "\n".join(lines).encode("utf-8")
    st.sidebar.download_button("下载会话（txt）", b, file_name=f"{st.session_state.current_session}.txt")

if st.session_state.get("need_rerun"):
    st.session_state.pop("need_rerun", None)
    st.experimental_rerun()
'@

Write-UTF8File "ai_companion_app.py" $ai

# deepseek_client.py
$client = @'
# deepseek_client.py (占位)
import os
import requests

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

def simple_search(query, top_k=5):
    if not DEEPSEEK_API_KEY:
        return []
    # TODO: implement real request based on Deepseek doc
    return []
'@
Write-UTF8File "deepseek_client.py" $client

# requirements.txt
$req = @'
streamlit>=1.20
openai>=1.0.0
python-dotenv
'@
Write-UTF8File "requirements.txt" $req

# .gitignore
$gitignore = @'
__pycache__/
*.py[cod]
*.so
*.egg-info/
.venv/
.env
.env.*
.streamlit/
.ipynb_checkpoints
.DS_Store
1/sessions/
'@
Write-UTF8File ".gitignore" $gitignore

# README.md
$readme = @'
# AI_pander — AI 伴侣 Demo (Streamlit + Deepseek-compatible)

简介
- 本仓库包含一个基于 Streamlit 的 AI 智能伴侣 Demo（入口：ai_companion_app.py）。
- 支持本地演示模式（无需 key）和调用 OpenAI-compatible Deepseek endpoint（需配置环境变量）。

快速开始
1. 创建并激活虚拟环境：
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

2. 安装依赖：
   pip install -r requirements.txt

3. 运行：
   streamlit run ai_companion_app.py

配置（可选）
- 若要调用 Deepseek，请设置环境变量 DEEPSEEK_API_KEY（在 PowerShell 中）：
  $env:DEEPSEEK_API_KEY="your_key_here"
  或持久化使用 setx：
  setx DEEPSEEK_API_KEY "your_key_here"
'@
Write-UTF8File "README.md" $readme

# docs/prompt.md
$prompt = @'
# Persona 与 Prompt 策略（说明 / 合规建议）

Persona（示例）
- system prompt（示例安全版）:
  你是“AI 伴侣”小桃，回复应简短、温柔、并带甜系 emoji。若遇到敏感或违法话题，请温柔拒绝或引导用户寻求专业帮助。

Prompt 设计要点
- 拼接检索上下文时应限制 token 上限（例如 1500 tokens）。
- 优先使用最相似的 top-K 片段（K=3–8），按相似度降序累加直到接近 token 限制。
- 回答后列出依据的证据（文件名/片段/相似度）。

合规、安全建议
- 避免在公开 demo 中使用未成年或容易引发伦理问题的角色设定。
- 对用户输入和模型输出做敏感词检测与速率限制。
- 明确在 README 提示：该项目为示范用途，不作为专业或医疗/法律建议。
'@
Write-UTF8File "docs/prompt.md" $prompt

# examples
$ex1 = @'
学校图书馆开放时间：
图书馆周一至周五 08:30-20:30，周六日 09:00-17:00。
考试周延长开放时间以公告为准。
'@
Write-UTF8File "examples/doc1.txt" $ex1

$ex2 = @'
校园计算机实验室使用规则：
实验室需刷卡进出，非实验课时间需预约。饮食请勿带入。实验设备损坏需及时报修。
'@
Write-UTF8File "examples/doc2.txt" $ex2

# resources placeholder
if (-not (Test-Path ".\1\resources")) { New-Item -ItemType Directory -Path ".\1\resources" -Force | Out-Null }
Write-UTF8File ".\1\resources/README.txt" "Place your logo/avatar files here: 设计AI智能伴侣logo.png, 小桃.png"

# LICENSE
$license = @'
MIT License

Copyright (c) 2026 <Your Name>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'@
Write-UTF8File "LICENSE" $license

Write-Host "初始化完成：已创建文件 (ai_companion_app.py, deepseek_client.py, requirements.txt, .gitignore, README.md, docs/prompt.md, examples/*, 1/resources/*)."
Write-Host "下一步：git add . ; git commit -m 'Initial scaffold' ; git push origin main"