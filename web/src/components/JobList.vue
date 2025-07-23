<template>
  <div class="job-list">
    <JobCard 
      v-for="job in jobs" 
      :key="job.id"
      :job="job"
      :expanded-id="expandedId"
      @toggle-expand="handleToggleExpand"
    />
  </div>
</template>

<script>
import JobCard from '@/components/JobCard.vue'

export default {
  components: { JobCard },
  data() {
    return {
      expandedId: null,
      jobs: [] // 您的职位数据
    }
  },
  methods: {
    handleToggleExpand(jobId) {
      this.expandedId = this.expandedId === jobId ? null : jobId
    }
  }
}
</script>