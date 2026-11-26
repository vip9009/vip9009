<script setup>
import { computed, ref } from 'vue'
import { RouterLink } from 'vue-router'
import AppIcon from '@/components/AppIcon.vue'
import { useCart } from '@/stores/cart'
import { useWishlist } from '@/stores/wishlist'
import { site } from '@/data'
import { asset, decodeEntities, detectBrand, formatPrice, productRoute } from '@/utils'

const props = defineProps({
  product: { type: Object, required: true },
  sectionId: { type: String, required: true },
  sectionTitle: { type: String, default: '' },
  index: { type: Number, required: true },
  eager: { type: Boolean, default: false }
})

const cart = useCart()
const wishlist = useWishlist()
const option = ref('')

const title = computed(() => decodeEntities(props.product.title))
const brand = computed(() => detectBrand(props.product))
const brandLogo = computed(() => site.brandLogos?.[brand.value] || '')
const route = computed(() => productRoute(props.sectionId, props.index))
const image = computed(() => asset(props.product.localImage))
const badges = computed(() => {
  const list = Array.isArray(props.product.badges) ? [...props.product.badges] : []
  if (props.product.recommend && !list.includes('店长推荐')) list.push('店长推荐')
  return list.slice(0, 4)
})
const isHot = computed(
  () => props.product.hot === true || badges.value.some((badge) => String(badge).toUpperCase() === 'HOT')
)
const stock = computed(() => props.product.stock !== false)
const options = computed(() => {
  const list = Array.isArray(props.product.options) ? props.product.options : []
  return list
    .map((entry) =>
      typeof entry === 'string'
        ? { label: entry, price: props.product.price }
        : { label: entry.label || entry.name || '', price: entry.price ?? props.product.price }
    )
    .filter((entry) => entry.label)
})
const priceLabel = computed(() => {
  const price = Number(props.product.price)
  const max = Number(props.product.priceMax)
  if (Number.isFinite(max) && max > price) {
    return `${formatPrice(price)} – ${formatPrice(max)}`
  }
  return formatPrice(props.product.price)
})
const activePrice = computed(() => {
  const match = options.value.find((entry) => entry.label === option.value)
  return match ? match.price : props.product.price
})

function addToCart() {
  if (!stock.value) return
  if (options.value.length && !option.value) {
    window.alert('请先选择口味/规格。')
    return
  }
  cart.add({
    sectionId: props.sectionId,
    index: props.index,
    title: title.value,
    price: activePrice.value,
    image: image.value,
    option: option.value
  })
}

function toggleWishlist() {
  wishlist.toggle({
    sectionId: props.sectionId,
    index: props.index,
    title: title.value,
    price: props.product.price,
    image: image.value
  })
}
</script>

<template>
  <article class="vp-card" :class="{ 'is-sold': !stock }">
    <div class="card-top">
      <img v-if="brandLogo" class="card-brand-logo" :src="asset(brandLogo)" :alt="brand" />
      <span v-else class="card-brand">{{ brand }}</span>
      <div class="card-badges">
        <span v-for="badge in badges" :key="badge" class="card-badge">{{ badge }}</span>
      </div>
    </div>

    <RouterLink class="card-image" :to="route">
      <img :src="image" :alt="title" :loading="eager ? 'eager' : 'lazy'" decoding="async" />
    </RouterLink>

    <button
      class="card-wish"
      type="button"
      :class="{ active: wishlist.has(sectionId, index) }"
      aria-label="收藏"
      @click="toggleWishlist"
    >
      <AppIcon name="heart" :size="16" />
    </button>

    <span v-if="!stock" class="card-sold">无货</span>
    <span v-if="isHot" class="card-hot">HOT</span>

    <div class="card-body">
      <span class="card-cat">{{ sectionTitle }}</span>
      <RouterLink class="card-title" :to="route">{{ title }}</RouterLink>
      <div class="card-price">{{ priceLabel }}</div>

      <template v-if="stock">
        <div v-if="options.length" class="card-buy">
          <select v-model="option" aria-label="选择口味">
            <option value="">选择口味</option>
            <option v-for="entry in options" :key="entry.label" :value="entry.label">
              {{ entry.label }}
            </option>
          </select>
          <button type="button" @click="addToCart">GET</button>
        </div>
        <div v-else class="card-buy">
          <RouterLink class="card-view" :to="route">查看详情</RouterLink>
          <button type="button" @click="addToCart">GET</button>
        </div>
      </template>
      <button v-else class="card-disabled" type="button" disabled>无货</button>
    </div>
  </article>
</template>

<style scoped>
.vp-card {
  position: relative;
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 14px;
  background: #ffffff;
  border: 1px solid #e5e5e5;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.vp-card:hover {
  border-color: #cfcfcf;
  box-shadow: 0 14px 34px rgba(0, 0, 0, 0.08);
}

.card-top {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  min-height: 22px;
  gap: 8px;
}

.card-brand {
  overflow: hidden;
  max-width: 45%;
  font-family: var(--font-heading);
  font-size: 10px;
  font-weight: 900;
  letter-spacing: 0.08em;
  color: #242125;
  text-transform: uppercase;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.card-brand-logo {
  display: block;
  max-width: 72px;
  max-height: 22px;
  object-fit: contain;
  object-position: left center;
}

.card-badges {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 4px;
}

.card-badge {
  display: inline-flex;
  align-items: center;
  height: 18px;
  padding: 0 6px;
  font-size: 9px;
  color: #ffffff;
  background: var(--color-primary);
}

.card-badge:nth-child(2n) {
  background: #242125;
}

.card-image {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 245px;
  margin: 4px 0 6px;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 10px;
  filter: drop-shadow(0 14px 12px rgba(0, 0, 0, 0.08));
  transition: transform 0.25s ease;
}

.vp-card:hover .card-image img {
  transform: scale(1.035);
}

.card-wish {
  position: absolute;
  top: 40px;
  right: 12px;
  z-index: 3;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  color: #bbbbbb;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #eeeeee;
  border-radius: 50%;
  opacity: 0;
  transition: opacity 0.18s ease, color 0.18s ease;
}

.vp-card:hover .card-wish,
.card-wish.active {
  opacity: 1;
}

.card-wish.active {
  color: var(--color-primary);
}

.card-sold {
  position: absolute;
  top: 44%;
  left: 50%;
  z-index: 2;
  padding: 2px 10px;
  font-size: 14px;
  color: #999999;
  background: rgba(255, 255, 255, 0.86);
  border: 1px solid #dddddd;
  transform: translate(-50%, -50%) rotate(-8deg);
}

.card-hot {
  position: absolute;
  top: 50%;
  right: 12px;
  z-index: 2;
  padding: 2px 7px;
  font-family: var(--font-heading);
  font-size: 9px;
  font-weight: 900;
  color: #ffffff;
  background: #242125;
}

.card-body {
  display: flex;
  flex: 1;
  flex-direction: column;
  text-align: center;
}

.card-cat {
  font-size: 11px;
  color: #aaaaaa;
}

.card-title {
  display: -webkit-box;
  min-height: 40px;
  margin: 4px 0 5px;
  overflow: hidden;
  font-size: 14px;
  line-height: 20px;
  color: #3372a2;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

.card-title:hover {
  color: var(--color-primary);
}

.card-price {
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 700;
  color: #242125;
}

.card-buy {
  display: grid;
  grid-template-columns: 1fr 74px;
  gap: 6px;
  margin-top: auto;
}

.card-buy select {
  width: 100%;
  height: 34px;
  padding: 0 8px;
  font-size: 11px;
  color: #555555;
  background: #ffffff;
  border: 1px solid #dddddd;
  border-radius: 2px;
}

.card-buy button,
.card-view {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 34px;
  font-size: 11px;
  font-weight: 700;
  color: #d9a8bf;
  background: #fafafa;
  border: 1px solid #f0f0f0;
  transition: background 0.18s ease, color 0.18s ease;
}

.card-buy button:hover,
.card-view:hover {
  color: #ffffff;
  background: var(--color-primary);
  border-color: var(--color-primary);
}

.card-view {
  grid-column: 1;
}

.card-buy button:only-child {
  grid-column: 1 / -1;
}

.card-disabled {
  width: 100%;
  height: 34px;
  margin-top: auto;
  font-size: 11px;
  color: #cccccc;
  background: #fafafa;
  border: 1px solid #f0f0f0;
}

@media (max-width: 900px) {
  .vp-card {
    padding: 9px;
  }

  .card-image {
    height: 170px;
    margin: 2px 0 4px;
  }

  .card-image img {
    padding: 6px;
  }

  .card-title {
    min-height: 36px;
    font-size: 12px;
    line-height: 18px;
  }

  .card-price {
    font-size: 13px;
  }

  .card-buy {
    grid-template-columns: 1fr;
    gap: 4px;
  }

  .card-buy select,
  .card-buy button,
  .card-view {
    height: 30px;
    font-size: 10px;
  }

  .card-wish {
    display: none;
  }
}
</style>
