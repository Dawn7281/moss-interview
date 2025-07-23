import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useInterviewStore = defineStore('interview', () => {
  const currentInterview = ref(null)
  const chatMessages = ref([])
  
  // 加载面试记录
  const loadInterviewRecord = (record) => {
    currentInterview.value = record
    chatMessages.value = record.messages || []
  }
  
  // 开始新面试
  const startNewInterview = () => {
    currentInterview.value = {
      id: Date.now().toString(),
      position: '新面试',
      createdAt: new Date().toISOString(),
      messages: [
        { role: 'ai', text: '您好！我是面试助手，请问您想进行什么类型的模拟面试？' }
      ]
    }
    chatMessages.value = currentInterview.value.messages
  }
  
  // 添加新消息
  const addMessage = (message) => {
    if (!currentInterview.value) {
      startNewInterview()
    }
    chatMessages.value.push(message)
    currentInterview.value.messages = [...chatMessages.value]
    saveCurrentInterview()
  }
  
  // 保存当前面试到历史记录
  const saveCurrentInterview = () => {
    if (!currentInterview.value) return
    
    const history = JSON.parse(localStorage.getItem('textInterviewHistory') || '[]')
    const existingIndex = history.findIndex(item => item.id === currentInterview.value.id)
    
    if (existingIndex >= 0) {
      history[existingIndex] = currentInterview.value
    } else {
      history.unshift(currentInterview.value)
    }
    
    localStorage.setItem('textInterviewHistory', JSON.stringify(history))
  }
  
  return {
    currentInterview,
    chatMessages,
    loadInterviewRecord,
    startNewInterview,
    addMessage
  }
})