<template>
  <div class="history-sidebar">
    <div class="sidebar-header">
      <h3>📝 文本模拟历史</h3>
      <button class="clear-btn" @click="clearHistory">清空</button>
    </div>
    <div class="history-list">
      <div 
        v-for="(item, index) in userTextHistory" 
        :key="index" 
        class="history-item"
        @click="loadHistory(item)"
      >
        <div class="history-date">{{ formatDate(item.timestamp) }}</div>
        <div class="history-title">{{ item.scene }} - {{ item.mode }}</div>
        <div class="history-summary">
          {{ getFirstMessage(item) }}
        </div>
        <div class="message-count">
          共 {{ item.messages.length }} 条对话
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'

const store = useStore()
const emit = defineEmits(['load'])
const textHistory = ref([])

// 只获取当前用户的历史记录
const userTextHistory = computed(() => {
  if (!store.state.user?.username) return []
  return textHistory.value.filter(item => item.username === store.state.user.username)
})

// 从本地存储加载文本模拟历史
const loadTextHistory = () => {
  const history = JSON.parse(localStorage.getItem('textInterviewHistory') || '[]')
  // 只加载当前用户的历史记录
  textHistory.value = history
    .filter(item => item.username === store.state.user?.username)
    .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
}

const formatDate = (dateString) => {
  const options = { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }
  return new Date(dateString).toLocaleString('zh-CN', options)
}

// 获取第一条消息作为摘要
const getFirstMessage = (item) => {
  if (item.messages.length === 0) return '无对话内容'
  const firstMsg = item.messages[0]
  const text = firstMsg.text.length > 20 
    ? firstMsg.text.substring(0, 20) + '...' 
    : firstMsg.text
  return `${firstMsg.role === 'ai' ? 'AI' : '我'}: ${text}`
}

const loadHistory = (item) => {
  // 验证历史记录是否属于当前用户
  if (item.username !== store.state.user?.username) {
    console.warn('尝试加载其他用户的历史记录')
    return
  }
  emit('load', item)
}

const clearHistory = () => {
  if(confirm('确定要清空所有文本模拟历史记录吗？')) {
    // 只清除当前用户的历史记录
    const updatedHistory = textHistory.value.filter(
      item => item.username !== store.state.user?.username
    )
    localStorage.setItem('textInterviewHistory', JSON.stringify(updatedHistory))
    textHistory.value = [] // 清空当前显示
  }
}

onMounted(() => {
  if (!store.state.user?.username) {
    console.warn('未登录用户尝试访问历史记录')
    return
  }
  loadTextHistory()
})
</script>

<style scoped>
/* 保持原有样式不变 */
.history-sidebar {
  width: 280px;
  height: 100%;
  background: #f8fafc;
  border-right: 1px solid #e0e7ef;
  overflow-y: auto;
  padding: 1rem;
  box-sizing: border-box;
  float: left;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e0e7ef;
  margin-bottom: 1rem;
}

.sidebar-header h3 {
  margin: 0;
  color: #2b7a78;
  font-size: 1.1rem;
}

.clear-btn {
  background: none;
  border: none;
  color: #e74c3c;
  font-size: 0.8rem;
  cursor: pointer;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
}

.clear-btn:hover {
  background: #ffeeee;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.history-item {
  background: #fff;
  border-radius: 8px;
  padding: 0.8rem;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  border-left: 3px solid #42b983;
}

.history-item:hover {
  background: #f0f9ff;
  transform: translateX(3px);
}

.history-date {
  font-size: 0.75rem;
  color: #888;
  margin-bottom: 0.3rem;
}

.history-title {
  font-weight: bold;
  color: #2b7a78;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  line-height: 1.5;
}

.history-summary {
  font-size: 0.85rem;
  color: #555;
  line-height: 1.4;
  margin-bottom: 0.5rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.message-count {
  font-size: 0.7rem;
  color: #999;
  text-align: right;
}
</style>