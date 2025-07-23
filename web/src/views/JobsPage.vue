<template>
  <div class="jobs-page">
    <div class="page-header">
      <h1>在招职位</h1>
      <div class="filters">
        <div class="filter-dropdown">
          <select v-model="jobTypeFilter" @change="queryJobInfo">
            <option
                v-for="type in jobTypes"
                :key="type.value"
                :value="type.value"
            >
              {{ type.label }}
            </option>
          </select>
        </div>
        <div class="filter-dropdown">
          <select v-model="cityFilter" @change="queryJobInfo">
            <option
                v-for="city in cities"
                :key="city.value"
                :value="city.value"
            >
              {{ city.label }}
            </option>
          </select>
        </div>

        <div class="search-box">
          <input type="text" placeholder="请输入公司名或职位名搜索" v-model="searchQuery" @keyup.enter="queryJobInfo">
          <svg class="search-icon" viewBox="0 0 24 24" @click="queryJobInfo">
            <path d="M15.5 14h-.79l-.28-.27a6.5 6.5 0 0 0 1.48-5.34c-.47-2.78-2.79-5-5.59-5.34a6.505 6.505 0 0 0-7.27 7.27c.34 2.8 2.56 5.12 5.34 5.59a6.5 6.5 0 0 0 5.34-1.48l.27.28v.79l4.25 4.25c.41.41 1.08.41 1.49 0 .41-.41.41-1.08 0-1.49L15.5 14zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
          </svg>
        </div>
      </div>
    </div>

    <div class="jobs-grid">
      <JobCard
          v-for="(job, index) in jobs"
          :key="index"
          :job="job"
      />
      <p v-if="jobs.length === 0" class="no-jobs-message">暂无匹配的职位。</p>
    </div>

    <div class="pagination">
      <button :disabled="currentPage === 1" @click="changePage(currentPage - 1)">上一页</button>
      <span>{{ currentPage }} / {{ totalPages }}</span>
      <button :disabled="currentPage === totalPages" @click="changePage(currentPage + 1)">下一页</button>
    </div>
  </div>
</template>

<script>
import JobCard from '@/components/JobCard.vue'
import { getJob } from "@/api/job";

export default {
  components: { JobCard },
  data() {
    return {
      identityFilter: 'all', // Unused in template, consider removing if not needed
      jobTypeFilter: 'all',
      cityFilter: 'all',
      searchQuery: '',
      minSalary: '',
      maxSalary: '',
      jobTypes: [
        {value: 'all', label: '全部职位'},
        {value: 'Java', label: 'Java开发'},
        {value: '前端', label: '前端开发'},
        {value: '后端', label: '后端开发'},
        {value: 'Android', label: 'Android开发'},
        {value: 'iOS', label: 'iOS开发'},
        {value: '大数据', label: '大数据开发'},
        {value: '人工智能', label: '人工智能'},
        {value: '运维', label: '运维开发'},
        {value: '测试工程师', label: '测试工程师'},
        {value: '产品经理', label: '产品经理'},
        {value: 'UI设计师', label: 'UI设计师'}
      ],
      cities: [
        {value: 'all', label: '全部城市'},
        {value: '北京', label: '北京'},
        {value: '上海', label: '上海'},
        {value: '广州', label: '广州'},
        {value: '深圳', label: '深圳'},
        {value: '杭州', label: '杭州'},
        {value: '成都', label: '成都'},
        {value: '重庆', label: '重庆'},
        {value: '武汉', label: '武汉'},
        {value: '南京', label: '南京'},
        {value: '苏州', label: '苏州'},
        {value: '西安', label: '西安'}
      ],
      jobs: [], // Initialize as an empty array
      currentPage: 1,
      totalPages: 1,
      totalItems: 0,
      itemsPerPage: 20 // Matches the backend default
    }
  },
  methods: {
      async applySalaryFilter() {
      this.currentPage = 1;
      await this.fetchJobs();
    },
    async queryJobInfo() {
      // Always reset to the first page when applying new filters or search
      this.currentPage = 1;
      await this.fetchJobs();
    },
    async fetchJobs() {
      const data = {
        'search': this.searchQuery,
        'title': this.jobTypeFilter,
        'location': this.cityFilter,
        'min_salary': this.minSalary,
        'max_salary': this.maxSalary,
        'page': this.currentPage,
        'per_page': this.itemsPerPage
      };
      console.log('Requesting jobs with:', data);
      try {
        const res = await getJob(data);
        this.jobs = res.data.data;
        this.totalPages = res.data.totalPages;
        this.currentPage = res.data.currentPage;
        this.totalItems = res.data.totalItems;
        console.log('Received job data:', this.jobs);
      } catch (error) {
        console.error('Error fetching job info:', error);
        // Optionally, display an error message to the user
      }
    },
    changePage(page) {
      if (page > 0 && page <= this.totalPages) {
        this.currentPage = page;
        this.fetchJobs(); // Fetch new data for the selected page
      }
    }
  },
  mounted() {
    this.fetchJobs(); // Initial fetch when the component mounts
  }
}
</script>

<style scoped>
.jobs-page {
 width: 90vw; /* 使用视口宽度确保撑满整个页面 */
  margin-left: calc(-50vw + 56%); /* 抵消父容器的padding/margin */
  padding: 40px 55px; /* 只保留上下padding */
  background-color: #ffffff;
  min-height: 100vh;
  border-radius: 14px;
  box-sizing: border-box; /* 确保padding包含在宽度内 */
}

.page-header {
  margin-bottom: 24px;
  padding: 0 10px; /* 头部内容保留10px边距 */
}

.page-header h1 {
  padding: 0 26px; 
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 24px;
  color: #333;
}

.filters {
  display: flex;
  gap: 12px;
  align-items: center;
  padding: 0 10px; /* 筛选栏也保留10px边距 */
  margin-left: 0; /* 确保筛选栏左对齐 */
}

.filter-dropdown select {
  width: 140px;
  height: 40px;
  padding: 0 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  color: #333;
  background-color: #f8f8f8;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 16px;
}

.search-box {
   position: relative;
  flex-grow: 1;
  max-width: 300px;  /* 限制搜索框最大宽度 */
  margin-left: 20px;  /* 增加左边距 */
}

.search-box input {
   width: 100%;
  height: 40px;
  padding: 0 10px 0 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  background-color: #f8f8f8; /* 添加这行设置背景色 */
}

.search-icon {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  fill: #999;
}

.jobs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(290px, 1fr)); /* 增大卡片最小宽度 */
  gap: 20px; /* 统一间距 */
  padding: 0 17px; /* 增大两侧内边距 */
  width: 100%;
  box-sizing: border-box;

  max-width: 1300px; /* 限制最大宽度 */
}


@media (max-width: 768px) {
  .jobs-grid {
    gap: 20px; /* 在小屏幕上减少间距 */
  }
}

.no-jobs-message {
  grid-column: 1 / -1; /* Span across all columns */
  text-align: center;
  padding: 50px;
  color: #777;
  font-size: 1.2em;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin-top: 20px;
}

.pagination button {
  padding: 8px 15px;
  border: 1px solid #42b983;
  border-radius: 4px;
  background-color: #42b983;
  color: white;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.2s, opacity 0.2s;
}

.pagination button:disabled {
  background-color: #cccccc;
  border-color: #cccccc;
  cursor: not-allowed;
  opacity: 0.7;
}

.pagination button:not(:disabled):hover {
  background-color: #42b983;
}

.pagination span {
  font-size: 1.1em;
  color: #333;
}

</style>