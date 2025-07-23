<template>
    <div class="interview-container">
    <!-- 左侧导航栏 -->
    <div class="left-sidebar">
      <div class="sidebar-logo">
        <span class="logo-icon">📁</span>
        <span class="logo-text">题目</span>
      </div>
      <div class="sidebar-item">
        <span class="item-icon">🎓</span>
      </div>
      <div class="sidebar-item active" @click="showMyQuestions = !showMyQuestions">
        <span class="item-text">我的题单</span>
        <span class="item-action">+</span>
      </div>

       <!-- 我的题单列表 -->
     <div 
        v-for="(record, index) in myQuestions" 
        :key="index" 
        class="my-question-item"
        @click="showRecordedQuestion(record)"
    >
        <span class="record-time">{{ formatTime(record.time) }}</span>
        <span class="record-title">{{ truncateString(record.questionData.question, 15) }}</span>
        <button class="delete-btn" @click.stop="deleteQuestion(index)">×</button>
    </div>
    </div>
    <!-- 中间主内容区 -->
    <div class="main-content">
      <!-- 顶部横幅 -->
      <div class="banner-section">
        <div class="banner-card" style="background: #000;">
          <div class="banner-title">算法面试</div>
          <div class="banner-subtitle">专项面试题</div>
        </div>
        <div class="banner-card" style="background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);">
          <div class="banner-title">MySQL必知必会</div>
          <div class="banner-subtitle">由浅入深，学透MySQL</div>
        </div>
        <div class="banner-card" style="background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);">
          <div class="banner-title">递归与分治</div>
          <div class="banner-play">▶</div>
          <div class="banner-subtitle">全视角解析</div>
        </div>
      </div>

    <!-- 筛选与搜索 -->
  <div class="filter-section">
  <div class="filter-container">
    <!-- 添加标题 -->
    <h3 class="filter-title">岗位</h3>

    <!-- 修改岗位按钮部分 -->
    <div class="filter-buttons" ref="filterButtons">
      <button class="filter-btn" @click="selectPositionTag('后端')">后端</button>
      <button class="filter-btn" @click="selectPositionTag('前端')">前端</button>
      <button class="filter-btn" @click="selectPositionTag('软件')">软件</button>
      <button class="filter-btn" @click="selectPositionTag('测试')">测试</button>
      <button class="filter-btn" @click="selectPositionTag('自动化')">自动化</button>
      <button class="filter-btn" @click="selectPositionTag('数据分析')">数据分析</button>
      <button class="filter-btn" @click="selectPositionTag('全栈')">全栈</button>
      <button class="filter-btn" @click="selectPositionTag('架构师')">架构师</button>
      <button class="filter-btn" @click="selectPositionTag('云计算')">云计算</button>
      <!-- 以下按钮默认隐藏 -->
      <button class="filter-btn" @click="selectPositionTag('运维')">运维</button>
      <button class="filter-btn" @click="selectPositionTag('DevOps')">DevOps</button>
      <button class="filter-btn" @click="selectPositionTag('网络安全')">网络安全</button>
      <button class="filter-btn" @click="selectPositionTag('机器学习')">机器学习</button>
      <button class="filter-btn" @click="selectPositionTag('人工智能')">人工智能</button>
      <button class="filter-btn" @click="selectPositionTag('移动开发')">移动开发</button>
      <button class="filter-btn" @click="selectPositionTag('游戏开发')">游戏开发</button>
      <button class="filter-btn" @click="selectPositionTag('算法')">算法</button>
      <button class="filter-btn" @click="selectPositionTag('图像识别')">图像识别</button>
      <button class="filter-btn" @click="selectPositionTag('分布式')">分布式</button>
      <button class="filter-btn" @click="selectPositionTag('计算机视觉')">计算机视觉</button>
      <button class="filter-btn" @click="selectPositionTag('区块链')">区块链</button>
      <button class="filter-btn" @click="selectPositionTag('嵌入式')">嵌入式</button>
    </div>
    <button class="filter-more-btn" @click="toggleShowAll">
      {{ showAllFilters ? '收起 ' : '更多 ' }}
    </button>
  </div>
</div>

      <!-- 个性化面试试题区域 -->
      <div class="personalized-section">
        <h2>个性化面试试题</h2>
        <div class="qa-toolbar">
          <button class="toolbar-btn" @click="updateQuestions">
              <span class="icon">🔄</span> 重新生成面试题
          </button>
          
          <button class="toolbar-btn" @click="convertQA">
            <span class="icon">👁</span>
            {{ showAllAnswers ? '隐藏所有答案' : '显示所有答案' }}
          </button>
          
          <div class="export-dropdown">
            <button class="toolbar-btn" @click.stop="showExport = !showExport">
              <span class="icon">📄</span> 导出 <span style="font-size:0.9em;">▼</span>
            </button>
            <div v-if="showExport" class="export-menu">
              <div class="export-item" @click="exportQuestions('txt')">TXT</div>
              <div class="export-item" @click="exportQuestions('docx')">DOCX</div>
              <div class="export-item" @click="exportQuestions('pdf')">PDF</div>
            </div>
          </div>
        </div>
        
        <div v-for="(item, idx) in qaList" :key="item.id" class="qa-card">
          <div class="qa-card">
          <button 
            v-if="currentViewingRecord" 
            class="qa-btn back-btn" 
            @click="backToFullList"
          >
            <span class="icon">🔙</span> 返回
          </button>
  
          <div class="qa-header">
            <span class="qa-index">{{ idx + 1 }}.</span>
            <span class="qa-tag">{{ item.category || '通用' }}</span>
            <span class="qa-level" :class="item.level">{{ item.level }}</span>
          </div>
          <div class="qa-question">{{ item.question }}</div>
          <div class="qa-actions">
            <button class="qa-btn" @click="toggleAnswer(idx)">
              {{ item.showAnswer ? '隐藏答案' : '查看答案' }}
            </button>
            <button
                class="qa-btn"
                :class="{ 'wave-anim': recordingIdx === idx }"
                @click="startVoice(idx)"
            >
              <span v-if="recordingIdx === idx && !endRecordingIdxList.includes(idx)">
                录音中...
                <span class="voice-wave">
                  <span class="dot"></span>
                  <span class="dot"></span>
                  <span class="dot"></span>
                  <span class="dot"></span>
                </span>
              </span>
              <span v-else-if="recordingIdx === idx && endRecordingIdxList.includes(idx)">
                播放中...
                <span class="voice-wave">
                  <span class="dot"></span>
                  <span class="dot"></span>
                  <span class="dot"></span>
                  <span class="dot"></span>
                </span>
              </span>
              <span v-else-if="endRecordingIdxList.includes(idx)">播放语音</span>
              <span v-else>语音答题</span>
            </button>
            <button class="qa-btn" v-if="endRecordingIdxList.includes(idx)" @click="stopVoice(idx)">重新回答</button>
            <button class="qa-btn" @click="copyAnswer(item.answer, idx)">
              {{ copiedIdx === idx ? '已复制' : '复制答案' }}
            </button>
             <!-- 新增的保存单个题目按钮 -->
           <button class="qa-btn" @click="saveSingleQuestion(item)">
             <span class="icon">💾</span> 加入我的题单
           </button>
          </div>
          <div class="qa-answer" v-if="item.showAnswer">
            <span class="answer-label">参考答案：</span>
            <span>{{ item.answer }}</span>
          </div>
          <div class="qa-voice" v-if="recordingIdx === idx || item.audioUrl">
            <div class="voice-bar" v-if="recordingIdx === idx"></div>
            <button class="qa-btn" v-if="recordingIdx === idx" @click="cancelVoice">
              取消
            </button>
            <button class="qa-btn" v-if="recordingIdx === idx && !endRecordingIdxList.includes(idx)" @click="stopVoice(idx)">结束</button>
          </div>
        </div>
      </div>
    </div>
    </div>

    <!-- 右侧功能区 -->
  <div class="right-sidebar">
    <!-- 每日1题日历 -->
    <div class="sidebar-card">
      <div class="card-header">
        <span class="header-title">每日1题</span>
        <div class="calendar-nav">
          <button class="nav-btn" @click="prevMonth">&lt;</button>
          <span class="current-month">{{ currentMonthYear }}</span>
          <button class="nav-btn" @click="nextMonth">&gt;</button>
        </div>
        <span class="date-badge">{{ currentDate }}</span>
      </div>
      <div class="calendar-grid">
        <div class="weekdays">
          <span v-for="day in weekdays" :key="day">{{ day }}</span>
        </div>
        <div class="dates">
          <span 
            v-for="(date, index) in dates" 
            :key="index" 
            :class="{ 
              'current-date': date.isCurrentDate,
              'other-month': date.isOtherMonth
            }"
            @click="selectDate(date)"
          >
            {{ date.day }}
          </span>
        </div>
      </div>
    </div>

    
      <!-- 新增岗位填写功能 -->
      <div class="sidebar-card position-card">
        <div class="card-header">
          <span class="header-title">填写岗位获取对应岗位试题</span>
        </div>
        <div class="position-input">
          <input 
            v-model="positionInput" 
            type="text" 
            placeholder="请输入岗位名称"
            class="position-input-field"
          >
        </div>
      </div>

      <!-- 新增难度设置功能 -->
      <div class="sidebar-card difficulty-card">
        <div class="card-header">
          <span class="header-title">试题难度设置</span>
        </div>
        <div class="difficulty-options">
          <button
            v-for="level in difficultyLevels" 
            :key="level.value" 
            class="difficulty-option"
            :class="{ active: currentDifficulty === level.value }"
            @click="setDifficulty(level.value)"
          >
             <span class="difficulty-icon" :style="{ backgroundColor: level.color }"></span>
             <span class="difficulty-label">{{ level.label }}</span>
          </button>
        </div>
      </div>
      <!-- 修改右侧功能区的按钮顺序 -->
      <div class="interview-simulation-btn" @click="submitPosition">
        <span class="btn-text">获取试题</span>
        <span class="btn-icon">📄</span>
      </div>
      <!-- 在日历卡片结束后添加 -->
     <div class="interview-simulation-btn" @click="startMockInterview">
       <span class="btn-text">前往模拟面试</span>
       <span class="btn-icon">🎤</span>
     </div>
    </div>

    <!-- 加载提示 -->
    <div v-if="generatingQA" class="loading-overlay">
      <div class="loading-content">
        <div class="spinner"></div>
        <p>正在生成面试题，请稍候...</p>
      </div>
    </div>
  </div>
</template>

<script>
import {saveAs} from "file-saver";
import {Document, Packer, Paragraph, TextRun} from "docx";
import jsPDF from "jspdf";
import {getQA, updateQA} from "@/api/interview";
import store from "@/store";
import html2canvas from 'html2canvas'

export default {
  name: 'InterviewQAPro',
  data() {
    return {
      qaList: [
       
      ],
      showAllAnswers: false,
      showAllFilters: false,
      recordingIdx: null,
      audioUrl: null,
      showExport: false,
      copiedIdx: null,
      endRecordingIdxList: [],
      mediaRecorder: null,
      audioStream: null,
      recordingTimers: {},
      playingAudios: {},
      generatingQA: false,
      hiddenButtonCount: 0,
       currentDate: new Date().getDate(),
      currentMonth: new Date().getMonth(),
      currentYear: new Date().getFullYear(),
      weekdays: ['日', '一', '二', '三', '四', '五', '六'],
      selectedDate: null,
      showMyQuestions: false, 
      myQuestions: [], 
      currentViewingRecord: null ,
      positionInput: '',
      selectedPositionTag: '',
      currentDifficulty: '初级',
      difficultyLevels: [
        { value: '初级', label: '简单', color: '#8be6c5' },
        { value: '中级', label: '中等', color: '#7ecbff' },
        { value: '高级', label: '困难', color: '#ffb366' }
      ],
    }
  },
   computed: {
    currentMonthYear() {
      return `${this.currentYear}年${this.currentMonth + 1}月`;
    },
    dates() {
      const dates = [];
      const firstDay = new Date(this.currentYear, this.currentMonth, 1);
      const lastDay = new Date(this.currentYear, this.currentMonth + 1, 0);
      const daysInMonth = lastDay.getDate();
      const startingDay = firstDay.getDay();
      
      const today = new Date();
      const isCurrentMonth = today.getFullYear() === this.currentYear && 
                            today.getMonth() === this.currentMonth;
      
      // 上个月的最后几天
      const prevMonthLastDay = new Date(this.currentYear, this.currentMonth, 0).getDate();
      for (let i = startingDay - 1; i >= 0; i--) {
        dates.push({
          day: prevMonthLastDay - i,
          isOtherMonth: true
        });
      }
      
      // 当前月的所有天
      for (let i = 1; i <= daysInMonth; i++) {
        dates.push({
          day: i,
          isCurrentDate: isCurrentMonth && i === today.getDate(),
          isOtherMonth: false
        });
      }
      
      // 下个月的前几天
      const remainingDays = 42 - dates.length; // 6行 x 7天 = 42格
      for (let i = 1; i <= remainingDays; i++) {
        dates.push({
          day: i,
          isOtherMonth: true
        });
      }
      
      return dates;
    }
  },
  methods: {
    convertQA() {
      this.showAllAnswers = !this.showAllAnswers;
      this.qaList.forEach(item => {
        item.showAnswer= this.showAllAnswers;
      })
    },
     backToFullList() {
    this.currentViewingRecord = null;
    this.fetchQuestions(); // 重新加载完整的问题列表
  },
    // 新增方法：从路由参数中获取岗位信息
    fetchPositionFromRoute() {
      if (this.$route.query.position) {
        this.positionInput = this.$route.query.position;
        // 自动触发提交
        this.submitPosition();
      }
    },
  // 新增岗位相关方法
     async submitPosition() {
       if (!this.positionInput.trim()) return;

       // const originalText = this.$el.querySelector('.position-submit-btn').textContent;
       // const submitBtn = this.$el.querySelector('.position-submit-btn');
       // submitBtn.textContent = '获取中...';
       // submitBtn.disabled = true;

       console.log('获取岗位试题:', this.positionInput);

       await this.updateQuestions();

       // submitBtn.textContent = originalText;
       // submitBtn.disabled = false;
       // this.$toast && this.$toast(`已获取${this.positionInput}相关试题`);
     },
    
    selectPositionTag(tag) {
      this.positionInput = tag;
      this.selectedPositionTag = tag;
     // this.submitPosition(); // 如果需要自动提交
    },
    
    // 新增难度设置方法
    setDifficulty(level) {
      this.currentDifficulty = level;
      console.log('设置难度:', level);
      
      // 这里可以添加根据难度筛选试题的逻辑
      this.$toast && this.$toast(`已设置为${this.difficultyLevels.find(l => l.value === level).label}难度`);
    },
  startMockInterview() {
    // 使用路由跳转到模拟面试页面
    this.$router.push('/mock-interview');
    
  },
     // 格式化时间显示
    formatTime(timestamp) {
      const date = new Date(timestamp);
      return `${date.getMonth() + 1}月${date.getDate()}日 ${date.getHours()}:${date.getMinutes().toString().padStart(2, '0')}`;
    },
    // 显示记录的试题
     showRecordedQuestion(record) {
    this.qaList = [record.questionData];
    this.showAllAnswers = false;
    this.currentViewingRecord = record.id;
  },
    
    // 从本地存储加载我的题单
    loadMyQuestions() {
      const saved = localStorage.getItem('myQuestions');
      if (saved) {
        try {
          this.myQuestions = JSON.parse(saved);
          // 添加当前查看标记
          if (this.currentViewingRecord && !this.myQuestions.some(q => q.id === this.currentViewingRecord)) {
            this.currentViewingRecord = null;
          }
        } catch (e) {
          console.error('解析我的题单数据失败', e);
          this.myQuestions = [];
        }
      }
    },
     // 新增工具方法：截取字符串前n个字符
 truncateString(str, n = 15) {
      if (!str) return '';
      
      // 尝试解码整个字符串（如果它是编码的）
      try {
        const decoded = decodeURIComponent(str);
        // 如果解码后的字符串长度小于等于n，直接返回
        if (decoded.length <= n) return decoded;
        
        // 否则安全截取并添加省略号
        return decoded.slice(0, n) + '...';
      } catch (e) {
        // 如果解码失败，处理原始字符串
        if (str.length <= n) return str;
        
        // 安全截取原始字符串（避免截断多字节字符）
        let result = '';
        let length = 0;
        for (const char of str) {
          // 简单处理多字节字符（更精确的方法需要使用TextEncoder API）
          const charLength = char.charCodeAt(0) > 127 ? 2 : 1;
          if (length + charLength > n) break;
          result += char;
          length += charLength;
        }
        return result + '...';
      }
    },

    async saveSingleQuestion(question) {
      const now = new Date();
      
      const truncatedTitle = this.truncateString(question.question, 15);
      
      const questionToSave = {
        id: `${question.id}-${now.getTime()}`,
        type: question.category || '通用',
        time: now.getTime(),
        // 保存原始题目和截取后的标题
        title: truncatedTitle,
        questionData: {...question}
      };
      
      // 添加到数组开头
      this.myQuestions.unshift(questionToSave);
      
      // 限制记录数量
      if (this.myQuestions.length > 20) {
        this.myQuestions = this.myQuestions.slice(0, 20);
      }
      
      // 保存到本地存储
      localStorage.setItem('myQuestions', JSON.stringify(this.myQuestions));
      
      // 添加视觉反馈
      this.$toast && this.$toast('已保存到我的题单');
      
      // 短暂高亮"我的题单"菜单项
      const menuItem = this.$el.querySelector('.sidebar-item.active');
      if (menuItem) {
        menuItem.style.animation = 'none';
        menuItem.offsetHeight; // 触发重绘
        menuItem.style.animation = 'highlight 1.5s';
      }
    },
// 新增删除题单记录的方法
        deleteQuestion(index) {
            this.myQuestions.splice(index, 1);
            // 保存更新后的题单到本地存储
            localStorage.setItem('myQuestions', JSON.stringify(this.myQuestions));
            // 可以在这里添加删除后的反馈，比如提示消息
            this.$toast && this.$toast('已删除题单记录');
        },
       prevMonth() {
      this.currentMonth--;
      if (this.currentMonth < 0) {
        this.currentMonth = 11;
        this.currentYear--;
      }
    },
    nextMonth() {
      this.currentMonth++;
      if (this.currentMonth > 11) {
        this.currentMonth = 0;
        this.currentYear++;
      }
    },
    selectDate(date) {
      if (date.isOtherMonth) return;
      this.selectedDate = date.day;
      // 这里可以添加选择日期后的逻辑
    },
    async fetchQuestions() {
      try {
        // this.generatingQA = true;
        await getQA(store.state.user?.username).then((res) => {
          console.log(res.data);
          if (res.status === 200) {
            this.qaList = []
            res.data.forEach(qa => {
              this.qaList.push(qa);
            })
          }
        })
        this.qaList = this.qaList.map(q => ({...q, showAnswer: false}))
        this.showAllAnswers = false
      } finally {
        // this.generatingQA = false;
      }
    },
    async updateQuestions() {
      try {
        this.generatingQA = true;
        await updateQA({
          'username':store.state.user?.username,
          'position': this.positionInput,
          'level': this.currentDifficulty
        }).then((res) => {
          console.log(res.data);
          if (res.status === 200) {
            this.qaList = []
            res.data.forEach(qa => {
              this.qaList.push(qa);
            })
          }
        })
        this.qaList = this.qaList.map(q => ({...q, showAnswer: false}))
        this.showAllAnswers = false
      } finally {
        this.generatingQA = false;
      }
    },
    
    toggleAnswer(idx) {
      this.qaList[idx].showAnswer = !this.qaList[idx].showAnswer
    },
   async startVoice(idx) {
  this.recordingIdx = idx
  this.audioUrl = null

  if (this.endRecordingIdxList.includes(idx)) {
    this.playRecording(idx);
    return;
  }

  if (this.recordingIdx !== null && this.recordingIdx !== idx) {
    this.cancelVoice();
  }
  
  try {
    this.audioStream = await navigator.mediaDevices.getUserMedia({
      audio: {
        echoCancellation: true,
        noiseSuppression: true,
        sampleRate: 44100
      }
    });

    this.mediaRecorder = new MediaRecorder(this.audioStream, {
      mimeType: MediaRecorder.isTypeSupported('audio/webm') ? 'audio/webm' : 'audio/mp4'
    });

    const audioChunks = [];

    this.mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.push(event.data);
      }
    };

    this.mediaRecorder.onstop = () => {
      const audioBlob = new Blob(audioChunks, {
        type: this.mediaRecorder.mimeType || 'audio/webm'
      });
      const audioUrl = URL.createObjectURL(audioBlob);

      this.qaList[idx]['audioBlob'] = audioBlob;
      this.qaList[idx]['audioUrl'] = audioUrl;
    };

    this.mediaRecorder.start(100);

    this.recordingTimers[idx] = {
      startTime: Date.now(),
      timer: setInterval(() => {}, 100)
    };

    console.log(`开始录音题目 ${idx + 1}`);

  } catch (error) {
    console.error('录音失败:', error);
    this.recordingIdx = null;
  }
},
    cancelVoice() {
      this.recordingIdx = null
      if (this.mediaRecorder && this.mediaRecorder.state === 'recording') {
        this.mediaRecorder.stop()
      }

      if (this.audioStream) {
        this.audioStream.getTracks().forEach(track => track.stop());
        this.audioStream = null;
      }

      Object.keys(this.recordingTimers).forEach(key => {
        if (this.recordingTimers[key].timer) {
          clearInterval(this.recordingTimers[key].timer);
          delete this.recordingTimers[key];
        }
      });

      console.log('已取消录音');
    },
    stopVoice(idx) {
      this.recordingIdx = null
      if (!this.endRecordingIdxList.includes(idx)) {
        this.endRecordingIdxList.push(idx)
        console.log(this.endRecordingIdxList)
        if (this.mediaRecorder && this.mediaRecorder.state === 'recording') {
          this.mediaRecorder.stop();
        }

        if (this.audioStream) {
          this.audioStream.getTracks().forEach(track => track.stop());
          this.audioStream = null;
        }

        if (this.recordingTimers[idx]) {
          clearInterval(this.recordingTimers[idx].timer);
          delete this.recordingTimers[idx];
        }

        console.log(`完成录音题目 ${idx + 1}`);
      } else {
        const index = this.endRecordingIdxList.indexOf(idx);

        if (index > -1) {
          this.endRecordingIdxList.splice(index, 1);
          console.log(`已删除值 ${idx}当前列表:`, this.endRecordingIdxList);
        } else {
          console.warn(`列表中未找到值: ${idx}`);
        }
        this.deleteRecording(idx);
      }
    },
    playRecording(idx) {
      const item = this.qaList[idx];
      if (!item.audioUrl) return;

      Object.keys(this.playingAudios).forEach(key => {
        if (key != idx && this.playingAudios[key]) {
          this.playingAudios[key].pause();
          this.playingAudios[key].currentTime = 0;
        }
      });

      if (this.playingAudios[idx]) {
        this.playingAudios[idx].pause();
        this.playingAudios[idx].currentTime = 0;
        delete this.playingAudios[idx];
        return;
      }

      const audio = new Audio(item.audioUrl);
      this.playingAudios[idx] = audio;

      audio.addEventListener('ended', () => {
        delete this.playingAudios[idx];
        console.log(`播放完成题目 ${idx + 1}`);
      });

      audio.addEventListener('error', (error) => {
        console.error('播放失败:', error);
        delete this.playingAudios[idx];
      });

      audio.play().then(() => {
        console.log(`开始播放题目 ${idx + 1}`);
      }).catch(error => {
        console.error('播放失败:', error);
        delete this.playingAudios[idx];
      });
      audio.addEventListener('ended', () => {
        this.recordingIdx = null
      })
    },
    deleteRecording(idx) {
      const item = this.qaList[idx];

      if (this.playingAudios[idx]) {
        this.playingAudios[idx].pause();
        delete this.playingAudios[idx];
      }

      if (item.audioUrl) {
        URL.revokeObjectURL(item.audioUrl);
        this.qaList[idx]['audioUrl'] = null;
        this.qaList[idx]['audioBlob'] = null;
      }

      console.log(`删除录音题目 ${idx + 1}`);
    },
    copyAnswer(answer, idx) {
      navigator.clipboard.writeText(answer)
      this.copiedIdx = idx
      this.$toast && this.$toast('已复制到剪贴板')
      setTimeout(() => {
        this.copiedIdx = null
      }, 2000)
    },
    async exportQuestions(type) {
      if (type === 'txt') {
        const content = this.qaList.map((q, i) =>
            `Q${i + 1}: ${q.question}\nA: ${q.answer}\n`
        ).join('\n')
        const blob = new Blob([content], {type: 'text/plain'})
        saveAs(blob, 'interview-questions.txt')
      } else if (type === 'docx') {
        const doc = new Document({
          sections: [{
            properties: {},
            children: this.qaList.flatMap((q, i) => [
              new Paragraph({
                children: [
                  new TextRun({text: `Q${i + 1}: ${q.question}`, bold: true, size: 28}),
                ],
                spacing: {after: 120}
              }),
              new Paragraph({
                children: [
                  new TextRun({text: `A: ${q.answer}`, size: 24}),
                ],
                spacing: {after: 240}
              }),
            ])
          }]
        });
        Packer.toBlob(doc).then(blob => {
          saveAs(blob, "interview-questions.docx");
        });
      } else if (type === 'pdf') {
        const element = document.createElement('div');
        element.style.cssText = `
          font-family: 'Microsoft YaHei', '微软雅黑', SimSun, sans-serif;
          padding: 20px;
          background: white;
          width: 800px;
        `;

        let content = '';
        this.qaList.forEach((q, i) => {
          content += `
          <div style="margin-bottom: 20px;">
            <h3 style="font-size: 16px; margin-bottom: 10px;">Q${i + 1}: ${q.question}</h3>
            <p style="font-size: 14px; line-height: 1.6; margin-left: 20px;">A: ${q.answer}</p>
          </div>
          `;
        });

        element.innerHTML = content;
        document.body.appendChild(element);

        const canvas = await html2canvas(element, {
          scale: 2,
          useCORS: true,
          allowTaint: true
        });

        document.body.removeChild(element);

        const imgData = canvas.toDataURL('image/png');
        const pdf = new jsPDF();
        const imgWidth = 210;
        const pageHeight = 295;
        const imgHeight = (canvas.height * imgWidth) / canvas.width;
        let heightLeft = imgHeight;
        let position = 0;

        pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
        heightLeft -= pageHeight;

        while (heightLeft >= 0) {
          position = heightLeft - imgHeight;
          pdf.addPage();
          pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
          heightLeft -= pageHeight;
        }

        pdf.save('interview-questions.pdf');
      }
      this.showExport = false;
    },
    handleClickOutside(event) {
      if (this.showExport) {
        const dropdown = this.$el.querySelector('.export-dropdown');
        if (dropdown && !dropdown.contains(event.target)) {
          this.showExport = false;
        }
      }
    },
     // 修改methods中的toggleShowAll方法
toggleShowAll() {
  this.showAllFilters = !this.showAllFilters;
  this.$nextTick(() => {
    const buttons = this.$refs.filterButtons?.querySelectorAll('.filter-btn');
    if (!buttons) return;
    
    // 默认显示9个按钮（索引0-8）
    buttons.forEach((btn, index) => {
      if (index < 9 || this.showAllFilters) {
        btn.style.display = 'inline-block';
      } else {
        btn.style.display = 'none';
      }
    });
  });
},

// 修改calculateHiddenButtons方法
calculateHiddenButtons() {
  this.$nextTick(() => {
    const buttons = this.$refs.filterButtons?.querySelectorAll('.filter-btn');
    if (!buttons) return;
    
    // 默认显示9个按钮（索引0-8）
    buttons.forEach((btn, index) => {
      if (index < 9) {
        btn.style.display = 'inline-block';
      } else {
        btn.style.display = this.showAllFilters ? 'inline-block' : 'none';
      }
    });
    
    this.hiddenButtonCount = Math.max(0, buttons.length - 9);
  });
}
  },
 mounted() {
   // 添加登录状态检查
   if (!store.state.user || !store.state.user.username) {
     this.$router.push('/login'); // 假设登录路由是/login
     return;
   }

   this.calculateHiddenButtons();
   this.loadMyQuestions();
    this.fetchPositionFromRoute();
   const style = document.createElement('style');
   style.textContent = `
     @keyframes highlight {
       0% { background-color: #e8f7f0; }
       50% { background-color: #d1f0e0; }
       100% { background-color: transparent; }
     }`;
   document.head.appendChild(style);
       
   this.loadMyQuestions();
   // 添加键盘快捷键监听，例如Ctrl+S保存当前题目
   document.addEventListener('keydown', (e) => {
     if (e.ctrlKey && e.key === 's') {
       e.preventDefault();
       this.recordCurrentQuestion();
       this.$toast && this.$toast('已保存到我的题单');
     }
   });
     const rightContainer = this.$el.querySelector('.right-scroll-container');
   
   window.addEventListener('resize', this.calculateHiddenButtons);
   this.fetchQuestions();
  
 },

  beforeDestroy() {
     window.removeEventListener('resize', this.calculateHiddenButtons);
    document.removeEventListener('click', this.handleClickOutside);
     document.removeEventListener('keydown', this.handleKeyDown);

    if (this.recordingIdx !== null) {
      this.cancelVoice();
    }

    Object.keys(this.playingAudios).forEach(key => {
      if (this.playingAudios[key]) {
        this.playingAudios[key].pause();
      }
    });

    this.qaList.forEach(item => {
      if (item.audioUrl) {
        URL.revokeObjectURL(item.audioUrl);
      }
    });

    Object.keys(this.recordingTimers).forEach(key => {
      if (this.recordingTimers[key].timer) {
        clearInterval(this.recordingTimers[key].timer);
      }
    });
  }
}
</script>

<style scoped>
/* 基础样式 */
:root {
  --primary-blue: #2dbd7f;
  --hover-blue: #e8f7f0;
  --border-color: #e0e0e0;
  --shadow-color: rgba(60, 80, 120, 0.08);
  --card-bg: #f7faf9;
  --text-primary: #333;
  --text-secondary: #666;
  --text-hint: #999;
}

html, body {
  overflow-x: hidden; /* 禁用水平滚动 */
  width: 100%;
  margin: 0;
  padding: 0;
}
* {
  margin: 0;
  padding: 0;
}

.interview-container {
  border-radius: 14px;
  display: flex;
  height: 100%;
  background: #fff;
  font-family: 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', Arial, sans-serif;
  color: var(--text-primary);
  width: 100%;
  max-width: 2660vh; /* 增大最大宽度 */
  margin: 0 auto;
  padding: 0 30px; /* 增大左右内边距 */
}


/* 左侧导航栏样式 - 修改为 sticky 定位 */
.left-sidebar {
  border-radius: 12px;
  width: 330px; /* 增大宽度 */
  background: #fff;
  padding: 20px 0;
  border-right: 1px solid #f0f0f0;
  height: 100vh;
  overflow-y: auto;
  position: sticky;
  top: 0;
  align-self: flex-start;
  margin-left: -160px; /* 增加向左移动距离 */
  transition: all 0.3s ease;
}
.sidebar-logo {
  padding: 0 20px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 16px;
  font-weight: bold;
  color: var(--text-primary);
}

.logo-icon {
  font-size: 18px;
}

.logo-text {
  font-weight: 300;
}

.sidebar-item {
  padding: 10px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  color: var(--text-primary);
  cursor: pointer;
  transition: background 0.2s;
}

.sidebar-item:hover {
  background: #f5f5f5;
}

.sidebar-item.active {
  border-left: 3px solid var(--primary-blue);
  background: var(--hover-blue);
  color: var(--primary-blue);
}

.item-icon {
  font-size: 16px;
}

.item-action {
  color: var(--text-hint);
  font-size: 12px;
}

/* 新增滚动容器样式 */
.main-scroll-container {
  flex: 1;
  min-width: 800px;
  max-width: 860px;
  height: 100vh;
  overflow-y: auto;
  margin: 0;
  padding: 24px 15px;
  box-sizing: border-box;
  scroll-behavior: smooth; /* 平滑滚动效果 */
}
/* 中间主内容区样式 */
.main-content {
   flex: 1;
  min-width: 780px; /* 增大最小宽度 */
  max-width: 860px; /* 增大最大宽度 */
  padding: 24px 30px; /* 增加内边距 */
  background: #fff;
  overflow-y: auto;
   overflow-x: hidden;
  margin: 0 15px; /* 添加左右外边距 */
}


.right-sidebar {
  border-radius: 12px;
  width: 390px;
   min-width: 390px; /* 固定宽度防止收缩 */
  overflow-x: hidden; /* 禁止水平滚动 */
  padding: 20px 15px; /* 调整内边距 */
  box-sizing: border-box;
  background: #fff;
  border-left: 1px solid #f0f0f0;
  height: 100vh;
  overflow-y: auto;
  position: sticky;
  top: 0;
  align-self: flex-start;
  margin-right: -100px; /* 向右移动以补偿容器的内边距 */
   scroll-behavior: smooth;
}
/* 顶部横幅 */
.banner-section {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.banner-card {
   flex: 1;
  min-width: 220px; /* 增大最小宽度 */
  height: 110px; /* 增高卡片 */
  border-radius: 8px;
  padding: 18px; /* 增加内边距 */
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  position: relative;
  overflow: hidden;
  transition: transform 0.2s;
}

.banner-card:hover {
  transform: translateY(-2px);
}

.banner-title {
  font-size: 16px;
  font-weight: bold;
  color: #fff;
  margin-bottom: 10px;
}

.banner-card:nth-child(2) .banner-title,
.banner-card:nth-child(3) .banner-title {
  color: #333;
}

.banner-play {
  position: absolute;
  right: 15px;
  top: 15px;
  background: #fff;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-blue);
  font-size: 12px;
  cursor: pointer;
}

.banner-subtitle {
  font-size: 14px;
  color: #fff;
}

/* 题目分类标签 */
.category-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
  overflow-x: auto;
  padding: 5px 0;
}

.tag-item {
  font-size: 13px;
  color: var(--text-secondary);
  white-space: nowrap;
  padding: 5px 0;
  cursor: pointer;
}

.tag-item:hover {
  color: var(--primary-blue);
}

.tag-item:last-child {
  color: var(--text-hint);
}

/* 筛选与搜索区域 */
.filter-section {
   display: flex;
  align-items: flex-start;
  gap: 20px;
  margin-bottom: 24px;
  padding: 18px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  position: relative;
}
.filter-container {
   display: flex;
  align-items: flex-start;
  width: 100%;
  position: relative;
  flex-wrap: wrap;
}
.filter-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap; /* 允许换行 */
  overflow: visible; /* 改为visible确保内容可见 */
  flex-grow: 1;
  min-width: 0;
  max-width: calc(100% +60px); /* 留出更多按钮的空间 */
}

.filter-btn {
   background: #f0f0f0;
  color: var(--text-secondary);
  border-radius: 20px;
  padding: 5px 15px;
  font-size: 13px;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  flex-shrink: 0;
  height: 32px;
  margin-bottom: 8px; /* 添加底部间距 */
}

.filter-btn:not(.active) {
  background: #f0f0f0;
  color: var(--text-secondary);
}

.filter-btn.active {
  background: var(--primary-blue);
  color: white;
}
.filter-more-btn {
  background: none;
  border: none;
  color: var(--text-hint);
  font-size: 12px;
  cursor: pointer;
  padding: 5px 10px;
  white-space: nowrap;
  flex-shrink: 0;
}
.filter-btn:hover:not(.active) {
  background: #e0e0e0;
}
.filter-more-btn:hover {
  color: var(--primary-blue);
}

.search-box {
  width: 100%;
  position: relative;
}

.search-icon {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-hint);
}

.search-input {
  width: 100%;
  padding: 8px 10px 8px 30px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  font-size: 13px;
  color: var(--text-primary);
  outline: none;
  transition: border 0.2s;
}

.search-input:focus {
  border-color: var(--primary-blue);
}

.sort-options {
  display: flex;
  align-items: center;
  gap: 15px;
  color: var(--text-hint);
  font-size: 13px;
}

.sort-icon {
  cursor: pointer;
  transition: color 0.2s;
}

.sort-icon:hover {
  color: var(--primary-blue);
}

.progress-text {
  color: #ff6b00;
}

/* 个性化面试试题区域 */
.personalized-section {
  width: 100%;
}

.personalized-section h2 {
  text-align: left;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  color: var(--text-primary);
  font-weight: 800;
  letter-spacing: 1px;
}

.qa-toolbar {
  display: flex;
  gap: 1.2rem;
  margin-bottom: 1.8rem;
  justify-content: flex-end;
  align-items: center;
  position: relative;
}

.toolbar-btn {
  background: var(--card-bg);
  color: var(--text-primary);
  border: 1.5px solid var(--border-color);
  border-radius: 8px;
  padding: 0.45rem 1.2rem;
  font-size: 1.08rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.4em;
  font-family: inherit;
  letter-spacing: 0.5px;
}

.toolbar-btn:hover {
  background: var(--hover-blue);
  color: var(--primary-blue);
  border-color: #b7e5d0;
}

.toolbar-btn .icon {
  font-size: 1.15em;
  margin-right: 0.2em;
}

.all-btn {
  display: inline-block !important;
}

.export-dropdown {
  position: relative;
  display: inline-block;
}

.export-menu {
  position: absolute;
  top: 110%;
  right: 0;
  background: #fff;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  box-shadow: 0 2px 8px var(--shadow-color);
  min-width: 90px;
  z-index: 10;
  animation: fadeIn 0.18s;
  overflow: hidden;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.export-item {
  padding: 0.6em 1.2em;
  color: var(--text-primary);
  cursor: pointer;
  font-size: 1.05rem;
  font-weight: 600;
  font-family: inherit;
  transition: all 0.2s;
  letter-spacing: 0.5px;
}

.export-item:hover {
  background: var(--hover-blue);
  color: var(--primary-blue);
}

/* 题目卡片样式 */
.qa-card {
     display: flex;
    flex-direction: column;
    background: #fff;
    border-radius: 16px;
    padding: 2rem 2.2rem;
    margin-bottom: 2rem;
    box-shadow: 0 2px 12px rgba(60, 180, 120, 0.08);
    transition: all 0.3s ease;
    border: 1px solid #f2f2f2;
}

.qa-card:hover {
  box-shadow: 0 2px 12px var(--shadow-color);
}

.qa-card:not(:last-child) {
  margin-bottom: 1.5rem;
}

.qa-header {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  margin-bottom: 0.7rem;
  flex-wrap: wrap;
}

.qa-index {
  background: var(--card-bg);
  color: var(--text-primary);
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  font-size: 1.15rem;
  flex-shrink: 0;
}

.qa-tag {
  background: var(--card-bg);
  color: var(--text-primary);
  border-radius: 999px;
  padding: 0.2em 1.2em;
  font-size: 0.92rem;
  font-weight: 500;
  letter-spacing: 0.5px;
  margin-right: 0.5rem;
}

.qa-level {
  border-radius: 999px;
  padding: 0.15em 1.1em;
  font-size: 0.92rem;
  font-weight: 500;
  color: #fff;
  letter-spacing: 0.5px;
  display: inline-block;
  line-height: 1.7;
  min-width: 0;
}

.qa-level.难 {
  background: #ffb366;
}

.qa-level.中等 {
  background: #7ecbff;
}

.qa-level.简单 {
  background: #8be6c5;
}

.qa-question {
 font-size: 1.25rem; /* 增大字体 */
  margin: 1.2rem 0; /* 增加间距 */
  color: var(--text-primary);
  font-weight: 500;
  line-height: 1.8; /* 增加行高 */
}

.qa-actions {
  display: flex;
  gap: 1.1rem;
  margin: 1rem 0;
  flex-wrap: wrap;
}

.qa-btn {
  background: #fff;
  color: var(--text-primary);
  border: 1.5px solid var(--border-color);
  border-radius: 8px;
  padding: 0.32rem 1.1rem;
  font-size: 0.92rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 1px 4px 0 rgba(66, 185, 131, 0.04);
  letter-spacing: 0.5px;
  position: relative;
  overflow: hidden;
  display: inline-flex;
  align-items: center;
  gap: 0.5em;
}

.qa-btn:hover {
  background: var(--hover-blue);
  color: var(--primary-blue);
  border-color: #b7e5d0;
}

.qa-btn.wave-anim {
  color: var(--primary-blue);
  border-color: #8be6c5;
}

.voice-wave {
  display: inline-flex;
  align-items: flex-end;
  margin-left: 0.5em;
  height: 1em;
}

.voice-wave .dot {
  display: inline-block;
  width: 0.22em;
  height: 0.5em;
  margin: 0 0.08em;
  background: #7ed6a5;
  border-radius: 2px;
  animation: waveDot 1s infinite;
}

.voice-wave .dot:nth-child(2) {
  animation-delay: 0.2s;
}

.voice-wave .dot:nth-child(3) {
  animation-delay: 0.4s;
}

.voice-wave .dot:nth-child(4) {
  animation-delay: 0.6s;
}

@keyframes waveDot {
  0%, 100% {
    height: 0.5em;
  }
  50% {
    height: 1em;
  }
}

.qa-answer {
  background: var(--card-bg);
  border-radius: 8px;
  padding: 0.9rem 1.2rem;
  color: var(--text-primary);
  margin: 1rem 0;
  font-size: 1.08rem;
  line-height: 1.7;
  box-shadow: 0 1px 4px 0 rgba(66, 185, 131, 0.04);
}

.answer-label {
  color: var(--primary-blue);
  font-weight: bold;
  margin-right: 0.5rem;
}

.qa-voice {
  margin-top: 0.7rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.voice-bar {
  width: 120px;
  height: 18px;
  background: linear-gradient(90deg, #8be6c5 60%, #7ecbff 100%);
  border-radius: 8px;
  animation: voice-bar 1.2s infinite linear;
}

@keyframes voice-bar {
  0% {
    opacity: 0.5;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0.5;
  }
}

/* 新增内容区容器样式 */
.content-wrapper {
  display: flex;
  flex: 1;
  overflow: hidden;
}
/* 右侧功能区样式 */
.sidebar-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px var(--shadow-color);
  padding: 14px;
  margin-bottom: 10px;
    width: 100%; 
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.header-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.header-action {
  font-size: 12px;
  color: var(--text-hint);
  cursor: pointer;
}

.date-badge {
  background: var(--primary-blue);
  color: white;
  width: 26px;
  height: 24px;
  border-radius: 60%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: bold;
}

.calendar-grid {
   margin-top: 12px;
  border: 1.5px solid #e0e0e0;
  border-radius: 12px;
  padding: 12px;
  background: #f9f9f9;
  width: 90%; /* 确保日历填满父容器 */
}

.weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
  margin-bottom: 8px;
}

.weekdays span {
  font-size: 10px;
  color: var(--text-hint);
  text-align: center;
}

.dates {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}

.dates span {
  font-size: 12px;
  color: var(--text-hint);
  text-align: center;
  padding: 4px 0;
  cursor: pointer;
}

.dates span.current-date {
  background: linear-gradient(135deg, #2dbd7f 0%, #1a9e65 100%);
  color: white;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 14px;
  line-height: 1.4;
  letter-spacing: 0.5px;
  position: relative;
  top: -2px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 可选：增加阴影增强立体感 */
}
@keyframes pulse {
  0% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(45, 189, 127, 0.4);
  }
  70% {
    transform: scale(1.05);
    box-shadow: 0 0 0 6px rgba(45, 189, 127, 0);
  }
  100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(45, 189, 127, 0);
  }
}
.week-progress {
  display: flex;
  gap: 8px;
  margin: 16px 0;
  justify-content: center;
}

.week-tag {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 1px solid var(--primary-blue);
  color: var(--primary-blue);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  cursor: pointer;
}

.week-tag.completed {
  background: var(--primary-blue);
  color: white;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: var(--text-hint);
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}

.company-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}

.company-tag {
  font-size: 12px;
  color: var(--text-secondary);
  padding: 4px 8px;
  background: #f5f5f5;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.company-tag:hover {
  background: var(--hover-blue);
  color: var(--primary-blue);
}

/* 加载动画 */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.loading-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid var(--primary-blue);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}
.filter-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 15px 0 0;
  padding: 5px 0;
  white-space: nowrap;
  flex-shrink: 0;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 响应式设计调整 */
@media (max-width: 1400px) {
  .interview-container {
    padding-left: 40px;
  }
  .left-sidebar {
    margin-left: -40px;
  }
  .right-sidebar {
    margin-right: -40px;
  }
  .main-content {
    min-width: 600px;
  }
}

@media (max-width: 1200px) {
  .interview-container {
    padding-left: 20px;
  }
  .left-sidebar {
    margin-left: -20px;
  }
  .right-sidebar {
    margin-right: -20px;
  }
  .main-content {
    min-width: 500px;
  }
}

@media (max-width: 992px) {
  .interview-container {
    padding-left: 0;
  }
  .left-sidebar {
    margin-left: 0;
  }
  .right-sidebar {
    display: none;
  }
  .main-content {
    min-width: auto;
    max-width: 100%;
  }
}
.calendar-nav {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-btn {
  background: none;
  border: none;
  color: var(--text-hint);
  font-size: 14px;
  cursor: pointer;
  padding: 2px 6px;
  border-radius: 4px;
}

.nav-btn:hover {
  background: #f0f0f0;
  color: var(--primary-blue);
}

.current-month {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-primary);
  min-width: 80px;
  text-align: center;
}

.dates span {
  font-size: 12px;
  color: var(--text-hint);
  text-align: center;
  padding: 4px 0;
  cursor: pointer;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}

.dates span.other-month {
  color: #ccc;
}

.dates span.current-date {
  background: linear-gradient(135deg, #2dbd7f 0%, #1a9e65 100%);
  color: white;
  font-weight: bold;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.dates span:hover:not(.other-month) {
  background: #f0f0f0;
  color: var(--primary-blue);
}
/* 我的题单样式 */
.my-questions-list {
  margin-top: 8px;
  border-top: 1px solid #f0f0f0;
  padding-top: 8px;
   font-weight: 600; 
}

.my-question-item {
  padding: 12px 20px 12px 40px;
  font-size: 17px;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 4px;
  transition: all 0.2s;
  position: relative;
  line-height: 1.5; /* 增加行高 */
  font-weight: 400; 
}

.my-question-item:hover {
  background: var(--hover-blue);
  color: var(--primary-blue);
}

.my-question-item::before {
  content: "•";
  position: absolute;
  left: 25px;
  color: var(--text-hint);
}

.record-type {
  font-weight: 500;
}

.record-time {
  font-size: 12px;
  color: var(--text-hint);
}

/* 当前查看的记录高亮 */
.my-question-item.current {
  background: var(--hover-blue);
  color: var(--primary-blue);
  border-left: 3px solid var(--primary-blue);
  padding-left: 37px;
}

.my-question-item.current .record-time {
  color: var(--primary-blue);
}
/* 新增删除按钮样式 */
.delete-btn {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-40%);
    background: #8be6c5;
    border: none;
    color: #dd1d20;
    font-size: 16px;
    cursor: pointer;
    padding: 0 5px;
    display: none;
}

.my-question-item:hover .delete-btn {
    display: block;
}

.delete-btn:hover {
    color: #3dcd9f;
}
/* 添加在日历相关样式后面 */
.interview-simulation-btn {
  margin-top: 16px;
  padding: 12px 16px;
  background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 99%, #fad0c4 100%);
  border-radius: 50px 12px 12px 50px;
  color: #fff;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(250, 208, 196, 0.4);
  position: relative;
  overflow: hidden;
  border: 2px solid #fff;
}
.interview-simulation-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(250, 208, 196, 0.6);
  background: linear-gradient(135deg, #ff8a8e 0%, #f9c0b4 99%, #f9c0b4 100%);
}

.interview-simulation-btn:active {
  transform: translateY(0);
}

.btn-text {
  font-size: 16px;
  letter-spacing: 1px;
  text-shadow: 0 1px 2px rgba(0,0,0,0.1);
  z-index: 2;
}

.btn-icon {
  font-size: 20px;
  background: rgba(255,255,255,0.3);
  padding: 8px;
  border-radius: 50%;
  z-index: 2;
}

.interview-simulation-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    120deg,
    transparent,
    rgba(255,255,255,0.3),
    transparent
  );
  transition: all 0.5s;
  z-index: 1;
}

.interview-simulation-btn:hover::before {
  left: 100%;
}
/* 新增岗位填写功能样式 */
.position-card {
  margin-top: 16px;
}

.position-input {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.position-input-field {
  width: 90%; /* 宽度填满父容器 */
  min-width: 250px; /* 设置最小宽度 */
  padding: 12px 15px; /* 增加内边距使输入框更高 */
  font-size: 14px; /* 增大字体大小 */
  border: 1.8px solid #e0e0e0; 
  border-radius: 8px; /* 圆角 */
  transition: all 0.3s ease; 
  box-sizing: border-box; 
}

.position-input-field:focus {
  border-color: var(--primary-blue);
}

.position-submit-btn {
  padding: 8px 16px;
  background: var(--primary-blue);
  color: rgb(27, 27, 27);
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.position-submit-btn:hover {
  background: #1a9e65;
}

.position-submit-btn:disabled {
  background: #8be6c5;
  cursor: not-allowed;
}

.position-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.position-tag {
  padding: 6px 12px;
  background: #f5f5f5;
  border-radius: 20px;
  font-size: 13px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
}

.position-tag:hover {
  background: var(--hover-blue);
  color: var(--primary-blue);
}

/* 新增难度设置功能样式 - 优化版 */
.difficulty-card {
  margin-top: 8px;
  padding: 12px;
}

.difficulty-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.difficulty-option {
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  border: 1.5px solid #f0f0f0;
}

.difficulty-option:hover {
  background: var(--hover-blue);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(60, 180, 120, 0.1);
}

.difficulty-option.active {
  background: linear-gradient(135deg, #e8f7f0 0%, #d1f0e0 100%);
  color: var(--primary-blue);
  border-color: #8be6c5;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(60, 180, 120, 0.15);
}

.difficulty-option.active::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: var(--primary-blue);
}

.difficulty-icon {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  display: inline-block;
  transition: all 0.3s ease;
  position: relative;
}

.difficulty-icon::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) scale(0);
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(45, 189, 127, 0.2);
  transition: transform 0.3s ease;
}

.difficulty-option.active .difficulty-icon::after {
  transform: translate(-50%, -50%) scale(1);
}

.difficulty-label {
  font-size: 14px;
  letter-spacing: 0.5px;
  position: relative;
  z-index: 1;
}

/* 添加平滑过渡动画 */
.difficulty-option {
  animation: fadeInUp 0.4s ease forwards;
  opacity: 0;
  transform: translateY(10px);
}

.difficulty-option:nth-child(1) { animation-delay: 0.1s; }
.difficulty-option:nth-child(2) { animation-delay: 0.2s; }
.difficulty-option:nth-child(3) { animation-delay: 0.3s; }
.difficulty-option:nth-child(4) { animation-delay: 0.4s; }

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
/* 返回按钮样式 */
.back-btn {
  background: var(--card-bg);
  color: var(--primary-blue);
  border: 1px solid var(--primary-blue);
  margin-bottom: 1rem;
  display: inline-flex;
  align-items: center;
  padding: 0.4rem 1rem;
  order: 2; /* 调整顺序 */
  align-self: flex-end; 
}

.back-btn:hover {
  background: var(--primary-blue);
  color: #8be6c5;
}

.back-btn .icon {
  margin-right: 0.5rem;
}
</style>