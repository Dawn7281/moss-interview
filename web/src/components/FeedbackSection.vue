<template>
  <section class="feedback-section">
    <h2>智能评测反馈</h2>
    <div class="feedback-container">
      <div class="radar-chart-container">
        <canvas ref="radarChart"></canvas>
      </div>
      <div class="suggestions">
        <h3>改进建议</h3>
        <ul class="suggestion-list">
          <li v-for="(suggestion, index) in evaluationData.suggestions" :key="index">
            {{ suggestion }}
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>

<script>
import Chart from 'chart.js/auto'

export default {
  name: 'FeedbackSection',
  data() {
    return {
      evaluationData: {
        indicators: [
          {name: '专业知识', score: 85},
          {name: '技能匹配', score: 78},
          {name: '表达能力', score: 90},
          {name: '逻辑思维', score: 82},
          {name: '创新能力', score: 75}
        ],
        suggestions: [
          "建议使用STAR结构回答问题",
          "注意保持适当的眼神交流",
          "技术细节描述可以更具体"
        ]
      },
      chart: null
    }
  },
  mounted() {
    this.renderChart()
  },
  methods: {
    renderChart() {
      const ctx = this.$refs.radarChart.getContext('2d')
      this.chart = new Chart(ctx, {
        type: 'radar',
        data: {
          labels: this.evaluationData.indicators.map(item => item.name),
          datasets: [{
            label: '能力评估',
            data: this.evaluationData.indicators.map(item => item.score),
            backgroundColor: 'rgba(52, 152, 219, 0.2)',
            borderColor: 'rgba(52, 152, 219, 1)',
            borderWidth: 2,
            pointBackgroundColor: 'rgba(52, 152, 219, 1)',
            pointRadius: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            r: {
              angleLines: {
                display: true
              },
              suggestedMin: 0,
              suggestedMax: 100,
              ticks: {
                stepSize: 20
              }
            }
          }
        }
      })
    }
  },
  beforeUnmount() {
    if (this.chart) {
      this.chart.destroy()
    }
  }
}
</script>

<style scoped>
.feedback-section {
  display: inline-block;
  width: 100%;
  vertical-align: top;
  margin-left: -45px;
  margin-top: 15px; /* 保持与多模态组件的间距 */
}

.feedback-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%; /* 新增：确保宽度一致 */
}

.radar-chart-container {
  min-height: 350px; /* 调整图表高度 */
  width: 100%;
}

.suggestions h3 {
  color: #32ca99;
  margin-top: 0;
  font-size: 1.1rem;
}

.suggestion-list {
  padding-left: 1.5rem;
  list-style: none;
}

.suggestion-list li {
  margin-bottom: 0.8rem;
  padding-left: 1.2rem;
  position: relative;
  font-size: 1rem;
  line-height: 1.4;
}

.suggestion-list li:before {
  content: "•";
  color: #f39c12;
  position: absolute;
  left: 0;
  font-size: 1.2rem;
}

@media (max-width: 992px) {
  .feedback-section {
    width: 100%;
    margin: 10px 0 0 0;
    display: block;
  }
  
  .feedback-container {
    grid-template-columns: 1fr;
    padding: 1rem;
  }
  
  .radar-chart-container {
    min-height: 300px;
  }
}
</style>