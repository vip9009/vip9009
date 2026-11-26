<script setup>
import { computed, watchEffect } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { site, productsData } from '@/data'
import ProductCard from '@/components/ProductCard.vue'
import AppIcon from '@/components/AppIcon.vue'
import { asset, decodeEntities } from '@/utils'

const route = useRoute()

const section = computed(() =>
  productsData.sections.find((item) => item.id === route.params.section)
)
const index = computed(() => Number(route.params.index))
const product = computed(() => {
  if (!section.value || Number.isNaN(index.value)) return null
  return section.value.products[index.value] || null
})
const title = computed(() => (product.value ? decodeEntities(product.value.title) : '商品详情'))

const related = computed(() => {
  if (!section.value) return []
  return section.value.products
    .map((item, itemIndex) => ({ product: item, index: itemIndex, sectionId: section.value.id }))
    .filter((item) => item.index !== index.value)
    .slice(0, 4)
})

const features = [
  { icon: 'shield', title: '正品保证', text: '品牌正品，支持扫码验证' },
  { icon: 'globe', title: '全球包邮', text: '海外直邮，覆盖多个国家' },
  { icon: 'truck', title: '现货速发', text: '确认后尽快安排发出' },
  { icon: 'scan', title: '支持扫码验证', text: '收到货后可扫码核对真伪' }
]

watchEffect(() => {
  document.title = `${title.value} - 泡泡哥雾化`
})
</script>

<template>
  <div class="product-page">
    <div class="wrapper">
      <nav class="breadcrumb" aria-label="面包屑">
        <RouterLink to="/">首页</RouterLink>
        <span class="sep">/</span>
        <RouterLink v-if="section" :to="`/category/${section.id}`">{{ section.title }}</RouterLink>
        <span v-if="section" class="sep">/</span>
        <span>商品详情</span>
      </nav>

      <template v-if="product && section">
        <div class="detail-card">
          <div class="detail-media img-placeholder">
            <img
              :src="asset(product.localImage)"
              :alt="decodeEntities(product.imageAlt || product.title)"
            />
          </div>

          <div class="detail-info">
            <h1>{{ title }}</h1>

            <div class="price-line">
              <span class="price-label">参考价</span>
              <span class="now">￥{{ product.price }}</span>
              <span class="price-note">最终价格以泡泡哥确认为准</span>
            </div>

            <p class="lead">
              加泡泡哥微信或 QQ 获取实时价格、口味与物流方案。泡泡哥只做正品，支持扫码验证，
              不同国家与地区的配送方式由泡泡哥一对一确认。
            </p>

            <ul class="features">
              <li v-for="feature in features" :key="feature.title">
                <span class="feature-icon"><AppIcon :name="feature.icon" :size="20" /></span>
                <span>
                  <b>{{ feature.title }}</b>
                  <small>{{ feature.text }}</small>
                </span>
              </li>
            </ul>

            <div class="actions">
              <RouterLink class="btn btn-primary" to="/contact">加泡泡哥微信 / QQ 下单</RouterLink>
            </div>

            <p class="quick-contact">泡泡哥 QQ：{{ site.contacts.qq.number }}</p>
            <p class="note">本站仅展示分类与商品信息，下单请加泡泡哥微信或 QQ。</p>
          </div>
        </div>

        <section v-if="related.length" class="related">
          <div class="section-head">
            <h2>相关推荐</h2>
          </div>
          <div class="product-grid related-grid">
            <ProductCard
              v-for="item in related"
              :key="`${item.sectionId}-${item.index}`"
              :product="item.product"
              :section-id="item.sectionId"
              :index="item.index"
            />
          </div>
        </section>
      </template>

      <div v-else class="empty-state">
        <h3>商品不存在或已下架</h3>
        <p>该商品可能已经调整，返回首页看看其他现货商品吧。</p>
        <div class="empty-actions">
          <RouterLink class="btn btn-primary" to="/">返回首页</RouterLink>
          <RouterLink class="btn btn-ghost" to="/contact">联系我们</RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.detail-card {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 32px;
  padding: 24px;
  margin-bottom: 24px;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(17, 58, 93, 0.05);
}

.detail-media {
  position: relative;
  aspect-ratio: 1 / 1;
  overflow: hidden;
  background: #fff;
  border: 1px solid #f5f6f7;
  border-radius: 4px;
}

.detail-media img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.detail-info h1 {
  margin-bottom: 16px;
  font-size: 24px;
  font-weight: 600;
  line-height: 1.45;
}

.price-line {
  display: flex;
  align-items: baseline;
  gap: 10px;
  padding: 12px 16px;
  margin-bottom: 14px;
  background: #f8fbff;
  border-top: 1px solid #f5f6f7;
  border-bottom: 1px solid #f5f6f7;
}

.price-line .now {
  font-size: 28px;
  font-weight: 600;
  color: #f44336;
}

.lead {
  padding: 14px 16px;
  margin-bottom: 18px;
  font-size: 13px;
  line-height: 1.85;
  color: #666;
  background: #fafafa;
  border-radius: 4px;
}

.features {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.features li {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px;
  border: 1px solid #f2f2f2;
  border-radius: 4px;
}

.feature-icon {
  display: flex;
  flex: 0 0 34px;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  color: var(--accent);
  background: rgba(252, 60, 45, 0.07);
  border-radius: 50%;
}

.features b {
  display: block;
  margin-bottom: 2px;
  font-size: 13px;
  font-weight: 600;
}

.features small {
  display: block;
  font-size: 11px;
  line-height: 1.5;
  color: #999;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 20px;
}

.note {
  margin-top: 12px;
  font-size: 12px;
  color: #aaa;
}

.related {
  padding-bottom: 8px;
}

.section-head {
  margin-bottom: 16px;
}

.section-head h2 {
  font-size: 22px;
  font-weight: 600;
  line-height: 1.2;
}

@media (max-width: 768px) {
  .detail-card {
    grid-template-columns: minmax(0, 1fr);
    gap: 16px;
    padding: 16px;
    margin-bottom: 24px;
  }

  .detail-info h1 {
    font-size: 22px;
    margin-bottom: 12px;
  }

  .price-line .now {
    font-size: 24px;
  }

  .features {
    grid-template-columns: minmax(0, 1fr);
  }

  .section-head h2 {
    font-size: 18px;
  }
}

/* UI UX Pro Max design system overrides */
.detail-card {
  gap: 40px;
  padding: 32px;
  margin-bottom: 32px;
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 28px;
  box-shadow: var(--shadow-card);
}

.detail-media {
  background: #f7fffb;
  border: 1px solid var(--color-border);
  border-radius: 20px;
}

.detail-info h1 {
  margin-bottom: 18px;
  font-family: var(--font-heading);
  font-size: clamp(26px, 2.6vw, 34px);
  font-weight: 600;
  line-height: 1.3;
  color: var(--color-foreground);
}

.price-line {
  padding: 14px 18px;
  margin-bottom: 16px;
  background: var(--color-muted);
  border: 0;
  border-radius: 14px;
}

.price-line .now {
  color: var(--color-primary);
  font-family: var(--font-heading);
  font-size: 32px;
}

.price-line {
  display: flex;
  align-items: baseline;
  flex-wrap: wrap;
  gap: 10px;
}

.price-label {
  align-self: center;
  padding: 4px 9px;
  font-size: 11px;
  font-weight: 600;
  color: var(--color-on-primary);
  background: var(--color-primary);
  border-radius: 999px;
}

.price-note {
  margin-left: auto;
  font-size: 12px;
  color: var(--color-muted-foreground);
}

.lead {
  padding: 16px 18px;
  margin-bottom: 20px;
  color: var(--color-muted-foreground);
  background: var(--color-muted);
  border-radius: 14px;
}

.features {
  gap: 14px;
}

.features li {
  padding: 14px;
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 14px;
}

.feature-icon {
  color: var(--color-primary);
  background: var(--color-muted);
  border-radius: 12px;
}

.features b {
  font-family: var(--font-heading);
  font-size: 14px;
  color: var(--color-foreground);
}

.features small {
  color: var(--color-muted-foreground);
}

.actions {
  gap: 12px;
  margin-top: 24px;
}

.note {
  color: var(--color-muted-foreground);
}

.quick-contact {
  display: inline-flex;
  align-items: center;
  margin-top: 14px;
  padding: 6px 12px;
  font-family: var(--font-heading);
  font-size: 13px;
  font-weight: 600;
  color: var(--color-on-accent);
  background: var(--color-accent);
  border-radius: 999px;
  user-select: all;
}

.related {
  padding-bottom: 16px;
}

.related-grid {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

@media (max-width: 900px) {
  .related-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

.section-head {
  margin-bottom: 20px;
}

.section-head h2 {
  font-size: clamp(28px, 3.4vw, 40px);
  color: var(--color-foreground);
}

@media (max-width: 768px) {
  .detail-card {
    padding: 16px;
    border-radius: 20px;
  }

  .detail-media {
    border-radius: 16px;
  }

  .price-line .now {
    font-size: 26px;
  }

  .section-head h2 {
    font-size: 26px;
  }
}
</style>
