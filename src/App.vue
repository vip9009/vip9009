<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { RouterView, useRouter } from 'vue-router'
import SiteHeader from '@/components/SiteHeader.vue'
import SiteFooter from '@/components/SiteFooter.vue'
import ContactWidget from '@/components/ContactWidget.vue'
import AgeGate from '@/components/AgeGate.vue'
import { preloadPrimaryViews, preloadView } from '@/router/lazyViews'
import { prefetchPathImages } from '@/utils/prefetch'
import { asset } from '@/utils'

const booting = ref(true)

const router = useRouter()
const showProgress = ref(false)
const mainRef = ref(null)

function skipToMain() {
  mainRef.value?.focus({ preventScroll: true })
  mainRef.value?.scrollIntoView({ block: 'start' })
}

let progressTimer = null

const removeBefore = router.beforeEach((to, from) => {
  if (to.path === from.path) return
  clearTimeout(progressTimer)
  // Only show the bar when a transition actually takes noticeable time.
  progressTimer = setTimeout(() => {
    showProgress.value = true
  }, 120)
})

const removeAfter = router.afterEach(() => {
  clearTimeout(progressTimer)
  showProgress.value = false
})

const removeError = router.onError(() => {
  clearTimeout(progressTimer)
  showProgress.value = false
})

function parsePath(href) {
  if (!href || !href.startsWith('#/')) return ''
  return href.slice(1)
}

function preloadForPath(path) {
  const pathname = path.split('?')[0]
  if (pathname.startsWith('/category')) preloadView('category')
  else if (pathname.startsWith('/product')) preloadView('product')
  else if (pathname === '/search') preloadView('search')
  else if (pathname === '/contact') preloadView('contact')
  else if (pathname === '/cart') preloadView('cart')
  else if (pathname === '/checkout') preloadView('checkout')
  else if (pathname === '/activity') preloadView('activity')
  else if (pathname.startsWith('/info/')) preloadView('info')
  else if (pathname === '/sitemap') preloadView('sitemap')

  prefetchPathImages(path)
}

function onIntent(event) {
  const anchor = event.target?.closest?.('a')
  if (!anchor) return
  const path = parsePath(anchor.getAttribute('href'))
  if (path) preloadForPath(path)
}

onMounted(() => {
  const started = Date.now()
  const hideBoot = () => {
    booting.value = false
  }
  const finishBoot = () => {
    const wait = Math.max(0, 1100 - (Date.now() - started))
    window.setTimeout(hideBoot, wait)
  }
  window.setTimeout(hideBoot, 2500)
  if (document.readyState === 'complete') finishBoot()
  else window.addEventListener('load', finishBoot, { once: true })

  document.addEventListener('pointerover', onIntent, { passive: true })
  document.addEventListener('focusin', onIntent)

  if ('requestIdleCallback' in window) {
    window.requestIdleCallback(() => preloadPrimaryViews(), { timeout: 2500 })
  } else {
    setTimeout(preloadPrimaryViews, 1500)
  }
})

onBeforeUnmount(() => {
  document.removeEventListener('pointerover', onIntent)
  document.removeEventListener('focusin', onIntent)
  removeBefore()
  removeAfter()
  removeError()
  clearTimeout(progressTimer)
})
</script>

<template>
  <div class="site">
    <Transition name="boot-fade">
      <div v-if="booting" class="boot-loader" aria-hidden="true">
        <img class="boot-logo" :src="asset('/images/ui/logo-vapepu.webp')" alt="" />
        <span class="boot-spinner" />
      </div>
    </Transition>
    <a class="skip-link" href="#main-content" @click.prevent="skipToMain">跳到主要内容</a>
    <div class="route-progress" :class="{ active: showProgress }" aria-hidden="true">
      <span />
    </div>
    <div class="sr-only" role="status" aria-live="polite">
      {{ showProgress ? '页面加载中' : '' }}
    </div>
    <SiteHeader />
    <main ref="mainRef" id="main-content" class="site-content" tabindex="-1" :aria-busy="showProgress">
      <RouterView />
    </main>
    <SiteFooter />
    <ContactWidget />
    <AgeGate />
  </div>
</template>

<style scoped>
.boot-loader {
  position: fixed;
  inset: 0;
  z-index: 5000;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 22px;
  background: rgba(255, 255, 255, 0.94);
  backdrop-filter: blur(1px);
}

.boot-logo {
  width: 150px;
  height: auto;
  opacity: 0.9;
}

.boot-spinner {
  width: 28px;
  height: 28px;
  border: 2px solid rgba(0, 0, 0, 0.14);
  border-top-color: #242125;
  border-radius: 50%;
  animation: boot-spin 0.8s linear infinite;
}

@keyframes boot-spin {
  to {
    transform: rotate(360deg);
  }
}

.boot-fade-leave-active {
  transition: opacity 0.35s ease;
}

.boot-fade-leave-to {
  opacity: 0;
}

@media (prefers-reduced-motion: reduce) {
  .boot-spinner {
    animation-duration: 1.8s;
  }
}

.route-progress {
  position: fixed;
  top: 0;
  right: 0;
  left: 0;
  z-index: 9999;
  height: 2px;
  overflow: hidden;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.15s ease;
}

.route-progress.active {
  opacity: 1;
}

.route-progress span {
  display: block;
  width: 36%;
  height: 100%;
  background: linear-gradient(90deg, var(--color-primary), var(--color-accent));
  border-radius: 0 2px 2px 0;
  animation: route-progress 0.9s ease-in-out infinite;
}

@keyframes route-progress {
  0% {
    transform: translateX(-110%);
  }
  100% {
    transform: translateX(320%);
  }
}
</style>
