<template>
  <div class="history-container">
    <h2>历史面试报告</h2>
    <div class="growth-track-container">
      <button class="drop-btn" @click="showGrowthTrack = true">
        <!-- 雨滴元素 -->
        <div class="raindrops">
          <div v-for="i in 5" :key="i" class="raindrop" :style="`left: ${i * 15 - 10}%; animation-delay: ${i * 0.2}s`"></div>
        </div>
        <div class="drop-shape"></div>
        <div class="drop-content">
          <span class="btn-icon">📈</span>
          <span class="btn-text">成长轨迹</span>
        </div>
        <div class="drop-highlight"></div>
        <div class="drop-waves">
          <div class="wave wave1"></div>
          <div class="wave wave2"></div>
        </div>
        <!-- 水滴飞溅效果 -->
        <div class="splash-container">
          <div v-for="i in 6" :key="i" class="splash-drop" :style="`left: ${i * 15}%; animation-delay: ${0.5 + i * 0.1}s`"></div>
        </div>
      </button>
    </div>
     
   <!-- 无历史报告时的提示 -->
<div v-if="!hasReports" class="empty-history">
  <!-- 替换img标签为内联SVG -->
 <svg class="empty-image" viewBox="0 0 24 24" aria-hidden="true">
  <path class="document-main" d="M19 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2zm0 16H5V5h14v14z"/>
  <path class="document-lines" d="M11 7h2v2h-2zm4 4h-2v2H9v-2H7V9h2V7h2v2h2zm-8 8v-1H5v1h2zm2 0v-1H7v1h2zm2 0v-1H9v1h2zm2 0v-1h-2v1h2zm2 0v-1h-2v1h2zm2 0v-1h-2v1h2z"/>
  <path class="document-highlight" d="M8 16h8v1H8z"/>
</svg>
  <p class="empty-text">暂无面试历史记录</p>
  <p class="empty-subtext">开始一次面试，记录您的成长轨迹</p>
</div>

    <div class="report-list">
      <div 
         v-for="(report, index) in reversedReports" 
         :key="index" 
         class="report-item"
       >
        <div class="report-summary">
          <div>
            <div class="report-date">{{ formatDate(report.date) }}</div>
            <div class="report-event">面试场景：{{ sceneOptions[report.scene] }}</div>
            <div class="report-event">面试类型：{{ typeOptions[report.type] }}</div>
            <div class="report-event">面试压力等级：{{ levelOptions[report.level] }}</div>
            <div class="report-event report-job-role">面试岗位：{{ report.job_role }}</div>
            <div class="report-summary-text">
              <strong>总分：</strong> {{ report.fullReport.overall_recommendation?.total_score }}
            </div>
            <div class="report-summary-text">
              <strong>综合建议：</strong>
              {{ report.fullReport.overall_recommendation?.decision }}，
              {{ report.fullReport.overall_recommendation?.reasoning }}
            </div>
            
          </div>
        </div>
        <transition name="slide">

          <div v-if="expandedIndex === index && report.fullReport" class="report-detail">
            <InterviewReport :report-data="report.fullReport" />
            
          </div>
        </transition>
        <button class="detail-btn" @click="toggleReport(index, $event)">
          {{ expandedIndex === index ? '收起' : '查看详情' }}
        </button>
      </div>
    </div>

    <!-- 成长轨迹详情框 -->
    <div v-if="showGrowthTrack" class="growth-track-modal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>面试成长轨迹</h3>
          <button class="close-btn" @click="showGrowthTrack = false">×</button>
        </div>
        <div class="modal-body">
          <div ref="chart" class="chart-container"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick, computed } from 'vue' 
import InterviewReport from './InterviewReport.vue'
import {getHistory} from "@/api/interview";
import store from "@/store";
import * as echarts from 'echarts';

const reports = ref([])
const expandedIndex = ref(null)
const showGrowthTrack = ref(false)
const chart = ref(null)
// 计算属性：判断是否有历史报告
const hasReports = computed(() => reports.value.length > 0)

const sceneOptions = {
  'text': '文本模拟',
  'audio': '语音模拟',
  'video': '视频模拟',
}

const typeOptions = {
  'hr': 'HR 初面',
  'business': '业务面试',
  'final': '终面'
}

const levelOptions = {
  'mild': '轻松模式',
  'medium': '普通模式',
  'high': '高压模式'
}

// 格式化日期
function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    timeZone: 'Asia/Shanghai'
  });
}

// 切换报告展开状态
function toggleReport(index, e) {
  e.stopPropagation()
  expandedIndex.value = expandedIndex.value === index ? null : index
}
function addNewReport(newReport) {
  reports.value = [newReport, ...reports.value]; // 添加到数组开头
}
// // 保存报告到历史记录
// function saveReportToHistory(report) {
//   const history = JSON.parse(localStorage.getItem('interviewHistory') || '[]')
//   history.unshift({
//     date: new Date().toISOString(),
//     event: report.event || '技术面试',
//     summary: report.overall_recommendation, // 综合建议
//     fullReport: report // 完整报告
//   })
//   localStorage.setItem('interviewHistory', JSON.stringify(history))
// }
// 初始化折线图
// 初始化折线图
const reversedReports = computed(() => [...reports.value].reverse());

function initChart() {
  if (!chart.value) return;
  const myChart = echarts.init(chart.value);
  
  // 直接使用 reports.value（已经是升序）
  const dates = reports.value.map(report => formatDate(report.date));
  const scores = reports.value.map(report => report.fullReport.overall_recommendation?.total_score || 0);

  const option = {
    title: {
      text: '面试成绩趋势',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      formatter: '{b}<br/>总分: {c}'
    },
    xAxis: {
      type: 'category',
      data: dates,
      axisLabel: {
        rotate: 45,
        formatter: function (value) {
          const date = new Date(value);
          return `${(date.getMonth() + 1).toString().padStart(2, '0')}/${date.getDate().toString().padStart(2, '0')}`;
        }
      }
       },
    yAxis: {
      type: 'value',
      min: 0,
      max: 100
    },
    series: [{
      data: scores,
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 8,
      itemStyle: {
        color: '#2b7a78'
      },
      lineStyle: {
        color: '#2b7a78',
        width: 3
      },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(43, 122, 120, 0.2)' },
          { offset: 1, color: 'rgba(43, 122, 120, 0)' }
        ])
      }
    }]
  };
    myChart.setOption(option);
  window.addEventListener('resize', () => myChart.resize());
}
// 加载历史报告（实际应从后端或本地存储获取）
// 修改 onMounted 中的排序逻辑
onMounted(async () => {
  let combinedHistory = [];
  
  try {
    const res = await getHistory(store.state.user.username);
    if (res.status === 200) {
      combinedHistory = res.data.map(item => ({
        ...item,
        fullReport: {
          ...item.fullReport,
          dialogue_records: item.chatlog || []
        }
      }));
    }
  } catch (e) {
    console.error('后端获取失败:', e);
  }
  
  // 保持升序（从早到晚），但通过计算属性反转显示顺序
  reports.value = combinedHistory.sort((a, b) => new Date(a.date) - new Date(b.date));
});

// const storageListener = () => {
//   try {
//     const localHistory = JSON.parse(localStorage.getItem('interviewHistory') || '[]');
//     reports.value = [
//       ...localHistory,
//       ...reports.value.filter(r => !localHistory.some(l => l.date === r.date))
//     ];
//   } catch (e) {
//     console.error('监听存储变化出错:', e);
//   }
// };

// onMounted(() => {
//   window.addEventListener('storage', storageListener);
// });

// onUnmounted(() => {
//   window.removeEventListener('storage', storageListener);
// });
// 监听详情框显示变化
watch(showGrowthTrack, (newVal) => {
  if (newVal) {
    nextTick(() => {
      initChart();
    });
  }
});
</script>

<style scoped>
.history-container {
   max-width: 1300px;
  margin: 0 auto;
  margin-left: -3.9rem;
  padding: 0 2rem 2rem 2rem;
  position: relative; /* 为绝对定位的子元素提供参考 */
  min-height: 100vh; /* 确保容器有足够高度 */
}
h2 {
  color: #2b7a78;
  margin-top: 0.01rem;
  margin-bottom: 2.5rem;
  text-align: center;
}

.report-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.report-item {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: visible;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  padding: 2rem 2rem;
}

.report-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.report-summary {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: space-between;
  gap: 2rem;
  width: 100%;
}

.report-summary > div {
  flex: 1 1 auto;
  min-width: 0;
}

.report-date {
  font-weight: bold;
  color: #2b7a78;
}

.report-event {
 color: #888; /* 从#888改为#555，提高可读性 */
  margin: 0.8rem 0; /* 从0.5rem改为0.8rem，增加间距 */
  font-size: 1.05rem; /* 新增：稍微增大字体 */
  line-height: 0.8; /* 新增：调整行高 */
  letter-spacing: 0.2px; 
}

.report-summary-text {
  margin-top: 0.5rem;
  color: #333;
  font-size: 1rem;
  word-break: break-all;
  white-space: pre-line;
  line-height: 1.8;
}

.detail-btn {
  margin: 1.5rem 0 0 0;
  align-self: flex-start;
  background: none;
  color: #2b7a78;
  border: none;
  border-radius: 0;
  padding: 0;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  transition: color 0.2s;
}

.detail-btn:hover {
  color: #42b983;
}

.report-detail {
  padding: 0;
  background: none;
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
  max-height: 1000px;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  max-height: 0;
  padding: 0;
}

/* 水滴按钮样式 */
.growth-track-container {
  position: absolute;
  top: -1.5rem;
  right: -11rem;
  z-index: 100;
}

.drop-btn {
  position: relative;
  width: 140px;
  height: 140px;
  border: none;
  background: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.drop-shape {
  position: absolute;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #68abe6 0%, #64babe 100%);
  border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
  box-shadow: 
    0 8px 20px rgba(79, 172, 254, 0.3),
    inset -5px -5px 10px rgba(0, 0, 0, 0.1),
    inset 5px 5px 10px rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.drop-btn:hover .drop-shape {
  border-radius: 50% 50% 50% 50% / 40% 40% 60% 60%;
  transform: scale(1.05);
  box-shadow: 
    0 12px 25px rgba(79, 172, 254, 0.4),
    inset -8px -8px 15px rgba(0, 0, 0, 0.1),
    inset 8px 8px 15px rgba(255, 255, 255, 0.4);
}

.drop-content {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  color: white;
  font-weight: bold;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
  z-index: 2;
}

.btn-icon {
  font-size: 1.8rem;
  transition: all 0.3s ease;
}

.btn-text {
  font-size: 0.9rem;
  letter-spacing: 0.5px;
}

.drop-btn:hover .btn-icon {
  transform: translateY(-3px) scale(1.1);
  animation: dropBounce 0.8s ease infinite;
}

@keyframes dropBounce {
  0%, 100% { transform: translateY(-3px) scale(1.1); }
  50% { transform: translateY(-6px) scale(1.2); }
}

/* 高光效果 */
.drop-highlight {
  position: absolute;
  top: 20%;
  left: 20%;
  width: 30%;
  height: 30%;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  filter: blur(3px);
  z-index: 1;
  transition: all 0.3s ease;
}

.drop-btn:hover .drop-highlight {
  top: 15%;
  left: 15%;
  width: 35%;
  height: 35%;
  background: rgba(255, 255, 255, 0.4);
}

/* 波纹效果 */
.drop-waves {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  overflow: hidden;
  border-radius: 50%;
  pointer-events: none;
}

.wave {
  position: absolute;
  width: 200%;
  height: 200%;
  top: -50%;
  left: -50%;
  background: radial-gradient(circle at center, rgba(79, 172, 254, 0.2) 0%, transparent 60%);
  border-radius: 40% 60% 60% 40% / 50% 50% 50% 50%;
  animation: waveRotate 8s linear infinite;
  opacity: 0;
}

.wave1 { animation-delay: 0s; }
.wave2 { animation-delay: -4s; }

@keyframes waveRotate {
  0% {
    transform: rotate(0deg) scale(0.5);
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    transform: rotate(360deg) scale(1);
    opacity: 0;
  }
}

/* 点击效果 */
.drop-btn:active .drop-shape {
  transform: scale(0.98);
  transition: all 0.1s ease;
}

.drop-btn:active::after {
  content: '';
  position: absolute;
  width: 80%;
  height: 80%;
  background: radial-gradient(circle at center, rgba(255, 255, 255, 0.3) 0%, transparent 70%);
  border-radius: 50%;
  animation: clickRipple 0.6s ease-out;
}

@keyframes clickRipple {
  0% { transform: scale(0); opacity: 0.6; }
  100% { transform: scale(2); opacity: 0; }
}
/* 添加雨滴样式 */
.raindrops {
  position: absolute;
  width: 120%;
  height: 120%;
  top: -20%;
  left: -10%;
  z-index: 3;
  pointer-events: none;
}

.raindrop {
  position: absolute;
  width: 8px;
  height: 12px;
  background: rgba(210, 216, 218, 0.8);
  border-radius: 50% 50% 60% 40% / 70% 70% 30% 30%;
  animation: raindropFall 4s linear infinite;
  opacity: 0;
}

@keyframes raindropFall {
  0% {
    transform: translateY(-20px) scaleX(1);
    opacity: 0;
  }
  10% {
    opacity: 0.8;
  }
  70% {
    opacity: 0.8;
  }
  100% {
    transform: translateY(80px) scaleX(0.5);
    opacity: 0;
  }
}

/* 水滴飞溅效果 */
.splash-container {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  z-index: 4;
  pointer-events: none;
}

.splash-drop {
  position: absolute;
  width: 4px;
  height: 4px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  bottom: 20%;
  opacity: 0;
  transform: scale(0);
}

.drop-btn:hover .splash-drop {
  animation: splash 1.5s ease-out infinite;
}

@keyframes splash {
  0% {
    transform: translateY(0) scale(0);
    opacity: 0;
  }
  10% {
    opacity: 0.8;
  }
  30% {
    transform: translateY(-30px) scale(1.2);
    opacity: 0;
  }
  100% {
    transform: translateY(-60px) scale(0);
    opacity: 0;
  }
}

/* 增强水滴按钮的悬停效果 */
.drop-btn:hover .raindrop {
  animation: raindropFallHover 1.5s linear infinite;
}

@keyframes raindropFallHover {
  0% {
    transform: translateY(-15px) scaleX(1);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  70% {
    opacity: 1;
  }
  100% {
    transform: translateY(60px) scaleX(0.5);
    opacity: 0;
  }
}
/* 成长轨迹详情框样式 */
.growth-track-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.modal-header {
  padding: 1.5rem;
  background: linear-gradient(135deg, #65b0db 0%, #96cded 100%);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.5rem;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0 0.5rem;
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  max-height: calc(80vh - 6rem);
}

.chart-container {
  width: 100%;
  height: 400px;
}
/* 空状态样式 */
.empty-history {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 0;
  text-align: center;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 1rem;
}

.empty-image {
  width: 350px;
  height: 350px;
  margin-bottom: 1.5rem;
  opacity: 0.7;
}
/* 呼吸动画 */
.document-main {
  fill: #2b7a78;
  fill-opacity: 0.5;
  animation: breathe 3s ease-in-out infinite;
  transform-origin: center;
}

.document-lines {
  fill: #2b7a78;
  animation: fade 4s ease-in-out infinite;
}

.document-highlight {
  fill: #2b7a78;
  fill-opacity: 0.7;
  animation: highlight 2s ease-in-out infinite;
}

@keyframes breathe {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

@keyframes fade {
  0%, 100% { opacity: 0.8; }
  50% { opacity: 1; }
}

@keyframes highlight {
  0%, 100% { fill-opacity: 0.7; }
  50% { fill-opacity: 0.9; }
}
.empty-text {
  font-size: 1.5rem;
  color: #2b7a78;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.empty-subtext {
  color: #888;
  font-size: 0.95rem;
}
/* 对话记录部分样式 */
.dialogue-section {
  margin-top: 2.5rem;
  border-top: 2px solid #42b983;
  padding-top: 1.5rem;
}

.dialogue-section h3 {
  color: #2b7a78;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.dialogue-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.dialogue-item {
  background: #f8fafc;
  border-radius: 8px;
  padding: 1.2rem 1.5rem;
  box-shadow: 0 1px 4px rgba(66, 185, 131, 0.06);
  transition: transform 0.2s;
}

.dialogue-item:hover {
  transform: translateX(4px);
}

.dialogue-question, 
.dialogue-answer {
  margin-bottom: 0.8rem;
  line-height: 1.6;
  word-break: break-word;
}

.speaker {
  font-weight: bold;
  color: #2c3e50;
}

.dialogue-question .speaker {
  color: #e74c3c;
}

.dialogue-answer .speaker {
  color: #3498db;
}

.dialogue-feedback {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px dashed #ddd;
}

.feedback-title {
  font-weight: bold;
  color: #e67e22;
  margin-bottom: 0.5rem;
}

.feedback-content {
  white-space: pre-wrap;
  font-family: inherit;
  line-height: 1.6;
  color: #555;
  background: #f0f4f8;
  padding: 0.8rem;
  border-radius: 4px;
  font-size: 0.95rem;
}

@media (max-width: 768px) {
  .dialogue-item {
    padding: 1rem;
  }
  
  .dialogue-section h3 {
    font-size: 1.3rem;
  }
  
  .feedback-content {
    font-size: 0.9rem;
  }
}
</style>