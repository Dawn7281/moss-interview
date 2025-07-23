<template>
  <div class="feedback-container">
    <div class="feedback-header">
      <h2>面试情绪反馈分析</h2>
      <button class="back-btn" @click="$router.go(-1)">返回</button>
    </div>
    
    <div class="feedback-content">
      <div class="feedback-chart">
        <!-- 这里放置情绪分析图表 -->
        <div class="chart-placeholder">
          <h3>情绪变化趋势图</h3>
          <!-- 实际项目中这里应该是一个图表组件 -->
          <div class="chart-simulator">
            <div class="chart-line" v-for="(emotion, name) in emotionData" :key="name">
              <div class="emotion-name">{{ name }}</div>
              <div class="emotion-bar" :style="{ width: `${emotion * 100}%` }"></div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="feedback-details">
        <div class="detail-card" v-for="(emotion, name) in emotionData" :key="name">
          <h3>{{ getEmotionName(name) }}</h3>
          <div class="progress-container">
            <div class="progress-bar" :style="{ width: `${emotion * 100}%` }"></div>
          </div>
          <p class="score">{{ Math.round(emotion * 100) }}分</p>
          <p class="analysis">{{ getEmotionAnalysis(name) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      emotionData: {
        attentiveness: 0.85,
        confidence: 0.72,
        confusion: 0.15,
        frustration: 0.08,
        nervousness: 0.25
      }
    }
  },
  methods: {
    getEmotionName(name) {
      const names = {
        attentiveness: '专注度',
        confidence: '自信心',
        confusion: '困惑度',
        frustration: '挫败感',
        nervousness: '紧张度'
      }
      return names[name] || name
    },
    getEmotionAnalysis(name) {
      const analyses = {
        attentiveness: '您在面试过程中保持了较高的专注度，能够很好地集中注意力。',
        confidence: '表现出较好的自信心，但仍有提升空间。',
        confusion: '偶尔表现出困惑，建议提前准备常见问题。',
        frustration: '挫败感较低，说明您能很好地处理压力。',
        nervousness: '有一定紧张感，但属于正常范围。'
      }
      return analyses[name] || '暂无详细分析'
    }
  }
}
</script>

<style scoped>
.feedback-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.feedback-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.feedback-content {
  display: flex;
  gap: 2rem;
}

.feedback-chart {
  flex: 2;
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}

.feedback-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.detail-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.progress-container {
  height: 10px;
  background: #f0f0f0;
  border-radius: 5px;
  margin: 1rem 0;
}

.progress-bar {
  height: 100%;
  background: #42b983;
  border-radius: 5px;
  transition: width 0.5s ease;
}

.score {
  font-weight: bold;
  color: #42b983;
  margin-bottom: 0.5rem;
}

.analysis {
  color: #666;
  line-height: 1.6;
}

.chart-placeholder {
  height: 300px;
  display: flex;
  flex-direction: column;
}

.chart-simulator {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  padding: 1rem 0;
}

.chart-line {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}

.emotion-name {
  width: 100px;
  font-size: 0.9rem;
}

.emotion-bar {
  height: 10px;
  background: #42b983;
  border-radius: 5px;
  transition: width 0.5s ease;
}

.back-btn {
  background: none;
  border: none;
  color: #42b983;
  font-size: 1rem;
  cursor: pointer;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  border: 1px solid #42b983;
}

@media (max-width: 768px) {
  .feedback-content {
    flex-direction: column;
  }
}
</style>