<template>
  <div class="learning-path-detail">
    <div class="path-header">
      <h1 class="art-title">{{ pathDetail.title }}</h1>
      <p class="art-desc">{{ pathDetail.description }}</p>
    </div>

    <div class="resources-container">

      <div v-if="pathDetail.id === 1" class="resource-list">
        <h2>面试视频资源</h2>
        <div class="video-grid">
          <div v-for="(video, index) in interviewVideos" :key="index" class="video-card">
            <video controls width="100%">
              <source :src="video.url" type="video/mp4">
              您的浏览器不支持HTML5视频标签。
            </video>
            <h3>{{ video.title }}</h3>
          </div>
        </div>
      </div>

      <!-- 表达训练视频部分 -->
      <div v-if="pathDetail.id === 2" class="resource-list">
        <h2>表达训练视频</h2>
        <div class="video-grid">
          <div v-for="(video, index) in videoList" :key="index" class="video-card">
            <video controls width="100%">
              <source :src="video.url" type="video/mp4">
              您的浏览器不支持HTML5视频标签。
            </video>
            <h3>{{ video.title }}</h3>
          </div>
        </div>
      </div>

      <!-- 岗位技能课程部分 -->
      <div v-if="pathDetail.id === 3" class="resource-list">
        <h2>技能课程视频</h2>
        <div class="video-grid">
          <div v-for="(video, index) in skillVideos" :key="index" class="video-card">
            <video controls width="100%">
              <source :src="video.url" type="video/mp4">
              您的浏览器不支持HTML5视频标签。
            </video>
            <h3>{{ video.title }}</h3>
          </div>
        </div>
      </div>
    </div>

    <button @click="goBack" class="btn-back">返回首页</button>
  </div>
</template>

<script>
import { computed, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'LearningPathDetail',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const videoList = ref([])
    const skillVideos = ref([])
    const interviewVideos = ref([]) // 新增面试题库视频列表

    const pathDetail = computed(() => {
      const paths = [
        { id: 1, title: '行业面试视频', description: '精选行业岗位面试真题视频' }, // 修改描述
        { id: 2, title: '表达训练视频', description: '提升沟通与表达能力的专业课程' },
        { id: 3, title: '岗位技能课程', description: '针对目标岗位的技术提升路径' }
      ]
      return paths.find(p => p.id === Number(route.params.id)) || paths[0]
    })

    // 修改后的面试题库视频数据
    const fetchInterviewVideos = async () => {
      try {
        const videos = [
          { title: '24秋招|某大厂面试"', url: '/videos3/video1.mp4' },
          { title: '沉浸式面试', url: '/videos3/video2.mp4' },
          { title: '面试86.4分考生作答全流程', url: '/videos3/video3.mp4' },
          { title: '面试礼仪示范视频', url: '/videos3/video4.mp4' },
          { title: '模拟面试视频', url: '/videos3/video5.mp4' },
          { title: '南方电网校园招聘面试流程', url: '/videos3/video6.mp4' },
          { title: '求职面试优秀模板', url: '/videos3/video7.mp4' },
          { title: '不肯后退的眼睛', url: '/videos3/video8.mp4' },

        ]
        interviewVideos.value = videos
      } catch (error) {
        console.error('获取面试题库视频失败:', error)
      }
    }

    const fetchVideos = async () => {
      try {
        const videos = [
          { title: '【面试必会】90%的同学都打错了！面试被问到"与团队意见不一致，你会怎么做？"', url: '/videos/video1.mp4' },
          { title: '教科书式面试回答！普通人真的可以学到很多面试技巧', url: '/videos/video2.mp4' },
          { title: '面试八股文实际在考察你的什么能力？', url: '/videos/video3.mp4' },
          { title: '面试高频题拆解', url: '/videos/video5.mp4' },
          { title: '面试了快20位实习生之后，我总结了一大堆面试经验', url: '/videos/video6.mp4' },
          { title: '教科书式面试回答！求职战役的六个阶段', url: '/videos/video7.mp4' },
          { title: '教科书式面试回答！如何设定你的目标', url: '/videos/video8.mp4' },
          
          { title: '救命！我好像真的打通了事业单位面试的任督二脉！', url: '/videos/video9.mp4' },
          { title: '面试礼仪示范视频', url: '/videos/video10.mp4' }
        ]
        videoList.value = videos
      } catch (error) {
        console.error('获取视频列表失败:', error)
      }
    }

    const fetchSkillVideos = async () => {
      try {
        const videos = [
          { title: '【入门必备】学习物联网的最短路径', url: '/videos2/video1.mp4' },
          { title: '10分钟解密大数据所有招聘岗位及区别', url: '/video2.mp4' },
          { title: '20分钟速通大学所有专业', url: '/videos2/video3.mp4' },
          { title: '2025计算机专业就业方向和发展前景分析', url: '/videos2/video4.mp4' },
          { title: '不要荒废！死磕这四门技能', url: '/videos2/video5.mp4' },
          { title: '大数据怎么处理？Hedoop是什么？', url: '/videos2/video6.mp4' },
          { title: 'HR招聘技能合集：从撰写岗位JD到选人全流程P01', url: '/videos2/video7.mp4' },
          { title: 'HR招聘技能合集：从撰写岗位JD到选人全流程P02', url: '/videos2/video8.mp4' }
        ]
        skillVideos.value = videos
      } catch (error) {
        console.error('获取技能视频列表失败:', error)
      }
    }

    onMounted(() => {
      if (pathDetail.value.id === 1) {
        fetchInterviewVideos()
      } else if (pathDetail.value.id === 2) {
        fetchVideos()
      } else if (pathDetail.value.id === 3) {
        fetchSkillVideos()
      }
    })

    const goBack = () => {
      router.push('/')
    }

    return {
      pathDetail,
      interviewVideos, // 返回新增的视频列表
      videoList,
      skillVideos,
      goBack
    }
  }
}
</script>

<style scoped>
/* 保持原有样式不变 */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@500&display=swap');

.art-title {
  font-family: 'Playfair Display', serif;
  font-size: 2rem;
  font-weight: 600;
  margin-top: -1.5rem;
  color: #2c3e50;
  text-shadow: 7px 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 0.5rem;
}

.art-desc {
  font-family: 'Montserrat', sans-serif;
  font-size: 1.1rem;
  color: #7f8c8d;
  letter-spacing: 1px;
}

.learning-path-detail {
  max-width: 1300px;
  margin: 0 auto;
  margin-top: -2.5rem;
  padding: 2rem;
  margin-left: -6.5rem;
}

.path-header {
  text-align: center;
  margin-bottom: 2rem;
}

.resources-container {
  margin-left: -5rem;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 1300px;
  margin-left: 0;
  height: auto;
}

.resource-list {
  margin-top: -2.5rem;
  line-height: 1.6;
}

/* 统一的视频网格样式 */
.video-grid {
  margin-top: 1.5rem;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.8rem;
}

/* 统一的视频卡片样式 */
.video-card {
  border-radius: 12px;
  transition: transform 0.3s ease;
  background: white;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.video-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.video-card video {
  width: 100%;
  height: 160px;
  object-fit: cover;
  display: block;
}

.video-card h3 {
  margin: 0;
  padding: 12px 15px;
  font-size: 0.95rem;
  color: #2c3e50;
  text-align: center;
  background: #f8f9fa;
  min-height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-back {
  display: block;
  margin: 2rem auto 0;
  padding: 0.8rem 1rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-back:hover {
  background-color: #2980b9;
}
</style>