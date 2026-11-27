<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { site, productsData } from '@/data'
import VpProductCard from '@/components/VpProductCard.vue'
import AppIcon from '@/components/AppIcon.vue'
import { useCart } from '@/stores/cart'
import { useWishlist } from '@/stores/wishlist'
import { asset, decodeEntities, detectBrand, formatPrice } from '@/utils'
import { isFeatureTag } from '@/utils/tags'

const route = useRoute()
const cart = useCart()
const wishlist = useWishlist()

const sectionId = computed(() => String(route.params.section || ''))
const productIndex = computed(() => Number(route.params.index ?? -1))
const section = computed(() => productsData.sections.find((entry) => entry.id === sectionId.value) || null)
const product = computed(() => section.value?.products?.[productIndex.value] || null)
const category = computed(() => site.categories[sectionId.value] || null)

const option = ref('')
const quantity = ref(1)
const activeTab = ref('description')
const added = ref(false)
const error = ref('')
let addedTimer = null

const title = computed(() => decodeEntities(product.value?.title || ''))
const brand = computed(() => detectBrand(product.value || {}))
const brandLogo = computed(() => site.brandLogos?.[brand.value] || '')
const image = computed(() => asset(product.value?.localImage || ''))
const gallery = computed(() => {
  const list = Array.isArray(product.value?.gallery) ? product.value.gallery : []
  return list.length ? list.map(asset) : [image.value]
})
const activeImage = ref('')
const allBadges = computed(() => {
  const list = Array.isArray(product.value?.badges) ? [...product.value.badges] : []
  if (product.value?.recommend && !list.includes('店长推荐')) list.push('店长推荐')
  return list
})
const badges = computed(() =>
  allBadges.value
    .filter((badge) => String(badge).toUpperCase() !== 'HOT' && !isFeatureTag(badge))
    .slice(0, 4)
)
const isHot = computed(
  () =>
    product.value?.hot === true ||
    allBadges.value.some((badge) => String(badge).toUpperCase() === 'HOT')
)
const stock = computed(() => product.value?.stock !== false)
const options = computed(() => {
  const list = Array.isArray(product.value?.options) ? product.value.options : []
  return list
    .map((entry) =>
      typeof entry === 'string'
        ? { label: entry, price: product.value?.price, stock: true }
        : {
            label: entry.label || entry.name || '',
            price: entry.price ?? product.value?.price,
            stock: entry.stock !== false
          }
    )
    .filter((entry) => entry.label)
})
const selectedOption = computed(
  () => options.value.find((entry) => entry.label === option.value) || null
)
const priceLabel = computed(() => {
  const price = Number(product.value?.price)
  const max = Number(product.value?.priceMax)
  if (Number.isFinite(max) && max > price) return `${formatPrice(price)} – ${formatPrice(max)}`
  return formatPrice(product.value?.price)
})
const activePrice = computed(() => selectedOption.value?.price ?? product.value?.price)
const canAdd = computed(
  () =>
    stock.value &&
    (!options.value.length || Boolean(option.value)) &&
    (selectedOption.value ? selectedOption.value.stock : true)
)
const addLabel = computed(() => {
  if (!stock.value) return '无货'
  if (selectedOption.value && !selectedOption.value.stock) return '该口味无货'
  return added.value ? '已加入购物车' : '加入购物车'
})
const zoomOpen = ref(false)
const zoomed = ref(false)
const specRows = computed(() => {
  const specs = product.value?.specs
  if (specs && typeof specs === 'object' && !Array.isArray(specs)) {
    return Object.entries(specs).map(([label, value]) => ({ label, value }))
  }
  const rows = []
  const puffs = title.value.match(/(\d{3,6})\s*口/)
  if (puffs) rows.push({ label: '口数', value: `${puffs[1]} 口` })
  rows.push({ label: '类型', value: section.value?.title || '' })
  if (brand.value) rows.push({ label: '品牌', value: brand.value })
  if (options.value.length) rows.push({ label: '口味/规格', value: `${options.value.length} 种` })
  return rows.filter((row) => row.value)
})
const related = computed(() => {
  if (!section.value || !product.value) return []
  const products = section.value.products || []
  return products
    .map((item, index) => ({ product: item, index, sectionId: section.value.id, sectionTitle: section.value.title }))
    .filter((item) => item.index !== productIndex.value)
    .sort((a, b) => {
      const aMatch = a.product.subcategory === product.value.subcategory ? 0 : 1
      const bMatch = b.product.subcategory === product.value.subcategory ? 0 : 1
      return aMatch - bMatch
    })
    .slice(0, 4)
})

function addToCart() {
  error.value = ''
  if (!stock.value) {
    error.value = '该商品暂时无货，可以联系客服确认补货时间。'
    return
  }
  if (options.value.length && !option.value) {
    error.value = '请先选择口味/规格。'
    return
  }
  if (selectedOption.value && !selectedOption.value.stock) {
    error.value = '该口味暂时无货，请选择其他口味。'
    return
  }
  if (!canAdd.value) return
  cart.add({
    sectionId: sectionId.value,
    index: productIndex.value,
    title: title.value,
    price: activePrice.value,
    image: image.value,
    option: option.value,
    qty: quantity.value
  })
  added.value = true
  clearTimeout(addedTimer)
  addedTimer = setTimeout(() => {
    added.value = false
  }, 1800)
}

function clearOption() {
  option.value = ''
  error.value = ''
}

function openZoom() {
  zoomOpen.value = true
  zoomed.value = false
  document.body.style.overflow = 'hidden'
}

function closeZoom() {
  zoomOpen.value = false
  zoomed.value = false
  document.body.style.overflow = ''
}

function toggleZoom() {
  zoomed.value = !zoomed.value
}

function onKeydown(event) {
  if (event.key === 'Escape' && zoomOpen.value) closeZoom()
}

onMounted(() => window.addEventListener('keydown', onKeydown))

onBeforeUnmount(() => {
  window.removeEventListener('keydown', onKeydown)
  document.body.style.overflow = ''
  clearTimeout(addedTimer)
})

function toggleWishlist() {
  if (!product.value) return
  wishlist.toggle({
    sectionId: sectionId.value,
    index: productIndex.value,
    title: title.value,
    price: product.value.price,
    image: image.value
  })
}

function changeQty(delta) {
  quantity.value = Math.max(1, Math.min(99, quantity.value + delta))
}

watch(
  image,
  (value) => {
    activeImage.value = value
  },
  { immediate: true }
)

watch(
  product,
  () => {
    option.value = ''
    quantity.value = 1
    added.value = false
    error.value = ''
    if (product.value) {
      document.title = `${title.value} - 泡泡哥雾化`
      try {
        const key = 'paopao-recent-v1'
        const list = JSON.parse(localStorage.getItem(key) || '[]')
        const current = {
          sectionId: sectionId.value,
          index: productIndex.value,
          title: title.value,
          price: Number(product.value.price) || 0,
          image: image.value
        }
        const next = [current, ...list.filter((item) => !(item.sectionId === current.sectionId && item.index === current.index))]
        localStorage.setItem(key, JSON.stringify(next.slice(0, 6)))
      } catch {
        /* ignore storage errors */
      }
    }
  },
  { immediate: true }
)
</script>

<template>
  <div class="wrapper product-page">
    <template v-if="product">
      <nav class="breadcrumb">
        <RouterLink to="/">首页</RouterLink>
        <span>/</span>
        <RouterLink to="/category/disposables">电子雾化</RouterLink>
        <span>/</span>
        <RouterLink :to="`/category/${sectionId}`">{{ section?.title }}</RouterLink>
      </nav>

      <div class="product-main">
        <div class="gallery">
          <div class="gallery-stage">
            <div class="gallery-brand-row">
              <img v-if="brandLogo" class="gallery-brand-logo" :src="asset(brandLogo)" :alt="brand" />
              <span v-else class="gallery-brand">{{ brand }}</span>
            </div>
            <div class="gallery-image">
              <img :src="activeImage || image" :alt="title" />
              <div v-if="badges.length" class="gallery-badges">
                <span v-for="badge in badges" :key="badge" class="gallery-badge">{{ badge }}</span>
              </div>
              <span v-if="isHot" class="gallery-hot">HOT</span>
              <button class="zoom-button" type="button" aria-label="查看大图" @click="openZoom">
                <AppIcon name="expand" :size="15" />
              </button>
            </div>
          </div>
          <div v-if="gallery.length > 1" class="gallery-thumbs">
            <button
              v-for="thumb in gallery"
              :key="thumb"
              type="button"
              :class="{ active: thumb === activeImage }"
              @click="activeImage = thumb"
            >
              <img :src="thumb" :alt="title" />
            </button>
          </div>
          <div class="gallery-hint" style="display: none">
            <AppIcon name="scan" :size="14" />
            图片为实拍参考，批次不同包装可能略有差异
          </div>
        </div>

        <div class="info">
          <h1>{{ title }}</h1>
          <span class="title-divider"></span>

          <div class="price-row">
            <div class="price">{{ priceLabel }}</div>
            <button v-if="option" class="clear-option" type="button" @click="clearOption">清除</button>
          </div>

          <div v-if="options.length" class="option-row">
            <label for="option">口味</label>
            <select id="option" v-model="option">
              <option value="">选择一个选项</option>
              <option v-for="entry in options" :key="entry.label" :value="entry.label">
                {{ entry.label }}{{ entry.stock === false ? '（无货）' : '' }}
              </option>
            </select>
          </div>

          <div v-if="selectedOption" class="variation-meta">
            <div class="variation-price">{{ formatPrice(selectedOption.price) }}</div>
            <p class="variation-stock" :class="{ out: !selectedOption.stock }">
              {{ selectedOption.stock ? '有货' : '无货' }}
            </p>
          </div>

          <div class="buy-row">
            <div class="qty">
              <button type="button" aria-label="减少" @click="changeQty(-1)">−</button>
              <input :value="quantity" readonly aria-label="数量" />
              <button type="button" aria-label="增加" @click="changeQty(1)">＋</button>
            </div>
            <button class="add-cart" type="button" :disabled="!canAdd" @click="addToCart">
              {{ addLabel }}
            </button>
          </div>

          <p v-if="error" class="form-error">{{ error }}</p>

          <div class="sub-actions">
            <button class="wish-btn" type="button" :class="{ active: wishlist.has(sectionId, productIndex) }" @click="toggleWishlist">
              <AppIcon name="heart" :size="16" />
              {{ wishlist.has(sectionId, productIndex) ? '已收藏' : '加入收藏' }}
            </button>
          </div>

          <div class="meta">
            <p><span>分类：</span>{{ section?.title }}<template v-if="product.subcategory && site.categories[product.subcategory]">，{{ site.categories[product.subcategory].title }}</template></p>
            <p v-if="allBadges.length"><span>标签：</span>{{ allBadges.join('，') }}</p>
            <p v-if="brand"><span>品牌：</span>{{ brand }}</p>
            <p>
              <span>库存：</span>
              <template v-if="selectedOption">
                {{ selectedOption.stock ? '现货，确认后发出' : '该口味暂时无货，请选择其他口味' }}
              </template>
              <template v-else>{{ stock ? '现货，确认后发出' : '暂时无货，可联系客服' }}</template>
            </p>
          </div>

        </div>
      </div>

      <div class="product-tabs">
        <div class="tab-head">
          <button type="button" :class="{ active: activeTab === 'description' }" @click="activeTab = 'description'">描述</button>
          <button type="button" :class="{ active: activeTab === 'specs' }" @click="activeTab = 'specs'">参数</button>
          <button type="button" :class="{ active: activeTab === 'faq' }" @click="activeTab = 'faq'">常见问题</button>
          <button type="button" :class="{ active: activeTab === 'links' }" @click="activeTab = 'links'">相关链接</button>
          <button type="button" :class="{ active: activeTab === 'notice' }" @click="activeTab = 'notice'">声明 FAQ</button>
        </div>

        <div class="tab-body">
          <div v-if="activeTab === 'description'" class="description">
            <p>{{ product.description || '加泡泡哥微信或 QQ 获取实时价格、口味与物流方案。泡泡哥只做正品，支持扫码验证，不同国家与地区的配送方式由泡泡哥一对一确认。' }}</p>
          </div>

          <table v-else-if="activeTab === 'specs'" class="spec-table">
            <tbody>
              <tr v-for="row in specRows" :key="row.label">
                <th>{{ row.label }}</th>
                <td>{{ row.value }}</td>
              </tr>
            </tbody>
          </table>

          <div v-else-if="activeTab === 'faq'" class="faq">
            <details open>
              <summary>怎么确认是正品？</summary>
              <p>收到货后扫描包装上的防伪二维码，在品牌官方渠道验证。有疑问把包装正面、防伪码和查询结果拍给泡泡哥核对。</p>
            </details>
            <details>
              <summary>哪些国家能发？大概多久？</summary>
              <p>多数国家和地区可发，具体运费、时效和清关要求由泡泡哥按目的地确认。</p>
            </details>
            <details>
              <summary>口味怎么选？</summary>
              <p>把你常抽的口感、凉度和预算发给泡泡哥，会按你的习惯推荐；不确定就先拿小规格试。</p>
            </details>
            <details>
              <summary>收到货不合适怎么办？</summary>
              <p>先联系泡泡哥说明情况，保留开箱视频和照片；未拆封商品按实际情况协商处理。</p>
            </details>
          </div>

          <div v-else-if="activeTab === 'links'" class="links">
            <RouterLink :to="`/category/${sectionId}`">← 返回 {{ section?.title }}</RouterLink>
            <RouterLink to="/info/verification">真假验证说明</RouterLink>
            <RouterLink to="/info/delivery">配送说明</RouterLink>
            <RouterLink to="/info/returns">退换政策</RouterLink>
          </div>

          <div v-else class="notice">
            <p>本站仅做商品信息展示与咨询，不向未成年人销售。电子雾化产品含尼古丁，具有成瘾性，请勿在禁烟场所使用。</p>
            <p>页面价格为参考价，最终价格、库存与物流以泡泡哥微信 / QQ 确认为准。</p>
          </div>
        </div>
      </div>

      <section v-if="related.length" class="related">
        <div class="related-head">
          <h2>相关产品</h2>
          <RouterLink :to="`/category/${sectionId}`">查看全部 →</RouterLink>
        </div>
        <div class="product-grid-3">
          <VpProductCard
            v-for="item in related"
            :key="`${item.sectionId}-${item.index}`"
            :product="item.product"
            :section-id="item.sectionId"
            :section-title="item.sectionTitle"
            :index="item.index"
            bordered
          />
        </div>
      </section>
    </template>

    <div v-else class="empty-state">
      <h1>没有找到这个商品</h1>
      <p>商品可能已经下架，返回首页看看当前在售的商品。</p>
      <RouterLink class="black-btn" to="/">返回首页</RouterLink>
    </div>

    <Teleport to="body">
      <div v-if="zoomOpen" class="zoom-viewer" @click.self="closeZoom">
        <button class="zoom-close" type="button" aria-label="关闭" @click="closeZoom">
          <AppIcon name="close" :size="22" />
        </button>
        <img
          :class="{ zoomed }"
          :src="activeImage || image"
          :alt="title"
          @click="toggleZoom"
        />
        <span class="zoom-tip">{{ zoomed ? '点击图片缩小' : '点击图片放大' }} · ESC 关闭</span>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
.product-page {
  padding: 20px 0 50px;
}

.breadcrumb {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  padding: 0 15px 18px;
  font-size: 12px;
  color: #999999;
}

.breadcrumb a:hover {
  color: var(--color-primary);
}

.product-main {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 0;
  padding: 10px 0 30px;
}

.gallery {
  position: relative;
  padding: 0 15px;
}

.info {
  padding: 0 15px;
}

.gallery-stage {
  position: relative;
}

.gallery-brand-row {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 5;
  display: flex;
  align-items: center;
  min-height: 24px;
}

.gallery-brand {
  display: block;
  font-family: var(--font-heading);
  font-size: 11px;
  font-weight: 900;
  letter-spacing: 0.08em;
  color: #242125;
}

.gallery-brand-logo {
  display: block;
  max-width: 110px;
  max-height: 24px;
  object-fit: contain;
  object-position: left center;
}

.gallery-image {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 510px;
  padding-top: 32px;
  box-sizing: border-box;
}

.gallery-image img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  filter: drop-shadow(0 30px 24px rgba(0, 0, 0, 0.12));
}

.gallery-badges {
  position: absolute;
  top: 2px;
  right: 4px;
  z-index: 6;
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 5px;
  max-width: calc(100% - 8px);
}

.gallery-badge {
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
  animation: detail-bounce 2000ms ease-in-out 0ms infinite;
}

.gallery-hot {
  position: absolute;
  top: 50%;
  right: 0;
  z-index: 5;
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
  animation: detail-heartbeat 2000ms ease-in-out 0ms infinite;
}

.zoom-button {
  position: absolute;
  bottom: 9px;
  left: 12px;
  z-index: 7;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 39px;
  height: 39px;
  color: #c0c0c0;
  background: rgba(255, 255, 255, 0.7);
  border: 2px solid #c0c0c0;
  border-radius: 999px;
  transition: color 0.18s ease, border-color 0.18s ease, background 0.18s ease;
}

.zoom-button:hover {
  color: #242125;
  background: #ffffff;
  border-color: #242125;
}

@keyframes detail-bounce {
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

@keyframes detail-heartbeat {
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
  .gallery-badge,
  .gallery-hot {
    animation: none;
  }
}

.gallery-thumbs {
  display: flex;
  gap: 8px;
  margin-top: 10px;
}

.gallery-thumbs button {
  width: 56px;
  height: 56px;
  padding: 4px;
  border: 1px solid #eeeeee;
}

.gallery-thumbs button.active {
  border-color: var(--color-primary);
}

.gallery-thumbs img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.gallery-hint {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 14px;
  font-size: 10px;
  color: #aaaaaa;
}

.info h1 {
  margin-bottom: 10px;
  font-size: 27px;
  line-height: 1.3;
  color: #555555;
}

.title-divider {
  display: block;
  width: 30px;
  height: 1px;
  margin-bottom: 14px;
  background: #dddddd;
}

.price-row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 12px;
  margin-top: 12px;
}

.price {
  font-size: 24px;
  font-weight: 700;
  color: #777777;
}

.clear-option {
  font-size: 13px;
  color: #666666;
}

.clear-option:hover {
  color: var(--color-primary);
}

.option-row {
  display: flex;
  align-items: center;
  margin-top: 6px;
}

.option-row label {
  flex: 0 0 auto;
  padding-right: 20px;
  font-size: 14px;
  font-weight: 700;
  color: #777777;
}

.option-row select {
  flex: 1;
  height: 40px;
  padding: 0 15px;
  margin: 7px 0 15px;
  font-size: 14px;
  color: #333333;
  background: #ffffff;
  border: 1px solid #dddddd;
  border-radius: 8px;
}

.option-row select:focus,
.option-row select:focus-visible {
  outline: none;
  border-color: #dddddd;
  box-shadow: none;
}

.variation-meta {
  padding-top: 7px;
  border-top: 1px dashed #dddddd;
}

.variation-price {
  font-size: 24px;
  font-weight: 700;
  line-height: 1.2;
  color: #777777;
}

.variation-stock {
  margin: 4px 0 15px;
  font-size: 13px;
  color: #008000;
}

.variation-stock.out {
  color: #c0392b;
}

.buy-row {
  display: flex;
  gap: 24px;
  margin-bottom: 10px;
}

.qty {
  display: inline-flex;
  flex: 0 0 auto;
  align-items: center;
  width: 112px;
  height: 45px;
  overflow: hidden;
  border: 1px solid #dddddd;
  border-radius: 8px;
}

.qty button {
  width: 35px;
  height: 100%;
  font-size: 18px;
  font-weight: 700;
  color: #333333;
  background: #f5f5f5;
}

.qty input {
  width: 40px;
  height: 100%;
  text-align: center;
  background: #ffffff;
  border: 0;
  outline: none;
}

.add-cart {
  height: 45px;
  min-width: 122px;
  padding: 0 25px;
  font-size: 14px;
  font-weight: 600;
  color: #ffffff;
  background: #000000;
  border-radius: 8px;
}

.add-cart:hover:not(:disabled) {
  background: var(--color-primary);
}

.add-cart:disabled {
  color: #ffffff;
  background: #000000;
  opacity: 0.6;
  cursor: not-allowed;
}

.form-error {
  margin-bottom: 8px;
  font-size: 11px;
  color: #c0392b;
}

.sub-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: 14px;
}

.wish-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #777777;
}

.wish-btn.active {
  color: var(--color-primary);
}

.meta {
  padding: 12px 0;
  font-size: 11px;
  line-height: 1.9;
  color: #777777;
  border-top: 1px solid #eeeeee;
  border-bottom: 1px solid #eeeeee;
}

.meta span {
  color: #999999;
}



.product-tabs {
  padding: 10px 15px 0;
}

.tab-head {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding-bottom: 16px;
}

.tab-head button {
  height: 34px;
  padding: 0 18px;
  font-size: 11px;
  color: #666666;
  background: #f5f5f5;
  border-radius: 999px;
}

.tab-head button.active {
  color: #ffffff;
  background: #242125;
}

.tab-body {
  min-height: 160px;
  padding: 26px;
  border: 1px solid #eeeeee;
}

.description p,
.notice p {
  font-size: 13px;
  line-height: 1.9;
  color: #666666;
  white-space: pre-line;
}

.notice p + p {
  margin-top: 10px;
}

.spec-table {
  width: 100%;
  border-collapse: collapse;
}

.spec-table th,
.spec-table td {
  padding: 10px 12px;
  font-size: 12px;
  text-align: left;
  border-bottom: 1px solid #f2f2f2;
}

.spec-table th {
  width: 140px;
  font-weight: 400;
  color: #999999;
  background: #fafafa;
}

.faq details {
  padding: 12px 0;
  border-bottom: 1px solid #f2f2f2;
}

.faq summary {
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
}

.faq p {
  padding-top: 8px;
  font-size: 12px;
  line-height: 1.8;
  color: #777777;
}

.links {
  display: flex;
  flex-wrap: wrap;
  gap: 12px 26px;
}

.links a {
  font-size: 12px;
  color: #3372a2;
}

.links a:hover {
  color: var(--color-primary);
}

.related {
  padding: 44px 15px 0;
}

.related-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 14px;
  margin-bottom: 16px;
  border-bottom: 1px solid #eeeeee;
}

.related-head h2 {
  font-size: 20px;
}

.related-head a {
  font-size: 12px;
  color: #999999;
}

.product-grid-3 {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0;
}

.empty-state {
  padding: 90px 20px;
  text-align: center;
}

.empty-state h1 {
  margin-bottom: 10px;
  font-size: 26px;
}

.empty-state p {
  margin-bottom: 18px;
  font-size: 13px;
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

.zoom-viewer {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  background: rgba(0, 0, 0, 0.9);
}

.zoom-viewer img {
  max-width: 92vw;
  max-height: 86vh;
  object-fit: contain;
  cursor: zoom-in;
  user-select: none;
  transition: transform 0.25s ease;
}

.zoom-viewer img.zoomed {
  transform: scale(1.6);
  cursor: zoom-out;
}

.zoom-close {
  position: absolute;
  top: 22px;
  right: 26px;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  color: #ffffff;
  background: rgba(255, 255, 255, 0.14);
  border-radius: 999px;
  transition: background 0.18s ease;
}

.zoom-close:hover {
  background: rgba(255, 255, 255, 0.28);
}

.zoom-tip {
  position: absolute;
  bottom: 24px;
  left: 50%;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.72);
  transform: translateX(-50%);
}

@media (max-width: 900px) {
  .product-page {
    padding: 20px 15px 50px;
  }

  .breadcrumb {
    justify-content: center;
    padding: 0 0 0;
    font-size: 16px;
  }

  .product-tabs {
    padding: 10px 0 0;
  }

  .related {
    padding: 44px 0 0;
  }

  .product-main {
    grid-template-columns: minmax(0, 1fr);
    gap: 10px;
  }

  .gallery,
  .info {
    padding: 0;
  }

  .gallery-image {
    height: 360px;
    padding-top: 28px;
  }

  .zoom-button {
    width: 34px;
    height: 34px;
    bottom: 8px;
    left: 8px;
  }

  .gallery-brand-logo {
    max-height: 20px;
  }

  .info h1 {
    font-size: 22px;
  }

  .price,
  .variation-price {
    font-size: 20px;
  }

  .option-row label {
    padding-right: 12px;
    font-size: 13px;
  }

  .option-row select {
    padding: 0 10px;
    font-size: 13px;
  }

  .qty {
    width: 112px;
    height: 45px;
  }

  .qty button {
    width: 35px;
  }

  .add-cart {
    height: 45px;
    min-width: 122px;
    padding: 0 25px;
    font-size: 14px;
  }

  .zoom-viewer {
    padding: 18px;
  }

  .tab-body {
    padding: 16px;
  }

  .product-grid-3 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0;
    margin: 0 -10px;
  }

  .tab-head button {
    padding: 0 12px;
    font-size: 10px;
  }
}
</style>
