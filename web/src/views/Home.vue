<template>
  <div class="home">
    <FeatureCarousel :features="features" @feature-click="handleFeatureClick" />
    
    <!-- 仅添加外层布局容器，不修改内部组件样式 -->
    <div class="modules-container">
      <InterviewModules />
      <InterviewTopList />
    </div>

    <EvaluationFeatures />
    <FeedbackSection />
    <LearningPath @path-selected="handlePathSelect" />
  </div>
</template>

<script>
import InterviewModules from '@/components/InterviewModules.vue'
import EvaluationFeatures from '@/components/EvaluationFeatures.vue'
import FeedbackSection from '@/components/FeedbackSection.vue'
import LearningPath from '@/components/LearningPath.vue'
import FeatureCarousel from '@/components/FeatureCarousel.vue'
import InterviewTopList from '@/components/InterviewTopList.vue'

export default {
  name: 'Home',
  components: {
    InterviewModules,
    EvaluationFeatures,
    FeedbackSection,
    LearningPath,
    FeatureCarousel,
    InterviewTopList
  },
  data() {
    return {
      features: [
        {
          id: 'mock',
          title: 'AI模拟面试',
          icon: 'interview'
        },
        {
          id: 'resume',
          title: '智能简历优化',
          icon: 'resume'
        },
        {
          id: 'qa',
          title: '面试题库',
          icon: 'qa'
        },
        {
          id: 'history',
          title: '成长轨迹',
          icon: 'history'
        }
      ]
    }
  },
  computed: {
    isAuthenticated() {
      return this.$store.state.isAuthenticated
    }
  },
  methods: {
    handleModuleSelect(moduleId) {
      this.$router.push(`/interview/${moduleId}`)
    },
    handlePathSelect(pathId) {
      this.$router.push(`/learning-path/${pathId}`)
    },
    handleFeatureClick(featureId) {
      this.$router.push(`/${featureId === 'mock' ? 'mock-interview' : featureId}`)
    }
  }
}
</script>


<style>
/* 仅添加最基础的布局样式 */
.modules-container {
  display: flex;
  justify-content: space-between;
  max-width: 1200px;
  margin: 30px auto;
  gap: 20px;
}

/* 响应式调整 */
@media (max-width: 992px) {
  .modules-container {
    flex-direction: column;
    gap: 30px;
  }
}

/* 基础布局样式 */
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* 修改后的导航栏样式 */
.header {
  background: #ffffff; /* 改为白色背景 */
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* 添加阴影 */
  padding: 0.8rem 1rem;
}

/* 修改后的导航链接样式 */
.nav-link {
  color: #333333 !important; /* 深灰色字体 */
  font-size: 1.1rem;
  text-decoration: none;
  padding: 0.5rem 1rem;
  transition: all 0.3s ease;
  position: relative;
}

.nav-link:hover {
  color: #3dcd9f !important; /* 悬停时变为绿色 */
  background: transparent !important; /* 移除原hover背景色 */
}

/* 修改后的选中状态样式 */
.nav-link.active {
  color: #3dcd9f !important; /* 选中时绿色 */
  font-weight: 500;
  background: transparent !important;
}

.nav-link.active::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 70%;
  height: 3px;
  background: #3dcd9f; /* 绿色下划线 */
  border-radius: 3px;
}

/* 修改后的登录注册按钮样式 */
.auth-button {
  padding: 0.5rem 1.5rem;
  background-color: transparent !important;
  color: #333333 !important;
  border: 1px solid #e0e0e0 !important;
  border-radius: 20px;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.auth-button:hover {
  background-color: #f5f5f5 !important;
  color: #3dcd9f !important;
  border-color: #3dcd9f !important;
}

.auth-button:last-child {
  background-color: #3dcd9f !important;
  color: white !important;
  border-color: #3dcd9f !important;
}

.auth-button:last-child:hover {
  background-color: #34b38a !important;
  border-color: #34b38a !important;
}

/* 修改后的logo样式 */
.moss-logo {
  color: #333333 !important;
  text-shadow: none !important;
  font-size: 2.3rem; /* 修正原23rem的错误 */
  font-weight: 800; /* 修正原1800的错误 */
}

/* 修改后的欢迎消息样式 */
.welcome-message {
  color: #333333 !important;
}

/* 保留原有的布局结构 */
.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
}

.title-nav-container {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-left: -40px;
}

.main-nav {
  display: flex;
  gap: 1.5rem;
}

.auth-buttons {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.auth-buttons > div {
  margin-top: 15px;
}

.container {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.footer {
  background: #333;
  color: white;
  text-align: center;
  padding: 1rem;
}

/* 保留原有的其他样式 */
.header-content {
  position: relative;
}

.title {
  position: relative;
  margin-bottom: 1.5rem;
}

.main-nav {
  z-index: 2;
}

.nav-link {
  transition: background 0.2s;
}

.nav-link.active {
  position: relative;
}

.auth-button {
  transition: all 0.3s ease;
}

.auth-button:hover {
  transition: all 0.3s ease;
}

.auth-button:last-child:hover {
  transition: all 0.3s ease;
}

.container {
  width: 100%;
}

.auth-button.user-center-btn {
  margin-left: 0;
}

.auth-buttons > div:first-child > .auth-button:not(:last-child) {
  margin-right: 2rem;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
  }
  
  .title-nav-container {
    margin-left: 0;
    width: 100%;
    justify-content: space-between;
  }
  
  .main-nav {
    gap: 0.8rem;
  }
  
  .nav-link {
    font-size: 1rem;
    padding: 0.3rem 0.8rem;
  }
}
</style>