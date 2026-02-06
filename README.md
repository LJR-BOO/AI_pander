# AI_pander — AI 智能伴侣 Demo

[Demo (在线链接占位)](REPLACE_WITH_DEPLOY_URL) · License: MIT

简介
- 基于 Streamlit 的 AI 智能伴侣（聊天 + 文档检索）。支持本地 mock 演示模式与调用 Deepseek (OpenAI-compatible) endpoint。
- 入口文件：`ai_companion_app.py`。示例检索场景：`app.py`。
- 项目亮点：流式回复支持、mock 回退、会话持久化、应答证据显示、易于部署（Docker / Streamlit Cloud / Render）。

快速开始（本地）
1. 克隆仓库并进入目录：
   ```bash
   git clone https://github.com/LJR-BOO/AI_pander.git
   cd AI_pander
   ```

2. 创建虚拟环境并安装依赖：
   ```bash
   python -m venv .venv
   # mac/linux
   source .venv/bin/activate
   # windows (PowerShell)
   .\.venv\Scripts\Activate.ps1

   pip install -r requirements.txt
   ```

3. 复制示例环境变量并运行（演示模式，不需要 API Key）：
   ```bash
   cp .env.example .env
   # 编辑 .env 如需设置真实 DEEPSEEK_API_KEY（不要将真实 key 提交到仓库）
   streamlit run ai_companion_app.py
   ```

演示（README 中放入截图/GIF）
- 请把 4 张关键截图上传到 `docs/screenshots/` 并替换下列占位：
  - `docs/screenshots/01-input.png`：上传文档 / 输入问题
  - `docs/screenshots/02-answer.png`：答案与证据片段
  - `docs/screenshots/03-history.png`：会话历史 / 导出
  - `docs/screenshots/04-deploy.png`：已部署页面截图

部署（建议）
- Streamlit Community Cloud（最简单）
  - 在 https://share.streamlit.io 创建新 app，连接本仓库 `main` 分支，设置 Secrets: `DEEPSEEK_API_KEY`、`DEEPSEEK_BASE_URL`（如需）。
- 使用 Docker（推荐复现）：
  - 构建： `docker build -t ai_pander:latest .`
  - 运行： `docker run -p 8501:8501 --env-file .env ai_pander:latest`
- Render / Railway：参考 Docker 或 Python 服务部署。

环境变量（.env.example）
- 请使用 `.env.example` 作参考：
  ```
  DEEPSEEK_API_KEY=PLACEHOLDER_DEEPSEEK_KEY
  DEEPSEEK_BASE_URL=https://api.deepseek.com
  DEEPSEEK_STREAM_TIMEOUT=15
  DEEPSEEK_RETRY_ATTEMPTS=2
  DEEPSEEK_RETRY_BACKOFF=0.6
  ```

Mock 模式
- 当未设置 `DEEPSEEK_API_KEY` 时，应用会自动进入演示模式（不调用远端 API），适合公开 demo / 录屏展示，避免产生费用或泄露 key。

安全与合规提示
- 请勿把真实密钥提交到仓库；若误提交，立即撤销并更换密钥。
- 对用户上传内容请提示隐私与合规（见 `docs/prompt.md`）。

如何贡献
- 新功能请在 feature 分支上开发并提交 PR。
- 建议写单元测试并确保 CI 通过（仓库含 GitHub Actions 工作流）。


- 中文：使用 Python + Streamlit 开发 AI 智能伴侣 Demo，集成 Deepseek-compatible API 实现文档检索与流式问答；含 mock 模式、部署说明与演示。
- English: Built a Streamlit-based AI companion demo integrating a Deepseek-compatible API for document retrieval & streaming chat; includes mock fallback and deployment instructions.

联系方式
- 仓库: https://github.com/LJR-BOO/AI_pander
- Demo: REPLACE_WITH_DEPLOY_URL
