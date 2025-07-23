<template>
  <div class="profile-container">
     <div v-if="showWelcomeMessage" class="welcome-message">
      <div class="message-content">
        <span class="close-btn" @click="closeWelcomeMessage">×</span>
        <h3>欢迎加入Moss！</h3>
        <p>为了提供基于用户自己的模拟面试，请填写必要的个人信息和上传简历</p>
      </div>
    </div>
    <!-- 主体内容区 -->
    <div class="profile-content">
      <!-- 左侧主体信息区 -->
      <div class="main-content">
        <!-- 个人信息模块 -->
        <div class="profile-info">
          <div class="avatar-section">
            <img src="@/assets/empty-comment.png" alt="头像" class="avatar">
            <div class="basic-info">
              <h1 class="username">{{ profileData.basicInfo.nickname }} <span class="badge">青出于蓝</span></h1>
              <div class="detail-info">
                <span class="detail-item">
                  <svg viewBox="0 0 24 24" width="14" height="14">
                    <path
                        d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                  </svg>
                  {{ profileData.basicInfo.university }} {{ profileData.basicInfo.graduationYear }}
                </span>
                <span class="detail-item">
                  <svg viewBox="0 0 24 24" width="14" height="14">
                    <path
                        d="M19 3h-4.18C14.4 1.84 13.3 1 12 1c-1.3 0-2.4.84-2.82 2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 0c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm0 15l-5-5h3V9h4v4h3l-5 5z"/>
                  </svg>
                  {{ profileData.jobExpectation.position }}
                </span>
                <span class="detail-item">IP 属地：{{ profileData.basicInfo.location }}</span>
              </div>
              <a href="#" class="add-intro">点击添加简介，让大家认识你</a>
            </div>
          </div>

          <div class="stats-section">
            <div class="stat-item">
              <div class="stat-number">{{ textInterviewCount }}</div>
              <div class="stat-label">文本面试次数</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">{{ audioInterviewCount }}</div>
              <div class="stat-label">语音面试次数</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">{{ videoInterviewCount }}</div>
              <div class="stat-label">视频面试次数</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">{{ QACount }}</div>
              <div class="stat-label">面试试题次数</div>
            </div>
          </div>

          <div class="action-buttons">
            <button class="profile-btn complete-btn" @click="openEditPanel">
              {{ completionRateText }} <span class="edit-link">去编辑 ></span>
            </button>
            <button class="profile-btn resume-btn" @click="goToResumeSetting">
              我的简历
              <span class="status-badge" :class="{'badge-success': profileData.hasResume}">
                {{ resumeStatus }}
              </span>
            </button>
            <ResumeSetting ref="resumeSetting" @has-resume="handleHasResume"/>
          </div>
        </div>

        <!-- 导航标签栏 -->
        <div class="tab-bar">
          <button class="tab-item" :class="{ active: activeTab === 'comprehensive' }"
                  @click="switchTab('comprehensive')">综合
          </button>
          <button class="tab-item" :class="{ active: activeTab === 'dynamic' }" @click="switchTab('dynamic')">动态
          </button>
          <button class="tab-item" :class="{ active: activeTab === 'article' }" @click="switchTab('article')">文章
          </button>
          <button class="tab-item" :class="{ active: activeTab === 'referral' }" @click="switchTab('referral')">内推
          </button>
        </div>
        <transition name="fade" mode="out-in">
          <!-- 内容展示区 -->
          <div class="content-section">
            <!-- 综合内容 -->
            <div v-if="activeTab === 'comprehensive'" class="tab-content">
              <div v-if="filteredPosts.length > 0">
                <div class="post-item" v-for="(item, idx) in filteredPosts" :key="item.id">
                  <!-- 用户信息部分 -->
                  <div class="user-info">
                    <div class="avatar">
                      <i class="icon-user-default"></i>
                    </div>
                    <div class="user-details">
                      <div class="username">
                        <span>{{ item.username }}</span>
                        <span class="user-level">{{ item.level }}</span>
                      </div>
                      <div class="post-meta">
                        <span class="post-time">{{ item.time }}</span>
                        <span class="school">{{ item.school }}</span>
                        <span class="contentType">{{ item.contentType }}</span>
                      </div>
                    </div>
                  </div>

                  <!-- 标题和内容 -->
                  <h3 v-if="item.title" class="post-title">{{ item.title }}</h3>
                  <p class="post-content">
                    <span v-html="isExpanded[idx] ? item.fullContent || item.content : item.content"></span>
                    <a v-if="item.fullContent && item.fullContent.length > 200" href="#" class="read-more"
                       @click.prevent="toggleExpand(idx)">
                      {{ isExpanded[idx] ? '收起' : '查看更多' }}
                    </a>
                  </p>
                </div>
              </div>
              <div v-else class="empty-content">
                <img src="@/assets/empty-folder.png" alt="空文件夹" class="empty-icon">
                <p class="empty-text">暂无内容，快来发布第一条动态吧！</p>
              </div>
            </div>

            <!-- 动态内容 -->
            <div v-if="activeTab === 'dynamic'" class="tab-content">
              <div v-if="dynamicPosts.length > 0">
                <div class="post-item" v-for="(item, idx) in dynamicPosts" :key="item.id">
                  <div class="user-info">
                    <div class="avatar">
                      <i class="icon-user-default"></i>
                    </div>
                    <div class="user-details">
                      <div class="username">
                        <span>{{ item.username }}</span>
                        <span class="user-level">{{ item.level }}</span>
                      </div>
                      <div class="post-meta">
                        <span class="post-time">{{ item.time }}</span>
                        <span class="school">{{ item.school }}</span>
                        <span class="contentType">{{ item.contentType }}</span>
                      </div>
                    </div>
                  </div>
                  <h3 v-if="item.title" class="post-title">{{ item.title }}</h3>
                  <p class="post-content">
                    <span v-html="isExpanded[idx] ? item.fullContent || item.content : item.content"></span>
                    <a v-if="item.fullContent && item.fullContent.length > 200" href="#" class="read-more"
                       @click.prevent="toggleExpand(idx)">
                      {{ isExpanded[idx] ? '收起' : '查看更多' }}
                    </a>
                  </p>
                </div>
              </div>
              <div v-else class="empty-content">
                <img src="@/assets/empty-folder.png" alt="空文件夹" class="empty-icon">
                <p class="empty-text">暂无动态内容</p>
              </div>
            </div>

            <!-- 文章内容 -->
            <div v-if="activeTab === 'article'" class="tab-content">
              <div v-if="articlePosts.length > 0">
                <div class="post-item" v-for="(item, idx) in articlePosts" :key="item.id">
                  <div class="user-info">
                    <div class="avatar">
                      <i class="icon-user-default"></i>
                    </div>
                    <div class="user-details">
                      <div class="username">
                        <span>{{ item.username }}</span>
                        <span class="user-level">{{ item.level }}</span>
                      </div>
                      <div class="post-meta">
                        <span class="post-time">{{ item.time }}</span>
                        <span class="school">{{ item.school }}</span>
                        <span class="contentType">{{ item.contentType }}</span>
                      </div>
                    </div>
                  </div>
                  <h3 v-if="item.title" class="post-title">{{ item.title }}</h3>
                  <p class="post-content">
                    <span v-html="isExpanded[idx] ? item.fullContent || item.content : item.content"></span>
                    <a v-if="item.fullContent && item.fullContent.length > 200" href="#" class="read-more"
                       @click.prevent="toggleExpand(idx)">
                      {{ isExpanded[idx] ? '收起' : '查看更多' }}
                    </a>
                  </p>
                </div>
              </div>
              <div v-else class="empty-content">
                <img src="@/assets/empty-folder.png" alt="空文件夹" class="empty-icon">
                <p class="empty-text">暂无文章内容</p>
              </div>
            </div>

            <!-- 内推内容 -->
            <div v-if="activeTab === 'referral'" class="tab-content">
              <div v-if="referralPosts.length > 0">
                <div class="post-item" v-for="(item, idx) in referralPosts" :key="item.id">
                  <div class="user-info">
                    <div class="avatar">
                      <i class="icon-user-default"></i>
                    </div>
                    <div class="user-details">
                      <div class="username">
                        <span>{{ item.username }}</span>
                        <span class="user-level">{{ item.level }}</span>
                      </div>
                      <div class="post-meta">
                        <span class="post-time">{{ item.time }}</span>
                        <span class="school">{{ item.school }}</span>
                        <span class="contentType">{{ item.contentType }}</span>
                      </div>
                    </div>
                  </div>
                  <h3 v-if="item.title" class="post-title">{{ item.title }}</h3>
                  <p class="post-content">
                    <span v-html="isExpanded[idx] ? item.fullContent || item.content : item.content"></span>
                    <a v-if="item.fullContent && item.fullContent.length > 200" href="#" class="read-more"
                       @click.prevent="toggleExpand(idx)">
                      {{ isExpanded[idx] ? '收起' : '查看更多' }}
                    </a>
                  </p>
                </div>
              </div>
              <div v-else class="empty-content">
                <img src="@/assets/empty-folder.png" alt="空文件夹" class="empty-icon">
                <p class="empty-text">暂无内推内容</p>
              </div>
            </div>
            <!-- 在每个 tab-content div 的末尾添加 -->
           <div v-if="filteredPosts.length > 0" class="pagination-controls">
             <button 
               class="page-btn" 
               @click="goToPage(currentPage - 1)" 
               :disabled="currentPage === 1"
             >
               上一页
             </button>
  
             <span class="page-info">
               第 {{ currentPage }} 页 / 共 {{ totalPages }} 页
             </span>
  
             <button 
               class="page-btn" 
               @click="goToPage(currentPage + 1)" 
               :disabled="currentPage === totalPages || totalPages === 0"
             >
               下一页
             </button>
           </div>
          </div>
        </transition>
        
      </div>
      

      <!-- 右侧功能快捷操作区 -->
      <div class="sidebar">
        <!-- 创作者中心模块 -->
        <div class="sidebar-card">
          <h3 class="card-title">创作者中心 <a href="#" class="card-link" @click.prevent="goToCreatePost('dynamic')">进入
            ></a></h3>
          <div class="creator-actions">
            <button class="creator-btn" @click="goToCreatePost('dynamic')">
              <svg viewBox="0 0 24 24" width="18" height="18">
                <path d="M14 10H2v2h12v-2zm0-4H2v2h12V6zm4 8v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zM2 16h8v-2H2v2z"/>
              </svg>
              发动态
            </button>
            <button class="creator-btn" @click="goToCreatePost('article')">
              <svg viewBox="0 0 24 24" width="18" height="18">
                <path
                    d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
              </svg>
              写文章
            </button>
          </div>
        </div>
        <div class="check-in-stats">
          <div class="tool-item">
            <span>每日打卡</span>
            <span class="tool-status" :class="{'checked-in': checkInStatus}">
                   {{ checkInStatus ? '已打卡' : '未打卡' }}
                 </span>
            <button class="check-in-btn" @click="checkIn" :disabled="checkInStatus">
              {{ checkInStatus ? '已打卡' : '打卡' }}
            </button>
          </div>
          <div class="achievement-wall">
            <div class="achievement-card consecutive">
              <div class="card-icon">
                <svg viewBox="0 0 24 24" width="24" height="24">
                  <path
                      d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/>
                </svg>
              </div>
              <div class="card-content">
                <div class="card-title">连续打卡</div>
                <div class="card-value">{{ consecutiveDays }}<span class="unit">天</span></div>
                <div class="progress-bar">
                  <div class="progress" :style="{width: `${Math.min(100, consecutiveDays * 100 / 7)}%`}"></div>
                </div>
              </div>
            </div>

            <div class="achievement-card total">
              <div class="card-icon">
                <svg viewBox="0 0 24 24" width="24" height="24">
                  <path
                      d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/>
                </svg>
              </div>
              <div class="card-content">
                <div class="card-title">累计打卡</div>
                <div class="card-value">{{ checkInDays }}<span class="unit">天</span></div>
                <div class="sparkline">
                  <div class="sparkline-bar" v-for="(bar, index) in sparklineData" :key="index"
                       :style="{height: `${bar}%`, backgroundColor: getSparklineColor(index)}"></div>
                </div>
              </div>
            </div>
          </div>
          <div class="encouragement">{{ getEncouragementText() }}</div>
        </div>
      </div>
    </div>
  </div>
  <ProfileEditPanel
      :show-panel="showEditPanel"
      :profile-data="profileData"
      :completion-rate="profileData.basicInfo.completionRate"
      mode="slide"
      @close="closeEditPanel"
      @save="handleSave"
  />
</template>

<script>
import ProfileEditPanel from '@/components/ProfileEditPanel.vue'
import ResumeSetting from '@/components/ResumeSetting.vue'
import ResumeDesign from '@/components/ResumeDesign.vue'
import {editJobInfo, editUserInfo, getCheckIn, getJobInfo, getUserInfo, updateCheckIn} from "@/api/user";
import store from "@/store";
import {getExperience, listExperiences} from "@/api/experience";
import {getInterviewCount} from "@/api/interview";

export default {
 props: {
    firstRegister: {
      type: Boolean,
      default: false
    }
  },
  name: 'Profile',
  components: {
    ResumeSetting,
    ProfileEditPanel,
    ResumeDesign,
  },
  data() {
    return {
      showWelcomeMessage: false,
      isExpanded: [],
      postList: [],
      dynamicPosts: [], 
      articlePosts: [], 
      referralPosts: [],
      currentPage: 1,
      pageSize: 5,
      totalPages: 1,
      checkInStatus: false,
      checkInDate: null,
      checkInDays: 0, // 累计打卡天数
      consecutiveDays: 0,
      salaryQuery: {
        position: '',
        location: ''
      },
      salaryResults: [],
      salaryQueried: false,
      showEditPanel: false,
      activeTab: 'comprehensive', // 默认显示发布标签页
      publishList: [], // 发布内容列表
      sparklineData: [],
      loading: false,
      error: null,
      comments: [
        // 示例数据 - 实际项目中应该从API获取
        {
          id: 1,
          postTitle: "如何准备前端面试",
          content: "这篇文章很有帮助，特别是关于Vue.js面试问题的部分！",
          time: "2023-05-15 14:30"
        },
        {
          id: 2,
          postTitle: "后端开发学习路线",
          content: "感谢分享，对新手很有指导意义",
          time: "2023-05-10 09:15"
        }
      ],
      interviewStats: {
        total: 0,
        types: {
          text: 0,
          audio: 0,
          video: 0
        }
      },
      interviewRecords: [],
      practiceStats: { // 刷题统计
        total: 0,
        correctRate: 0
      },
      practiceRecords: [], // 刷题记录
      favoriteTabs: [ // 收藏标签
        {label: '文章', value: 'posts'},
        {label: '职位', value: 'jobs'},
        {label: '问题', value: 'questions'}
      ],
      favoriteTab: 'posts',
      profileData: {
        basicInfo: {
          realname: '',
          nickname: store.state.user.username,
          gender: '',
          bio: '',
          verified: false,
          location: '',
          graduationYear: '2023',
          education: '本科',
          university: '长春工业大学',
          major: '计算机科学与技术',
          completionRate: 70
        },
        hasResume: false,
        jobExpectation: {
          position: '前端工程师',
          jobRequirements: '213',
          status: '在职，考虑新机会',
          salaryRange: '不限 - 不限',
          workLocation: '深圳'
        },
        workExperience: [
          {
            company: '腾讯科技',
            position: '前端开发工程师',
            time: '2021.07 - 至今',
            description: '负责公司核心产品的前端开发工作，使用Vue.js框架'
          },
          {
            company: '字节跳动',
            position: '前端实习生',
            time: '2020.07 - 2021.06',
            description: '参与公司内部管理系统的前端开发'
          }
        ],
        projectExperience: [
          {
            name: '电商后台管理系统',
            role: '前端负责人',
            time: '2022.03 - 2022.12',
            description: '带领3人前端团队完成系统开发，使用Vue3+TypeScript'
          }
        ],
        skills: [
          {name: 'HTML/CSS', level: 90},
          {name: 'JavaScript', level: 85},
          {name: 'Vue.js', level: 80}
        ]
      },
      textInterviewCount: 0,
      audioInterviewCount: 0,
      videoInterviewCount: 0,
      QACount: 0,
    }
  },
  computed: {

  
    filteredPosts() {
      // 先过滤
      let filtered;
      switch (this.activeTab) {
        case 'comprehensive':
          filtered = this.postList;
          break;
        case 'dynamic':
          filtered = this.postList.filter(post => 
            post.contentType === '动态' || post.contentType === 'dynamic'
          );
          break;
        case 'article':
          filtered = this.postList.filter(post => 
            post.contentType === '文章' || post.contentType === 'article'
          );
          break;
        case 'referral':
          filtered = this.postList.filter(post => 
            post.contentType === '内推' || post.contentType === 'referral'
          );
          break;
        default:
          filtered = this.postList;
      }
      
      // 再分页
      this.totalPages = Math.ceil(filtered.length / this.pageSize);
      const startIndex = (this.currentPage - 1) * this.pageSize;
      const endIndex = startIndex + this.pageSize;
      return filtered.slice(startIndex, endIndex);
    },
  // 将动态文章内推列表改为计算属性
    dynamicPosts() {
      return this.postList.filter(post =>
        post.contentType === '动态' || post.contentType === 'dynamic'
      );
    },
    articlePosts() {
      return this.postList.filter(post =>
        post.contentType === '文章' || post.contentType === 'article'
      );
    },
    referralPosts() {
      return this.postList.filter(post =>
        post.contentType === '内推' || post.contentType === 'referral'
      );
    },
    resumeStatus() {
      return this.profileData.hasResume ? '已完善' : '未完善';
    },
    completionRateText() {
      return `个人资料完善度：${this.profileData.basicInfo.completionRate}%`;
    },
    displayedSkills() {
      return this.profileData.skills.slice(0, 3);
    },
    averageSalary() {
      if (this.salaryResults.length === 0) return 0;
      // 提取薪资数字并计算平均值
      const salaries = this.salaryResults.map(result => {
        // 提取数字部分，假设格式为 "15000-25000" 或 "15000"
        const match = result.salary.match(/\d+/g);
        if (!match) return 0;
        // 如果是范围，取中间值
        if (match.length > 1) {
          return (parseInt(match[0]) + parseInt(match[1])) / 2;
        }
        return parseInt(match[0]);
      });
      const sum = salaries.reduce((acc, val) => acc + val, 0);
      return Math.round(sum / salaries.length);
    }
  },
   watch: {
    firstRegister(newVal) {
      if (newVal) {
        this.showWelcomeMessage = true
        // 3秒后自动关闭提示
        setTimeout(() => {
          this.showWelcomeMessage = false
        }, 30000) // 30秒后自动关闭
      }
    }
  },
  methods: {
    closeWelcomeMessage() {
      this.showWelcomeMessage = false
    },
   sortPostsByTime() {
    // 按时间降序排列（最新的在前）
    this.postList.sort((a, b) => new Date(b.time) - new Date(a.time));
    
    // 对各个分类列表也进行排序
    this.dynamicPosts = this.postList.filter(post => 
      post.contentType === '动态' || post.contentType === 'dynamic'
    ).sort((a, b) => new Date(b.time) - new Date(a.time));
    
    this.articlePosts = this.postList.filter(post => 
      post.contentType === '文章' || post.contentType === 'article'
    ).sort((a, b) => new Date(b.time) - new Date(a.time));
    
    this.referralPosts = this.postList.filter(post => 
      post.contentType === '内推' || post.contentType === 'referral'
    ).sort((a, b) => new Date(b.time) - new Date(a.time));
  },
    handleHasResume() {
      this.profileData.hasResume = true
    },
    // 添加切换标签页方法
    switchTab(tab) {
      this.activeTab = tab;
      this.currentPage = 1; // 切换标签时重置页码
    },

    // 添加分页方法
    goToPage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },

    // 添加展开/收起方法
    toggleExpand(index) {
      this.$set(this.isExpanded, index, !this.isExpanded[index])
    },

    // 添加格式化内容方法
    formatContent(content) {
      return content
          .replace(/\n/g, '<br>')
          .replace(/!\[图片\]\((.*?)\)/g, '<img src="$1" style="max-width:100%;"/>');
    },
    checkIn() {
      updateCheckIn({'username': store.state.user.username}).then(res => {
        if (res.status !== 200) {
          alert('打卡失败,请重新打卡')
        } else {
          this.checkInDays = res.data.total_count
          this.consecutiveDays = res.data.continue_count
          this.checkInStatus = true
        }
      });

      // 更新sparkline数据
      this.generateSparklineData();
    },
    getEncouragementText() {
      const texts = [
        "太棒了！你已经养成持续打卡的好习惯，继续保持！",
        "坚持就是胜利！你已经连续打卡一周，加油！",
        "良好的开端！继续保持这个节奏！",
        "迈出了成功的第一步，明天继续来打卡吧！",
        "开始你的打卡之旅，记录每一天的进步！"
      ];

      if (this.consecutiveDays >= 30) return texts[0];
      if (this.consecutiveDays >= 7) return texts[1];
      if (this.consecutiveDays >= 3) return texts[2];
      if (this.consecutiveDays >= 1) return texts[3];
      return texts[4];
    },

    // 添加生成sparkline数据的方法
    generateSparklineData() {
      // 生成随机数据模拟打卡趋势
      this.sparklineData = Array.from({length: 7}, () => Math.floor(Math.random() * 60) + 20).sort((a, b) => a - b);
      // 确保最后一天是最高的（代表今天）
      if (this.sparklineData.length > 0) {
        this.sparklineData[this.sparklineData.length - 1] = 100;
      }
    },

    // 添加获取sparkline颜色的方法
    getSparklineColor(index) {
      const colors = ['#4CAF50', '#66BB6A', '#81C784', '#A5D6A7', '#C8E6C9', '#E8F5E9', '#00C853'];
      return colors[index % colors.length];
    },
    saveCheckInData() {
      const checkInData = {
        checkInDate: this.checkInDate,
        checkInDays: this.checkInDays,
        consecutiveDays: this.consecutiveDays
      };
      localStorage.setItem('userCheckIn', JSON.stringify(checkInData));
    },
    loadCheckInData() {
      const checkInData = JSON.parse(localStorage.getItem('userCheckIn') || '{}');
      if (checkInData.checkInDate) {
        const today = new Date().toDateString();
        // 如果今天已经打过卡
        if (checkInData.checkInDate === today) {
          this.checkInStatus = true;
          this.checkInDate = checkInData.checkInDate;
        }
        this.checkInDays = checkInData.checkInDays || 0;
        this.consecutiveDays = checkInData.consecutiveDays || 0;
      }
    },
    querySalary() {
      if (!this.salaryQuery.position || !this.salaryQuery.location) {
        this.$message.warning('请输入职位和地点');
        return;
      }

      // 模拟查询结果
      this.salaryResults = [
        {position: this.salaryQuery.position, location: this.salaryQuery.location, salary: '15000-25000'},
        {position: this.salaryQuery.position, location: this.salaryQuery.location, salary: '12000-20000'},
        {position: this.salaryQuery.position, location: this.salaryQuery.location, salary: '10000-18000'}
      ];
      this.salaryQueried = true;

      // 实际项目中，这里应该调用API获取薪资数据
      // axios.get('/api/salary', { params: this.salaryQuery }).then(response => {
      //   this.salaryResults = response.data;
      //   this.salaryQueried = true;
      // }).catch(error => {
      //   this.$message.error('查询失败');
      // });
    },
    async querySalary() {
      if (!this.salaryQuery.position || !this.salaryQuery.location) {
        this.$message.warning('请输入职位和地点');
        return;
      }

      try {
        // 这里应该是调用API获取薪资数据
        // 模拟API调用，实际应用中替换为真实的API调用
        const response = await this.mockSalaryApiCall();
        this.salaryResults = response.data;
        this.salaryQueried = true;
      } catch (error) {
        console.error('查询失败:', error);
        this.$message.error('查询失败');
      }
    },

    // 模拟API调用，实际应用中删除此方法并使用真实的API调用
    mockSalaryApiCall() {
      return new Promise(resolve => {
        setTimeout(() => {
          // 模拟数据 - 实际应用中从API获取
          const mockData = [
            {position: this.salaryQuery.position, location: this.salaryQuery.location, salary: '15000-25000'},
            {position: this.salaryQuery.position, location: this.salaryQuery.location, salary: '12000-20000'},
            {position: this.salaryQuery.position, location: this.salaryQuery.location, salary: '10000-18000'}
          ];
          resolve({data: mockData});
        }, 500);
      });
    },
    goToCreatePost(type) {
      this.$router.push({
        path: '/', // 跳转到首页
        query: {
          postType: type, // 传递帖子类型参数
          from: 'creatorCenter' // 来源标记
        }
      });
    },
    getInterviewTypeName(type) {
      const typeMap = {
        text: '文本面试',
        audio: '语音面试',
        video: '视频面试'
      };
      return typeMap[type] || type;
    },
    // 修改 loadInterviewRecords 方法
    loadInterviewRecords() {
      const records = JSON.parse(localStorage.getItem('interviewHistory') || '[]');

      // 初始化统计对象
      const stats = {
        total: records.length,
        types: {
          text: 0,
          audio: 0,
          video: 0
        }
      };

      // 处理面试记录
      this.interviewRecords = records.map(record => {
        // 确保每条记录都有type字段，默认为text
        const type = record.fullReport?.type || 'text';

        // 格式化时间显示
        const date = new Date(record.date || Date.now());
        const formattedTime = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;

        return {
          id: record.date || Date.now().toString(),
          type: type,
          time: formattedTime,
          duration: record.duration || Math.floor(Math.random() * 30) + 10
        };
      });

      // 统计各类面试数量
      this.interviewRecords.forEach(record => {
        if (stats.types[record.type] !== undefined) {
          stats.types[record.type]++;
        }
      });

      this.interviewStats = stats;
    },
    goToHomePublish() {
      this.$router.push('/');
    },

    async fetchUserData() {
      try {
        const response = await axios.get('/api/user/profile');
        this.profileData = response.data;
        this.calculateCompletionRate();
      } catch (error) {
        console.error('获取用户数据失败', error);
      }
    },
    created() {
      this.fetchUserData();
      this.fetchResumeStatus(); // 添加这行
      this.loadCheckInData();
      this.generateSparklineData();

      const today = new Date().toDateString();
      const lastCheckInDate = localStorage.getItem('lastCheckInDate');
      if (lastCheckInDate === today) {
        this.checkInStatus = true;
        this.checkInDate = today;
      }
    },

    // 在UserCenter.vue中修改goToResumeSetting方法
    async goToResumeSetting() {
      try {
        await this.$refs.resumeSetting.openUploadPanel();

        // 添加立即更新UI的逻辑
        this.profileData.hasResume = true;

        // 监听上传成功事件
        const resumeSetting = this.$refs.resumeSetting;
        const handleUploadSuccess = async () => {
          this.$message.success('简历上传成功');
          // 确保状态更新
          this.profileData.hasResume = true;
          // 移除事件监听器
          resumeSetting.$off('upload-success', handleUploadSuccess);
        };

        resumeSetting.$on('upload-success', handleUploadSuccess);

      } catch (error) {
        console.error('操作失败:', error);
        this.$message.error('操作失败');
      }
    },


    async fetchResumeStatus() {
      try {
        // 使用正确的API方法
        const response = await getResumeStatus(store.state.user.username);

        // 更健壮的响应处理
        if (response && response.data) {
          // 明确检查是否有简历数据
          const hasResumeData = response.data.resumeId ||
              response.data.resumeUrl ||
              (response.data instanceof Blob) ||
              (typeof response.data === 'string' && response.data.trim() !== '');

          this.profileData.hasResume = !!hasResumeData;
        } else {
          this.profileData.hasResume = false;
        }
      } catch (error) {
        console.error('获取简历状态失败:', error);
        this.profileData.hasResume = false;
      }
    },

    // 面板控制方法
    openEditPanel() {
      this.showEditPanel = true;
      document.body.style.overflow = 'hidden';
    },
    closeEditPanel() {
      this.showEditPanel = false;
      document.body.style.overflow = '';
    },

    // 完成度计算
    // 修改 UserCenter.vue 中的 calculateCompletionRate 方法
    calculateCompletionRate() {
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
      const rate = Math.round((completedWeight / totalWeight) * 100);
      this.profileData.basicInfo.completionRate = rate;
      return rate;
    },
    // 数据保存方法
    saveToServer() {
      // 模拟API调用
      console.log('保存数据到服务器:', this.profileData);
      // 实际项目中替换为真实的API调用:
      // axios.post('/api/profile', this.profileData)
      //   .then(response => {
      //     console.log('保存成功', response.data);
      //   })
      //   .catch(error => {
      //     console.error('保存失败', error);
      //   });
    },

    // 原有方法
    addWorkExperience() {
      this.profileData.workExperience.push({
        company: '',
        position: '',
        time: '',
        description: ''
      });
    },
    removeWorkExperience(index) {
      this.profileData.workExperience.splice(index, 1);
    },
    addProjectExperience() {
      this.profileData.projectExperience.push({
        name: '',
        role: '',
        time: '',
        description: ''
      });
    },
    removeProjectExperience(index) {
      this.profileData.projectExperience.splice(index, 1);
    },
    addSkill() {
      this.profileData.skills.push({
        name: '',
        level: 50
      });
    },
    removeSkill(index) {
      this.profileData.skills.splice(index, 1);
    },
    getSkillColor(level) {
      if (level >= 80) return '#4CAF50';
      if (level >= 60) return '#2196F3';
      return '#FFC107';
    },
    // 在UserCenter.vue中添加
    // 修改 handleSave 方法
    // 在UserCenter.vue中修改handleSave方法
    async handleSave({section, data}) {
      try {
        // 更新对应section的数据
        Object.assign(this.profileData[section], data);

        // 重新计算完整度
        this.calculateCompletionRate();

        // 保存到服务器
        const apiMap = {
          basicInfo: editUserInfo,
          jobExpectation: editJobInfo
        };

        const response = await apiMap[section]({
          ...this.profileData[section],
          username: this.profileData.basicInfo.nickname
        });

        if (response.status !== 200) {
          throw new Error('保存失败');
        }

        // this.$message.success('个人信息保存成功');
      } catch (error) {
        console.error('保存失败:', error);
        // this.$message.error(error.message || '保存失败，请重试');

        // 恢复数据
        const apiMap = {
          basicInfo: getUserInfo,
          jobExpectation: getJobInfo
        };
        const response = await apiMap[section](store.state.user.username);
        this.profileData[section] = response.data;
        this.calculateCompletionRate();
      }
    },
    async loadComments() {
      try {
        // 替换为实际的API调用
        // const response = await getUserComments(store.state.user.username);
        // this.comments = response.data;

        // 模拟数据 - 实际项目中删除这部分
        this.comments = [
          {
            id: 1,
            postTitle: "如何准备前端面试",
            content: "这篇文章很有帮助，特别是关于Vue.js面试问题的部分！",
            time: "2023-05-15 14:30"
          },
          {
            id: 2,
            postTitle: "后端开发学习路线",
            content: "感谢分享，对新手很有指导意义",
            time: "2023-05-10 09:15"
          }
        ];
      } catch (error) {
        console.error('加载评论失败:', error);
        this.$message.error('加载评论失败');
      }
    },

  },
  created() {
    // 初始化临时数据
    getUserInfo(store.state.user.username).then(res => {
      this.profileData.basicInfo = res.data;
      this.calculateCompletionRate();
    })
    getJobInfo(store.state.user.username).then(res => {
      this.profileData.jobExpectation = res.data;
      this.calculateCompletionRate();
    })

    getInterviewCount({username: store.state.user.username}).then(res => {
      if (res.status !== 200) return;
      this.textInterviewCount = res.data.text;
      this.audioInterviewCount = res.data.audio;
      this.videoInterviewCount = res.data.video;
      this.QACount = res.data.qa;
    })
    getCheckIn({username: store.state.user.username}).then(res => {
      if (res.status !== 200) return;
      this.checkInDays = res.data.total_count
      this.consecutiveDays = res.data.continue_count
      this.checkInStatus = res.data.is_checked_in
      this.generateSparklineData();
    });
      // 检查是否为首次注册
  if (this.firstRegister) {
    this.showWelcomeMessage = true;
    setTimeout(() => {
      this.showWelcomeMessage = false;
    }, 30000); // 30秒后自动关闭
  }

  },
  beforeDestroy() {
    document.body.style.overflow = '';
  },

  getStatusText(status) {
    const statusMap = {
      pending: '待处理',
      rejected: '已拒绝',
      accepted: '已通过'
    };
    return statusMap[status] || status;
  },

   async mounted() {
    this.loading = true;
    this.error = null;
    try {
      const res = await getExperience({
        username: store.state.user.username
      });
      if (res.status === 200) {
        this.postList = res.data;
        this.isExpanded = new Array(this.postList.length).fill(false);
        this.sortPostsByTime(); // 调用排序方法
      }
    } catch (error) {
      console.error('获取经验分享失败:', error);
      this.error = '获取经验分享失败';
      this.$message.error('获取经验分享失败');
    } finally {
      this.loading = false;
    }
  }
}
</script>
<style scoped>

/* 导航标签栏样式 */
.tab-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.tab-item {
  padding: 4px 8px;
  font-size: 14px;
  color: #999;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
  background: none;
  border: none;
}

.tab-item:after {
  content: '';
  position: absolute;
  bottom: -11px;
  left: 0;
  width: 100%;
  height: 2px;
  background: transparent;
  transition: all 0.2s;
}

.tab-item.active {
  color: #32ca99;
  font-weight: bold;
}

.tab-item.active:after {
  background: #32ca99;
}

.tab-item:hover:not(.active) {
  color: #777;
}

/* 内容展示区样式 */
.content-section {
  background-color: #fff;
  border-radius: 12px;
  padding: 30px;
  min-height: 500px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
}

.post-item {
  padding: 20px 0;
  border-bottom: 1px solid #f0f0f0;
  transition: background-color 0.2s;
}

.post-item:hover {
  background-color: #f9f9f9;
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.avatar {
  width: 25px;
  height: 20px;
  border-radius: 50%;
  background-color: #f0f0f0;
  margin-right: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-user-default {
  display: inline-block;
  width: 24px;
  height: 24px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23999'%3E%3Cpath d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z'/%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.user-details {
  flex: 1;
  min-width: 0;
}

.username {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-level {
  display: inline-block;
  padding: 0 4px;
  margin-left: 6px;
  background-color: #e8f5e9;
  border-radius: 2px;
  font-size: 10px;
  color: #2E8B57;
}

.post-meta {
  font-size: 12px;
  color: #999;
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}

.post-meta span {
  margin-right: 12px;
  position: relative;
}

.post-meta span:not(:last-child):after {
  content: '•';
  position: absolute;
  right: -6px;
}

.post-title {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: #333;
  line-height: 1.4;
}

.post-content {
  margin: 0;
  font-size: 14px;
  color: #333;
  line-height: 1.5;
}

.read-more {
  float: right;
  color: #3CB371;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.read-more:hover {
  color: #2E8B57;
  text-decoration: underline;
}

/* 空状态样式 */
.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  color: #999;
}

.empty-icon {
  width: 120px;
  height: 120px;
  margin-bottom: 20px;
  opacity: 0.6;
}

.empty-text {
  font-size: 16px;
  margin: 0;
}

/* 分页样式 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  padding: 10px 0;
}

.page-btn {
  padding: 6px 12px;
  margin: 0 5px;
  border: 1px solid #ddd;
  background-color: #fff;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) {
  background-color: #f5f5f5;
  border-color: #32ca99;
  color: #32ca99;
}

.page-btn:disabled {
  color: #ccc;
  cursor: not-allowed;
}

.page-number {
  margin: 0 2px;
}

.page-link {
  padding: 4px 8px;
  margin: 0 2px;
  border: 1px solid #ddd;
  background-color: #fff;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  min-width: 30px;
}

.page-link:hover:not(.active) {
  border-color: #32ca99;
  color: #32ca99;
}

.page-link.active {
  background-color: #32ca99;
  color: white;
  border-color: #32ca99;
}

.section-header h3 {
  flex: 1;
  margin: 0;
  font-size: 16px;
  font-weight: 500;
}

.edit-btn {

  background-color: #00dcb5;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 6px 12px;
  font-size: 14px;
  cursor: pointer;
}


.link {
  color: #00dcb5;
  cursor: pointer;
}

/* 输入框圆角样式 */

.edit-input:focus {
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
  outline: none;
}

.btn-primary {
  background: linear-gradient(to right, #4CAF50, #66BB6A);
  box-shadow: 0 2px 6px rgba(76, 175, 80, 0.2);
}


/* 基础按钮样式 - 圆角优化 */
.btn {

  border-radius: 8px; /* 统一8px圆角 */
  padding: 10px 24px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s ease;
  border: 1px solid transparent;
}


.save-btn:hover {
  background-color: #00dcb5;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3);
}


/* 响应式设计 */
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

/* 基础样式 */
.profile-container {

  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  color: #333;
  min-height: 100vh;
  padding: 30px 0;
  margin-left: -110px;
}

/* 主体内容区 */
.profile-content {

  margin-top: 0.5rem;
  display: flex;
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 30px;
  gap: 30px;
}

.main-content {
  margin-top: 0.5rem;
  flex: 1;
  min-width: 0;
}

.sidebar {
  margin-top: 0.5rem;
  width: 300px;
  min-width: 300px;
  margin-right: -120px;
}

/* 个人信息模块 */
.profile-info {

  background-color: #fff;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  margin-bottom: 30px;
}

.avatar-section {
  display: flex;
  margin-bottom: 25px;
}

.avatar {
  width: 50px !important;
  height: 50px !important;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 25px;
  border: 4px solid #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.basic-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px; /* 增加子元素之间的间距 */
}

.username {
  font-size: 26px;
  font-weight: 400;
  margin: 6px 0; /* 增加上下边距 */
  padding: 8px 0; /* 增加内边距 */
  font-family: Arial, sans-serif;
  line-height: 1; /* 增加行高 */
}

.name-text {
  letter-spacing: 5px; /* 根据需要调整 */
  margin: 0 5px; /* 增加左右外边距 */
}

.badge {
  font-size: 16px;
  font-weight: normal;
  color: #666;
  background-color: #f0f0f0;
  padding: 4px 12px;
  border-radius: 6px;
  margin-left: 10px;
}

.auth-status {
  margin-bottom: 15px;
}

.auth-text {
  color: #666;
  font-size: 16px;
}

.auth-link {
  color: #1e88e5;
  font-size: 16px;
  text-decoration: none;
  margin-left: 10px;
}

.detail-info {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 15px;
  font-size: 16px;
  color: #666;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.detail-item svg {
  fill: #666;
}

.add-intro {
  color: #999;
  font-size: 16px;
  text-decoration: underline;
}

.stats-section {
  display: flex;
  justify-content: space-around;
  margin-bottom: 25px;
  padding: 20px 0;
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 6px;
}

.stat-label {
  font-size: 16px;
  color: #666;
  margin-top: 2vh;
}

.action-buttons {
  display: flex;
  gap: 20px;
}

.profile-btn {
  flex: 1;
  padding: 15px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.complete-btn {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.edit-link {
  color: #1e88e5;
  margin-left: 10px;
}

.resume-btn {
  background-color: #00dcb5;
  color: white;
  position: relative;
}

.status-badge {
  position: absolute;
  top: -10px;
  right: -10px;
  background-color: #ff3d00;
  color: white;
  font-size: 14px;
  padding: 3px 8px;
  border-radius: 12px;
}

/* 内容展示区 */
.content-section {
  background-color: #fff;
  border-radius: 12px;
  padding: 30px;
  min-height: 400px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
}

.tab-content {
  width: 100%;
}

.empty-content {
  text-align: center;
  padding: 40px 0;
}

.empty-icon {
  width: 120px;
  height: 120px;
  margin-bottom: 20px;
  opacity: 0.6;
}

.empty-text {
  font-size: 16px;
  color: #666;
  margin-bottom: 25px;
}

/* 内容列表样式 */
.content-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.content-item {
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.content-item h3 {
  margin: 0 0 10px 0;
  font-size: 18px;
}

.content-meta {
  display: flex;
  gap: 15px;
  font-size: 14px;
  color: #999;
  margin-top: 10px;
}

/* 评论列表样式 */
.comment-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.comment-item {
  padding: 15px;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
  color: #666;
}

.comment-content {
  margin: 0;
  line-height: 1.6;
}

/* 投递记录表格样式 */
.application-list table {
  width: 100%;
  border-collapse: collapse;
}

.application-list th,
.application-list td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.application-list th {
  font-weight: 500;
  color: #666;
}

.status-pending {
  color: #ff9800;
}

.status-rejected {
  color: #f44336;
}

.status-accepted {
  color: #4caf50;
}

/* 刷题统计样式 */
.practice-stats {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  flex: 1;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 8px;
  text-align: center;
}

.stat-card .stat-number {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 5px;
}

/* 练习记录样式 */
.practice-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.practice-item {
  display: flex;
  align-items: center;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.question-info {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 10px;
}

.difficulty {
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.difficulty-1 {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.difficulty-2 {
  background-color: #fff8e1;
  color: #ff8f00;
}

.difficulty-3 {
  background-color: #ffebee;
  color: #c62828;
}

.result {
  width: 60px;
  text-align: center;
  font-weight: 500;
}

.result-true {
  color: #4caf50;
}

.result-false {
  color: #f44336;
}

.practice-time {
  width: 120px;
  text-align: right;
  font-size: 14px;
  color: #666;
}

/* 收藏标签样式 */
.favorite-tabs {
  display: flex;
  margin-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.favorite-tabs button {
  padding: 10px 20px;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  font-size: 16px;
  color: #666;
}

.favorite-tabs button.active {
  color: #00dcb5;
  border-bottom-color: #00dcb5;
  font-weight: 500;
}

/* 导航标签栏 */
.tab-bar {
  background-color: #fff;
  border-radius: 12px;
  padding: 0 25px;
  margin-bottom: 30px;
  display: flex;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
}

.tab-item {
  padding: 12px 24px;
  border: none;
  background: none;
  font-size: 16px;
  color: #666;
  cursor: pointer;
  position: relative;
  transition: all 0.3s ease;
  margin: 0 4px;
  border-radius: 8px;
}

.tab-item:hover {
  color: #00dcb5;
  background-color: rgba(0, 220, 181, 0.1);
}

.tab-item.active {
  color: #00dcb5;
  font-weight: 500;
  background-color: rgba(0, 220, 181, 0.1);
}

/* 过渡效果 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.tab-item.active:after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 40%;
  transform: translateX(-30%);
  width: 100px;
  height: 6px;
  background-color: #00dcb5;
  border-radius: 4px 4px 0 0;
}

/* 内容展示区 */
.content-section {
  background-color: #fff;
  border-radius: 12px;
  padding: 30px;
  min-height: 400px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.empty-content {
  text-align: center;
}

.empty-icon {
  width: 150px;
  height: 150px;
  margin-bottom: 25px;
}

.empty-text {
  font-size: 16px;
  color: #666;
  margin-bottom: 25px;
}

.publish-btn {
  padding: 12px 30px;
  background-color: #00dcb5;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.publish-btn:hover {
  background-color: #00c7a3;
  transform: translateY(-2px);
}

/* 右侧边栏 */
.sidebar-card {
  background-color: #fff;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
}

.card-title {
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 20px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-link {
  font-size: 16px;
  font-weight: normal;
  color: #1e88e5;
  text-decoration: none;
}

.creator-actions {
  display: flex;
  gap: 15px;
}

.creator-btn {
  flex: 1;
  padding: 10px;
  border: 1px solid #eee;
  border-radius: 2px;
  font-size: 16px;
  background: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.creator-btn svg {
  fill: #00dcb5;
}

.activity-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.activity-item {
  padding: 12px 0;
  border-bottom: 1px solid #eee;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-item a {
  color: #333;
  text-decoration: none;
  font-size: 16px;
  display: block;
}

.tool-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 0;
  border-bottom: 1px solid #eee;
  font-size: 16px;
}

.tool-item:last-child {
  border-bottom: none;
}

.tool-item svg {
  fill: #00dcb5;
}

.tool-status {
  margin-left: auto;
  color: #ff3d00;
  font-size: 14px;
}

/* 响应式设计 */
@media (max-width: 100px) {
  .profile-content {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    min-width: auto;
  }
}

@media (max-width: 800px) {
  .avatar-section {
    flex-direction: column;
  }

  .avatar {
    margin-right: 0;
    margin-bottom: 5px;
  }

  .action-buttons {
    flex-direction: column;
  }

  .tab-bar {
    overflow-x: auto;
    padding: 0;
  }

  .tab-item {
    white-space: nowrap;
  }

  .profile-info,
  .sidebar-card {
    padding: 10px;
  }
}

@media (max-width: 768px) {
  .profile-content {
    flex-direction: column;
  }

  .main-content {
    margin-right: 0;
    margin-bottom: 20px;
  }

  .sidebar {
    width: 100%;
  }
}

@media (max-width: 768px) {
  .avatar-section {
    flex-direction: column;
  }

  .avatar {
    margin-right: 0;
    margin-bottom: 15px;
  }

  .action-buttons {
    flex-direction: column;
  }

  .tab-bar {
    overflow-x: auto;
    padding: 0;
  }

  .tab-item {
    white-space: nowrap;
  }
}

.status-badge {
  position: absolute;
  top: -10px;
  right: -10px;
  font-size: 14px;
  padding: 3px 8px;
  border-radius: 12px;
}

.badge-success {
  background-color: #00dcb5;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.comment-item {
  padding: 15px;
  border-radius: 8px;
  background-color: #f9f9f9;
  transition: all 0.3s ease;
}

.comment-item:hover {
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
  color: #666;
}

.comment-post {
  font-weight: 500;
  color: #333;
}

.comment-time {
  color: #999;
}

.comment-content {
  margin: 0;
  line-height: 1.6;
  color: #333;
  word-break: break-word;
}

.comment-from {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.from-user {
  color: #1e88e5;
  font-weight: 500;
}

/* 添加面试记录相关样式 */
.interview-stats {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
}

.interview-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.interview-item {
  display: flex;
  align-items: center;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.interview-type {
  width: 100px;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 14px;
  text-align: center;
}

.interview-type.type-text {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.interview-type.type-audio {
  background-color: #e3f2fd;
  color: #1976d2;
}

.interview-type.type-video {
  background-color: #fce4ec;
  color: #c2185b;
}

.interview-time {
  flex: 1;
  margin-left: 20px;
  font-size: 14px;
  color: #666;
}

.interview-duration {
  width: 100px;
  text-align: right;
  font-size: 14px;
  color: #666;
}

.stat-card {
  flex: 1;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 8px;
  text-align: center;
}

.stat-card .stat-number {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 5px;
}

/* 添加打卡按钮样式 */
.check-in-btn {
  margin-left: 10px;
  padding: 4px 10px;
  background-color: #00dcb5;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
}

.check-in-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.checked-in {
  color: #00dcb5;
}

/* 添加打卡数据高亮样式 */
.check-in-stats {
  margin-top: 20px;
  padding: 16px;
  background-color: #f8fdff;
  border-radius: 12px;
  border: 1px solid #e1f5fe;
  font-size: 16px;
}

.consecutive-days {
  margin-bottom: 12px;
  color: #333;
}

.total-days {
  margin-bottom: 12px;
  color: #333;
}

.highlight-text {
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 4px;
  margin: 0 2px;
  display: inline-block;
}

.consecutive-highlight {
  background-color: #ffecb3;
  color: #ff6f00;
  font-size: 18px;
}

.total-highlight {
  background-color: #e1f5fe;
  color: #0288d1;
  font-size: 18px;
}

.fire-icon {
  margin-right: 4px;
  font-size: 18px;
}

.encouragement {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px dashed #b3e5fc;
  color: #0288d1;
  font-size: 14px;
  font-weight: 500;
}

/* 添加新的样式 */
.achievement-wall {
  display: flex;
  gap: 20px;
  margin: 20px 0;
  flex-wrap: wrap;
}

.achievement-card {
  flex: 1;
  min-width: 200px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  padding: 20px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.achievement-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
}

.achievement-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
}

.achievement-card.consecutive::before {
  background: linear-gradient(90deg, #4ECDC4, #44A08D);
}

.achievement-card.total::before {
  background: linear-gradient(90deg, #4ECDC4, #44A08D);
}

.card-icon {
  width: 50px;
  height: 50px;
  background: rgba(0, 220, 181, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
}

.card-icon svg {
  fill: #00dcb5;
}

.card-content {
  flex: 1;
}

.card-title {
  font-size: 14px;
  color: #666;
  margin-bottom: 4px;
  font-weight: 500;
}

.card-value {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  line-height: 1.2;
}

.unit {
  font-size: 14px;
  color: #999;
  margin-left: 4px;
}

.progress-bar {
  height: 6px;
  background: #f0f0f0;
  border-radius: 3px;
  margin-top: 8px;
  overflow: hidden;
}

.progress {
  height: 100%;
  border-radius: 3px;
  background: linear-gradient(90deg, #00dcb5, #00c7a3);
  transition: width 0.8s ease;
}

.sparkline {
  display: flex;
  align-items: flex-end;
  height: 30px;
  margin-top: 8px;
  gap: 2px;
}

.sparkline-bar {
  flex: 1;
  border-radius: 2px 2px 0 0;
  transition: all 0.3s ease;
  min-width: 4px;
}

.sparkline-bar:hover {
  transform: scaleY(1.2);
}

.encouragement {
  margin-top: 15px;
  padding: 12px;
  background: linear-gradient(90deg, #e3f2fd, #bbdefb);
  border-radius: 8px;
  color: #1976D2;
  font-size: 14px;
  font-weight: 500;
  line-height: 1.6;
  text-align: center;
  border-left: 4px solid #1976D2;
  position: relative;
  overflow: hidden;
}

.encouragement::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  animation: shine 3s infinite;
}

@keyframes shine {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

/* 响应式调整 */
@media (max-width: 768px) {
  .achievement-wall {
    flex-direction: column;
  }

  .achievement-card {
    width: 100%;
  }

  .card-value {
    font-size: 24px;
  }
}

/* 薪资查询样式 */
.query-form.vertical {
  flex-direction: column;
  gap: 10px;
}

.salary-query {
  width: 100%;
  margin-top: 10px;
}

.salary-query h4 {
  margin: 0 0 12px 0;
  font-size: 16px;
  color: #333;
}

.query-form {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.query-input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.query-btn {
  width: 4rem;
  margin-left: 6rem;

  padding: 8px 16px;
  background-color: #00dcb5;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
}

.salary-results {
  margin-top: 10px;
  font-size: 14px;
}

.result-item {
  padding: 12px 8px;
  background-color: #f9f9f9;
  border-radius: 4px;
  margin-bottom: 8px;
  line-height: 1.6;
}

.no-results {
  color: #999;
  font-size: 14px;
  text-align: center;
  padding: 10px;
}

.result-summary {
  padding: 10px;
  background-color: #e8f5e9;
  border-radius: 4px;
  margin-bottom: 10px;
  font-weight: 500;
  color: #2e7d32;
  line-height: 1.6;
}
/* 内容展示区样式 */
.content-display {
  margin-top: 20px;
}

.post-item {
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}

.post-title {
  margin: 10px 0;
  font-size: 18px;
  font-weight: bold;
}

.post-content {
  margin: 10px 0;
  line-height: 1.6;
  color: #333;
}

.read-more {
  color: #32ca99;
  cursor: pointer;
  margin-left: 5px;
}

.empty-state {
  text-align: center;
  padding: 40px 0;
  color: #999;
}

.empty-icon {
  font-size: 50px;
  margin-bottom: 15px;
}

.empty-text {
  font-size: 16px;
}

/* 分页样式 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  padding: 10px 0;
}

.page-btn {
  padding: 6px 12px;
  margin: 0 5px;
  border: 1px solid #ddd;
  background-color: #fff;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) {
  background-color: #f5f5f5;
  border-color: #32ca99;
  color: #32ca99;
}

.page-btn:disabled {
  color: #ccc;
  cursor: not-allowed;
}

.page-number {
  margin: 0 2px;
}

.page-link {
  padding: 4px 8px;
  margin: 0 2px;
  border: 1px solid #ddd;
  background-color: #fff;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  min-width: 30px;
}

.page-link:hover:not(.active) {
  border-color: #32ca99;
  color: #32ca99;
}

.page-link.active {
  background-color: #32ca99;
  color: white;
  border-color: #32ca99;
}

/* 标签栏样式 */
.tab-bar {
  display: flex;
  border-bottom: 1px solid #eee;
  margin-bottom: 20px;
}

.tab-item {
  padding: 10px 20px;
  cursor: pointer;
  font-size: 16px;
  color: #666;
  position: relative;
}

.tab-item.active {
  color: #32ca99;
}

.tab-item.active:after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 20px;
  right: 20px;
  height: 3px;
  background-color: #32ca99;
}
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  padding: 10px 0;
  
  .page-btn {
    padding: 6px 12px;
    margin: 0 5px;
    border: 1px solid #ddd;
    background-color: #fff;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s;
    
    &:hover:not(:disabled) {
      background-color: #f5f5f5;
      border-color: #32ca99;
      color: #32ca99;
    }
    
    &:disabled {
      color: #ccc;
      cursor: not-allowed;
    }
  }
  
  .page-info {
    margin: 0 15px;
    font-size: 14px;
    color: #666;
  }
}
/* 添加页码按钮样式 */
.page-number {
  margin: 0 2px;
  
  .page-link {
    padding: 4px 8px;
    margin: 0 2px;
    border: 1px solid #ddd;
    background-color: #fff;
    border-radius: 4px;
    cursor: pointer;
    font-size: 12px;
    min-width: 30px;
    
    &:hover:not(.active) {
      border-color: #32ca99;
      color: #32ca99;
    }
    
    &.active {
      background-color: #32ca99;
      color: white;
      border-color: #32ca99;
    }
  }
}
.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  padding: 10px;
  gap: 15px;
}

.page-btn {
  padding: 8px 16px;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) {
  background-color: #32ca99;
  color: white;
  border-color: #32ca99;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-size: 14px;
  color: #666;
}
.welcome-message {
  position: fixed;
  top: 30%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
  max-width: 350px;
  animation: fadeIn 0.3s ease-out;
}

.message-content {
  position: relative;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border-left: 4px solid #26bd98;
}

.message-content h3 {
  margin: 0 0 10px 0;
  font-size: 18px;
  color: #333;
}

.message-content p {
  margin: 0;
  font-size: 14px;
  color: #666;
  line-height: 1.5;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 20px;
  color: #999;
  cursor: pointer;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s;
}

.close-btn:hover {
  background-color: #f0f0f0;
  color: #666;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

</style>