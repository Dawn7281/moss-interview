import { createApp } from 'vue'
import { createPinia } from 'pinia' // 导入 Pinia
import App from './App.vue'
import store from './store' // 引入 Vuex Store
import router from './router' // 引入路由配置
           

// 创建并挂载应用
const pinia = createPinia()
const app = createApp(App)
app.use(store) // 使用 Vuex Store
app.use(router) // 使用路由
app.mount('#app')
// 使用 Pinia
app.use(pinia)
