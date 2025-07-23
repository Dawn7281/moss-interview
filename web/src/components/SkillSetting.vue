//技能组件
<template>
  <div class="skill-setting">
    <h2>面试技能填写</h2>
    <div class="skill-block">
      <div class="block-title">▸ 技能类型选择（必填）</div>
      <select v-model="form.type" required>
        <option disabled value="">请选择类型</option>
        <option value="技术类">技术类</option>
        <option value="管理类">管理类</option>
        <option value="沟通表达">沟通表达</option>
        <option value="其它">其它</option>
      </select>
    </div>
    <div class="skill-block">
      <div class="block-title">▸ 技能名称输入（必填）</div>
      <input v-model="form.name" type="text" placeholder="如：Java 编程 / 团队协作" required />
    </div>
    <div class="skill-block">
      <div class="block-title">▸ 熟练程度选择（必填）</div>
      <label v-for="level in levels" :key="level" :class="{active: form.level===level}">
        <input type="radio" v-model="form.level" :value="level" required /> {{ level }}
      </label>
    </div>
    <div class="skill-block">
      <div class="block-title">▸ 应用场景说明（可选）</div>
      <textarea v-model="form.scene" rows="3" placeholder="描述你如何使用此技能"></textarea>
    </div>
    <div class="skill-block">
      <div class="block-title">▸ 相关证书/作品上传（可选）</div>
      <input type="file" @change="handleFile" accept=".pdf,image/*" />
      <div v-if="form.fileName" class="file-tip">已上传：{{ form.fileName }}</div>
    </div>
    <div class="skill-block">
      <div class="block-title">▸ 技能列表展示（已填写技能）</div>
      <ul class="skill-list">
        <li v-for="(skill, idx) in skills" :key="idx">
          <span class="skill-content">{{ skill.name }}｜{{ skill.level }}｜{{ skill.scene || '无应用说明' }}</span>
          <div class="skill-actions-row">
            <button class="edit-btn" @click="editSkill(idx)">✏️ 编辑</button>
            <button class="del-btn" @click="deleteSkill(idx)">🗑 删除</button>
          </div>
        </li>
        <li v-if="!skills.length" class="empty-tip">暂无技能，请添加</li>
      </ul>
    </div>
    <div class="skill-actions">
      <button class="add-btn" @click="addSkill">➕ 添加技能</button>
      <button class="save-btn" @click="saveSkills">✅ 保存并继续</button>
    </div>
  </div>
</template>

<script setup>
import {onMounted, ref} from 'vue'
import {getSkills, reviseSkills} from "@/api/user";
import {uploadCertificate} from "@/api/file";
import store from "@/store";

const levels = ['入门', '熟练', '精通']

const form = ref({
  type: '',
  name: '',
  level: '',
  scene: '',
  file: null,
  fileName: ''
})

const skills = ref([]) // {type, name, level, scene, fileName}

const handleFile = (e) => {
  const file = e.target.files[0]
  if (file) {
    const formData = new FormData();
    formData.append('file', file);
    const res = uploadCertificate(formData);
    if (res.status === 200) {
      form.value.file = file
      form.value.fileName = file.name
    }
  }
}

const addSkill = () => {
  if (!form.value.type || !form.value.name || !form.value.level) {
    alert('请填写必填项')
    return
  }
  if (editIdx.value !== null) {
    // 编辑模式
    skills.value[editIdx.value] = { ...form.value }
    editIdx.value = null
  } else {
    skills.value.push({ ...form.value })
  }
  resetForm()
  console.log(skills.value)
}

const resetForm = () => {
  form.value = {
    type: '',
    name: '',
    level: '',
    scene: '',
    file: null,
    fileName: ''
  }
  editIdx.value = null
}

const editIdx = ref(null)
const editSkill = (idx) => {
  editIdx.value = idx
  form.value = { ...skills.value[idx] }
}

const deleteSkill = (idx) => {
  if (confirm('确定要删除该技能吗？')) {
    skills.value.splice(idx, 1)
    if (editIdx.value === idx) resetForm()
  }
}

const saveSkills = async () => {
  const data = {
    username: store.state.user?.username,
    type: [],
    name: [],
    level: [],
    scene: [],
    filename: [],
  }
  skills.value.forEach((skill) => {
    data["type"].push(skill.type || "")
    data["name"].push(skill.name || "")
    data["level"].push(skill.level || "")
    data["scene"].push(skill.scene || "")
    data["filename"].push(skill.fileName || "")
  })
  console.log(data)
  const res = await reviseSkills(data)
  if (res.status === 200) {
    alert(res.data.message)
  }
}

onMounted(() => {
  getSkills(store.state.user?.username).then((res) => {
    if (res.status === 200) {
      if (res.data.type === null) return;
      for (let i = 0; i < res.data.type.length; i++) {
        skills.value[i] = {
          type: res.data.type[i],
          name: res.data.name[i],
          level: res.data.level[i],
          scene: res.data.scene[i],
        }
      }
      // console.log(res.data.type)
    }
  })
})
</script>

<style scoped>
.skill-setting {
  max-width: 540px;
  margin: 0 auto;
  background: #f8fafc;
  border-radius: 14px;
  padding: 2rem 2.5rem;
  box-shadow: 0 2px 12px 0 rgba(60,80,120,0.08);
}
.skill-setting h2 {
  text-align: center;
  margin-bottom: 1.5rem;
}
.skill-block {
  margin-bottom: 1.2rem;
}
.block-title {
  font-weight: bold;
  margin-bottom: 0.6rem;
}
select, input[type="text"], textarea {
  width: 100%;
  border: 1px solid #d3dbe8;
  border-radius: 6px;
  padding: 0.5rem 0.8rem;
  font-size: 1rem;
  margin-bottom: 0.3rem;
  box-sizing: border-box;
}
input[type="text"] {
  min-width: 100px;
  max-width: 100%;
}
textarea {
  min-height: 48px;
  max-height: 200px;
  width: 100%;
  resize: vertical;
  overflow-y: auto;
}
.skill-block label {
  margin-right: 1.5rem;
  font-size: 1.08rem;
  cursor: pointer;
  padding: 0.3rem 1.1rem;
  border-radius: 8px;
  transition: background 0.2s;
  display: inline-block;
}
.skill-block label.active {
  background: #e6f7ff;
  color: #42b983;
  font-weight: bold;
}
.file-tip {
  color: #888;
  font-size: 0.98rem;
  margin-top: 0.3rem;
}
.skill-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.skill-list li {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  background: #f4f7fa;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  margin-bottom: 0.5rem;
  font-size: 1.05rem;
  word-break: break-all;
  max-width: 100%;
}

.skill-content {
  width: 100%;
  word-break: break-all;
  white-space: pre-line;
  margin-bottom: 0.7rem;
  line-height: 1.8;
}

.skill-actions-row {
  width: 100%;
  display: flex;
  gap: 1rem;
  justify-content: flex-start; /* 或 flex-end 右对齐 */
}

.edit-btn, .del-btn {
  margin: 0;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.08rem;
  border-radius: 5px;
  padding: 0.2rem 0.7rem;
  transition: background 0.2s;
}
.edit-btn:hover {
  background: #e6f7ff;
  color: #42b983;
}
.del-btn:hover {
  background: #ffeaea;
  color: #e74c3c;
}
.empty-tip {
  color: #aaa;
  text-align: center;
  background: none;
  padding: 0.5rem 0;
}
.skill-actions {
  text-align: center;
  margin-top: 1.5rem;
}
.add-btn, .save-btn {
  background: #42b983;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.7rem 2rem;
  font-size: 1.1rem;
  margin-right: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}
.save-btn {
  background: #e0e7ef;
  color: #333;
}
.add-btn:hover {
  background: #369f6b;
}
.save-btn:hover {
  background: #d3dbe8;
}
</style>