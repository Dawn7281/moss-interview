<template>
  <section class="learning-path">
    <h2>学习资源</h2>
    <div class="path-container">
      <div 
        v-for="path in learningPaths" 
        :key="path.id"
        class="path-card"
        @click="selectPath(path.id)"
      >
        <h3>{{ path.title }}</h3>
        <p>{{ path.description }}</p>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'LearningPath',
  data() {
    return {
      learningPaths: [
        {
          id: 1,
          title: '行业面试视频',
          description: '精选岗位面试真实视频'
        },
        {
          id: 2,
          title: '表达训练视频',
          description: '提升沟通与表达能力的专业课程'
        },
        {
          id: 3,
          title: '岗位技能课程',
          description: '针对目标岗位的技术提升路径'
        }
      ]
    }
  },
  methods: {
    selectPath(pathId) {
      this.$emit('path-selected', pathId)
    }
  }
}
</script>

<style scoped>
.learning-path {
  display: inline-block;
  width: calc(100% + 45px);
  margin-left: -45px;
  margin-top: 15px;
  box-sizing: border-box;
}

h2 {
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
  color: #333;
}

.path-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.path-card {
  padding: 1rem;
  transition: all 0.3s ease;
  cursor: pointer;
  border-left: 3px solid #32ca99;
}

.path-card:hover {
  background: #f8f9fa;
  transform: translateY(-2px);
}

.path-card h3 {
  color: #32ca99;
  margin-top: 0;
  font-size: 1.1rem;
}

.path-card p {
  color: #555;
  font-size: 0.9rem;
  margin-bottom: 0;
}

@media (max-width: 992px) {
  .learning-path {
    width: 100%;
    margin-left: 0;
  }
  
  .path-container {
    grid-template-columns: 1fr;
    padding: 1rem;
  }
}
</style>