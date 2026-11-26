<script setup>
import { computed, ref, watchEffect } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { productsData } from '@/data'
import ProductCard from '@/components/ProductCard.vue'
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
    const haystack = `${decodeEntities(product.title)} ${decodeEntities(product.imageAlt)}`.toLowerCase()
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
  <div class="search-page">
    <div class="wrapper">
      <nav class="breadcrumb" aria-label="面包屑">
        <RouterLink to="/">首页</RouterLink>
        <span class="sep">/</span>
        <span>搜索</span>
      </nav>

      <div class="page-head">
        <div>
          <h1 class="page-title">搜索{{ query ? `“${query}”` : '' }}</h1>
          <p class="page-subtitle">
            <template v-if="query">共找到 {{ total }} 款产品</template>
            <template v-else>输入关键词搜索产品</template>
          </p>
        </div>
      </div>

      <form class="inline-search" @submit.prevent="submit">
        <AppIcon name="search" :size="18" />
        <input v-model="draft" type="search" placeholder="搜索产品名称" aria-label="搜索产品名称" autocomplete="off" />
        <button type="submit">搜索</button>
      </form>

      <template v-if="query">
        <template v-if="products.length">
          <section class="result-block">
            <h2 class="result-title">产品 <span>{{ products.length }}</span></h2>
            <div class="product-grid">
              <ProductCard
                v-for="item in products"
                :key="`${item.sectionId}-${item.index}`"
                :product="item"
                :section-id="item.sectionId"
                :index="item.index"
              />
            </div>
          </section>
        </template>

        <div v-else class="empty-state">
          <h3>没有找到“{{ query }}”相关产品</h3>
          <p>换个关键词试试，或者直接联系客服，我们会帮你确认具体产品。</p>
          <div class="empty-actions">
            <RouterLink class="btn btn-primary" to="/contact">联系客服</RouterLink>
            <RouterLink class="btn btn-ghost" to="/">返回首页</RouterLink>
          </div>
        </div>
      </template>

      <div v-else class="empty-state">
        <h3>搜索泡泡哥雾化</h3>
        <p>可以搜索品牌、产品名称或口味关键词，例如“悦刻”“积木”“冰熊”。</p>
        <div class="empty-actions">
          <RouterLink class="btn btn-primary" to="/category/hot">浏览热门产品</RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.inline-search {
  display: flex;
  align-items: center;
  gap: 10px;
  height: 48px;
  padding: 0 6px 0 16px;
  margin-bottom: 24px;
  color: #999;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(17, 58, 93, 0.05);
}

.inline-search input {
  flex: 1;
  min-width: 0;
  height: 100%;
  font-size: 14px;
  background: none;
  border: 0;
  outline: none;
}

.inline-search button {
  height: 36px;
  padding: 0 20px;
  font-size: 13px;
  color: #fff;
  background: var(--accent);
  border-radius: 4px;
}

.result-block {
  margin-bottom: 24px;
}

.result-title {
  margin-bottom: 14px;
  font-size: 20px;
  font-weight: 600;
}

.result-title span {
  font-size: 12px;
  font-weight: 400;
  color: #9aa0a6;
}

@media (max-width: 768px) {
  .inline-search {
    margin-bottom: 12px;
  }

  .result-block {
    margin-bottom: 12px;
  }

  .result-title {
    margin-bottom: 10px;
    font-size: 17px;
  }
}

/* UI UX Pro Max design system overrides */
.inline-search {
  height: 56px;
  padding: 0 8px 0 18px;
  margin-bottom: 32px;
  color: var(--color-muted-foreground);
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  box-shadow: var(--shadow-card);
}

.inline-search input {
  color: var(--color-foreground);
  font-size: 15px;
}

.inline-search button {
  height: 40px;
  padding: 0 22px;
  font-family: var(--font-heading);
  font-weight: 600;
  color: var(--color-on-accent);
  background: var(--color-accent);
  border-radius: 10px;
}

.inline-search button:hover {
  background: #f97316;
}

.result-block {
  margin-bottom: 40px;
}

.result-title {
  margin-bottom: 18px;
  font-family: var(--font-heading);
  font-size: clamp(24px, 2.6vw, 32px);
  font-weight: 600;
  color: var(--color-foreground);
}

.result-title span {
  display: inline-flex;
  align-items: center;
  height: 24px;
  padding: 0 9px;
  margin-left: 6px;
  font-family: var(--font-heading);
  font-size: 12px;
  font-weight: 600;
  color: var(--color-on-primary);
  background: var(--color-primary);
  border-radius: 999px;
}

@media (max-width: 768px) {
  .inline-search {
    height: 50px;
    padding-left: 14px;
    margin-bottom: 20px;
    border-radius: 14px;
  }

  .inline-search button {
    height: 36px;
    padding: 0 16px;
  }

  .result-block {
    margin-bottom: 24px;
  }

  .result-title {
    font-size: 22px;
  }
}
</style>
