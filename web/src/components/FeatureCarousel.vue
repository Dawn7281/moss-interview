<template>
  <div class="feature-container">
    <div class="modern-feature-showcase">
      <div class="showcase-container">
        <!-- 左侧菜单栏 -->
        <div class="feature-menu">
          <div 
            v-for="(feature, index) in features" 
            :key="feature.id"
            class="menu-item"
            :class="{ active: activeIndex === index }"
            @click="changeFeature(index)"
            @mouseenter="pauseAutoPlay"
            @mouseleave="resumeAutoPlay"
          >
            <div class="menu-content">
              <h4>{{ feature.title }}</h4>
              <p>{{ feature.shortDesc }}</p>
            </div>
            <div class="menu-indicator"></div>
          </div>
        </div>
        
        <!-- 右侧功能展示区 -->
        <div class="feature-display">
          <transition name="fade-slide" mode="out-in">
            <div class="display-content" :key="currentFeature.id">
              <div class="display-header">
                <h3>{{ currentFeature.title }}</h3>
                <p class="subtitle">{{ currentFeature.description }}</p>
              </div>
              
              <div class="feature-image-container">
    <div class="image-wrapper">
      <img 
        :src="getFeatureImage(currentFeature.id)" 
        :alt="currentFeature.title"
        class="feature-image"
        ref="featureImage"
        @load="handleImageLoad"
        @click="handleImageClick(currentFeature.id)"  
      >
    </div>
  </div>
              
              <div class="feature-highlights">
                <div 
                  v-for="(item, i) in currentFeature.details" 
                  :key="i" 
                  class="highlight-item"
                >
                  <div class="highlight-icon">
                    <i class="check">✓</i>
                  </div>
                  <div class="highlight-text">{{ item }}</div>
                </div>
              </div>
              
              <div class="action-button-container">
                <button 
                  class="modern-action-button"
                  @click="navigateToFeature(currentFeature.id)"
                >
                </button>
              </div>
            </div>
          </transition>
        </div>
      </div>
    </div>

    <!-- 工具箱区域 -->
    <div class="toolbox-container">
      <div class="toolbox-header">
        <h3 class="toolbox-title">工具箱</h3>
        <div class="toolbox-divider"></div>
      </div>
      <div class="toolbox-grid">
        <div 
          class="toolbox-card" 
          v-for="(tool, index) in tools" 
          :key="index"
          @click="handleToolClick(tool)"
        >
          <div class="toolbox-icon-frame">
            <div class="toolbox-icon">
              <i :class="'icon-' + tool.icon"></i>
            </div>
          </div>
          <span class="toolbox-text">{{ tool.name }}</span>
          <div class="toolbox-hover-effect"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ModernFeatureCarousel',
  props: {
    features: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      activeIndex: 0,
      autoPlayInterval: null,
      isAutoPlaying: true,
      featureImages: {
        'qa': '/images/qa.jpg',
        'mock': '/images/ai_interview.jpg',
        'history': '/images/report.jpg',
        'resume': '/images/resume.jpg'
      },
       tools: [
        { icon: 'search', name: '岗位查找', action: 'job-search' },
        { icon: 'history', name: '历史记录', action: 'history' },
        { icon: 'account_circle', name: '个人中心', action: 'profile' },
        { icon: 'help', name: '帮助文档', action: 'help', docFile: 'MOSS-Help-Document.docx' } // 添加docFile属性
      ],
      imageAspectRatio: 16/9
    }
  },
  computed: {
    currentFeature() {
      return this.features[this.activeIndex]
    }
  },
  methods: {
    getFeatureImage(featureId) {
      return this.featureImages[featureId] || ''
    },
    changeFeature(index) {
      this.activeIndex = index
    },
    startAutoPlay() {
      this.autoPlayInterval = setInterval(() => {
        if (this.isAutoPlaying) {
          this.activeIndex = (this.activeIndex + 1) % this.features.length
        }
      }, 5000)
    },
    pauseAutoPlay() {
      this.isAutoPlaying = false
    },
    resumeAutoPlay() {
      this.isAutoPlaying = true
    },
    handleImageClick(featureId) {
      const routeMap = {
        'mock': '/mock-interview',  
        'resume': '/resume', 
        'qa': '/qa',    
        'history': '/interview-history' 
      };
      
      if (routeMap[featureId]) {
        this.$router.push(routeMap[featureId]);
      }
    },
    navigateToFeature(featureId) {
      const routeMap = {
        'mock': '/mock-interview',
        'resume': '/resume',
        'qa': '/qa',
        'history': '/interview-history'
      }
      this.$router.push(routeMap[featureId] || '/')
    },
      handleToolClick(tool) {
      console.log('Tool clicked:', tool.action);
      if (tool.action === 'profile') {
        this.$router.push('/user-center');
      } else if (tool.action === 'history') {
        this.$router.push('/interview-history').catch(err => {
          console.error('路由跳转失败:', err);
        });
      } else if (tool.action === 'job-search') {
        this.$router.push('/jobs').catch(err => {
          console.error('路由跳转失败:', err);
        });
      } else if (tool.action === 'help') {
        this.downloadHelpDocument(tool.docFile);
      } else {
        this.$emit('tool-click', tool.action);
      }
    },
     // 新增下载帮助文档方法
   downloadHelpDocument(filename) {
  if (!filename) {
    console.error('帮助文档文件名未配置');
    return;
  }
  
  // 使用浏览器原生确认对话框
  const userConfirmed = confirm('是否要下载MOSS多模态智能模拟面试评测系统帮助文档？');
  if (!userConfirmed) {
    return; // 用户取消下载
  }
  
  try {
    // 创建隐藏的a标签用于下载
    const link = document.createElement('a');
    link.href = `/${filename}`; // 指向public目录下的文件
    link.download = filename;
    
    // 临时添加到DOM并触发点击
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    // 下载完成后提示用户
    setTimeout(() => {
      alert('帮助文档下载已开始，请检查浏览器的下载目录。');
    }, 500);
  } catch (error) {
    console.error('下载帮助文档时出错:', error);
    alert('下载失败，请稍后重试或联系管理员。');
  }
}
  
   
  },
  mounted() {
    this.startAutoPlay()
  },
  beforeUnmount() {
    clearInterval(this.autoPlayInterval)
  }
}
</script>

<style scoped>
.feature-container {
  display: flex;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto 0 0; /* 修改这里：取消 auto 水平居中，改为左对齐 */
  gap: 70px;
  padding: 0 15px;
  transform: translateX(-13px); /* 可选：如果还不够，用这个微调 */
   background-color: #F9FAFB;
}

.modern-feature-showcase {
  width: fit-content !important;  /* 新增：使宽度贴合内容 */
  flex: 1;
  background: #F9FAFB;
  border-radius: 11px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  
  margin-left: -50px; /* 新增：保持居中 */
  margin-right: -50px; /* 新增：保持居中 */
  display: inline-block !important;  /* 新增 */
  overflow: hidden !important;       /* 新增 */
  padding: 0 !important;     
  
}

/* 统一容器尺寸 */
.showcase-container {
  display: flex;
  min-height: 350px;
  border-radius: 11px; /* 新增圆角 */
  overflow: hidden; /* 确保内部元素也显示圆角 */
}

/* 功能菜单区域 */
.feature-menu {
  width: 200px;
  background: #ffffff;
  border-radius: 11px 0 0 11px; /* 左上和左下圆角 */
}

/* 1. 修改展示容器高度计算 */
.feature-display {
  flex: 1;
  padding: 0;
  position: relative;
  min-height: 200px;
  background: transparent;
  display: flex;
  flex-direction: column;
  overflow: hidden; /* 新增 */
}



/* 工具箱区域 */
.toolbox {
  border-radius: 11px; /* 如果也需要圆角 */
}
.feature-menu {
  width: 200px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-right: 1px solid #e2e8f0;
  padding: 1rem 0;
}

.menu-item {
  padding: 1.25rem 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  border-left: 4px solid transparent;
}

.menu-content {
  margin-left: 0;
}

.menu-item:hover {
  background: rgba(255, 255, 255, 0.6);
}

.menu-item.active {
  border-left: 4px solid;
  border-image: #e9fef4;
  box-shadow: 0 4px 12px rgba(0, 198, 255, 0.2);
}

.menu-content h4 {
  font-size: 1.1rem;
  color: #334155;
  margin-bottom: 0.25rem;
  font-weight: 600;
}

.menu-content p {
  font-size: 0.85rem;
  color: #64748b;
  line-height: 1.4;
  margin: 0;
}

.menu-indicator {
  position: absolute;
  right: 1rem;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #cbd5e1;
  transition: all 0.3s;
}

.menu-item.active .menu-indicator {
  background: #e9fef4;
  transform: scale(1.4);
}

.feature-display {
  flex: 1;
  padding: 0;
  position: relative;
  min-height: 200px;
  background: transparent;
}

.feature-image-container {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0px; /* 新增：保留50px底部空间 */
  z-index: 0;
  margin: -10;
  padding: 0;
  line-height: 10;
  font-size: 0;
}

.image-wrapper {
  width: 100%;
  height: 100%;
  display: block;
  position: relative;
  overflow: hidden;
}

/* 修改3：彻底修正图片显示 */
.feature-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  border-radius: 0 11px 11px 0;
  display: block;
  margin: 0;
  padding: 0;
  border: none;
  line-height: 0;
}
/* 2. 调整内容容器 */
.display-content {
  position: relative;
  height: 100%;
  padding: 2rem;
  z-index: 2;
  flex: 1; /* 新增 */
  display: flex; /* 新增 */
  flex-direction: column; /* 新增 */
}

.display-header h3 {
  color: white;
  text-shadow: 0 2px 4px rgba(0,0,0,0.5);
}

.display-header .subtitle {
  color: rgba(255,255,255,0.9);
  text-shadow: 0 1px 2px rgba(0,0,0,0.3);
}

.highlight-text {
  color: white;
  text-shadow: 0 1px 2px rgba(0,0,0,0.3);
}

.highlight-icon {
  background: rgba(255,255,255,0.2);
  color: white;
}

.modern-action-button {
  padding: 12px 24px;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 2px 8px rgba(66, 185, 131, 0.2);
}

.modern-action-button:hover {
  background: #3aa876;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(66, 185, 131, 0.3);
}

.modern-action-button .arrow {
  transition: transform 0.3s;
}

.modern-action-button:hover .arrow {
  transform: translateX(3px);
}

.action-button-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  padding: 16px 0;
}

.toolbox-container {
  width: 25%;
  background: rgb(245, 250, 250);
  border-radius: 16px;
  box-shadow:0 14px 35px rgba(0, 0, 0, 0.08);
  padding: 1.5rem;
  border: 2px solid rgba(0, 120, 255, 0.12);
  position: relative;
  overflow: hidden;
}

.toolbox-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, rgb(245, 255, 220), rgb(220, 250, 230)); /* 浅绿色渐变 */
}

.toolbox-header {
  margin-bottom: 1.5rem;
  position: relative;
}

.toolbox-title {
  font-size: 1.8rem;
  color: rgba(0, 150, 100, 0.3);
  font-weight: 600;
  letter-spacing: 0.8px;
  margin: 0 0 1rem 0;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.toolbox-divider {
  height: 2px;
  background: linear-gradient(90deg, rgba(0, 150, 100, 0.3), transparent);
  width: 80px;
}

.toolbox-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: -5px;
}

.toolbox-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.9rem 1rem;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  background: white;
  box-shadow: 0 4px 12px rgba(0, 120, 100, 0.1);
  border: 1px solid rgba(0, 150, 100, 0.15);
  position: relative;
  overflow: hidden;
  z-index: 1;
}

.toolbox-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 120, 100, 0.15);
  border-color: rgba(0, 150, 100, 0.3);
}

.toolbox-hover-effect {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(100, 210, 150, 0.05) 0%, rgba(0, 150, 100, 0.1) 100%);
  opacity: 0;
  opacity: 0;
  transition: opacity 0.3s;
  z-index: -1;
}

.toolbox-card:hover .toolbox-hover-effect {
  opacity: 1;
}

.toolbox-icon-frame {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgb(245, 255, 220), rgb(220, 250, 230)); /* 浅绿色渐变 */
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
  box-shadow: 0 4px 8px rgba(0, 120, 100, 0.1);
  border: 1px solid rgba(0, 150, 100, 0.1);
}

.toolbox-icon {
  font-size: 28px;
  color: rgb(0, 150, 100); /* 绿色图标 */
  transition: all 0.3s;
}

.toolbox-card:hover .toolbox-icon {
  transform: scale(1.1);
  color: rgb(0, 150, 100); /* 绿色图标 */
}

.toolbox-text {
  font-size: 1rem;
  color:  rgb(0, 0, 0);
  font-weight: 500;
  text-align: center;
  transition: all 0.3s;
}

.toolbox-card:hover .toolbox-text {
  color: rgb(0, 150, 100); /* 绿色文字 */
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.4s cubic-bezier(0.55, 0, 0.1, 1);
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

@media (max-width: 992px) {
  .feature-container {
    flex-direction: column;
  }
  
  .modern-feature-showcase,
  .toolbox-container {
    width: 100%;
  }
  
  .toolbox-container {
    margin-top: 2rem;
  }

  .feature-display {
    min-height: 350px;
  }
}

@media (max-width: 576px) {
  .feature-display {
    min-height: 300px;
  }
  
  .modern-action-button {
    padding: 10px 20px;
    font-size: 14px;
  }
  
  .toolbox-grid {
    grid-template-columns: 1fr;
  }
}

.icon-search:before {
  content: "🔍";
}

.icon-history:before {
  content: "🕒";
}

.icon-account_circle:before {
  content: "👤";
  font-size: 1.1em;
}

.icon-help:before {
  content: "?";
  font-weight: bold;
  font-size: 1.2em;
}

.feature-image {
  cursor: pointer; /* 添加指针样式表明可点击 */
  transition: transform 0.3s ease;
}
.feature-image:hover {
  transform: scale(1.02); /* 添加悬停效果 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}
</style>