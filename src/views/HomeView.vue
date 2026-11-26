<script setup>
import { computed, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { site, productsData } from '@/data'
import VpProductCard from '@/components/VpProductCard.vue'
import CategoryGlyph from '@/components/CategoryGlyph.vue'

const activeTab = ref('tag')
const page = ref(0)
const pageSize = 6

const hero = computed(() => site.hero || {})

const allProducts = computed(() =>
  productsData.sections
    .filter((section) => section.id !== 'hot')
    .flatMap((section) =>
      (section.products || []).map((product, index) => ({
        ...product,
        sectionId: section.id,
        sectionTitle: section.title,
        index
      }))
    )
)

const heroProducts = computed(() => allProducts.value.slice(0, 3))

const tiles = computed(() => {
  const glyphMap = {
    disposables: 'disposable',
    pods: 'pod',
    jimu: 'box',
    'pod-system': 'device',
    'e-liquid': 'liquid',
    gbxl: 'gbxl'
  }
  const fromCategories = Object.entries(site.categories)
    .filter(([id, item]) => !item.parent && id !== 'hot' && id !== 'contact' && item.section)
    .sort((a, b) => (a[1].sort ?? 999) - (b[1].sort ?? 999))
    .map(([id, item]) => ({
      title: item.title,
      to: `/category/${id}`,
      glyph: glyphMap[id] || 'disposable',
      accent: false
    }))
  return [
    ...fromCategories,
    { title: '组合专区', to: '/category/hot', glyph: 'combo', accent: false },
    { title: '优惠活动', to: '/category/hot', glyph: 'promo', accent: true }
  ].slice(0, 8)
})

const newProducts = computed(() => allProducts.value.slice(0, 24))
const pageCount = computed(() => Math.max(1, Math.ceil(newProducts.value.length / pageSize)))
const visibleProducts = computed(() =>
  newProducts.value.slice(page.value * pageSize, (page.value + 1) * pageSize)
)

const tags = computed(() => site.tags || [])
const brands = computed(() => site.brands || [])
const news = computed(() => site.news || [])

function setPage(index) {
  page.value = index
}
</script>

<template>
  <div class="home-page">
    <div class="wrapper home-top">
      <RouterLink class="hero-banner" :to="hero.link || '/category/hot'">
        <div class="hero-copy">
          <span class="hero-eyebrow">{{ hero.eyebrow }}</span>
          <h1>{{ hero.title }}</h1>
          <p>{{ hero.subtitle }}</p>
          <span class="hero-cta">{{ hero.cta }} →</span>
          <small>{{ hero.note }}</small>
        </div>

        <div v-if="heroProducts.length" class="hero-products">
          <div v-for="(product, idx) in heroProducts" :key="product.title" class="hero-product" :class="`hero-product-${idx + 1}`">
            <img :src="product.localImage" :alt="product.title" />
          </div>
        </div>
        <div v-else class="hero-wordmark" aria-hidden="true">
          <b>PAOPAO</b>
          <span>SELECT</span>
        </div>
      </RouterLink>
    </div>

    <section class="category-section">
      <div class="wrapper">
        <div class="category-tiles">
          <RouterLink
            v-for="tile in tiles"
            :key="tile.title"
            class="category-tile"
            :class="{ accent: tile.accent }"
            :to="tile.to"
          >
            <span class="category-glyph"><CategoryGlyph :name="tile.glyph" /></span>
            <b>{{ tile.title }}</b>
          </RouterLink>
        </div>
      </div>
    </section>

    <section class="new-section">
      <div class="wrapper">
        <div class="new-divider" aria-hidden="true">
          <span class="divider-arrow left" />
          <b>NEW</b>
          <span class="divider-arrow right" />
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
            {{ index }}
          </button>
        </div>

        <div v-if="visibleProducts.length" class="product-grid-3">
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

        <div v-if="activeTab === 'tag'" class="tag-cloud">
          <RouterLink
            v-for="tag in tags"
            :key="tag.label"
            class="tag-pill"
            :class="`tone-${tag.tone}`"
            :to="`/search?q=${encodeURIComponent(tag.label)}`"
          >
            {{ tag.label }}
          </RouterLink>
        </div>

        <div v-else-if="activeTab === 'brand'" class="brand-wall">
          <RouterLink
            v-for="brand in brands"
            :key="brand"
            class="brand-word"
            :to="`/search?q=${encodeURIComponent(brand.split(' ').pop())}`"
          >
            {{ brand }}
          </RouterLink>
        </div>

        <div v-else class="news-grid">
          <RouterLink v-for="(item, index) in news" :key="item.title" class="news-card" :to="item.to || '/info/about'">
            <span class="news-thumb" :class="`news-thumb-${(index % 3) + 1}`">
              <b>PAOPAO</b>
              <small>NEWS</small>
            </span>
            <h3>{{ item.title }}</h3>
            <p>{{ item.excerpt }}</p>
            <time>{{ item.date }}</time>
          </RouterLink>
        </div>
      </div>
    </section>

    <div class="no-smoking" aria-hidden="true">
      <span class="ns-arrow left" />
      <b>NO SMOKING</b>
      <span class="ns-arrow right" />
    </div>

    <section class="brand-strip">
      <div class="wrapper">
        <div class="brand-strip-grid">
          <RouterLink
            v-for="brand in brands"
            :key="brand"
            class="brand-logo"
            :to="`/search?q=${encodeURIComponent(brand.split(' ').pop())}`"
          >
            {{ brand }}
          </RouterLink>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-page {
  background: #ffffff;
}

.home-top {
  padding-top: 28px;
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
  padding: 34px 0 8px;
}

.category-tiles {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  row-gap: 26px;
}

.category-tile {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  color: #242125;
  transition: color 0.18s ease;
}

.category-tile:hover {
  color: var(--color-primary);
}

.category-glyph {
  width: 128px;
  height: 128px;
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
  padding-top: 28px;
}

.new-divider {
  display: flex;
  align-items: center;
  gap: 18px;
  margin-bottom: 10px;
}

.new-divider b {
  font-family: var(--font-heading);
  font-size: 40px;
  font-weight: 900;
  letter-spacing: 0.02em;
  font-style: italic;
  color: #242125;
}

.divider-arrow {
  position: relative;
  flex: 1;
  height: 1px;
  background: #dddddd;
}

.divider-arrow::before,
.divider-arrow::after {
  content: '';
  position: absolute;
  top: -3px;
  width: 8px;
  height: 8px;
  border-top: 1px solid #999999;
  border-right: 1px solid #999999;
}

.divider-arrow.left::before {
  left: 0;
  transform: rotate(-135deg);
}

.divider-arrow.left::after {
  left: 14px;
  transform: rotate(-135deg);
}

.divider-arrow.right::before {
  right: 0;
  transform: rotate(45deg);
}

.divider-arrow.right::after {
  right: 14px;
  transform: rotate(45deg);
}

.page-tabs {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 22px;
}

.page-tab {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  font-size: 11px;
  color: #999999;
  border: 1px solid #dddddd;
  border-radius: 50%;
  transition: color 0.16s ease, border-color 0.16s ease, background 0.16s ease;
}

.page-tab:hover {
  color: var(--color-primary);
  border-color: var(--color-primary);
}

.page-tab.active {
  color: #ffffff;
  background: #242125;
  border-color: #242125;
}

.product-grid-3 {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
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
  padding-top: 36px;
}

.tag-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 64px;
  height: 34px;
  background: #111111;
  clip-path: polygon(2% 0, 98% 0, 100% 50%, 98% 100%, 2% 100%, 0 50%);
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

.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 6px;
  max-width: 760px;
  padding: 20px 0 4px;
  margin: 0 auto;
}

.tag-pill {
  display: inline-flex;
  align-items: center;
  height: 24px;
  padding: 0 9px;
  font-size: 10px;
  font-weight: 700;
  color: #ffffff;
  background: #242125;
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
  grid-template-columns: repeat(6, minmax(0, 1fr));
  max-width: 900px;
  padding: 22px 0 8px;
  margin: 0 auto;
}

.brand-word {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 56px;
  font-family: var(--font-heading);
  font-size: 14px;
  font-weight: 900;
  color: #999999;
  letter-spacing: 0.04em;
  text-align: center;
}

.brand-word:hover {
  color: var(--color-primary);
}

.news-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
  padding-top: 22px;
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
  height: 120px;
  color: #ffffff;
  background: linear-gradient(135deg, #111111, #e6007e);
}

.news-thumb-2 {
  background: linear-gradient(135deg, #e6007e, #7500c0);
}

.news-thumb-3 {
  background: linear-gradient(135deg, #111111, #16c8d6);
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
  padding: 12px 12px 4px;
  font-size: 13px;
  line-height: 1.5;
  color: #242125;
}

.news-card p {
  padding: 0 12px;
  font-size: 11px;
  line-height: 1.6;
  color: #888888;
  display: -webkit-box;
  overflow: hidden;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.news-card time {
  display: block;
  padding: 10px 12px 12px;
  font-size: 10px;
  color: #aaaaaa;
}

.no-smoking {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 22px;
  padding: 46px 20px 26px;
}

.no-smoking b {
  font-family: var(--font-heading);
  font-size: clamp(36px, 5vw, 64px);
  font-weight: 900;
  font-style: italic;
  letter-spacing: -0.03em;
  color: #242125;
}

.ns-arrow {
  position: relative;
  width: 80px;
  height: 1px;
  background: #cccccc;
}

.ns-arrow::before,
.ns-arrow::after {
  content: '';
  position: absolute;
  top: -3px;
  width: 8px;
  height: 8px;
  border-top: 1px solid #999999;
  border-right: 1px solid #999999;
}

.ns-arrow.left::before {
  left: 0;
  transform: rotate(-135deg);
}

.ns-arrow.right::before {
  right: 0;
  transform: rotate(45deg);
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
  font-family: var(--font-heading);
  font-size: 13px;
  font-weight: 900;
  letter-spacing: 0.04em;
  color: #b5b5b5;
}

.brand-logo:hover {
  color: var(--color-primary);
}

@media (max-width: 900px) {
  .home-top {
    padding-top: 16px;
  }

  .hero-banner {
    height: 230px;
    padding: 0 22px;
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
    padding-top: 22px;
  }

  .category-glyph {
    width: 74px;
    height: 74px;
  }

  .category-tile b {
    font-size: 13px;
  }

  .category-tiles {
    row-gap: 16px;
  }

  .new-divider b {
    font-size: 30px;
  }

  .product-grid-3 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
  }

  .tag-bar {
    gap: 40px;
  }

  .brand-wall {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .news-grid {
    grid-template-columns: minmax(0, 1fr);
  }

  .no-smoking {
    padding: 30px 16px 18px;
  }

  .ns-arrow {
    width: 40px;
  }
}
</style>
