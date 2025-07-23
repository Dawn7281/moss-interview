<template>
  <div class="interview-type-setting">
    <h2>🎯 面试类型选择</h2>
    <div class="type-list">
      <div
        v-for="item in interviewTypes"
        :key="item.value"
        :class="['type-card', {active: interviewType === item.value}]"
        @click="handleType(item)"
      >
        <span class="type-icon" v-html="item.icon"></span>
        <div class="type-info">
          <div class="type-label">{{ item.label }}</div>
          <div class="type-desc">{{ item.desc }}</div>
        </div>
        <input
          type="radio"
          v-model="interviewType"
          :value="item.value"
          style="display:none"
        />
      </div>
    </div>
    <div class="type-current">
      当前选择：<b>{{ currentLabel }}</b>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { postType } from "@/api/interview";
import store from "@/store";

const interviewType = ref('hr')
const interviewTypes = [
  {
    label: 'HR 初面',
    value: 'hr',
    desc: '简历筛选 & 基础评估',
    icon: '👩‍💼'
  },
  {
    label: '业务面试',
    value: 'business',
    desc: '专业能力考核',
    icon: '💼'
  },
  {
    label: '终面',
    value: 'final',
    desc: '综合素质与团队匹配',
    icon: '🏆'
  }
]
const currentLabel = computed(() =>
  interviewTypes.find(i => i.value === interviewType.value)?.label || ''
)
const handleType = (item) => {
  interviewType.value = item.value
  postType({'type': interviewType.value, 'username': store.state.user?.username})
}
</script>

<style scoped>
.pressure-setting,
.interview-type-setting {
  
  height: 100%;
  display: flex;
  flex-direction: column;
  width: 100%;
  background: none;
  border-radius: 0;
  padding: 0;
  box-shadow: none;
  box-sizing: border-box;
   margin-top: -35px;
}
.interview-type-setting h2 {
  font-weight: 500;
  text-align: center;
  margin-bottom: 2.0rem;
  font-size: 1.5rem;
  letter-spacing: 1px;
}
.type-list {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  margin-bottom: 2rem;
}
.type-card {
  display: flex;
  align-items: center;
  gap: 1.7rem;
  background: #fff;
  border-radius: 16px;
  padding: 1.4rem 2rem;
  box-shadow: 0 2px 12px 0 rgba(66,185,131,0.08);
  cursor: pointer;
  border: 2px solid transparent;
  transition: border 0.2s, box-shadow 0.2s, background 0.2s;
  position: relative;
  min-height: 80px;
}
.type-card:hover,
.type-card.active {
  border: 1.5px solid #42b983;
  background: linear-gradient(90deg, #e0f7fa 60%, #c6f7e2 100%);
  box-shadow: 0 4px 18px 0 rgba(66,185,131,0.10);
}
.type-icon {
  font-size: 2.5rem;
  width: 3.2rem;
  text-align: center;
}
.type-info {
  flex: 1;
}
.type-label {
  font-size: 1.22rem;
  font-weight: 500;
  color: #2b7a78;
  margin-bottom: 0.3rem;
  letter-spacing: 1px;
}
.type-desc {
  color: #888;
  font-size: 1.05rem;
  line-height: 1.7;
}
.type-current {
  color: #888;
  text-align: center;
  margin-top: 1.5rem;
  font-size: 1.12rem;
  margin-bottom: 1.2rem;
}
</style>