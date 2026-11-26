<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import AppIcon from '@/components/AppIcon.vue'
import { asset, decodeEntities, productRoute } from '@/utils'

const props = defineProps({
  product: { type: Object, required: true },
  sectionId: { type: String, required: true },
  index: { type: Number, required: true },
  eager: { type: Boolean, default: false }
})

const title = computed(() => decodeEntities(props.product.title))

const brand = computed(() => {
  if (props.product.brand) return props.product.brand
  const text = title.value.toLowerCase()
  const brands = [
    ['悦刻', ['悦刻', 'relx']],
    ['雪加', ['雪加', 'snowplus']],
    ['冰熊', ['冰熊', 'zgar']],
    ['柚子', ['柚子', 'yooz']],
    ['崧', ['song', '崧']],
    ['ELFBAR', ['elfbar']],
    ['Bubblemon', ['bubblemon']],
    ['ICEMAX', ['icemax']]
  ]
  const hit = brands.find(([, keys]) => keys.some((key) => text.includes(key)))
  return hit ? hit[0] : ''
})

const tags = computed(() => {
  const list = []
  if (props.product.spec) list.push(props.product.spec)
  const puffs = title.value.match(/(\d{3,6})\s*口/)
  if (puffs) list.push(`${puffs[1]} 口`)
  if (/口味/.test(title.value)) list.push('多口味')
  return list.slice(0, 2)
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
      <div v-if="brand || tags.length" class="meta-row">
        <span v-if="brand" class="brand-chip">{{ brand }}</span>
        <span v-for="tag in tags" :key="tag" class="tag">{{ tag }}</span>
      </div>

      <h2 class="product-title">{{ title }}</h2>

      <div class="price-row">
        <span class="price">￥{{ product.price }}</span>
        <span class="card-action">
          看详情
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
  border-radius: 18px;
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
  aspect-ratio: 4 / 5;
  margin: 10px 10px 0;
  overflow: hidden;
  background: #f7f3ea;
  border-radius: 12px;
}

.thumb img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 8px;
  transition: transform 0.3s ease;
}

.product-card:hover .thumb img {
  transform: scale(1.04);
}

.product-body {
  display: flex;
  flex: 1;
  flex-direction: column;
  padding: 12px 14px 14px;
}

.meta-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
  margin-bottom: 8px;
}

.brand-chip {
  display: inline-flex;
  align-items: center;
  height: 20px;
  padding: 0 8px;
  font-family: var(--font-heading);
  font-size: 10px;
  font-weight: 600;
  color: #ffffff;
  background: var(--color-primary);
  border-radius: 999px;
}

.tag {
  display: inline-flex;
  align-items: center;
  height: 20px;
  padding: 0 7px;
  font-size: 10px;
  font-weight: 600;
  color: var(--color-muted-foreground);
  background: var(--color-muted);
  border-radius: 999px;
}

.product-title {
  display: -webkit-box;
  min-height: 42px;
  margin: 0 0 10px;
  overflow: hidden;
  font-family: var(--font-heading);
  font-size: 15px;
  font-weight: 600;
  line-height: 21px;
  color: var(--color-foreground);
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

.price-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding-top: 10px;
  margin-top: auto;
  border-top: 1px dashed var(--color-border);
}

.price {
  font-family: var(--font-heading);
  font-size: 19px;
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
    padding: 5px;
  }

  .product-body {
    padding: 9px 10px 10px;
  }

  .meta-row {
    gap: 4px;
    margin-bottom: 6px;
  }

  .brand-chip,
  .tag {
    height: 18px;
    font-size: 9px;
  }

  .product-title {
    min-height: 38px;
    margin-bottom: 7px;
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
