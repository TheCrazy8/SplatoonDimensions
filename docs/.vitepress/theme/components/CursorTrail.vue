<script setup>
import { onMounted, onUnmounted } from 'vue'

let canvas, ctx
const particles = []

onMounted(() => {
  canvas = document.createElement('canvas')
  canvas.style.position = 'fixed'
  canvas.style.top = '0'
  canvas.style.left = '0'
  canvas.style.pointerEvents = 'none'
  canvas.style.zIndex = '9999'
  canvas.width = window.innerWidth
  canvas.height = window.innerHeight
  document.body.appendChild(canvas)
  
  ctx = canvas.getContext('2d')
  
  window.addEventListener('mousemove', createParticle)
  window.addEventListener('resize', resizeCanvas)
  
  animate()
})

onUnmounted(() => {
  window.removeEventListener('mousemove', createParticle)
  window.removeEventListener('resize', resizeCanvas)
  if (canvas) canvas.remove()
})

function createParticle(e) {
  particles.push({
    x: e.clientX,
    y: e.clientY,
    size: Math.random() * 5 + 2,
    speedY: Math.random() * -2 - 1,
    life: 1
  })
}

function resizeCanvas() {
  canvas.width = window.innerWidth
  canvas.height = window.innerHeight
}

function animate() {
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  
  for (let i = particles.length - 1; i >= 0; i--) {
    const p = particles[i]
    
    p.y += p.speedY
    p.life -= 0.02
    
    if (p.life <= 0) {
      particles.splice(i, 1)
      continue
    }
    
    const gradient = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.size)
    gradient.addColorStop(0, `rgba(255, 69, 0, ${p.life})`)
    gradient.addColorStop(0.5, `rgba(255, 167, 38, ${p.life * 0.5})`)
    gradient.addColorStop(1, `rgba(255, 200, 0, 0)`)
    
    ctx.fillStyle = gradient
    ctx.beginPath()
    ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2)
    ctx.fill()
  }
  
  requestAnimationFrame(animate)
}
</script>

<template>
  <div></div>
</template>