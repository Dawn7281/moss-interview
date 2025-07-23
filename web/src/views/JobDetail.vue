<template>
  <div class="job-detail-container">
    <div class="back-button" @click="$router.go(-1)">
      <svg viewBox="0 0 24 24" width="24" height="24">
        <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/>
      </svg>
      返回职位列表
    </div>
    
    <div class="job-detail-card">
      <div class="job-header">
        <h1 class="job-title">{{ job.title }}</h1>
        <div class="job-meta">
          <span class="job-salary">{{ job.salary }}</span>
          <span class="job-location">{{ job.location }}</span>
          <span class="job-experience">{{ job.experience }}</span>
          <span class="job-education">{{ job.education }}</span>
        </div>
      </div>
      
      <div class="company-info">
        <div class="company-logo" :style="{ backgroundColor: logoColor }">
          {{ job.companyName.substring(0, 1) }}
        </div>
        <div class="company-details">
          <h2 class="company-name">{{ job.companyName }}</h2>
          <div class="company-meta">
            <span class="company-industry">{{ job.industry }}</span>
            <span class="company-size">{{ job.companySize }}</span>
          </div>
        </div>
      </div>
      
      <div class="job-content">
        <div class="section">
          <h3 class="section-title">职位描述</h3>
          <div class="section-content" v-html="formattedDescription"></div>
        </div>
        
        <div class="section">
          <h3 class="section-title">任职要求</h3>
          <div class="section-content" v-html="formattedRequirements"></div>
        </div>
        
        <div class="section">
          <h3 class="section-title">工作地点</h3>
          <div class="section-content">
            <p>{{ job.address }}</p>
          </div>
        </div>
      </div>
      
      <div class="job-footer">
        <div class="update-time">更新于 {{ job.updateTime }}</div>
        <button class="apply-button" @click="handleApply">立即申请</button>
      </div>
    </div>
  </div>
</template>

<script>
import { stringToColor } from '../utils/colorUtils'
// import { getJobById } from '../api/jobs'

export default {
  name: 'JobDetail',
  props: {
    id: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      job: {}
    }
  },
  computed: {
    logoColor() {
      return stringToColor(this.job.companyName)
    },
    formattedDescription() {
      return this.job.description?.replace(/\n/g, '<br>') || ''
    },
    formattedRequirements() {
      return this.job.requirements?.replace(/\n/g, '<br>') || ''
    }
  },
  async created() {
    await this.fetchUserData()
    await this.fetchResumeStatus() // 初始化时获取简历状态
},
  methods: {
    async fetchJobDetail() {
      try {
        const response = await getJobById(this.id)
        this.job = response.data
      } catch (error) {
        console.error('获取职位详情失败:', error)
        this.$router.push('/jobs')
      }
    },
    handleApply() {
      // 处理申请逻辑
      alert(`已申请职位: ${this.job.title}`)
    }
  }
}
</script>

<style scoped>
.job-detail-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 24px;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #42b983;
  font-size: 14px;
  margin-bottom: 16px;
  cursor: pointer;
}

.back-button svg {
  fill: #42b983;
}

.job-detail-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  padding: 24px;
}

.job-header {
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.job-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
}

.job-meta {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  font-size: 14px;
  color: #666;
}

.job-salary {
  color: #ff6b00;
  font-weight: 500;
}

.company-info {
  display: flex;
  gap: 16px;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.company-logo {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
  font-weight: bold;
  flex-shrink: 0;
}

.company-details {
  flex: 1;
}

.company-name {
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 4px;
  color: #333;
}

.company-meta {
  display: flex;
  gap: 12px;
  font-size: 14px;
  color: #666;
}

.job-content {
  margin-bottom: 24px;
}

.section {
  margin-bottom: 24px;
}

.section-title {
  font-size: 18px;
  font-weight: 500;
  color: #333;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #f0f0f0;
}

.section-content {
  font-size: 17px !important;
  line-height: 1.8;
  color: #444;
}

.job-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 1px dashed #eaeaea;
}

.update-time {
  font-size: 13px;
  color: #999;
}

.apply-button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 4px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.apply-button:hover {
  background-color: #3aa876;
}
</style>