<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const progress = ref(0)

const updateProgress = () => {
  const windowHeight = window.innerHeight
  const documentHeight = document.documentElement.scrollHeight
  const scrollTop = window.scrollY
  const scrollPercent = (scrollTop / (documentHeight - windowHeight)) * 100
  progress.value = Math.min(scrollPercent, 100)
}

onMounted(() => {
  window.addEventListener('scroll', updateProgress)
  updateProgress()
})

onUnmounted(() => {
  window.removeEventListener('scroll', updateProgress)
})
</script>

<template>
  <div class="progress-bar-container" role="progressbar" :aria-valuenow="Math.round(progress)" aria-valuemin="0" aria-valuemax="100" aria-label="Page scroll progress">
    <div class="progress-bar" :style="{ width: progress + '%' }"></div>
  </div>
</template>

<style scoped>
.progress-bar-container {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: transparent;
  z-index: 1000;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #cd3b86, #2962eb);
  transition: width 0.1s ease;
  box-shadow: 0 0 10px rgba(255, 69, 0, 0.5);
}
</style>
