<template>
    <div class="summary">
      <!-- Header -->
      <header class="bg-white shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center mr-3">
                <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clip-rule="evenodd" />
                </svg>
              </div>
              <h1 class="text-xl font-semibold text-gray-900">Kora 语音面试</h1>
            </div>
            <div class="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
              面试完成
            </div>
          </div>
        </div>
      </header>
  
      <!-- Main Content -->
      <main class="main">
        <div class="container">
          <!-- Summary Header -->
          <section class="summary-header">
            <h1>🎉 面试总结</h1>
            <p>恭喜您完成了本次语音面试！以下是您的面试记录和表现总结。</p>
            <div class="interview-info">
              <div class="info-item">
                <span class="label">面试风格：</span>
                <span class="value">{{ getStyleName(interviewData.style) }}</span>
              </div>
              <div class="info-item">
                <span class="label">完成时间：</span>
                <span class="value">{{ formatDate(interviewData.completedAt) }}</span>
              </div>
              <div class="info-item">
                <span class="label">问题数量：</span>
                <span class="value">{{ interviewData.questions.length }} 个</span>
              </div>
            </div>
          </section>

          <!-- 完整对话记录部分 -->
          <section class="full-conversation">
            <h2>🗣️ 完整对话记录</h2>
            <div class="conversation-list">
              <div
                v-for="(msg, index) in interviewData.conversation"
                :key="index"
                :class="['conversation-item', msg.sender === 'ai' ? 'ai-message' : 'user-message']"
              >
                <div class="sender-avatar">
                  <div :class="['avatar-icon', msg.sender === 'ai' ? 'ai-avatar' : 'user-avatar']">
                    {{ msg.sender === 'ai' ? 'AI' : 'U' }}
                  </div>
                  <span class="sender-label">{{ msg.sender === 'ai' ? '面试官' : '您' }}</span>
                </div>
                <div class="message-content">
                  <p v-html="formatMessage(msg.text)"></p>
                  <span class="message-time">{{ formatTime(msg.timestamp) }}</span>
                </div>
              </div>
            </div>
          </section>

          <!-- AI 专业分析 -->
          <section class="ai-analysis">
            <h2>🤖 AI 专业分析</h2>
            <div class="analysis-card">
              <div v-if="isAnalysisLoading" class="loading-state">
                <div class="spinner"></div>
                <p>正在生成您的专属分析报告，请稍候...</p>
              </div>
              <div v-else v-html="marked(llmAnalysisReport)" class="analysis-report"></div>
            </div>
          </section>

          <!-- Export Options -->
          <section class="export-section">
            <h2>📤 导出选项</h2>
            <div class="export-buttons">
              <button @click="exportJSON" class="export-btn">
                📄 导出 JSON
              </button>
              <button @click="exportText" class="export-btn">
                📝 导出文本
              </button>
              <button @click="printSummary" class="export-btn">
                🖨️ 打印总结
              </button>
            </div>
          </section>

          <!-- Action Buttons -->
          <section class="actions">
            <button @click="startNewInterview" class="action-btn primary">
              🔄 重新面试
            </button>
            <button @click="goHome" class="action-btn secondary">
              🏠 返回首页
            </button>
          </section>
        </div>
      </main>
    </div>
  </template>

  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRouter, useRoute } from 'vue-router'
  import { marked } from 'marked'
  import axios from 'axios';

  const router = useRouter()
  const route = useRoute()

  const interviewData = ref({
    questions: [],
    style: 'professional',
    completedAt: new Date().toISOString()
  })

  // Navigation functions
  const startNewInterview = () => {
    router.push('/interview')
  }

  const goHome = () => {
    router.push('/')
  }

  // 格式化消息时间
  const formatTime = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString('zh-CN', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  // 复用消息格式化方法
  const formatMessage = (text) => {
    return text
      .replace(/\n/g, '<br>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  };

  // Helper functions
  const getStyleName = (style) => {
    const styles = {
      friendly: '亲切友好',
      formal: '正式严肃',
      casual: '校园风格'
    }
    return styles[style] || '未知'
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  // Export functions
  const exportJSON = () => {
    // 包含完整对话记录的导出数据
    const exportData = {
      ...interviewData.value,
      exportAt: new Date().toISOString(),
      metadata: {
        version: '1.0',
        exportType: 'full-interview-record'
      }
    };
    const dataStr = JSON.stringify(exportData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `面试记录_${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const exportText = () => {
    let content = `Kora 语音面试记录\n`;
    content += `==================\n\n`;
    content += `面试风格：${getStyleName(interviewData.value.style)}\n`;
    content += `完成时间：${formatDate(interviewData.value.completedAt)}\n`;
    content += `问题数量：${interviewData.value.questions.length} 个\n\n`;

    // 完整对话记录
    content += `========== 完整对话记录 ==========\n\n`;
    interviewData.value.conversation.forEach((msg) => {
      const sender = msg.sender === 'ai' ? '面试官' : '您';
      content += `${sender}：${msg.text}\n`;
      content += `[${formatTime(msg.timestamp)}]\n\n`;
    });

    const dataBlob = new Blob([content], {type: 'text/plain;charset=utf-8'});
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `面试记录_${new Date().toISOString().split('T')[0]}.txt`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const printSummary = () => {
    window.print()
  }

  const llmAnalysisReport = ref('') // 存储LLM分析报告
  const isAnalysisLoading = ref(true) // 分析加载状态

  const getLLMAnalysis = async () => {
    isAnalysisLoading.value = true
    try {
      // 直接传递原始对象，与后端测试用例格式一致
      const response = await axios.post('/api/analyze', {
        interviewData: interviewData.value // 传递对象而非字符串
      })
      llmAnalysisReport.value = response.data.analysis
    } catch (error) {
      console.error('LLM analysis error:', error)
      llmAnalysisReport.value = '抱歉，AI分析报告生成失败...'
    } finally {
      isAnalysisLoading.value = false
    }
  }

  onMounted(() => {
    const data = route.query.interviewData || route.params.interviewData
    if (data) {
      try {
        interviewData.value = JSON.parse(data)
        getLLMAnalysis() // 获取数据后调用LLM分析
      } catch (error) {
        console.error('Failed to parse interview data:', error)
        llmAnalysisReport.value = '无法解析面试数据，报告生成失败。'
        isAnalysisLoading.value = false
      }
    } else {
      llmAnalysisReport.value = '未找到面试数据，无法生成报告。'
      isAnalysisLoading.value = false
    }
  })
  </script>

<style scoped>
/* 基础样式 */
.summary {
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f9ff 0%, #e6fffa 100%);
}

.header {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(226, 232, 240, 0.7);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 10;
}

.summary-header h1 {
  background: linear-gradient(to right, #059669, #10b981);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  display: inline-block;
}

.analysis-card {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  text-align: center;
  transition: transform 0.3s, box-shadow 0.3s;
  border: 1px solid rgba(226, 232, 240, 0.7);
}

.analysis-card:hover {
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  transform: translateY(-2px);
}

.export-btn {
  background: linear-gradient(to right, #6366f1, #8b5cf6);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 500;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.3), 0 2px 4px -1px rgba(99, 102, 241, 0.2);
}

.export-btn:hover {
  background: linear-gradient(to right, #4f46e5, #7c3aed);
  transform: translateY(-1px);
  box-shadow: 0 6px 10px -1px rgba(99, 102, 241, 0.4), 0 2px 6px -1px rgba(99, 102, 241, 0.2);
}

.action-btn.primary {
  background: linear-gradient(to right, #059669, #10b981);
  color: white;
  box-shadow: 0 4px 6px -1px rgba(5, 150, 105, 0.3), 0 2px 4px -1px rgba(5, 150, 105, 0.2);
}

.action-btn.primary:hover {
  background: linear-gradient(to right, #047857, #059669);
  transform: translateY(-1px);
  box-shadow: 0 6px 10px -1px rgba(5, 150, 105, 0.4), 0 2px 6px -1px rgba(5, 150, 105, 0.2);
}

.logo-icon {
  width: 2rem;
  height: 2rem;
  background: #059669;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  position: relative;
}

.logo-icon span {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

/* 完整对话记录区域 */
.full-conversation {
  margin: 3rem 0;
  padding: 1.5rem;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

.full-conversation h2 {
  font-size: 1.875rem;
  margin-bottom: 1.5rem;
  color: #1e293b;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #059669;
  display: inline-block;
}

.conversation-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  padding: 0.5rem 0;
}

/* 对话项通用样式 */
.conversation-item {
  display: flex;
  gap: 1rem;
  max-width: 85%;
  animation: fadeIn 0.3s ease-out forwards;
  opacity: 0;
}

/* 消息淡入动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* AI消息样式 */
.ai-message {
  align-self: flex-start;
  animation-delay: calc(0.1s * var(--index, 0));
}

.ai-message .message-content {
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 0.3rem 1rem 1rem 1rem;
  position: relative;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* 用户消息样式 */
.user-message {
  align-self: flex-end;
  margin-left: auto;
  animation-delay: calc(0.1s * var(--index, 0));
  flex-direction: row-reverse;
}

.user-message .message-content {
  background-color: #059669;
  color: white;
  border-radius: 1rem 0.3rem 1rem 1rem;
  position: relative;
  box-shadow: 0 2px 8px rgba(5, 150, 105, 0.15);
}

.user-message .sender-label {
  text-align: center;
}

/* 头像样式优化 */
.sender-avatar {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 48px;
  margin-top: 0.25rem;
}

.avatar-icon {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.ai-avatar {
  background-color: #059669;
}

.user-avatar {
  background-color: #3b82f6;
}

.avatar-icon:hover {
  transform: scale(1.05);
}

/* 消息内容样式 */
.message-content {
  flex: 1;
  padding: 1rem 1.25rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.conversation-item:hover .message-content {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.message-content p {
  margin: 0;
  line-height: 1.6;
  word-wrap: break-word;
}

/* 时间戳样式优化 */
.message-time {
  display: inline-block;
  font-size: 0.7rem;
  margin-top: 0.5rem;
  opacity: 0.7;
  text-align: right;
  float: right;
  clear: both;
  padding-left: 1rem;
}

.sender-label {
  font-size: 0.75rem;
  color: #64748b;
  margin-top: 0.25rem;
}

.analysis-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 4rem;
}

.status {
  background: #10b981;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.main {
  padding: 2rem 0;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 2rem;
}

.summary-header {
  text-align: center;
  margin-bottom: 3rem;
}

.summary-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #1e293b;
}

.summary-header p {
  font-size: 1.125rem;
  color: #64748b;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.interview-info {
  display: flex;
  justify-content: center;
  gap: 2rem;
  flex-wrap: wrap;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.label {
  font-weight: 500;
  color: #64748b;
}

.value {
  font-weight: 600;
  color: #1e293b;
}

.export-section, .actions {
  margin-bottom: 3rem;
}

.export-section h2 {
  font-size: 1.875rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: #1e293b;
}

.export-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
}

.export-btn {
  background: #6366f1;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 500;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.export-btn:hover {
  background: #4f46e5;
  transform: translateY(-1px);
}

.actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.action-btn {
  border: none;
  padding: 1rem 2rem;
  font-size: 1.125rem;
  font-weight: 600;
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn.primary {
  background: #059669;
  color: white;
}

.action-btn.primary:hover {
  background: #047857;
  transform: translateY(-1px);
}

.action-btn.secondary {
  background: #f1f5f9;
  color: #475569;
  border: 1px solid #d1d5db;
}

.action-btn.secondary:hover {
  background: #e2e8f0;
  transform: translateY(-1px);
}

/* AI分析部分样式 */
.ai-analysis {
  margin: 3rem 0;
  padding: 1rem;
}

.ai-analysis h2 {
  font-size: 1.875rem;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #059669;
  display: inline-block;
}

.analysis-card {
  background: white;
  border-radius: 1rem;
  padding: 2.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #f0f0f0;
}

.analysis-report {
  line-height: 1.8;
  color: #333;
  font-size: 1rem;
  text-align: left;
}

/* 报告标题样式 */
.analysis-report > strong:first-child {
  font-size: 1.5rem !important;
  display: block;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #eee;
  color: #1e293b;
}

/* 主要部分标题样式 */
.analysis-report ol > li > strong {
  color: #059669;
  font-size: 1.15rem !important;
  display: block;
  margin: 1.5rem 0 0.75rem 0;
}

/* 子项样式 */
.analysis-report ol > li > ol {
  margin-left: 0.5rem;
  padding-left: 1.5rem;
}

/* 引用内容样式强化 */
.analysis-report p:has(> span:contains("> ")) {
  background-color: #f8fafc;
  border-left: 4px solid #059669;
  padding: 1rem;
  margin: 0.75rem 0;
  border-radius: 0 4px 4px 0;
  font-style: italic;
  color: #475569;
}

/* 潜力预估和匹配度部分特殊样式 */
.analysis-report ol > li:nth-child(4),
.analysis-report ol > li:nth-child(5),
.analysis-report ol > li:nth-child(6) {
  margin-top: 1rem;
}

/* 加载状态优化 */
.loading-state {
  text-align: center;
  padding: 3rem 1rem;
}

.spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto 1.5rem;
  border: 4px solid #f0f9ff;
  border-top: 4px solid #059669;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }

  .summary-header h1 {
    font-size: 2rem;
  }

  .interview-info {
    flex-direction: column;
    gap: 1rem;
  }

  .export-buttons, .actions {
    flex-direction: column;
    align-items: center;
  }

  /* 移动端对话样式调整 */
  .conversation-item {
    max-width: 90%;
  }

  .message-content {
    padding: 0.75rem 1rem;
  }

  .full-conversation {
    padding: 1rem;
    margin: 2rem 0;
  }
}

@media print {
  .header, .export-section, .actions {
    display: none;
  }

  .main {
    padding: 0;
  }

  .container {
    max-width: none;
    padding: 0;
  }
}
</style>