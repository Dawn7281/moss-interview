<template>
  <div>
    <!-- 遮罩层 -->
    <div class="overlay" :class="{ 'active': showPanel }" @click="closePanel"></div>

    <!-- 主编辑面板 -->
    <div class="edit-panel" :class="{ 'active': showPanel }">
      <div class="edit-header">
        <div class="edit-title">
          <span>基本资料</span>
          <span class="completion-rate">完善度{{ calculatedCompletionRate }}%</span>
        </div>
        <button class="close-btn" @click="$emit('close')">×</button>
      </div>

      <div class="edit-content">
        <!-- 基本信息部分 -->
        <div class="section">
          <div class="section-header">
            <span class="section-icon">●</span>
            <h3>基本信息</h3>
          </div>

          <div class="info-item">
            <span class="info-label">姓名</span>
            <span
                v-if="!editMode.realname"
                class="info-value"
                @click="startEditing('realname')"
                :class="{ 'required': requiredFields.includes('realname'), 'empty': !profileData.basicInfo.realname }"
            >
              {{ profileData.basicInfo.realname || '点击编辑' }}
            </span>
            <input
                v-else
                v-model="tempProfileData.basicInfo.realname"
                class="edit-input"
                @blur="saveEdit('realname')"
                @keyup.enter="saveEdit('realname')"
                ref="realnameInput"
                :class="{ 'error': requiredFields.includes('realname') && (!tempProfileData.basicInfo.realname || tempProfileData.basicInfo.realname.trim() === '') }"
            >
            <span
                v-if="requiredFields.includes('realname') && (!profileData.basicInfo.realname || profileData.basicInfo.realname.trim() === '')"
                class="error-message">
              * 必填
            </span>
          </div>

          <div class="info-item">
            <span class="info-label">我的昵称</span>
            <span
                v-if="!editMode.nickname"
                class="info-value"
                @click="startEditing('nickname')"
            >
              {{ profileData.basicInfo.nickname || '点击编辑' }}
            </span>
            <input
                v-else
                v-model="tempProfileData.basicInfo.nickname"
                class="edit-input"
                @blur="saveEdit('nickname')"
                @keyup.enter="saveEdit('nickname')"
                ref="nicknameInput"
            >
          </div>

          <div class="info-item">
            <span class="info-label">我的性别</span>
            <span
                v-if="!editMode.gender"
                class="info-value"
                @click="startEditing('gender')"
            >
              {{ profileData.basicInfo.gender || '点击编辑' }}
            </span>
            <select
                v-else
                v-model="tempProfileData.basicInfo.gender"
                class="edit-input"
                @blur="saveEdit('gender')"
                @change="saveEdit('gender')"
                ref="genderInput"
            >
              <option value="">请选择</option>
              <option value="男">男</option>
              <option value="女">女</option>
              <option value="其他">其他</option>
            </select>
          </div>

          <div class="info-item">
            <span class="info-label">我的简介</span>
            <span
                v-if="!editMode.bio"
                class="info-value"
                @click="startEditing('bio')"
            >
              {{ profileData.basicInfo.bio || '点击编辑' }}
            </span>
            <textarea
                v-else
                v-model="tempProfileData.basicInfo.bio"
                class="edit-input textarea"
                @blur="saveEdit('bio')"
                @keyup.enter="saveEdit('bio')"
                ref="bioInput"
            ></textarea>
          </div>

          <div class="info-item">
            <span class="info-label">居住地</span>
            <span
                v-if="!editMode.location"
                class="info-value"
                @click="startEditing('location')"
            >
              {{ profileData.basicInfo.location || '点击编辑' }}
            </span>
            <input
                v-else
                v-model="tempProfileData.basicInfo.location"
                class="edit-input"
                @blur="saveEdit('location')"
                @keyup.enter="saveEdit('location')"
                ref="locationInput"
            >
          </div>

          <div class="info-item">
            <span class="info-label">毕业年份</span>
            <span
                v-if="!editMode.graduationYear"
                class="info-value"
                @click="startEditing('graduationYear')"
            >
              {{ profileData.basicInfo.graduationYear || '点击编辑' }}
            </span>
            <input
                v-else
                v-model="tempProfileData.basicInfo.graduationYear"
                type="number"
                class="edit-input"
                @blur="saveEdit('graduationYear')"
                @keyup.enter="saveEdit('graduationYear')"
                ref="graduationYearInput"
            >
          </div>

          <div class="info-item">
            <span class="info-label">学历</span>
            <span
                v-if="!editMode.education"
                class="info-value"
                @click="startEditing('education')"
            >
              {{ profileData.basicInfo.education || '点击编辑' }}
            </span>
            <select
                v-else
                v-model="tempProfileData.basicInfo.education"
                class="edit-input"
                @blur="saveEdit('education')"
                @change="saveEdit('education')"
                ref="educationInput"
            >
              <option value="高中">高中</option>
              <option value="大专">大专</option>
              <option value="本科">本科</option>
              <option value="硕士">硕士</option>
              <option value="博士">博士</option>
            </select>
          </div>

          <div class="info-item">
            <span class="info-label">毕业院校</span>
            <span
                v-if="!editMode.university"
                class="info-value"
                @click="startEditing('university')"
            >
              {{ profileData.basicInfo.university || '点击编辑' }}
            </span>
            <input
                v-else
                v-model="tempProfileData.basicInfo.university"
                class="edit-input"
                @blur="saveEdit('university')"
                @keyup.enter="saveEdit('university')"
                ref="universityInput"
            >
          </div>

          <div class="info-item">
            <span class="info-label">专业</span>
            <span
                v-if="!editMode.major"
                class="info-value"
                @click="startEditing('major')"
            >
              {{ profileData.basicInfo.major || '点击编辑' }}
            </span>
            <input
                v-else
                v-model="tempProfileData.basicInfo.major"
                class="edit-input"
                @blur="saveEdit('major')"
                @keyup.enter="saveEdit('major')"
                ref="majorInput"
            >
          </div>
        </div>

        <!-- 求职期望部分 -->
        <div class="section">
          <div class="section-header">
            <span class="section-icon">●</span>
            <h3>求职期望</h3>
          </div>

          <div class="info-item">
            <span class="info-label">期望职位</span>
            <span
                v-if="!editMode.position"
                class="info-value"
                @click="startEditing('position', 'jobExpectation')"
                :class="{ 'required': requiredFields.includes('position'), 'empty': !profileData.jobExpectation.position }"
            >
              {{ profileData.jobExpectation.position || '点击编辑' }}
            </span>
            <input
                v-else
                v-model="tempProfileData.jobExpectation.position"
                class="edit-input"
                @blur="saveEdit('position', 'jobExpectation')"
                @keyup.enter="saveEdit('position', 'jobExpectation')"
                ref="positionInput"
                :class="{ 'error': requiredFields.includes('position') && (!tempProfileData.jobExpectation.position || tempProfileData.jobExpectation.position.trim() === '') }"
            >
            <span
                v-if="requiredFields.includes('position') && (!profileData.jobExpectation.position || profileData.jobExpectation.position.trim() === '')"
                class="error-message">
              * 必填
            </span>
          </div>

          <div class="info-item">
            <span class="info-label">岗位要求</span>
            <span
                v-if="!editMode.jobRequirements"
                class="info-value"
                @click="startEditing('jobRequirements', 'jobExpectation')"
                :class="{ 'required': requiredFields.includes('jobRequirements'), 'empty': !profileData.jobExpectation.jobRequirements }"
            >
              {{ profileData.jobExpectation.jobRequirements || '点击编辑' }}
            </span>
            <textarea
                v-else
                v-model="tempProfileData.jobExpectation.jobRequirements"
                class="edit-input textarea"
                @blur="saveEdit('jobRequirements', 'jobExpectation')"
                @keyup.enter="saveEdit('jobRequirements', 'jobExpectation')"
                ref="jobRequirementsInput"
                :class="{ 'error': requiredFields.includes('jobRequirements') && (!tempProfileData.jobExpectation.jobRequirements || tempProfileData.jobExpectation.jobRequirements.trim() === '') }"
            ></textarea>
            <span
                v-if="requiredFields.includes('jobRequirements') && (!profileData.jobExpectation.jobRequirements || profileData.jobExpectation.jobRequirements.trim() === '')"
                class="error-message">
              * 必填
            </span>
          </div>

          <div class="info-item">
            <span class="info-label">求职状态</span>
            <span
                v-if="!editMode.status"
                class="info-value"
                @click="startEditing('status', 'jobExpectation')"
            >
              {{ profileData.jobExpectation.status || '点击编辑' }}
            </span>
            <select
                v-else
                v-model="tempProfileData.jobExpectation.status"
                class="edit-input"
                @blur="saveEdit('status', 'jobExpectation')"
                @change="saveEdit('status', 'jobExpectation')"
                ref="statusInput"
            >
              <option value="在职，考虑新机会">在职，考虑新机会</option>
              <option value="在职，暂不考虑">在职，暂不考虑</option>
              <option value="离职，正在找工作">离职，正在找工作</option>
              <option value="在校生">在校生</option>
            </select>
          </div>

          <div class="info-item">
            <span class="info-label">期望薪资</span>
            <span
                v-if="!editMode.salaryRange"
                class="info-value"
                @click="startEditing('salaryRange', 'jobExpectation')"
            >
              {{ profileData.jobExpectation.salaryRange || '点击编辑' }}
            </span>
            <select
                v-else
                v-model="tempProfileData.jobExpectation.salaryRange"
                class="edit-input"
                @blur="saveEdit('salaryRange', 'jobExpectation')"
                @change="saveEdit('salaryRange', 'jobExpectation')"
                ref="salaryRangeInput"
            >
              <option value="不限 - 不限">不限</option>
              <option value="5k - 10k">5k - 10k</option>
              <option value="10k - 15k">10k - 15k</option>
              <option value="15k - 20k">15k - 20k</option>
              <option value="20k - 30k">20k - 30k</option>
              <option value="30k以上">30k以上</option>
            </select>
          </div>

          <div class="info-item">
            <span class="info-label">工作地点</span>
            <span
                v-if="!editMode.workLocation"
                class="info-value"
                @click="startEditing('workLocation', 'jobExpectation')"
            >
              {{ profileData.jobExpectation.workLocation || '点击编辑' }}
            </span>
            <input
                v-else
                v-model="tempProfileData.jobExpectation.workLocation"
                class="edit-input"
                @blur="saveEdit('workLocation', 'jobExpectation')"
                @keyup.enter="saveEdit('workLocation', 'jobExpectation')"
                ref="workLocationInput"
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProfileEditPanel',
  props: {
    showPanel: {
      type: Boolean,
      default: false
    },
    profileData: {
      type: Object,
      required: true,
      default: () => ({
        basicInfo: {
          realname: '',
          nickname: '',
          gender: '',
          bio: '',
          location: '',
          graduationYear: '',
          education: '',
          university: '',
          major: ''
        },
        jobExpectation: {
          position: '',
          jobRequirements: '',
          status: '',
          salaryRange: '',
          workLocation: ''
        }
      })
    },
    completionRate: {
      type: Number,
      default: 0
    }
  },

  data() {
    return {
      editMode: {
        realname: false,
        nickname: false,
        gender: false,
        bio: false,
        location: false,
        graduationYear: false,
        education: false,
        university: false,
        major: false,
        position: false,
        jobRequirements: false,
        status: false,
        salaryRange: false,
        workLocation: false
      },
      tempProfileData: {
        basicInfo: {},
        jobExpectation: {}
      },
      currentEditingField: null,
      currentEditingSection: null,
      fieldWeights: {
        basicInfo: {
          realname: 10,
          nickname: 8,
          gender: 6,
          bio: 12,
          location: 8,
          graduationYear: 7,
          education: 9,
          university: 10,
          major: 10
        },
        jobExpectation: {
          position: 12,
          jobRequirements: 15,
          status: 8,
          salaryRange: 7,
          workLocation: 10
        }
      },
      requiredFields: [
        'realname',        // 姓名（基本信息）
        'position',        // 期望职位（求职期望）
        'jobRequirements'  // 岗位要求（求职期望）
      ]
    }
  },

  computed: {
    calculatedCompletionRate() {
      // 使用与UserCenter.vue相同的计算逻辑
      let totalWeight = 0;
      let completedWeight = 0;

      // 基本信息权重
      const basicWeights = {
        realname: 10,
        nickname: 8,
        gender: 6,
        bio: 12,
        location: 8,
        graduationYear: 7,
        education: 9,
        university: 10,
        major: 10
      };

      // 求职期望权重
      const jobWeights = {
        position: 12,
        jobRequirements: 15,
        status: 8,
        salaryRange: 7,
        workLocation: 10
      };

      // 计算基本信息
      Object.entries(basicWeights).forEach(([field, weight]) => {
        totalWeight += weight;
        if (this.profileData.basicInfo[field]) {
          completedWeight += weight;
        }
      });

      // 计算求职期望
      Object.entries(jobWeights).forEach(([field, weight]) => {
        totalWeight += weight;
        if (this.profileData.jobExpectation[field]) {
          completedWeight += weight;
        }
      });

      if (totalWeight === 0) return 0;
      return Math.round((completedWeight / totalWeight) * 100);
    }
  },
  methods: {
    closePanel() {
      this.$emit('close');
      // 重置所有编辑状态
      Object.keys(this.editMode).forEach(key => {
        this.editMode[key] = false;
      });
      this.currentEditingField = null;
      this.currentEditingSection = null;
    },

    startEditing(field, section = 'basicInfo') {
      // 只重置当前字段的编辑状态
      Object.keys(this.editMode).forEach(key => {
        this.editMode[key] = false;
      });

      this.editMode[field] = true;
      this.currentEditingField = field;
      this.currentEditingSection = section;

      // 确保tempProfileData中有当前section
      if (!this.tempProfileData[section]) {
        this.tempProfileData[section] = {};
      }

      // 设置临时数据
      this.tempProfileData[section][field] = this.profileData[section][field];

      this.$nextTick(() => {
        const refName = `${field}Input`;
        const inputRef = this.$refs[refName];

        // 更健壮的输入框聚焦逻辑
        if (inputRef) {
          if (Array.isArray(inputRef)) {
            // 处理多个同名ref的情况（如v-for生成的）
            inputRef[0].focus();
          } else {
            inputRef.focus();

            // 对于textarea，将光标移动到末尾
            if (inputRef.tagName === 'TEXTAREA' || inputRef.type === 'text') {
              const length = inputRef.value.length;
              inputRef.setSelectionRange(length, length);
            }
          }
        }
      });
    },

    saveEdit(field, section = 'basicInfo') {
      // 验证当前编辑字段
      if (this.currentEditingField !== field || this.currentEditingSection !== section) {
        return;
      }

      const value = this.tempProfileData[section][field];

      // 必填字段验证
      if (this.requiredFields.includes(field)) {
        if (!value || value.toString().trim() === '') {
          this.$emit('error', {
            message: `请填写${this.getFieldLabel(field, section)}`,
            field: field
          });
          return;
        }
      }

      // 特定字段验证
      if (field === 'graduationYear') {
        const year = parseInt(value);
        if (isNaN(year) || year < 1900 || year > 2100) {
          this.$emit('error', {
            message: '请输入有效的毕业年份（1900-2100）',
            field: field
          });
          return;
        }
      }

      // 更新profileData
      this.profileData[section][field] = value;

      // 触发保存事件
      this.$emit('save', {
        section,
        data: {[field]: value}
      });

      // 重置编辑状态
      this.editMode[field] = false;
      this.currentEditingField = null;
      this.currentEditingSection = null;

      // 强制更新视图（如果需要）
      this.$forceUpdate();
    },

    getFieldLabel(field, section = 'basicInfo') {
      const labels = {
        basicInfo: {
          realname: '姓名',
          nickname: '我的昵称',
          gender: '我的性别',
          bio: '我的简介',
          location: '居住地',
          graduationYear: '毕业年份',
          education: '学历',
          university: '毕业院校',
          major: '专业'
        },
        jobExpectation: {
          position: '期望职位',
          jobRequirements: '岗位要求',
          status: '求职状态',
          salaryRange: '期望薪资',
          workLocation: '工作地点'
        }
      };
      return labels[section]?.[field] || field;
    },

    validateRequiredFields() {
      const missingFields = [];

      // 验证基本信息中的必填字段
      if (!this.profileData.basicInfo.realname || this.profileData.basicInfo.realname.trim() === '') {
        missingFields.push('姓名');
      }

      // 验证求职期望中的必填字段
      if (!this.profileData.jobExpectation.position || this.profileData.jobExpectation.position.trim() === '') {
        missingFields.push('期望职位');
      }

      if (!this.profileData.jobExpectation.jobRequirements || this.profileData.jobExpectation.jobRequirements.trim() === '') {
        missingFields.push('岗位要求');
      }

      if (missingFields.length > 0) {
        this.$emit('error', `请填写以下必填字段：${missingFields.join('、')}`);
        return false;
      }

      return true;
    }
  },

  watch: {
    showPanel(newVal) {
      if (!newVal) {
        // 当面板关闭时重置所有编辑状态
        Object.keys(this.editMode).forEach(key => {
          this.editMode[key] = false;
        });
        this.currentEditingField = null;
        this.currentEditingSection = null;
      }
    },
    profileData: {
      deep: true,
      handler(newVal) {
        // 当profileData变化时更新临时数据
        this.tempProfileData.basicInfo = JSON.parse(JSON.stringify(newVal.basicInfo));
        this.tempProfileData.jobExpectation = JSON.parse(JSON.stringify(newVal.jobExpectation));
      }
    },
    // profileData: {
    //   deep: true,
    //   handler(newVal) {
    //     // 当profileData变化时更新临时数据
    //     this.tempProfileData.basicInfo = {...newVal.basicInfo};
    //     this.tempProfileData.jobExpectation = {...newVal.jobExpectation};
    //   }
    // }
  },

  created() {
    this.tempProfileData.basicInfo = JSON.parse(JSON.stringify(this.profileData.basicInfo));
    this.tempProfileData.jobExpectation = JSON.parse(JSON.stringify(this.profileData.jobExpectation));
  }
}
</script>

<style scoped>
/* 保留原有样式不变 */
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

.completion-rate {
  margin-left: 15px;
  color: #00dcb5;
  font-size: 14px;
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

.section {
  margin-bottom: 30px;
}

.section-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.section-icon {
  color: #00dcb5;
  margin-right: 10px;
  font-size: 12px;
}

.section-header h3 {
  flex: 1;
  margin: 0;
  font-size: 16px;
  font-weight: 500;
}

.info-item {
  line-height: 1.6;
  display: flex;
  padding: 18px 0;
  margin-bottom: 12px;
  border-bottom: 1px dashed #eee;
  line-height: 0.5;
  align-items: center;
}

.info-label {
  width: 140px;
  color: #666;
  font-size: 15px;
  padding-right: 20px;
  line-height: 1.6;
  font-weight: 500;
}

.info-value {
  line-height: 1.6;
  flex: 1;
  font-size: 15px;
  padding-left: 15px;
  color: #333;
  cursor: pointer;
}

.info-value:hover {
  color: #00dcb5;
  text-decoration: underline;
}

.link {
  color: #00dcb5;
  cursor: pointer;
}

.edit-input {
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  padding: 12px 16px;
  transition: all 0.3s;
  flex: 1;
  max-width: 400px;
}

.edit-input:focus {
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
  outline: none;
}

.textarea {
  min-height: 100px;
  resize: vertical;
  width: 100%;
  max-width: 400px;
}

@media (max-width: 768px) {
  .edit-panel {
    width: 80%;
    right: -80%;
  }

  .info-item {
    flex-direction: column;
  }

  .info-label {
    width: auto;
    margin-bottom: 5px;
  }
}
</style>