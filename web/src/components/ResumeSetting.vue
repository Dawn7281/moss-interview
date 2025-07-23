<!-- filepath: d:\Project\SoftworkCup\front-6-16\src\components\ResumeSetting.vue -->
<template>
  <div class="edit-panel" :class="{ 'active': showUploadPanel }">
    <div class="edit-header">
      <div class="edit-title">
        <span>简历上传</span>
      </div>
      <button class="close-btn" @click="closeUploadPanel">×</button>
    </div>

    <div class="edit-content">
      <div class="upload-area" :class="{hasFile: !!resumeUrl}">
        <label class="upload-label" v-if="!resumeUrl">
          <input type="file" accept="application/pdf" @change="handleResumeUpload" hidden />
          <span class="upload-btn">点击上传PDF简历</span>
          <span class="upload-tip">仅支持PDF格式，最大10MB</span>
        </label>
        <div v-else class="file-info">
          <div class="file-name-wrap">
            <span class="file-icon">📄</span>
            <span class="file-name">{{ fileName }}</span>
          </div>
          <div class="file-actions">
            <button class="reupload-btn" @click="triggerUpload">重新上传</button>
            <button class="delete-btn" @click="removeFile">删除</button>
          </div>
        </div>
        <input ref="fileInput" type="file" accept="application/pdf" @change="handleResumeUpload" style="display:none" />
      </div>
      
      <div v-if="resumeUrl" class="resume-preview">
        <iframe :src="resumeUrl" width="100%" height="400px" style="border:1px solid #eee;"></iframe>
      </div>
      
      <div class="edit-actions">
        <button class="save-btn" @click="saveResume" :disabled="!resumeUrl">保存简历</button>
        <button class="cancel-btn" @click="closeUploadPanel">取消</button>
      </div>
    </div>
  </div>

  <!-- 遮罩层 -->
  <div class="overlay" :class="{ 'active': showUploadPanel }" @click="closeUploadPanel"></div>
</template>

<script setup>
import {getCurrentInstance, onMounted, ref} from 'vue'
import {getResume, resumeOptimization, uploadResume} from "@/api/file"
import store from "@/store"

const showUploadPanel = ref(false)
const resumeUrl = ref('')
const fileName = ref('')
const fileInput = ref(null)
const fileBlob = ref(null)

const emit = defineEmits(['upload-success'])

function openUploadPanel() {
  showUploadPanel.value = true
  document.body.style.overflow = 'hidden'
  // 返回Promise以便外部可以等待
  return new Promise((resolve) => {
    // 保存resolve函数以便内部调用
    const closePanel = () => {
      showUploadPanel.value = false
      document.body.style.overflow = ''
      resolve()
    }
    // 覆盖原来的closeUploadPanel方法
    closeUploadPanel = closePanel
  })
}

function closeUploadPanel() {
  showUploadPanel.value = false
  document.body.style.overflow = ''
}

function triggerUpload() {
  fileInput.value && fileInput.value.click()
}

function removeFile() {
  resumeUrl.value = ''
  fileName.value = ''
  fileBlob.value = null
  if (fileInput.value) fileInput.value.value = ''
}

async function handleResumeUpload(e) {
  const file = e.target.files[0]
  if (file && file.type === 'application/pdf') {
    if (file.size > 10 * 1024 * 1024) {
      alert('文件不能超过10MB')
      return
    }
    resumeUrl.value = URL.createObjectURL(file)
    fileName.value = file.name
    fileBlob.value = file
  } else {
    alert('请上传PDF格式的简历')
  }
}

// 在saveResume方法中更新Vuex状态
// 在ResumeSetting.vue的saveResume方法中
async function saveResume() {
  if (!fileBlob.value) return
  const formData = new FormData()
  formData.append('file', fileBlob.value)
  try {
    const res = await uploadResume(formData, store.state.user?.username)
    await resumeOptimization({'filename': res.data.filename, 'username': store.state.user?.username})
    
    // 新增：更新本地hasResume状态
    store.commit('setHasResume', true)
    
    // 触发上传成功事件
    emit('upload-success')
    
    // 显示成功消息
    alert('简历保存成功')
    
    // 关闭面板
    closeUploadPanel()
  } catch (error) {
    alert('简历保存失败')
    console.error('简历保存失败:', error)
    throw error
  }
}

onMounted(() => {
  const instance = getCurrentInstance()

  // 自动获取已上传简历
  getResume(store.state.user?.username).then((response) => {
    if (response.status === 200 && response.data) {
      // 兼容后端返回二进制流或URL
      if (response.data instanceof Blob) {
        // 后端返回文件流
        const contentDisposition = response.headers['content-disposition']
        let filename = 'resume.pdf'

        if (contentDisposition) {
          // 优先尝试 RFC 5987 格式 (filename*=UTF-8''...)
          const filenameStarMatch = contentDisposition.match(/filename\*=UTF-8''(.+)/i)
          if (filenameStarMatch) {
            // 解码 URL 编码的中文文件名
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

        fileName.value = filename
        const file = new File([response.data], fileName.value, { type: response.data.type })
        resumeUrl.value = URL.createObjectURL(file)
        fileBlob.value = file
        instance?.emit('has-resume', true)
      } else if (typeof response.data === 'string') {
        // 后端返回文件URL
        resumeUrl.value = response.data
        let filename = response.data.split('/').pop() || 'resume.pdf'
        // URL解码中文字符
        try {
          filename = decodeURIComponent(filename)
        } catch (e) {
          console.warn('URL文件名解码失败:', e)
        }
        fileName.value = filename
      }
    }
  })
})

defineExpose({
  openUploadPanel
})
</script>

<style scoped>
.edit-panel {
  position: fixed;
  top: 0;
  right: -820px;
  width: 760px;
  height: 100vh;
  background: #fff;
  box-shadow: -4px 0 24px rgba(0, 0, 0, 0.08);
  transition: right 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1001;
  overflow-y: auto;
  border-top-left-radius: 16px;
  border-bottom-left-radius: 16px;
}
.edit-panel.active {
  right: 0;
}
.edit-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #f0f0f0;
}
.edit-title {
  font-size: 18px;
  font-weight: 500;
}
.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  color: #666;
  cursor: pointer;
  padding: 5px 10px;
}
.edit-content {
  padding: 20px;
}
.upload-area {
  background: #fff;
  border: 2px dashed #42b983;
  border-radius: 12px;
  padding: 2.2rem 1.5rem;
  text-align: center;
  margin-bottom: 1.2rem;
  transition: border-color 0.2s;
  position: relative;
}
.upload-area.hasFile {
  border-style: solid;
  border-color: #e0e7ef;
  background: #f4f7fa;
}
.upload-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
}
.upload-btn {
  background: #42b983;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.7rem 2rem;
  font-size: 1.1rem;
  margin-bottom: 0.7rem;
  cursor: pointer;
  transition: background 0.2s;
}
.upload-btn:hover {
  background: #369f6b;
}
.upload-tip {
  color: #aaa;
  font-size: 0.98rem;
}
.file-info {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.file-name-wrap {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  width: 100%;
}
.file-icon {
  font-size: 1.6rem;
  margin-right: 0.5rem;
  vertical-align: top;
  flex-shrink: 0;
  margin-top: 2px;
}
.file-name {
  color: #42b983;
  font-weight: bold;
  font-size: 1.08rem;
  max-width: 100%;
  word-break: break-all;
  white-space: pre-line;
  overflow-wrap: break-word;
  line-height: 1.7;
  display: block;
}
.file-actions {
  display: flex;
  flex-direction: row;
  gap: 1rem;
  justify-content: flex-end;
  width: 100%;
}
.reupload-btn, .delete-btn {
  background: #e0e7ef;
  color: #333;
  border: none;
  border-radius: 6px;
  padding: 0.3rem 1.1rem;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}
.reupload-btn:hover {
  background: #c6f7e2;
  color: #42b983;
}
.delete-btn {
  background: #ffeaea;
  color: #e74c3c;
}
.delete-btn:hover {
  background: #ffd6d6;
}
.resume-preview {
  margin-top: 1.2rem;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(60,80,120,0.08);
}
.edit-actions {
  display: flex;
  gap: 16px;
  margin-top: 24px;
  justify-content: flex-end;
}
.save-btn {
  border-radius: 8px;
  background-color: #00dcb5;
  color: white;
  border: 1px solid #00dcb5;
  padding: 10px 24px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s ease;
}
.save-btn:hover {
  background-color: #00dcb5;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3);
}
.save-btn:disabled {
  background-color: #ccc;
  border-color: #ccc;
  cursor: not-allowed;
}
.cancel-btn {
  border-radius: 8px;
  background-color: #f8f8f8;
  color: #666;
  border: 1px solid #e0e0e0;
  padding: 10px 24px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
}
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
}
.overlay.active {
  opacity: 1;
  visibility: visible;
}
@media (max-width: 768px) {
  .edit-panel {
    width: 80%;
    right: -80%;
  }
}
</style>