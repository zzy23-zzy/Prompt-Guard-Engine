# 🛡️ Prompt Guard Engine

一个基于纵深防御（Defense-in-Depth）架构的大模型提示词安全网关。集成 **DeepSeek API** 语义审计与动态威胁情报库，实时拦截越狱（Jailbreak）与提示词注入（Injection）攻击。

## ✨ 核心特性
- **三层审计架构**：
  - **L1 静态规则层**：毫秒级关键词匹配，支持动态黑名单注入。
  - **L2 语义审计层**：调用 **DeepSeek LLM API**，精准识别变种攻击与混淆载荷。
  - **L3 风险溯源层**：基于多维权重的攻击行为画像评分。
- **实时监控看板**：可视化展示攻击趋势、高危占比及详细拦截取证日志。
- **动态情报系统**：支持通过 UI 界面实时更新黑名单，实现防御能力的平滑演进。

## 🛠️ 技术栈
- **Frontend**: Streamlit (Custom CSS Optimized)
- **Engine**: Python / Pandas / DeepSeek API
- **Deployment**: Git / Python 3.10+

## 📦 快速开始
1. 克隆仓库：
   `git clone https://github.com/zzy23-zzy/Prompt-Guard-Engine.git`
2. 配置环境变量：
   在根目录创建 `.env` 文件并填入你的 DeepSeek API Key。
3. 运行应用：
   `streamlit run app.py`

---
*Created by Mia | 网络空间安全专业 · 转型 AI 安全工程*