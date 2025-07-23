import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'


import path from 'path'

export default defineConfig({
  plugins: [vue()],
  assetsInclude: ['**/*.docx'],
  // build: {
  //   assetsInlineLimit: 0 // 确保docx文件不会被内联
  // },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
       // '@': path.resolve(__dirname, './src')
    }
  },
  define: {
    'process.env': {},
    'import.meta.env': JSON.stringify(import.meta.env)
  },
  server: {
    port: 3000,
    open: true,
    host: true,
    browser: 'chrome',
    
    proxy: {
      '/api': {
        ws: true,
        target: 'http://127.0.0.1:5000',
        // target: 'https://www.moss-interviewer.website',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      },
      // 新增Google Fonts代理配置
      '/fonts': {
        target: 'http://fonts.googleapis.com',  // 使用HTTP协议
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/fonts/, '')
      }
    }
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@import "@/assets/styles/variables.scss";`
      }
    }
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    emptyOutDir: true,
    assetsInlineLimit: 0 // 确保docx文件不会被内联
  }
})