<script setup>
import { RouterLink } from 'vue-router'
import AppIcon from '@/components/AppIcon.vue'
import { asset, decodeEntities, productRoute } from '@/utils'

defineProps({
  product: { type: Object, required: true },
  sectionId: { type: String, required: true },
  index: { type: Number, required: true },
  eager: { type: Boolean, default: false }
})
</script>

<template>
  <RouterLink class="product-card" :to="productRoute(sectionId, index)">
    <div class="thumb img-placeholder">
      <img
        :src="asset(product.localImage)"
        alt=""
        :loading="eager ? 'eager' : 'lazy'"
        decoding="async"
      />
    </div>

    <div class="product-body">
      <h2 class="product-title">{{ decodeEntities(product.title) }}</h2>

      <div class="price-row">
        <span class="price">￥{{ product.price }}</span>
        <span class="card-action">
          查看详情
          <AppIcon name="arrow-right" :size="14" />
        </span>
      </div>
    </div>
  </RouterLink>
</template>

<style scoped>
.product-card {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 20px;
  box-shadow: var(--shadow-card);
  transition: transform 0.24s ease, box-shadow 0.24s ease, border-color 0.24s ease;
}

.product-card:hover {
  transform: translateY(-6px);
  border-color: var(--color-primary);
  box-shadow: var(--shadow-hover);
}

.thumb {
  position: relative;
  aspect-ratio: 4 / 3;
  margin: 8px 8px 0;
  overflow: hidden;
  background: #f7fffb;
  border-radius: 12px;
}

.thumb img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 4px;
  transition: transform 0.3s ease;
}

.product-card:hover .thumb img {
  transform: scale(1.04);
}

.product-body {
  display: flex;
  flex: 1;
  flex-direction: column;
  padding: 12px;
}

.product-title {
  display: -webkit-box;
  min-height: 40px;
  margin: 0 0 8px;
  overflow: hidden;
  font-family: var(--font-heading);
  font-size: 15px;
  font-weight: 500;
  line-height: 20px;
  color: var(--color-foreground);
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

.price-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding-top: 9px;
  margin-top: auto;
  border-top: 1px dashed var(--color-border);
}

.price {
  font-family: var(--font-heading);
  font-size: 18px;
  font-weight: 700;
  line-height: 1.2;
  color: var(--color-primary);
}

.card-action {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  font-weight: 600;
  color: var(--color-muted-foreground);
  transition: color 0.2s ease;
}

.product-card:hover .card-action {
  color: var(--color-primary-strong);
}

@media (max-width: 768px) {
  .product-card {
    border-radius: 14px;
  }

  .thumb {
    margin: 6px 6px 0;
    border-radius: 10px;
  }

  .thumb img {
    padding: 3px;
  }

  .product-body {
    padding: 10px;
  }

  .product-title {
    min-height: 38px;
    margin-bottom: 6px;
    font-size: 14px;
    line-height: 19px;
  }

  .price-row {
    padding-top: 8px;
  }

  .price {
    font-size: 16px;
  }

  .card-action {
    font-size: 10px;
  }
}
</style>
