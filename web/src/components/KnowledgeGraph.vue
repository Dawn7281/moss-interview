<template>
  <div class="knowledge-graph-container">
    <!-- 历史记录侧边栏（覆盖式） -->
     <transition name="slide">
    <div class="history-sidebar-overlay" v-if="showHistory && hasHistoryItems" @click.self="toggleHistorySidebar">
      <div class="history-sidebar" :class="{ visible: showHistory }">
        <div class="sidebar-header">
          <h3 class="sidebar-title">
            <span>搜索历史</span>
            <button class="sidebar-close" @click="toggleHistorySidebar">×</button>
          </h3>
        </div>
        
        <div class="sidebar-search">
          <input type="text" placeholder="搜索历史记录..." v-model="searchQuery">
        </div>
        
        <div class="history-list-container">
          <ul class="history-list" v-if="history.length > 0">
            <li 
              v-for="(item, index) in history"
              :key="index"
              @click="loadHistoryItem(item.keyword, index)"
              :class="{ active: index === historyIndex }"
            >
              <span>{{ item.keyword }}</span>
              <span class="history-item-time">{{ formatDate(item.time) }}</span>
            </li>
          </ul>
          <div class="history-empty" v-else>
            <div class="history-empty-icon">🕒</div>
            <p>暂无搜索历史</p>
          </div>
        </div>
      </div>
    </div>
  </transition>

    <!-- 顶部固定按钮 -->
    <button class="history-toggle-btn" @click="toggleHistorySidebar">
      <i class="icon-history"></i>
      {{ '查看搜索历史' }}
    </button>

    <!-- 主内容区域 -->
    <div class="main-content">
      <!-- 左侧图谱区域 -->
      <div class="graph-section">
        <div class="graph-header">
          <h2 class="graph-title">知识图谱</h2>
          <div class="graph-controls">
            <button @click="getURL" class="btn btn-primary" :disabled="!clickedNode.name">
              <i class="icon-search"></i>
              搜索资源
            </button>
            <button id="export" @click="exportNetwork" class="btn btn-secondary">
              <i class="icon-download"></i>
              导出PNG
            </button>
          </div>
        </div>
        <div id="network"></div>
        <div class="graph-status" v-if="clickedNode.name">
          <span class="status-text">已选择节点：<strong>{{ clickedNode.name }}</strong></span>
        </div>
      </div>

      <!-- 右侧资源区域 -->
      <div class="resources-section">
        <div class="resources-header">
          <h2 class="resources-title">学习资源</h2>
          <div class="resources-subtitle" v-if="clickedNode.name">
            关于 "{{ clickedNode.name }}" 的推荐资源
          </div>
        </div>

        <div class="resources-content">
          <!-- 视频课程 -->
          <div class="resource-category" v-if="learnURL.video_courses && learnURL.video_courses.length > 0">
            <h3 class="category-title">
              <i class="icon-video"></i>
              视频课程
            </h3>
            <div class="cards-grid">
              <LinkPreview
                  v-for="doc in learnURL.video_courses"
                  :key="doc.url"
                  :url="doc.url"
                  :fallback-title="doc.name"
                  :fallback-description="doc.desc"
                  type="视频课程"
                  :enable-preview="false"
              />
            </div>
          </div>

          <!-- 学习文档 -->
          <div class="resource-category" v-if="learnURL.learning_docs && learnURL.learning_docs.length > 0">
            <h3 class="category-title">
              <i class="icon-book"></i>
              学习文档
            </h3>
            <div class="cards-grid">
              <LinkPreview
                  v-for="doc in learnURL.learning_docs"
                  :key="doc.url"
                  :url="doc.url"
                  :fallback-title="doc.name"
                  :fallback-description="doc.desc"
                  type="文档"
                  :enable-preview="false"
              />
            </div>
          </div>

          <!-- 项目实战 -->
          <div class="resource-category" v-if="learnURL.projects && learnURL.projects.length > 0">
            <h3 class="category-title">
              <i class="icon-code"></i>
              项目实战
            </h3>
            <div class="cards-grid">
              <LinkPreview
                  v-for="doc in learnURL.projects"
                  :key="doc.url"
                  :url="doc.url"
                  :fallback-title="doc.name"
                  :fallback-description="doc.desc"
                  type="项目"
                  :enable-preview="false"
              />
            </div>
          </div>

          <!-- 其他平台 -->
          <div class="resource-category" v-if="learnURL.other_platforms && learnURL.other_platforms.length > 0">
            <h3 class="category-title">
              <i class="icon-globe"></i>
              其他平台
            </h3>
            <div class="cards-grid">
              <LinkPreview
                  v-for="doc in learnURL.other_platforms"
                  :key="doc.url"
                  :url="doc.url"
                  :fallback-title="doc.name"
                  :fallback-description="doc.desc"
                  type="平台"
                  :enable-preview="false"
              />
            </div>
          </div>

          <!-- 空状态提示 -->
          <div class="empty-state" v-if="!hasAnyResources">
            <div class="empty-icon">🔍</div>
            <h3>暂无资源</h3>
            <p>请先点击左侧图谱中的节点，然后点击"搜索资源"按钮来获取相关学习资源。</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Network } from 'vis-network';
import { getSearch } from "@/api/search";
import LinkPreview from "./LinkPreview.vue";
import {List} from "echarts";

export default {
  name: 'KnowledgeGraph',
  components: {
    LinkPreview,
  },
  props: {
    graphData: {
      type: Object,
      required: true,
      validator: (value) => {
        return value.nodes && Array.isArray(value.nodes) && value.edges && Array.isArray(value.edges);
      }
    },
    history: {
      type: List,
      required: true,
    },
    historyIndex: {
      type: Number,
    }
  },
  data() {
    return {
      network: null,
      clickedNode: { name: "" },
      learnURL: {},
      showHistory: false,
      searchHistory: [],
      devHistory: ["人工智能", "机器学习", "深度学习", "神经网络"],
      maxHistoryItems: 10,
      searchQuery: '',
    };
  },
  computed: {
    hasHistoryItems() {
      return (this.searchHistory && this.searchHistory.length > 0) || 
             (process.env.NODE_ENV === 'development' && this.devHistory && this.devHistory.length > 0);
    },
    displayHistory() {
      if (process.env.NODE_ENV === 'development' && (!this.searchHistory || this.searchHistory.length === 0)) {
        return this.devHistory;
      }
      return this.searchHistory || [];
    },
    filteredHistory() {
      const history = this.displayHistory;
      if (!history) return [];
      
      if (!this.searchQuery) {
        return history;
      }
      
      const query = this.searchQuery.toLowerCase();
      return history.filter(item => 
        item.toLowerCase().includes(query)
      );
    },
    hasAnyResources() {
      return (this.learnURL.video_courses && this.learnURL.video_courses.length > 0) ||
          (this.learnURL.learning_docs && this.learnURL.learning_docs.length > 0) ||
          (this.learnURL.projects && this.learnURL.projects.length > 0) ||
          (this.learnURL.other_platforms && this.learnURL.other_platforms.length > 0);
    }
  },
  mounted() {
    this.renderGraph();
  },
  watch: {
    graphData: {
      handler() {
        this.renderGraph();
      },
      deep: true,
    },
    'clickedNode.name': {
      handler(newVal) {
        if (newVal) {
          this.addToHistory(newVal);
        }
      },
      immediate: true
    }
  },
  methods: {
    formatDate(dateString) {
      const date = new Date(dateString)
      date.setHours(date.getHours() - 8);
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        timeZone: 'Asia/Shanghai'
      });
    },
    toggleHistorySidebar() {
      this.showHistory = !this.showHistory;
    },
    addToHistory(keyword) {
      if (!keyword) return;
      
      if (!this.searchHistory) {
        this.searchHistory = [];
      }
      
      const index = this.searchHistory.indexOf(keyword);
      if (index !== -1) {
        this.searchHistory.splice(index, 1);
      }
      
      this.searchHistory.unshift(keyword);
      
      if (this.searchHistory.length > this.maxHistoryItems) {
        this.searchHistory.pop();
      }
      
      localStorage.setItem('searchHistory', JSON.stringify(this.searchHistory));
    },
    loadHistoryItem(keyword, index) {
      // this.historyIndex = index;
      this.$emit('keyword-selected', keyword, index);
      this.showHistory = false;
    },
    exportNetwork() {
      if (this.network) {
        const canvas = this.network.canvas.frame.canvas;
        const dataURL = canvas.toDataURL('image/png');
        const link = document.createElement('a');
        link.href = dataURL;
        link.download = 'knowledge-graph.png';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } else {
        console.error("Network is not initialized.");
      }
    },
    renderGraph() {
      if (!this.graphData || !this.graphData.nodes || !this.graphData.edges) {
        console.warn("Invalid graphData prop provided.");
        return;
      }

      const container = document.getElementById('network');
      if (!container) {
        console.error("Network container element not found.");
        return;
      }

      // 颜色逻辑保持不变
      const colorPalette = [
        '#E6E6FA', '#FFF0F5', '#F0FFF0', '#F5FFFA', '#F0F8FF',
        '#FAEBD7', '#FFEFD5', '#FFE4E1', '#D2B48C', '#ADD8E6',
        '#E0FFFF', '#FAFAD2', '#D3D3D3', '#FFDAB9', '#FFEBCD',
      ];
      const nodeColors = {};
      let colorIndex = 0;
      const getNextColor = () => {
        const color = colorPalette[colorIndex % colorPalette.length];
        colorIndex++;
        return color;
      };

      const adjacencyList = {};
      this.graphData.nodes.forEach(node => {
        adjacencyList[node.id] = [];
      });
      this.graphData.edges.forEach(edge => {
        adjacencyList[edge.source].push(edge.target);
        adjacencyList[edge.target].push(edge.source);
      });

      const sortedNodes = [...this.graphData.nodes].sort((a, b) => {
        return adjacencyList[b.id].length - adjacencyList[a.id].length;
      });

      sortedNodes.forEach(centerNode => {
        if (nodeColors[centerNode.id]) {
          return;
        }

        const neighborColor = getNextColor();
        const neighbors = adjacencyList[centerNode.id];

        neighbors.forEach(neighborId => {
          if (!nodeColors[neighborId]) {
            nodeColors[neighborId] = neighborColor;
          }
        });

        let centerColor = getNextColor();
        if (neighbors.length > 0 && centerColor === neighborColor) {
          centerColor = getNextColor();
        }
        nodeColors[centerNode.id] = centerColor;
      });

      this.graphData.nodes.forEach(node => {
        if (!nodeColors[node.id]) {
          nodeColors[node.id] = getNextColor();
        }
      });

      const finalNodes = this.graphData.nodes.map(node => ({
        id: node.id,
        label: node.name,
        color: {
          background: nodeColors[node.id] || '#FFFFFF',
          border: '#4a4a4a',
          highlight: {
            background: '#d1e3f8',
            border: '#2B7CE9'
          },
          hover: {
            background: '#eef4fc',
            border: '#2B7CE9'
          }
        },
      }));

      const edges = this.graphData.edges.map(edge => ({
        from: edge.source,
        to: edge.target,
        label: edge.relation,
        arrows: 'to',
        color: {
          color: '#848484',
          highlight: '#2B7CE9',
          hover: '#848484',
        }
      }));

      const data = {
        nodes: finalNodes,
        edges: edges,
      };

      const options = {
        nodes: {
          font: {
            size: 14,
            color: '#333333'
          },
          borderWidth: 1.5,
          shape: 'box',
          margin: 10,
        },
        edges: {
          font: {
            size: 14,
            align: 'middle'
          },
          width: 1
        },
        physics: {
          solver: 'forceAtlas2Based',
          forceAtlas2Based: {
            gravitationalConstant: -50,
            centralGravity: 0.01,
            springLength: 200,
            springConstant: 0.08,
            avoidOverlap: 0.5
          }
        },
        interaction: {
          hover: true,
          tooltipDelay: 200,
        },
      };

      if (this.network) {
        this.network.destroy();
      }
      this.network = new Network(container, data, options);

      this.network.on("click", (params) => {
        if (params.nodes.length > 0) {
          const nodeId = params.nodes[0];
          this.clickedNode = this.graphData.nodes.find(node => node.id === nodeId);
        } else if (params.edges.length > 0) {
          const edgeId = params.edges[0];
          const clickedEdge = this.graphData.edges.find(edge => edge.id === edgeId);
        }
      });
    },
    async getURL() {
      if (!this.clickedNode.name) return;
      try {
        const res = await getSearch({"keyword": this.clickedNode.name});
        this.learnURL = res.data;
      } catch (error) {
        console.error("获取资源失败:", error);
      }
    }
  },
  beforeUnmount() {
    if (this.network) {
      this.network.destroy();
      this.network = null;
    }
  },
  created() {
    const savedHistory = localStorage.getItem('searchHistory');
    if (savedHistory) {
      try {
        this.searchHistory = JSON.parse(savedHistory);
      } catch (e) {
        console.error("Failed to parse search history:", e);
        this.searchHistory = [];
      }
    }
    if (process.env.NODE_ENV === 'development' && (!this.searchHistory || this.searchHistory.length === 0)) {
      this.searchHistory = [...this.devHistory];
      localStorage.setItem('searchHistory', JSON.stringify(this.searchHistory));
    }
  }
};
</script>

<style scoped>
/* 容器样式 */
.knowledge-graph-container {
  display: flex;
  height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  position: relative;
  overflow: hidden;
}

/* 主内容区域（保持固定宽度） */
.main-content {
  display: flex;
  width: 100%;
  height: 100%;
}

/* 历史记录侧边栏（覆盖式） */
.history-sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1000;

}

.history-sidebar {
  position: fixed;
  left: 0;
  top: 0;
  width: 280px; /* 稍微加宽 */
  height: 100vh;
  background: #ffffff;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.05), 8px 0 16px -4px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  z-index: 1001;
  padding: 0; /* 重置内边距 */
  display: flex;
  border-radius: 6px;
  flex-direction: column;
  transform: translateX(-100%);
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
/* 显示状态 */
.history-sidebar.visible {
  transform: translateX(0);
}

/* 滑动动画 */
.slide-enter-active, .slide-leave-active {
  transition: all 0.3s ease;
}
.slide-enter-from, .slide-leave-to {
  opacity: 0;
  transform: translateX(-100%);
}
/* 侧边栏头部 */
.sidebar-header {
  padding: 20px;
  background: linear-gradient(135deg, #3dcd9f 0%, #88d5bd 100%);
  color: white;
  position: sticky;
  top: 0;
  z-index: 10;
}
.sidebar-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.sidebar-close {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 20px;
  padding: 0;
  opacity: 0.8;
}

.sidebar-close:hover {
  opacity: 1;
}
.history-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
/* 搜索框 */
.sidebar-search {
  padding: 10px 5px;
   border-radius: 6px;
  background: #f8f9fa;
  position: sticky;
  top: 64px; /* 头部高度 */
  z-index: 9;
}

.sidebar-search input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.sidebar-search input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
}
.history-list-container {
  flex: 1;
  overflow-y: auto;
  padding: 8px 0;
}

.history-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.history-list li {
  padding: 12px 20px;
  margin: 4px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  color: #2d3748;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: space-between;
}


.history-list li:hover {
  background-color: #f8f9fa;
}

.history-list li.active {
  background: linear-gradient(135deg, #3dcd9f 0%, #7ac4ad 100%);
  color: white;
}
.history-item-time {
  font-size: 12px;
  opacity: 0.7;
  margin-left: 8px;
}

/* 空状态 */
.history-empty {
  padding: 40px 20px;
  text-align: center;
  color: #718096;
}

.history-empty-icon {
  font-size: 32px;
  margin-bottom: 12px;
  opacity: 0.5;
}
/* 历史记录按钮 */
.history-toggle-btn {
  position: fixed;
  left: 20px;
  top: 6rem;
  padding: 10px 16px 10px 14px;
  background: linear-gradient(135deg, #a4a8a7 0%, #7d8482 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  z-index: 999;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  font-size: 14px;
  font-weight: 500;
  /* 添加以下样式使其不像标签 */
  transform: none;
  writing-mode: horizontal-tb;
  height: auto;
  width: auto;
  opacity: 0.95;
}


.history-toggle-btn:hover {
  transform: translateY(-2px) translateX(4px) !important;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15) !important;
  opacity: 1;
}
.icon-history::before {
  content: "🕒";
  font-size: 16px;
}


/* 左侧图谱区域 */
.graph-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
  margin: 20px;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  position: relative;
  z-index: 1;
}

.graph-header {
  background: linear-gradient(135deg, #fbfee0 0%, #8bd7bf 100%);
  color: #4e4f4f;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.graph-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.graph-controls {
  display: flex;
  gap: 12px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}

.btn-primary {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  backdrop-filter: blur(10px);
}

.btn-primary:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  backdrop-filter: blur(10px);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

#network {
  flex: 1;
  background: #fdfdfd;
  border: none;
}

.graph-status {
  background: #f8f9fa;
  padding: 12px 20px;
  border-top: 1px solid #e9ecef;
}

.status-text {
  color: #495057;
  font-size: 14px;
}

/* 右侧资源区域 */
.resources-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
  margin: 20px 20px 20px 0;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  position: relative;
  z-index: 1;
}

.resources-header {
  background: linear-gradient(135deg, #fbfee0 0%, #9be2cc 100%);
  color: #4e4f4f;
  padding: 25px;
}

.resources-title {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 600;
}

.resources-subtitle {
  margin: 0;
  font-size: 14px;
  opacity: 0.9;
}

.resources-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.resource-category {
  margin-bottom: 32px;
}

.category-title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0 0 16px 0;
  font-size: 18px;
  font-weight: 600;
  color: #2d3748;
  padding-bottom: 8px;
  border-bottom: 2px solid #e2e8f0;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 60px 20px;
  color: #718096;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.empty-state h3 {
  margin: 0 0 12px 0;
  font-size: 20px;
  color: #4a5568;
}

.empty-state p {
  margin: 0;
  font-size: 14px;
  line-height: 1.6;
  max-width: 400px;
}

/* 图标样式 */
.icon-search::before { content: "🔍"; }
.icon-download::before { content: "📥"; }
.icon-video::before { content: "🎥"; }
.icon-book::before { content: "📚"; }
.icon-code::before { content: "💻"; }
.icon-globe::before { content: "🌐"; }
.icon-external-link::before { content: "🔗"; }

/* 响应式调整 - 中等屏幕 */
@media (max-width: 1024px) {
  .history-toggle-btn {
    left: 20px;
    top: 5rem; /* 稍微减少顶部距离 */
    font-size: 13px;
    padding: 8px 14px 8px 12px;
  }
}

/* 响应式调整 - 平板设备 */
@media (max-width: 768px) {
  .history-toggle-btn {
    left: 16px;
    top: 70px; /* 使用固定像素值确保不被rem影响 */
    padding: 7px 12px 7px 10px;
    font-size: 12px;
    gap: 6px;
  }
}

/* 响应式调整 - 手机设备 */
@media (max-width: 480px) {
  .history-toggle-btn {
    left: 12px;
    top: 60px;
    padding: 6px 10px 6px 8px;
    font-size: 11px;
    border-radius: 6px;
  }
  
  .icon-history::before {
    font-size: 14px;
  }
}

/* 超小屏幕处理 */
@media (max-width: 360px) {
  .history-toggle-btn {
    left: 8px;
    top: 55px;
    padding: 5px 8px;
    gap: 4px;
  }
  
  .history-toggle-btn span {
    display: none; /* 超小屏幕隐藏文字，只显示图标 */
  }
}
</style>