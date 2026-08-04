<script setup>
import { onMounted } from 'vue'

onMounted(() => {
  createParticles()
})

function createParticles() {
  const container = document.querySelector('.fire-particles')
  if (!container) return
  
  setInterval(() => {
    const particle = document.createElement('div')
    particle.className = 'particle'
    particle.style.left = Math.random() * 100 + '%'
    particle.style.animationDuration = (Math.random() * 3 + 2) + 's'
    particle.style.opacity = Math.random() * 0.5 + 0.3
    container.appendChild(particle)
    
    setTimeout(() => particle.remove(), 5000)
  }, 300)
}
</script>

<template>
  <div class="fire-particles"></div>
</template>

<style scoped>
.fire-particles {
  position: fixed;
  top: 0;
  left:  0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.particle {
  position: absolute;
  bottom: -10px;
  width: 4px;
  height: 4px;
  background: radial-gradient(circle, #ff4500, #ffa726);
  border-radius: 50%;
  animation:  rise linear infinite;
  box-shadow: 0 0 10px rgba(255, 69, 0, 0.8);
}

@keyframes rise {
  0% {
    transform: translateY(0) scale(1);
    opacity: 1;
  }
  100% {
    transform: translateY(-100vh) scale(0);
    opacity: 0;
  }
}
</style>