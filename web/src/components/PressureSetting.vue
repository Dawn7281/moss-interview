<template>
  <div class="pressure-setting">
    <h2>🎭 模拟面试压力设置</h2>
    <div class="pressure-block">
      <div class="block-title">▸ 请选择压力等级：</div>
      <div class="pressure-levels">
        <label
          v-for="item in pressureOptions"
          :key="item.value"
          :class="['level-card', {active: pressureLevel === item.value}]"
        >
          <input type="radio" v-model="pressureLevel" :value="item.value" hidden @click="handle(item)" />
          <div class="level-header">
            <span class="level-radio">
              <span :class="['circle', {checked: pressureLevel === item.value}]"></span>
            </span>
            <span class="level-title">{{ item.label }} <span class="level-emoji">{{ item.emoji }}</span></span>
          </div>
          <ul class="level-desc">
            <li v-for="desc in item.desc" :key="desc">{{ desc }}</li>
          </ul>
        </label>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import {postPressure} from "@/api/interview";
import store from "@/store";
const pressureLevel = ref('mild')
const pressureOptions = [
  {
    label: '轻松模式',
    value: 'mild',
    emoji: '😌',
    desc: ['节奏缓和、语气友好', '适合初学者']
  },
  {
    label: '普通模式',
    value: 'medium',
    emoji: '🙂',
    desc: ['标准语速、正常节奏', '真实还原典型面试氛围']
  },
  {
    label: '高压模式',
    value: 'high',
    emoji: '😠',
    desc: ['快速追问、语气略严厉', '模拟压力面、挑战性强']
  }
]

const handle = (item) => {
  console.log(item.value)
  postPressure({'level': item.value, 'username': store.state.user?.username})
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
.pressure-setting h2 {
  font-weight: 500;
  text-align: center;
  margin-bottom: 2.8rem;
  font-size: 1.5rem;
  letter-spacing: 1px;
}
.pressure-block {
  margin-bottom: 2.5rem;
}
.block-title {
  font-weight: bold;
  margin-bottom: 1.3rem;
  font-size: 1.08rem;
  letter-spacing: 1px;
}
.pressure-levels {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}
.level-card {
  height: 96px;
  background: #fff;
  border-radius: 12px;
  padding: 1.2rem 1.5rem;
  box-shadow: 0 2px 8px 0 rgba(66,185,131,0.06);
  border: 2px solid transparent;
  cursor: pointer;
  transition: border 0.2s, box-shadow 0.2s, background 0.2s;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
}
.level-card.active,
.level-card:hover {
  border: 1.5px solid #42b983;
  background: linear-gradient(90deg, #e0f7fa 60%, #c6f7e2 100%);
  box-shadow: 0 4px 18px 0 rgba(66,185,131,0.10);
}
.level-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.2rem;
}
.level-radio {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1.1rem;
  height: 1.1rem;
}
.circle {
  display: inline-block;
  width: 1.1rem;
  height: 1.1rem;
  border-radius: 50%;
  border: 2px solid #bbb;
  background: #fff;
  transition: border 0.2s, background 0.2s;
}
.circle.checked {
  border: 1.5px solid #42b983;
  background: #42b983;
  box-shadow: 0 0 0 2px #c6f7e2;
}
.level-title {
  font-size: 1.15rem;
  font-weight: 500;
  color: #2b7a78;
  letter-spacing: 1px;
}
.level-emoji {
  font-size: 1.3rem;
  margin-left: 0.3rem;
}
.level-desc {
  margin: 0 0 0 2.2rem;
  padding: 0;
  color: #888;
  font-size: 1.03rem;
  line-height: 1.7;
  list-style: disc;
}
.scene-card {
  min-width: 340px;
  max-width: 400px;
  flex: 1 1 0;
  /* 其它样式不变 */
}
</style>