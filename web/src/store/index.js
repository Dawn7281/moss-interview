import { createStore } from 'vuex'
import {addUser, checkUser} from "@/api/user";
import resume from './modules/resume' // 导入简历模块
export default createStore({
  state: {
    user: {
      username: '',
      hasResume: false // 添加默认值
    },
    isAuthenticated: localStorage.getItem('isAuthenticated') === 'true',
    user: localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null,
    currentModule: 'ai',
     resume: {
      url: null,
      filename: null,
      blob: null
    },
    learningPaths: [
      {
        id: 1,
        title: '行业面试题库',
        description: '精选200+技术岗位面试真题',
        selected: false
      },
      {
        id: 2,
        title: '表达训练视频',
        description: '提升沟通与表达能力的专业课程',
        selected: false
      },
      {
        id: 3,
        title: '岗位技能课程',
        description: '针对目标岗位的技术提升路径',
        selected: false
      }
    ],
    evaluationData: {
      indicators: [
        { name: '专业知识', score: 85 },
        { name: '技能匹配', score: 78 },
        { name: '表达能力', score: 90 },
        { name: '逻辑思维', score: 82 },
        { name: '创新能力', score: 75 }
      ],
      suggestions: [
        '建议使用STAR结构回答问题',
        '注意保持适当的眼神交流',
        '技术细节描述可以更具体'
      ]
    }
  },
    modules: {
    resume // 注册简历模块
  },

  mutations: {
     setHasResume(state, value) {
      state.user.hasResume = value
    },
    SET_AUTH(state, payload) {
      state.isAuthenticated = payload.isAuthenticated;
      state.user = payload.user || null;

      // 同步到 localStorage
      if (payload.isAuthenticated) {
        localStorage.setItem('isAuthenticated', 'true');
        localStorage.setItem('user', JSON.stringify(payload.user));
      } else {
        localStorage.removeItem('isAuthenticated');
        localStorage.removeItem('user');
      }
    },
    setCurrentModule(state, moduleId) {
      state.currentModule = moduleId;
    },
    selectLearningPath(state, pathId) {
      state.learningPaths.forEach((path) => {
        path.selected = path.id === pathId;
      });
    }
  },
  actions: {
    async login({ commit }, credentials) {
      return  await new Promise(async (resolve, reject) => {
        const res = await checkUser({
          username: credentials.username,
          password: credentials.password,
        });
        if (res.status === 200) {
          commit('SET_AUTH', {
            isAuthenticated: true,
            user: { username: credentials.username }
          });
          resolve();
        }
        else if (res.status === 400) {
          reject(new Error(res.data.error));
        }
      });
    },
    logout({ commit }) {
      commit('SET_AUTH', {
        isAuthenticated: false,
        user: null
      });
      localStorage.removeItem('isAuthenticated');
      localStorage.removeItem('user');
    },
    async register({ commit }, userData) {
      return await new Promise(async (resolve, reject) => {
        const res = await addUser({
          username: userData.username,
          password: userData.password,
          email: userData.email
        });
        if (res.status === 200) {
          commit('SET_AUTH', {
            isAuthenticated: true,
            user: { username: userData.username, email: userData.email }
          });
          resolve();
        }
        else if (res.status === 400) {
          reject(new Error(res.data.error));
        }
      });
    }
  },
  getters: {
    getCurrentEvaluation: (state) => state.evaluationData,
    getSelectedPaths: (state) => state.learningPaths.filter((path) => path.selected)
  }
});
