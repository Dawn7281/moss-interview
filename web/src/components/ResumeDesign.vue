<template>
  <div class="resume-optimizer">

    <div class="resume-corner-image">
      <img src="@/assets/resume.jpg" alt="简历角标">
    </div>
    <!-- 主标题区 -->
    <div class="header">
      <h1>简历优化助手</h1>
    </div>

    <!-- 主要内容区 -->
    <div class="main-content">
      <!-- 左侧上传和预览区 -->
      <div class="upload-preview-section">
        <div class="upload-panel">
          <h2>上传您的简历</h2>
          <div v-if="hasResume" class="reupload-btn-container">
            <button class="reupload-btn" @click="triggerFileInput">
              <svg class="reupload-icon" viewBox="0 0 24 24">
                <path fill="currentColor"
                      d="M12,4V1L8,5L12,9V6C15.31,6 18,8.69 18,12C18,15.31 15.31,18 12,18C8.69,18 6,15.31 6,12H4C4,16.42 7.58,20 12,20C16.42,20 20,16.42 20,12C20,7.58 16.42,4 12,4Z"/>
              </svg>
              重新上传简历
            </button>
            <p class="file-info">当前文件: {{ resumeFilename }}</p>
          </div>
          <div v-else>
            <div
                class="upload-area"
                @dragover.prevent="handleDragOver"
                @dragleave="handleDragLeave"
                @drop.prevent="handleDrop"
                @click="triggerFileInput"
            >
              <svg class="upload-icon" viewBox="0 0 24 24">
                <path fill="currentColor"
                      d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20M8,15V13H16V15H8M8,11V9H16V11H8Z"/>
              </svg>
              <p>点击或拖拽文件到此处</p>
            </div>
            <p class="file-info">仅支持PDF格式</p>
          </div>

          <!-- 将input元素移到外层，确保始终存在 -->
          <input
              type="file"
              ref="fileInput"
              @change="handleFileChange"
              accept=".pdf"
              style="display: none"
          />

          <!-- 简历预览区 -->
          <div class="resume-preview" v-if="hasResume">
            <h2>简历预览</h2>
            <div class="preview-content">
              <div v-if="debugMode" class="debug-info">
                <p>当前文件: {{ resumeFilename }}</p>
                <p>文件类型: PDF</p>
<!--                <p>文件URL: {{ resumeUrl }}</p>-->
              </div>
              <div v-if="loading" class="loading-state">
                正在加载预览...
              </div>
              <div v-else-if="previewError" class="error-state">
                预览加载失败
                <button @click="retryPreview">重试</button>
              </div>
              <iframe
                  v-else
                  :src="resumeUrl"
                  @load="onIframeLoad"
                  @error="onPreviewError"
                  class="resume-iframe"
              ></iframe>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧建议区 -->
      <div class="suggestions-section">
        <h2>优化建议</h2>
        <div v-if="hasResume && suggestions.length > 0" class="suggestion-list">
          <div
              v-for="(suggestion, index) in suggestions"
              :key="index"
              class="suggestion-card"
              :class="{ important: suggestion.severity === 'high' }"
          >
            <h3>{{ suggestion.title || suggestion.category }}</h3>
            <p>{{ suggestion.content }}</p>
            <p class="advice">{{ suggestion.examples.join(' ') }}</p>
          </div>
        </div>
        <div v-else-if="hasResume" class="empty-suggestions">
          <p>正在生成优化建议...</p>
        </div>
        <div v-else class="empty-suggestions">
          <div class="upload-icon-container">
            <svg class="upload-illustration" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path
                  d="M14 2H6C4.89543 2 4 2.89543 4 4V20C4 21.1046 4.89543 22 6 22H18C19.1046 22 20 21.1046 20 20V8L14 2Z"
                  stroke="#95a5a6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M14 2V8H20" stroke="#95a5a6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M16 13H8" stroke="#95a5a6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M16 17H8" stroke="#95a5a6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M10 9H8" stroke="#95a5a6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <p>请先上传简历以获取优化建议</p>
        </div>
      </div>
    </div>

    <!-- 底部操作区 -->
    <div class="footer">
      <button
          v-if="hasResume"
          class="export-btn"
          @click="exportSuggestions"
      >
        导出优化意见
      </button>
    </div>
  </div>
</template>

<script>
import {mapState} from 'vuex'
import {getResume, resumeOptimization, uploadResume} from "@/api/file";
import store from "@/store";

export default {
  name: 'ResumeOptimizer',
  data() {
    return {
      isDragging: false,
      optimizationData: {
        "matching_scores": {
          "skills_match": {
            "score": 75,
            "details": {
              "core_skills": 80,
              "tech_stack": 70,
              "project_relevance": 70
            },
            "comments": [
              "掌握Python、Flask、Vue等核心技能，符合岗位技术栈要求",
              "具备前后端分离开发经验，但后端框架（如Spring）熟练度待验证",
              "项目涉及AI大模型集成，与岗位中'计算机视觉'方向部分契合"
            ]
          },
          "experience_match": {
            "score": 60,
            "details": {
              "years_fit": 40,
              "project_scale": 70,
              "industry_fit": 50
            },
            "comments": [
              "在校生缺乏全职工作经验，仅参与实验室及竞赛项目",
              "智能模拟面试系统项目规模较大且技术复杂度高",
              "学术项目与工业界落地场景存在一定差距"
            ]
          },
          "career_fit": {
            "score": 85,
            "details": {
              "career_path": 90,
              "growth_potential": 85,
              "stability": 80
            },
            "comments": [
              "职业路径明确，持续深耕计算机科学与技术领域",
              "在校期间已展现较强的技术学习能力和项目成果",
              "学生身份稳定性较高，但需验证长期职业规划"
            ]
          }
        },
        "overall_match": 73,
        "resume_optimization": {
          "highlights": [
            "智能模拟面试系统负责人经历",
            "国家级大学生创新大赛优秀结题",
            "数学建模省二等奖",
            "GPA 3.58/4.0（专业前10%）"
          ],
          "improvements_needed": [
            "未量化项目成果（如系统处理并发量/响应时间）",
            "缺乏企业级开发流程经验（如CI/CD、代码评审）",
            "未体现团队协作中的具体角色贡献"
          ],
          "expression_suggestions": [
            "将'协助进行资料收集整理'改为'主导实验数据采集方案设计'",
            "用'开发无人机行为识别系统（识别准确率达92%）'替代笼统描述",
            "增加技术博客/开源贡献等自我提升记录"
          ]
        },
        "final_recommendation": {
          "decision": "待定",
          "key_reasons": [
            "技术基础扎实但工程实践经验不足",
            "学术项目与商业落地存在转化风险",
            "需补充企业级开发流程认知"
          ],
          "suggested_actions": [
            "建议增加GitHub代码仓库链接展示工程能力",
            "补充项目性能指标和技术选型理由",
            "推荐参加企业级项目实战培训"
          ]
        }
      },
      debugMode: import.meta.env.MODE === 'development',
      loading: false,
      previewError: false,
      hasResume: false,
      resumeUrl: '',
      resumeFilename: '',
      suggestions: []
    }
  },
  methods: {
    onIframeLoad() {
      this.loading = false;
      this.previewError = false;
    },
    onPreviewError() {
      this.loading = false;
      this.previewError = true;
    },
    retryPreview() {
      this.previewError = false;
      this.loading = true;
    },
    triggerFileInput() {
      this.$refs.fileInput.click()
    },
    handleFileChange(event) {
      const file = event.target.files[0]
      if (!file) return
      this.uploadFile(file)
    },
    handleDragOver() {
      this.isDragging = true
      event.currentTarget.style.border = '2px solid #3498db'
      event.currentTarget.style.backgroundColor = 'rgba(52, 152, 219, 0.1)'
    },
    handleDragLeave() {
      this.isDragging = false
      event.currentTarget.style.border = '2px dashed #bdc3c7'
      event.currentTarget.style.backgroundColor = 'white'
    },
    handleDrop(event) {
      this.handleDragLeave()
      const file = event.dataTransfer.files[0]
      if (file) {
        this.uploadFile(file)
      }
    },
    async uploadFile(file) {
      try {
        if (!file || !(file instanceof File)) {
          throw new Error('请选择有效的文件');
        }

        if (file.type !== 'application/pdf') {
          throw new Error('仅支持PDF格式');
        }

        this.loading = true;
        this.previewError = false;

        const formData = new FormData()
        formData.append('file', file)
        const res = await uploadResume(formData, store.state.user?.username)
        this.getResumeFile()
        await resumeOptimization({'filename': res.data.filename, 'username': store.state.user?.username}).then(res => {
          this.optimizationData = res.data.advice
          this.suggestions = this.getSuggestions()
        })

      } catch (error) {
        console.error('上传失败:', error);
        this.previewError = true;
        alert(`上传失败: ${error.message}`);
      } finally {
        this.loading = false;
      }
    },
    async fetchOptimizationSuggestions() {
      setTimeout(() => {
        // 模拟API调用
      }, 1500)
    },
    exportSuggestions() {
      if (!this.suggestions || this.suggestions.length === 0) {
        alert('没有可导出的优化建议');
        return;
      }

      // 生成建议文本内容
      let content = `简历优化建议报告\n\n`;
      content += `生成时间: ${new Date().toLocaleString()}\n\n`;

      this.suggestions.forEach((suggestion, index) => {
        content += `建议 ${index + 1}: ${suggestion.title}\n`;
        content += `重要程度: ${suggestion.severity === 'high' ? '高' : '中'}\n`;
        content += `问题描述: ${suggestion.content}\n`;
        content += `具体建议: ${suggestion.examples.join('\n           ')}\n\n`;
      });

      // 创建Blob对象
      const blob = new Blob([content], {type: 'text/plain;charset=utf-8'});

      // 创建下载链接
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);

      // 设置下载文件名
      const filename = this.resumeFilename
          ? `优化建议_${this.resumeFilename.replace('.pdf', '.txt')}`
          : '简历优化建议.txt';
      link.download = filename;

      // 触发下载
      document.body.appendChild(link);
      link.click();

      // 清理
      setTimeout(() => {
        document.body.removeChild(link);
        URL.revokeObjectURL(link.href);
      }, 100);
    },
    getResumeFile() {
      getResume(store.state.user?.username).then((response) => {
        if (response.status === 200 && response.data) {
          // 兼容后端返回二进制流或URL
          if (response.data instanceof Blob) {
            // 后端返回文件流
            this.hasResume = true;

            // 正确解析中文文件名
            const contentDisposition = response.headers['content-disposition']
            let filename = 'resume.pdf'

            if (contentDisposition) {
              // 优先尝试 RFC 5987 格式
              const filenameStarMatch = contentDisposition.match(/filename\*=UTF-8''(.+)/i)
              if (filenameStarMatch) {
                filename = decodeURIComponent(filenameStarMatch[1])
              } else {
                // 退回到普通格式
                const filenameMatch = contentDisposition.match(/filename="?(.+?)"?(?:;|$)/)
                if (filenameMatch) {
                  filename = filenameMatch[1]
                  // 如果是乱码，尝试UTF-8解码
                  try {
                    filename = decodeURIComponent(escape(filename))
                  } catch (e) {
                    console.warn('文件名解码失败:', e)
                  }
                }
              }
            }

            this.resumeFilename = filename
            const file = new File([response.data], this.resumeFilename, {type: response.data.type})
            this.resumeUrl = URL.createObjectURL(file)

            resumeOptimization({'filename': this.resumeFilename.replace('.pdf', '-active.pdf'), 'username': store.state.user?.username}).then(res => {
              this.optimizationData = res.data.advice
              this.suggestions = this.getSuggestions()
            })
          } else if (typeof response.data === 'string') {
            // 后端返回文件URL
            this.resumeUrl = response.data
            let filename = response.data.split('/').pop() || 'resume.pdf'
            // URL解码中文字符
            try {
              filename = decodeURIComponent(filename)
            } catch (e) {
              console.warn('URL文件名解码失败:', e)
            }
            this.resumeFilename = filename
          }
        }
      })
    },
    getSuggestions() {
      return [
        {
          severity: 'high',
          title: '技能匹配度 (' + this.optimizationData.matching_scores.skills_match.score + '%)',
          content: this.optimizationData.matching_scores.skills_match.comments.join(' '),
          examples: [
            '核心技能匹配度: ' + this.optimizationData.matching_scores.skills_match.details.core_skills + '%',
            '技术栈匹配度: ' + this.optimizationData.matching_scores.skills_match.details.tech_stack + '%',
            '项目相关性: ' + this.optimizationData.matching_scores.skills_match.details.project_relevance + '%'
          ]
        },
        {
          severity: 'medium',
          title: '经验匹配度 (' + this.optimizationData.matching_scores.experience_match.score + '%)',
          content: this.optimizationData.matching_scores.experience_match.comments.join(' '),
          examples: [
            '年限匹配度: ' + this.optimizationData.matching_scores.experience_match.details.years_fit + '%',
            '项目规模: ' + this.optimizationData.matching_scores.experience_match.details.project_scale + '%',
            '行业匹配度: ' + this.optimizationData.matching_scores.experience_match.details.industry_fit + '%'
          ]
        },
        {
          severity: 'low',
          title: '职业契合度 (' + this.optimizationData.matching_scores.career_fit.score + '%)',
          content: this.optimizationData.matching_scores.career_fit.comments.join(' '),
          examples: [
            '职业路径: ' + this.optimizationData.matching_scores.career_fit.details.career_path + '%',
            '成长潜力: ' + this.optimizationData.matching_scores.career_fit.details.growth_potential + '%',
            '稳定性: ' + this.optimizationData.matching_scores.career_fit.details.stability + '%'
          ]
        },
        {
          severity: 'high',
          title: '简历亮点',
          content: '您的简历有以下突出优势',
          examples: this.optimizationData.resume_optimization.highlights
        },
        {
          severity: 'medium',
          title: '需要改进的方面',
          content: '以下方面可以进一步提升',
          examples: this.optimizationData.resume_optimization.improvements_needed
        },
        {
          severity: 'high',
          title: '表达优化建议',
          content: '建议调整以下表述方式',
          examples: this.optimizationData.resume_optimization.expression_suggestions
        },
        {
          severity: 'high',
          title: '最终评估: ' + this.optimizationData.final_recommendation.decision,
          content: this.optimizationData.final_recommendation.key_reasons.join(' '),
          examples: this.optimizationData.final_recommendation.suggested_actions
        }
      ]
    }
  },
  mounted() {
    this.getResumeFile()
  }
}
</script>

<style scoped>
/* 基础样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Roboto', sans-serif;
}

.resume-optimizer {
  /* 保持原始宽度和高度 */
  width: 90vw;
  max-width: 90rem; /* 添加最大宽度限制 */
  min-width: 70rem; /* 添加最小宽度保证 */
  height: 95vh;    /* 改为视口高度 */
  min-height: 65rem; /* 最小高度保证 */
  margin-left: -6.7rem !important; /* 保持原始定位 */
  /* 保持原始定位和边框 */
  position: relative;
 /* 重置偏移 */
  margin: 0 auto; /* 居中显示 */
  padding: 1.5rem;
  border-radius: 12px;
  background-color: #ffffff;
  color: #2c3e50;
  border: 1px solid #4ECDC4; /* 合并边框 */
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
  
  /* 添加溢出控制 */
  overflow: hidden;
  display: flex;
  flex-direction: column;
}




/* 添加新样式 */
.resume-corner-image {
  position: absolute;
  top: 0px; /* 向上移动部分图片到边框外 */
  left: -5px; /* 向左移动部分图片到边框外 */
  width: 80px; /* 适当大小 */
  height: 80px; /* 保持正方形 */
  border-radius: 30%; /* 圆形裁剪 */
  overflow: hidden; /* 隐藏超出部分 */
  border: 3px solid white; /* 白色边框 */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2); /* 轻微阴影 */
  z-index: 100; /* 确保在最上层 */
  transform: rotate(5deg); /* 添加15度逆时针旋转 */
  transform-origin: bottom right; /* 以右下角为旋转中心 */
  transition: transform 0.3s ease;
}

.resume-corner-image img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 确保图片内容居中显示 */
  object-position: center; /* 聚焦中间的小玩偶 */
}

/* 主标题区 */
.header {
  height: 75px;
  background-color: #f9fbfb;
  display: flex;
  align-items: center;
  padding: 0 20px;
  border-bottom: 1px solid #e0e0e0;
  border-radius: 8px;
  margin-bottom: 15px;
  z-index: 10; /* 确保标题在最上层 */
  
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}
.header h1 {
  font-family: 'ZCOOL XiaoWei', serif;
  font-size: 28px;
  font-weight: 400;
  color: #2c3e50;
  position: relative;
  display: inline-block;
  padding-bottom: 15px;
   margin-left: 40px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

/* 不规则下划线效果 */
.header h1::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg,
  #4ECDC4 0%,
  #4ECDC4 10%,
  #32ca99 20%,
  #32ca99 35%,
  #4ECDC4 50%,
  #4ECDC4 65%,
  #32ca99 80%,
  #32ca99 100%);
  border-radius: 2px;
  clip-path: polygon(
      0% 0%,
      10% 100%,
      20% 0%,
      30% 100%,
      40% 0%,
      50% 100%,
      60% 0%,
      70% 100%,
      80% 0%,
      90% 100%,
      100% 0%
  );
  transform: skewX(-15deg);
}

/* 悬停动画效果 */
.header h1:hover::after {
  animation: underlineWave 1.5s ease infinite;
}

@keyframes underlineWave {
  0% {
    clip-path: polygon(
        0% 0%,
        10% 100%,
        20% 0%,
        30% 100%,
        40% 0%,
        50% 100%,
        60% 0%,
        70% 100%,
        80% 0%,
        90% 100%,
        100% 0%
    );
  }
  50% {
    clip-path: polygon(
        0% 100%,
        10% 0%,
        20% 100%,
        30% 0%,
        40% 100%,
        50% 0%,
        60% 100%,
        70% 0%,
        80% 100%,
        90% 0%,
        100% 100%
    );
  }
  100% {
    clip-path: polygon(
        0% 0%,
        10% 100%,
        20% 0%,
        30% 100%,
        40% 0%,
        50% 100%,
        60% 0%,
        70% 100%,
        80% 0%,
        90% 100%,
        100% 0%
    );
  }
}

/* 主要内容区 */
.main-content {
   display: flex;
  flex: 1;
  gap: 20px;
  overflow: hidden;
  height: calc(100% - 170px);
}

/* 左侧上传和预览区 */
.upload-preview-section {
  width: 65%; /* 保持比例但基于更宽的父容器 */
  min-width: 820px; /* 设置更大的最小宽度 */
  background-color: #f8f9fa;
  display: flex;
  flex-direction: column;
  padding: 30px;
  overflow-y: auto;
  border-right: 1px solid #e0e0e0;
  border-radius: 12px;
}

.upload-panel {
  margin-bottom: 30px;
}

.upload-panel h2 {
  font-size: 18px;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 10px;
}

.upload-area {
  height: 180px;
  border: 2px dashed #bdc3c7;
  background-color: white;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 20px;
  border-radius: 12px;
}

.upload-area:hover {
  border-color: #3498db;
  background-color: rgba(52, 152, 219, 0.05);
}

.upload-icon {
  width: 48px;
  height: 48px;
  color: #3498db;
  margin-bottom: 15px;
}

.file-info {
  font-size: 12px;
  color: #95a5a6;
  text-align: center;
  margin-top: 10px;
}

/* 简历预览区 */
.resume-preview {
  margin-top: 30px;
  flex: 1;
  display: flex;
  flex-direction: column;
  width: 100%; /* 新增：确保宽度填满容器 */
  border-radius: 12px;
  height: 1500px;
}

.resume-preview h2 {
  font-size: 18px;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 15px;
}

.preview-content {
  flex: 1;
  border: 1px solid #e0e0e0;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  min-height: 900px; /* 新增：设置最小高度 */
}

.resume-iframe {
  width: 100%;
  flex: 1;
  border: none;
  min-height: 700px;
  background-color: #f5f5f5; /* 新增：设置最小高度 */
}

.doc-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 30px;
  flex: 1;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.download-btn {
  margin-top: 20px;
  padding: 10px 24px;
  background-color: #3498db;
  color: white;
  border-radius: 4px;
  text-decoration: none;
  font-size: 14px;
  transition: background-color 0.3s;
}

.download-btn:hover {
  background-color: #2980b9;
}

/* 右侧建议区 */
.suggestions-section {
  width: 55%;
  padding: 30px;
  overflow-y: auto;
  background-color: white;
}

.suggestions-section h2 {
  font-size: 18px;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 20px;
}

.suggestion-list {
  margin-top: 20px;
}

.suggestion-card {
  background-color: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 15px;
  transition: all 0.3s ease;
  border-left: 4px solid #3498db;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.suggestion-card.important {
  border-left-color: #e74c3c;
  background-color: #fff9f9;
}

.suggestion-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.suggestion-card h3 {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 10px;
  color: #2c3e50;
}

.suggestion-card p {
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 10px;
  color: #555;
}

.suggestion-card .advice {
  font-size: 14px;
  font-style: italic;
  color: #3498db;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px dashed #e0e0e0;
}

.empty-suggestions {
  text-align: center;
  padding: 50px 0;
  color: #95a5a6;
  font-size: 14px;
}

/* 底部操作区 */
.footer {
  height: 80px;
  background-color: white;
  border-top: 1px solid #e0e0e0;
  padding: 20px;
  display: flex;
  justify-content: flex-end;
  flex-shrink: 0;
}

.export-btn {
  background-color: #32ca99;
  color: white;
  padding: 10px 24px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.export-btn:hover {
  background-color: #27ae60;
  box-shadow: 0 2px 8px rgba(39, 174, 96, 0.3);
}

.export-btn:active {
  transform: translateY(1px);
}

@media (max-width: 1300px) {
  .resume-optimizer {
    width: 95vw;
    min-width: auto;
  }
  
  .upload-preview-section,
  .suggestions-section {
    min-width: auto;
  }
}

/* 动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.suggestion-card {
  animation: fadeIn 0.3s ease forwards;
}

.suggestion-card:nth-child(1) {
  animation-delay: 0.1s;
}

.suggestion-card:nth-child(2) {
  animation-delay: 0.2s;
}

.suggestion-card:nth-child(3) {
  animation-delay: 0.3s;
}

.suggestion-card:nth-child(4) {
  animation-delay: 0.4s;
}

.debug-info {
  font-size: 14px; /* 增大字体 */
  color: #666;
  background: #f5f5f5;
  padding: 15px; /* 增大内边距 */
  margin-bottom: 15px;
  border-radius: 4px;
  white-space: pre-wrap;
  word-break: break-all;
  line-height: 1.1; /* 增大行高 */
}

.debug-info p {
  margin: 8px 0; /* 为每个段落添加间距 */
}

.loading-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #7f8c8d;
}

.docx-preview-container {
  width: 100%;
  flex: 1;
  min-height: 500px;
  background-color: #f5f5f5;
  overflow: auto;
  padding: 20px;
  border: 1px solid #ddd;
  position: relative;
}

.docx-loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #666;
}

.docx-preview-container >>> .docx-wrapper {
  background-color: white;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.docx-preview-container >>> .docx {
  font-family: Arial, sans-serif;
  line-height: 1.5;
}

.empty-suggestions {
  text-align: center;
  padding: 30px 0; /* 增加内边距 */
  color: #95a5a6;
  font-size: 16px; /* 加大文字 */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.upload-illustration {
  width: 150px; /* 从80px增加到120px */
  height: 150px; /* 从80px增加到120px */
  margin-bottom: 30px; /* 从20px增加到25px */
  opacity: 0.8; /* 提高透明度 */
}

.upload-icon-container {
  margin-bottom: 25px; /* 从15px增加到20px */
}

.reupload-btn-container {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  margin-bottom: 20px;

}

.reupload-btn {
  display: flex;
  justify-content: center;
  width: 100%;
  align-items: center;
  padding: 12px 24px;
  background-color: #f8f9fa;
  color: #3498db;
  border: 2px solid #d3cece;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-sizing: border-box; /* 包含边框和内边距在宽度内 */
  height: 48px;
}

.reupload-btn:hover {
  background-color: #f5f5f5;
  color: white;
  box-shadow: 0 2px 8px rgba(52, 152, 219, 0.3);
}

.reupload-icon {
  width: 20px;
  height: 20px;
  margin-right: 8px;
}
</style>