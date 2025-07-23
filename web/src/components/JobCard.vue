<template>
  <div class="job-card-container">
    <div class="job-card" @click.stop="toggleExpand">
      <div class="job-header">
        <h3 class="job-title">{{ truncatedTitle }}</h3>
        <span class="job-salary">{{ job.salary }}</span>
      </div>
      
      <div class="job-location">
        <span>{{ job.location }}</span>
        <span>{{ job.education }}</span>
        <span class="job-salary">{{ job.salary }}</span> <!-- 确保薪资显示 -->
      </div>
      
      <div class="job-company">
        <div class="logo-placeholder" :style="{ backgroundColor: logoColor }">
          {{ job.companyName.substring(0, 1) }}
        </div>
        <span class="company-name">{{ job.companyName }}</span>
        <span class="industry-tag">{{ job.industry }}</span>
      </div>
    </div>

    <transition name="fade">
      <div 
        v-if="isExpanded" 
        class="details-box"
        @click.stop
        ref="detailsBox"
      >
        <div class="detail-section">
          <div class="detail-row">
            <span class="detail-label">公司规模:</span>
            <span>{{ job.companySize }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">工作经验:</span>
            <span>{{ job.experience }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">工作地点:</span>
            <span>{{ job.address }}</span>
          </div>
        </div>
        
        <div class="detail-section">
          <h4 class="section-title">职位描述</h4>
          <p class="job-description">{{ job.description }}</p>
        </div>
        
        <div class="detail-section">
          <h4 class="section-title">技能要求</h4>
          <div class="skill-tags">
            <span v-for="(skill, index) in job.skills" :key="index" class="skill-tag">
              {{ skill }}
            </span>
          </div>
        </div>
        
        <div class="update-time">更新于 {{ job.updateTime }}</div>

        <!-- 添加按钮部分 -->
       <div class="button-container">
    <div class="button-group">
      <button class="action-button mock-interview-button" @click="goToMockInterview">
        前往面试
      </button>
      <button class="action-button generate-question-button" @click="goToInterviewQA">
        生成个性化试题
      </button>
    </div>
  </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { stringToColor } from '../utils/colorUtils'

export default {
  props: {
    job: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      isExpanded: false
    }
  },
  computed: {
    truncatedTitle() {
      const maxLength = 15
      return this.job.title.length > maxLength 
        ? this.job.title.substring(0, maxLength) + '...' 
        : this.job.title
    },
    logoColor() {
      return stringToColor(this.job.companyName)
    }
  },
  methods: {
     
    goToMockInterview() {
      // 提取岗位要求和职位描述中的任职要求部分
      const jobRequirements = this.extractJobRequirements();
      
      // 跳转到面试页面并携带数据
      this.$router.push({
        path: '/mock-interview',
        query: {
          position: this.job.title,          // 面试岗位
          requirements: jobRequirements,    // 岗位要求
          company: this.job.companyName     // 公司名称
        }
      });
    },
    
    // 从职位描述中提取任职要求
    extractJobRequirements() {
      // 职位描述中包含"任职要求"或"岗位要求"这样的标题
      // 这里实现一个简单的提取逻辑，实际可以根据需求调整
      const description = this.job.description || '';
      const requirementsSection = description.split('\n').find(line => 
        line.includes('任职要求') || line.includes('岗位要求')
      );
      
      if (requirementsSection) {
        // 提取从标题开始到下一个标题或结尾的内容
        const startIndex = description.indexOf(requirementsSection);
        const remainingText = description.substring(startIndex);
        const nextSectionIndex = remainingText.indexOf('\n\n');
        
        return nextSectionIndex > 0 
          ? remainingText.substring(0, nextSectionIndex)
          : remainingText;
      }
      
      // 如果没有找到明确的标题，返回整个描述或空字符串
      return description || '无具体要求';
    },
    goToInterviewQA() {
      this.$router.push({
        path: '/qa',
        query: {
          position: this.job.title
        }
      });
      // 关闭展开的详情框
      this.isExpanded = false;
    },
    handleDocumentClick(event) {
      if (this.isExpanded && !this.$el.contains(event.target)) {
        this.isExpanded = false
      }
    },
    // toggleExpand() {
    //   this.isExpanded = !this.isExpanded
    //   if(this.isExpanded) {
    //     this.$nextTick(() => {
    //       this.adjustDetailsHeight()
    //     })
    //   }
    // },
     handleCardClick() {
      if (!this.expandedId || this.expandedId === this.job.id) {
        this.$emit('toggle-expand', this.job.id)
      }
    },
    toggleExpand() {
      this.isExpanded = !this.isExpanded
      if(this.isExpanded) {
        this.$nextTick(() => {
          this.adjustDetailsPosition()
        })
      }
    },
    adjustDetailsPosition() {
      const detailsBox = this.$refs.detailsBox;
      if (detailsBox) {
        // 居中定位
        detailsBox.style.position = 'fixed';
        detailsBox.style.top = '50%';
        detailsBox.style.left = '50%';
        detailsBox.style.transform = 'translate(-50%, -50%)';
        
        // 设置固定宽度和最大高度
        detailsBox.style.width = '600px';
        detailsBox.style.maxHeight = '80vh';
      }
    }
  },
  mounted() {
    // 添加全局点击监听器来关闭详情框
    document.addEventListener('click', this.handleDocumentClick)
  },
  beforeDestroy() {
    // 移除监听器
    document.removeEventListener('click', this.handleDocumentClick)
  },
}
</script>


<style scoped>
/* 修改后的按钮样式 */
.button-container {
  display: flex;
  justify-content: flex-end;
  margin-top: auto;
  padding-top: 20px;
  border-top: 1px solid #eaeaea;
}

.button-group {
  display: flex;
  gap: 24px;
}

.action-button {
  padding: 10px 24px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
   min-width: 120px; /* 添加最小宽度保证按钮大小一致 */
}

.mock-interview-button {
  background-color: #3dcd9f;
  color: white;
}

.mock-interview-button:hover {
  background-color: #3dcd9f;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
}

.generate-question-button {
  background-color: #2196F3;
  color: white;
}

.generate-question-button:hover {
  background-color: #0b7dda;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.3);
}
.job-card-container {
  width: 285px;
  height: 100%;
  position: relative;
  margin-bottom: 8px; /* 为详情框预留空间 */
}

.job-card {
  width: 100%;
  height: 140px;
  min-height: 110px;
  padding: 10px;
  background: #f8f8f8;
  border: 1px solid #eaeaea;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  gap: 8px;
  flex-direction: column;
  overflow: hidden;
  position: relative;
  z-index: 1;
}


.job-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.details-box {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 600px;
  height: 700px; /* 固定高度 */
  background: white;
  border: 1px solid #eaeaea;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  padding: 20px;
  z-index: 1000;
  overflow-y: auto; /* 内容过长时显示滚动条 */
  display: flex;
  flex-direction: column;
  font-size: 19px; /* 基础字体大小 */
}


/* 调整内容区域高度 */
.detail-content {
  flex: 1;
  overflow-y: auto;
  padding-right: 8px; /* 为滚动条留出空间 */
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

/* 其他原有样式保持不变 */
.job-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
}

.job-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  color: #333;
  line-height: 1.4;
  flex: 1;
  margin-right: 8px;
}

.job-salary {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  color: #333;
  line-height: 1.4;
  flex: 1;
  flex-shrink: 0;
  white-space: normal;
  overflow: visible;
  text-overflow: clip;
  word-break: break-word;
}

.job-location {
  font-size: 12px;
  color: #666;
  margin-bottom: 12px;
  display: flex;
  gap: 8px;
  align-items: center;
}

.job-company {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: auto;
}

.logo-placeholder {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 12px;
  margin-right: 8px;
  flex-shrink: 0;
}

.company-name {
  font-size: 13px;
  line-height: 1.4;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
}

.industry-tag {
  font-size: 11px;
  color: #666;
  background: #f5f5f5;
  padding: 2px 6px;
  border-radius: 10px;
  margin-left: 8px;
  white-space: nowrap;
}

.detail-section {
  margin-bottom: 16px;
}

.section-title {
  font-size: 22px;
  font-weight: 400;
  color: #333;
  margin: 0 0 8px 0;
   line-height: 1.3;
  letter-spacing: 0.3px;
}

.detail-row {
  display: flex;
  font-size: 17px;
  color: #666;
  margin-bottom: 6px;
  line-height: 1.8;
}

.detail-label {
  font-size: 18px; 
  font-weight: 400;
  color: #333;
  min-width: 70px;
}

.job-description {
  font-size: 15px;
  color: #666;
  line-height: 1.8;
  margin: 8px 0 0 0;
  white-space: pre-line;
    word-break: break-word;
  max-width: 600px; /* 控制文本最大宽度 */
}

.skill-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  max-width: 600px;
  margin-top: 8px;
}

.skill-tag {
  background: #f0f7ff;
  color: #1890ff;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 15px;
}

.update-time {
  font-size: 14px;
  color: #999;
  text-align: right;
  margin-top: 12px;
}
</style>