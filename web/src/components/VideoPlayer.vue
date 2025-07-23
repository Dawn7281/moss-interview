<template>
  <div class="video-player">
    <h3>{{ videoTitle }}</h3>
    <video controls width="100%">
      <source :src="videoSrc" type="video/mp4">
      您的浏览器不支持HTML5视频标签。
    </video>
  </div>
</template>

<script>
export default {
  name: 'VideoPlayer',
  props: {
    videoTitle: {
      type: String,
      required: true
    },
    videoSrc: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
.video-player {
  margin-top: 20px;
}

.video-player h3 {
  color: #32ca99;
  margin-bottom: 10px;
}

video {
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>