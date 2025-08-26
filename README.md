# Kora 语音面试

Kora 语音面试是一个创新的 AI 面试平台，旨在通过模拟真实的面试场景，帮助求职者提升面试技巧、增强信心。平台利用先进的语音识别和自然语言处理技术，提供即时反馈和专业评估，帮助用户在求职路上走得更远。

## ✨ 功能特性

- **多种面试风格**: 提供多种面试风格（如正式、友好、校园），模拟不同公司的面试氛围。
- **智能语音交互**: 支持语音输入，AI 面试官能够理解并跟进您的回答，实现流畅的对话式面试。
- **即时反馈与评估**: 在每次回答后，AI 会提供针对性的反馈，帮助您即时改进。
- **综合评估报告**: 面试结束后，系统会生成一份详细的评估报告，全面分析您的表现，并提供改进建议。
- **完整的面试记录**: 所有对话都将被记录下来，方便您随时回顾、复盘。
- **导出与分享**: 您可以将完整的面试记录和评估报告导出为 JSON 或文本格式，方便分享和存档。

## 🚀 安装指南

### 系统要求

- Node.js >= 16.0.0
- Python >= 3.8
- 一个有效的 DashScope API 密钥

### 依赖安装

1.  **克隆项目到本地**:
    ```bash
    git clone https://github.com/Brwaey/Kora.git
    cd kora-voice-interview
    ```

2.  **安装前端依赖**:
    ```bash
    npm install
    ```

3.  **安装后端依赖**:
    ```bash
    cd api
    pip install -r requirements.txt
    ```

### 环境配置

1.  在 `api` 目录下创建一个名为 `.env` 的文件。
2.  在 `.env` 文件中，添加您的 DashScope API 密钥，格式如下：
    ```
    DASHSCOPE_API_KEY=your_api_key_here
    ```

## 📖 使用说明

1.  **启动后端服务**:
    ```bash
    cd api
    python index.py
    ```
    后端服务将在 `http://127.0.0.1:5000` 上运行。

2.  **启动前端开发服务器**:
    ```bash
    npm run dev
    ```
    前端应用将在 `http://localhost:3000` (或另一个可用端口) 上运行。

3.  在浏览器中打开前端应用的地址，开始您的 AI 面试之旅！

4.  也可直接点击该链接访问使用vercel部署好的版本：https://kora-ai-voice-interview.vercel.app/

## 📂 项目结构

```
.
├── README.md
├── api/
│   ├── __init__.py
│   ├── vercel.py       
│   ├── .env             # 存储环境变量 (需自行创建)
│   ├── index.py           # Flask 后端主应用
│   └── test.http        # 用于测试 API 的文件
├── index.html
├── package.json
├── vercel.json
│   requirements.txt     # Python 依赖
├── src/
│   ├── App.vue          # Vue 应用根组件
│   ├── main.js          # Vue 应用入口
│   ├── assets/
│   │   └── main.css     # 全局样式
│   └── views/
│       ├── Home.vue     # 首页
│       ├── Interview.vue# 面试页面
│       └── Summary.vue  # 总结报告页面
└── vite.config.js
```

### 关键文件说明

-   `backend/index.py`: 实现了所有后端逻辑，包括与 DashScope API 的交互、CORS 配置以及 API 端点。
-   `src/views/Interview.vue`: 包含了面试页面的所有交互逻辑和 UI，是项目的核心组件之一。
-   `src/views/Summary.vue`: 用于展示面试完成后的总结报告，包括对话记录和 AI 分析。

## 🤝 贡献指南

我们欢迎任何形式的贡献！

### 提交问题

如果您在使用中遇到问题，或者有任何改进建议，请通过 [GitHub Issues](https://github.com/Brwaey/Kora/issues) 提交问题。

### 代码提交规范

-   请确保您的代码风格与项目现有代码保持一致。
-   提交前请进行充分测试，确保不会引入新的 bug。
-   Commit message 请遵循清晰、有意义的原则。

## 📄 许可证信息

本项目采用 [MIT License](https://opensource.org/licenses/MIT) 开源许可证。

## 📞 联系方式

-   **维护者**: [Brwaey](https://github.com/Brwaey)
-   **问题反馈**: [GitHub Issues](https://github.com/Brwaey/Kora/issues)