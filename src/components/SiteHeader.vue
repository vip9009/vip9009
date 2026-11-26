<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { site } from '@/data'
import AppIcon from '@/components/AppIcon.vue'

const route = useRoute()
const router = useRouter()

const keyword = ref('')
const drawerOpen = ref(false)
const drawerRef = ref(null)
const drawerCloseRef = ref(null)
const menuBtnRef = ref(null)
const searchOpen = ref(false)
const scrolled = ref(false)
const openGroups = ref([])
const mobileSearchInput = ref(null)
const desktopSearchInput = ref(null)

function submitSearch() {
  const q = keyword.value.trim()
  if (!q) {
    const target = desktopSearchInput.value?.offsetParent
      ? desktopSearchInput.value
      : mobileSearchInput.value
    target?.focus()
    return
  }
  router.push({ path: '/search', query: { q } })
  searchOpen.value = false
}

async function openSearch() {
  searchOpen.value = true
  await nextTick()
  mobileSearchInput.value?.focus()
}

function toggleGroup(label) {
  openGroups.value = openGroups.value.includes(label)
    ? openGroups.value.filter((item) => item !== label)
    : [...openGroups.value, label]
}

function closeMenu() {
  drawerOpen.value = false
  searchOpen.value = false
}

function onScroll() {
  scrolled.value = window.scrollY > 48
}

watch(drawerOpen, async (open) => {
  document.body.style.overflow = open ? 'hidden' : ''
  if (open) {
    await nextTick()
    drawerCloseRef.value?.focus()
  } else {
    menuBtnRef.value?.focus()
  }
})

function onKeydown(event) {
  if (event.key !== 'Escape') return
  if (searchOpen.value) {
    searchOpen.value = false
  } else if (drawerOpen.value) {
    drawerOpen.value = false
  }
}

function trapDrawerFocus(event) {
  if (event.key !== 'Tab') return
  const nodes = drawerRef.value?.querySelectorAll(
    'a[href], button:not([disabled]), input, [tabindex]:not([tabindex="-1"])'
  )
  if (!nodes || !nodes.length) return
  const focusable = [...nodes].filter((node) => node.offsetParent !== null)
  const first = focusable[0]
  const last = focusable[focusable.length - 1]
  if (!first || !last) return
  if (event.shiftKey && document.activeElement === first) {
    event.preventDefault()
    last.focus()
  } else if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault()
    first.focus()
  }
}

watch(
  () => route.fullPath,
  () => {
    closeMenu()
  }
)

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })
  document.addEventListener('keydown', onKeydown)
  onScroll()
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScroll)
  document.removeEventListener('keydown', onKeydown)
  document.body.style.overflow = ''
})
</script>

<template>
  <header class="header-shell" :class="{ 'is-scrolled': scrolled }">
    <div class="header-top">
      <div class="wrapper header-top-inner">
        <div class="top-links">
          <RouterLink v-for="link in site.topLinks" :key="link.label" :to="link.to">
            {{ link.label }}
          </RouterLink>
          <span class="top-tagline">真人选品 · 扫码验真</span>
        </div>

        <div class="top-actions">
          <button class="mobile-top-search" type="button" aria-label="搜索" @click="openSearch">
            <AppIcon name="search" :size="22" />
          </button>

          <form class="top-search" role="search" @submit.prevent="submitSearch">
            <input
              ref="desktopSearchInput"
              v-model="keyword"
              type="search"
              name="s"
              placeholder="搜索产品名称"
              aria-label="搜索产品名称"
              autocomplete="off"
            />
            <button class="search-submit" type="submit" aria-label="搜索">
              <AppIcon name="search" :size="18" />
            </button>
          </form>
        </div>
      </div>
    </div>

    <div class="header-main">
      <div class="wrapper header-main-inner">
        <button ref="menuBtnRef" class="menu-btn" type="button" aria-label="打开菜单" @click="drawerOpen = true">
          <AppIcon name="menu" :size="22" />
        </button>

        <RouterLink class="brand" to="/" aria-label="泡泡哥雾化首页">
          <span class="brand-mark">泡泡哥雾化<span class="brand-dot" /></span>
          <span class="brand-en">PAOPAO VAPE</span>
        </RouterLink>

        <nav class="main-nav" aria-label="主导航">
          <ul>
            <li
              v-for="item in site.nav"
              :key="item.label"
              :class="{ 'has-sub': item.children && item.children.length }"
            >
              <RouterLink :to="item.to">
                <span>{{ item.label }}</span>
                <AppIcon v-if="item.children && item.children.length" name="chevron-down" :size="14" />
              </RouterLink>

              <ul v-if="item.children && item.children.length" class="submenu">
                <li
                  v-for="child in item.children"
                  :key="child.label"
                  :class="{ 'has-sub': child.children && child.children.length }"
                >
                  <RouterLink :to="child.to">
                    <span>{{ child.label }}</span>
                    <AppIcon
                      v-if="child.children && child.children.length"
                      name="chevron-right"
                      :size="14"
                    />
                  </RouterLink>
                  <ul v-if="child.children && child.children.length" class="submenu submenu-nested">
                    <li v-for="leaf in child.children" :key="leaf.label">
                      <RouterLink :to="leaf.to">{{ leaf.label }}</RouterLink>
                    </li>
                  </ul>
                </li>
              </ul>
            </li>
          </ul>
        </nav>

        <div class="header-tools">
          <button type="button" aria-label="搜索" @click="openSearch">
            <AppIcon name="search" :size="21" />
          </button>
        </div>

        <RouterLink class="header-cta" to="/contact">
          立即咨询
          <AppIcon name="arrow-right" :size="15" />
        </RouterLink>
      </div>
    </div>
  </header>

  <Teleport to="body">
    <Transition name="fade">
      <div v-if="drawerOpen" class="drawer-mask" @click="drawerOpen = false" />
    </Transition>

    <aside
      ref="drawerRef"
      class="drawer"
      :class="{ open: drawerOpen }"
      role="dialog"
      aria-modal="true"
      aria-label="移动端菜单"
      @keydown="trapDrawerFocus"
    >
      <div class="drawer-head">
        <RouterLink to="/" aria-label="泡泡哥雾化首页">
          <span class="drawer-brand">泡泡哥雾化<span class="brand-dot" /></span>
        </RouterLink>
        <button ref="drawerCloseRef" type="button" aria-label="关闭菜单" @click="drawerOpen = false">
          <AppIcon name="close" :size="22" />
        </button>
      </div>

      <div class="drawer-body">
        <div v-for="item in site.nav" :key="item.label" class="drawer-item">
          <div class="drawer-row">
            <RouterLink class="drawer-link" :to="item.to" @click="drawerOpen = false">
              {{ item.label }}
            </RouterLink>
            <button
              v-if="item.children && item.children.length"
              class="drawer-toggle"
              type="button"
              :aria-expanded="openGroups.includes(item.label)"
              :aria-label="`展开${item.label}`"
              @click="toggleGroup(item.label)"
            >
              <AppIcon :name="openGroups.includes(item.label) ? 'minus' : 'plus'" :size="16" />
            </button>
          </div>

          <ul v-if="item.children && item.children.length && openGroups.includes(item.label)" class="drawer-sub">
            <li v-for="child in item.children" :key="child.label">
              <RouterLink :to="child.to" @click="drawerOpen = false">{{ child.label }}</RouterLink>
            </li>
          </ul>
        </div>
      </div>

      <div class="drawer-foot">
        <RouterLink to="/contact" @click="drawerOpen = false">微信 / QQ 咨询</RouterLink>
        <span class="drawer-qq">QQ：{{ site.contacts.qq.number }}</span>
      </div>
    </aside>

    <div
      v-if="searchOpen"
      class="search-overlay"
      role="dialog"
      aria-modal="true"
      aria-label="站内搜索"
    >
      <div class="search-overlay-inner">
        <form class="overlay-search" @submit.prevent="submitSearch">
          <input
            ref="mobileSearchInput"
            v-model="keyword"
            type="search"
            placeholder="搜索产品名称"
            aria-label="搜索产品名称"
            autocomplete="off"
          />
          <button type="submit" class="overlay-submit">搜索</button>
          <button type="button" class="overlay-close" aria-label="关闭搜索" @click="searchOpen = false">
            <AppIcon name="close" :size="22" />
          </button>
        </form>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.header-shell {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: #fff;
  box-shadow: 0 5px 40px rgba(17, 58, 93, 0.07);
  transition: transform 0.3s ease;
}

.header-shell.is-scrolled {
  transform: translateY(-64px);
}

.header-top {
  height: 64px;
  background: #fff;
}

.header-top-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  font-size: 13px;
}

.top-links a {
  display: inline-flex;
  align-items: center;
  padding: 21px 0;
  color: #121212;
  transition: color 0.18s ease;
}

.top-links a:hover {
  color: var(--accent);
}

.top-actions {
  display: flex;
  align-items: center;
}

.top-search {
  position: relative;
  display: flex;
  align-items: center;
  width: 236px;
  height: 34px;
  background: rgba(204, 204, 204, 0.21);
  border-radius: 4px;
}

.top-search input {
  flex: 1;
  min-width: 0;
  height: 100%;
  padding: 8px;
  font-size: 12px;
  background: none;
  border: 0;
  outline: none;
}

.top-search input::placeholder {
  color: #121212;
  opacity: 0.55;
}

.top-search input::-webkit-search-cancel-button {
  display: none;
}

.search-submit {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 100%;
  color: #121212;
}

.search-submit::after {
  content: '';
  position: absolute;
  inset: -5px 0;
}

.mobile-top-search {
  position: relative;
  display: none;
  align-items: center;
  justify-content: center;
  color: #121212;
}

.mobile-top-search::after {
  content: '';
  position: absolute;
  inset: -6px;
}

.header-main {
  height: 58px;
  background: #fff;
}

.header-main-inner {
  display: flex;
  align-items: center;
  height: 58px;
}

.menu-btn {
  display: none;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  margin-right: 4px;
}

.brand {
  display: flex;
  align-items: center;
  flex: 0 0 auto;
  margin-right: 30px;
  padding: 12px 0;
}

.main-nav {
  flex: 1;
  min-width: 0;
}

.main-nav > ul {
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

.main-nav > ul > li {
  position: relative;
  display: flex;
}

.main-nav > ul > li > a {
  position: relative;
  display: flex;
  align-items: center;
  gap: 1px;
  height: 57px;
  padding: 0 12px;
  font-size: 14px;
  line-height: 57px;
  white-space: nowrap;
}

.main-nav > ul > li:first-child > a {
  padding-left: 0;
}

.main-nav > ul > li > a::after {
  content: '';
  position: absolute;
  right: 12px;
  bottom: 0;
  left: 12px;
  height: 3px;
  background: var(--accent);
  transform: scale(1, 0);
  transform-origin: bottom center;
  transition: transform 0.2s ease-out;
}

.main-nav > ul > li:first-child > a::after {
  left: 0;
}

.main-nav > ul > li:hover > a::after {
  transform: scale(1, 1);
}

.main-nav > ul > li > a :deep(svg) {
  color: #bbb;
  transition: transform 0.15s ease;
}

.main-nav > ul > li:hover > a :deep(svg) {
  transform: rotate(180deg);
}

.main-nav > ul > li:focus-within > a :deep(svg) {
  transform: rotate(180deg);
}

.submenu {
  position: absolute;
  top: 100%;
  left: 0;
  z-index: 20;
  min-width: 190px;
  padding: 10px 0;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.16);
  opacity: 0;
  visibility: hidden;
  transform: translateY(8px);
  transition: opacity 0.18s ease, transform 0.18s ease, visibility 0.18s;
}

.has-sub:hover > .submenu {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.has-sub:focus-within > .submenu {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.submenu li {
  position: relative;
}

.submenu li > a {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 10px 14px;
  font-size: 14px;
  white-space: nowrap;
  transition: background 0.15s ease, color 0.15s ease;
}

.submenu li > a:hover {
  color: var(--accent);
  background: #f5f6f7;
}

.submenu-nested {
  top: -10px;
  left: 100%;
}

.submenu li:hover > .submenu-nested {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.header-tools {
  display: none;
  align-items: center;
  margin-left: auto;
}

.header-tools button {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
}

.header-tools button::after {
  content: '';
  position: absolute;
  inset: -2px;
}

.menu-btn,
.header-tools button {
  color: #121212;
}

/* Drawer */
.drawer-mask {
  position: fixed;
  inset: 0;
  z-index: 200;
  background: rgba(0, 0, 0, 0.55);
}

.drawer {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  z-index: 201;
  display: flex;
  flex-direction: column;
  width: min(84vw, 340px);
  background: #fff;
  transform: translateX(-101%);
  transition: transform 0.25s ease;
  overflow-y: auto;
}

.drawer.open {
  transform: translateX(0);
}

.drawer-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex: 0 0 auto;
  height: 58px;
  padding: 0 14px;
  border-bottom: 1px solid #f0f0f0;
}

.drawer-brand {
  display: inline-flex;
  align-items: flex-start;
  gap: 4px;
  font-family: var(--font-heading);
  font-size: 23px;
  font-weight: 700;
  line-height: 1;
  color: var(--color-foreground);
  letter-spacing: -0.05em;
}

.drawer-head button {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
}

.drawer-head button::after {
  content: '';
  position: absolute;
  inset: -4px;
}

.drawer-body {
  flex: 1;
  padding: 12px;
}

.drawer-item {
  margin-bottom: 8px;
  overflow: hidden;
  background: #fff;
  border-radius: 3px;
}

.drawer-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.drawer-link {
  flex: 1;
  padding: 12px;
  font-size: 16px;
  font-weight: 600;
}

.drawer-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 38px;
  margin: 4px 8px;
  color: #333;
  background: #f7f7f7;
  border-radius: 3px;
}

.drawer-sub {
  padding: 0 12px 10px;
}

.drawer-sub a {
  display: block;
  padding: 9px 0 9px 10px;
  font-size: 14px;
  color: #666;
  border-top: 1px solid #f5f5f5;
}

.drawer-foot {
  display: flex;
  gap: 10px;
  flex: 0 0 auto;
  padding: 16px;
  border-top: 1px solid #f0f0f0;
}

.drawer-foot a {
  flex: 1;
  padding: 9px 8px;
  font-size: 12px;
  text-align: center;
  color: #fff;
  background: var(--accent);
  border-radius: 4px;
}

/* Mobile search overlay */
.search-overlay {
  position: fixed;
  inset: 0;
  z-index: 210;
  padding: 14px;
  background: rgba(0, 0, 0, 0.6);
}

.search-overlay-inner {
  padding: 10px;
  background: #fff;
  border-radius: 6px;
}

.overlay-search {
  display: flex;
  align-items: center;
  gap: 8px;
}

.overlay-search input {
  flex: 1;
  min-width: 0;
  height: 42px;
  padding: 0 14px;
  font-size: 14px;
  background: #f5f6f7;
  border: 0;
  border-radius: 40px;
  outline: none;
}

.overlay-submit {
  height: 42px;
  padding: 0 16px;
  font-size: 13px;
  color: #fff;
  background: var(--accent);
  border-radius: 40px;
}

.overlay-close {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  color: #666;
}

.overlay-close::after {
  content: '';
  position: absolute;
  inset: -4px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 1080px) {
  .main-nav > ul > li > a {
    padding: 0 8px;
    font-size: 13px;
  }

  .brand {
    margin-right: 16px;
  }
}

@media (max-width: 992px) {
  .header-shell {
    height: 85px;
    box-shadow: 0 2px 10px rgba(17, 58, 93, 0.05);
  }

  .header-shell.is-scrolled {
    transform: none;
  }

  .header-top {
    display: block;
    height: 43px;
    box-shadow: none;
  }

  .header-top-inner {
    height: 43px;
    padding: 0 16px;
    font-size: 15px;
  }

  .top-links a {
    padding: 0;
  }

  .top-search {
    display: none;
  }

  .mobile-top-search {
    display: flex;
    width: 32px;
    height: 32px;
  }

  .header-main {
    height: 42px;
    box-shadow: none;
  }

  .header-main-inner {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 42px;
    padding: 0 12px;
  }

  .menu-btn {
    position: absolute;
    top: 50%;
    left: 12px;
    display: block;
    width: 29px;
    height: 27px;
    padding: 7px 5px;
    margin: 0;
    color: #121212;
    background: rgba(246, 246, 246, 0.67);
    border-radius: 2px;
    transform: translateY(-50%);
  }

  .menu-btn::after {
    content: '';
    position: absolute;
    inset: -7px;
  }

  .menu-btn :deep(svg) {
    width: 19px;
    height: 13px;
  }

  .header-tools {
    display: none;
  }

  .main-nav {
    display: none;
  }

  .brand {
    margin: 0 auto;
    padding: 0;
  }

}
</style>

<style scoped>
/* UI UX Pro Max design system overrides */
.header-shell {
  background: var(--color-card);
  box-shadow: 0 14px 44px rgba(6, 78, 59, 0.1);
}

.header-top {
  height: 48px;
  background: var(--color-foreground);
}

.header-top-inner {
  height: 48px;
  color: #e7efe9;
}

.top-links {
  display: flex;
  align-items: center;
  gap: 20px;
}

.top-links a {
  padding: 0;
  color: #e7efe9;
  font-size: 13px;
}

.top-links a:hover {
  color: #ffffff;
}

.top-tagline {
  font-size: 12px;
  letter-spacing: 0.06em;
  color: #cbe3d6;
}

.top-search {
  width: 258px;
  height: 36px;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 10px;
}

.top-search input {
  padding: 0 8px 0 14px;
  color: #ffffff;
  font-size: 13px;
}

.top-search input::placeholder {
  color: rgba(255, 255, 255, 0.68);
}

.search-submit {
  color: #ffffff;
}

.header-shell.is-scrolled {
  transform: translateY(-48px);
}

.header-main {
  height: 76px;
  background: var(--color-card);
  border-bottom: 1px solid var(--color-border);
}

.header-main-inner {
  height: 76px;
}

.brand {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  gap: 2px;
  flex: 0 0 auto;
  margin-right: 26px;
  padding: 0;
}

.brand-mark {
  display: inline-flex;
  align-items: flex-start;
  gap: 4px;
  font-family: var(--font-heading);
  font-size: 26px;
  font-weight: 700;
  line-height: 1;
  color: var(--color-foreground);
  letter-spacing: -0.05em;
}

.brand-dot {
  width: 7px;
  height: 7px;
  background: var(--color-accent);
  border-radius: 50%;
}

.brand-en {
  font-family: var(--font-heading);
  font-size: 9px;
  font-weight: 600;
  letter-spacing: 0.28em;
  line-height: 1;
  color: var(--color-primary-strong);
}

.main-nav > ul {
  justify-content: flex-start;
}

.main-nav > ul > li > a {
  height: 75px;
  padding: 0 14px;
  color: var(--color-foreground);
  font-family: var(--font-heading);
  font-size: 15px;
  font-weight: 500;
  line-height: 75px;
}

.main-nav > ul > li > a::after {
  right: 14px;
  left: 14px;
  height: 4px;
  background: var(--color-primary);
  border-radius: 4px 4px 0 0;
}

.main-nav > ul > li:first-child > a::after {
  left: 0;
}

.main-nav > ul > li:hover > a,
.main-nav > ul > li:focus-within > a {
  color: var(--color-primary-strong);
}

.main-nav > ul > li > a :deep(svg) {
  color: var(--color-primary);
}

.submenu {
  padding: 8px;
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 14px;
  box-shadow: var(--shadow-card);
}

.submenu li > a {
  padding: 11px 16px;
  color: var(--color-foreground);
  font-family: var(--font-body);
  font-size: 14px;
  border-radius: 8px;
}

.submenu li > a:hover {
  color: var(--color-primary);
  background: var(--color-muted);
}

.header-cta {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  flex: 0 0 auto;
  height: 44px;
  padding: 0 20px;
  margin-left: 18px;
  color: var(--color-on-accent);
  font-family: var(--font-heading);
  font-size: 14px;
  font-weight: 600;
  background: var(--color-accent);
  border-radius: 12px;
  box-shadow: 0 12px 24px rgba(234, 88, 12, 0.24);
  transition: transform 0.22s ease, background 0.22s ease, box-shadow 0.22s ease;
}

.header-cta:hover {
  color: var(--color-on-accent);
  background: #f97316;
  transform: translateY(-2px);
  box-shadow: 0 16px 30px rgba(234, 88, 12, 0.3);
}

.header-tools button {
  color: var(--color-foreground);
}

.drawer {
  background: var(--color-background);
  border-right: 1px solid var(--color-border);
}

.drawer-head {
  height: 72px;
  background: var(--color-card);
  border-bottom: 1px solid var(--color-border);
}

.drawer-head button {
  color: var(--color-foreground);
}

.drawer-body {
  padding: 16px;
}

.drawer-item {
  margin-bottom: 10px;
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 14px;
}

.drawer-link {
  padding: 14px 16px;
  color: var(--color-foreground);
  font-family: var(--font-heading);
  font-size: 16px;
}

.drawer-toggle {
  color: var(--color-primary);
  background: var(--color-muted);
  border-radius: 9px;
}

.drawer-sub {
  padding: 0 16px 12px;
}

.drawer-sub a {
  padding: 10px 0 10px 12px;
  color: var(--color-muted-foreground);
  border-top-color: var(--color-muted);
}

.drawer-sub a:hover {
  color: var(--color-primary);
}

.drawer-foot {
  flex-wrap: wrap;
  padding: 18px 16px;
  background: var(--color-card);
  border-top: 1px solid var(--color-border);
}

.drawer-foot a {
  flex: 1 0 100%;
  padding: 12px 10px;
  color: var(--color-on-accent);
  font-family: var(--font-heading);
  font-weight: 600;
  background: var(--color-accent);
  border-radius: 10px;
}

.drawer-qq {
  width: 100%;
  padding: 2px 0;
  font-size: 12px;
  text-align: center;
  color: var(--color-primary-strong);
  user-select: all;
}

.search-overlay-inner {
  padding: 14px;
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 18px;
  box-shadow: var(--shadow-hover);
}

.overlay-search input {
  background: var(--color-muted);
  color: var(--color-foreground);
  border-radius: 12px;
}

.overlay-submit {
  color: var(--color-on-accent);
  background: var(--color-accent);
  border-radius: 12px;
}

.overlay-close {
  color: var(--color-foreground);
}

@media (max-width: 1200px) and (min-width: 993px) {
  .brand {
    margin-right: 14px;
  }

.main-nav > ul > li > a {
    padding: 0 9px;
    font-size: 14px;
  }

  .main-nav > ul > li > a::after {
    right: 9px;
    left: 9px;
  }

  .header-cta {
    padding: 0 14px;
    margin-left: 10px;
  }
}

@media (max-width: 992px) {
  .header-shell {
    height: 102px;
  }

  .header-top {
    height: 44px;
  }

  .header-top-inner {
    height: 44px;
    padding: 0 16px;
  }

  .top-tagline {
    display: none;
  }

  .top-links a {
    color: #e7efe9;
    font-size: 14px;
  }

  .mobile-top-search {
    color: #ffffff;
  }

  .header-main,
  .header-main-inner {
    height: 58px;
  }

  .main-nav {
    display: none;
  }

  .header-cta {
    display: none;
  }

  .menu-btn {
    width: 32px;
    height: 32px;
    padding: 7px;
    color: var(--color-foreground);
    background: var(--color-muted);
    border-radius: 9px;
  }

  .brand {
    margin: 0 auto;
    align-items: center;
  }

  .brand-mark {
    font-size: 22px;
  }

  .brand-en {
    font-size: 8px;
  }

  .header-tools {
    display: none;
  }
}
</style>
