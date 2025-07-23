<template>
  <div class="page">
    <div class="search-box">
      <input type="text" v-model="seed" placeholder="请输入关键词" @keyup.enter="updateGraphData(seed)">
      <svg class="search-icon" viewBox="0 0 24 24" @click="updateGraphData(seed)">
        <path d="M15.5 14h-.79l-.28-.27a6.5 6.5 0 0 0 1.48-5.34c-.47-2.78-2.79-5-5.59-5.34a6.505 6.505 0 0 0-7.27 7.27c.34 2.8 2.56 5.12 5.34 5.59a6.5 6.5 0 0 0 5.34-1.48l.27.28v.79l4.25 4.25c.41.41 1.08.41 1.49 0 .41-.41.41-1.08 0-1.49L15.5 14zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
      </svg>
    </div>
    <div id="graph">
      <KnowledgeGraph 
        :graphData="GraphData"
        :history="history"
        :historyIndex="historyIndex"
        @keyword-selected="handleKeywordSelected"
      />
    </div>
    <!-- 加载提示 -->
    <div v-if="generating" class="loading-overlay">
      <div class="loading-content">
        <div class="spinner"></div>
        <p>正在生成知识图谱，请稍候...</p>
      </div>
    </div>
  </div>
</template>

<script>
import KnowledgeGraph from '@/components/KnowledgeGraph.vue';
import {feedbackGraph, getGraph, updateGraph} from "@/api/search";
import store from "@/store";

export default {
  name: 'GraphView',
  components: {
    KnowledgeGraph,
  },
  data() {
    return {
      GraphData: {},
      history: [],
      historyIndex: 0,
      seed: "",
      generating: false,
    };
  },
  methods: {
    async getGraphData() {
      try {
        this.generating = true;
        const res = await getGraph({"username": store.state.user?.username});
        if (res.status !== 200) return;
        this.GraphData = res.data.graph;
        this.history = res.data.history.reverse();
        console.log(res.data);
        return res.data.graph;
      } catch (error) {
        console.error("获取图数据失败:", error);
        throw error;
      } finally {
        this.generating = false;
      }
    },
    
    async updateGraphData(seed) {
      console.log(seed)
      if (!seed.trim()) return;

      try {
        this.generating = true;
        const res = await updateGraph({ "keyword": seed, "username": store.state.user?.username });
        if (res.status !== 200) return;
        this.GraphData = res.data.graph;
        if (res.data.history.length !== this.history.length) {
          this.history = res.data.history.reverse();
          this.historyIndex = 0;
        }
        this.seed = "";
      } catch (error) {
        console.error("更新图数据失败:", error);
        throw error;
      } finally {
        this.generating = false;
      }
    },

    async handleFeedback(feedback) {
      try {
        this.generating = true;
        const res = await feedbackGraph({'feedback': feedback, username: store.state.user?.username});
        if (res.status !== 200) return;
        this.GraphData = res.data.graph;
        this.history = res.data.history.reverse();
      } finally {
        this.generating = false;
      }
    },

    // 处理关键词选择的方法
    handleKeywordSelected(keyword, index) {
      this.historyIndex = index;
      this.updateGraphData(keyword);
    }
  },
  async mounted() {
    if (this.$route.query.feedback) {
      await this.handleFeedback(this.$route.query.feedback)
    } else {
      await this.getGraphData()
    }

  },
};
</script>

<style>
.page {
  width: 90vw;
  margin-left: calc(-50vw + 56%);
  padding: 26px 16px;
  background-color: #ffffff;
  min-height: 100vh;
  box-sizing: border-box;
}

.search-box {
  position: relative;
  flex-grow: 1;
  margin-bottom: 1.5rem;
  max-width: 300px;
  margin-left: 20px;
}

.search-box input {
  width: 100%;
  height: 40px;
  padding: 0 10px 0 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  background-color: #f8f8f8;
}

.search-icon {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  fill: #999;
  cursor: pointer;
}

/* 加载动画 */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.loading-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid var(--primary-blue);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}
.filter-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 15px 0 0;
  padding: 5px 0;
  white-space: nowrap;
  flex-shrink: 0;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>