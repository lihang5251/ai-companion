# 🤖 AI Chat — 你的 AI 智能聊天体

基于 **Streamlit** + **DeepSeek** 打造的 AI 聊天应用，支持自定义人设、关系、回复风格，带会话管理和密码保护。

## ✨ 功能特性

- 🎭 **自定义人设**：自由设定 AI 的昵称、性格、与你的关系
- 💬 **流式对话**：像微信一样逐字输出，体验丝滑
- 📂 **会话管理**：新建 / 切换 / 删除历史会话，聊天记录本地持久化
- 🔐 **密码保护**：部署后只有知道密码的人才能使用
- 🎨 **Streamlit 原生 UI**：侧边栏配置 + 聊天界面，简洁美观

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/lihang5251/streamlit-ai-chat.git
cd streamlit-ai-chat
```

### 2. 安装依赖

```bash
pip install streamlit openai
```

### 3. 配置 API Key

设置 DeepSeek API Key 环境变量：

**Windows (PowerShell):**
```powershell
$env:DEEPSEEK_API_KEY = "你的API密钥"
```

**macOS / Linux:**
```bash
export DEEPSEEK_API_KEY="你的API密钥"
```

> 去 [DeepSeek 开放平台](https://platform.deepseek.com/) 注册获取 API Key。

### 4. 修改密码

打开 `AI Chat.py`，找到第 36 行，把 `A114514` 改成你自己的密码：

```python
PASSWORD = "你的密码"
```

### 5. 运行

```bash
streamlit run Ai Chat.py
```

浏览器打开 `http://localhost:8501` 即可使用。

## 📖 使用说明

### 侧边栏配置

| 配置项 | 说明 |
|--------|------|
| 昵称 | AI 伴侣的名字 |
| 与您的关系 | 如"好友"、"恋人"、"导师" |
| 一次回复几条消息 | 控制 AI 每次回复的消息数量 |
| 是否禁止描述性文字 | "允许" 或 "禁止" |
| 回复方式 | 如"回复简短，像微信聊天一样" |
| 人设 / 角色设定 | 越详细越好，决定 AI 的性格和行为 |

### 会话管理

- 点击 **📄 会话时间** 切换历史会话
- 点击 **❌** 删除会话
- 点击 **✏️ 新建会话** 开始新对话
- 当前会话会高亮显示

## 🛠 技术栈

| 技术 | 用途 |
|------|------|
| [Streamlit](https://streamlit.io/) | Web 界面框架 |
| [DeepSeek API](https://platform.deepseek.com/) | 大语言模型 |
| [OpenAI SDK](https://github.com/openai/openai-python) | API 调用（兼容 DeepSeek） |
| JSON | 会话数据本地存储 |

## 📁 项目结构

```
├── AI Chat.py    # 主程序
├── sessions/           # 会话存档（自动生成）
├── resources/          # 资源文件（logo 等）
└── README.md
```

## 📄 License

MIT
