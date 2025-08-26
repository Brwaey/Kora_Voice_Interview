<template>
    <div class="min-h-screen bg-gray-50">
      <!-- Header -->
      <header class="bg-white shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div class="flex items-center"> <!-- 添加 justify-center -->
            <div class="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center mr-3">
              <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clip-rule="evenodd" />
              </svg>
            </div>
            <h1 class="text-xl font-semibold text-gray-900">Kora 语音面试</h1>
          </div>
        </div>
      </header>
  
      <!-- Main Content -->
      <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <!-- Hero Section -->
        <div class="text-center mb-16">
          <h1 class="text-4xl font-bold text-gray-900 mb-4">
            欢迎使用 AI 语音面试官
          </h1>
          <p class="text-lg text-gray-600 max-w-2xl mx-auto">
            体验智能化的中文语音面试，通过结构化的行为面试问题，帮助您提升面试表现和沟通能力。
          </p>
        </div>
  
        <!-- Features -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 flex flex-col items-center text-center">
            <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4 flex-shrink-0">
              <svg class="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clip-rule="evenodd" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">语音识别</h3>
            <p class="text-gray-600">
              先进的中文语音识别技术，准确捕捉您的回答内容
            </p>
          </div>
  
          <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 flex flex-col items-center text-center">
            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4 flex-shrink-0">
              <svg class="w-6 h-6 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3z" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">智能交互</h3>
            <p class="text-gray-600">
              AI 驱动的面试官，提供个性化的追问和反馈
            </p>
          </div>
  
          <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 flex flex-col items-center text-center">
            <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4 flex-shrink-0">
              <svg class="w-6 h-6 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">高效体验</h3>
            <p class="text-gray-600">
              约 5 分钟的结构化面试，快速评估您的表达能力
            </p>
          </div>
        </div>
  
        <!-- Interview Process -->
        <div class="bg-white rounded-xl p-8 shadow-sm border border-gray-100 mb-12">
          <h2 class="text-2xl font-bold text-gray-900 mb-6">面试流程</h2>
          <p class="text-gray-600 mb-8">了解我们的面试过程，为最佳体验做好准备</p>
          
          <div class="space-y-6">
            <div class="flex items-start">
              <div class="flex-shrink-0 w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center font-semibold text-sm">
                1
              </div>
              <div class="ml-4">
                <h3 class="text-lg font-semibold text-gray-900 mb-1">欢迎介绍</h3>
                <p class="text-gray-600">系统将向您介绍面试流程和注意事项</p>
              </div>
            </div>
  
            <div class="flex items-start">
              <div class="flex-shrink-0 w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center font-semibold text-sm">
                2
              </div>
              <div class="ml-4">
                <h3 class="text-lg font-semibold text-gray-900 mb-1">行为面试问题</h3>
                <p class="text-gray-600">回答 3 个结构化的行为面试问题，每个问题都有追问环节</p>
              </div>
            </div>
  
            <div class="flex items-start">
              <div class="flex-shrink-0 w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center font-semibold text-sm">
                3
              </div>
              <div class="ml-4">
                <h3 class="text-lg font-semibold text-gray-900 mb-1">面试总结</h3>
                <p class="text-gray-600">查看您的回答记录和面试表现总结</p>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Start Interview Button -->
        <div class="text-center">
          <button 
            @click="startInterview"
            class="inline-flex items-center px-8 py-4 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 transition-colors duration-200 shadow-lg"
          >
            <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
            </svg>
            开始面试
          </button>
          <p class="text-sm text-gray-500 mt-4">
            请确保您的麦克风已开启，并在安静的环境中进行面试
          </p>
        </div>
      </main>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Home',
    methods: {
      startInterview() {
        this.$router.push('/interview')
      }
    }
  }
  </script>

  <!-- 在<style>标签中添加以下CSS -->
  <style scoped>
  /* 添加渐变背景 */
  .min-h-screen {
    background: linear-gradient(135deg, #f0f9ff 0%, #e6fffa 100%);
  }
  
  /* 美化标题 */
  .text-4xl.font-bold {
    background: linear-gradient(to right, #059669, #10b981);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    display: inline-block;
  }
  
  /* 美化卡片 */
  .bg-white.rounded-xl {
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    border: none;
    transition: transform 0.3s, box-shadow 0.3s;
  }
  
  .bg-white.rounded-xl:hover {
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    transform: translateY(-2px);
  }
  
  /* 美化图标容器 */
  .w-12.h-12 {
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 1rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  }
  
  /* 美化流程数字 */
  .w-8.h-8.bg-green-600 {
    background: linear-gradient(to right, #059669, #10b981);
    box-shadow: 0 2px 4px rgba(5, 150, 105, 0.2);
  }
  
  /* 美化按钮 */
  button.bg-green-600 {
    background: linear-gradient(to right, #059669, #10b981);
    box-shadow: 0 10px 15px -3px rgba(5, 150, 105, 0.3), 0 4px 6px -2px rgba(5, 150, 105, 0.2);
    transition: all 0.3s;
  }
  
  button.bg-green-600:hover {
    background: linear-gradient(to right, #047857, #059669);
    box-shadow: 0 15px 20px -3px rgba(5, 150, 105, 0.4), 0 8px 10px -2px rgba(5, 150, 105, 0.2);
    transform: translateY(-2px);
  }
  /* 在style部分添加 */
  .features-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
  }
  
  .features-grid > div {
    display: flex;
    flex-direction: column;
    align-items: center; /* 居中图标和文字 */
    text-align: center; /* 文字居中 */
  }
  
  .features-grid h3 {
    margin-top: 1rem;
    margin-bottom: 0.5rem;
  }
  
  .features-grid p {
    text-align: center;
  }
  
  /* 确保标题靠左 */
  header h1 {
    text-align: left;
  }
  </style>
  