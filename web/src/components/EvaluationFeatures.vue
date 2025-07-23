<template>
  <section class="evaluation-features">
    <h2>多模态评测维度</h2>
    <ul class="feature-list">
      <li v-for="(feature, index) in features" :key="index">
        {{ feature }}
      </li>
    </ul>
  </section>
</template>

<script>
export default {
  name: 'EvaluationFeatures',
  data() {
    return {
      features: [
        '语音分析：语言逻辑与情感语调',
        '视频分析：微表情与肢体语言',
        '文本分析：应答内容与简历匹配'
      ]
    }
  }
}
</script>

<style scoped>
.evaluation-features {
  display: inline-block;
  width: 100%;
  vertical-align: top;
  margin-left: -45px;
  margin-top: -18px;
}

.feature-list {
  width: 100%;
  background: white;
  padding: 1.5rem;
  margin-top: 0.9rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h2 {
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
  color: #333;
}

.feature-list li {
  margin-bottom: 0.5rem;
  padding-left: 1.9rem;
  position: relative;
  font-size: 1rem;
  line-height: 1.4;
}

.feature-list li:before {
  content: "✓";
  color: #2ecc71;
  position: absolute;
  left: 0;
}

@media (max-width: 992px) {
  .evaluation-features {
    width: 100%;
    margin: 6px 0 0 0;
    display: block;
  }
  
  .feature-list {
    padding: 0.8rem;
  }
}
</style>