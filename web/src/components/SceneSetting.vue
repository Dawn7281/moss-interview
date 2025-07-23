<!-- filepath: d:\Project\SoftworkCup\front-6-16\src\components\SceneSetting.vue -->
<template>
  
  <div class="scene-setting">
  
    <template v-if="step === 'select'">
        <ProfileForm />
      <!-- 只在选择阶段显示类型和压力设置 -->
      <div class="setting-row">
        <InterviewTypeSetting />
        <PressureSetting />
      </div>
      <h2>🧭 请选择你要体验的面试场景：</h2>
      <div class="scene-cards">
        <div
          v-for="item in sceneOptions"
          :key="item.value"
          :class="['scene-card', {active: sceneMode === item.value}]"
          @click="sceneMode = item.value"
        >
          <div class="scene-icon">{{ item.icon }}</div>
          <div class="scene-title">{{ item.title }}</div>
          <div class="scene-desc" v-for="desc in item.desc" :key="desc">{{ desc }}</div>
          <button
            class="select-btn"
            :class="{selected: sceneMode === item.value}"
            @click.stop="sceneMode = item.value"
          >{{ sceneMode === item.value ? '已选择' : '选择' }}</button>
        </div>
      </div>
      <div class="scene-actions">
        <button class="confirm-btn" @click="startInterview">🚀 开始模拟面试</button>
      </div>
    </template>

<!-- 修改文本模拟部分的结构 -->
<template v-else-if="sceneMode === 'text'">
  <!-- 文本模拟：分屏布局 -->
  <div class="text-interview-container">
    <!-- 左侧：历史记录侧边栏 -->
    <InterviewSidebar @load="loadChatHistory" />
    
    <!-- 中间：文本交互界面 -->
    <div class="chat-interview">
      <div class="chat-header">📝 文本模拟面试 <button class="back-btn" @click="reset">返回</button></div>
      <div class="chat-body" ref="chatBodyRef">
        <div v-for="(msg, idx) in chatList" :key="idx" :class="['chat-msg', msg.role]">
          <span class="avatar">{{ msg.role === 'ai' ? '🤖' : '🧑' }}</span>
          <span class="bubble">{{ msg.text }}</span>
        </div>
      </div>
      <div class="chat-input">
        <input v-model="userInput" @keyup.enter="sendMsg" placeholder="请输入你的回答..." />
        <button @click="sendMsg">发送</button>
      </div>

      <!-- 生成报告按钮 -->
      <div class="generate-report-container">
        <button class="generate-report-btn" @click="generateTextReport">
          📊 生成面试报告
        </button>
      </div>
    </div>

  </div>
</template>

<!-- 修改audio-interview部分 -->
<template v-else-if="sceneMode === 'audio'">
  <!-- 语音模拟：分屏布局 -->
  <div class="audio-interview-container">

    <!-- 左侧：语音选择侧边栏 -->
<div class="audio-history-panel">
  <h3>语音风格选择</h3>
  <ul class="voice-style-list">
    <li 
      v-for="(style, index) in voiceStyles" 
      :key="index"
      class="voice-style-item"
      :class="{ 'active': selectedVoiceStyle === style.value }"
      @click="selectVoiceStyle(style.value)"
    >
      <span class="style-icon">{{ style.icon }}</span>
      <span class="style-name">{{ style.name }}</span>
    </li>
  </ul>
</div>
    
    <!-- 中间：语音交互界面 -->
    <div class="audio-interview">
      <div class="audio-header">🎙️ 语音模拟面试 <button class="back-btn" @click="reset">返回</button></div>
      <div class="audio-body">
        <div class="audio-avatar">🎧</div>
        <div class="audio-tip">
         <!-- 动态语音波动图 - 始终动画 -->
         <div class="voice-wave-container">
  <div class="voice-wave" 
       v-for="(bar, index) in voiceWaveBars" 
       :key="index" 
       :style="{
         height: `${bar.height}px`, 
         backgroundColor: bar.color,
         animationDelay: `${index * 0.05}s`
       }"></div>
</div>
       </div>
      </div>
      <div class="audio-actions">
        <button 
          class="audio-btn" 
          @click="toggleAudioRecording"
          :style="{ backgroundColor: isAudioRecording ? '#f59694' : '#3dcd9f' }"
        >
          {{ isAudioRecording ? '⏹️ 结束语音面试' : '🎤 开始语音面试' }}
        </button>
        <button 
          class="audio-btn report-btn"
          @click="confirmGenerateFeedback"
          :disabled="!recordedBlob"
        >
          📄 生成面试报告
        </button>
      </div>
    </div>
  </div>
</template>

    <template v-else-if="sceneMode === 'video'">
      <!-- 视频模拟：分屏+摄像头流 -->
      <div class="video-interview-area-inner">
        <EmotionFeedback :current-time="interviewTime" :emotions="emotionData"/>

        <div class="video-toolbar">
          <button v-if="!videoStarted" class="video-btn" @click="startVideo">接通视频</button>
          <button v-if="videoStarted" class="video-btn end" @click="endVideo">结束视频</button>
          <button v-if="!videoInterviewStarted" class="video-btn" @click="startVideoInterview">开始面试</button>
          <button v-if="videoInterviewStarted" class="video-btn end" @click.stop="showStopConfirm">结束面试</button>
          <button class="video-btn" @click="showFeedbackConfirm">生成反馈</button>
          <input type="file" accept="image/*" @change="onInterviewerImg" class="upload-input" title="上传面试官头像" />
          <button class="back-btn" @click="reset">返回</button>
        </div>
        
        <div class="video-split-row-inner">
          <!-- 左侧：面试官 -->
          <div class="video-half-inner left">
            <div class="video-rect-inner">
              <img v-if="interviewerImg" :src="interviewerImg" alt="面试官" class="video-img-inner" />
              <div v-else class="virtual-ai-rect-inner">
<!--                <div class="ai-icon">🤖</div>-->
<!--                <div class="ai-label">虚拟面试官</div>-->
                <div id="wrapper"></div>
              </div>
            </div>
          </div>
          <!-- 右侧：面试人 -->
          <div class="video-half-inner right">
            <div class="video-rect-inner">
              <video
                v-if="videoStarted && userStream"
                ref="userVideo"
                autoplay
                muted
                playsinline
                class="video-img-inner"
              ></video>
              <div v-else class="virtual-ai-rect-inner self-black"></div>
            </div>
          </div>
        </div>
<div class="video-interview-area-inner">

  <!-- 生成反馈确认对话框 -->
  <div v-if="showGenerateConfirm" class="confirm-dialog">
    <div class="dialog-content">
      <h3>确认生成报告</h3>
      <p>是否确定要生成面试评估报告？</p>
      <div class="dialog-actions">
        <button class="dialog-btn cancel" @click="showGenerateConfirm = false">取消</button>
        <button class="dialog-btn confirm" @click="confirmGenerateFeedback">确定</button>
      </div>
    </div>
  </div>

  <!-- 结束面试确认对话框 -->
  <div v-if="showEndConfirm" class="confirm-dialog">
    <div class="dialog-content">
      <h3>确认结束面试</h3>
      <p>是否确定要结束当前面试？</p>
      <div class="dialog-actions">
        <button class="dialog-btn cancel" @click="showEndConfirm = false">取消</button>
        <button class="dialog-btn confirm" @click="confirmStopInterview">确定</button>
      </div>
     </div>
    </div>
  </div>
     </div>
    </template>
<!--    <InterviewReport -->
<!--      v-if="showReport"-->
<!--      :report-data="reportData"-->
<!--      @close="showReport = false"-->
<!--    />-->

    <template>
      <!-- 在text-interview-container中添加侧边栏 -->
      <div class="text-interview-container">
        <InterviewSidebar />
    
        <!-- 左侧：文本交互界面 -->
        <div class="chat-interview">
          <!-- 原有聊天界面内容保持不变 -->
        </div>
    
        <!-- 右侧：个人信息编辑面板 -->
        <div class="profile-toggle-container">
          <!-- 原有个人信息面板内容保持不变 -->
        </div>
      </div>
    </template>

    <InterviewReport 
    v-if="showReport"
    :report-data="reportData"
    @close="showReport = false"
    @save="saveReportToHistory"
  />
  
  <!-- 保存成功提示 -->
  <div v-if="showSaveSuccess" class="save-success-message">
    报告已成功保存到历史记录
  </div>

    <!-- 添加加载提示 -->
    <div v-if="generatingReport" class="loading-overlay">
      <div class="loading-content">
      <div class="spinner"></div>
      <p>正在生成报告，请稍候...</p>
    </div>
    </div>
  </div>
  
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import {
  getBase64,
  initBot,
  txtChart,
  videoChart,
  uploadMedia,
  handleSentiments,
  fetchFrame,
  textAnalyze,
  updateVCN,
  endSentiments
} from "@/api/interview";
import store from "@/store";
import EmotionFeedback from './EmotionFeedback.vue'
import InterviewReport from './InterviewReport.vue'
import { useRouter } from 'vue-router'

import InterviewTypeSetting from './InterviewTypeSetting.vue'
import PressureSetting from './PressureSetting.vue'
import ProfileEditPanel from './ProfileEditPanel.vue'
import InterviewSidebar from './InterviewSidebar.vue'
import ProfileForm from './ProfileForm.vue' 

import AvatarPlatform, {
  PlayerEvents,
  SDKEvents,
} from "@/vm-sdk/avatar-sdk-web_3.1.1.1011/index.js";
import {getJobInfo, getUserInfo} from "@/api/user";

const endAnalyze = ref(false);
const postAnalyze = ref({});
const currentPlayingQuestion = ref("")

let avatarPlatform2 = null;

const form = {
   appid: import.meta.env.VITE_APPID,
  apikey: import.meta.env.VITE_APIKEY,
  apisecret: import.meta.env.VITE_APISECRET,
  sceneid: import.meta.env.VITE_SCENEID,
  serverurl: "wss://avatar.cn-huadong-1.xf-yun.com/v1/interact"
}

const setglobalparamsform = {
  stream: {
    protocol: "xrtc",//（必传）实时视频协议，支持webrtc/xrtc/rtmp，其中只有xrtc支持透明背景，需参数alpha传1
    fps: 25,//（非必传）视频刷新率,值越大，越流畅，取值范围0-25，默认25即可
    bitrate: 1000000,//（非必传）视频码率，值越大，越清晰，对网络要求越高，默认1000000即可
    alpha: false,//（非必传）是否开启透明背景，0关闭1开始，需配合protocol=xrtc使用
  },
  avatar: {
    avatar_id: "110117005",//（必传）授权的形象资源id，请到交互平台-接口服务-形象列表中获取
    width: 1080,//（非必传）视频分辨率宽（不是画布的宽，调整画布大小需调整名为wrapper的div宽）
    height: 960,//（非必传）视频分辨率高（不是画布的高，调整画布大小需调整名为wrapper的div高）
    mask_region: "[0,0,1080,1080]",//（非必传）形象裁剪参数，[从左到右，从上到下，从右到左，从下到上]
    scale: 1,//（非必传）形象缩放比例，取值范围0.1-1
    move_h: 0,//（非必传）形象左右移动
    move_v: 0,//（非必传）形象上下移动
    audio_format: 1,//（非必传）音频采样率，传1即可
  },
  tts: {
    vcn: "x4_lingxiaoyue_oral",//（必传）授权的声音资源id，请到交互平台-接口服务-声音列表中获取
    speed: 50,//（非必传）语速
    pitch: 50,//（非必传）语调
    volume: 100,//（非必传）音量
    emotion:13,//（非必传）情感系数，仅带有情感能力的超拟人音色支持该能力，普通音色不支持
  },
  avatar_dispatch: {
    interactive_mode: 1,//（非必传）0追加模式，1打断模式
  },
  subtitle:{
    subtitle:0,
    font_color:"#FFFFFF",
    font_name:"Sanji.Suxian.Simple",
   
    position_x:100,
    position_y:0,
    font_size:10,
    width:100,
    height:100,
  },
  enable:true,
  background: {
    type: "res_key",//（非必传）上传图片的类型，支持url以及res_key。（res_key请到交互平台-素材管理-背景中上传获取)
    data: import.meta.env.VITE_RES_KEY //（非必传）图片的值，当type='url'时,data='http://xxx/xxx.png'，当type='res_key'时，data='res_key值'（res_key请到交互平台-素材管理-背景中上传获取)
  }
}

function initAvatar() {
  //必须先实例化SDK，再去调用其挂载的方法
  avatarPlatform2 = new AvatarPlatform();
  if (avatarPlatform2 != null) {
    console.log("实例化SDK成功");
  }
}

function onEvents() {
  if (avatarPlatform2 != null) {
    avatarPlatform2.on(SDKEvents.frame_stop, function () {
      console.log('-------------------on')
      if (videoInterviewStarted.value){
        // speechNumber += 1
        if (!endInterview.value){
          startRecording()
        } else {
          stopVideoInterview()
          endInterview.value = false
          //   speechNumber = 0
        }
      }
      else {
        stopVideoInterview()
      }
      // if (sceneMode.value === 'audio') {
      //
      // }
    })
  }
}

function avatarPlay(text) {
  if (avatarPlatform2) {
    avatarPlatform2.writeText(text, {
      nlp: false,
      tts: {
        emotion: getEmotionValue(selectedVoiceStyle.value),
        volume: 100,
      },
    })
  }
}

function SetApiInfo2() {
  if (avatarPlatform2 == null) {
    console.log("请先实例化SDK");
  } else {
    console.log("设置setApiInfo");
    const params = {
      appId: form.appid,
      apiKey: form.apikey,
      apiSecret: form.apisecret,
      serverUrl: form.serverurl,
      sceneId: form.sceneid,
    };
    console.log("初始化SDK信息：", params);
    //初始化SDK
    avatarPlatform2.setApiInfo(params);
    console.log("初始化SDK成功");
  }
}

function SetGlobalParams() {
  if (avatarPlatform2 != null) {
    let params = Object.assign({}, setglobalparamsform);
    console.log("setglobalparamsform.stream.alpha",setglobalparamsform.stream.alpha)
    if(setglobalparamsform.enable == false){
      delete params.background;
      delete params.enable;
    }
    console.log("setglobalparamsform",setglobalparamsform)
    if(setglobalparamsform.stream.alpha == true){
      console.log("设置alpha=1")
      params.stream.alpha = 1
    }else{
      console.log("设置alpha=0")
      params.stream.alpha = 0
    }
    console.log("设置的全局变量为：",params);
    avatarPlatform2.setGlobalParams(params);
    console.log("设置全局变量成功")
  } else {
    console.log("请先实例化SDK");
  }
}

function startAvatar() {
  if(avatarPlatform2!=null){
    avatarPlatform2
        .start({ wrapper: document.querySelector("#wrapper") })
        .catch((e) => {
          console.error(e.code, e.message, e.name, e.stack);
        });
  }else{
    console.log("请先实例化SDK")
  }
}

function destroyAvatar() {
  if(avatarPlatform2 != null){
    //销毁SDK示例，内部包含stop协议，重启需重新示例化avatarPlatform实例
    avatarPlatform2.destroy();
    avatarPlatform2 = null;
  }else {
    console.log("请先实例化SDK")
  }
}


const router = useRouter()
const showReport = ref(false)
const reportData = ref(null)
const generatingReport = ref(false)

const step = ref('select')
const sceneMode = ref('text')
const isPaused = ref(false)
const showEndConfirm = ref(false)
const showSaveSuccess = ref(false)
const showSetting = ref(true) // true 时显示类型和压力设置
const showProfilePanel = ref(false)


const profileData = ref({
  basicInfo: {
    realname: '姓名',
    nickname: '用户昵称',
    gender: '男',
    bio: '个人简介',
    location: '北京',
    graduationYear: 2023,
    education: '本科',
    university: '某某大学',
    major: '计算机科学'
  },
  jobExpectation: {
    position: '前端开发工程师',
    jobRequirements: '岗位要求',
    status: '在职，考虑新机会',
    salaryRange: '15k - 20k',
    workLocation: '北京'
  }
})
const completionRate = ref(75)

const sceneOptions = [
  {
    value: 'text',
    icon: '📝',
    title: '文本模拟',
    desc: ['💬 聊天框风格，对话式提问', '✏️ 锻炼文字组织表达能力']
  },
  {
    value: 'audio',
    icon: '🎙️',
    title: '语音模拟',
    desc: ['🎧 听语音提问，语音回答', '🗣️ 训练语速与语调']
  },
  {
    value: 'video',
    icon: '🎥',
    title: '视频模拟',
    desc: ['🎭 AI 视频面试官出镜', '📸 摄像头录你回答过程']
  }
]

const text =ref('请简要介绍一下你自己。')

// 文本模拟面试
const chatList = ref([
  { role: 'ai', text: '欢迎来到模拟面试，请简单自我介绍一下。' }
])
const userInput = ref('')
const chatBodyRef = ref(null)
// 语音风格选项
const voiceStyles = ref([
  { value: "x4_yezi", name: '严肃正式', icon: '🎩' },
  { value: "x4_xiaoyan", name: '亲切温柔', icon: '🌷' },
  { value: 3, name: '幽默风趣', icon: '😂' },
  { value: 4, name: '积极正向', icon: '🌟' },
  { value: 5, name: '冷酷批评', icon: '❄️' },
  { value: 6, name: '挑剔质问', icon: '❓' }
])
const selectedVoiceStyle = ref("x4_yezi") // 默认选择严肃正式


// 加载历史聊天记录
const loadChatHistory = (historyItem) => {
  chatList.value = historyItem.messages
  nextTick(() => {
    if (chatBodyRef.value) {
      chatBodyRef.value.scrollTop = chatBodyRef.value.scrollHeight
    }
  })
}


async function sendMsg() {
  if (!userInput.value.trim()) return
  chatList.value.push({role: 'user', text: userInput.value})
  const input = userInput.value
  userInput.value = '' // 先清空输入框
  await nextTick()
  if (chatBodyRef.value) {
    chatBodyRef.value.scrollTop = chatBodyRef.value.scrollHeight
  }
  const res = await txtChart({text: input, 'username': store.state.user?.username})
  if (res.status === 200) {
    chatList.value.push({ role: 'ai', text: res.data.reply })
    textAnalyze({'username': store.state.user?.username})
  }
  else {
    chatList.value.push({ role: 'ai', text: '请求失败，请重试' })
  }
  await nextTick()
  if (chatBodyRef.value) {
    chatBodyRef.value.scrollTop = chatBodyRef.value.scrollHeight
  }
  
  // 新增：每次对话后自动保存
  if (sceneMode.value === 'text') {
    saveTextHistory()
  }
}

// 保存文本模拟历史

const saveTextHistory = () => {
  if (chatList.value.length === 0 || !store.state.user?.username) return;
  
  const historyItem = {
    timestamp: new Date().toISOString(),
    username: store.state.user.username, // 保存用户名
    scene: '文本模拟面试',
    mode: profileData.value.jobExpectation.position || '通用面试',
    messages: [...chatList.value]
  }
  
  const history = JSON.parse(localStorage.getItem('textInterviewHistory') || '[]')
  // 只保留当前用户的历史记录
  const filteredHistory = history.filter(
    item => item.username !== store.state.user.username
  )
  filteredHistory.unshift(historyItem)
  localStorage.setItem('textInterviewHistory', JSON.stringify(filteredHistory))
}

// 替换原来的两个reset函数，保留这个合并后的版本
const reset = () => {
  if (sceneMode.value === 'text' && chatList.value.length > 1) {
    saveTextHistory()
  }
  step.value = 'select'
  
  // 如果是视频模式，停止所有相关资源
  if (sceneMode.value === 'video') {
    stopVideoInterview()
  }
  
  // 重置其他必要状态
  chatList.value = [{ role: 'ai', text: '欢迎来到模拟面试，请简单自我介绍一下。' }]
  userInput.value = ''
}

// 选择语音风格
function selectVoiceStyle(style) {
  selectedVoiceStyle.value = style
  console.log(style)
  updateVCN({'vcn': selectedVoiceStyle.value, 'username': store.state.user?.username})
  // 根据选择的风格更新虚拟人语音参数
  // updateVoiceParameters(style)
}

// 更新语音参数
function updateVoiceParameters(style) {
  if (avatarPlatform2) {
    const params = {
      tts: {
        ...setglobalparamsform.tts,
        emotion: getEmotionValue(style)
      }
    }
    avatarPlatform2.setGlobalParams(params)
  }
}

// 获取对应情感值
function getEmotionValue(style) {
  const emotionMap = {
    1: 13, // 严肃正式
    2: 10, // 亲切温柔
    3: 16, // 幽默风趣
    4: 14, // 积极正向
    5: 17, // 冷酷批评
    6: 18  // 挑剔质问
  }
  return emotionMap[style] || 13 // 默认严肃正式
}

async function generateTextReport() {
  showGenerateConfirm.value = false
  generatingReport.value = true

  try {
    router.push({
      name: 'InterviewReport',
      state: {
        type: sceneMode.value,
      }
    })
  } catch (error) {
    console.error('生成报告失败:', error)
    alert(`生成报告失败: ${error.message}`)
  } finally {
    generatingReport.value = false
  }
  // generatingReport.value = true;
  // try {
  //   // 这里可以调用API生成报告
  //   reportData.value = {
  //     type: 'text',
  //     messages: chatList.value,
  //     profile: profileData.value
  //   };
  //   showReport.value = true;
  // } catch (error) {
  //   console.error('生成报告失败:', error);
  // } finally {
  //   generatingReport.value = false;
  // }
}

// 在script部分修改
const voiceWaveBars = ref([])
let waveAnimationId = null

// 初始化语音波动图
function initVoiceWave() {
  const bars = []
  const colors = ['#42b983', '#3dcd9f', '#369f6b', '#2b7a78']
  for (let i = 0; i < 40; i++) {
    bars.push({
      height: Math.random() * 20 + 5,
      color: colors[Math.floor(Math.random() * colors.length)]
    })
  }
  voiceWaveBars.value = bars
}

// 持续更新语音波动图
function startWaveAnimation() {
  const now = Date.now();
  voiceWaveBars.value.forEach((bar, index) => {
    // 基础波动 + 音量影响
    const baseWave = Math.sin(now/300 + index*0.2) * 10;
    const volumeEffect = volumeLevel.value > 0 ? 
      (volumeLevel.value/100 * 40) : 
      (Math.random() * 5);
    bar.height = Math.max(8, Math.min(60, 30 + baseWave + volumeEffect));
    
    // 渐变颜色计算
    const hue = 200 + index * 2; // 基础色调
    const saturation = 80; // 饱和度固定
    const lightness = 50 + volumeLevel.value/2; // 亮度随音量变化
    
    // 计算渐变颜色 - 从蓝绿色渐变到紫色
    const gradientPercent = index / voiceWaveBars.value.length;
    const startColor = [66, 185, 131]; // #42b983
    const endColor = [147, 112, 219]; // #9370db
    
    const r = Math.floor(startColor[0] + (endColor[0] - startColor[0]) * gradientPercent);
    const g = Math.floor(startColor[1] + (endColor[1] - startColor[1]) * gradientPercent);
    const b = Math.floor(startColor[2] + (endColor[2] - startColor[2]) * gradientPercent);
    
    // 根据音量调整透明度
    const alpha = 0.7 + (volumeLevel.value / 100) * 0.3;
    
    bar.color = `rgba(${r}, ${g}, ${b}, ${alpha})`;
  });
  
  waveAnimationId = requestAnimationFrame(startWaveAnimation);
}


// 组件挂载时启动动画
onMounted(() => {
  
  if (voiceWaveBars.value.length === 0) {
    initVoiceWave();
  }
  if (!waveAnimationId) {
    startWaveAnimation();
  }
});
function adjustColorBrightness(hex, intensity) {
  // 省略实现细节...
}

// 组件卸载时停止动画
onBeforeUnmount(() => {
  if (waveAnimationId) {
    cancelAnimationFrame(waveAnimationId)
  }
})

// 视频面试摄像头流
const userStream = ref(null)
const userVideo = ref(null)
const interviewerImg = ref('')
const videoStarted = ref(false)
const videoInterviewStarted = ref(false)
const endInterview = ref(false)
function onInterviewerImg(e) {
  const file = e.target.files[0]
  if (file) {
    interviewerImg.value = URL.createObjectURL(file)
  }
}
function startVideo() {
  initAvatar()
  onEvents()
  SetApiInfo2()
  SetGlobalParams()
  startAvatar()
  navigator.mediaDevices.getUserMedia({ video: true, audio: false }).then(async stream => {
    userStream.value = stream
    videoStarted.value = true
    await nextTick()
    if (userVideo.value) userVideo.value.srcObject = stream
  }).catch(() => {
    userStream.value = null
    videoStarted.value = false
  })
  navigator.mediaDevices.getUserMedia({
    audio: {
      echoCancellation: true,
      noiseSuppression: true,
      autoGainControl: true
    }
  }).then(stream => {
    mediaStream = stream;
  })
}
function endVideo() {
  destroyAvatar()
  if (userStream.value) {
    userStream.value.getTracks().forEach(track => track.stop())
    userStream.value = null
  }
  if (mediaStream) {
    mediaStream.getTracks().forEach(track => track.stop())
    mediaStream = null
  }

  // 停止帧捕获
  stopFrameCapture()

  videoStarted.value = false
}

const audioName = ref('')

// 修改 startInterview 方法
async function startInterview() {
  step.value = 'interview'
  const res = await initBot({'username': store.state.user?.username, 'scene': sceneMode.value})
  if (res.status === 200) {
    if (sceneMode.value === 'video') {
      audioName.value = res.data.file
    }
    
    // 新增：保存面试类型到本地存储
    // saveInterviewType(sceneMode.value)
  }
  else {
    alert('请重试')
  }
}

// 新增方法：保存面试类型
function saveInterviewType(type) {
  const interviewData = {
    type: type,
    timestamp: new Date().toISOString()
  }
  
  // 保存到本地存储
  const history = JSON.parse(localStorage.getItem('interviewHistory') || '[]')
  history.unshift({
    date: new Date().toISOString(),
    type: sceneMode.value,
    duration: Math.floor(interviewTime.value), // 保存面试时长(秒)
    summary: report.overall_recommendation,
    fullReport: report
  });
  localStorage.setItem('interviewHistory', JSON.stringify(history))
  
  // 同时保存到特定类型的面试历史中
  const typeSpecificKey = `${type}InterviewHistory`
  const typeSpecificHistory = JSON.parse(localStorage.getItem(typeSpecificKey) || '[]')
  typeSpecificHistory.unshift({
    timestamp: new Date().toISOString(),
    type: type
  })
  localStorage.setItem(typeSpecificKey, JSON.stringify(typeSpecificHistory))
}

// 监听 userStream 和 videoStarted，确保每次都赋值
watch([userStream, videoStarted], async ([stream, started]) => {
  if (started && stream) {
    await nextTick()
    if (userVideo.value) userVideo.value.srcObject = stream
  }
})

const isAudioRecording = ref(false)
const isInitializing = ref(false)
const isRecording = ref(false)
const isPlaying = ref(false)
const recordedBlob = ref(null)
const recordingDuration = ref(0)
const volumeLevel = ref(0)
const status = ref('')
const error = ref('')
const countdown = ref(3)
const evaluationData = ref([])
const interviewTime = ref(0.0)
const interviewInterval = ref(null)

const emotionData = ref({
  attentiveness: 0.2,
  confidence: 0.5,
  confusion: 0.05,
  frustration: 0.01,
  nervousness: 0.02
})

let mediaRecorder = null
let audioContext = null
let analyser = null
let microphone = null
let mediaStream = null
let recordingChunks = []
let recordingInterval = null
let countdownInterval = null
let volumeInterval = null
let audioElement = null
// let silenceTimer = null
let speechNumber = 0

async function playSpeech(filename, text) {
  const res = await getBase64({'filename': filename, 'username': store.state.user?.username})
  if (res.status === 200) {
    currentPlayingQuestion.value = text
    const audioUrl = `data:audio/mpeg;base64,${res.data.base64_audio}`
    const audio = new Audio(audioUrl)
    audio.play()

    audio.addEventListener('ended', () => {
      if (videoInterviewStarted.value){
        // speechNumber += 1
        if (!endInterview.value){
          startRecording()
        } else {
          stopRecording()
          endInterview.value = false
        //   speechNumber = 0
        }
      }
      else {
        stopVideoInterview()
      }
      if (sceneMode.value === 'audio') {
        if (!endInterview.value){
          startAudioRecording()
        } else {
          stopVideoInterview()
          endInterview.value = false
          //   speechNumber = 0
        }
      }
    })
  }
}

async function startVideoInterview() {
  if (sceneMode.value === 'audio') {
    navigator.mediaDevices.getUserMedia({
      audio: {
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: true
      }
    }).then(stream => {
      mediaStream = stream;
    })

    const audioUrl = `../../public/${ selectedVoiceStyle.value }.mp3`
    const audio = new Audio(audioUrl)
    audio.play()

    currentPlayingQuestion.value = "你好，请先开始自我介绍"

    audio.addEventListener('ended', () => {
      startAudioRecording()
    })
  }
  if (!videoStarted.value) return;

  // await playSpeech(audioName.value)
  interviewInterval.value = setInterval(() => {
    interviewTime.value += 0.1
  }, 100)

  if (sceneMode.value === 'video') {
    videoInterviewStarted.value = true
    // 开始定时帧捕获（每1秒一次）
    startFrameCapture(1000)
    avatarPlay("你好，请先开始自我介绍")
  }
}

async function stopVideoInterview() {
  try {
    if (interviewInterval.value) {
      clearInterval(interviewInterval.value)
      interviewTime.value = 0
    }
    if (videoInterviewStarted.value) {
      await stopRecording()

      // 停止帧捕获
      stopFrameCapture()

      videoInterviewStarted.value = false
      videoStarted.value = false
      endVideo() // 确保关闭视频流
      showEndConfirm.value = false // 关闭确认对话框
    }
  } catch (error) {
    console.error('结束面试失败:', error)
  }
}

function startRecording() {
  startAudioRecording()
  startMediaRecording()
}

function stopRecording() {
  stopAudioRecording()
  stopMediaRecording()
  if (mediaStream && sceneMode.value === 'audio') {
    mediaStream.getTracks().forEach(track => track.stop())
    mediaStream = null
  }
}

function toggleAudioRecording() {
  if (isAudioRecording.value) {
    stopRecording()
    isAudioRecording.value = false
  } else {
    startVideoInterview()
    isAudioRecording.value = true
    console.log(sceneMode.value)
  }
}

async function startAudioRecording() {
  try {
    isInitializing.value = true
    status.value = '正在请求麦克风权限...'
    error.value = ''

    if (sceneMode.value === 'audio') {
      mediaStream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true
        }
      })
    }

    status.value = '正在初始化录音设置...'

    audioContext = new (window.AudioContext || window.webkitAudioContext)()
    analyser = audioContext.createAnalyser()
    microphone = audioContext.createMediaStreamSource(mediaStream)
    microphone.connect(analyser)

    mediaRecorder = new MediaRecorder(mediaStream)
    recordingChunks = []

    mediaRecorder.ondataavailable = event => {
      if (event.data.size > 0) {
        recordingChunks.push(event.data)
      }
    }

    mediaRecorder.onstop = () => {
      recordedBlob.value = new Blob(recordingChunks, { type: 'audio/wav' })
      status.value = `录音完成，时长: ${formatTime(recordingDuration.value)}`
      console.log(status.value)
      recordingDuration.value = 0
      if ((videoInterviewStarted.value) || (sceneMode.value === 'audio')) {
        postRecording()
      }
    }

    mediaRecorder.start(100)
    isRecording.value = true

    recordingInterval = setInterval(() => {
      recordingDuration.value += 0.1
      if (volumeLevel.value > 40) {
        countdown.value = 1
        // clearInterval(countdownInterval)
        // countdownInterval = setInterval(() => {
        //   console.log('倒计时：', countdown.value)
        //   if (countdown.value === 0) {
        //     stopRecording()
        //     clearInterval(countdownInterval)
        //   } else {
        //     countdown.value -= 1
        //   }
        // }, 1000)
        // clearTimeout(silenceTimer)
        // silenceTimer = setTimeout(() => {
        //   stopRecording()
        //   silenceTimer = null
        // }, 3000)
      }
    }, 100)

    startVolumeMeter()
    status.value = '正在录音...'

    countdownInterval = setInterval(() => {
      console.log('倒计时：', countdown.value)
      if (countdown.value === 0) {
        stopRecording()
        clearInterval(countdownInterval)
        countdown.value = 3
      } else {
        countdown.value -= 1
      }
    }, 1000)
    // silenceTimer = setTimeout(() => {
    //   stopRecording()
    //   silenceTimer = null
    // }, 3000)
  } catch (err) {
    error.value = `录音失败: ${err.message}`
    console.error('录音错误:', err)
    stopRecording()
  } finally {
    isInitializing.value = false
  }
}

/**
 * 停止音频录制
 */
function stopAudioRecording() {
  // if (silenceTimer) {
  //   clearTimeout(silenceTimer)
  // }
  if (countdownInterval) {
    clearInterval(countdownInterval)
    countdown.value = 3
  }
  if (mediaRecorder && isRecording.value) {
    mediaRecorder.stop()
    isRecording.value = false

    if (recordingInterval) {
      clearInterval(recordingInterval)
      recordingInterval = null
    }

    stopVolumeMeter()

    if (microphone) {
      microphone.disconnect()
      microphone = null
    }

    // if (mediaStream) {
    //   mediaStream.getTracks().forEach(track => track.stop())
    //   mediaStream = null
    // }
  }
}

function startVolumeMeter() {
  const dataArray = new Uint8Array(analyser.frequencyBinCount)

  volumeInterval = setInterval(() => {
    analyser.getByteFrequencyData(dataArray)
    let sum = 0
    for (let i = 0; i < dataArray.length; i++) {
      sum += dataArray[i]
    }
    volumeLevel.value = Math.min(100, Math.max(0, (sum / dataArray.length) * 2))
  }, 100)
}

function stopVolumeMeter() {
  if (volumeInterval) {
    clearInterval(volumeInterval)
    volumeInterval = null
    volumeLevel.value = 0
  }
}

async function postRecording() {
  if (!recordedBlob.value) return

  try {
    const formData = new FormData()
    formData.append('audio', recordedBlob.value, `recording-${new Date().toISOString().slice(0, 19)}.wav`)
    formData.append('timestamp', new Date().toISOString())

    const response = await videoChart(formData, store.state.user?.username)

    if (response.status !== 200) {
      throw new Error('上传失败')
    }

    const result = response.data.message
    console.log('上传成功:', result)
    text.value = response.data.text
    if (videoInterviewStarted.value){
      avatarPlay(text.value)
    } else if (sceneMode.value === 'audio'){
      await playSpeech(response.data.file, text.value)
    }
    if (text.value.includes("感谢您的时间，我们的面试到此结束")){
      endInterview.value = true
      isAudioRecording.value = false
    }
    handleSentiments(store.state.user?.username).then((res) => {
      console.log('------------', (!videoInterviewStarted.value && sceneMode.value === 'video') || (!isAudioRecording.value && sceneMode.value === 'audio'))
      if ((!videoInterviewStarted.value && sceneMode.value === 'video') || (!isAudioRecording.value && sceneMode.value === 'audio')) {
        endSentiments(store.state.user?.username).then((res) => {
          if (res.status !== 200) return;
          postAnalyze.value = {
            type: sceneMode.value,
            reportData: JSON.stringify(res.data.evaluation),
            emotionFrames: JSON.stringify(res.data.emotions),
            dialogueRecords: JSON.stringify(res.data.chatlog),
          }
          console.log(postAnalyze.value)
          if (generatingReport.value === false){
            endAnalyze.value = true;
            return
          }
          router.push({
            name: 'InterviewReport',
            state: postAnalyze.value,
          })
          generatingReport.value = false
        })
      }
    })
  } catch (error) {
    console.error('上传错误:', error)
  }
}

function formatTime(seconds) {
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  const tenths = Math.floor((seconds % 1) * 10)
  return `${mins}:${secs < 10 ? '0' : ''}${secs}.${tenths}`
}

function cleanup() {
  stopRecording()
  stopFrameCapture()

  if (audioElement) {
    audioElement.pause()
    audioElement = null
  }

  if (audioContext && audioContext.state !== 'closed') {
    audioContext.close()
  }

  endVideo()
}

let mediaRecord = null
let recordedChunks = []

function startMediaRecording() {
  if (!userStream.value) {
    console.warn('摄像头未开启')
    return
  }

  recordedChunks = []
  mediaRecord = new MediaRecorder(userStream.value, {
    mimeType: 'video/webm; codecs=vp9' // 根据浏览器兼容性可以调整
  })

  mediaRecord.ondataavailable = (event) => {
    if (event.data && event.data.size > 0) {
      recordedChunks.push(event.data)
    }
  }

  mediaRecord.onstop = async () => {
    // 停止后立即保存视频
    const blob = new Blob(recordedChunks, {type: 'video/webm'})
    const formData = new FormData()
    formData.append('media', blob, `recording-${new Date().toISOString().slice(0, 19)}.webm`)
    formData.append('timestamp', new Date().toISOString())

    const res = await uploadMedia(formData, store.state.user?.username)
    if (res.status === 200) {
      console.log(res.data.message)
    }
  }

  mediaRecord.start()
  console.log('开始录制')
}

function stopMediaRecording() {
  if (mediaRecord && mediaRecord.state !== 'inactive') {
    mediaRecord.stop()
    console.log('停止录制并保存视频')
  }
}

watch(chatList, () => {
  nextTick(() => {
    if (chatBodyRef.value) {
      chatBodyRef.value.scrollTop = chatBodyRef.value.scrollHeight
    }
  })
})

onBeforeUnmount(() => {
  cleanup()
  destroyAvatar()
})

// 添加新的响应式变量
const frameCapture = ref({
  isCapturing: false,
  interval: 2000, // 默认每2秒捕获一次
  canvas: null,
  context: null
})

let frameCaptureTimer = null

// 初始化画布用于帧捕获
function initFrameCapture() {
  if (!frameCapture.value.canvas) {
    frameCapture.value.canvas = document.createElement('canvas')
    frameCapture.value.context = frameCapture.value.canvas.getContext('2d')
  }
}

// 捕获当前视频帧
function captureCurrentFrame() {
  if (!userVideo.value || !videoStarted.value) {
    console.warn('视频未启动或视频元素不存在')
    return null
  }

  try {
    const video = userVideo.value
    const canvas = frameCapture.value.canvas
    const context = frameCapture.value.context

    // 设置画布尺寸与视频尺寸一致
    canvas.width = video.videoWidth || video.clientWidth
    canvas.height = video.videoHeight || video.clientHeight

    // 将当前视频帧绘制到画布上
    context.drawImage(video, 0, 0, canvas.width, canvas.height)

    // 获取图像数据
    const imageData = context.getImageData(0, 0, canvas.width, canvas.height)

    // 转换为base64格式（可选）
    const frameDataURL = canvas.toDataURL('image/jpeg', 0.8)

    console.log('帧捕获成功:', {
      timestamp: new Date().toISOString(),
      width: canvas.width,
      height: canvas.height,
      dataURL: frameDataURL.substring(0, 50) + '...' // 只显示前50个字符
    })

    // 这里可以处理捕获的帧数据
    processFrameData(frameDataURL, imageData)

    return {
      dataURL: frameDataURL,
      imageData: imageData,
      timestamp: new Date().toISOString(),
      width: canvas.width,
      height: canvas.height
    }
  } catch (error) {
    console.error('帧捕获失败:', error)
    return null
  }
}

// 处理捕获的帧数据
async function processFrameData(dataURL, imageData) {
  // 示例：将帧数据发送到服务器进行分析
  try {
    // 转换为Blob进行上传
    const response = await fetch(dataURL)
    const blob = await response.blob()

    const formData = new FormData()
    formData.append('frame', blob, `frame-${Date.now()}.jpg`)
    formData.append('timestamp', new Date().toISOString())
    formData.append('username', store.state.user?.username || 'anonymous')

    fetchFrame(formData, interviewTime.value, store.state.user?.username).then(response => {
      if (response.status === 200) {
        if (response.data.attentiveness) {
          emotionData.value.attentiveness = response.data.attentiveness
          emotionData.value.confidence = response.data.confidence
          emotionData.value.confusion = response.data.confusion
          emotionData.value.frustration = response.data.frustration
          emotionData.value.nervousness = response.data.nervousness
        }
      }
    })

  } catch (error) {
    console.error('帧数据处理失败:', error)
  }
}

// 开始定时帧捕获
function startFrameCapture(interval = 2000) {
  if (frameCapture.value.isCapturing) {
    console.warn('帧捕获已在进行中')
    return
  }

  initFrameCapture()
  frameCapture.value.isCapturing = true
  frameCapture.value.interval = interval

  console.log(`开始定时帧捕获，间隔: ${interval}ms`)

  // 立即捕获一次
  captureCurrentFrame()

  // 设置定时器
  frameCaptureTimer = setInterval(() => {
    if (videoStarted.value && videoInterviewStarted.value) {
      captureCurrentFrame()
    }
  }, interval)
}

// 停止定时帧捕获
function stopFrameCapture() {
  if (frameCaptureTimer) {
    clearInterval(frameCaptureTimer)
    frameCaptureTimer = null
  }
  frameCapture.value.isCapturing = false
  console.log('停止定时帧捕获')
}

// 暂停面试方法
function pauseInterview() {
  isPaused.value = true
  // 暂停媒体录制
  stopMediaRecording()
  // 暂停计时器等
}

// 继续面试方法
function resumeInterview() {
  isPaused.value = false
  // 恢复媒体录制
  startMediaRecording()
  // 恢复计时器等
}

const showGenerateConfirm = ref(false)

function showFeedbackConfirm() {
  showGenerateConfirm.value = true
}

// 修改confirmGenerateFeedback方法
async function confirmGenerateFeedback() {
  showGenerateConfirm.value = false
  if (endAnalyze.value) {
    router.push({
      name: 'InterviewReport',
      state: postAnalyze.value,
    })
  }

  generatingReport.value = true
  
  // try {
  //    router.push({
  //      name: 'InterviewReport',
  //      state: {
  //        type: sceneMode.value
  //      }
  //    })
  // } catch (error) {
  //   console.error('生成报告失败:', error)
  //   alert(`生成报告失败: ${error.message}`)
  // } finally {
  //   generatingReport.value = false
  // }
}

// 修改 saveReportToHistory 方法确保类型正确
function saveReportToHistory(report) {
  if (!report) return;
  
  const interviewType = sceneMode.value || 'text'; // 确保有默认值
  
  const history = JSON.parse(localStorage.getItem('interviewHistory') || '[]');
  history.unshift({
    date: new Date().toISOString(),
    type: interviewType, // 明确保存面试类型
    duration: Math.floor(interviewTime.value),
    summary: report.overall_recommendation,
    fullReport: report
  });
  localStorage.setItem('interviewHistory', JSON.stringify(history));
  
  // 同时保存到特定类型的面试历史中
  const typeSpecificKey = `${interviewType}InterviewHistory`;
  const typeSpecificHistory = JSON.parse(localStorage.getItem(typeSpecificKey) || '[]');
  typeSpecificHistory.unshift({
    timestamp: new Date().toISOString(),
    type: interviewType,
    duration: Math.floor(interviewTime.value),
  });
  localStorage.setItem(typeSpecificKey, JSON.stringify(typeSpecificHistory));
}

function showStopConfirm() {
  showEndConfirm.value = true
}

async function confirmStopInterview() {
  showEndConfirm.value = false
  await stopVideoInterview()
}

// 确认结束面试
function onReportGenerated(report) {
  localStorage.setItem('latestReport', JSON.stringify(report))
  router.push('/interview-report')
}

onMounted(() => {
  
  
  getUserInfo(store.state.user.username).then(res => {
    profileData.value.basicInfo = res.data;
  })
  getJobInfo(store.state.user.username).then(res => {
    profileData.value.jobExpectation = res.data;
  })
})
</script>

<style scoped>
/* 添加ProfileForm的样式调整 */
.profile-form-container {
   margin: -2.5rem auto 0; 
  margin-bottom: 4rem;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 调整设置行的间距 */
.setting-row {
  margin-top: 1.5rem;
}
.header {
   z-index: 1000 !important; /* 确保导航栏在最上层 */
  position: relative; 
    transform: none !important;
  border-bottom: 1.5px solid #30629b;
}
.main-nav {
  position: static; /* 改为static避免创建新的层叠上下文 */
  transform: none !important;
}
.scene-setting {
  max-width: none;
  margin: 2px auto 0 0; /* 增加左边距250px */
  background: none;
  border-radius: 0;
  padding: 0;
  box-shadow: none;
  position: relative;
  top: 0;
  z-index: 100;
}

body, #app {
  margin: 0;

   position: relative;
  z-index: auto;
}
.container {
  position: relative;
  z-index: auto;
  overflow: visible !important; /* 确保不会裁剪下拉菜单 */
}
.scene-setting h2 {
  text-align: center;
  margin-bottom: 2rem;
  font-size: 1.2rem;
  letter-spacing: 1px;
}
.setting-row,
.scene-cards {
  max-width: 1500px; /* 或900px，和你实际页面一致 */
  margin: 0 auto 2.5rem auto;
  display: flex;
  justify-content: center;
  gap: 2.5rem;
  flex-wrap: nowrap;     /* 不换行，始终一行 */
}

.setting-row > *,
.scene-card {
  min-width: 340px;
  max-width: 400px;
  width: 100%;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 8px 0 rgba(66,185,131,0.08);
  padding: 1.5rem 1.2rem 1.2rem 1.2rem;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  height: 100%;
}
.scene-card {
  min-width: 340px;
  max-width: 400px;
  width: 100%;
  background: #fff;
  border: 2px solid #d7ebfb; /* 新增边框样式 */
  border-radius: 16px;
  box-shadow: 0 2px 8px 0 rgba(66,185,131,0.08);
  padding: 1.5rem 1.2rem 1.2rem 1.2rem;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  transition: border 0.2s, box-shadow 0.2s, background 0.2s;
  position: relative;
  margin-bottom: 0.5rem;
  min-height: 220px;
  height: 240px;

 
}
.scene-card.active,
.scene-card:hover {
  border: 2px solid #e0e7ef; /* 柔和浅灰色 */
  background: linear-gradient(90deg, #e0f7fa 60%, #c6f7e2 100%);
  box-shadow: 0 4px 18px 0 rgba(60,80,120,0.10);
}
.scene-icon {
  font-size: 2rem;
  margin-bottom: 0.7rem;
}
.scene-title {
  font-size: 1.05rem;
  font-weight: bold;
  color: #2b7a78;
  margin-bottom: 0.5rem;
  letter-spacing: 1px;
}
.scene-desc {
  color: #888;
  font-size: 0.95rem;
  margin-bottom: 0.2rem;
  text-align: center;
  line-height: 1.6;
  width: 100%;
  word-break: break-word;
}
.select-btn {
  margin-top: 0.7rem;
  background: #e0e7ef;
  color: #333;
  border: none;
  border-radius: 8px;
  padding: 0.4rem 1rem;
  font-size: 0.98rem;
  cursor: pointer;
  transition: background 0.2s;
  font-weight: bold;
  letter-spacing: 1px;
}
.select-btn.selected,
.select-btn:hover {
  background: #42b983;
  color: #fff;
}
.scene-actions {
  text-align: center;
  margin-top: 1.5rem;
}
.confirm-btn {
  background: #42b983;
  color: #fff;
  border: none;
  border-radius: 10px;
  padding: 0.8rem 2.2rem;
  font-size: 1.05rem;
  cursor: pointer;
  transition: background 0.2s;
  font-weight: bold;
  letter-spacing: 2px;
  box-shadow: 0 2px 8px 0 rgba(66,185,131,0.10);
}
.confirm-btn:hover {
  background: #369f6b;
}

/* 文本模拟面试样式 */
.chat-interview {
  max-width: none;
  margin: 0;
  min-height: 800px; /* 从650px增加到800px */
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 12px 0 rgba(60,80,120,0.08);
  padding: 1.5rem 1.2rem 1.2rem 1.2rem;
  display: flex;
  flex-direction: column;
}
/* 容器样式 - 控制内部元素排列 */
.interaction-container {
  display: flex;
  flex-direction: column;  /* 垂直排列（输入框在上，按钮在下）*/
  align-items: center;     /* 水平居中 */
  gap: 5px;               /* 元素间距 */
  margin-top: 1000px;        /* 整体下移 */
}
.chat-header {
  font-weight: bold;
  font-size: 1.15rem;
  margin-bottom: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.back-btn {
  background: none;
  border: none;
  color: #42b983;
  font-size: 1rem;
  cursor: pointer;
}
.chat-body {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 1rem;
  padding-right: 0.5rem;
  max-height: 4cap; /* 新增，限制最大高度，超出可滚动 */
  min-height: 500px; /* 可选，保证有基础高度 */
}
.chat-msg {
  display: flex;
  align-items: flex-end;
  margin-bottom: 0.8rem;
}
.chat-msg.ai {
  flex-direction: row;
  color: #000; /* 添加这一行 */
}
.chat-msg.user {
  flex-direction: row-reverse;
  color: #fff;
}
.avatar {
  font-size: 1.5rem;
  margin: 0 0.7rem;
}
.bubble {
  background: #f4f7fa;
  border-radius: 12px;
  padding: 0.7rem 1.1rem;
  font-size: 1.05rem;
  max-width: 80%; /* 从70%增加到80% */
  word-break: break-word;
  line-height: 1.8;
  margin-bottom: 1rem; /* 增加消息间距 */
}
.chat-msg.user .bubble {
  background: #f4f7fa;
  color: #131314;
}
.chat-input {
   margin-top: 1rem;   
  width: 100%;       
  display: flex;
  gap: 0.7rem;
}
.chat-input input {
  flex: 1 1 auto;
  border: 1px solid #d3dbe8;
  border-radius: 8px;
  padding: 0.6rem 1rem;
  font-size: 1rem;
  margin-top: 0;  
}
.chat-input button {
  background: #42b983;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.6rem 1.5rem;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 0;
  transition: background 0.2s;
}
.chat-input button:hover {
  background: #369f6b;
}


.audio-header {
  font-weight: bold;
  font-size: 1.15rem;
  margin-bottom: 1.5rem;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.audio-body {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 2rem;
  width: 100%;
}
.audio-avatar {
  font-size: 3.2rem;
  margin-bottom: 1.5rem;
}
.audio-tip {
  color: #444;
  font-size: 1.15rem;
  line-height: 2.1;
  text-align: center;
  background: #f8fafc;
  border-radius: 10px;
  padding: 1.2rem 1.5rem;
  margin-bottom: 0.5rem;
  width: 100%;
  margin-top: 50px; /* 增加上边距 */
  box-sizing: border-box;
   left: 50px; /* 向右移动50像素 */
}
.audio-question {
  font-weight: bold;
  font-size: 1.13rem;
  margin-bottom: 0.5rem;
}
.audio-question-content {
  color: #2b7a78;
  font-size: 1.12rem;
  margin-bottom: 0.7rem;
}
.audio-answer-tip {
  color: #888;
  font-size: 1.05rem;
  margin-top: 0.7rem;
}

/* 视频模拟样式 */
.video-interview-area {
  width: 90vw;
  height: 90vh;
  background: #f8fafc;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 1500;
  display: flex;
  flex-direction: column;
}
.video-toolbar {
  margin-top:-1.5rem;
  margin-left: -4rem;
  display: flex;
  align-items: center;
  gap: 1.2rem;
  margin-bottom: 1.2rem;
  width: 76rem;
  padding: 1rem 2rem 0.5rem 2rem;
  background: #fff;
  border-radius: 8px;
  border-bottom: 1px solid #e0e7ef;
}
.video-btn {
  background: #42b983;
  color: #fff;
  border: none;
  
  border-radius: 8px;
  padding: 0.5rem 1.5rem;
  font-size: 1.08rem;
  cursor: pointer;
  transition: background 0.2s;
  font-weight: bold;
}
.video-btn.end {
  background: #e74c3c;
}
.upload-input {
  background: #fff;
  border-radius: 6px;
  padding: 2px 8px;
}
.back-btn {
  background: none;
  border: none;
  color: #42b983;
  font-size: 1rem;
  cursor: pointer;
  margin-left: auto;
}
.video-split-row-inner {
  margin-left: -4rem !important;
  display: flex;
  width: 80rem;
  height: 570px;
  gap: 0.1%;
  background: #fff; /* 只用白色 */
  border-radius: 18px;
  box-shadow: 0 4px 14px 0 rgba(60,80,120,0.08); /* 灰色阴影可保留 */
  margin: 0 auto 2rem auto;
  padding: 1.5rem 0;
  transition: box-shadow 0.2s;
}

.video-half-inner {
  flex: 1 1 0;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fff; /* 只用白色 */
  border-radius: 14px;
  margin: 0 1.2rem;
  box-shadow: 0 2px 12px 0 rgba(60,80,120,0.06); /* 灰色阴影可保留 */
  transition: box-shadow 0.2s, background 0.2s;
  overflow: hidden;
  position: relative;
}

/* 移除渐变背景 */
.video-half-inner.left,
.video-half-inner.right {
  background: #fff;
}

.video-rect-inner {
  width: 96%;
  height: 94%;
  background: #181c1f;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  border-radius: 12px;
  position: relative;
  box-shadow: 0 2px 12px 0 rgba(60,80,120,0.10);
}

.video-img-inner {
  width: 100%;
  height: 100%;
  object-fit: cover;
  background: #222;
  display: block;
  border-radius: 12px;
  box-shadow: 0 2px 8px 0 rgba(60,80,120,0.10);
}

.virtual-ai-rect-inner {
  width: 100%;
  height: 100%;
  background: #222;
  color: #42b983;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: 2.2rem;
  font-weight: 500;
  border-radius: 12px;
  letter-spacing: 1px;
  box-shadow: 0 2px 8px 0 rgba(60,80,120,0.10);
}

.virtual-ai-rect-inner .ai-icon {
  font-size: 3.2rem;
  margin-bottom: 0.7rem;
  filter: drop-shadow(0 2px 6px #42b98333);
}

.virtual-ai-rect-inner .ai-label {
  font-size: 1.08rem;
  color: #42b983;
  opacity: 0.85;
  margin-top: 0.2rem;
  letter-spacing: 1px;
}

.self-black {
  background: #181c1f;
}

.video-btn {
  background: #42b983;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.5rem 1.5rem;
  font-size: 1.08rem;
  cursor: pointer;
  transition: background 0.2s, box-shadow 0.2s;
  font-weight: 500;
  box-shadow: 0 2px 8px 0 rgba(66,185,131,0.08);
  margin-right: 0.7rem;
}
.video-btn.end {
  background: #e74c3c;
}
.video-btn:hover {
  background: #369f6b;
  box-shadow: 0 4px 16px 0 rgba(66,185,131,0.13);
}

@media (max-width: 900px) {
  .video-split-row-inner {
    flex-direction: column;
    height: 90vw;
    min-height: 320px;
    gap: 1.2rem;
    padding: 0.5rem 0;
  }
  .video-half-inner {
    margin: 0 0.5rem;
    height: 50%;
  }
  .video-rect-inner {
    width: 98%;
    height: 96%;
  }
}
.virtual-ai-rect-inner .ai-icon {
  font-size: 3rem;
  margin-bottom: 0.7rem;
}
.virtual-ai-rect-inner .ai-label {
  font-size: 1.1rem;
  color: #42b983;
}
.self-black {
  background: #000;
}
@media (max-width: 900px) {
  .video-split-row-inner {
    flex-direction: column;
    height: 90vw;      /* 保持自适应 */
    min-height: 320px; /* 可适当增加 */
  }
  .video-half-inner {
    height: 50%;
  }
}

/* 新增暂停按钮样式 */
.video-btn.pause {
  background-color: #FFC107;
  color: #333;
}

/* 确认弹窗样式 */
.confirm-dialog {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.dialog-content {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  max-width: 400px;
  width: 90%;
  text-align: center;
}

.dialog-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 1.5rem;
}

.dialog-btn {
  padding: 0.7rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
}

.dialog-btn.cancel {
  background-color: #e0e0e0;
}

.dialog-btn.confirm {
  background-color: #42b983;
  color: white;
}

/* 添加加载样式 */
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
  border-top: 4px solid #42b983;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.save-success-message {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: #42b983;
  color: white;
  padding: 10px 20px;
  border-radius: 4px;
  animation: fadeInOut 2s ease-in-out;
}

@keyframes fadeInOut {
  0% { opacity: 0; transform: translateY(20px); }
  20% { opacity: 1; transform: translateY(0); }
  80% { opacity: 1; transform: translateY(0); }
  100% { opacity: 0; transform: translateY(20px); }
}


.setting-row {
  display: flex;
  gap: 2.5rem;
  justify-content: center;
  align-items: stretch;
  margin-bottom: 2.5rem;
}

.setting-row > * {
  min-width: 550px;
  max-width: 550px;
  width: 100%;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 8px 0 rgba(66,185,131,0.08);
  padding: 1.5rem 1.2rem 1.2rem 1.2rem;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

#wrapper {
  width: 100%;
  height: 100%;
}

/* 修改文本模拟容器样式 */
.text-interview-container {
   border-top: 2px solid #e0e7ef;
  display: flex;
  position: fixed;
  left: 0;
  top: 85px;
  bottom: 80px;
  width: 100%; /* 改为100%宽度 */
  height: calc(100vh - 145px);
  background: #fff; /* 移除背景色 */
  z-index: 1 !important; /* 确保在最上层 */
  overflow: hidden;
  box-shadow: none; /* 移除阴影 */
  padding: 0 20px; /* 添加内边距 */
}


.chat-interview,
.audio-interview {
  flex: 2;
  min-height: 680px;  /* 增大最小高度 */
  width: 100%;        /* 确保宽度填满 */
  max-width: none;    /* 移除最大宽度限制 */
  margin: 0;       

  background: #fff;
  border-radius: 0;
  box-shadow: 0 2px 12px 0 rgba(60,80,120,0.08);

}


/* 确保侧边栏和右侧面板固定宽度 */
.history-sidebar,
.profile-toggle-container {
  flex: 0 0 300px;

  background: #fff; /* 改为浅灰色背景 */
}

.audio-history-panel h3 {
  color: #2b7a78;
  font-size: 1.15rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #e0e7ef;
}

.audio-interview-container {
   border-top: 2px solid #e0e7ef;
  display: flex;
  position: fixed;
  left: 0;
  top: 85px;
  bottom: 80px;
  width: 100%;
  height: calc(100vh - 145px);
  z-index: 1 !important;
  overflow: hidden;
}

.audio-history-panel {
  width: 300px;
  border-right: 1px solid #e0e7ef;
  padding: 1rem;
  overflow-y: auto;
  background: #fff;
}

.audio-record-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.audio-record-item {
  padding: 0.8rem;
  border-bottom: 1px solid #e0e7ef;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  transition: background 0.2s;
  color: #2b7a78; /* 新增文字颜色 */
}

.audio-record-item:hover {
  background: #e0f7fa;
}

.record-time {
  color: #2b7a78; /* 修改为指定颜色 */
  font-size: 0.9rem;
  font-weight: 500; /* 增加字体权重 */
}


.record-duration {
  color: #2b7a78; /* 修改为指定颜色 */
  opacity: 0.8; /* 添加透明度区分 */
  font-size: 0.85rem;
}

audio {
  width: 100%;
  margin: 1rem 0;
}

.audio-actions {
  display: flex;
  justify-content: center; /* 居中 */
  gap: 2rem; /* 增加按钮间距 */
  margin-top: 2rem;
  width: 100%;
}

.audio-btn {
  background: #3dcd9f;
  color: #fff;
  border: none;
  border-radius: 12px;
  padding: 1rem 1.5rem; /* 增大内边距 */
  font-size: 1rem; /* 增大字体 */
  cursor: pointer;
  transition: background 0.2s;
  font-weight: bold;
  min-width: 180px; /* 设置最小宽度 */
  box-shadow: 0 4px 12px rgba(66, 185, 131, 0.2);
}

.audio-btn:hover {
  background: #f59694;
  transform: translateY(-2px);
}

/* 停止按钮特殊样式 */
.audio-btn:last-child {
  background: #3dcd9f;
}

.audio-btn:last-child:hover {
  background: #c0392b;
}

/* 按钮容器：调整位置与响应式布局 */
.generate-report-container {
  position: fixed;
  bottom: 65px; 
  right: 680px; 
  z-index: 90;
}

/* 核心按钮样式优化 */
.generate-report-btn {
  background: linear-gradient(135deg, #00dc9f 0%, #2ca772 100%);
  color: white;
  border: none;
  border-radius: 8px; 
  padding: 12px 24px; 
  font-size: 15px; 
  font-weight: 600; 
  cursor: pointer;
  
  box-shadow: 0 4px 12px rgba(66, 185, 131, 0.25), 
              inset 0 1px 2px rgba(255, 255, 255, 0.1); 
  transition: all 0.25s ease; 
  display: inline-flex; 
  align-items: center;
  gap: 8px; 
}


.generate-report-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(66, 185, 131, 0.35); 
  background: linear-gradient(135deg, #48c78e 0%, #30b07b 100%);
}

/* 点击效果：强化按压反馈 */
.generate-report-btn:active {
  transform: translateY(0); /* 原+1px → 取消位移，改用背景色加深 */
  background: linear-gradient(135deg, #3ba573 0%, #2a9465 100%); /* 颜色压暗，模拟按压感 */
  box-shadow: 0 2px 8px rgba(66, 185, 131, 0.2); /* 阴影缩小，贴近页面 */
}

/* 禁用态补充（当面试未完成时） */
.generate-report-btn:disabled {
  background: #e8f5e9; /* 浅色背景，与输入框呼应 */
  color: #81c784; /* 低饱和绿色文字，保留关联性 */
  cursor: not-allowed;
  box-shadow: none;
  transform: none;
  opacity: 0.9; /* 轻微透明，区分可用状态 */
}

/* 图标优化：使用线性图标更贴合科技感（假设使用自定义图标字体） */
.generate-report-btn .icon {
  width: 18px;
  height: 18px;
  display: inline-block;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white'%3E%3Cpath d='M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z'/%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
}
.interview-tip {
  position: fixed;
  top: 80px;
  left: 0;
  right: 0;
  background: #fff8e6;
  color: #ff9800;
  padding: 10px 0;
  text-align: center;
  z-index: 99;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.tip-content {
  max-width: 1200px;
  margin: 0 auto;
  font-weight: bold;
  font-size: 14px;
}
.voice-style-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.voice-style-item {
  padding: 1.2rem 1.5rem;
  border-bottom: 2px solid #e0e7ef;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.8rem;
  transition: all 0.2s;
  border-radius: 8px;
  margin-bottom: 0.5rem;
  color: #2b7a78;
}

.voice-style-item:hover {
  background: #e0f7fa;
  transform: translateX(5px);
}

.voice-style-item.active {
  background: #f5fafa;
  color: #2b7a78;
}

.style-icon {
  font-size: 1.2rem;
}

.style-name {
  font-size: 0.95rem;
  font-weight: 500;
}

/* 添加语音波动图样式 */
.voice-wave-container {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  height: 120px;
  width: 100%;
  gap: 8px;
  padding: 10px 0;
}

.voice-wave {
  width: 8px;
  min-height: 9px;
  border-radius: 4px;
  transition: 
    height 0.15s ease-out, 
    background-color 0.3s ease,
    opacity 0.3s ease;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.audio-tip {
  /* 调整原有样式以适应波动图 */
  padding: 1.5rem;
  margin-top: 50px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
@keyframes pulse {
  0%, 100% {
    transform: scaleY(1);
    opacity: 0.8;
  }
  50% {
    transform: scaleY(1.2);
    opacity: 1;
  }
}
</style>