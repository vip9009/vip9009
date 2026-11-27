<script setup>
import { computed, ref, watch } from 'vue'
import { RouterLink } from 'vue-router'
import { useCart } from '@/stores/cart'
import { site } from '@/data'
import { asset, decodeEntities, detectBrand, formatPrice, productRoute } from '@/utils'
import { featureTagStyle, isFeatureTag } from '@/utils/tags'

const props = defineProps({
  product: { type: Object, required: true },
  sectionId: { type: String, required: true },
  sectionTitle: { type: String, default: '' },
  index: { type: Number, required: true },
  eager: { type: Boolean, default: false }
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
const allBadges = computed(() => {
  const list = Array.isArray(props.product.badges) ? [...props.product.badges] : []
  if (props.product.recommend && !list.includes('店长推荐')) list.push('店长推荐')
  return list
})
const featureTags = computed(() => allBadges.value.filter((badge) => isFeatureTag(badge)).slice(0, 4))
const badges = computed(() =>
  allBadges.value
    .filter((badge) => String(badge).toUpperCase() !== 'HOT' && !isFeatureTag(badge))
    .slice(0, 4)
)
const isHot = computed(
  () =>
    props.product.hot === true ||
    allBadges.value.some((badge) => String(badge).toUpperCase() === 'HOT')
)
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
  <article class="vp-card" :class="{ 'is-sold': !stock }">
    <div class="card-top">
      <img v-if="brandLogo" class="card-brand-logo" :src="asset(brandLogo)" :alt="brand" />
      <span v-else class="card-brand">{{ brand }}</span>
    </div>

    <RouterLink class="card-image" :to="route">
      <img :src="image" :alt="title" :loading="eager ? 'eager' : 'lazy'" decoding="async" />
      <div v-if="badges.length" class="card-badges">
        <span v-for="badge in badges" :key="badge" class="card-badge">{{ badge }}</span>
      </div>
      <span v-if="isHot" class="card-hot">HOT</span>
      <div v-if="featureTags.length" class="card-feature-tags">
        <span v-for="tag in featureTags" :key="tag" :style="featureTagStyle(tag)">{{ tag }}</span>
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
  padding: 14px;
  background: #ffffff;
  box-shadow: 0 1px 3px -2px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
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
  height: 245px;
  margin: 4px 0 6px;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 10px;
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
  display: flex;
  flex-direction: column;
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

.card-buy select:focus,
.card-buy select:focus-visible {
  outline: none;
  border-color: #dddddd;
  box-shadow: none;
}

.get-btn {
  width: 100%;
  height: 36px;
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
