<template>
  <div class="register-container">
    <!-- 左侧背景展示区 -->
    <div class="register-bg">
      <img src="@/assets/login-bg.jpg" alt="背景图片" class="bg-image" />
    </div>

    <!-- 右侧注册功能区 -->
    <div class="register-form">
      <h1 class="logo">Moss</h1>
      <div class="form-content">
        <form @submit.prevent="handleRegister">
          <div class="form-group">
            <label for="username">用户</label>
            <input
              id="username"
              v-model="username"
              type="text"
              placeholder="请输入姓名"
              required
            />
          </div>
          <div class="form-group">
            <label for="email">邮箱</label>
            <input
              id="email"
              v-model="email"
              type="email"
              placeholder="请输入邮箱"
              required
            />
          </div>
          <div class="form-group">
            <label for="password">密码</label>
            <input
              id="password"
              v-model="password"
              type="password"
              placeholder="请输入密码"
              required
            />
          </div>
          <div class="form-group">
            <label for="confirmPassword">确认密码</label>
            <input
              id="confirmPassword"
              v-model="confirmPassword"
              type="password"
              placeholder="请确认密码"
              required
            />
          </div>
          <button type="submit" class="register-btn">注册</button>
        </form>
        <p class="switch-auth">
          已有账号？<router-link to="/login">立即登录</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Register',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    }
  },
  methods: {
    async handleRegister() {
      if (this.password !== this.confirmPassword) {
        alert('两次输入的密码不一致');
        return;
      }
      try {
        await this.$store.dispatch('register', {
          username: this.username,
          email: this.email,
          password: this.password
        });
        // 修改这里，确保传递布尔值true而不是字符串'true'
        this.$router.push({
          path: '/user-center',
          query: { firstRegister: true }
        });
      } catch (error) {
        alert(error.message);
      }
    }
  }
}
</script>

<style scoped>
/* 整体布局 */
.register-container {
  display: flex;
  height: 70vh;
  width: 100%;
}

/* 左侧背景区 */
.register-bg {
  border-radius: 12px;
  flex: 1;
  background: #2E375D;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.bg-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 右侧注册表单区 */
.register-form {
  border-radius: 12px;
  flex: 1;
  max-width: 520px;
  padding: 3rem;
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

/* 新增表单内容容器 */
.form-content {
  width: 70%;
  margin-left: 15%;
}

.logo {
  font-family: 'Potta One', cursive;
  font-size: 3rem;
  color: #00dcb6;
  margin-bottom: 2rem;
  text-align: center;
}

/* 表单组样式 */
.form-group {
  width: 100%;
  margin-bottom: 1.2rem;
}

label {
  display: block;
  font-size: 0.9rem;
  color: #00dcb6;
  margin-bottom: 0.5rem;
  font-family: 'Poppins', sans-serif;
}

input {
  width: 90%; /* 缩小输入框宽度 */
  padding: 0.8rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #F5F5F5;
  font-size: 0.85rem;
  color: #00dcb6;
  margin: 0 auto; /* 水平居中 */
  display: block; /* 使margin auto生效 */
}

input::placeholder {
  color: #aaaaaa;
  opacity: 0.6;
}

/* 注册按钮 */
.register-btn {
  display: block; /* 改为块级元素 */
  width: 28%;
  padding: 0.8rem;
  background-color: #3dcd9f;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 0.9rem;
  font-family: 'Poppins', sans-serif;
  cursor: pointer;
  transition: background-color 0.3s;
  margin: 1rem auto 0; /* 修改为自动外边距实现居中 */
}

.register-btn:hover {
  background-color: #29dcb6;
}

/* 切换登录链接 */
.switch-auth {
  margin-top: 1.5rem;
  color: #29dcb6;
  text-align: center; /* 从left改为center */
  font-family: 'Poppins', sans-serif;
  width: 100%; /* 确保容器宽度足够 */
}

.switch-auth a {
  color: #2E375D;
  text-decoration: none;
  font-weight: bold;
}

.switch-auth a:hover {
  text-decoration: underline;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .register-container {
    flex-direction: column;
  }
  
  .register-bg {
    display: none;
  }
  
  .register-form {
    max-width: 100%;
    padding: 2rem;
  }
  
  .form-content {
    width: 90%;
    margin-left: 5%;
  }
  .register-btn {
    width: 50%; /* 在小屏幕上适当加宽 */
  }
}
</style>