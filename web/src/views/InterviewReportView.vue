<template>
  <div class="report-view">
    <div class="report-container"> <!-- 确保这个div会闭合 -->
      <div class="report-header">
        <h1>面试评估报告</h1>
      </div>
      
      <!-- 空状态提示 - 优化后的艺术字版本 -->
      <div class="empty-report-container">
      <div v-show="!reportData" class="empty-report">
        <div class="empty-icon">📊</div>
        <div class="empty-title">
          <span class="letter" v-for="(char, index) in '暂无报告数据'" :key="index" :style="{animationDelay: `${index * 0.1}s`}">
            {{ char }}
          </span>
        </div>
        <div class="empty-subtitle">请先完成面试流程以生成评估报告</div>
        <button class="empty-action-btn" @click="goToInterview">开始面试</button>
      </div>
    </div>
      
       <div v-if="reportData" class="report-container">
        <!-- 雷达图与情绪波动图并排展示 -->
        <div class="charts-row">
          <!-- 雷达图 -->
          <div class="radar-section">
            <div class="radar-canvas-wrap">
              <canvas ref="radarChart" width="400" height="400"></canvas>
            </div>
            <div class="chart-title">能力雷达图</div>
          </div>
          
          <!-- 情绪波形图或评分标准说明 -->
          <div v-if="MoodWaveform" class="chart-section chart-scrollable wave-section">
            <div class="wave-canvas-wrap">
              <canvas
                ref="emotionWaveChart"
                width="400"
                height="400"
                style="display:block;width:400px;height:400px;"
              ></canvas>
            </div>
            <div class="chart-title">实时情绪波形图</div>
          </div>
          
          <div v-else class="chart-section chart-scrollable">
            <div class="chart-title">评分标准说明</div>
            <div class="score-criteria">
              所有单项能力评分统一使用1~5分<br>
              5分: 表现非常出色，远超岗位预期，有清晰证据支持<br>
              4分: 表现良好，达到岗位要求，偶有小缺陷<br>
              3分: 基本符合要求，存在可改善空间<br>
              2分: 略低于岗位要求，能力不足较明显<br>
              1分: 远未达标，表现存在较大短板
            </div>
          </div>
        </div>
        
        <!-- 能力分数与证据 -->
        <div class="report-section">
          <h3>专业能力评分</h3>
          <div class="score-section">
            <div v-for="(item, key) in reportData.ability_scores" :key="key" class="score-item">
              <div class="score-title">{{ key }}：{{ item.score }}/5</div>
              <div class="star-rating">
                <span 
                  v-for="star in 5" 
                  :key="star" 
                  class="star" 
                  :class="{ 'filled': star <= item.score }"
                >★</span>
              </div>
              <div class="score-evidence">{{ item.evidence }}</div>
            </div>
          </div>
        </div>
        
        <!-- 问题洞察 -->
        <div class="insight-section">
          <h3>问题洞察与建议</h3>
          <div v-for="insight in reportData.problem_insights" :key="insight.dimension" class="insight-item">
            <div>
              <strong>{{ insight.dimension }}</strong>：
              <span class="insight-issue">{{ insight.issue }}</span>
            </div>
            <div class="insight-suggestion">建议：{{ insight.suggestion }}</div>
          </div>
        </div>
        
        <!-- 总结建议 -->
        <div class="summary-section">
          <h3>综合建议</h3>
          <div><strong>结论：</strong>{{ reportData.overall_recommendation.decision }}</div>
          <div><strong>理由：</strong>{{ reportData.overall_recommendation.reasoning }}</div>
          <div><strong>建议：</strong>{{ reportData.overall_recommendation.closing_remark }}</div>
        </div>

         <div class="dialogue-section">
          <h3>面试对话记录与分析</h3>
          <div class="dialogue-list">
            <div 
              v-for="(item, index) in dialogueRecords"
              :key="index" 
              class="dialogue-item"
              @click="pushFeedback(item.feedback)"
            >
            <!-- 添加悬停提示 -->
             <div class="dialogue-tooltip">点击可跳转到学习资源推荐</div>
              <div class="dialogue-question">
                <span class="speaker">面试官：</span>
                {{ item.interviewer }}
              </div>
              <div class="dialogue-answer">
                <span class="speaker">候选人：</span>
                {{ item.candidate }}
              </div>
              <div class="dialogue-feedback" v-if="item.feedback">
                <div class="feedback-title">反馈分析：</div>
                <pre class="feedback-content">{{ item.feedback }}</pre>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div> 
    
   <!-- 加载提示 - 绝对定位覆盖 -->
    <div v-if="generatingReport" class="loading-overlay">
      <div class="loading-content">
        <div class="spinner"></div>
        <div class="loading-text-container">
          <p class="loading-text">正在生成报告</p>
          <p class="loading-subtext">请稍候，这可能需要几秒钟...</p>
        </div>
      </div>
    </div>
      
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import Chart from 'chart.js/auto'
import { useRoute, useRouter } from 'vue-router'
import {endSentiments, textReport} from "@/api/interview";
import store from "@/store";

const MoodWaveform = ref(true)
const reportData = ref(null)
const radarChart = ref(null)
const emotionWaveChart = ref(null)
const generatingReport = ref(false)
let radarChartInstance = null
let emotionWaveChartInstance = null
const route = useRoute()
const router = useRouter()

const pushFeedback =(feedback) => {
  router.push({
    path: '/graph',
    query: {
      feedback: feedback,
    }
  });
}

const abilityOrder = [
  "专业知识水平",
  "技能匹配度",
  "逻辑思维能力",
  "语言表达能力",
  "应变与抗压能力"
]
const dialogueRecords = ref([
  {
    interviewer: "你好，请简单介绍一下自己吧。",
    candidate: "结束",
    feedback: "【准确率】：0%\n\n【反馈】：候选人未提供任何有效信息，回答内容为空，完全未响应问题要求。\n\n【改进建议】：\n– 需按照问题要求进行自我介绍，包括基本信息、教育背景、工作/实习经历、技能特长等核心内容\n– 应控制回答时长在1-2分钟，重点突出与岗位相关的个人优势\n– 可增加实践案例或项目成果佐证能力，避免空泛陈述\n– 注意语言简洁流畅，逻辑层次清晰，展现沟通能力"
  },
  {
    interviewer: "请描述一下你在上一个项目中的角色和贡献。",
    candidate: "在那个项目中，我负责了部分模块的开发工作，主要是前端页面的实现。",
    feedback: "【准确率】：60%\n\n【反馈】：候选人提供了基本的信息，但描述较为简略，缺乏具体数据和成果支撑。\n\n【改进建议】：\n– 使用STAR法则（情境-任务-行动-结果）描述项目经历\n– 量化贡献，如：\"通过优化代码使页面加载速度提升30%\"\n– 突出遇到的挑战及解决方案\n– 强调个人成长和收获"
  }
])
const props = defineProps({
  reportData: {
    type: Object,
    required: true
  },
  emotionFrames: {
    type: Array,
    default: () => []
  }
});


const emotionFrames = ref([
  {
    interview_emotions: {
      attentiveness: 0,
      confidence: 0,
      confusion: 0,
      frustration: 0,
      nervousness: 0,
    },
    time_sec: 0
  },
])
// if (history.state?.emotionFrames) {
//   try {
//     emotionFrames.value = JSON.parse(history.state?.emotionFrames)
//   } catch (e) {}
// }
function downsampleEmotionFrames(frames, intervalSec = 30) {
  if (!frames.length) return []
  const result = [frames[0]]
  let lastTime = frames[0].time
  for (const frame of frames) {
    if (frame.time - lastTime >= intervalSec) {
      result.push(frame)
      lastTime = frame.time
    }
  }

const reportData = ref({
  dialogue_records: dialogueRecords,
  // 其他报告数据...
})

  // 保证最后一个点也在
  if (result[result.length - 1] !== frames[frames.length - 1]) {
    result.push(frames[frames.length - 1])
  }
  return result
}

function getEmotionColor(key) {
  const colorMap = {
    frustration: '#e74c3c',
    nervousness: '#f39c12',
    attentiveness: '#2ecc71',
    confusion: '#3498db',
    confidence: '#f1c40f',
  }
  return colorMap[key] || '#888'
}
function renderRadarChart() {
  if (!reportData.value || !radarChart.value) return
  if (radarChartInstance) radarChartInstance.destroy()
  radarChartInstance = new Chart(radarChart.value, {
    type: 'radar',
    data: {
      labels: Object.keys(reportData.value.radar_data),
      datasets: [{
        label: '能力评估',
        data: Object.values(reportData.value.radar_data),
        backgroundColor: 'rgba(66,185,131,0.2)',
        borderColor: 'rgba(66,185,131,1)',
        borderWidth: 2,
        pointBackgroundColor: 'rgba(66,185,131,1)'
      }]
    },
    options: {
      responsive: false,
      maintainAspectRatio: false,
      scales: {
        r: {
          min: 0,
          max: 5,  // 修改为5分制
          ticks: { 
            stepSize: 1,  // 刻度间隔改为1
            callback: function(value) {
              return value + '/5'  // 显示为1/5, 2/5等格式
            }
          }
        }
      },
      plugins: {
        legend: { display: false }
      }
    }
  })
}
function renderEmotionWaveChart() {
  if (!emotionWaveChart.value) return
  if (emotionWaveChartInstance) emotionWaveChartInstance.destroy()
  const sampledFrames = emotionFrames.value
  const emotionKeys = ['confidence', 'nervousness', 'frustration', 'attentiveness', 'confusion']
  const timeLabels = sampledFrames.map(item => item.time_sec.toFixed(1))
  const emotionDatasets = emotionKeys.map(key => ({
    label: key,
    data: sampledFrames.map(item => item.interview_emotions[key]),
    fill: false,
    borderColor: getEmotionColor(key),
    backgroundColor: getEmotionColor(key),
    tension: 0.3,
    pointRadius: 1.5
  }))
  emotionWaveChartInstance = new Chart(emotionWaveChart.value, {
    type: 'line',
    data: {
      labels: timeLabels,
      datasets: emotionDatasets
    },
    options: {
      responsive: false, // 关键
      maintainAspectRatio: false,
      scales: {
        x: {
          ticks: {
            autoSkip: true,
            maxTicksLimit: 10
          }
        },
        y: {
          min: 0,
          max: 1,
          ticks: { stepSize: 0.2 }
        }
      },
      plugins: {
        legend: { display: false }
      }
    }
  })
}

onMounted(async () => {
  try {
    generatingReport.value = true
    if (history.state?.type === 'video' || history.state?.type === 'audio') {
      MoodWaveform.value = true
      // const res = await endSentiments(store.state.user?.username)
      // if (res?.status === 200) {
      //   reportData.value = res.data.evaluation;
      //   emotionFrames.value = res.data.emotions;
      //   dialogueRecords.value = res.data.chatlog;
      //
      //   await nextTick();
      //   renderRadarChart();
      //   renderEmotionWaveChart();
      //
      //   // 确保在这里才保存数据
      //   saveReportToHistory(res.data.evaluation);
      // }
      reportData.value = JSON.parse(history.state?.reportData);
      emotionFrames.value = [...emotionFrames.value, ...JSON.parse(history.state?.emotionFrames)];
      dialogueRecords.value = JSON.parse(history.state?.dialogueRecords);

      await nextTick();
      renderRadarChart();
      renderEmotionWaveChart();

    } else if (history.state?.type === 'text') {
      MoodWaveform.value = false
      const res = await textReport(store.state.user?.username)
      if (res?.status === 200) {
        reportData.value = res.data.evaluation;
        // emotionFrames.value = res.data.emotions;
        dialogueRecords.value = res.data.chatlog;

        await nextTick();
        renderRadarChart();
        // renderEmotionWaveChart();

        // 确保在这里才保存数据
        // saveReportToHistory(res.data.evaluation);
      }
    }
  } finally {
    generatingReport.value = false;
  }
})

watch(reportData, async () => {
  await nextTick()
  renderRadarChart()
})

// // 生成报告后
// saveReportToHistory(reportData.value)
//
// router.push({
//   name: 'InterviewReport',
//   query: {
//     emotionFrames: JSON.stringify(emotionFrames)
//   }
// })

function saveReportToHistory(report, emotionFrames = []) {
  if (!report) return;

  try {
    const history = JSON.parse(localStorage.getItem('interviewHistory') || '[]');
    history.unshift({
      date: new Date().toISOString(),
      event: report.event || '技术面试',
      summary: report.overall_recommendation,
      fullReport: report,
      emotionFrames: emotionFrames  // 新增情绪数据
    });
    localStorage.setItem('interviewHistory', JSON.stringify(history));
  } catch (e) {
    console.error('保存历史记录失败:', e);
  }
}
</script>

<style scoped>
.dialogue-item {
  position: relative; /* 为提示定位做准备 */
}

.dialogue-tooltip {
  position: absolute;
  top: -12px;
  left: 360px;
  background-color: #42b983;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 16px;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s, visibility 0.3s;
  z-index: 10;
  white-space: nowrap;
}

.dialogue-item:hover .dialogue-tooltip {
  opacity: 1;
  visibility: visible;
}

/* 调整对话项的内边距，防止提示被截断 */
.dialogue-item {
  padding-top: 18px;
}
.empty-report {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 8rem 4rem;
  text-align: center;
  color: #666;
  min-height: 600px;
  background-color: #f9f9f9;
  border-radius: 12px;
  margin: 2rem 0;
  box-shadow: 0 2px 12px rgba(0,0,0,0.05);
  transition: opacity 0.3s ease;
}

.empty-icon {
  font-size: 5rem;
  margin-bottom: 3rem;
  opacity: 0.7;
  animation: pulse 2s infinite;
  color: #42b983;
}

.empty-title {
  margin-bottom: 2.5rem;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  line-height: 1.8;
}

.letter {
  font-size: 2.8rem;
  font-weight: 300;
  margin: 0 0.4rem;
  display: inline-block;
  animation: bounce 0.6s ease infinite alternate;
  transform: translateY(0);
  color: #333;
  text-shadow: 0 2px 4px rgba(0,0,0,0.1);
  min-width: 1.5rem;
}

@keyframes bounce {
  to {
    transform: translateY(-15px);
    text-shadow: 0 12px 8px rgba(0,0,0,0.1);
  }
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.empty-subtitle {
  font-size: 1.3rem;
  color: #888;
  margin-bottom: 3rem;
  letter-spacing: 1px;
  line-height: 1.8;
  max-width: 500px;
  font-weight: 300;
}

.empty-action-btn {
  background: linear-gradient(135deg, #42b983, #2b7a78);
  color: white;
  border: none;
  padding: 14px 36px;
  font-size: 1.1rem;
  border-radius: 50px;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(66, 185, 131, 0.3);
  transition: all 0.3s ease;
  letter-spacing: 1px;
  font-weight: 500;
  text-transform: uppercase;
}

.empty-action-btn:hover {
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 8px 25px rgba(66, 185, 131, 0.4);
}

/* 响应式调整 */
@media (max-width: 768px) {
  .empty-report {
    padding: 4rem 1rem;
    min-height: 400px;
  }
  
  .empty-icon {
    font-size: 4rem;
    margin-bottom: 2rem;
  }
  
  .letter {
    font-size: 2rem;
    margin: 0 0.3rem;
  }
  
  .empty-subtitle {
    font-size: 1.1rem;
    margin-bottom: 2rem;
  }
  
  .empty-action-btn {
    padding: 12px 28px;
    font-size: 1rem;
  }
}
.star-rating {
  font-size: 1.5rem;
  letter-spacing: 2px;
  margin: 8px 0;
}

.star {
  color: #ddd; /* 默认灰色 */
  transition: all 0.2s;
}

.star.filled {
  color: #ffc107; /* 亮起的星星使用金色 */
  text-shadow: 0 0 2px rgba(255, 193, 7, 0.5);
}
.score-criteria {
  height: 350px; /* 与雷达图高度一致 */
  overflow-y: auto; /* 如果内容过多，允许垂直滚动 */
  line-height: 2.5; /* 调整行间距 */
  padding: 20px; /* 增加内边距 */
 
  border-radius: 10px; /* 添加圆角 */
  white-space: pre-line; /* 允许换行，但保留空白符 */
  font-size: 1.2rem; /* 增加字体大小 */
  color: #333; /* 设置字体颜色 */
  text-align: left; /* 设置文本对齐方式为左对齐 */
   margin-top: 20px; 
}
.score-criteria-title {
  font-weight: bold; /* 设置为粗体 */
  color: #ff0000; /* 设置为红色 */
  /* 可以添加更多样式，如字体大小、边距等 */
}
.score-criteria p {
  margin: 0; /* 移除段落默认的外边距 */
  padding: 0; /* 移除段落默认的内边距 */
}

.score-criteria strong {
  color: #42b983; /* 设置评分项标题颜色 */
}
 .chart-title {
  margin-top: -20px; /* 向上移动20像素 */
}

.chart-title{
  font-weight: bold;
  color: #42b983;
  margin-top: -10px;
  font-size: 1.08rem;
  text-align: center;
}
/* 新增的外框样式 */
.report-container {
    position: relative;
  border: 0.5px solid #42b983;
  border-radius: 12px;
  padding: 2.5rem;
  box-shadow: 0 4px 20px rgba(66, 185, 131, 0.15);
  background: white;
  margin: 0; /* 移除外边距 */
  width: 100%;
  box-sizing: border-box;
  animation: fadeIn 0.5s ease;
}
.report-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0; /* 移除内边距 */
  position: relative;
  min-height: 600px;
}
.empty-report-container {
  position: relative;
  z-index: 1;
}
.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding-bottom: 2px;
  border-bottom: 1px solid #eee;
}
.report-header h1 {
  font-size: 2.2rem;
  color: #2b7a78;
  font-weight: 500;
  letter-spacing: 1px;
  position: relative;
  display: inline-block;
  padding: 0 25px 10px;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.charts-row {
  display: flex;
  gap: 40px;
  align-items: flex-start;
  margin-bottom: 2.5rem;
  flex-wrap: nowrap;
  max-width: 100%;
  overflow-x: auto;
}

.chart-section {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(66,185,131,0.08);
  padding: 18px 12px 12px 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 0;
  max-width: none;
  flex: 1 1 auto;
  position: relative;
  z-index: 1;
}

/* 只给雷达图固定宽度和不拉伸 */
.radar-section {
  width: 420px !important;
  min-width: 420px !important;
  max-width: 420px !important;
  flex: 0 0 420px !important;
  flex-shrink: 0 !important;
  flex-grow: 0 !important;
  box-sizing: border-box;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(66,185,131,0.08);
  padding: 18px 12px 12px 12px;
  display: block;
  position: relative;
  z-index: 2;
}
.radar-canvas-wrap,
.wave-canvas-wrap {
  width: 400px;
  height: 400px;
  display: block;
  margin: 0 auto;
}
.radar-canvas-wrap canvas,
.wave-canvas-wrap canvas {
  width: 400px !important;
  height: 400px !important;
  display: block;
}
.wave-section {
  min-width: 0 !important;
  max-width: none !important;
  flex: 1 1 auto !important;
}
.chart-title {
  text-align: center;
  font-size: 1.08rem;
  color: #42b983;
  margin-top: 10px;
  font-weight: bold;
}

.score-section {
  display: flex;
  flex-wrap: wrap;
  gap: 20px 16px; /* 行间距20px，列间距16px */
  justify-content: flex-start;
  margin-bottom: 1rem;
}

/* 修改.score-item的样式 */
.score-item {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(66,185,131,0.08);
  padding: 12px 15px;
  width: calc(33.333% - 11px); /* 计算宽度，考虑间距 */
  min-width: 280px; /* 设置最小宽度 */
  max-width: 320px; /* 设置最大宽度 */
  display: flex;
  flex-direction: column;
  gap: 12px;
  box-sizing: border-box;
  margin-bottom: 0;
}
/* 响应式调整 - 在小屏幕上改为两列 */
@media (max-width: 1024px) {
  .score-item {
    width: calc(50% - 8px); /* 两列布局 */
  }
}

/* 在更小的屏幕上改为单列 */
@media (max-width: 768px) {
  .score-item {
    width: 100%; /* 单列布局 */
    max-width: 100%;
  }
}
.score-title {
  font-weight: bold;
  font-size: 1.1rem;
  margin-bottom: 6px;
}

.score-bar {
  background: #eee;
  border-radius: 6px;
  height: 12px;
  margin: 6px 0 10px 0;
  width: 100%;
}

.score-bar-inner {
  background: #42b983;
  height: 100%;
  border-radius: 6px;
  transition: width 0.5s;
}

.score-evidence {
  color: #888;
  font-size: 0.97rem;
  margin-top: 4px;
}

.insight-section {
  margin-bottom: 2.5rem;
}

.insight-item {
  background: #f8fafc;
  border-radius: 8px;
  padding: 18px 20px;
  margin-bottom: 18px;
  box-shadow: 0 1px 4px rgba(66,185,131,0.06);
  line-height: 1.8;
  font-size: 1.08rem;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.insight-issue {
  color: #e67e22;
  font-weight: 500;
  word-break: break-all;
}

.insight-suggestion {
  color: #42b983;
  margin-left: 0;
  font-weight: 500;
  word-break: break-all;
}

.summary-section {
  background: #f8fafc;
  border-radius: 10px;
  padding: 1.5rem 2rem;
  margin-top: 2.5rem;
  font-size: 1.08rem;
  box-shadow: 0 1px 4px rgba(66,185,131,0.06);
  line-height: 1.8; /* 新增或调整 */
  word-break: break-all; /* 防止长词溢出 */
}

.summary-section > div {
  margin-bottom: 12px;
}

/* 样式部分 */
.chart-scrollable {
  overflow-x: auto;
  width: 100%;
}

@media (max-width: 900px) {
  .charts-row {
    flex-direction: column;
    gap: 20px;
  }
  .chart-section {
    max-width: 100%;
    min-width: 0;
  }
  .score-section {
    flex-direction: column;
    gap: 20px 0;
  }
  .score-item {
    min-width: 0;
    max-width: 100%;
  }
}

/* 添加加载样式 */
.loading-overlay {
   position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  border-radius: 12px;
  margin: 2rem 0;
}
.loading-content {
  background: white;
  padding: 2.5rem 3rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(66, 185, 131, 0.15);
  text-align: center;
  border: 2px solid #42b983;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 300px;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #42b983;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.report-section {
  margin-bottom: 2rem;
  line-height: 1.8;
  word-break: break-all;
  white-space: pre-line;
}

.report-section h3 {
  color: #2b7a78;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #eee;
}

.score-section {
  margin-top: 1.5rem;
}

.score-item {
  margin-bottom: 1.2rem;
}

.score-title {
  font-weight: bold;
  color: #2b7a78;
}

.score-bar {
  width: 100%;
  height: 10px;
  background: #eee;
  border-radius: 5px;
  margin: 0.5rem 0;
  overflow: hidden;
}

.score-bar-inner {
  height: 100%;
  background: #42b983;
  border-radius: 5px;
  transition: width 0.5s ease;
}

.score-evidence {
  color: #888;
  font-size: 0.95rem;
  margin-bottom: 0.5rem;
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


.checkin-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.checkin-dialog {
  background: white;
  border-radius: 12px;
  width: 400px;
  max-width: 90%;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

.checkin-header {
  padding: 16px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  h3 {
    margin: 0;
    font-size: 18px;
    color: #333;
  }
  
  .close-btn {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: #999;
    padding: 0 8px;
    
    &:hover {
      color: #666;
    }
  }
}

.checkin-body {
  padding: 16px;
  overflow-y: auto;
  flex: 1;
}

.checkin-section {
  margin-bottom: 20px;
  
  .section-label {
    display: block;
    margin-bottom: 8px;
    font-size: 14px;
    color: #666;
  }
}

.checkin-types {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.checkin-type {
  flex: 1;
  min-width: calc(50% - 8px);
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
  
  &:hover {
    border-color: #32ca99;
  }
  
  &.active {
    background-color: #e8f5e9;
    border-color: #32ca99;
    color: #2E8B57;
  }
  
  .type-icon {
    display: block;
    font-size: 20px;
    margin-bottom: 4px;
  }
  
  .type-name {
    font-size: 12px;
  }
}

.checkin-textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-height: 80px;
  resize: vertical;
  font-size: 14px;
  
  &:focus {
    border-color: #32ca99;
    outline: none;
  }
}

.mood-options {
  display: flex;
  gap: 8px;
}

.mood-option {
  flex: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
  
  &:hover {
    border-color: #32ca99;
  }
  
  &.active {
    background-color: #e8f5e9;
    border-color: #32ca99;
    color: #2E8B57;
  }
  
  .mood-icon {
    display: block;
    font-size: 20px;
    margin-bottom: 4px;
  }
  
  .mood-name {
    font-size: 12px;
  }
}

.additional-info {
  margin-top: 16px;
}

.info-item {
  margin-bottom: 12px;
  
  .info-label {
    display: flex;
    align-items: center;
    font-size: 14px;
    color: #666;
    margin-bottom: 6px;
    
    i {
      margin-right: 6px;
      font-size: 16px;
    }
  }
  
  .info-input {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
    
    &:read-only {
      background-color: #f5f5f5;
    }
  }
}

.image-upload {
  margin-top: 16px;
  
  .upload-label {
    display: block;
    margin-bottom: 8px;
    font-size: 14px;
    color: #666;
  }
  
  .upload-btn {
    display: block;
    width: 100%;
    padding: 8px;
    border: 1px dashed #ddd;
    border-radius: 4px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
    
    &:hover {
      border-color: #32ca99;
      color: #2E8B57;
    }
  }
  
  .image-preview {
    margin-top: 8px;
    
    img {
      max-width: 100%;
      max-height: 150px;
      border-radius: 4px;
      display: block;
    }
  }
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  padding: 16px;
  border-top: 1px solid #eee;
  gap: 12px;
  
  button {
    padding: 8px 16px;
    border-radius: 4px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s;
  }
  
  .cancel-btn {
    background: none;
    border: none;
    color: #666;
    
    &:hover {
      color: #333;
    }
  }
  
  .confirm-btn {
    background-color: #32ca99;
    color: white;
    border: none;
    
    &:hover {
      background-color: #35a066;
    }
  }
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