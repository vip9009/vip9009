<script setup>
import { computed, watchEffect } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { site, productsData } from '@/data'
import ProductCard from '@/components/ProductCard.vue'
import { filterByBrand } from '@/utils/categories'

const route = useRoute()

function bySort(a, b) {
  return (a[1].sort ?? 999) - (b[1].sort ?? 999)
}

const categoryId = computed(() => String(route.params.id || ''))
const category = computed(() => site.categories[categoryId.value] || null)
const isChild = computed(() => Boolean(category.value?.parent))
const parentId = computed(() => category.value?.parent || categoryId.value)
const parentCategory = computed(() => site.categories[parentId.value] || category.value)
const sub = computed(() => String(route.query.sub || '').trim())
const subCategory = computed(() => {
  const id = sub.value
  const item = id ? site.categories[id] : null
  return item ? { id, ...item } : null
})
const brand = computed(() => String(route.query.brand || '').trim())

const sourceSection = computed(() => {
  const owner = isChild.value ? parentCategory.value : category.value
  const sectionId = owner?.section
  if (!sectionId) return null
  return productsData.sections.find((section) => section.id === sectionId) || null
})

const items = computed(() => {
  if (!sourceSection.value) return []
  const section = sourceSection.value
  let products = section.products

  if (isChild.value) {
    products = products.filter((product) => product.subcategory === categoryId.value)
  } else if (subCategory.value) {
    products = products.filter((product) => product.subcategory === subCategory.value.id)
  } else if (brand.value) {
    products = filterByBrand(products, brand.value)
  }

  return products.map((product) => ({
    product,
    index: section.products.indexOf(product),
    sectionId: section.id
  }))
})

const title = computed(() => {
  if (!category.value) return '商品分类'
  if (isChild.value) return category.value.title
  if (subCategory.value) return subCategory.value.title
  if (brand.value) return `${brand.value}${category.value.title}`
  return category.value.title
})

const description = computed(() => {
  if (!category.value) return ''
  return category.value.desc || parentCategory.value?.desc || ''
})

const topEntries = computed(() =>
  Object.entries(site.categories)
    .filter(([id, item]) => !item.parent && id !== 'hot' && item.section)
    .sort(bySort)
)

const childChips = computed(() => {
  const owner = parentCategory.value
  if (!owner?.children?.length) return []
  const list = owner.children
    .map((childId) => [childId, site.categories[childId]])
    .filter(([, child]) => Boolean(child))
    .sort(bySort)
    .map(([childId, child]) => ({
      id: childId,
      title: child.title,
      to: `/category/${parentId.value}?sub=${childId}`
    }))
  return [{ id: '', title: '全部', to: `/category/${parentId.value}` }, ...list]
})

const topChips = computed(() =>
  topEntries.value.map(([id, item]) => ({ id, title: item.title, to: `/category/${id}` }))
)

const chips = computed(() => (childChips.value.length ? childChips.value : topChips.value))

const activeSub = computed(() => (isChild.value ? categoryId.value : subCategory.value?.id || ''))

function chipActive(chip) {
  if (childChips.value.length) {
    return activeSub.value ? chip.id === activeSub.value : chip.id === ''
  }
  return chip.id === categoryId.value
}

const crumbParent = computed(() => {
  if (isChild.value) return parentCategory.value
  if (subCategory.value) return category.value
  return null
})

const crumbParentId = computed(() => (isChild.value ? parentId.value : categoryId.value))
const crumbCurrent = computed(() => {
  if (isChild.value) return category.value
  if (subCategory.value) return subCategory.value
  return category.value
})

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
        <template v-if="crumbParent">
          <RouterLink :to="`/category/${crumbParentId}`">{{ crumbParent.title }}</RouterLink>
          <span class="sep">/</span>
        </template>
        <span>{{ crumbCurrent ? crumbCurrent.title : '商品分类' }}</span>
        <template v-if="brand && !isChild && !subCategory">
          <span class="sep">/</span>
          <span>{{ brand }}</span>
        </template>
      </nav>

      <template v-if="category">
        <div class="page-head">
          <div>
            <h1 class="page-title">{{ title }}</h1>
            <p class="page-subtitle">{{ description }} · 共 {{ items.length }} 件商品</p>
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
          <h3>{{ title }}商品正在整理中</h3>
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
            :key="chip.to"
            class="chip"
            :class="{ active: chipActive(chip) }"
            :to="chip.to"
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
