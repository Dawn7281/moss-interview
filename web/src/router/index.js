import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import MockInterview from '../views/MockInterview.vue'
import InterviewReportView from '@/views/InterviewReportView.vue'


const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue')
  },
  {
    path: '/qa',
    name: 'InterviewQA',
    component: () => import('../components/InterviewQA.vue')
  },
  {
    path: '/resume',
    name: 'ResumeDesign',
    component: () => import('../components/ResumeDesign.vue')
  },
  {
    path: '/learning-path/:id',
    name: 'LearningPath',
    component: () => import('../views/LearningPathDetail.vue'),
    props: true
  },
  {
    path: '/ai-careers',
    name: 'AICareers',
    component: () => import('../views/AICareers.vue')
  },
   {
    path: '/user-center',
    name: 'UserCenter',
    component: () => import('../views/UserCenter.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ firstRegister: route.query.firstRegister === 'true' }),
    meta: { requiresAuth: true }
  },
  {
    path: '/mock-interview',
    name: 'MockInterview',
    component: MockInterview
  },
  // 在router/index.js中添加
  {
    path: '/resume-setting',
    name: 'ResumeSetting',
    component: () => import('../components/ResumeSetting.vue')
  },
{
    path: '/interview-history',
    name: 'InterviewHistory',
    component: () => import('../components/InterviewHistory.vue')
  },
{
  path: '/interview-report',  // 报告详情页
  name: 'InterviewReport',
  component: () => import('../views/InterviewReportView.vue'),
  props: (route) => ({ firstRegister: route.query.firstRegister === true }) 
},
 {
  path: '/jobs',
  name: 'JobList',
  component: () => import('../views/JobsPage.vue')
},
{
  path: '/jobs/:id',
  name: 'JobDetail',
  component: () => import('../views/JobDetail.vue'),
  props: true
},
  {
    path: '/graph',
    name: 'Graph',
    component: () => import('../views/GraphView.vue'),
  },
{
    path: '/mock-interview',
    name: 'MockInterview',
    component: () => import('../views/MockInterview.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
// 修改后的路由守卫
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('isAuthenticated')
  
  // 需要登录的路由集合
  const authRequiredRoutes = [
    '/mock-interview',       // 智能面试
    '/interview-history',    // 面试历史
    '/resume',              // 简历优化
    '/qa',                  // 面试试题
    '/graph',               // 学习资源
    '/jobs',                // 岗位详情（包括列表和详情页）
    '/jobs/:id',
    '/user-center',         // 个人中心
    '/interview-report',    // 面试报告
    '/resume-setting'       // 简历设置
  ]
  
  // 检查目标路由是否需要认证
  const requiresAuth = authRequiredRoutes.some(route => {
    // 处理动态路由
    if (route.includes(':')) {
      const baseRoute = route.split('/:')[0]
      return to.path.startsWith(baseRoute)
    }
    return to.path === route
  })
  
  // 如果路由需要认证且用户未登录，则重定向到登录页
  if (requiresAuth && !isAuthenticated) {
    next({
      path: '/login',
      query: { redirect: to.fullPath } // 登录后可以重定向回原页面
    })
  } else {
    next()
  }
})
export default router
