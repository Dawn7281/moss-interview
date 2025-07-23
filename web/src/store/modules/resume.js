// store/modules/resume.js
import { uploadResume } from '@/api/file'

export default {
  namespaced: true,
  state: {
    resumeUrl: null,
    resumeFileType: null,
    resumeFilename: null
  },
  mutations: {
   SET_RESUME(state, payload) {
    try {
      // 释放之前创建的URL
      if (state.resumeUrl && state.resumeUrl.startsWith('blob:')) {
        URL.revokeObjectURL(state.resumeUrl);
      }
      
      // 处理直接传入的file对象
      if (payload && payload.file instanceof Blob) {
        state.resumeUrl = URL.createObjectURL(payload.file);
        state.resumeFileType = payload.file.type.includes('pdf') ? 'pdf' : 'docx';
        state.resumeFilename = payload.file.name;
      }
      // 处理传入的url和其他参数
      else if (payload && payload.url) {
        state.resumeUrl = payload.url;
        state.resumeFileType = payload.fileType || 
          (payload.url.endsWith('.pdf') ? 'pdf' : 'docx');
        state.resumeFilename = payload.filename || payload.url.split('/').pop();
      }
    } catch (error) {
      console.error('设置简历状态失败:', error);
      state.resumeUrl = null;
      state.resumeFileType = null;
      state.resumeFilename = null;
    }
  }
  },
 actions: {
  async uploadResume({ commit }, { file, username }) {
    try {
      if (!file || !(file instanceof Blob)) {
        throw new Error('无效的文件对象');
      }

      const formData = new FormData();
      formData.append('file', file);
      
      const res = await uploadResume(formData, username);
      
      if (!res.data || !res.data.filename) {
        throw new Error('服务器返回无效响应');
      }

      // 修改这里：使用import.meta.env代替process.env
      const baseUrl = import.meta.env.VITE_API_BASE_URL || window.location.origin;
// 确保路径正确拼接
const serverUrl = `${baseUrl.replace(/\/$/, '')}/uploads/${res.data.filename}`;
      commit('SET_RESUME', {
  file: file,
  serverUrl: serverUrl + '?t=' + Date.now(), // 添加时间戳避免缓存
  filename: file.name,
  fileType: 'pdf' // 强制设置为pdf
});
      
      return res;
    } catch (error) {
      console.error('上传简历失败:', error);
      throw error;
    }
  }
}

}