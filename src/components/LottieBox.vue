<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { asset } from '@/utils'

const props = defineProps({
  src: { type: String, required: true },
  loop: { type: Boolean, default: true },
  autoplay: { type: Boolean, default: true },
  speed: { type: Number, default: 1 },
  fit: { type: String, default: 'contain' },
  label: { type: String, default: '' }
})

const container = ref(null)
let animation = null

onMounted(async () => {
  try {
    const [{ default: lottie }, response] = await Promise.all([
      import('lottie-web'),
      fetch(asset(props.src))
    ])
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    const data = await response.json()
    const preserveAspectRatio =
      props.fit === 'fill'
        ? 'none'
        : props.fit === 'cover'
          ? 'xMidYMid slice'
          : 'xMidYMid meet'
    animation = lottie.loadAnimation({
      container: container.value,
      renderer: 'svg',
      loop: props.loop,
      autoplay: props.autoplay,
      animationData: data,
      rendererSettings: {
        preserveAspectRatio,
        progressiveLoad: true
      }
    })
    animation.setSpeed(props.speed)
  } catch (error) {
    container.value?.classList.add('is-error')
  }
})

onBeforeUnmount(() => {
  animation?.destroy()
})
</script>

<template>
  <div ref="container" class="lottie-box" role="img" :aria-label="label" />
</template>

<style scoped>
.lottie-box {
  width: 100%;
  height: 100%;
}

.lottie-box :deep(svg) {
  display: block;
  width: 100%;
  height: 100%;
}
</style>
