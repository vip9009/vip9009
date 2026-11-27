<script setup>
import { computed, ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { site, productsData } from '@/data'
import VpProductCard from '@/components/VpProductCard.vue'
import LottieBox from '@/components/LottieBox.vue'
import AppIcon from '@/components/AppIcon.vue'
import { asset } from '@/utils'
import newDividerImg from '@/assets/images/new-divider.png'
import arrowDownImg from '@/assets/images/arrow-down.png'
import noSmokingDividerImg from '@/assets/images/no-smoking-divider.png'

const router = useRouter()
const activeTab = ref('tag')
const page = ref(0)
const pageSize = 3
const pageCount = 9
const homeKeyword = ref('')

function submitHomeSearch() {
  const value = homeKeyword.value.trim()
  if (!value) return
  router.push({ path: '/search', query: { q: value } })
}

function circledNumber(value) {
  if (value >= 1 && value <= 20) return String.fromCodePoint(0x2460 + value - 1)
  if (value >= 21 && value <= 35) return String.fromCodePoint(0x3251 + value - 21)
  return String(value)
}

function pageLabel(index) {
  return circledNumber((pageCount - index) * pageSize)
}

const hero = computed(() => site.hero || {})

const allProducts = computed(() => {
  const seen = new Set()
  const list = []
  productsData.sections
    .filter((section) => section.id !== 'hot')
    .forEach((section) => {
      ;(section.products || []).forEach((product, index) => {
        const key = product.sourceId || product.title
        if (seen.has(key)) return
        seen.add(key)
        list.push({
          ...product,
          sectionId: section.id,
          sectionTitle: section.title,
          index
        })
      })
    })
  return list
})

const tiles = computed(() => {
  const order = ['disposables', 'pods', 'jimu', 'gbxl', 'shisha', 'wanghong', 'combo']
  const fromCategories = order
    .map((id) => {
      const item = site.categories[id]
      if (!item) return null
      return {
        title: item.title,
        to: `/category/${id}`,
        image: `/images/categories/${id}.webp`,
        lottie: ''
      }
    })
    .filter(Boolean)
  return [
    ...fromCategories,
    { title: '优惠活动', to: '/activity', image: '', lottie: '/animations/rocket.json' }
  ]
})

const newProducts = computed(() => {
  const score = (product) => {
    const badges = product.badges || []
    if (badges.includes('上新')) return 0
    if (badges.includes('上新口味')) return 1
    if (product.hot) return 2
    return 3
  }
  return [...allProducts.value]
    .sort((a, b) => score(a) - score(b))
    .slice(0, pageCount * pageSize)
})
const visibleProducts = computed(() =>
  newProducts.value.slice(page.value * pageSize, (page.value + 1) * pageSize)
)

const tags = computed(() => site.tags || [])
const tagRows = computed(() => {
  const list = tags.value
  return [list.slice(0, 5), list.slice(5, 9), list.slice(9, 13), list.slice(13)]
})
const TAG_COLORS = {
  HOT: '#000000',
  上新: '#ff0077',
  上新口味: '#ff0077',
  模式切换: '#00f2f2',
  凉度调节: '#45f7d6',
  自定义口感: '#00efc7',
  强击喉: '#0a0002',
  FREE: '#ff0077',
  'SMART VAPE': '#ce2cd3',
  KOREA: '#8224e3',
  'MINI GAME': '#4423ea',
  呼吸灯: '#b4f230',
  极致顺滑: '#0a0103',
  口味切换: '#ff7c7c',
  'NIC1-2%': '#c5ff33',
  免充电: '#09ed77',
  适配悦刻: '#8e8e8e',
  烟杆: '#8e8e8e'
}
const TAG_LIGHT_TEXT = new Set(['HOT', '强击喉', '极致顺滑'])

function tagStyle(label) {
  return {
    background: TAG_COLORS[label] || '#0a0002',
    color: TAG_LIGHT_TEXT.has(label) ? '#ffffff' : '#000000'
  }
}
const brands = computed(() => site.brands || [])
const brandItems = computed(() =>
  brands.value.map((name) => ({ name, logo: site.brandLogos?.[name] || '' }))
)
const news = computed(() => site.news || [])
const newsPage = ref(0)
const newsPerPage = 2
const newsPages = computed(() => Math.max(1, Math.ceil(news.value.length / newsPerPage)))
const visibleNews = computed(() =>
  news.value.slice(newsPage.value * newsPerPage, (newsPage.value + 1) * newsPerPage)
)

function prevNews() {
  newsPage.value = (newsPage.value - 1 + newsPages.value) % newsPages.value
}

function nextNews() {
  newsPage.value = (newsPage.value + 1) % newsPages.value
}

function setPage(index) {
  page.value = index
}
</script>

<template>
  <div class="home-page">
    <div class="wrapper home-search">
      <form class="home-search-form" role="search" @submit.prevent="submitHomeSearch">
        <input v-model="homeKeyword" type="search" placeholder="搜索..." aria-label="搜索产品" />
        <button type="submit" aria-label="搜索">
          <AppIcon name="search" :size="22" />
        </button>
      </form>
    </div>

    <div class="wrapper home-top">
      <RouterLink class="hero-banner hero-lottie" :to="hero.link || '/info/about'">
        <LottieBox src="/animations/faq.json" label="常见问题 FAQ 动画" />
      </RouterLink>
    </div>

    <section class="category-section">
      <div class="wrapper">
        <div class="category-tiles">
          <RouterLink
            v-for="tile in tiles"
            :key="tile.title"
            class="category-tile"
            :to="tile.to"
          >
            <span class="category-glyph" :class="{ 'is-lottie': tile.lottie }">
              <LottieBox v-if="tile.lottie" :src="tile.lottie" label="优惠活动动画" />
              <img v-else :src="asset(tile.image)" :alt="tile.title" />
            </span>
          </RouterLink>
        </div>
      </div>
    </section>

    <section class="new-section">
      <div class="wrapper">
        <div class="new-head">
          <img class="new-divider-img" :src="newDividerImg" alt="NEW 上新专区" />
          <img class="new-arrow-down" :src="arrowDownImg" alt="" aria-hidden="true" />
        </div>

        <div v-if="newProducts.length" class="page-tabs">
          <button
            v-for="index in pageCount"
            :key="index"
            type="button"
            class="page-tab"
            :class="{ active: page === index - 1 }"
            @click="setPage(index - 1)"
          >
            {{ pageLabel(index - 1) }}
          </button>
        </div>

        <div v-if="visibleProducts.length" :key="page" class="product-grid-3 page-slide">
          <VpProductCard
            v-for="(product, index) in visibleProducts"
            :key="`${product.sectionId}-${product.index}`"
            :product="product"
            :section-id="product.sectionId"
            :section-title="product.sectionTitle"
            :index="product.index"
            :eager="index < 3"
          />
        </div>

        <div v-else class="empty-new">
          <b>本周上新更新中</b>
          <p>加泡泡哥微信，先看最新到货、口味和价格。</p>
          <RouterLink class="empty-cta" to="/contact">加微信</RouterLink>
        </div>
      </div>
    </section>

    <section class="tag-section">
      <div class="wrapper">
        <div class="tag-bar">
          <button type="button" :class="{ active: activeTab === 'tag' }" @click="activeTab = 'tag'">TAG</button>
          <button type="button" :class="{ active: activeTab === 'brand' }" @click="activeTab = 'brand'">BRAND</button>
          <button type="button" :class="{ active: activeTab === 'news' }" @click="activeTab = 'news'">NEWS</button>
        </div>

        <img class="tag-arrow-down" :src="arrowDownImg" alt="" aria-hidden="true" />

        <div v-if="activeTab === 'tag'" class="tag-cloud">
          <div v-for="(row, rowIndex) in tagRows" :key="rowIndex" class="tag-row">
            <RouterLink
              v-for="tag in row"
              :key="tag.label"
              class="tag-pill"
              :class="`tone-${tag.tone}`"
              :style="tagStyle(tag.label)"
              :to="`/search?q=${encodeURIComponent(tag.label)}`"
            >
              {{ tag.label }}
            </RouterLink>
          </div>
        </div>

        <div v-else-if="activeTab === 'brand'" class="brand-wall">
          <RouterLink
            v-for="item in brandItems"
            :key="item.name"
            class="brand-word"
            :to="`/search?q=${encodeURIComponent(item.name.split(' ').pop())}`"
          >
            <img v-if="item.logo" :src="asset(item.logo)" :alt="item.name" />
            <span v-else>{{ item.name }}</span>
          </RouterLink>
        </div>

        <div v-else class="news-carousel">
          <button class="news-arrow prev" type="button" aria-label="上一组新闻" @click="prevNews">‹</button>
          <div class="news-track">
            <RouterLink v-for="item in visibleNews" :key="item.title" class="news-card" :to="item.to || '/info/news'">
              <span class="news-thumb">
                <img v-if="item.image" :src="asset(item.image)" :alt="item.title" />
                <template v-else>
                  <b>PAOPAO</b>
                  <small>NEWS</small>
                </template>
              </span>
              <h3>{{ item.title }}</h3>
              <div class="news-meta">
                <time>{{ item.date }}</time>
                <span v-if="item.comments">{{ item.comments }} 评论</span>
              </div>
            </RouterLink>
          </div>
          <button class="news-arrow next" type="button" aria-label="下一组新闻" @click="nextNews">›</button>
        </div>
        <div v-if="activeTab === 'news' && newsPages > 1" class="news-dots">
          <button
            v-for="index in newsPages"
            :key="index"
            type="button"
            :class="{ active: newsPage === index - 1 }"
            :aria-label="`第 ${index} 页新闻`"
            @click="newsPage = index - 1"
          />
        </div>
      </div>
    </section>

    <div class="wrapper no-smoking">
      <img class="no-smoking-divider" :src="noSmokingDividerImg" alt="" aria-hidden="true" />
      <div class="no-smoking-lottie">
        <LottieBox src="/animations/no-smoking-ref.json" fit="contain" :speed="0.5" label="NO SMOKING 动画" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-page {
  background: #ffffff;
}

.home-search {
  padding-top: 11px;
}

.home-search-form {
  display: flex;
  align-items: center;
  height: 40px;
  overflow: hidden;
  background: rgba(0, 0, 0, 0.03);
  border: 1px solid rgba(0, 0, 0, 0.09);
  border-radius: 99px;
  box-shadow: none;
}

.home-search-form input {
  flex: 1;
  min-width: 0;
  height: 100%;
  padding: 0 12px;
  font-size: 16px;
  color: #777777;
  background: transparent;
  border: 0;
  outline: none;
}

.home-search-form input::placeholder {
  color: #999999;
}

.home-search-form button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 100%;
  color: #777777;
  background: transparent;
}

.home-top {
  padding-top: 15px;
}

.hero-banner {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 336px;
  padding: 0 58px;
  overflow: hidden;
  color: #ffffff;
  background:
    radial-gradient(circle at 78% 20%, rgba(230, 0, 126, 0.95) 0, rgba(230, 0, 126, 0.4) 22%, transparent 48%),
    linear-gradient(115deg, #111111 0%, #1b0b15 55%, #2a0a1c 100%);
  border-radius: 4px;
}

.hero-banner::before {
  content: '';
  position: absolute;
  inset: 14px;
  border: 1px dashed rgba(255, 255, 255, 0.18);
  border-radius: 2px;
  pointer-events: none;
}

.hero-banner.hero-lottie {
  display: block;
  height: auto;
  aspect-ratio: 750 / 227;
  padding: 0;
  background: #000000;
  border-radius: 10px;
  box-shadow: 0 1px 3px -2px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
}

.hero-banner.hero-lottie::before {
  display: none;
}

.hero-lottie .lottie-box {
  width: 100%;
  height: 100%;
}

.hero-copy {
  position: relative;
  z-index: 2;
  max-width: 520px;
}

.hero-eyebrow {
  display: inline-block;
  margin-bottom: 12px;
  font-family: var(--font-heading);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.24em;
  color: #ff77bb;
}

.hero-copy h1 {
  margin-bottom: 12px;
  font-size: clamp(38px, 4.4vw, 58px);
  font-weight: 900;
  line-height: 1.04;
  letter-spacing: -0.04em;
  color: #ffffff;
}

.hero-copy p {
  max-width: 460px;
  margin-bottom: 18px;
  font-size: 14px;
  line-height: 1.7;
  color: rgba(255, 255, 255, 0.72);
}

.hero-cta {
  display: inline-flex;
  align-items: center;
  height: 42px;
  padding: 0 20px;
  font-size: 13px;
  font-weight: 700;
  color: #ffffff;
  background: var(--color-primary);
}

.hero-copy small {
  display: block;
  margin-top: 14px;
  font-size: 11px;
  letter-spacing: 0.08em;
  color: rgba(255, 255, 255, 0.5);
}

.hero-products {
  position: relative;
  z-index: 2;
  width: 380px;
  height: 270px;
}

.hero-product {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 150px;
  height: 190px;
  padding: 8px;
  background: #ffffff;
  border-radius: 2px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.35);
}

.hero-product img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.hero-product-1 {
  top: 34px;
  left: 0;
  transform: rotate(-5deg);
}

.hero-product-2 {
  top: 0;
  left: 118px;
  transform: rotate(3deg);
}

.hero-product-3 {
  top: 74px;
  left: 238px;
  transform: rotate(8deg);
}

.hero-wordmark {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #ffffff;
  transform: rotate(-4deg);
}

.hero-wordmark b {
  font-family: var(--font-heading);
  font-size: 64px;
  font-weight: 900;
  letter-spacing: -0.06em;
  line-height: 1;
}

.hero-wordmark span {
  font-size: 11px;
  letter-spacing: 0.5em;
  color: #ff77bb;
}

.category-section {
  padding: 15px 0 0;
}

.category-tiles {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  column-gap: 20px;
  row-gap: 7px;
}

.category-tile {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #242125;
  transition: color 0.18s ease;
}

.category-tile:hover {
  color: var(--color-primary);
}

.category-glyph {
  width: 100%;
  height: auto;
  aspect-ratio: 1;
  transition: transform 0.25s ease;
}

.category-glyph img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.category-tile:hover .category-glyph {
  transform: translateY(-4px) scale(1.04);
}

.category-glyph.is-lottie {
  width: 100%;
  height: auto;
  aspect-ratio: 1;
}

.category-tile b {
  font-size: 21px;
  font-weight: 700;
  letter-spacing: 0.02em;
}

.category-tile.accent b {
  color: var(--color-primary);
}

.new-section {
  padding-top: 20px;
}

.new-head {
  text-align: center;
}

.new-divider-img {
  display: block;
  width: 100%;
  height: auto;
}

.new-arrow-down {
  display: block;
  width: 14.4px;
  height: 12.8px;
  margin: 7px auto 0;
}

.page-tabs {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 0;
  margin-top: 1px;
  margin-bottom: 16px;
}

.page-tab {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 33.2px;
  height: 32px;
  padding: 0 9.6px;
  font-size: 12.8px;
  color: rgba(102, 102, 102, 0.85);
  border: 0;
  border-radius: 99px;
  transition: color 0.16s ease, background 0.16s ease;
}

.page-tab:hover {
  color: var(--color-primary);
}

.page-tab.active {
  color: #ffffff;
  background: #242125;
}

.product-grid-3 {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0;
}

.page-slide {
  animation: page-slide 0.38s cubic-bezier(0.22, 0.61, 0.36, 1) both;
}

@keyframes page-slide {
  from {
    opacity: 0;
    transform: translateX(22px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.empty-new {
  padding: 54px 20px;
  text-align: center;
  background: #fafafa;
  border: 1px solid #eeeeee;
}

.empty-new b {
  display: block;
  margin-bottom: 6px;
  font-size: 18px;
}

.empty-new p {
  margin-bottom: 16px;
  font-size: 13px;
  color: #888888;
}

.empty-cta {
  display: inline-flex;
  align-items: center;
  height: 38px;
  padding: 0 18px;
  font-size: 12px;
  font-weight: 700;
  color: #ffffff;
  background: var(--color-primary);
}

.tag-section {
  padding: 8px 0 36px;
}

.tag-bar {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 64px;
  max-width: 1050px;
  height: 37px;
  margin: 0 auto;
  overflow: hidden;
  background: #111111;
}

.tag-bar::before,
.tag-bar::after {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  width: 44px;
  background: repeating-linear-gradient(115deg, #111111 0 7px, #ffffff 7px 14px);
}

.tag-bar::before {
  left: 0;
  clip-path: polygon(0 0, 100% 0, 65% 100%, 0 100%);
}

.tag-bar::after {
  right: 0;
  clip-path: polygon(35% 0, 100% 0, 100% 100%, 0 100%);
}

.tag-bar button {
  position: relative;
  z-index: 1;
}

.tag-bar button {
  font-family: var(--font-heading);
  font-size: 11px;
  font-weight: 900;
  letter-spacing: 0.08em;
  color: #777777;
  transition: color 0.18s ease;
}

.tag-bar button.active,
.tag-bar button:hover {
  color: #ffffff;
}

.tag-arrow-down {
  display: block;
  width: 14.4px;
  height: 12.8px;
  margin: 4px auto 0;
}

.tag-cloud {
  display: flex;
  flex-direction: column;
  gap: 5px;
  max-width: 760px;
  padding: 14px 0 0;
  margin: 0 auto;
}

.tag-row {
  display: flex;
  flex-wrap: nowrap;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.tag-pill {
  display: inline-flex;
  align-items: center;
  height: 27.5px;
  padding: 0 8px;
  font-size: 11px;
  font-weight: 400;
  color: #000000;
  border-radius: 5px;
}

.tone-pink { background: #e6007e; }
.tone-black { background: #111111; }
.tone-cyan { background: #16c8d6; color: #083a3e; }
.tone-green { background: #14c98e; color: #063b2a; }
.tone-purple { background: #7500c0; }
.tone-blue { background: #3a37ff; }
.tone-coral { background: #ff5a5a; }
.tone-lime { background: #a8f000; color: #1a2b00; }
.tone-gray { background: #9a9a9a; }

.brand-wall {
  display: grid;
  grid-template-columns: repeat(6, 61px);
  gap: 5px 6px;
  justify-content: center;
  padding: 18px 0 8px;
  margin: 0 auto;
}

.brand-word {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 61px;
  height: 62px;
  padding: 4px;
  font-family: var(--font-heading);
  font-size: 9px;
  font-weight: 900;
  color: #999999;
  letter-spacing: 0.02em;
  text-align: center;
  background: #ffffff;
  border: 2px double #000000;
  transition: border-color 0.18s ease;
}

.brand-word img {
  max-width: 88%;
  max-height: 58%;
  object-fit: contain;
  filter: grayscale(1);
  opacity: 0.78;
  transition: opacity 0.18s ease;
}

.brand-word:hover {
  color: var(--color-primary);
  border-color: var(--color-primary);
}

.brand-word:hover img {
  filter: none;
  opacity: 1;
}

.news-carousel {
  position: relative;
  max-width: 900px;
  padding: 22px 40px 4px;
  margin: 0 auto;
}

.news-track {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.news-card {
  display: block;
  border: 1px solid #eeeeee;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.news-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 34px rgba(0, 0, 0, 0.08);
}

.news-thumb {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  aspect-ratio: 16 / 9;
  overflow: hidden;
  color: #ffffff;
  background: linear-gradient(135deg, #111111, #e6007e);
}

.news-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.news-thumb b {
  font-family: var(--font-heading);
  font-size: 22px;
  font-weight: 900;
  letter-spacing: 0.1em;
}

.news-thumb small {
  font-size: 9px;
  letter-spacing: 0.4em;
}

.news-card h3 {
  display: -webkit-box;
  min-height: 54px;
  padding: 12px 12px 4px;
  overflow: hidden;
  font-size: 13px;
  line-height: 1.5;
  color: #242125;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.news-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 14px;
  padding: 8px 12px 12px;
  font-size: 10px;
  color: #aaaaaa;
}

.news-arrow {
  position: absolute;
  top: 46%;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 46px;
  font-size: 28px;
  line-height: 1;
  color: #999999;
  transition: color 0.18s ease;
}

.news-arrow:hover {
  color: var(--color-primary);
}

.news-arrow.prev {
  left: 0;
}

.news-arrow.next {
  right: 0;
}

.news-dots {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding-top: 12px;
}

.news-dots button {
  width: 8px;
  height: 8px;
  background: #d5d5d5;
  border-radius: 50%;
  transition: background 0.18s ease, transform 0.18s ease;
}

.news-dots button.active {
  background: #242125;
  transform: scale(1.15);
}

.no-smoking {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 7px;
}

.no-smoking-divider {
  display: block;
  width: 100%;
  height: auto;
}

.no-smoking-lottie {
  width: 100%;
  height: 300px;
  margin-top: 0;
}

.brand-strip {
  padding: 10px 0 40px;
}

.brand-strip-grid {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 18px 38px;
  padding: 18px 0;
  border-top: 1px solid #eeeeee;
  border-bottom: 1px solid #eeeeee;
}

.brand-logo {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-heading);
  font-size: 13px;
  font-weight: 900;
  letter-spacing: 0.04em;
  color: #b5b5b5;
}

.brand-logo img {
  max-width: 96px;
  max-height: 28px;
  object-fit: contain;
  filter: grayscale(1);
  opacity: 0.65;
  transition: filter 0.2s ease, opacity 0.2s ease;
}

.brand-logo:hover img {
  filter: none;
  opacity: 1;
}

.brand-logo:hover {
  color: var(--color-primary);
}

@media (min-width: 901px) {
  .category-section {
    padding-top: 12px;
  }

  .new-section {
    padding-top: 17px;
  }

  .tag-pill {
    height: 38px;
    padding: 10px 11px;
  }

  .tag-section {
    padding-bottom: 23px;
  }
}

@media (max-width: 900px) {
  .home-top {
    padding-top: 15px;
  }

  .hero-banner {
    height: 230px;
    padding: 0 22px;
  }

  .hero-banner.hero-lottie {
    height: auto;
    padding: 0;
    aspect-ratio: 750 / 227;
  }

  .hero-copy {
    max-width: 100%;
  }

  .hero-copy h1 {
    font-size: 32px;
  }

  .hero-copy p {
    font-size: 12px;
    display: -webkit-box;
    overflow: hidden;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
  }

  .hero-products {
    display: none;
  }

  .hero-copy small {
    display: none;
  }

  .hero-products {
    width: 120px;
    height: 180px;
  }

  .hero-product {
    width: 82px;
    height: 110px;
    padding: 4px;
  }

  .hero-product-1 {
    top: 30px;
    left: -10px;
  }

  .hero-product-2 {
    top: 0;
    left: 30px;
  }

  .hero-product-3 {
    display: none;
  }

  .hero-wordmark b {
    font-size: 40px;
  }

  .category-section {
    padding-top: 15px;
  }

  .new-section {
    padding-top: 26px;
  }

  .product-grid-3 {
    display: flex;
    gap: 0;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    scrollbar-width: none;
  }

  .product-grid-3::-webkit-scrollbar {
    display: none;
  }

  .product-grid-3 > * {
    flex: 0 0 50%;
    max-width: 50%;
    scroll-snap-align: start;
  }

  .tag-bar {
    gap: 40px;
  }

  .brand-wall {
    grid-template-columns: repeat(6, 39px);
    gap: 5px 6px;
    padding: 12px 0 8px;
  }

  .brand-word {
    width: 39px;
    height: 40px;
    padding: 3px;
    font-size: 7px;
    line-height: 1.1;
    letter-spacing: 0;
    word-break: break-word;
  }

  .news-carousel {
    padding: 18px 24px 4px;
  }

  .news-track {
    gap: 10px;
  }

  .news-card h3 {
    min-height: 48px;
    padding: 8px 8px 2px;
    font-size: 11px;
  }

  .news-meta {
    padding: 6px 8px 8px;
    font-size: 9px;
  }

  .news-arrow {
    width: 22px;
    height: 40px;
    font-size: 22px;
  }

  .no-smoking {
    padding-top: 7px;
  }

  .no-smoking-lottie {
    height: 150px;
    margin-top: 3px;
  }
}
</style>
