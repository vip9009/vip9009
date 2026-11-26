<script setup>
import { computed, ref, watchEffect } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { productsData } from '@/data'
import VpProductCard from '@/components/VpProductCard.vue'
import AppIcon from '@/components/AppIcon.vue'
import { allProducts, decodeEntities } from '@/utils'

const route = useRoute()
const router = useRouter()

const query = computed(() => String(route.query.q || '').trim())
const draft = ref(query.value)

const products = computed(() => {
  if (!query.value) return []
  const word = query.value.toLowerCase()
  return allProducts(productsData.sections).filter((product) => {
    const haystack = `${decodeEntities(product.title)} ${decodeEntities(product.imageAlt || '')}`.toLowerCase()
    return haystack.includes(word)
  })
})

const total = computed(() => products.value.length)

function submit() {
  const value = draft.value.trim()
  if (!value) return
  router.push({ path: '/search', query: { q: value } })
}

watchEffect(() => {
  draft.value = query.value
  document.title = query.value ? `搜索“${query.value}” - 泡泡哥雾化` : '搜索 - 泡泡哥雾化'
})
</script>

<template>
  <div class="wrapper search-page">
    <nav class="breadcrumb">
      <RouterLink to="/">首页</RouterLink>
      <span>/</span>
      <span>搜索</span>
    </nav>

    <div class="search-head">
      <h1>搜索{{ query ? `“${query}”` : '' }}</h1>
      <p v-if="query">共找到 {{ total }} 款产品</p>
      <p v-else>输入产品名、品牌或口味关键词</p>
    </div>

    <form class="inline-search" role="search" @submit.prevent="submit">
      <AppIcon name="search" :size="18" />
      <input v-model="draft" type="search" placeholder="搜索产品 / 品牌 / 口味" aria-label="搜索产品" autocomplete="off" />
      <button type="submit">搜索</button>
    </form>

    <template v-if="query">
      <div v-if="products.length" class="product-grid-3">
        <VpProductCard
          v-for="(item, index) in products"
          :key="`${item.sectionId}-${item.index}`"
          :product="item"
          :section-id="item.sectionId"
          :section-title="item.sectionTitle"
          :index="item.index"
          :eager="index < 6"
        />
      </div>

      <div v-else class="empty-state">
        <h2>没有找到“{{ query }}”相关产品</h2>
        <p>换个关键词试试，或者直接联系泡泡哥，我们帮你确认具体产品和口味。</p>
        <div class="empty-actions">
          <RouterLink class="black-btn" to="/contact">联系客服</RouterLink>
          <RouterLink class="ghost-btn" to="/">返回首页</RouterLink>
        </div>
      </div>
    </template>

    <div v-else class="empty-state">
      <h2>搜索泡泡哥雾化</h2>
      <p>可以搜品牌（悦刻、雪加、冰熊、柚子）、系列名、口数或口味。</p>
    </div>
  </div>
</template>

<style scoped>
.search-page {
  padding-top: 26px;
  padding-bottom: 50px;
}

.breadcrumb {
  display: flex;
  gap: 7px;
  padding-bottom: 20px;
  font-size: 12px;
  color: #999999;
}

.breadcrumb a:hover {
  color: var(--color-primary);
}

.search-head {
  padding-bottom: 16px;
}

.search-head h1 {
  font-size: 26px;
}

.search-head p {
  margin-top: 5px;
  font-size: 12px;
  color: #999999;
}

.inline-search {
  display: flex;
  align-items: center;
  height: 44px;
  padding-left: 12px;
  margin-bottom: 26px;
  border: 1px solid #dddddd;
}

.inline-search input {
  flex: 1;
  min-width: 0;
  height: 100%;
  padding: 0 10px;
  font-size: 13px;
  border: 0;
  outline: none;
}

.inline-search button {
  width: 92px;
  height: 100%;
  font-size: 12px;
  font-weight: 700;
  color: #ffffff;
  background: #242125;
}

.inline-search button:hover {
  background: var(--color-primary);
}

.product-grid-3 {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
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

.empty-actions {
  display: flex;
  justify-content: center;
  gap: 8px;
}

.black-btn,
.ghost-btn {
  display: inline-flex;
  align-items: center;
  height: 38px;
  padding: 0 16px;
  font-size: 12px;
  font-weight: 700;
}

.black-btn {
  color: #ffffff;
  background: #242125;
}

.ghost-btn {
  color: #555555;
  border: 1px solid #dddddd;
}

.black-btn:hover {
  background: var(--color-primary);
}

.ghost-btn:hover {
  color: var(--color-primary);
  border-color: var(--color-primary);
}

@media (max-width: 900px) {
  .product-grid-3 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
  }

  .search-head h1 {
    font-size: 22px;
  }
}
</style>
