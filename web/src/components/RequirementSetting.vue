//岗位要求组件<!-- filepath: d:\Project\Software-Cup\src\components\RequirementSetting.vue -->
<template>
  <div class="requirement-setting">
    <h2>🧾 岗位要求</h2>
    <div class="tip-text">请在下面的文本框填写岗位要求：</div>
    <textarea
      v-model="requirementText"
      class="requirement-textarea"
      placeholder="请粘贴岗位要求或面试描述..."
      rows="10"
    ></textarea>
    <div class="req-actions">
      <button class="save-btn" @click="save">保存</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getRequirements, reviseRequirement } from "@/api/user";
import store from "@/store";

const requirementText = ref('')

async function save() {
  const data = {
    username: store.state.user?.username,
    requirementText: requirementText.value
  }
  // 假设 reviseRequirement 支持 requirementText 字段
  const res = await reviseRequirement(data)
  if (res.status === 200) {
    alert(res.data.message)
  }
}

onMounted(() => {
  getRequirements(store.state.user?.username).then(res => {
    if (res.status === 200) {
      requirementText.value = res.data.requirementText || ''
    }
  })
})
</script>

<style scoped>
.requirement-setting {
  max-width: 440px;
  margin: 60px auto 0 auto;
  background: #f8fafc;
  border-radius: 18px;
  padding: 2.2rem 2rem 2rem 2rem;
  box-shadow: 0 2px 12px 0 rgba(60,80,120,0.09);
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

.requirement-setting h2 {
  text-align: center;
  margin-bottom: 1.5rem; /* 原来是0.7rem，增大间距 */
  font-size: 1.45rem;
  color: #2d8c6e;
  font-weight: 700;
  letter-spacing: 1px;
}

.tip-text {
  width: 100%;
  text-align: left;
  color: #5a6a85;
  font-size: 1.05rem;
  margin-bottom: 1.1rem;
  padding-left: 2px;
}

.requirement-textarea {
  width: 100%;
  min-height: 170px;
  border: 1.5px solid #b7d7c9;
  border-radius: 10px;
  padding: 1rem;
  font-size: 1.08rem;
  resize: vertical;
  background: #fff;
  box-sizing: border-box;
  margin-bottom: 1.5rem;
  transition: border 0.2s, box-shadow 0.2s;
  outline: none;
  box-shadow: 0 2px 8px 0 rgba(66,185,131,0.06);
}

.requirement-textarea:focus {
  border-color: #42b983;
  background: #f6fffa;
  box-shadow: 0 0 0 2px #b7f5d6;
}

.req-actions {
  text-align: center; /* 修改为居中 */
  width: 100%;
}

.save-btn {
  background: linear-gradient(90deg, #42b983 60%, #3bb2a0 100%);
  color: #fff;
  border: none;
  border-radius: 18px;
  padding: 0.8rem 2.2rem;
  font-size: 1.08rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 10px 0 rgba(66,185,131,0.10);
  letter-spacing: 1px;
}

.save-btn:hover {
  background: linear-gradient(90deg, #369f6b 60%, #2d8c6e 100%);
  box-shadow: 0 4px 16px 0 rgba(66,185,131,0.13);
}
</style>