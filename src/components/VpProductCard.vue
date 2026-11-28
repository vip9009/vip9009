<script setup>
import { computed, ref, watch } from 'vue'
import { RouterLink } from 'vue-router'
import { useCart } from '@/stores/cart'
import { site } from '@/data'
import { asset, decodeEntities, detectBrand, formatPrice, productRoute } from '@/utils'
import { leftTagStyle } from '@/utils/tags'

const props = defineProps({
  product: { type: Object, required: true },
  sectionId: { type: String, required: true },
  sectionTitle: { type: String, default: '' },
  index: { type: Number, required: true },
  eager: { type: Boolean, default: false },
  bordered: { type: Boolean, default: false }
})

const cart = useCart()
const option = ref('')
const added = ref(false)
let addedTimer = null

watch(
  () => props.product,
  () => {
    option.value = ''
    added.value = false
    clearTimeout(addedTimer)
  }
)

const title = computed(() => decodeEntities(props.product.title))
const brand = computed(() => detectBrand(props.product))
const brandLogo = computed(() => site.brandLogos?.[brand.value] || '')
const route = computed(() => productRoute(props.sectionId, props.index))
const image = computed(() => asset(props.product.localImage))
const topTags = computed(() =>
  (Array.isArray(props.product.topTags) ? props.product.topTags : [])
    .filter((tag) => String(tag || '').trim() && String(tag).toUpperCase() !== 'HOT')
    .slice(0, 4)
)
const leftTags = computed(() =>
  (Array.isArray(props.product.leftTags) ? props.product.leftTags : [])
    .filter((tag) => String(tag || '').trim() && String(tag).toUpperCase() !== 'HOT')
    .slice(0, 4)
)
const isHot = computed(() => props.product.hot === true)
const stock = computed(() => props.product.stock !== false)
const options = computed(() => {
  const list = Array.isArray(props.product.options) ? props.product.options : []
  return list
    .map((entry) =>
      typeof entry === 'string'
        ? { label: entry, price: props.product.price, stock: true }
        : {
            label: entry.label || entry.name || '',
            price: entry.price ?? props.product.price,
            stock: entry.stock !== false
          }
    )
    .filter((entry) => entry.label)
})
const selectedOption = computed(() =>
  options.value.find((entry) => entry.label === option.value)
)
const priceLabel = computed(() => {
  if (selectedOption.value) return formatPrice(selectedOption.value.price)
  const price = Number(props.product.price)
  const max = Number(props.product.priceMax)
  if (Number.isFinite(max) && max > price) {
    return `${formatPrice(price)} – ${formatPrice(max)}`
  }
  return formatPrice(props.product.price)
})
const activePrice = computed(() => selectedOption.value?.price ?? props.product.price)
const canAdd = computed(
  () =>
    stock.value &&
    (!options.value.length || Boolean(option.value)) &&
    (selectedOption.value ? selectedOption.value.stock : true)
)
const getImage = computed(() => {
  if (added.value) return asset('/images/ui/get-success.webp')
  if (canAdd.value) return asset('/images/ui/get-active.webp')
  return asset('/images/ui/get-default.webp')
})

function addToCart() {
  if (!canAdd.value) return
  cart.add({
    sectionId: props.sectionId,
    index: props.index,
    title: title.value,
    price: activePrice.value,
    image: image.value,
    option: option.value
  })
  added.value = true
  clearTimeout(addedTimer)
  addedTimer = setTimeout(() => {
    added.value = false
  }, 1600)
}

</script>

<template>
  <article class="vp-card" :class="{ 'is-sold': !stock, 'is-bordered': bordered }">
    <div class="card-top">
      <img v-if="brandLogo" class="card-brand-logo" :src="asset(brandLogo)" :alt="brand" />
      <span v-else class="card-brand">{{ brand }}</span>
    </div>

    <RouterLink class="card-image" :to="route">
      <img :src="image" :alt="title" :loading="eager ? 'eager' : 'lazy'" decoding="async" />
      <div v-if="topTags.length" class="card-badges">
        <span v-for="badge in topTags" :key="badge" class="card-badge">{{ badge }}</span>
      </div>
      <span v-if="isHot" class="card-hot">HOT</span>
      <div v-if="leftTags.length" class="card-feature-tags">
        <span v-for="tag in leftTags" :key="tag" :style="leftTagStyle(tag)">{{ tag }}</span>
      </div>
      <span v-if="!stock" class="card-sold">无货</span>
    </RouterLink>

    <div class="card-body">
      <span class="card-cat">{{ sectionTitle }}</span>
      <RouterLink class="card-title" :to="route">{{ title }}</RouterLink>
      <div class="card-price">{{ priceLabel }}</div>

      <template v-if="stock">
        <div v-if="options.length" class="card-buy">
          <select v-model="option" aria-label="选择口味">
            <option value="">SELECT</option>
            <option v-for="entry in options" :key="entry.label" :value="entry.label">
              {{ entry.label }}{{ entry.stock === false ? '（无货）' : '' }}
            </option>
          </select>
          <button class="get-btn" type="button" :disabled="!canAdd" @click="addToCart">
            <img :src="getImage" alt="GET" />
          </button>
        </div>
        <div v-else class="card-buy">
          <RouterLink class="card-view" :to="route">查看详情</RouterLink>
          <button class="get-btn" type="button" @click="addToCart">
            <img :src="getImage" alt="GET" />
          </button>
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
  padding: 0;
  background: transparent;
}

.vp-card.is-bordered {
  padding: 0 9.8px 19.6px;
  background: #ffffff;
  box-shadow: 0 0 0 1px #e5e5e5;
}

.vp-card.is-bordered .card-image {
  width: 100%;
}

.card-top {
  position: absolute;
  top: 8px;
  left: 10px;
  z-index: 4;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  max-width: 45%;
  gap: 8px;
}

.card-brand {
  overflow: hidden;
  max-width: 100%;
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
  max-height: 20px;
  object-fit: contain;
  object-position: left center;
}

.card-badges {
  position: absolute;
  top: 2px;
  right: 4px;
  z-index: 3;
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 5px;
  max-width: calc(100% - 8px);
}

.card-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.3em 0.6em;
  font-size: 10px;
  font-weight: 400;
  font-style: italic;
  line-height: 1;
  color: #ffffff;
  white-space: nowrap;
  background: #ff0077;
  border-radius: 2px;
  transform-origin: center;
  animation: awl-bounce-in 2000ms ease-in-out 0ms infinite;
}

.card-feature-tags {
  position: absolute;
  bottom: 4px;
  left: 4px;
  z-index: 3;
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  max-width: calc(100% - 8px);
}

.card-feature-tags span {
  padding: 3px 6px;
  font-size: 10px;
  font-weight: 600;
  line-height: 1;
  white-space: nowrap;
  border-radius: 2px;
}

@keyframes awl-bounce-in {
  0% {
    transform: scale(0);
    animation-timing-function: ease-in;
    opacity: 0;
  }
  38% {
    transform: scale(1);
    animation-timing-function: ease-out;
    opacity: 1;
  }
  55% {
    transform: scale(0.7);
    animation-timing-function: ease-in;
  }
  72%,
  89%,
  100% {
    transform: scale(1);
    animation-timing-function: ease-out;
  }
  81% {
    transform: scale(0.84);
    animation-timing-function: ease-in;
  }
  95% {
    transform: scale(0.95);
    animation-timing-function: ease-in;
  }
}

@media (prefers-reduced-motion: reduce) {
  .card-badge {
    animation: none;
  }
}

.card-image {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 70%;
  height: auto;
  aspect-ratio: 1;
  margin: 0 auto;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 0;
}

.card-sold {
  position: absolute;
  top: 40%;
  right: 0;
  left: 0;
  z-index: 3;
  padding: 20px 0;
  font-weight: 700;
  color: #333333;
  text-align: center;
  text-transform: uppercase;
  background: #ffffff;
  background: hsla(0, 0%, 100%, 0.9);
  opacity: 0.9;
}

.card-hot {
  position: absolute;
  top: 50%;
  right: 0;
  z-index: 2;
  padding: 0.3em 0.6em;
  font-family: var(--font-heading);
  font-size: 10px;
  font-weight: 400;
  font-style: italic;
  line-height: 1;
  color: #ffffff;
  background: #0a0002;
  border-radius: 2px;
  transform: translateY(-50%);
  animation: awl-heartbeat 2000ms ease-in-out 0ms infinite;
}

@keyframes awl-heartbeat {
  0% {
    transform: translateY(-50%) scale(1);
    animation-timing-function: ease-out;
  }
  10% {
    transform: translateY(-50%) scale(0.91);
    animation-timing-function: ease-in;
  }
  17% {
    transform: translateY(-50%) scale(0.98);
    animation-timing-function: ease-out;
  }
  33% {
    transform: translateY(-50%) scale(0.87);
    animation-timing-function: ease-in;
  }
  45% {
    transform: translateY(-50%) scale(1);
    animation-timing-function: ease-out;
  }
}

@media (prefers-reduced-motion: reduce) {
  .card-hot {
    animation: none;
  }
}

.card-body {
  display: flex;
  flex: 1;
  flex-direction: column;
  padding: 10px 10px 20px;
  text-align: center;
}

.card-cat {
  font-size: 12px;
  line-height: 1.2;
  color: #777777;
  text-transform: uppercase;
}

.card-title {
  display: -webkit-box;
  min-height: 23px;
  margin: 1.36px 0;
  overflow: hidden;
  font-size: 14.4px;
  font-weight: 400;
  line-height: 1.6;
  color: #334862;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

.card-title:hover {
  color: var(--color-primary);
}

.card-price {
  margin-bottom: 0;
  font-size: 14.4px;
  font-weight: 700;
  line-height: 1;
  color: black;
}

.card-buy {
  display: flex;
  flex-direction: column;
  gap: 3px;
  width: 140px;
  margin: 5px auto 0;
}

.card-buy select {
  width: 100%;
  height: 32.6px;
  padding: 5px 10px;
  font-size: 13px;
  color: #333333;
  background: #ffffff;
  border: 1px solid #dddddd;
  border-radius: 4px;
}

.card-buy select:focus,
.card-buy select:focus-visible {
  outline: none;
  border-color: #dddddd;
  box-shadow: none;
}

.get-btn {
  width: 100%;
  height: 32.5px;
  padding: 0;
  background: transparent;
  border: 0;
}

.get-btn img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: fill;
}

.get-btn:disabled {
  cursor: not-allowed;
}

.card-view {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 34px;
  font-size: 11px;
  font-weight: 700;
  color: #d9a8bf;
  background: #fafafa;
  border: 1px solid #f0f0f0;
  transition: background 0.18s ease, color 0.18s ease;
}

.card-view:hover {
  color: #ffffff;
  background: var(--color-primary);
  border-color: var(--color-primary);
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
    padding: 0;
  }

  .card-top {
    top: 4px;
    left: 8px;
  }

  .card-brand-logo {
    max-height: 16px;
  }

  .card-image {
    width: 70%;
    height: auto;
    margin: 0 auto;
  }

  .card-body {
    min-height: 167px;
    padding: 9.5px 10px 19px;
  }

  .card-cat {
    font-size: 12px;
  }

  .card-title {
    min-height: 22px;
    font-size: 13.6px;
    line-height: 19.4px;
  }

  .card-price {
    font-size: 13.6px;
  }

  .card-buy {
    width: 100%;
    gap: 3px;
  }

  .card-buy select,
  .card-buy button,
  .card-view {
    height: 30px;
    font-size: 12px;
  }

  .card-buy select {
    padding: 4px 8px;
  }

  .card-wish {
    display: none;
  }
}
</style>
