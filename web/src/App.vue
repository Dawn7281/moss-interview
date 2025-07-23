<template>   <div id="app">
    <header class="header">
      <div class="header-content">
        <div class="title-nav-container">
          <h1 class="moss-logo">Moss</h1>
                  <nav class="main-nav">
                    
          <a
          
            href="#"
            class="nav-link"
            :class="{ active: currentSection === 'home' }"
            @click.prevent="goSection('home')"
          >首页</a>
           <!-- 新增下拉菜单 -->

            <div class="dropdown">
              <button class="dropbtn nav-link" :class="{ active: ['mock', 'history'].includes(currentSection) }">
                面试功能 
              </button>
              
              <div class="dropdown-content">
                 
                <a
                  href="#"
                  class="nav-link"
                  :class="{ active: currentSection === 'mock' }"
                  @click.prevent="goSection('mock')"
                >智能面试</a>
                <a
                  href="#"
                  class="nav-link"
                  :class="{ active: currentSection === 'history' }"
                  @click.prevent="goSection('history')"
                >面试历史</a>
              </div>
            </div>

            <a
              href="#"
              class="nav-link"
              :class="{ active: currentSection === 'position' }"
              @click.prevent="goSection('position')"
            >岗位详情</a>
          <a
            href="#"
            class="nav-link"
            :class="{ active: currentSection === 'qa' }"
            @click.prevent="goSection('qa')"
          >面试试题</a>
                    <a
                        href="#"
                        class="nav-link"
                        :class="{ active: currentSection === 'resume' }"
                        @click.prevent="goSection('resume')"
                    >简历优化</a>
          <!-- 新增知识图谱 -->
            <a
              href="#"
              class="nav-link"
              :class="{ active: currentSection === 'knowledge' }"
              @click.prevent="goSection('knowledge')"
            >学习资源</a>
            
        
           
        </nav>
        </div>
        <div class="auth-buttons">
          <div v-if="!$store.state.isAuthenticated">
            <router-link to="/login" class="auth-button">登录</router-link>
            <router-link to="/register" class="auth-button">注册</router-link>
          </div>
          <div v-else>
            <span class="welcome-message">欢迎，{{ $store.state.user?.username }}</span>
            <button class="auth-button logout-button" @click="handleLogout">退出登录</button>
            <router-link to="/user-center" class="auth-button user-center-btn">个人中心</router-link>
          </div>
        </div>
      </div>
    </header>

    <main class="container">
      <router-view />
    </main>

    <footer class="footer">
      <p>© 2025 智能面试评测系统 | 助力职场成功</p>
    </footer>
  </div>
</template>

<script>
import UserCenter from './views/UserCenter.vue'

export default {
  name: 'App',
  components: {
    UserCenter
  },
  data() {
    return {
      currentSection: 'home',
      showUserCenter: false
    }
  },
  watch: {
    // 监听路由变化，自动设置 currentSection
    '$route.path': {
      immediate: true,
      handler(newPath) {
        if (newPath === '/' || newPath.startsWith('/home')) this.currentSection = 'home'
        else if (newPath.startsWith('/mock-interview')) this.currentSection = 'mock'
        else if (newPath.startsWith('/resume')) this.currentSection = 'resume'
        else if (newPath.startsWith('/qa')) this.currentSection = 'qa'
        else if (newPath.startsWith('/interview-history')) this.currentSection = 'history'
        else if (newPath.startsWith('/jobs')) this.currentSection = 'position'
        else if (newPath.startsWith('/graph')) this.currentSection = 'knowledge'

        else this.currentSection = ''
      }
    }
  },
  methods: {
    handleLogout() {
      this.$store.dispatch('logout')
      this.currentSection = 'home'
      this.$router.push('/')
    },
   goSection(section) {
  this.currentSection = section
      if (section === 'home') this.$router.push('/')
      if (section === 'mock') this.$router.push('/mock-interview')
      if (section === 'resume') this.$router.push('/resume')
      if (section === 'qa') this.$router.push('/qa')
      if (section === 'history') this.$router.push('/interview-history')
      if (section === 'position') this.$router.push('/jobs')
     if (section === 'knowledge') this.$router.push('/graph')
}
  }
  
}
</script>

<style>
/* 基础布局样式 */
/* 在App.vue的全局样式中添加 */
body {
  &.dialog-open {
    overflow: visible !important;
    position: relative !important;
    
    * {
      &:not(.salary-dialog-overlay):not(.salary-dialog) {
        z-index: auto !important;
      }
    }
  }
}
:root {
  --header-height: 64px; /* 推荐使用这个更合理的高度 */
   --footer-height: 56px; /* 16px(padding-top) + 16px(padding-bottom) + 24px(行高) */
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  transform: none; 
  perspective: none; 
}

.header {
  background: #42b983;
  color: white;
  padding: 0.2rem;
  height: 60px; /* 你可以调整 */
 /* 添加以下两行 */
  border-bottom: 1px solid #89cfb9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 1000;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
}

.title-nav-container {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-left: -40px;
}

.moss-logo {
  font-size: 23rem;
  font-weight: 1800;
  font-family: 'Potta One', sans-serif;
  letter-spacing: 4px;
  text-shadow: 1px 2px 4px rgba(0, 0, 0, 0.3);
  transform: skew(-10deg);
  display: inline-block;
  margin: 0;
  padding-left: -20px;
}

.main-nav {
  display: flex;
  gap: 2rem;
  align-items: center; /* 确保所有子项垂直居中 */
  margin-left: var(--sidebar-width);

}

.nav-link {
  color: white;
  font-size: 1.2rem;
  text-decoration: none;
  padding: 0.1rem 1rem;
  border-radius: 10px;
  transition: background 0.2s;
}

.nav-link:hover {
  background: rgba(255,255,255,0.2);
}

.nav-link.active {
  background: transparent;
  color: white;
  position: relative;
}

.nav-link.active::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 50%;
  transform: translateX(-50%);
  width: 60%;
  height: 2px;
  background: white;
  border-radius: 10px;
}

.auth-buttons {
  display: flex;
  gap: 1rem;
  margin-left: auto; /* 新增：使右侧区域自动靠右 */
  padding-right: -70px; /* 可选：增加右内边距 */
}

.auth-buttons > div {
  margin-top: 15px;
}

.auth-button {
  padding: 0.5rem 1.5rem;
  background-color: rgba(255,255,255,0.2);
  color: white;
  border: none;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.3s ease;
   margin-left: 8px;
}

.auth-button:hover {
  background-color: rgba(255,255,255,0.3);
}

.auth-button:last-child {
  background-color: rgba(255,255,255,0.4);
}

.auth-button:last-child:hover {
  background-color: rgba(255,255,255,0.5);
}

.container {
  flex: 1;
  padding: 0 2rem;
  max-width: 1200px;
  margin: -28rem auto 0 auto; /* 负值等于 .moss-logo 的 font-size，内容整体向上 */
  width: 100%;
   margin-left: var(--sidebar-width) ; /* 确保主内容避开侧边栏 */
}

.footer {
  background: #333;
  color: white;
  text-align: center;
  padding: 1rem;
   height: 46px;
}

.auth-buttons .welcome-message {
  margin-right: 1.2rem;
}

.auth-button.user-center-btn {
  margin-left: 0;
}

.auth-buttons > div:first-child > .auth-button:not(:last-child) {
  margin-right: 2rem;
}

/* 以下是原有所有不变的样式 */
.header-content {
  position: relative;
}

.title {
  position: relative;
  margin-bottom: 1.5rem;
}

.main-nav {
  z-index: 2;
}

.nav-link {
  transition: background 0.2s;
}

.nav-link.active {
  position: relative;
}

.auth-button {
  transition: all 0.3s ease;
}

.auth-button:hover {
  transition: all 0.3s ease;
}

.auth-button:last-child:hover {
  transition: all 0.3s ease;
}

.container {
  width: 100%;
}

.auth-button.user-center-btn {
  margin-left: 0;
}

.auth-buttons > div:first-child > .auth-button:not(:last-child) {
  margin-right: 2rem;
}

.auth-button:last-child:hover {
  transition: all 0.3s ease;
}

.container {
  width: 100%;
}

.auth-button.user-center-btn {
  margin-left: 0;
}

.auth-buttons > div:first-child > .auth-button:not(:last-child) {
  margin-right: 2rem;
}

/* 更新下拉菜单样式 */
.dropdown {
  position: relative;
  display: inline-flex; /* 改为inline-flex确保与其他导航项对齐 */
  align-items: center;
  height: auto; /* 改为auto避免高度问题 */
}


.dropbtn {
  background-color: transparent;
  border: none;
  cursor: pointer;
  padding: 0.5rem 1rem; /* 调整padding与其他导航项一致 */
  color: white;
  font-size: 1.2rem;
  text-decoration: none;
  border-radius: 10px;
  transition: background 0.2s;
  display: inline-flex;
  align-items: center;
  margin: 0;
  line-height: 1.5; /* 确保行高一致 */
  
}

.dropbtn:hover {
  background: rgba(255,255,255,0.2);
}

.dropdown-content {
   display: none;
  position: absolute;
  background-color: white;
  min-width: 140px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
  border-radius: 8px;
  padding: 0.5rem 0;
  top: 100%; /* 从按钮底部开始显示 */
  left: 0;
}

.dropdown-content a {
  color: #42b983;
  padding: 0.5rem 1rem;
  text-decoration: none;
  display: block;
  text-align: left;
  font-size: 1.1rem;
}

.dropdown-content a:hover {
  background-color: #f5f5f5;
}

.dropdown:hover .dropdown-content {
  display: block;
}

/* 激活状态样式 */
.dropbtn.active {
  position: relative;
}

/* 或者更精确的写法 */
.dropdown-content a.nav-link.active::after {
  content: none;
}

.dropbtn.active::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 50%;
  transform: translateX(-50%);
  width: 60%;
  height: 2px;
  background: white;
  border-radius: 10px;
}

.dropdown-content a.active {
  color: #2b7a78;
  font-weight: bold;
}
</style>