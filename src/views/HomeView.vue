<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { site, productsData } from '@/data'
import ProductSection from '@/components/ProductSection.vue'
import AppIcon from '@/components/AppIcon.vue'
import { asset } from '@/utils'

const moreLinks = {
  hot: '/category/hot',
  disposables: '/category/disposables',
  jimu: '/category/jimu',
  pods: '/category/pods'
}

const heroProducts = productsData.sections[0]?.products.slice(0, 4) || []

const trustItems = [
  { icon: 'shield', title: '正品保障', text: '支持官方扫码验证' },
  { icon: 'globe', title: '全球包邮', text: '海外直邮多个国家' },
  { icon: 'truck', title: '现货速发', text: '确认后尽快发出' },
  { icon: 'scan', title: '扫码验证', text: '收到货后可核对' }
]

const categoryIcons = {
  disposables: 'zap',
  pods: 'droplet',
  'pod-system': 'device',
  'e-liquid': 'flask',
  jimu: 'blocks',
  gbxl: 'shield'
}

const categoryCards = computed(() =>
  Object.entries(site.categories)
    .filter(([id]) => id !== 'hot')
    .map(([id, category]) => {
      const section = productsData.sections.find((item) => item.id === category.section)
      return {
        id,
        title: category.title,
        desc: category.desc,
        count: section?.products.length || 0,
        icon: categoryIcons[id] || 'blocks'
      }
    })
)
</script>

<template>
  <div class="home-page">
    <section class="hero">
      <div class="hero-shape hero-shape-a" aria-hidden="true" />
      <div class="hero-shape hero-shape-b" aria-hidden="true" />
      <div class="wrapper hero-grid">
        <div class="hero-copy">
          <span class="eyebrow"><i /> 泡泡哥雾化 · 海外电子烟直邮</span>
          <h1>正品电子烟<br /><em>直邮到家</em></h1>
          <p class="hero-lede">
            悦刻、雪加、冰熊、柚子等品牌现货。按分类查看产品与价格，选好后加泡泡哥微信或 QQ，
            由泡泡哥确认口味、价格与物流。
          </p>

          <div class="hero-actions">
            <RouterLink class="btn btn-primary" to="/contact">
              加泡泡哥咨询
              <AppIcon name="arrow-right" :size="18" />
            </RouterLink>
            <RouterLink class="btn btn-ghost" to="/category/hot">浏览全部产品</RouterLink>
          </div>

          <ul class="hero-trust">
            <li v-for="item in trustItems" :key="item.title">
              <span class="trust-icon"><AppIcon :name="item.icon" :size="18" /></span>
              <span>
                <b>{{ item.title }}</b>
                <small>{{ item.text }}</small>
              </span>
            </li>
          </ul>
        </div>

        <div class="hero-visual">
          <div class="hero-panel" aria-hidden="true" />
          <div class="hero-collage">
            <div
              v-for="(product, index) in heroProducts"
              :key="product.title"
              class="collage-item"
              :class="`collage-item-${index + 1}`"
            >
              <img :src="asset(product.localImage)" alt="" />
            </div>
          </div>
          <div class="floating-badge floating-badge-top">
            <AppIcon name="shield" :size="18" />
            正品保障
          </div>
          <div class="floating-badge floating-badge-bottom">
            <AppIcon name="truck" :size="18" />
            现货速发
          </div>
          <div class="hero-sticker" aria-hidden="true">
            <b>100%</b>
            <span>正品直供</span>
          </div>
        </div>
      </div>
    </section>

    <section class="seller-section">
      <div class="wrapper">
        <div class="seller-card">
          <img
            class="seller-photo"
            :src="asset('/images/paopao-avatar-600.jpg')"
            alt="泡泡哥"
            width="180"
            height="180"
          />
          <div class="seller-copy">
            <span class="section-eyebrow">MEET PAOPAO</span>
            <h2>我是泡泡哥，所有货由我亲自选</h2>
            <p>
              站内商品由我亲自选品、验货、发货。网站只做分类与价格展示，
              选好后加我微信或 QQ，我帮你确认口味、价格和物流。
            </p>
          </div>
          <RouterLink class="btn btn-primary seller-btn" to="/contact">
            加泡泡哥微信
            <AppIcon name="arrow-right" :size="17" />
          </RouterLink>
        </div>
      </div>
    </section>

    <section class="category-section">
      <div class="wrapper">
        <div class="section-head">
          <div>
            <span class="section-eyebrow">PRODUCT CATEGORIES</span>
            <h2>按分类找产品</h2>
          </div>
          <p>全品类电子烟目录，价格透明。展示价格为参考价，最终以泡泡哥微信 / QQ 确认为准。</p>
        </div>

        <div class="category-grid">
          <RouterLink
            v-for="category in categoryCards"
            :key="category.id"
            class="category-card"
            :to="`/category/${category.id}`"
          >
            <span class="category-icon"><AppIcon :name="category.icon" :size="24" /></span>
            <span class="category-info">
              <b>{{ category.title }}</b>
              <small>{{ category.desc }}</small>
            </span>
            <span class="category-meta">
              {{ category.count ? `${category.count} 款` : '咨询客服' }}
              <AppIcon name="arrow-right" :size="15" />
            </span>
          </RouterLink>
        </div>
      </div>
    </section>

    <ProductSection
      v-for="section in productsData.sections"
      :key="section.id"
      :section="section"
      :more-to="moreLinks[section.id] || '/category/hot'"
    />

    <section class="final-cta-section">
      <div class="wrapper">
        <div class="final-cta">
          <div class="final-cta-copy">
            <span class="section-eyebrow section-eyebrow-light">READY TO ORDER?</span>
            <h2>选好产品？<br />加泡泡哥微信或 QQ 下单</h2>
            <p>把产品名称或截图发给泡泡哥，确认口味、价格与物流后即可下单。只做正品，支持扫码验证。</p>
          </div>
          <div class="final-cta-actions">
            <RouterLink class="btn btn-primary" to="/contact">
              加泡泡哥微信 / QQ
              <AppIcon name="arrow-right" :size="18" />
            </RouterLink>
            <RouterLink class="btn btn-cta-light" to="/category/hot">浏览热门产品</RouterLink>
          </div>
          <div class="final-cta-shape" aria-hidden="true" />
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.hero {
  position: relative;
  padding: 28px 0 72px;
  overflow: hidden;
  background:
    radial-gradient(circle at 12% 18%, rgba(16, 185, 129, 0.16) 0, transparent 34%),
    radial-gradient(circle at 88% 12%, rgba(234, 88, 12, 0.1) 0, transparent 28%),
    var(--color-background);
}

.hero-grid {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: minmax(0, 1.02fr) minmax(0, 0.98fr);
  gap: 48px;
  align-items: center;
}

.hero-copy {
  max-width: 620px;
}

.eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  margin-bottom: 24px;
  font-family: var(--font-heading);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.08em;
  color: var(--color-primary-strong);
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 999px;
  box-shadow: 0 8px 20px rgba(6, 78, 59, 0.06);
}

.eyebrow i {
  width: 8px;
  height: 8px;
  background: var(--color-primary);
  border-radius: 50%;
  box-shadow: 0 0 0 4px rgba(5, 150, 105, 0.12);
}

.hero h1 {
  margin-bottom: 20px;
  font-size: clamp(44px, 5.2vw, 72px);
  font-weight: 700;
  line-height: 1.02;
  letter-spacing: -0.04em;
  color: var(--color-foreground);
}

.hero h1 em {
  position: relative;
  z-index: 1;
  font-style: normal;
  color: var(--color-primary);
}

.hero h1 em::after {
  content: '';
  position: absolute;
  right: -6px;
  bottom: 8px;
  left: -6px;
  z-index: -1;
  height: 18px;
  background: rgba(16, 185, 129, 0.22);
  border-radius: 4px;
  transform: rotate(-1deg);
}

.hero-lede {
  max-width: 580px;
  margin-bottom: 28px;
  font-size: 16px;
  line-height: 1.85;
  color: var(--color-muted-foreground);
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 30px;
}

.hero-actions .btn {
  min-height: 52px;
  padding: 0 26px;
}

.hero-trust {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px 20px;
  max-width: 520px;
}

.hero-trust li {
  display: flex;
  align-items: center;
  gap: 10px;
}

.trust-icon {
  display: flex;
  flex: 0 0 34px;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  color: var(--color-primary);
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 10px;
}

.hero-trust b {
  display: block;
  font-family: var(--font-heading);
  font-size: 13px;
  font-weight: 600;
  line-height: 1.3;
  color: var(--color-foreground);
}

.hero-trust small {
  display: block;
  font-size: 11px;
  line-height: 1.4;
  color: var(--color-muted-foreground);
}

.hero-visual {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 540px;
}

.hero-panel {
  position: absolute;
  inset: 18px 10px;
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
  border-radius: 32px;
  transform: rotate(-4deg);
  box-shadow: 0 30px 70px rgba(5, 150, 105, 0.24);
}

.hero-panel::after {
  content: '';
  position: absolute;
  inset: 18px;
  border: 2px dashed rgba(255, 255, 255, 0.32);
  border-radius: 22px;
}

.hero-collage {
  position: relative;
  z-index: 2;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
  width: min(100%, 430px);
  transform: rotate(2deg);
}

.collage-item {
  display: flex;
  align-items: center;
  justify-content: center;
  aspect-ratio: 1 / 1;
  padding: 10px;
  background: var(--color-card);
  border: 2px solid rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(6, 78, 59, 0.16);
  transition: transform 0.25s ease;
}

.collage-item:hover {
  transform: translateY(-4px) rotate(-1deg);
}

.collage-item img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.collage-item-2 {
  transform: translateY(18px);
}

.collage-item-3 {
  transform: translateY(-18px);
}

.floating-badge {
  position: absolute;
  z-index: 3;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  font-family: var(--font-heading);
  font-size: 13px;
  font-weight: 600;
  color: var(--color-foreground);
  background: var(--color-card);
  border: 2px solid var(--color-border);
  border-radius: 14px;
  box-shadow: var(--shadow-card);
  animation: float-badge 4s ease-in-out infinite;
}

.floating-badge :deep(svg) {
  color: var(--color-primary);
}

.floating-badge-top {
  top: 9%;
  right: 0;
}

.floating-badge-bottom {
  bottom: 10%;
  left: -4px;
  animation-delay: -2s;
}

@keyframes float-badge {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-8px);
  }
}

.hero-sticker {
  position: absolute;
  top: 12%;
  left: 2%;
  z-index: 3;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 92px;
  height: 92px;
  color: var(--color-on-accent);
  background: var(--color-accent);
  border-radius: 24px;
  transform: rotate(-8deg);
  box-shadow: 0 18px 34px rgba(234, 88, 12, 0.28);
}

.hero-sticker b {
  font-family: var(--font-heading);
  font-size: 24px;
  line-height: 1;
}

.hero-sticker span {
  margin-top: 4px;
  font-size: 11px;
  font-weight: 600;
}

.hero-shape {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
}

.hero-shape-a {
  top: -120px;
  right: -100px;
  width: 360px;
  height: 360px;
  background: rgba(5, 150, 105, 0.08);
}

.hero-shape-b {
  bottom: -140px;
  left: -80px;
  width: 300px;
  height: 300px;
  background: rgba(234, 88, 12, 0.06);
}

.seller-section {
  padding-bottom: var(--section-gap);
}

.seller-card {
  display: flex;
  align-items: center;
  gap: 28px;
  padding: 24px;
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 28px;
  box-shadow: var(--shadow-card);
}

.seller-photo {
  flex: 0 0 180px;
  width: 180px;
  height: 180px;
  object-fit: cover;
  border: 3px solid var(--color-border);
  border-radius: 20px;
}

.seller-copy {
  flex: 1;
  min-width: 0;
}

.seller-copy h2 {
  margin-bottom: 10px;
  font-size: clamp(24px, 2.6vw, 34px);
  color: var(--color-foreground);
}

.seller-copy p {
  max-width: 680px;
  font-size: 14px;
  line-height: 1.85;
  color: var(--color-muted-foreground);
}

.seller-btn {
  flex: 0 0 auto;
}

.category-section {
  padding-bottom: var(--section-gap);
}

.section-head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 32px;
  margin-bottom: 24px;
}

.section-eyebrow {
  display: block;
  margin-bottom: 8px;
  font-family: var(--font-heading);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.14em;
  color: var(--color-primary-strong);
}

.section-eyebrow-light {
  color: #a7f3d0;
}

.section-head h2 {
  font-size: clamp(28px, 3.4vw, 40px);
  color: var(--color-foreground);
}

.section-head > p {
  max-width: 430px;
  font-size: 14px;
  line-height: 1.7;
  color: var(--color-muted-foreground);
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 20px;
}

.category-card {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 22px;
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 20px;
  box-shadow: var(--shadow-card);
  transition: transform 0.24s ease, box-shadow 0.24s ease, border-color 0.24s ease;
}

.category-card:hover {
  transform: translateY(-5px);
  border-color: var(--color-primary);
  box-shadow: var(--shadow-hover);
}

.category-icon {
  display: flex;
  flex: 0 0 48px;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  color: var(--color-primary);
  background: var(--color-muted);
  border-radius: 14px;
}

.category-info {
  flex: 1;
  min-width: 0;
}

.category-info b {
  display: block;
  margin-bottom: 5px;
  font-family: var(--font-heading);
  font-size: 17px;
  font-weight: 600;
  color: var(--color-foreground);
}

.category-info small {
  display: -webkit-box;
  overflow: hidden;
  font-size: 12px;
  line-height: 1.7;
  color: var(--color-muted-foreground);
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

.category-meta {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  flex: 0 0 auto;
  padding-top: 3px;
  font-size: 12px;
  font-weight: 600;
  color: var(--color-primary-strong);
  white-space: nowrap;
}

.final-cta-section {
  padding-bottom: var(--section-gap);
}

.final-cta {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 32px;
  padding: 48px;
  overflow: hidden;
  color: #ffffff;
  background: linear-gradient(135deg, var(--color-foreground), #0b7a5f);
  border-radius: 28px;
  box-shadow: 0 30px 70px rgba(6, 78, 59, 0.24);
}

.final-cta-copy {
  position: relative;
  z-index: 1;
  max-width: 620px;
}

.final-cta h2 {
  margin-bottom: 12px;
  font-size: clamp(30px, 3.6vw, 44px);
  color: #ffffff;
}

.final-cta p {
  font-size: 14px;
  line-height: 1.8;
  color: #a7f3d0;
}

.final-cta-actions {
  position: relative;
  z-index: 1;
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  flex: 0 0 auto;
}

.btn-cta-light {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(255, 255, 255, 0.38);
}

.btn-cta-light:hover {
  color: var(--color-foreground);
  background: #ffffff;
  border-color: #ffffff;
}

.final-cta-shape {
  position: absolute;
  top: -80px;
  right: -40px;
  width: 260px;
  height: 260px;
  border: 40px solid rgba(255, 255, 255, 0.06);
  border-radius: 50%;
}

@media (max-width: 1024px) {
  .hero-grid {
    gap: 28px;
  }

  .hero-visual {
    min-height: 460px;
  }

  .hero-collage {
    width: min(100%, 360px);
  }

  .category-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .hero {
    padding: 18px 0 44px;
  }

  .hero-grid {
    grid-template-columns: minmax(0, 1fr);
    gap: 36px;
  }

  .hero-copy {
    max-width: none;
  }

  .hero h1 {
    font-size: clamp(38px, 10vw, 52px);
  }

  .hero-lede {
    font-size: 15px;
  }

  .hero-actions {
    margin-bottom: 24px;
  }

  .hero-actions .btn {
    flex: 1;
    min-height: 50px;
    padding: 0 16px;
  }

  .hero-trust {
    gap: 10px 12px;
  }

  .hero-visual {
    min-height: 360px;
  }

  .hero-panel {
    inset: 8px 0;
    border-radius: 24px;
  }

  .hero-collage {
    width: min(84%, 320px);
    gap: 10px;
  }

  .collage-item {
    border-radius: 16px;
  }

  .floating-badge {
    padding: 8px 10px;
    font-size: 11px;
    border-radius: 11px;
  }

  .floating-badge-top {
    top: 4%;
    right: -2px;
  }

  .floating-badge-bottom {
    bottom: 4%;
    left: -2px;
  }

  .hero-sticker {
    top: 6%;
    left: 0;
    width: 72px;
    height: 72px;
    border-radius: 18px;
  }

  .hero-sticker b {
    font-size: 19px;
  }

  .hero-sticker span {
    font-size: 9px;
  }

  .section-head {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .section-head > p {
    max-width: none;
  }

  .category-grid {
    grid-template-columns: minmax(0, 1fr);
    gap: 12px;
  }

  .seller-card {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
    padding: 18px;
    border-radius: 20px;
  }

  .seller-photo {
    flex: 0 0 140px;
    width: 140px;
    height: 140px;
    border-radius: 16px;
  }

  .seller-copy h2 {
    font-size: 22px;
  }

  .seller-copy p {
    font-size: 13px;
  }

  .seller-btn {
    width: 100%;
  }

  .category-card {
    padding: 18px;
  }

  .category-icon {
    flex-basis: 42px;
    width: 42px;
    height: 42px;
    border-radius: 12px;
  }

  .category-info b {
    font-size: 16px;
  }

  .final-cta {
    flex-direction: column;
    align-items: flex-start;
    padding: 28px;
    border-radius: 22px;
  }

  .final-cta-actions {
    width: 100%;
  }

  .final-cta-actions .btn {
    flex: 1;
  }
}
</style>
