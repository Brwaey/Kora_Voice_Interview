<template>
  <div class="flex flex-col h-screen bg-gray-100 font-sans">
    <!-- Header -->
    <header class="bg-white shadow-sm flex-shrink-0 z-10">
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
            {{ interviewStatus }}
          </div>
        </div>
      </div>
    </header>

    <!-- Welcome Phase -->
    <div v-if="phase === 'welcome'" class="flex-grow flex items-center justify-center p-4">
        <div class="text-center bg-white rounded-2xl p-8 sm:p-12 shadow-xl border border-gray-200 max-w-2xl mx-auto transform hover:scale-105 transition-transform duration-300">
            <h2 class="text-3xl font-bold text-gray-900 mb-4">开启您的专属面试体验</h2>
            <p class="text-gray-600 mb-8">请选择您偏好的面试风格，Kora将为您模拟最真实的面试场景。</p>
            <div class="mb-8">
              <select v-model="selectedStyle" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 text-lg">
                <option value="friendly">亲切友好型</option>
                <option value="formal">专业严肃型</option>
                <option value="casual">轻松校园型</option>
              </select>
            </div>
            <button @click="startInterview" class="w-full px-6 py-3 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5">
              立即开始
            </button>
        </div>
    </div>

    <!-- Chat Interface -->
    <main v-else ref="chatArea" class="flex-grow overflow-y-auto p-4 sm:p-6">
      <div class="max-w-3xl mx-auto space-y-6">
        <div v-for="(message, index) in messages" :key="index" class="chat-message-wrapper">
          <div :class="['flex items-end space-x-3', message.sender === 'ai' ? 'justify-start' : 'justify-end']">
            <!-- AI Avatar -->
            <div v-if="message.sender === 'ai'" class="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center flex-shrink-0">
              <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
              </svg>
            </div>
            
            <!-- Message Bubble -->
            <div :class="['max-w-[80%] px-4 py-3 rounded-2xl shadow-sm', 
                          message.sender === 'ai' ? 'bg-white text-gray-800 rounded-tl-none' : 
                                                  'bg-green-600 text-white rounded-tr-none']">
              <p v-html="formatMessage(message.text)"></p>
            </div>
            
            <!-- User Avatar -->
            <div v-if="message.sender === 'user'" class="w-10 h-10 rounded-full bg-gray-300 flex items-center justify-center flex-shrink-0">
              <svg class="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
            </div>
          </div>
        </div>
        
        <!-- Typing indicator -->
        <div v-if="isAiTyping" class="flex justify-start">
          <div class="max-w-xs p-4 rounded-2xl shadow-md bg-white">
            <div class="typing-indicator"><span></span><span></span><span></span></div>
          </div>
        </div>
      </div>
    </main>

    <!-- Action Button Area -->
    <footer v-if="showNextButton" class="bg-transparent py-4 px-4 sm:px-6 flex-shrink-0">
        <div class="max-w-3xl mx-auto">
            <div class="flex gap-3">
                <button @click="continueAnswering" class="flex-1 px-6 py-3 bg-gray-600 text-white font-semibold rounded-lg hover:bg-gray-700 transition-all duration-300 shadow-md">
                    继续回答该问题
                </button>
                <button @click="requestNextQuestion" class="flex-1 px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-all duration-300 shadow-md">
                    {{ isLastQuestion ? '完成面试并查看总结' : '好的，请问下一题' }}
                </button>
            </div>
        </div>
    </footer>

    <!-- Input Area -->
    <footer v-if="phase === 'question' && !isAiTyping && !showNextButton" class="bg-white border-t p-3 sm:p-4 flex-shrink-0">
      <div class="max-w-3xl mx-auto">
        <!-- 语音选择和控制区域 -->
        <div class="flex items-center space-x-2 mb-3">
          <select 
            v-model="selectedVoice" 
            class="flex-grow px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 text-sm"
          >
            <option value="">自动选择语音</option>
            <option v-for="voice in filteredVoices" :key="voice.voiceURI" :value="voice">
              {{ voice.name }} ({{ voice.lang }})
            </option>
          </select>
          
          <button 
            @click="toggleVoice" 
            class="p-2 rounded-lg bg-gray-200 hover:bg-gray-300 transition-colors"
            title="开启/关闭语音播放"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path v-if="voiceEnabled" d="M10 15A5 5 0 0015 10a5 5 0 00-5-5-5 5 0 00-5 5 5 5 0 005 5zm0 2a7 7 0 01-7-7 7 7 0 017-7 7 7 0 017 7 7 7 0 01-7 7zm-5-9a1 1 0 011-1h2a1 1 0 110 2H6a1 1 0 01-1-1zm4 5a1 1 0 100-2h2a1 1 0 100-2H9a1 1 0 00-1 1v4a1 1 0 001 1z" />
              <path v-else d="M13 10a1 1 0 000-2h-2a1 1 0 00-1 1v4a1 1 0 001 1h2a1 1 0 000-2h-1v-2h1zM8 10a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1zM10 3a7 7 0 100 14 7 7 0 000-14zm0 16A9 9 0 1110 1a9 9 0 010 18z" />
            </svg>
          </button>
        </div>
        
        <!-- 输入框区域 -->
        <div class="flex items-center space-x-2 sm:space-x-4">
          <button 
            @click="toggleRecording" 
            :class="['p-4 rounded-full text-white transition-all duration-300 shadow-lg relative overflow-hidden', 
                    isRecording ? 'bg-red-500 animate-pulse' : 'bg-green-600 hover:bg-green-700 hover:scale-105']"
          >
            <!-- 未录音状态：麦克风图标 -->
            <svg v-if="!isRecording" class="w-8 h-8" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 1a3 3 0 00-3 3v8a3 3 0 006 0V4a3 3 0 00-3-3zm-1 14a1 1 0 102 0v-1a1 1 0 10-2 0v1zm4 1a1 1 0 00-1-1H8a1 1 0 00-1 1v2a1 1 0 001 1h6a1 1 0 001-1v-2z" />
            </svg>
            
            <!-- 录音状态：带声波的麦克风图标 -->
            <svg v-else class="w-8 h-8" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 1a3 3 0 00-3 3v8a3 3 0 006 0V4a3 3 0 00-3-3zm-1 14a1 1 0 102 0v-1a1 1 0 10-2 0v1zm4 1a1 1 0 00-1-1H8a1 1 0 00-1 1v2a1 1 0 001 1h6a1 1 0 001-1v-2z" />
              <!-- 声波动画元素 -->
              <path class="animate-wave-1" d="M19 10v2a7 7 0 01-14 0v-2" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/>
              <path class="animate-wave-2" d="M21 10v2a9 9 0 01-18 0v-2" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/>
            </svg>
            
            <!-- 录音波纹效果 -->
            <span v-if="isRecording" class="absolute inset-0 rounded-full bg-white opacity-30 animate-ripple"></span>
          </button>
          <textarea v-model="userInput" @keyup.enter.exact="sendMessage" placeholder="请在此输入或点击麦克风回答..." class="flex-grow p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 transition-shadow" rows="1"></textarea>
          <button @click="sendMessage" :disabled="!userInput.trim() && !isRecording" class="px-5 py-3 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 disabled:opacity-50 transition-all duration-300 shadow-md">
            发送
          </button>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const chatArea = ref(null);

// --- 语音相关状态 ---
const voiceEnabled = ref(true); // 默认开启语音
const speechSynthesis = window.speechSynthesis;
const voices = ref([]);
const selectedVoice = ref(null);

// 筛选后的语音列表 - 只保留中文和英文
const filteredVoices = computed(() => {
  // 筛选出中文(zh)和英文(en)语音
  const filtered = voices.value.filter(voice => 
    voice.lang.startsWith('zh') || voice.lang.startsWith('en')
  );
  
  // 排序: 中文在前，英文在后；同一语言内部按名称排序
  return filtered.sort((a, b) => {
    // 先按语言排序(中文优先)
    if (a.lang.startsWith('zh') && !b.lang.startsWith('zh')) return -1;
    if (!a.lang.startsWith('zh') && b.lang.startsWith('zh')) return 1;
    
    // 同语言按名称排序
    return a.name.localeCompare(b.name);
  });
});

// --- 核心状态管理 ---
const phase = ref('welcome');
const selectedStyle = ref('friendly');
const messages = ref([]);
const userInput = ref('');
const isRecording = ref(false);
const interimResult = ref('');
const recordingErrorMessage = ref('');
const currentQuestionIndex = ref(0);
const isAiTyping = ref(false);
const showNextButton = ref(false);

const questions = [
  "你最近完成的一件最有成就感的事是什么？你在其中扮演了什么角色？",
  "请讲讲一次你解决冲突或困难的经历。",
  "如果你加入一个你不熟悉的项目团队，你会如何快速融入？"
];

// --- 计算属性 ---
const interviewStatus = computed(() => {
  if (phase.value === 'finished') return '面试已完成';
  if (phase.value === 'question') return `问题 ${currentQuestionIndex.value + 1}/${questions.length}`;
  return '准备开始';
});
const isLastQuestion = computed(() => currentQuestionIndex.value === questions.length - 1);

// --- 语音控制函数 ---
const toggleVoice = () => {
  voiceEnabled.value = !voiceEnabled.value;
  if (!voiceEnabled.value) {
    speechSynthesis.cancel(); // 关闭语音时停止当前播放
  }
};

const speakText = (text) => {
  if (!voiceEnabled.value) return;
  
  // 清除现有语音队列
  speechSynthesis.cancel();
  
  // 创建语音实例
  const utterance = new SpeechSynthesisUtterance(text);
  
  // 配置语音属性
  utterance.lang = 'zh-CN';
  utterance.rate = 1.15;
  utterance.pitch = 1;
  utterance.volume = 1;
  
  // 使用选中的语音
  if (selectedVoice.value) {
    utterance.voice = selectedVoice.value;
  }
  
  // 播放语音
  speechSynthesis.speak(utterance);
};

// 添加文本净化函数用于语音播放
const cleanTextForSpeech = (text) => {
  // 1. 移除Markdown标记
  let cleanText = text.replace(/\*\*/g, '').replace(/\n/g, ' ');
  
  // 2. 移除常见emoji（覆盖大部分表情符号范围）
  const emojiRegex = /[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F1E0}-\u{1F1FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/gu;
  cleanText = cleanText.replace(emojiRegex, '');
  
  // 3. 移除多余空格
  return cleanText.trim().replace(/\s+/g, ' ');
};

// --- 核心功能函数 ---
const startInterview = () => {
  phase.value = 'question';
  const welcomeMessage = `你好！我是你的AI面试官Kora。很高兴与你交流。\n\n我们开始吧，这是第一个问题：\n**${questions[0]}**`;
  addMessage('ai', welcomeMessage);
  // 使用净化后的文本进行语音播放
  nextTick(() => speakText(cleanTextForSpeech(welcomeMessage)));
};

const sendMessage = async () => {
  const text = userInput.value.trim();
  if (!text) return;
  addMessage('user', text);
  userInput.value = '';
  isAiTyping.value = true;
  await processUserAnswer(text);
};

const processUserAnswer = async (answer) => {
  const currentQ = questions[currentQuestionIndex.value];
  try {
    const response = await axios.post('/api/feedback', {
      question: currentQ, answer, style: selectedStyle.value
    });
    addMessage('ai', response.data.feedback);
    // 播放AI反馈语音
    const plainText = response.data.feedback.replace(/\*\*/g, '').replace(/\n/g, ' ');
    nextTick(() => speakText(cleanTextForSpeech(response.data.feedback)));
  } catch (error) {
    const errorMsg = '抱歉，网络似乎有些问题，我暂时无法连接。';
    addMessage('ai', errorMsg);
    nextTick(() => speakText(errorMsg));
  } finally {
    isAiTyping.value = false;
    showNextButton.value = true;
  }
};

const continueAnswering = () => {
  showNextButton.value = false;
};

const requestNextQuestion = () => {
  showNextButton.value = false;
  if (isLastQuestion.value) {
    endInterview();
  } else {
    isAiTyping.value = true;
    const continueMsg = '好的，我们继续。';
    addMessage('ai', continueMsg);
    nextTick(() => speakText(cleanTextForSpeech(continueMsg)));

    setTimeout(() => {
      currentQuestionIndex.value++;
      const nextQuestion = `接下来是这个问题：\n**${questions[currentQuestionIndex.value]}**`;
      addMessage('ai', nextQuestion);
      const plainText = nextQuestion.replace(/\*\*/g, '').replace(/\n/g, ' ');
      nextTick(() => speakText(cleanTextForSpeech(plainText)));
      isAiTyping.value = false;
    }, 2000);
  }
};

const endInterview = () => {
  phase.value = 'finished';
  isAiTyping.value = true;
  const endMsg = '非常感谢您的参与！本次面试的所有问题都已完成。\n\n我将根据我们刚才的对话，为您生成一份详细的面试表现总结报告。请稍候...';
  addMessage('ai', endMsg);
  const plainText = endMsg.replace(/\*\*/g, '').replace(/\n/g, ' ');
  nextTick(() => speakText(cleanTextForSpeech(plainText)));

  setTimeout(() => {
    // 构建完整对话记录
    const conversation = messages.value.map((msg, index) => ({
      id: index + 1,
      sender: msg.sender,
      text: msg.text,
      timestamp: new Date().toISOString()
    }));

    const interviewData = {
      style: selectedStyle.value,
      completedAt: new Date().toISOString(),
      questions: questions.map((q, index) => {
        const answerMsg = messages.value.find(m =>
                m.sender === 'user' &&
                messages.value.indexOf(m) > messages.value.findIndex(mm =>
                    mm.sender === 'ai' && mm.text.includes(q)
                )
        );

        const feedbackMsg = messages.value.find(m =>
            m.sender === 'ai' &&
            messages.value.indexOf(m) > (answerMsg ? messages.value.indexOf(answerMsg) : -1) &&
            messages.value.indexOf(m) < (index < questions.length - 1 ?
                messages.value.findIndex(mm => mm.text.includes(questions[index + 1])) :
                messages.value.length)
        );

        return {
          id: index + 1,
          text: q,
          answer: answerMsg ? answerMsg.text : '',
          feedback: feedbackMsg ? feedbackMsg.text : ''
        };
      }),
      conversation: conversation
    };
    router.push({name: 'Summary', query: {interviewData: JSON.stringify(interviewData)}});
  }, 2500);
};

// --- 辅助函数 ---
const addMessage = (sender, text) => {
  messages.value.push({sender, text});
  nextTick(() => {
    if (chatArea.value) chatArea.value.scrollTop = chatArea.value.scrollHeight;
  });
};

const formatMessage = (text) => {
  return text
      .replace(/\n/g, '<br>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
};

// --- 语音识别初始化 ---
let recognition = null;
onMounted(() => {
  // 初始化语音合成引擎
  const loadVoices = () => {
    voices.value = speechSynthesis.getVoices();
    // 尝试选择中文语音
    const chineseVoice = voices.value.find(voice =>
        voice.lang.includes('zh-CN') || voice.name.includes('Chinese')
    );
    if (chineseVoice) {
      selectedVoice.value = chineseVoice;
    }
  };

  // 监听语音列表变化
  speechSynthesis.onvoiceschanged = loadVoices;
  loadVoices(); // 立即加载一次

  // 语音识别初始化
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'zh-CN';
    recognition.onresult = (event) => {
      let finalTranscript = '';
      let interimTranscript = '';
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) finalTranscript += event.results[i][0].transcript;
        else interimTranscript += event.results[i][0].transcript;
      }
      interimResult.value = interimTranscript;
      if (finalTranscript) userInput.value += (userInput.value ? ' ' : '') + finalTranscript;
    };
    recognition.onerror = (event) => {
      recordingErrorMessage.value = `语音识别错误: ${event.error}`;
      stopRecording();
    };
  } else {
    recordingErrorMessage.value = '您的浏览器不支持语音识别。';
  }
});

const toggleRecording = () => {
  if (!recognition) return;
  isRecording.value ? stopRecording() : startRecording();
};

const startRecording = () => {
  interimResult.value = '';
  recordingErrorMessage.value = '';
  recognition.start();
  isRecording.value = true;
};

const stopRecording = () => {
  if (recognition) recognition.stop();
  isRecording.value = false;
  if (userInput.value.trim()) sendMessage();
};
</script>

<style scoped>
.h-screen {
  height: 100vh;
}

textarea {
  resize: none;
}

.chat-message-wrapper {
  animation: fadeIn 0.5s ease-in-out;
}

/* 添加录音动效样式 */
@keyframes wave-1 {
  0%, 100% {
    transform: scaleX(0.8);
    opacity: 0.6;
  }
  50% {
    transform: scaleX(1);
    opacity: 1;
  }
}

@keyframes wave-2 {
  0%, 100% {
    transform: scaleX(0.6);
    opacity: 0.4;
  }
  50% {
    transform: scaleX(1);
    opacity: 0.8;
  }
}

@keyframes ripple {
  0% {
    transform: scale(0.5);
    opacity: 1;
  }
  100% {
    transform: scale(2);
    opacity: 0;
  }
}

.animate-wave-1 {
  animation: wave-1 1.5s ease-in-out infinite;
}

.animate-wave-2 {
  animation: wave-2 2s ease-in-out infinite;
}

.animate-ripple {
  animation: ripple 2s linear infinite;
}

/* 调整按钮尺寸和间距 */
button[class*="bg-green-600"],
button[class*="bg-red-500"] {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 修复图标居中显示 */
button svg {
  display: block;
  margin: 0 auto;
}

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

.typing-indicator span {
  height: 8px;
  width: 8px;
  background-color: #9ca3af;
  border-radius: 50%;
  display: inline-block;
  margin: 0 2px;
  animation: bounce 1.4s infinite ease-in-out both;
}

.typing-indicator span:nth-child(1) {
  animation-delay: -0.32s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1.0);
  }
}
</style>