<template>
  <div class="login-container">
    <!-- 左侧登录功能区 -->
    <div class="login-form">
      <h1 class="logo">Moss</h1>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            id="username"
            v-model="username"
            type="text"
            placeholder="请输入你的姓名"
            required
          />
        </div>
        <div class="password-row">
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
          <button type="submit" class="login-btn">登录</button>
        </div>
      </form>
    </div>

    <!-- 右侧背景展示区 -->
    <div class="login-bg">
      <img src="@/assets/login-bg.jpg" alt="背景图片" class="bg-image" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    handleLogin() {
      this.$store.dispatch('login', {
        username: this.username,
        password: this.password
      }).then(() => {
        this.$router.push('/')
      }).catch(error => {
        alert(error.message)
      })
    }
  }
}
</script>

<style scoped>

/* 整体布局 */
.login-container {
  display: flex;
  height: 70h;
  width: 100%;
  border-radius: 6px;
}

/* 左侧登录表单区 */
.login-form {
  border-radius: 12px;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 3rem;
  background: white;
  max-width: 600px;
}

.logo {
  font-family: 'Potta One', cursive;
  font-size: 3rem;
  color: #00dcb6;
  margin-bottom: 3rem;
  text-align: center;
}


.form-group {
  width: 100%;
  max-width: 2000px;
  margin-bottom: 1.8rem;
}

label {
  display: block;
  font-size: 0.85rem;
  color: #00dcb6;
  margin-bottom: 0.5rem;
}

input {
  width: 100%;
  padding: 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  background-color: #f5f5f5;
  font-size: 0.9rem;
  transition: border-color 0.3s;
}

input:focus {
  border-color: #00dcb6;
  outline: none;
}

input::placeholder {
  color: #aaa;
  font-size: 0.85rem;
}

.login-btn {
  margin-left: auto;  /* 将按钮推到最右侧 */
  display: block;     /* 确保margin-left生效 */
  width: 90px;       /* 固定宽度 */
  /* 其他原有样式保持不变 */
  padding: 0.5rem;
  background-color: #3dcd9f;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-btn:hover {
  background-color: #3dcd9f;
}

/* 右侧背景区 - 优化图片显示 */
.login-bg {
  flex: 1;
  position: relative;
  display: none;
  overflow: hidden;
}

.bg-image {
  border-radius: 12px;
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: right;
}

/* 响应式设计 */
@media (min-width: 768px) {
  .login-bg {
    display: block;
  }
  
  .login-form {
    flex: 0 0 45%;
  }
}

@media (min-width: 1024px) {
  .login-form {
    flex: 0 0 40%;
  }
  
  .bg-image {
    object-fit: cover;
  }
}
</style>