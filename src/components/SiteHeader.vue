<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { site } from '@/data'
import AppIcon from '@/components/AppIcon.vue'
import { useCart } from '@/stores/cart'
import { asset, formatPrice } from '@/utils'

const route = useRoute()
const router = useRouter()
const { count, subtotal } = useCart()

const keyword = ref('')
const drawerOpen = ref(false)
const scrolled = ref(false)
const searchInput = ref(null)

function focusSearch() {
  if (route.path === '/' && searchInput.value) {
    searchInput.value.focus()
    return
  }
  router.push('/search')
}

const categories = computed(() =>
  Object.entries(site.categories)
    .filter(([id, item]) => !item.parent && id !== 'hot' && id !== 'contact' && item.section)
    .sort((a, b) => (a[1].sort ?? 999) - (b[1].sort ?? 999))
    .map(([id, item]) => ({ id, title: item.title }))
)

const drawerOrder = ['disposables', 'jimu', 'pods', 'gbxl', 'recommend', 'combo', 'wanghong', 'shisha']
const drawerCategories = computed(() =>
  drawerOrder
    .map((id) => site.categories[id] && { id, title: site.categories[id].title })
    .filter(Boolean)
    .map((item) => ({
      ...item,
      label: ['combo', 'wanghong', 'recommend'].includes(item.id)
        ? `${item.title} 🔥`
        : item.title
    }))
)

const drawerGroups = ref({ electronic: false, brand: false, about: false })

function toggleDrawerGroup(name) {
  drawerGroups.value[name] = !drawerGroups.value[name]
}

function submitDrawerSearch() {
  const value = keyword.value.trim()
  if (!value) return
  router.push({ path: '/search', query: { q: value } })
  drawerOpen.value = false
}

const brands = computed(() => site.brands || [])
const aboutLinks = [
  { label: '关于我们', to: '/info/about' },
  { label: '常见问题', to: '/info/faq' },
  { label: '付款方式', to: '/info/payment' },
  { label: '配送说明', to: '/info/delivery' },
  { label: '退换政策', to: '/info/returns' },
  { label: '真假验证', to: '/info/verification' },
  { label: '隐私政策', to: '/info/privacy' }
]

const navItems = [
  { label: '首页', to: '/' },
  { label: '电子雾化', to: '/category/disposables', mega: true },
  { label: '关于我们', to: '/info/about' },
  { label: '联系客服', to: '/contact' }
]

function submitSearch() {
  const value = keyword.value.trim()
  if (!value) return
  router.push({ path: '/search', query: { q: value } })
}

function onScroll() {
  scrolled.value = window.scrollY > 4
}

function onKeydown(event) {
  if (event.key === 'Escape') {
    drawerOpen.value = false
  }
}

watch(
  () => route.fullPath,
  () => {
    drawerOpen.value = false
  }
)

watch(drawerOpen, (open) => {
  document.body.style.overflow = open ? 'hidden' : ''
})

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
  <div class="header-wrap">
    <div class="announce">
      <div class="announce-marquee">
        <span>{{ site.announcement }}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{{ site.announcementRight }}</span>
      </div>
    </div>

    <header class="site-header" :class="{ 'is-scrolled': scrolled }">
      <div class="wrapper header-main">
        <button class="mobile-menu-btn" type="button" aria-label="打开菜单" @click="drawerOpen = true">
          <AppIcon name="menu" :size="24" />
        </button>

        <nav class="desktop-nav" aria-label="主导航">
          <button class="search-icon" type="button" aria-label="搜索" @click="focusSearch">
            <AppIcon name="search" :size="18" />
          </button>
          <ul>
            <li v-for="item in navItems" :key="item.label" :class="{ 'has-mega': item.mega }">
              <RouterLink :to="item.to">
                {{ item.label }}
                <AppIcon v-if="item.mega" name="chevron-down" :size="12" />
              </RouterLink>

              <div v-if="item.mega" class="mega">
                <div class="mega-col">
                  <b>系列</b>
                  <RouterLink v-for="category in categories" :key="category.id" :to="`/category/${category.id}`">
                    {{ category.title }}
                  </RouterLink>
                </div>
                <div class="mega-col mega-brands">
                  <b>品牌</b>
                  <div class="mega-brand-grid">
                    <RouterLink
                      v-for="brand in brands"
                      :key="brand"
                      :to="`/search?q=${encodeURIComponent(brand.split(' ').pop())}`"
                    >
                      {{ brand }}
                    </RouterLink>
                  </div>
                </div>
                <div class="mega-links">
                  <RouterLink v-if="site.categories.recommend" to="/category/recommend">店长推荐 🔥</RouterLink>
                </div>
                <RouterLink class="mega-all" to="/category/hot">查看全部商品 →</RouterLink>
              </div>
            </li>
          </ul>
        </nav>

        <RouterLink class="logo" to="/" aria-label="泡泡哥雾化首页">
          <img class="logo-img" :src="asset('/images/ui/logo-vapepu.webp')" alt="VAPEPU" />
        </RouterLink>

        <RouterLink class="cart-pill" to="/cart" aria-label="购物车">
          <span class="cart-pill-text">购物车 / {{ formatPrice(subtotal) }}</span>
          <AppIcon name="cart" :size="18" />
          <span v-if="count" class="cart-badge">{{ count }}</span>
        </RouterLink>

        <RouterLink class="mobile-cart" to="/cart" aria-label="购物车">
          <AppIcon name="cart" :size="18" />
          <span v-if="count" class="cart-badge">{{ count }}</span>
        </RouterLink>
      </div>
    </header>

    <Teleport to="body">
      <Transition name="fade">
        <div v-if="drawerOpen" class="drawer-mask" @click="drawerOpen = false" />
      </Transition>
      <aside class="drawer" :class="{ open: drawerOpen }" role="dialog" aria-modal="true" aria-label="移动端菜单">
        <div class="drawer-top">
          <form class="drawer-search" @submit.prevent="submitDrawerSearch">
            <input v-model="keyword" type="search" placeholder="搜索..." aria-label="搜索" />
            <button type="submit" aria-label="搜索">
              <AppIcon name="search" :size="18" />
            </button>
          </form>
        </div>

        <div class="drawer-body">
          <RouterLink class="drawer-link" to="/" @click="drawerOpen = false">首页</RouterLink>

          <div class="drawer-group">
            <button class="drawer-group-toggle" type="button" @click="toggleDrawerGroup('electronic')">
              <span>电子雾化</span>
              <span class="drawer-chevron" :class="{ open: drawerGroups.electronic }">
                <AppIcon name="chevron-down" :size="16" />
              </span>
            </button>
            <div v-if="drawerGroups.electronic" class="drawer-sub">
              <RouterLink
                v-for="item in drawerCategories"
                :key="item.id"
                :to="`/category/${item.id}`"
                @click="drawerOpen = false"
              >
                {{ item.label }}
              </RouterLink>
            </div>
          </div>

          <div class="drawer-group">
            <button class="drawer-group-toggle" type="button" @click="toggleDrawerGroup('brand')">
              <span>品牌分类</span>
              <span class="drawer-chevron" :class="{ open: drawerGroups.brand }">
                <AppIcon name="chevron-down" :size="16" />
              </span>
            </button>
            <div v-if="drawerGroups.brand" class="drawer-sub">
              <RouterLink
                v-for="brand in brands"
                :key="brand"
                :to="`/search?q=${encodeURIComponent(brand.split(' ').pop())}`"
                @click="drawerOpen = false"
              >
                {{ brand }}
              </RouterLink>
            </div>
          </div>

          <div class="drawer-group">
            <button class="drawer-group-toggle" type="button" @click="toggleDrawerGroup('about')">
              <span>关于我们</span>
              <span class="drawer-chevron" :class="{ open: drawerGroups.about }">
                <AppIcon name="chevron-down" :size="16" />
              </span>
            </button>
            <div v-if="drawerGroups.about" class="drawer-sub">
              <RouterLink
                v-for="item in aboutLinks"
                :key="item.to"
                :to="item.to"
                @click="drawerOpen = false"
              >
                {{ item.label }}
              </RouterLink>
            </div>
          </div>

          <RouterLink class="drawer-link" to="/contact" @click="drawerOpen = false">联系客服</RouterLink>
        </div>
      </aside>
    </Teleport>
  </div>
</template>

<style scoped>
.announce {
  overflow: hidden;
  padding: 10px 0;
  font-size: 14px;
  line-height: 1.6;
  color: #ffffff;
  text-align: center;
  background: #1d2327;
}

.announce-marquee {
  overflow: hidden;
  white-space: nowrap;
}

.announce-marquee span {
  display: inline-block;
  padding-left: 100%;
  white-space: nowrap;
  animation: annoscno-scroll 20s linear infinite;
}

.announce:hover .announce-marquee span {
  animation-play-state: paused;
}

@keyframes annoscno-scroll {
  from {
    transform: translateX(0);
  }
  to {
    transform: translateX(-100%);
  }
}

.site-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: #ffffff;
  transition: box-shadow 0.2s ease;
}

.site-header.is-scrolled {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
}

.header-main {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100px;
  padding: 0 15px;
}

.desktop-nav {
  display: flex;
  align-items: center;
  gap: 18px;
}

.search-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  color: var(--color-foreground);
}

.desktop-nav > ul {
  display: flex;
  align-items: center;
  gap: 26px;
}

.desktop-nav > ul > li {
  position: relative;
  display: flex;
  align-items: center;
  height: 100px;
}

.desktop-nav > ul > li > a {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  font-weight: 700;
  color: #666666;
  transition: color 0.18s ease;
}

.desktop-nav > ul > li > a:hover,
.desktop-nav > ul > li:hover > a {
  color: var(--color-primary);
}

.logo {
  position: absolute;
  left: 50%;
  top: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  transform: translate(-50%, -50%);
  white-space: nowrap;
}

.logo-cn {
  display: inline-flex;
  align-items: flex-start;
  gap: 3px;
  font-family: var(--font-heading);
  font-size: 28px;
  font-weight: 900;
  line-height: 1;
  letter-spacing: -0.07em;
  color: #242125;
}

.logo-img {
  display: block;
  width: auto;
  height: 26px;
}

.logo-dot {
  width: 7px;
  height: 7px;
  margin-top: 2px;
  background: var(--color-primary);
  border-radius: 50%;
}

.logo-en {
  font-family: var(--font-heading);
  font-size: 8px;
  font-weight: 700;
  letter-spacing: 0.42em;
  color: #999999;
}

.cart-pill {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  height: 32px;
  padding: 0 12px;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.03em;
  color: #000000;
  border: 1px solid #000000;
  border-radius: 999px;
  text-transform: uppercase;
  transition: border-color 0.18s ease, color 0.18s ease;
}

.cart-pill:hover {
  color: var(--color-primary);
  border-color: var(--color-primary);
}

.cart-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 17px;
  height: 17px;
  padding: 0 4px;
  font-size: 10px;
  color: #ffffff;
  background: var(--color-primary);
  border-radius: 999px;
}

.search-row {
  padding: 0 16px 14px;
}

.header-search {
  position: relative;
  display: flex;
  align-items: center;
  height: 40px;
  overflow: hidden;
  border: 1px solid #e5e5e5;
  border-radius: 3px;
  background: #f5f5f5;
  transform: skewX(-8deg);
}

.header-search input,
.header-search button {
  transform: skewX(8deg);
}

.header-search input {
  flex: 1;
  min-width: 0;
  height: 100%;
  padding: 0 14px;
  font-size: 13px;
  background: transparent;
  border: 0;
  outline: none;
}

.header-search input::placeholder {
  color: #aaaaaa;
}

.header-search button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 46px;
  height: 100%;
  color: #555555;
}

.mega {
  position: absolute;
  top: 100%;
  left: -120px;
  z-index: 30;
  display: grid;
  grid-template-columns: 180px 1fr;
  gap: 26px;
  width: 640px;
  padding: 24px;
  background: #ffffff;
  border: 1px solid #eeeeee;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.12);
  opacity: 0;
  visibility: hidden;
  transform: translateY(8px);
  transition: opacity 0.18s ease, transform 0.18s ease, visibility 0.18s;
}

.has-mega:hover .mega,
.has-mega:focus-within .mega {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.mega-col {
  display: flex;
  flex-direction: column;
  gap: 9px;
}

.mega-col b {
  padding-bottom: 8px;
  margin-bottom: 2px;
  font-size: 11px;
  letter-spacing: 0.12em;
  color: #999999;
  border-bottom: 1px solid #eeeeee;
}

.mega-col a {
  font-size: 13px;
  color: #444444;
}

.mega-col a:hover {
  color: var(--color-primary);
}

.mega-brand-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px 18px;
}

.mega-all {
  grid-column: 1 / -1;
  padding-top: 12px;
  font-size: 12px;
  font-weight: 700;
  color: var(--color-primary);
  border-top: 1px solid #eeeeee;
}

.mega-links {
  grid-column: 1 / -1;
  display: flex;
  flex-wrap: wrap;
  gap: 10px 22px;
  padding-top: 10px;
  margin-top: 4px;
  font-size: 12px;
  border-top: 1px solid #eeeeee;
}

.mega-links a {
  color: #666666;
}

.mega-links a:hover {
  color: var(--color-primary);
}

.mobile-menu-btn,
.mobile-cart {
  display: none;
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
  width: 300px;
  max-width: 84vw;
  background: #f7f7f7;
  transform: translateX(-101%);
  transition: transform 0.25s ease;
  overflow-y: auto;
}

.drawer.open {
  transform: translateX(0);
}

.drawer-body {
  padding: 0 0 16px;
}

.drawer-top {
  flex: 0 0 auto;
  padding: 12px 15px;
  background: #f7f7f7;
  border-bottom: 1px solid #eeeeee;
}

.drawer-search {
  display: flex;
  height: 40px;
  overflow: hidden;
  background: #ffffff;
  border: 1px solid #dddddd;
}

.drawer-search input {
  flex: 1;
  min-width: 0;
  padding: 0 12px;
  font-size: 16px;
  color: #333333;
  border: 0;
  outline: none;
}

.drawer-search input::placeholder {
  color: #999999;
}

.drawer-search button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  color: #222222;
  background: #e9e9e9;
  border-left: 1px solid #dddddd;
}

.drawer-group {
  margin: 0;
}

.drawer-link,
.drawer-group-toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 18px 20px;
  font-size: 16px;
  font-weight: 600;
  color: #242125;
  text-align: left;
  background: #ffffff;
  border-bottom: 1px solid #f0f0f0;
}

.drawer-link {
  display: block;
}

.drawer-chevron {
  display: flex;
  align-items: center;
  justify-content: center;
  color: #777777;
  transition: transform 0.2s ease;
}

.drawer-chevron.open {
  transform: rotate(180deg);
}

.drawer-sub {
  display: flex;
  flex-direction: column;
  padding: 2px 20px 10px;
  background: #fafafa;
}

.drawer-sub a {
  padding: 9px 0 9px 12px;
  font-size: 14px;
  color: #555555;
}

.drawer-sub a:hover {
  color: var(--color-primary);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 900px) {
  .site-header {
    background-color: #ffffff;
    background-image: url('../assets/images/header-bg.webp');
    background-repeat: no-repeat;
    background-position: 50% 50%;
    background-size: cover;
    border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  }

  .header-main {
    height: 70px;
    padding: 0 15px;
  }

  .desktop-nav,
  .cart-pill {
    display: none;
  }

  .mobile-menu-btn,
  .mobile-cart {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    color: #000000;
  }

  .mobile-menu-btn {
    width: 24px;
    height: 32px;
  }

  .mobile-cart {
    position: relative;
    border: 1px solid #000000;
    border-radius: 999px;
  }

  .mobile-cart .cart-badge {
    position: absolute;
    top: -6px;
    right: -6px;
    min-width: 17px;
    height: 17px;
    padding: 0 4px;
    font-size: 10px;
    color: #ffffff;
    background: #000000;
  }

  .logo-img {
    height: 26px;
  }

  .logo-cn {
    font-size: 22px;
  }

  .logo-en {
    font-size: 7px;
    letter-spacing: 0.3em;
  }
}

@media (min-width: 550px) and (max-width: 900px) {
  .header-main {
    height: 100px;
  }
}
</style>
