<script setup>
import { computed, watchEffect } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { site, productsData } from '@/data'
import ProductCard from '@/components/ProductCard.vue'
import { filterByBrand } from '@/utils/categories'

const route = useRoute()

const category = computed(() => site.categories[route.params.id] || null)
const brand = computed(() => String(route.query.brand || '').trim())

const sourceSection = computed(() => {
  const sectionId = category.value?.section
  if (!sectionId) return null
  return productsData.sections.find((section) => section.id === sectionId) || null
})

const items = computed(() => {
  if (!sourceSection.value) return []
  const section = sourceSection.value
  return filterByBrand(section.products, brand.value).map((product, index) => ({
    product,
    index: section.products.indexOf(product),
    sectionId: section.id
  }))
})

const title = computed(() => {
  if (!category.value) return '商品分类'
  return brand.value ? `${brand.value}${category.value.title}` : category.value.title
})

const chips = computed(() =>
  Object.entries(site.categories)
    .filter(([id]) => id !== 'hot')
    .map(([id, item]) => ({ id, title: item.title, section: item.section }))
)

watchEffect(() => {
  document.title = `${title.value} - 泡泡哥雾化`
})
</script>

<template>
  <div class="category-page">
    <div class="wrapper">
      <nav class="breadcrumb" aria-label="面包屑">
        <RouterLink to="/">首页</RouterLink>
        <span class="sep">/</span>
        <span>{{ category ? category.title : '商品分类' }}</span>
        <template v-if="brand">
          <span class="sep">/</span>
          <span>{{ brand }}</span>
        </template>
      </nav>

      <template v-if="category">
        <div class="page-head">
          <div>
            <h1 class="page-title">{{ title }}</h1>
            <p class="page-subtitle">{{ category.desc }} · 共 {{ items.length }} 件商品</p>
          </div>
        </div>

        <div v-if="items.length" class="product-grid category-grid">
          <ProductCard
            v-for="item in items"
            :key="`${item.sectionId}-${item.index}`"
            :product="item.product"
            :section-id="item.sectionId"
            :index="item.index"
          />
        </div>

        <div v-else class="empty-state">
          <h3>{{ brand || category.title }}商品正在整理中</h3>
          <p>
            该分类暂未上架可展示的商品。添加客服即可获取最新款式、口味与报价，我们会第一时间为你确认价格。
          </p>
          <div class="empty-actions">
            <RouterLink class="btn btn-primary" to="/contact">联系我们</RouterLink>
          </div>
          <p class="empty-qq">QQ：{{ site.contacts.qq.number }}</p>
        </div>

        <div class="category-chips">
          <RouterLink
            v-for="chip in chips"
            :key="chip.id"
            class="chip"
            :class="{ active: chip.id === route.params.id && !brand }"
            :to="`/category/${chip.id}`"
          >
            {{ chip.title }}
          </RouterLink>
        </div>
      </template>

      <div v-else class="empty-state">
        <h3>没有找到这个分类</h3>
        <p>分类可能已经调整，返回首页看看当前在售的商品吧。</p>
        <div class="empty-actions">
          <RouterLink class="btn btn-primary" to="/">返回首页</RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.category-grid {
  margin-bottom: 24px;
}

.category-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding-top: 4px;
}

.empty-qq {
  margin: 16px auto 0 !important;
  font-family: var(--font-heading);
  font-size: 14px;
  font-weight: 600;
  color: var(--color-primary-strong) !important;
  user-select: all;
}

.chip {
  display: inline-flex;
  align-items: center;
  height: 32px;
  padding: 0 14px;
  font-size: 12px;
  color: #666;
  background: #fff;
  border: 1px solid #f0f0f0;
  border-radius: 20px;
  transition: color 0.18s ease, border-color 0.18s ease, background 0.18s ease;
}

.chip:hover {
  color: var(--accent);
  border-color: rgba(252, 60, 45, 0.35);
}

.chip.active {
  color: #fff;
  background: var(--accent);
  border-color: var(--accent);
}

.chip {
  display: inline-flex;
  align-items: center;
  height: 38px;
  padding: 0 16px;
  font-family: var(--font-heading);
  font-size: 13px;
  font-weight: 500;
  color: var(--color-foreground);
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 999px;
  transition: color 0.2s ease, border-color 0.2s ease, background 0.2s ease;
}

.chip:hover {
  color: var(--color-primary-strong, #047857);
  border-color: var(--color-primary);
}

.chip.active {
  color: var(--color-on-primary);
  background: var(--color-primary);
  border-color: var(--color-primary);
}

@media (max-width: 768px) {
  .category-grid {
    margin-bottom: 20px;
  }

  .chip {
    height: 34px;
    padding: 0 12px;
    font-size: 12px;
  }
}
</style>
