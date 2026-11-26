<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { productsData } from '@/data'
import VpProductCard from '@/components/VpProductCard.vue'
import { useWishlist } from '@/stores/wishlist'

const wishlist = useWishlist()

const items = computed(() =>
  wishlist.items
    .map((item) => {
      const section = productsData.sections.find((entry) => entry.id === item.sectionId)
      const product = section?.products?.[item.index]
      if (!section || !product) return null
      return {
        product,
        sectionId: section.id,
        sectionTitle: section.title,
        index: item.index
      }
    })
    .filter(Boolean)
)
</script>

<template>
  <div class="wrapper page">
    <nav class="breadcrumb">
      <RouterLink to="/">首页</RouterLink>
      <span>/</span>
      <span>我的收藏</span>
    </nav>

    <h1>我的收藏</h1>

    <div v-if="items.length" class="grid">
      <VpProductCard
        v-for="item in items"
        :key="`${item.sectionId}-${item.index}`"
        :product="item.product"
        :section-id="item.sectionId"
        :section-title="item.sectionTitle"
        :index="item.index"
      />
    </div>

    <div v-else class="empty">
      <p>还没有收藏任何商品。</p>
      <RouterLink class="black-btn" to="/category/hot">去逛逛</RouterLink>
    </div>
  </div>
</template>

<style scoped>
.page {
  padding-top: 26px;
  padding-bottom: 40px;
}

.breadcrumb {
  display: flex;
  gap: 8px;
  padding-bottom: 22px;
  font-size: 12px;
  color: #999999;
}

.breadcrumb a:hover {
  color: var(--color-primary);
}

h1 {
  margin-bottom: 22px;
  font-size: 26px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.empty {
  padding: 70px 20px;
  text-align: center;
}

.empty p {
  margin-bottom: 16px;
  font-size: 14px;
  color: #777777;
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

@media (max-width: 900px) {
  .grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
  }
}
</style>
