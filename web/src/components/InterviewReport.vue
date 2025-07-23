<template>
  <div class="report-container">
    <div class="report-wrapper">
      <div class="report-header">
        <h2>面试评估报告</h2>
      </div>
      
      <!-- 空状态提示 -->
      <div v-if="!props.reportData" class="empty-report">
        <div class="empty-icon">📊</div>
        <div class="empty-title">暂无报告数据</div>
        <div class="empty-subtitle">请先完成面试流程以生成评估报告</div>
      </div>
      
      <div v-else class="report-content">
        <!-- 雷达图与评分标准并排展示 -->
        <div class="charts-row">
          <!-- 雷达图 -->
          <div class="radar-section">
            <div class="radar-canvas-wrap">
              <canvas ref="radarChart" width="400" height="400"></canvas>
            </div>
            <div class="chart-title">能力雷达图</div>
          </div>
          
          <!-- 评分标准说明 -->
          <div class="chart-section">
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
        
        <!-- 专业能力评分 -->
        <div class="report-section">
          <h3>专业能力评分</h3>
          <div class="score-section">
            <div v-for="(item, key) in props.reportData.ability_scores" :key="key" class="score-item">
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
        
        <!-- 问题洞察与建议 -->
        <div class="report-section" v-if="props.reportData.problem_insights">
          <h3>问题洞察与建议</h3>
          <div v-for="insight in props.reportData.problem_insights" :key="insight.dimension" class="insight-item">
            <div>
              <strong>{{ insight.dimension }}</strong>：
              <span class="insight-issue">{{ insight.issue }}</span>
            </div>
            <div class="insight-suggestion">建议：{{ insight.suggestion }}</div>
          </div>
        </div>
        
        <!-- 综合建议 -->
        <div class="report-section" v-if="props.reportData.overall_recommendation">
          <h3>综合建议</h3>
          <div class="summary-section">
            <div><strong>结论：</strong>{{ props.reportData.overall_recommendation.decision }}</div>
            <div><strong>理由：</strong>{{ props.reportData.overall_recommendation.reasoning }}</div>
            <div><strong>建议：</strong>{{ props.reportData.overall_recommendation.closing_remark }}</div>
          </div>
        </div>

        <!-- 新增：面试对话记录与分析 -->
        <div class="report-section" v-if="props.reportData.dialogue_records && props.reportData.dialogue_records.length > 0">
          <h3>面试对话记录与分析</h3>
          <div class="dialogue-list">
            <div 
              v-for="(item, idx) in props.reportData.dialogue_records"
              :key="idx" 
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
  </div>
</template>


<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import Chart from 'chart.js/auto'
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const pushFeedback =(feedback) => {
  router.push({
    path: '/graph',
    query: {
      feedback: feedback,
    }
  });
}

const props = defineProps({
  reportData: {
    type: Object,
    required: true
  }
})

const radarChart = ref(null)
let radarChartInstance = null

function renderRadarChart() {
  if (!radarChart.value || !props.reportData.radar_data) return
  if (radarChartInstance) radarChartInstance.destroy()
  
  const ctx = radarChart.value.getContext('2d')
  radarChartInstance = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: Object.keys(props.reportData.radar_data),
      datasets: [{
        label: '能力评估',
        data: Object.values(props.reportData.radar_data),
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
          max: 5,
          ticks: { 
            stepSize: 1,
            callback: function(value) {
              return value + '/5'
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

onMounted(() => {
  nextTick(() => {
    if (props.reportData?.radar_data) {
      renderRadarChart()
    }
  })
});

watch(() => props.reportData, async (newVal) => {
  await nextTick()
  if (newVal && newVal.radar_data) {
    renderRadarChart()
  }
}, { deep: true })
</script>

<style scoped>
/* 对话条目悬停提示样式 */
.dialogue-item {
  position: relative; /* 为提示定位做准备 */
}

.dialogue-tooltip {
  position: absolute;
  top: -12px;
  left: 360px;
  background-color: #171918;
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
/* 新增对话记录部分样式 */
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
  
  .feedback-content {
    font-size: 0.9rem;
  }
}
/* 基础样式 */
.report-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0;
  position: relative;
  min-height: 600px;
}

.report-wrapper {
  position: relative;
  border: 0.5px solid #42b983;
  border-radius: 12px;
  padding: 2.5rem;
  box-shadow: 0 4px 20px rgba(66, 185, 131, 0.15);
  background: white;
  margin: 0;
  width: 100%;
  box-sizing: border-box;
  animation: fadeIn 0.5s ease;
}

/* 头部样式 */
.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding-bottom: 2px;
  border-bottom: 1px solid #eee;
}

.report-header h2 {
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

/* 空状态样式 */
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
  font-size: 2.8rem;
  font-weight: 300;
  margin-bottom: 2.5rem;
  color: #333;
  text-shadow: 0 2px 4px rgba(0,0,0,0.1);
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

/* 图表区域样式 */
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

.radar-canvas-wrap {
  width: 400px;
  height: 400px;
  display: block;
  margin: 0 auto;
}

.radar-canvas-wrap canvas {
  width: 400px !important;
  height: 400px !important;
  display: block;
}

.chart-title {
  text-align: center;
  font-size: 1.08rem;
  color: #42b983;
  margin-top: 10px;
  font-weight: bold;
}

/* 评分标准样式 */
.score-criteria {
  height: 350px;
  overflow-y: auto;
  line-height: 2.5;
  padding: 20px;
  border-radius: 10px;
  white-space: pre-line;
  font-size: 1.2rem;
  color: #333;
  text-align: left;
  margin-top: 20px;
}

/* 能力评分样式 */
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
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: flex-start;
}

.score-item {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(66,185,131,0.08);
  padding: 8px 10px;
  width: 200px;
  min-width: 320px;
  max-width: 320px; 
  max-height: 180px;
  flex: 2 1 330px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 0;
}

.score-title {
  font-weight: bold;
  font-size: 1.1rem;
  margin-bottom: 6px;
}

.star-rating {
  font-size: 1.5rem;
  letter-spacing: 2px;
  margin: 8px 0;
}

.star {
  color: #ddd;
  transition: all 0.2s;
}

.star.filled {
  color: #ffc107;
  text-shadow: 0 0 2px rgba(255, 193, 7, 0.5);
}

.score-evidence {
  color: #888;
  font-size: 0.97rem;
  margin-top: 4px;
}

/* 问题洞察样式 */
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

/* 综合建议样式 */
.summary-section {
  background: #f8fafc;
  border-radius: 10px;
  padding: 1.5rem 2rem;
  margin-top: 1rem;
  font-size: 1.08rem;
  box-shadow: 0 1px 4px rgba(66,185,131,0.06);
  line-height: 1.8;
  word-break: break-all;
}

.summary-section > div {
  margin-bottom: 12px;
}

/* 动画效果 */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

/* 响应式设计 */
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

@media (max-width: 768px) {
  .report-wrapper {
    padding: 1.5rem;
  }
  
  .report-header h2 {
    font-size: 1.8rem;
  }
  
  .empty-report {
    padding: 4rem 1rem;
    min-height: 400px;
  }
  
  .empty-icon {
    font-size: 4rem;
    margin-bottom: 2rem;
  }
  
  .empty-title {
    font-size: 2rem;
  }
  
  .empty-subtitle {
    font-size: 1.1rem;
    margin-bottom: 2rem;
  }
  
  .radar-section {
    width: 100% !important;
    min-width: 100% !important;
    max-width: 100% !important;
    flex: 0 0 100% !important;
  }
  
  .radar-canvas-wrap {
    width: 100%;
    height: auto;
  }
  
  .score-item {
    min-width: 0;
    max-width: 100%;
  }
}
</style>