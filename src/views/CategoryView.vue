<script setup>
import { computed, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { site, productsData } from '@/data'
import VpProductCard from '@/components/VpProductCard.vue'
import AppIcon from '@/components/AppIcon.vue'
import { filterByBrand } from '@/utils/categories'
import { decodeEntities } from '@/utils'

const route = useRoute()
const page = ref(1)
const sort = ref('default')
const keyword = ref('')
const sidebarOpen = ref(false)
const pageSize = 10

const categoryId = computed(() => String(route.params.id || ''))
const category = computed(() => site.categories[categoryId.value] || null)
const parentId = computed(() => category.value?.parent || categoryId.value)
const parentCategory = computed(() => site.categories[parentId.value] || category.value)
const isChild = computed(() => Boolean(category.value?.parent))
const sub = computed(() => String(route.query.sub || '').trim())
const brand = computed(() => String(route.query.brand || '').trim())

const sourceSection = computed(() => {
  const owner = isChild.value ? parentCategory.value : category.value
  const sectionId = owner?.section
  if (!sectionId) return null
  return productsData.sections.find((section) => section.id === sectionId) || null
})

const rawItems = computed(() => {
  if (!sourceSection.value) return []
  const section = sourceSection.value
  let products = section.products || []

  if (isChild.value) {
    products = products.filter((product) => product.subcategory === categoryId.value)
  } else if (sub.value) {
    products = products.filter((product) => product.subcategory === sub.value)
  } else if (brand.value) {
    products = filterByBrand(products, brand.value)
  }

  const search = keyword.value.trim().toLowerCase()
  if (search) {
    products = products.filter((product) =>
      decodeEntities(product.title).toLowerCase().includes(search)
    )
  }

  return products.map((product) => ({
    product,
    index: section.products.indexOf(product),
    sectionId: section.id,
    sectionTitle: section.title
  }))
})

const sortedItems = computed(() => {
  const list = [...rawItems.value]
  if (sort.value === 'price-asc') list.sort((a, b) => Number(a.product.price) - Number(b.product.price))
  if (sort.value === 'price-desc') list.sort((a, b) => Number(b.product.price) - Number(a.product.price))
  if (sort.value === 'title') list.sort((a, b) => decodeEntities(a.product.title).localeCompare(decodeEntities(b.product.title)))
  return list
})

const total = computed(() => sortedItems.value.length)
const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize)))
const pageItems = computed(() =>
  sortedItems.value.slice((page.value - 1) * pageSize, page.value * pageSize)
)

const topCategories = computed(() =>
  Object.entries(site.categories)
    .filter(([id, item]) => !item.parent && id !== 'hot' && id !== 'contact' && item.section)
    .sort((a, b) => (a[1].sort ?? 999) - (b[1].sort ?? 999))
    .map(([id, item]) => ({ id, title: item.title }))
)

const activeParentId = computed(() => parentId.value)

const siblings = computed(() => {
  const parent = site.categories[activeParentId.value]
  if (!parent?.children?.length) return []
  return parent.children
    .map((id) => [id, site.categories[id]])
    .filter(([, child]) => Boolean(child))
    .sort((a, b) => (a[1].sort ?? 999) - (b[1].sort ?? 999))
    .map(([id, child]) => ({ id, title: child.title }))
})

const title = computed(() => {
  if (!category.value) return '商品分类'
  if (isChild.value) return category.value.title
  if (sub.value) return site.categories[sub.value]?.title || category.value.title
  return category.value.title
})

const description = computed(
  () => category.value?.desc || parentCategory.value?.desc || ''
)

const rangeText = computed(() => {
  if (!total.value) return '共 0 个结果'
  const start = (page.value - 1) * pageSize + 1
  const end = Math.min(page.value * pageSize, total.value)
  return `显示 ${start}-${end} 个结果（共 ${total.value} 个结果）`
})

const pageNumbers = computed(() => {
  const count = totalPages.value
  if (count <= 7) return Array.from({ length: count }, (_, index) => index + 1)
  const start = Math.max(1, Math.min(page.value - 3, count - 6))
  return Array.from({ length: 7 }, (_, index) => start + index)
})

watch(
  () => [route.fullPath, sort.value, keyword.value],
  () => {
    page.value = 1
  }
)

watch(
  () => route.fullPath,
  () => {
    sidebarOpen.value = false
  }
)
</script>

<template>
  <div class="wrapper category-page">
    <div class="category-head">
      <nav class="breadcrumb">
        <RouterLink to="/">首页</RouterLink>
        <span>/</span>
        <RouterLink to="/category/disposables">电子雾化</RouterLink>
        <span>/</span>
        <span>{{ title }}</span>
      </nav>

      <div class="category-tools">
        <button class="filter-toggle" type="button" @click="sidebarOpen = !sidebarOpen">
          <AppIcon name="menu" :size="16" />
          筛选
        </button>
        <span class="result-count">{{ rangeText }}</span>
        <select v-model="sort" aria-label="产品排序">
          <option value="default">默认产品排序</option>
          <option value="price-asc">价格从低到高</option>
          <option value="price-desc">价格从高到低</option>
          <option value="title">按名称排序</option>
        </select>
      </div>
    </div>

    <div class="category-layout">
      <aside class="sidebar" :class="{ open: sidebarOpen }">
        <form class="side-search" @submit.prevent>
          <input v-model="keyword" type="search" placeholder="搜索..." aria-label="分类内搜索" />
          <button type="button" aria-label="搜索"><AppIcon name="search" :size="17" /></button>
        </form>

        <h2>产品类别</h2>
        <div class="side-parent">
          <span>电子雾化</span>
          <AppIcon name="chevron-down" :size="14" />
        </div>
        <div class="side-cats">
          <RouterLink
            v-for="item in topCategories"
            :key="item.id"
            class="side-link side-link-child"
            :class="{ active: item.id === activeParentId }"
            :to="`/category/${item.id}`"
          >
            {{ item.title }}
          </RouterLink>
        </div>
      </aside>

      <section class="category-content">
        <h1 class="sr-only">{{ title }}</h1>

        <div v-if="pageItems.length" class="product-grid-3">
          <VpProductCard
            v-for="(item, index) in pageItems"
            :key="`${item.sectionId}-${item.index}`"
            :product="item.product"
            :section-id="item.sectionId"
            :section-title="item.sectionTitle"
            :index="item.index"
            :eager="index < 6"
            bordered
          />
        </div>

        <div v-else class="empty-state">
          <h2>商品正在整理中</h2>
          <p>该分类暂未上架可展示的商品。加泡泡哥微信获取最新款式、口味与报价。</p>
          <RouterLink class="black-btn" to="/contact">联系客服</RouterLink>
        </div>

        <nav v-if="totalPages > 1" class="pagination" aria-label="分页">
          <button type="button" :disabled="page === 1" @click="page -= 1">上一页</button>
          <button
            v-for="number in pageNumbers"
            :key="number"
            type="button"
            :class="{ active: page === number }"
            @click="page = number"
          >
            {{ number }}
          </button>
          <button type="button" :disabled="page === totalPages" @click="page += 1">下一页</button>
        </nav>
      </section>
    </div>
  </div>
</template>

<style scoped>
.category-page {
  padding-top: 25px;
  padding-bottom: 50px;
}

.category-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding: 0;
  margin-bottom: 28px;
}

.breadcrumb {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  font-size: 16px;
  color: #777777;
}

.breadcrumb a:hover {
  color: var(--color-primary);
}

.breadcrumb span:last-child {
  color: #242125;
  font-weight: 700;
}

.category-tools {
  display: flex;
  align-items: center;
  gap: 18px;
}

.result-count {
  font-size: 14.4px;
  color: #777777;
}

.category-tools select {
  height: 39px;
  padding: 0 30px 0 12px;
  font-size: 14.4px;
  color: #333333;
  background: #ffffff;
  border: 1px solid #dddddd;
  border-radius: 0;
}

.category-layout {
  display: grid;
  grid-template-columns: 240px minmax(0, 1fr);
  gap: 20px;
  padding-top: 0;
}

.side-search {
  display: flex;
  height: 38px;
  margin-bottom: 20px;
  border: 1px solid #dddddd;
}

.side-search input {
  flex: 1;
  min-width: 0;
  padding: 0 10px;
  font-size: 14px;
  border: 0;
  outline: none;
}

.side-search button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  color: #ffffff;
  background: #000000;
}

.sidebar h2 {
  position: relative;
  padding-bottom: 10px;
  margin-bottom: 4px;
  font-size: 16px;
  font-weight: 400;
  border: 0;
}

.sidebar h2::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 22px;
  height: 1px;
  background: #dddddd;
}

.side-parent {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 9px 0;
  font-size: 14px;
  color: #555555;
}

.side-cats {
  padding-left: 20px;
}

.side-group {
  padding: 4px 0;
}

.side-link {
  display: block;
  padding: 5px 0;
  font-size: 13px;
  color: #666666;
}

.side-link:hover {
  color: var(--color-primary);
}

.side-link.active {
  font-weight: 700;
  color: #242125;
}

.side-children {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 4px 0 6px 16px;
  border-left: 1px solid #eeeeee;
}

.side-children a {
  font-size: 13px;
  color: #888888;
}

.side-children a:hover,
.side-children a.active {
  color: var(--color-primary);
}

.filter-toggle {
  display: none;
  align-items: center;
  gap: 8px;
  height: auto;
  padding: 0;
  font-size: 16px;
  color: #333333;
  white-space: nowrap;
  border: 0;
}

.product-grid-3 {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0;
  width: calc(100% + 10px);
}

.empty-state {
  padding: 70px 20px;
  text-align: center;
  background: #fafafa;
  border: 1px solid #eeeeee;
}

.empty-state h2 {
  margin-bottom: 8px;
  font-size: 18px;
}

.empty-state p {
  margin-bottom: 16px;
  font-size: 12px;
  color: #888888;
}

.black-btn {
  display: inline-flex;
  align-items: center;
  height: 40px;
  padding: 0 20px;
  font-size: 12px;
  font-weight: 700;
  color: #ffffff;
  background: #242125;
}

.black-btn:hover {
  background: var(--color-primary);
}

.pagination {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding-top: 30px;
}

.pagination button {
  min-width: 32px;
  height: 32px;
  padding: 0 9px;
  font-size: 11px;
  color: #666666;
  border: 1px solid #dddddd;
}

.pagination button:hover {
  color: var(--color-primary);
  border-color: var(--color-primary);
}

.pagination button.active {
  color: #ffffff;
  background: #242125;
  border-color: #242125;
}

.pagination button:disabled {
  color: #cccccc;
  cursor: not-allowed;
}

@media (max-width: 900px) {
  .category-page {
    padding-top: 12px;
  }

  .category-head {
    flex-direction: column;
    align-items: center;
    gap: 14px;
    margin-bottom: 24px;
  }

  .breadcrumb {
    justify-content: center;
    font-size: 16px;
  }

  .category-tools {
    flex-direction: column;
    gap: 12px;
    width: 100%;
    justify-content: center;
  }

  .result-count {
    display: none;
  }

  .category-tools select {
    width: 148px;
    height: 40px;
    font-size: 14px;
  }

  .category-layout {
    grid-template-columns: minmax(0, 1fr);
    gap: 0;
    padding-top: 18px;
  }

  .sidebar {
    display: none;
  }

  .sidebar.open {
    display: block;
    padding: 10px;
    margin-bottom: 12px;
    background: #ffffff;
    border: 1px solid #eeeeee;
  }

  .filter-toggle {
    display: inline-flex;
  }

  .product-grid-3 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0;
    width: auto;
    margin: 0 -10px;
  }
}
</style>
