<!-- LinkPreview.vue -->
<template>
  <div class="link-preview-wrapper">
    <a :href="url" target="_blank" rel="noopener noreferrer" class="link-card-wrapper">
      <div class="custom-link-card">
        <!-- 加载状态 -->
        <div v-if="loading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>正在加载预览...</p>
        </div>

        <!-- 错误状态 -->
        <div v-else-if="error" class="error-state">
          <div class="error-icon">⚠️</div>
          <h4 class="card-title">{{ fallbackTitle }}</h4>
          <p class="card-description">{{ fallbackDescription }}</p>
          <div class="card-footer">
            <span class="card-type">{{ type }}</span>
            <span class="external-link-icon">🔗</span>
          </div>
        </div>

        <!-- 正常状态 -->
        <div v-else class="normal-state">
          <div class="card-image-container" v-if="previewData.image">
            <img
                :src="previewData.image"
                :alt="previewData.title"
                class="card-image"
                @error="handleImageError"
            />
          </div>
          <div class="card-image-container placeholder" v-else>
            <div class="placeholder-icon">{{ getPlaceholderIcon() }}</div>
          </div>

          <div class="card-content">
            <h4 class="card-title">{{ previewData.title || fallbackTitle }}</h4>
            <p class="card-description">{{ previewData.description || fallbackDescription }}</p>
            <div class="card-footer">
              <span class="card-type">{{ type }}</span>
              <span class="external-link-icon">🔗</span>
            </div>
          </div>
        </div>
      </div>
    </a>
  </div>
</template>

<script>
export default {
  name: 'LinkPreview',
  props: {
    url: {
      type: String,
      required: true
    },
    fallbackTitle: {
      type: String,
      default: '链接标题'
    },
    fallbackDescription: {
      type: String,
      default: '点击查看详细内容'
    },
    type: {
      type: String,
      default: '链接'
    },
    // 是否启用真实的链接预览功能
    enablePreview: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      loading: false,
      error: false,
      previewData: {
        title: '',
        description: '',
        image: '',
        favicon: ''
      }
    }
  },
  mounted() {
    if (this.enablePreview) {
      this.fetchPreviewData()
    } else {
      // 使用 fallback 数据
      this.previewData = {
        title: this.fallbackTitle,
        description: this.fallbackDescription,
        image: this.getDefaultImage(),
        favicon: ''
      }
    }
  },
  methods: {
    async fetchPreviewData() {
      this.loading = true
      this.error = false

      try {
        // 这里可以调用真实的链接预览 API
        // 例如：const response = await fetch(`/api/preview?url=${encodeURIComponent(this.url)}`)

        // 模拟 API 调用
        await this.simulateApiCall()

        // 模拟成功获取数据
        this.previewData = {
          title: this.fallbackTitle,
          description: this.fallbackDescription,
          image: this.getDefaultImage(),
          favicon: this.getFavicon()
        }

      } catch (error) {
        console.error('Failed to fetch preview data:', error)
        this.error = true
      } finally {
        this.loading = false
      }
    },

    simulateApiCall() {
      return new Promise((resolve) => {
        setTimeout(resolve, 1000) // 模拟网络延迟
      })
    },

    getDefaultImage() {
      // 根据链接类型返回默认图片
      const domain = this.getDomain()
      const imageMap = {
        'github.com': 'https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png',
        'youtube.com': 'https://img.youtube.com/vi/default/hqdefault.jpg',
        'deeplearning.ai': 'https://d2l.ai/_static/logo-with-text.png',
        'wikipedia.org': 'https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png',
        'aws.amazon.com': 'https://a0.awsstatic.com/libra-css/images/logos/aws_logo_smile_1200x630.png',
        'ibm.com': 'https://1.cms.s81c.com/sites/default/files/2021-01-06/ibm-logo-black.png'
      }

      return imageMap[domain] || this.generatePlaceholderImage()
    },

    generatePlaceholderImage() {
      // 生成一个基于域名的占位符图片
      const domain = this.getDomain()
      const color = this.getColorFromString(domain)
      const initial = domain.charAt(0).toUpperCase()

      // 这里可以返回一个 data URL 或者默认图片
      return `https://ui-avatars.com/api/?name=${initial}&background=${color}&color=fff&size=200`
    },

    getDomain() {
      try {
        return new URL(this.url).hostname
      } catch {
        return 'unknown'
      }
    },

    getColorFromString(str) {
      let hash = 0
      for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash)
      }
      const color = (hash & 0x00FFFFFF).toString(16).toUpperCase()
      return '00000'.substring(0, 6 - color.length) + color
    },

    getFavicon() {
      const domain = this.getDomain()
      return `https://www.google.com/s2/favicons?domain=${domain}&sz=32`
    },

    getPlaceholderIcon() {
      const domain = this.getDomain()
      const iconMap = {
        'github.com': '💻',
        'youtube.com': '🎥',
        'deeplearning.ai': '🤖',
        'wikipedia.org': '📚',
        'aws.amazon.com': '☁️',
        'ibm.com': '🏢',
        'd2l.ai': '📖'
      }

      return iconMap[domain] || '🔗'
    },

    handleImageError() {
      // 图片加载失败时的处理
      this.previewData.image = ''
    }
  }
}
</script>

<style scoped>
.link-preview-wrapper {
  display: block;
}

.link-card-wrapper {
  text-decoration: none;
  color: inherit;
  display: block;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  background: white;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.link-card-wrapper:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
  border-color: #cbd5e0;
}

.custom-link-card {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 280px;
}

/* 加载状态 */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: #718096;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f4f6;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 错误状态 */
.error-state {
  padding: 20px;
  text-align: center;
}

.error-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

/* 正常状态 */
.normal-state {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.card-image-container {
  height: 160px;
  overflow: hidden;
  background: #f7fafc;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-image-container.placeholder {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.link-card-wrapper:hover .card-image {
  transform: scale(1.05);
}

.placeholder-icon {
  font-size: 48px;
  color: white;
  opacity: 0.9;
}

.card-content {
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card-title {
  margin: 0 0 12px 0;
  font-size: 16px;
  font-weight: 600;
  color: #2d3748;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-description {
  margin: 0 0 16px 0;
  font-size: 14px;
  color: #4a5568;
  line-height: 1.5;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.card-type {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 500;
}

.external-link-icon {
  font-size: 16px;
  opacity: 0.6;
  transition: opacity 0.3s ease;
}

.link-card-wrapper:hover .external-link-icon {
  opacity: 1;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .custom-link-card {
    min-height: 240px;
  }

  .card-image-container {
    height: 120px;
  }

  .card-content {
    padding: 16px;
  }

  .card-title {
    font-size: 15px;
  }

  .card-description {
    font-size: 13px;
  }
}
</style>