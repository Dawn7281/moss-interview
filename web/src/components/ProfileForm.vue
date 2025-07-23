<template>
  <div class="profile-form-container">
    <div class="form-section">
      <h3 class="form-title">个人信息填写</h3>
      <div class="form-row triple-fields">
        <div class="form-group">
          <label for="name">姓名</label>
          <input 
            type="text" 
            id="name" 
            v-model="formData.name" 
            placeholder="请输入您的姓名"
            class="form-input"
            @change="handleUserInfo"
          >
        </div>
        <div class="form-group">
          <label for="major">专业</label>
          <input 
            type="text" 
            id="major" 
            v-model="formData.major" 
            placeholder="请输入您的专业"
            class="form-input"
            @change="handleUserInfo"
          >
        </div>
        <div class="form-group">
          <label for="expectedPosition">期望职位</label>
          <input 
            type="text" 
            id="expectedPosition" 
            v-model="formData.expectedPosition" 
            placeholder="请输入期望职位"
            class="form-input"
            @change="handleUserInfo"
          >
        </div>
      </div>
    </div>
    <div class="form-row single-field">
      <div class="form-group full-width">
        <label for="jobRequirements">面试岗位要求</label>
        <textarea 
          id="jobRequirements" 
          v-model="formData.jobRequirements" 
          placeholder="请描述该职位的面试要求"
          rows="4"
          class="form-textarea"
          @change="handleUserInfo"
        ></textarea>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import store from "@/store";
import {editInterviewInfo, getInterviewInfo} from "@/api/user";

const route = useRoute();
const formData = ref({
  name: '',
  major: '',
  expectedPosition: '',
  jobRequirements: ''
});

function  handleUserInfo(){
  const data = {...formData.value, 'username': store.state.user?.username};
  console.log('data', formData.value);
  editInterviewInfo(data)
}

onMounted(async () => {
  // 从路由查询参数中获取数据
  const {position, requirements} = route.query;

  const res = await getInterviewInfo(store.state.user?.username)
  if (res.status === 200) {
    formData.value = res.data;
  }

  // 如果存在路由参数，则填充表单
  if (position) {
    formData.value.expectedPosition = position;
    handleUserInfo()
  }

  if (requirements) {
    formData.value.jobRequirements = requirements;
    handleUserInfo()
  }
});
</script>

<style scoped>


.profile-form-container {
  background: #fff;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  max-width: 1200px;
  margin: 0 auto;
  border: 1px solid #e0e7ef;
   font-family: 'Microsoft YaHei UI', system-ui, sans-serif;
}

.form-section {
  margin-bottom: 2rem;
}

.form-title {
 color: #2c3e50;
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  position: relative; /* 为伪元素定位 */
  font-weight: 520;
  display: inline-block; /* 让下划线只跟随标题宽度 */
}
.form-title::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: 0;
  height: 4px; /* 增加初始高度 */
  width: 100%;
  background: linear-gradient(90deg, 
    #42b983 0%,        /* 左侧最粗 */
    #42b983 20%,       /* 保持粗度 */
    rgba(66, 185, 131, 0.8) 50%, /* 开始变细 */
    rgba(66, 185, 131, 0.4) 70%, /* 持续变细 */
    transparent 100%   /* 完全透明 */
  );
  border-radius: 3px; /* 增大圆角 */
  transform: skewX(-70deg); /* 增加倾斜角度 */
  transform-origin: left center;
  box-shadow: 0 1px 2.5px rgba(66, 185, 131, 0.3); /* 添加轻微阴影增强立体感 */
}
.form-row {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-row.triple-fields {
  justify-content: space-between;
}

.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.form-group label {
  color: #555;
  font-size: 0.95rem;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-input, 
.form-textarea {
  border: 1px solid #dfe2e6;
  border-radius: 8px;
  padding: 0.85rem 1rem;
  font-size: 1.1rem; /* 统一使用这个尺寸 */
  line-height: 1.8; /* 增强可读性 */
  transition: all 0.3s ease;
  background-color: #fafafa;
  outline: none;
  font-family: 'Homemade Apple', cursive;
  letter-spacing: 1px; /* 增加字间距 */
}

.form-input:hover, 
.form-textarea:hover {
  border-color: #b3b9c4;
  background-color: #fff;
}

.form-input:focus, 
.form-textarea:focus {
   border-color: #42b983 !important;
  background-color: #fff !important;
  box-shadow: 0 0 0 3px #fafafa!important;
  outline: 2px solid transparent !important;
}

.form-input:-webkit-autofill:focus,
.form-textarea:-webkit-autofill:focus {
  border-color: #42b983 !important;
  -webkit-box-shadow: 0 0 0 3px rgba(66, 185, 131, 0.15) !important;
}
.form-row.single-field {
  margin-bottom: 0;
}

.full-width {
  width: 100%;
}

.form-textarea {
  resize: vertical;
  min-height: 120px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .profile-form-container {
    padding: 1.5rem;
    border-radius: 12px;
  }
  
  .form-row {
    flex-direction: column;
    gap: 1rem;
  }
  
  .form-row.triple-fields {
    flex-direction: column;
    gap: 1rem;
  }
  
  .form-title {
    font-size: 1.25rem;
    text-align: left;
  }
}

/* 占位符样式 */
input::placeholder, 
textarea::placeholder {
  color: #a8a8a8;
  font-size: 0.95rem;
}

/* 聚焦时标签样式 */
.form-group:focus-within label {
  color: #42b983;
}
</style>