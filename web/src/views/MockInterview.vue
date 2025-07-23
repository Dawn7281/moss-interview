<template>
  <div class="mock-interview">
    <SceneSetting />
    <InterviewModules />
  </div>
</template>

<script>
import SceneSetting from '@/components/SceneSetting.vue'


export default {
  name: 'MockInterview',
  components: {
    SceneSetting,
  }
}
</script>

<style scoped>
.mock-interview {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}
</style>