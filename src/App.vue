<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { RouterView, useRouter } from 'vue-router'
import SiteHeader from '@/components/SiteHeader.vue'
import SiteFooter from '@/components/SiteFooter.vue'
import ContactWidget from '@/components/ContactWidget.vue'
import { preloadPrimaryViews, preloadView } from '@/router/lazyViews'
import { prefetchPathImages } from '@/utils/prefetch'

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
  </div>
</template>

<style scoped>
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
