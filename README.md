# AI_pander — AI 智能伴侣 Demo (Streamlit + Deepseek-compatible)

简介
- 本仓库包含一个基于 Streamlit 的 AI 智能伴侣 Demo（入口：`ai_companion_app.py`）。
- 支持本地演示模式（无需 key）与调用 OpenAI-compatible Deepseek endpoint（需配置环境变量）。
- 目标：快速得到可交互的 Demo，用于寒假项目产出与简历展示。

主要文件
- `ai_companion_app.py` — Streamlit 主程序（会话管理、流式回复兼容、会话持久化）
- `deepseek_client.py` — Deepseek 调用占位（可选）
- `requirements.txt` — 依赖列表
- `docs/prompt.md` — persona、prompt 与合规建议
- `examples/` — 示例文档 (`doc1.txt`, `doc2.txt`)
- `1/resources/` — 放置 logo / avatar（占位）
- `.gitignore`, `LICENSE`

快速开始（Windows / PowerShell）
1. 克隆你的仓库并进入目录（若未克隆）：
   ```
   git clone https://github.com/LJR-BOO/AI_pander.git
   cd AI_pander
   ```

2. （可选）运行初始化脚本（若你保存了 `init_repo.ps1`）：
   ```
   .\init_repo.ps1
   ```

3. 创建并激活虚拟环境（PowerShell）：
   ```
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

5. （可选）设置 Deepseek key（仅当要调用远端时）：
   - 临时（当前会话）：
     ```
     $env:DEEPSEEK_API_KEY = "your_key_here"
     $env:DEEPSEEK_BASE_URL = "https://api.deepseek.com"  # 如需自定义
     ```
   - 永久（当前用户，重启 PowerShell 生效）：
     ```
     setx DEEPSEEK_API_KEY "your_key_here"
     setx DEEPSEEK_BASE_URL "https://api.deepseek.com"
     ```

6. 运行应用：
   ```
   streamlit run ai_companion_app.py
   ```
   然后在浏览器打开 http://localhost:8501

部署建议
- Streamlit Community Cloud（最简单）：连接 GitHub，部署 `main` 分支，并在 Secrets/Environment variables 中设置 `DEEPSEEK_API_KEY`。
- Render / Railway / Docker：我可以为你生成 Dockerfile 与部署说明（如需告知）。

合规提示
- 公开 demo 时请注意 persona 描述的合规与伦理（docs/prompt.md 中有建议）。
- 切勿将密钥提交到仓库；使用环境变量或部署平台的 secrets。
