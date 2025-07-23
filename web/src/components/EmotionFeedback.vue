<template>
  <!-- 可拖动的小窗模式 -->
  <div 
    v-if="!expanded"
    class="emotion-mini"
    @click="toggleExpand"
    ref="draggable"
    :style="{
      left: `${position.x}px`,
      top: `${position.y}px`
    }"
  >
    <div class="mini-header" @mousedown="startDrag">
      <span class="mini-title">实时情绪分析</span>
      <span class="mini-time">{{ currentTime.toFixed(1) }}s</span>
    </div>
    <div class="time-progress">
      <div class="progress-bar" :style="{ width: `${progressPercentage}%` }"></div>
    </div>
    <div class="mini-bars">
      <div 
        v-for="emotion in emotionList" 
        :key="emotion"
        class="mini-bar"
        :style="{
          height: `${emotions[emotion] * 100}%`,
          background: getEmotionColor(emotion)
        }"
      >
        <span class="bar-label">{{ emotionNames[emotion] }}</span>
      </div>
    </div>
  </div>

  <!-- 放大模式 -->
  <div 
    v-else
    class="emotion-expanded"
    @click="toggleExpand"
    :style="{
      left: `${position.x}px`,
      top: `${position.y}px`
    }"
  >
    <div class="expanded-header" @mousedown="startDrag">
      <h3>实时情绪分析</h3>
      <div class="expanded-time">{{ currentTime.toFixed(1) }}s</div>
    </div>
    <div class="time-progress">
      <div class="progress-bar" :style="{ width: `${progressPercentage}%` }"></div>
    </div>
    <div class="expanded-waves">
      <div 
        v-for="emotion in emotionList" 
        :key="emotion"
        class="wave-item"
      >
        <div class="emotion-info">
          <span class="emotion-label" :style="{ color: getEmotionColor(emotion) }">
            {{ emotionNames[emotion] }}
          </span>
          <span class="emotion-value">
            {{ (emotions[emotion] * 100).toFixed(1) }}%
          </span>
        </div>
        
        <div class="wave-wrapper">
          <div 
            class="wave-progress"
            :style="{
              height: `${emotions[emotion] * 100}%`,
              background: getEmotionColor(emotion)
            }"
          >
            <div class="wave-animation"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  currentTime: {
    type: Number,
    default: 0
  },
  duration: {
    type: Number,
    default: 60
  },
  isInterviewActive: {
    type: Boolean,
    default: false
  },
  emotions: {
    required: true
  }
})

// UI状态
const expanded = ref(false)
const position = ref({ x: window.innerWidth - 240, y: 20 })
const isDragging = ref(false)
const dragStartPos = ref({ x: 0, y: 0 })

// // 数据状态
// const emotionData = ref([])
// const lastFetchTime = ref(0)
// const fetchInterval = 15000 // 15秒请求一次
// const dataCacheDuration = 30000 // 数据缓存30秒
//
// // 模拟数据
// const mockEmotionData = [
//   { time_sec: 0, emotions: { attentiveness: 0.2, confidence: 0.7, confusion: 0.05, frustration: 0.01, nervousness: 0.02} },
//   // ...其他模拟数据保持不变
// ]

const emotionNames = {
  attentiveness: '专心',
  confidence: '信心',
  confusion: '困惑',
  frustration: '挫折',
  nervousness: '紧张',
}

const emotionList = ['attentiveness', 'confidence', 'confusion', 'frustration', 'nervousness']

// 计算属性
const progressPercentage = computed(() => (props.currentTime / props.duration) * 100)

// const currentEmotions = computed(() => {
//   // 使用缓存数据如果仍在有效期内
//   if (Date.now() - lastFetchTime.value < dataCacheDuration && emotionData.value.length > 0) {
//     const closest = findClosestDataPoint(emotionData.value)
//     return closest.emotions || getMockData()
//   }
//   return getMockData()
// })

// // 辅助方法
// function findClosestDataPoint(data) {
//   return data.reduce((prev, curr) =>
//     Math.abs(curr.time_sec - props.currentTime) < Math.abs(prev.time_sec - props.currentTime)
//       ? curr
//       : prev
//   )
// }

// function getMockData() {
//   return findClosestDataPoint(mockEmotionData).emotions || {}
// }

function getEmotionColor(emotion) {
  const colors = {
    frustration: '#e74c3c',
    nervousness: '#f39c12',
    attentiveness: '#2ecc71',
    confusion: '#3498db',
    confidence: '#f1c40f',
  }
  return colors[emotion] || '#95a5a6'
}

// // 数据获取
// async function fetchEmotionData() {
//   if (!props.isInterviewActive) return
//
//   const now = Date.now()
//   if (now - lastFetchTime.value < fetchInterval) return
//
//   try {
//     const response = await handleSentiments()
//     if (response.status === 200 && response.data) {
//       emotionData.value = response.data
//       lastFetchTime.value = now
//     }
//   } catch (error) {
//     console.error('获取情绪数据失败:', error)
//   }
// }

// 定时器
let emotionInterval = null
onMounted(() => {
  window.addEventListener('mousemove', onDrag)
  window.addEventListener('mouseup', stopDrag)
  
  // 减少请求频率，只在面试激活时请求
  // emotionInterval = setInterval(fetchEmotionData, fetchInterval)
})

onBeforeUnmount(() => {
  window.removeEventListener('mousemove', onDrag)
  window.removeEventListener('mouseup', stopDrag)
  // clearInterval(emotionInterval)
})

// UI交互
function toggleExpand() {
  expanded.value = !expanded.value
}

function startDrag(e) {
  isDragging.value = true
  dragStartPos.value = {
    x: e.clientX - position.value.x,
    y: e.clientY - position.value.y
  }
  e.preventDefault()
}

function onDrag(e) {
  if (!isDragging.value) return
  position.value = {
    x: e.clientX - dragStartPos.value.x,
    y: e.clientY - dragStartPos.value.y
  }
}

function stopDrag() {
  isDragging.value = false
}
</script>


<style scoped>
/* 可拖动的小窗样式 - 优化版 */
.emotion-mini {
  position: fixed;
  right: 20px;
  top: 20px;
  width: 260px;
  height: 180px;
  background: rgba(255, 255, 255, 0.98);
  border-radius: 10px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  padding: 12px;
  cursor: move;
  z-index: 1000;
  transition: all 0.3s ease;
  user-select: none;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.mini-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  cursor: move;
}

.mini-title {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  letter-spacing: 0.5px;
}

.mini-time {
  font-size: 12px;
  color: #666;
  background: rgba(0, 0, 0, 0.05);
  padding: 2px 6px;
  border-radius: 4px;
}

.time-progress {
  height: 4px;
  background: rgba(0, 0, 0, 0.08);
  border-radius: 2px;
  margin-bottom: 12px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: #42b983;
  transition: width 0.3s ease;
}

.mini-bars {
  display: flex;
  height: 110px;
  gap: 6px;
  align-items: flex-end;
  margin-top: 10px;
}

.mini-bar {
  flex: 1;
  min-width: 0;
  position: relative;
  border-radius: 4px 4px 0 0;
  transition: height 0.3s ease;
}

.mini-bar::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 6px;
  border-radius: 4px 4px 0 0;
  background: inherit;
  filter: brightness(1.2);
}

.bar-label {
  position: absolute;
  bottom: -24px;
  left: 0;
  right: 0;
  font-size: 10px;
  font-weight: 500;
  color: #555;
  text-align: center;
  white-space: nowrap;
  overflow: visible;
  padding: 0 2px;
  transition: all 0.2s ease;
}

.mini-bar:hover .bar-label {
  color: #222;
  font-weight: 600;
}

/* 放大样式 */
.emotion-expanded {
  position: fixed;
  left: 20px;
  top: 20px;
  width: 400px;
  height: 280px;
  background: rgba(255, 255, 255, 0.96);
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 15px;
  cursor: move;
  z-index: 1000;
  transition: all 0.3s ease;
  user-select: none;
}

.expanded-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  cursor: move;
}

.expanded-header h3 {
  margin: 0;
  font-size: 16px;
  color: #333;
  letter-spacing: 1px;
}

.expanded-time {
  background: #42b983;
  color: white;
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 12px;
  letter-spacing: 0.5px;
}

.expanded-waves {
  display: flex;
  gap: 12px;
  height: 200px;
  align-items: flex-end;
  margin-top: 15px;
}

.wave-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.emotion-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 8px;
}

.emotion-label {
  font-size: 12px;
  font-weight: bold;
  margin-bottom: 4px;
  letter-spacing: 1px;
}

.emotion-value {
  font-size: 11px;
  color: #666;
  letter-spacing: 0.5px;
}

.wave-wrapper {
  width: 100%;
  height: 150px;
  background: #f5f7fa;
  border-radius: 6px;
  position: relative;
  overflow: hidden;
}

.wave-progress {
  position: absolute;
  bottom: 0;
  width: 100%;
  transition: height 0.3s ease;
  border-radius: 6px 6px 0 0;
}

.wave-animation {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 200%;
  background: linear-gradient(
    to bottom,
    rgba(255, 255, 255, 0.2) 0%,
    rgba(255, 255, 255, 0.5) 50%,
    rgba(255, 255, 255, 0.2) 100%
  );
  animation: wave 1.5s linear infinite;
  transform: translateY(-50%);
}

@keyframes wave {
  0% {
    transform: translateY(-50%) translateX(-100%);
  }
  100% {
    transform: translateY(-50%) translateX(100%);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .emotion-mini {
    width: 220px;
    height: 160px;
    right: 10px;
    top: 10px;
  }
  
  .mini-bars {
    height: 90px;
  }
  
  .bar-label {
    font-size: 9px;
    bottom: -22px;
  }
  
  .emotion-expanded {
    width: 90%;
    right: 10px;
    left: auto;
  }
  
  .expanded-waves {
    height: 150px;
  }
  
  .wave-wrapper {
    height: 100px;
  }
}
</style>