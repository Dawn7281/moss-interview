<template>
  <div class="experience-container">
    <!-- 经验分享部分 -->
    <div class="experience-sharing">
      <div class="post-type-buttons">
        <button 
          class="post-btn dynamic-btn"
          :class="{ active: postType === 'dynamic' }"
          @click="setPostType('dynamic')"
        >
          发动态
        </button>
        <button 
          class="post-btn article-btn"
          :class="{ active: postType === 'article' }"
          @click="setPostType('article')"
        >
          写文章
        </button>
        <button 
          class="post-btn referral-btn"
          :class="{ active: postType === 'referral' }"
          @click="setPostType('referral')"
        >
          发内推
        </button>
        <a href="#" class="travel-link">快抓住学生最后一个长假，背上行囊开启旅行 </a>
      </div>

       <div class="content-input">
         <input
          v-if="postType === 'article'"
          v-model="title"
          placeholder="输入文章标题"
          class="title-input"
         >
         <textarea
          v-model="content"
          :placeholder="postType === 'dynamic' ? '此刻你想和大家分享什么' : postType === 'article' ? '写下你的文章内容' : '输入内推信息'"
          class="post-textarea"
         ></textarea>
      </div>

  <!-- 添加打卡内容预览区域 -->
      <div v-if="draftCheckIn" class="draft-checkin-preview">
        <div class="draft-header">
          <span>打卡草稿</span>
          <button class="delete-draft-btn" @click="deleteDraftCheckIn">×</button>
        </div>
        <div class="draft-content">
          {{ draftCheckIn }}
        </div>
      </div>

      <div class="function-icons">
        <div class="icon-item" @click="toggleEmojiPanel">
          <i class="icon-smile"></i>
          <span class="icon-label">表情</span>
          <div v-if="showEmojiPanel" class="emoji-panel">
            <div class="emoji-categories">
              <span 
                v-for="(category, index) in categories" 
                :key="index"
                class="category-item"
                :class="{ active: activeCategory === category.key }"
                @click.stop="switchEmojiCategory(category.key, $event)" 
              >
                {{ category.name }}
              </span>
            </div>
            <div class="emoji-content">
              <div 
                v-for="(emojiGroup, index) in categorizedEmojis" 
                :key="index"
                class="emoji-group"
              >
                <div class="group-title" v-if="emojiGroup.category">{{ emojiGroup.category }}</div>
                <div class="emoji-grid">
                  <span 
                    v-for="(emoji, emojiIndex) in emojiGroup.emojis" 
                    :key="emojiIndex" 
                    class="emoji-item"
                    @click="selectEmoji(emoji)"
                  >
                    {{ emoji }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="icon-item" @click="uploadImage">
          <i class="icon-camera"></i>
          <span class="icon-label">图片</span>
        </div>
       <!-- 打卡图标 -->
       <div class="icon-item" @click="recordCheckIn">
         <i class="icon-check">
           <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#000000">
             <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/>
           </svg>
         </i>
         <span class="icon-label">打卡</span>
       </div>
  
       <!-- 发内推图标（使用原有briefcase图标） -->
       <div class="icon-item" @click="quickReferral">
         <i class="icon-briefcase">
           <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#000000">
             <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
           </svg>
         </i>
         <span class="icon-label">发内推</span>
       </div>
  
       <!-- 职位图标 -->
       <div class="icon-item" @click="postJob">
         <i class="icon-contentType">
           <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#000000">
             <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
           </svg>
         </i>
         <span class="icon-label">职位</span>
       </div>
  
       <button class="publish-btn" @click="handlePublish">
         发布
       </button>
      </div>

      <SalaryDialog v-model:visible="showSalaryDialog" @update:visible="closeSalaryDialog" />

 <!-- 打卡对话框 -->
      <div v-if="showCheckInDialog" class="check-in-dialog-overlay" @click.self="showCheckInDialog = false">
        <div class="check-in-dialog">
          <h3>今日打卡</h3>
          <textarea 
            v-model="checkInContent" 
            placeholder="分享你的学习心得或今日收获..."
            class="check-in-textarea"
          ></textarea>
          <div class="dialog-actions">
            <button class="cancel-btn" @click="showCheckInDialog = false">取消</button>
            <button class="confirm-btn" @click="saveDraftCheckIn">保存草稿</button>
            <button class="confirm-btn" @click="handleCheckInSubmit">直接打卡</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 经验展示部分 -->
    <div class="experience-display">
      
      <div class="tab-bar">
        <span class="tab-item" :class="{ active: activeTab === 'comprehensive' }" @click="activeTab = 'comprehensive'">综合</span>
        <span class="tab-item" :class="{ active: activeTab === 'dynamic' }" @click="activeTab = 'dynamic'">动态</span>
        <span class="tab-item" :class="{ active: activeTab === 'article' }" @click="activeTab = 'article'">文章</span>
        <span class="tab-item" :class="{ active: activeTab === 'referral' }" @click="activeTab = 'referral'">内推</span>
        <div class="tab-actions">
          <i class="icon-check-mark"></i>
          <i class="icon-close"></i>
          <i class="icon-refresh"></i>
        </div>
      </div>

      <div class="content-display">
        <template v-if="filteredPosts.length > 0">
        <div
          class="post-item"
          v-for="(item, idx) in filteredPosts"
          :key="item.id"
        >
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
          <h3 class="post-title">{{ item.title }}</h3>
          <p class="post-content">
            <span v-html="isExpanded[idx] ? item.fullContent || item.content : item.content"></span>
            <a href="#" class="read-more" @click.prevent="toggleExpand(idx)">
              {{ isExpanded[idx] ? '收起' : '查看更多' }}
            </a>
          </p>
        </div>
         </template>
          <div v-else class="empty-state">
           <i class="empty-icon">📝</i>
           <p class="empty-text">暂无内容，快来发布第一条动态吧！</p>
          </div>
      </div>
      <div class="pagination" v-if="totalPages > 1">
  <button 
    @click="goToPage(currentPage - 1)" 
    :disabled="currentPage === 1"
    class="page-btn"
  >
    上一页
  </button>
  
  <span class="page-number" v-for="page in totalPages" :key="page">
    <button 
      @click="goToPage(page)"
      :class="{ active: page === currentPage }"
      class="page-link"
    >
      {{ page }}
    </button>
  </span>
  
  <button 
    @click="goToPage(currentPage + 1)" 
    :disabled="currentPage === totalPages"
    class="page-btn"
  >
    下一页
  </button>
</div>
    </div>
  </div>

  <!-- 添加职位对话框 -->
<div v-if="showJobDialog" class="job-dialog-overlay" @click.self="showJobDialog = false">
  <div class="job-dialog">
    <h3>发布职位</h3>
    <div class="form-group">
      <label>职位名称</label>
      <input v-model="jobForm.title" placeholder="例如：Java开发工程师" class="form-input">
    </div>
    <div class="form-group">
      <label>公司名称</label>
      <input v-model="jobForm.company" placeholder="例如：腾讯" class="form-input">
    </div>
    <div class="form-group">
      <label>薪资范围</label>
      <input v-model="jobForm.salary" placeholder="例如：15k-25k" class="form-input">
    </div>
    <div class="form-group">
      <label>工作地点</label>
      <input v-model="jobForm.location" placeholder="例如：北京" class="form-input">
    </div>
    <div class="form-group">
      <label>职位描述</label>
      <textarea v-model="jobForm.description" placeholder="描述职位要求和职责" class="form-textarea"></textarea>
    </div>
    <div class="form-group">
      <label>联系方式</label>
      <input v-model="jobForm.contact" placeholder="邮箱或电话" class="form-input">
    </div>
    <div class="dialog-actions">
      <button class="cancel-btn" @click="showJobDialog = false">取消</button>
      <button class="confirm-btn" @click="submitJobPost">发布</button>
    </div>
  </div>
</div>
</template>

<script>
import store from "@/store";
import {addExperience, listExperiences} from "@/api/experience";
export default {
  name: 'ExperiencePost',

  data() {
    return {
      postType: 'dynamic',
      title: '',
      content: '',
      activeTab: 'comprehensive',
      selectedImages: [],
      selectedCircle: null,
      previewContent: '',
      isExpanded: [],
      showEmojiPanel: false,
      activeCategory: 'all',
      salaryItems: [],
      showCheckInDialog: false,
      checkInContent: '',
      draftCheckIn: '', // 存储打卡草稿内容
      tempCheckInContent: '',
      // 职位相关数据
      showJobDialog: false,
      currentPage: 1, // 当前页码
      pageSize: 5, // 每页显示条数
      totalPages: 1, // 总页数（计算得出）
      jobForm: {
        title: '',
        company: '',
        salary: '',
        location: '',
        description: '',
        contact: ''
      },
      categories: [
        { key: 'all', name: '全部' },
        { key: 'face', name: '表情' },
        { key: 'gesture', name: '手势' },
        { key: 'animal', name: '动物' },
        { key: 'food', name: '食物' },
        { key: 'sport', name: '运动' },
        { key: 'object', name: '物品' }
      ],
      emojiList: [
        { emoji: '😊', category: 'face' },
        { emoji: '😂', category: 'face' },
        { emoji: '😍', category: 'face' },
        { emoji: '😎', category: 'face' },
        { emoji: '🤩', category: 'face' },
        { emoji: '😢', category: 'face' },
        { emoji: '😡', category: 'face' },
        { emoji: '😱', category: 'face' },
        { emoji: '🤔', category: 'face' },
        { emoji: '😴', category: 'face' },
        
        { emoji: '👍', category: 'gesture' },
        { emoji: '👎', category: 'gesture' },
        { emoji: '👏', category: 'gesture' },
        { emoji: '💪', category: 'gesture' },
        { emoji: '👌', category: 'gesture' },
        { emoji: '✌️', category: 'gesture' },
        { emoji: '🤝', category: 'gesture' },
        { emoji: '🙏', category: 'gesture' },
        { emoji: '🤗', category: 'gesture' },
        { emoji: '🤭', category: 'gesture' },
        
        { emoji: '🐶', category: 'animal' },
        { emoji: '🐱', category: 'animal' },
        { emoji: '🐭', category: 'animal' },
        { emoji: '🐹', category: 'animal' },
        { emoji: '🐰', category: 'animal' },
        { emoji: '🦊', category: 'animal' },
        { emoji: '🐻', category: 'animal' },
        { emoji: '🐼', category: 'animal' },
        { emoji: '🦁', category: 'animal' },
        { emoji: '🐮', category: 'animal' },
        
        { emoji: '🍎', category: 'food' },
        { emoji: '🍊', category: 'food' },
        { emoji: '🍌', category: 'food' },
        { emoji: '🍉', category: 'food' },
        { emoji: '🍇', category: 'food' },
        { emoji: '🍓', category: 'food' },
        { emoji: '🍒', category: 'food' },
        { emoji: '🍑', category: 'food' },
        { emoji: '🥭', category: 'food' },
        { emoji: '🍍', category: 'food' },
        
        { emoji: '⚽️', category: 'sport' },
        { emoji: '🏀', category: 'sport' },
        { emoji: '🏈', category: 'sport' },
        { emoji: '⚾️', category: 'sport' },
        { emoji: '🎾', category: 'sport' },
        { emoji: '🏐', category: 'sport' },
        { emoji: '🏉', category: 'sport' },
        { emoji: '🎱', category: 'sport' },
        { emoji: '🎳', category: 'sport' },
        { emoji: '🏓', category: 'sport' },
        
        { emoji: '❤️', category: 'object' },
        { emoji: '💔', category: 'object' },
        { emoji: '💕', category: 'object' },
        { emoji: '💖', category: 'object' },
        { emoji: '💗', category: 'object' },
        { emoji: '💓', category: 'object' },
        { emoji: '💘', category: 'object' },
        { emoji: '💝', category: 'object' },
        { emoji: '💟', category: 'object' },
        { emoji: '❣️', category: 'object' },
        { emoji: '🎉', category: 'object' },
        { emoji: '🎊', category: 'object' },
        { emoji: '🎁', category: 'object' },
        { emoji: '🎈', category: 'object' },
        { emoji: '🎄', category: 'object' },
        { emoji: '🎃', category: 'object' },
        { emoji: '👻', category: 'object' },
        { emoji: '🎅', category: 'object' },
        { emoji: '🤶', category: 'object' }
      ],
      postList: [
        {
          id: 1,
          username: '面渣的幻想',
          level: 'LV.4',
          time: '06 - 11 16:44',
          school: '清华大学',
          contentType: '文章',
          title: '再也不用写代码了哈哈哈哈哈哈',
          content: '被烟草录取的那一天，我感觉整个人都飘起来了...'
        }
      ]
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
    categorizedEmojis() {
      if (this.activeCategory === 'all') {
        const groups = {};
        this.emojiList.forEach(item => {
          if (!groups[item.category]) {
            groups[item.category] = [];
          }
          groups[item.category].push(item.emoji);
        });
        
        return Object.keys(groups).map(category => ({
          category: this.getCategoryName(category),
          emojis: groups[category]
        }));
      }
      
      return [{
        category: this.getCategoryName(this.activeCategory),
        emojis: this.emojiList
          .filter(item => item.category === this.activeCategory)
          .map(item => item.emoji)
      }];
    }
  },
  methods: {
  goToPage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
    
     // 职位相关方法
  postJob() {
    this.resetJobForm();
    this.showJobDialog = true;
  },

  submitJobPost() {
    if (!this.validateJobForm()) {
      return;
    }
    
    // 设置职位类型
    this.postType = 'job';
    
    // 填充标题和内容
    this.title = `${this.jobForm.company}招聘：${this.jobForm.title}`;
    this.content = `
     职位名称：${this.jobForm.title}
     公司名称：${this.jobForm.company}
     薪资范围：${this.jobForm.salary}
     工作地点：${this.jobForm.location}
     职位描述：${this.jobForm.description}
     联系方式：${this.jobForm.contact}
         `.trim();
    
         this.showJobDialog = false;
    
    // 自动切换到文章类型以便显示完整信息
    this.setPostType('article');
  },

  validateJobForm() {
    if (!this.jobForm.title.trim()) {
      alert('请填写职位名称');
      return false;
    }
    if (!this.jobForm.company.trim()) {
      alert('请填写公司名称');
      return false;
    }
    return true;
  },

  resetJobForm() {
    this.jobForm = {
      title: '',
      company: '',
      salary: '',
      location: '',
      description: '',
      contact: ''
    };
  },
   
      // 修改打卡相关方法
    recordCheckIn() {
      this.tempCheckInContent = this.draftCheckIn; // 加载草稿内容到临时变量
      this.checkInContent = this.tempCheckInContent || '';
      this.showCheckInDialog = true;
    },
    
    // 保存为草稿
    saveDraftCheckIn() {
      if (!this.checkInContent.trim()) {
        alert('请输入打卡内容');
        return;
      }
      this.draftCheckIn = this.checkInContent;
      this.tempCheckInContent = this.checkInContent;
      this.showCheckInDialog = false;
    },
    
    // 删除草稿
    deleteDraftCheckIn() {
      this.draftCheckIn = '';
      this.tempCheckInContent = '';
    },
    
    // 直接打卡提交（原有功能保持不变）
    handleCheckInSubmit() {
      if (!this.checkInContent.trim()) {
        alert('请输入打卡内容');
        return;
      }

      const checkInPost = {
        id: Date.now(),
        username: '匿名用户',
        level: 'LV.1',
        time: this.getNowTime(),
        school: '未知学校',
        job: '打卡',
        title: '今日打卡',
        content: this.formatContent(this.checkInContent),
        fullContent: this.checkInContent
      };

      this.postList.unshift(checkInPost);
      this.$store.commit('addPost', checkInPost);
      this.showCheckInDialog = false;
      this.draftCheckIn = ''; // 清空草稿
      this.tempCheckInContent = '';
      alert('打卡成功！');
    },
      setPostType(type) {
        this.postType = type;
        // 如果是内推类型，清空内容并设置默认提示
        if (type === 'referral') {
          this.content = '';
          this.title = '';
        }
      },
    uploadImage() {
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = 'image/*';
      input.multiple = true;
      input.onchange = (e) => {
        const files = Array.from(e.target.files);
        this.selectedImages = [...this.selectedImages, ...files];
        files.forEach(file => {
          const reader = new FileReader();
          reader.onload = (event) => {
            this.content += `\n![图片](${event.target.result})`;
          };
          reader.readAsDataURL(file);
        });
      };
      input.click();
    },
    
    generateAIImage() {
      alert('AI配图功能即将上线，敬请期待！');
    },
    
    createPoll() {
      alert('投票功能即将上线，敬请期待！');
    },
    
    selectCircle() {
      alert('请选择要发布的圈子');
    },
    
    shareSalary() {
       this.showSalaryDialog = true
    },
    closeSalaryDialog() {
      this.showSalaryDialog = false
    },
    quickReferral() {
    this.setPostType('referral');
    this.content = ''; // 清空之前的内容
    this.title = '内推信息'; // 设置默认标题
  },
 // 修改 handlePublish 方法
  async handlePublish() {
      let publishContent = this.content;
      
      if (this.draftCheckIn) {
        publishContent += `\n\n[今日打卡]\n${this.draftCheckIn}`;
      }

      if (!publishContent.trim()) {
        alert('请输入要发布的内容');
        return;
      }

      if (this.postType === 'article' && !this.title.trim()) {
        alert('请输入文章标题');
        return;
      }


  const newPost = {
        id: Date.now(),
        username: store.state.user?.username || '匿名用户',
        level: 'LV.1',
        time: this.getNowTime(),
        school: '未知学校',
        contentType: this.postType === 'dynamic' ? '动态' : 
                    this.postType === 'article' ? '文章' : '内推',
        title: this.postType === 'article' ? this.title : 
               this.content.length > 20 ? this.content.slice(0, 20) + '...' : this.content,
        content: this.formatContent(this.content),
        fullContent: this.content
      };

  try {
    const res = await addExperience(newPost);
    if (res.status === 200) {
      // 更新本地数据
      this.postList.unshift({
        ...newPost,
        school: res.data.school || '未知学校'
      });
      
      // 重置分页到第一页
      this.currentPage = 1;
      
      // this.$message.success('发布成功！');
      alert('发布成功！');
      this.resetForm();
    }
  } catch (error) {
    console.error('发布失败:', error);
    this.$message.error('发布失败，请重试');
  }
},
  
 




    
    formatContent(content) {
      return content
        .replace(/\n/g, '<br>')
        .replace(/!\[图片\]\((.*?)\)/g, '<img src="$1" style="max-width:100%;"/>');
    },
    
    resetForm() {
      this.content = '';
      this.title = '';
      this.selectedImages = [];
      this.selectedCircle = null;
      setTimeout(() => {
        this.previewContent = '';
      }, 3000);
    },
    
    getNowTime() {
      const now = new Date();
      const MM = String(now.getMonth() + 1).padStart(2, '0');
      const dd = String(now.getDate()).padStart(2, '0');
      const hh = String(now.getHours()).padStart(2, '0');
      const mm = String(now.getMinutes()).padStart(2, '0');
      return `${MM} - ${dd} ${hh}:${mm}`;
    },
    
    toggleExpand(index) {
      this.$set(this.isExpanded, index, !this.isExpanded[index])
    },
    
   toggleEmojiPanel(event) {
    if (event) {
      event.stopPropagation();
    }
    
    // 切换面板显示状态
    this.showEmojiPanel = !this.showEmojiPanel;
    
    if (this.showEmojiPanel) {
      this.activeCategory = 'all';
      // 添加点击外部关闭的事件监听
      document.addEventListener('click', this.handleDocumentClick);
    } else {
      // 移除事件监听
      document.removeEventListener('click', this.handleDocumentClick);
    }
  },
    
  handleDocumentClick(event) {
    const emojiPanel = this.$el.querySelector('.emoji-panel');
    const emojiToggle = this.$el.querySelector('.icon-smile')?.parentNode;
    
    // 如果点击的是面板内部或触发按钮，不关闭
    if ((emojiPanel && emojiPanel.contains(event.target)) || 
        (emojiToggle && emojiToggle.contains(event.target))) {
      return;
    }
    
    // 点击外部，关闭面板
    this.showEmojiPanel = false;
    document.removeEventListener('click', this.handleDocumentClick);
  },
     switchEmojiCategory(categoryKey, event) {
    if (event) {
      event.stopPropagation();
    }
    this.activeCategory = categoryKey;
  },
    selectEmoji(emoji) {
      this.content += emoji;
    },
    
    getCategoryName(key) {
      const category = this.categories.find(c => c.key === key);
      return category ? category.name : '';
    }
  },
  
  async mounted() {
  // 初始时移除可能残留的事件监听
  document.removeEventListener('click', this.handleOutsideClick);
  
  try {
    const res = await listExperiences();
    if (res.status === 200) {
      // 获取数据后先排序
      this.postList = res.data.reverse();
    }
  } catch (error) {
    console.error('获取经验列表失败:', error);
  }
},
  beforeDestroy() {
    // 清理事件监听
    document.removeEventListener('click', this.handleOutsideClick);
  },
   created() {
    // 检查路由参数并设置帖子类型
    if (this.$route.query.postType) {
      this.setPostType(this.$route.query.postType);
      
      // 如果是从创作者中心跳转来的，可以显示提示或执行其他操作
      if (this.$route.query.from === 'creatorCenter') {
        console.log('从创作者中心跳转而来');
        // 可以在这里添加一些初始化逻辑
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.experience-container {
  width: 68%;
  max-width: 1200px;
  margin: 100 auto;
  padding: 0;
  transform: translateX(-45px);
}

.experience-sharing {
  width: 100%;
  margin: 10px 0 0 0;
  padding: 29px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  
  .post-type-buttons {
    display: flex;
    gap: 10px;
    margin-bottom: 15px;
    position: relative;

    .post-btn {
      flex: 0 0 auto;
      padding: 8px 16px;
      border: none;
      border-radius: 4px;
      font-size: 14px;
      font-weight: 500;
      cursor: pointer;
      
      &.dynamic-btn {
        background-color: #32ca99;
        color: white;
      }
      
      &.article-btn, &.referral-btn {
        background-color: #f0f0f0;
        color: #333;
      }

      &.active {
        box-shadow: 0 0 0 2px rgba(60, 179, 113, 0.3);
      }
    }

    .travel-link {
      position: absolute;
      right: 0;
      top: 50%;
      transform: translateY(-50%);
      color: #32ca99;
      font-size: 12px;
      text-decoration: none;
      white-space: nowrap;
    }
  }

  .content-input {
    margin-bottom: 15px;

    .title-input {
      width: 100%;
      padding: 12px;
      margin-bottom: 15px;
      border: 1px solid #e0e0e0;
      border-radius: 4px;
      font-size: 16px;
      font-weight: bold;
      
      &:focus {
        border-color: #32ca99;
        outline: none;
      }

      &::placeholder {
        color: #aaa;
        font-weight: normal;
      }
    }

    .post-textarea {
      width: 100%;
      min-height: 120px;
      padding: 12px;
      border: 1px solid #e0e0e0;
      border-radius: 4px;
      font-size: 14px;
      resize: none;
      transition: border-color 0.3s;

      &:focus {
        border-color: #32ca99;
        outline: none;
      }

      &::placeholder {
        color: #aaa;
      }
    }
  }

  .function-icons {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    margin-bottom: 20px;
    padding: 10px 0;
    border-bottom: 1px solid #eee;

    .icon-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      cursor: pointer;
      transition: transform 0.2s;

      &:hover {
        transform: translateY(-2px);
      }

      i {
        display: inline-block;
        width: 24px;
        height: 24px;
        margin-bottom: 4px;
        background-size: contain;
        background-repeat: no-repeat;
        
        &.icon-smile {
          background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23000000'%3E%3Cpath d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-5-9h2v2H7zm8 0h2v2h-2zm-4 4c1.66 0 3-1.34 3-3H9c0 1.66 1.34 3 3 3z'/%3E%3C/svg%3E");
        }
        
        &.icon-camera {
          background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23000000'%3E%3Cpath d='M9 2L7.17 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2h-3.17L15 2H9zm3 15c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z'/%3E%3Cpath d='M12 9c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z'/%3E%3C/svg%3E");
        }
        
        &.icon-ai {
          display: flex;
          span {
            font-size: 12px;
            font-weight: bold;
            &:first-child { color: #4285F4; }
            &:last-child { color: #EA4335; }
          }
        }
      }

      .icon-label {
        font-size: 12px;
        color: #666;
        transition: color 0.2s;
      }

      &:hover .icon-label {
        color: #3CB371;
      }
    }

    .publish-btn {
      padding: 6px 20px;
      background-color: #32ca99;
      color: white;
      border: none;
      border-radius: 4px;
      font-size: 14px;
      cursor: pointer;
      margin-left: auto;
      transition: all 0.2s;

      &:hover {
        background-color: #35a066;
        transform: translateY(-2px);
        box-shadow: 0 2px 8px rgba(60, 179, 113, 0.3);
      }
    }
  }
}

.experience-display {
  width: 100%;
  margin: 15px 0 0 0;
  padding: 29px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  
  .tab-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 1px solid #eee;

    .tab-item {
      padding: 4px 8px;
      font-size: 14px;
      color: #999;
      cursor: pointer;
      transition: all 0.2s;
      position: relative;

      &:after {
        content: '';
        position: absolute;
        bottom: -11px;
        left: 0;
        width: 100%;
        height: 2px;
        background: transparent;
        transition: all 0.2s;
      }

      &.active {
        color: #32ca99;
        font-weight: bold;

        &:after {
          background: #32ca99;
        }
      }

      &:hover:not(.active) {
        color: #777;
      }
    }

    .tab-actions {
      display: flex;
      gap: 12px;

      i {
        color: #32ca99;
        font-size: 16px;
        cursor: pointer;
        transition: transform 0.2s;

        &:hover {
          transform: scale(1.1);
        }
      }
    }
  }

  .content-display {
    .post-item {
      padding: 15px 0;
      border-bottom: 1px solid #eee;
      transition: background-color 0.2s;

      &:hover {
        background-color: #f9f9f9;
      }

      .user-info {
        display: flex;
        align-items: center;
        margin-bottom: 10px;

        .avatar {
           width: 40px;
           height: 40px;
           border-radius: 50%;
           background-color: #f0f0f0;
           margin-right: 10px;
           display: flex;
           align-items: center;
           justify-content: center;
  
           .icon-user-default {
             display: inline-block;
             width: 24px;
             height: 24px;
             background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23999'%3E%3Cpath d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z'/%3E%3C/svg%3E");
             background-size: contain;
             background-repeat: no-repeat;
             background-position: center;
           }
         }

        .user-details {
          flex:1;
          min-width: 0;
          .username {
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;

            .user-level {
              display: inline-block;
              padding: 0 4px;
              margin-left: 6px;
              background-color: #e8f5e9;
              border-radius: 2px;
              font-size: 10px;
              color: #2E8B57;
            }
          }

          .post-meta {
            font-size: 12px;
            color: #999;
            display: flex;
            gap: 12px;
            align-items: center;
            flex-wrap: wrap;

            span {
              margin-right: 12px;
              position: relative;

              &:not(:last-child):after {
                content: '•';
                position: absolute;
                right: -6px;
              }
            }
          }
        }
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

        .read-more {
          float: right;
          color: #3CB371;
          text-decoration: none;
          font-weight: 500;
          transition: color 0.2s;

          &:hover {
            color: #2E8B57;
            text-decoration: underline;
          }
        }
      }
    }
  }
}
.function-icons {
  position: relative;
  
  .icon-item {
    position: relative;
    
    &:hover {
      transform: translateY(-2px);
    }
  }
}

.inline-emoji-panel {
  position: absolute;
  top: 100%;
  left: 0;
  width: 320px;
  max-width: 100vw;
  margin-top: 10px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  z-index: 100;
  padding: 0;
  overflow: hidden;
}

.emoji-categories {
  display: flex;
  border-bottom: 1px solid #eee;
  padding: 8px 12px 0;
  flex-wrap: wrap;
  
  .category-item {
    padding: 6px 12px;
    margin-right: 8px;
    margin-bottom: 8px;
    font-size: 12px;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s;
    background-color: #f5f5f5;
    
    &:hover {
      background-color: #e0e0e0;
    }
    
    &.active {
      background-color: #32ca99;
      color: white;
    }
  }
}

.emoji-content {
  padding: 8px;
  max-height: 300px;
  overflow-y: auto;
}

.emoji-group {
  margin-bottom: 12px;
  
  .group-title {
    font-size: 12px;
    color: #999;
    margin-bottom: 8px;
    padding-left: 4px;
  }
}

.emoji-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  
  .emoji-item {
    font-size: 20px;
    cursor: pointer;
    text-align: center;
    padding: 6px;
    border-radius: 4px;
    transition: all 0.2s;
    width: calc(10% - 4px);
    box-sizing: border-box;
    
    &:hover {
      background-color: #f0f0f0;
      transform: scale(1.1);
    }
  }
}

@media (max-width: 768px) {
  .inline-emoji-panel {
    width: 280px;
  }
  
  .emoji-grid .emoji-item {
    width: calc(12.5% - 4px);
  }
}

@media (max-width: 480px) {
  .inline-emoji-panel {
    width: 240px;
  }
  
  .emoji-grid .emoji-item {
    width: calc(14.285% - 4px);
  }
}
.emoji-panel {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  padding: 0;
  z-index: 100;
  margin-bottom: 10px;
  width: 320px;
  max-height: 400px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
.emoji-categories {
  display: flex;
  border-bottom: 1px solid #eee;
  padding: 8px 12px 0;
  flex-wrap: wrap;
  
  .category-item {
    padding: 6px 12px;
    margin-right: 8px;
    margin-bottom: 8px;
    font-size: 12px;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s;
    background-color: #f5f5f5;
    
    &:hover {
      background-color: #e0e0e0;
    }
    
    &.active {
      background-color: #32ca99;
      color: white;
    }
  }
}

.emoji-content {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.emoji-group {
  margin-bottom: 12px;
  
  .group-title {
    font-size: 12px;
    color: #999;
    margin-bottom: 8px;
    padding-left: 4px;
  }
}

/* 在原有样式文件中添加 */
.salary-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.salary-dialog {
  z-index: 9999;
  background: white;
  border-radius: 12px;
  width: 700px;
  max-width: 90%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
/* 添加打卡对话框样式 */
.check-in-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.check-in-dialog {
  background: white;
  border-radius: 12px;
  width: 500px;
  max-width: 90%;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
   .dialog-actions {
    display: flex;
    gap: 8px;
    
    .confirm-btn {
      margin-left: auto;
    }
  }
  h3 {
    margin-top: 0;
    color: #333;
    font-size: 18px;
    text-align: center;
    margin-bottom: 15px;
  }
}

.check-in-textarea {
  width: 100%;
  min-height: 120px;
  padding: 12px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 14px;
  resize: none;
  margin-bottom: 15px;
  
  &:focus {
    border-color: #32ca99;
    outline: none;
  }
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  
  button {
    padding: 6px 16px;
    border-radius: 4px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s;
  }
  
  .cancel-btn {
    background-color: #f0f0f0;
    color: #333;
    border: none;
    
    &:hover {
      background-color: #e0e0e0;
    }
  }
  
  .confirm-btn {
    background-color: #32ca99;
    color: white;
    border: none;
    
    &:hover {
      background-color: #35a066;
    }
  }
}
/* 新增打卡草稿预览样式 */
.draft-checkin-preview {
  margin-top: 15px;
  border: 1px dashed #32ca99;
  border-radius: 4px;
  padding: 8px;
  background-color: #f9f9f9;
  width: 100%; /* 确保宽度填满父容器 */
  max-width: 100%; /* 防止溢出 */
  box-sizing: border-box; 
  .draft-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    font-size: 14px;
    color: #32ca99;
    font-weight: bold;
    
    .delete-draft-btn {
      background: none;
      border: none;
      color: #999;
      font-size: 16px;
      cursor: pointer;
      padding: 0 5px;
      
      &:hover {
        color: #ff4d4f;
      }
    }
  }
  
  .draft-content {
    white-space: pre-wrap;
    font-size: 14px;
    line-height: 1.5;
    color: #333;
    min-height: 30px;
    border-radius: 4px;
    padding: 12px;

    width: 100%; /* 内容区域宽度填满 */
    box-sizing: border-box; 
  }
}
/* 职位对话框样式 */
.job-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  background-color: rgba(0, 0, 0, 0.5);
}

.job-dialog {
  background: white;
  border-radius: 12px;
  width: 600px;
  max-width: 90%;
  padding: 35px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  max-height: 90vh;
  overflow-y: auto;
  
  h3 {
    margin-top: 0;
    color: #333;
    font-size: 18px;
    text-align: center;
    margin-bottom: 20px;
  }
  
  .form-group {
    margin-bottom: 16px;
    
    label {
      display: block;
      margin-bottom: 8px;
      font-size: 14px;
      color: #666;
    }
    
    .form-input {
      width: 100%;
      padding: 10px;
      border: 1px solid #e0e0e0;
      border-radius: 4px;
      font-size: 14px;
      
      &:focus {
        border-color: #32ca99;
        outline: none;
      }
    }
    
    .form-textarea {
      width: 100%;
      min-height: 100px;
      padding: 10px;
      border: 1px solid #e0e0e0;
      border-radius: 4px;
      font-size: 14px;
      resize: vertical;
      
      &:focus {
        border-color: #32ca99;
        outline: none;
      }
    }
  }
  
  .dialog-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 20px;
    
    button {
      padding: 8px 16px;
      border-radius: 4px;
      font-size: 14px;
      cursor: pointer;
      transition: all 0.2s;
    }
    
    .cancel-btn {
      background-color: #f5f5f5;
      color: #666;
      border: none;
      
      &:hover {
        background-color: #eee;
      }
    }
    
    .confirm-btn {
      background-color: #32ca99;
      color: white;
      border: none;
      
      &:hover {
        background-color: #2aa37d;
      }
    }
  }
}
@media (max-width: 992px) {
  .experience-container {
    width: 95%;
  }
}

@media (max-width: 768px) {
  .experience-container {
    width: calc(100% - 20px);
  }

  .experience-sharing {
    .post-type-buttons {
      flex-wrap: wrap;
      
      .travel-link {
        position: static;
        transform: none;
        width: 100%;
        margin-top: 8px;
        text-align: right;
      }
    }

    .function-icons {
        position: relative;
      .icon-item {
        flex: 0 0 calc(20% - 10px);
      }

      .publish-btn {
        margin-left: 0;
        width: 100%;
        margin-top: 10px;
      }
    }
  }
}

@media (max-width: 480px) {
  .experience-sharing,
  .experience-display {
    padding: 15px;
  }

  .experience-display {
    .tab-bar {
      flex-wrap: wrap;
      
      .tab-item {
        flex: 0 0 calc(33.333% - 10px);
        text-align: center;
        margin-bottom: 5px;
      }

      .tab-actions {
        width: 100%;
        justify-content: flex-end;
        margin-top: 5px;
      }
    }
  }
}
/* 在样式部分添加空状态样式 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  color: #999;
  
  .empty-icon {
    font-size: 48px;
    margin-bottom: 16px;
  }
  
  .empty-text {
    font-size: 16px;
    margin: 0;
  }
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
</style>