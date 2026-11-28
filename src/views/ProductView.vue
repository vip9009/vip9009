<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { site, productsData } from '@/data'
import VpProductCard from '@/components/VpProductCard.vue'
import AppIcon from '@/components/AppIcon.vue'
import { useCart } from '@/stores/cart'
import { asset, decodeEntities, detectBrand, formatPrice } from '@/utils'
import { isFeatureTag } from '@/utils/tags'

const route = useRoute()
const cart = useCart()

const sectionId = computed(() => String(route.params.section || ''))
const productIndex = computed(() => Number(route.params.index ?? -1))
const section = computed(
  () => productsData.sections.find((entry) => entry.id === sectionId.value) || null,
)
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
const detailBlocks = computed(() => {
  const list = Array.isArray(product.value?.detailBlocks) ? product.value.detailBlocks : []
  return list.filter((block) => {
    if (!block || typeof block !== 'object') return false
    if (block.type === 'text' || block.type === 'heading') return Boolean(String(block.text || '').trim())
    if (block.type === 'image' || block.type === 'video') return Boolean(String(block.src || '').trim())
    return false
  })
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
    .slice(0, 4),
)
const isHot = computed(
  () =>
    product.value?.hot === true ||
    allBadges.value.some((badge) => String(badge).toUpperCase() === 'HOT'),
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
            stock: entry.stock !== false,
          },
    )
    .filter((entry) => entry.label)
})
const selectedOption = computed(
  () => options.value.find((entry) => entry.label === option.value) || null,
)
const priceLabel = computed(() => {
  const price = Number(product.value?.price)
  const max = Number(product.value?.priceMax)
  if (Number.isFinite(max) && max > price)
    return `${formatPrice(price)} – ${formatPrice(max)}`
  return formatPrice(product.value?.price)
})
const activePrice = computed(() => selectedOption.value?.price ?? product.value?.price)
const canAdd = computed(
  () => stock.value && (selectedOption.value ? selectedOption.value.stock : true),
)
const addLabel = computed(() => (added.value ? '已加入购物车' : '加入购物车'))
const zoomOpen = ref(false)
const zoomed = ref(false)
const detailZoomSrc = ref('')
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
  if (options.value.length)
    rows.push({ label: '口味/规格', value: `${options.value.length} 种` })
  return rows.filter((row) => row.value)
})
const related = computed(() => {
  if (!section.value || !product.value) return []
  const products = section.value.products || []
  return products
    .map((item, index) => ({
      product: item,
      index,
      sectionId: section.value.id,
      sectionTitle: section.value.title,
    }))
    .filter((item) => item.index !== productIndex.value)
    .sort((a, b) => {
      const aMatch = a.product.subcategory === product.value.subcategory ? 0 : 1
      const bMatch = b.product.subcategory === product.value.subcategory ? 0 : 1
      return aMatch - bMatch
    })
    .slice(0, 4)
})

watch(option, (value) => {
  if (value) error.value = ''
})

function addToCart() {
  error.value = ''
  if (!stock.value || (selectedOption.value && !selectedOption.value.stock)) {
    error.value = '抱歉，该产品暂无库存,请选择其它产品。'
    return
  }
  if (options.value.length && !option.value) {
    error.value = '加入购物车之前请选定产品选项。'
    document.getElementById('option')?.focus()
    return
  }
  cart.add({
    sectionId: sectionId.value,
    index: productIndex.value,
    title: title.value,
    price: activePrice.value,
    image: image.value,
    option: option.value,
    qty: quantity.value,
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

function openZoom(src = '') {
  detailZoomSrc.value = src
  zoomOpen.value = true
  zoomed.value = false
  document.body.style.overflow = 'hidden'
}

function closeZoom() {
  zoomOpen.value = false
  zoomed.value = false
  detailZoomSrc.value = ''
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

function changeQty(delta) {
  quantity.value = Math.max(1, Math.min(99, quantity.value + delta))
}

watch(
  image,
  (value) => {
    activeImage.value = value
  },
  { immediate: true },
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
          image: image.value,
        }
        const next = [
          current,
          ...list.filter(
            (item) =>
              !(item.sectionId === current.sectionId && item.index === current.index),
          ),
        ]
        localStorage.setItem(key, JSON.stringify(next.slice(0, 6)))
      } catch {
        /* ignore storage errors */
      }
    }
  },
  { immediate: true },
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
              <img
                v-if="brandLogo"
                class="gallery-brand-logo"
                :src="asset(brandLogo)"
                :alt="brand" />
              <span v-else class="gallery-brand">{{ brand }}</span>
            </div>
            <div class="gallery-image">
              <img :src="activeImage || image" :alt="title" />
              <div v-if="badges.length" class="gallery-badges">
                <span v-for="badge in badges" :key="badge" class="gallery-badge">{{
                  badge
                }}</span>
              </div>
              <span v-if="isHot" class="gallery-hot">HOT</span>
              <button
                class="zoom-button"
                type="button"
                aria-label="查看大图"
                @click="openZoom()">
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
              @click="activeImage = thumb">
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
            <button v-if="option" class="clear-option" type="button" @click="clearOption">
              清除
            </button>
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
            <button
              class="add-cart"
              type="button"
              :class="{ 'is-unavailable': !canAdd }"
              @click="addToCart">
              {{ addLabel }}
            </button>
          </div>

          <p v-if="error" class="form-error">{{ error }}</p>

          <div class="meta">
            <p>
              <span>分类：</span>&nbsp;
              <RouterLink :to="`/category/${sectionId}`">{{ section?.title }}</RouterLink>
              <template
                v-if="product.subcategory && site.categories[product.subcategory]">
                ，<RouterLink :to="`/category/${sectionId}?sub=${product.subcategory}`">{{
                  site.categories[product.subcategory].title
                }}</RouterLink>
              </template>
            </p>
            <p v-if="allBadges.length">
              <span>标签：</span>&nbsp;
              <template v-for="(badge, badgeIndex) in allBadges" :key="badge">
                <RouterLink :to="`/search?q=${encodeURIComponent(badge)}`">{{
                  badge
                }}</RouterLink
                ><span v-if="badgeIndex < allBadges.length - 1" class="meta-sep">, </span>
              </template>
            </p>
            <p v-if="brand">
              <span>品牌：</span>&nbsp;
              <RouterLink :to="`/search?q=${encodeURIComponent(brand)}`">{{
                brand
              }}</RouterLink>
            </p>
          </div>
        </div>
      </div>

      <div class="product-tabs">
        <div class="tab-head">
          <button
            type="button"
            :class="{ active: activeTab === 'description' }"
            @click="activeTab = 'description'">
            描述
          </button>
          <button
            type="button"
            :class="{ active: activeTab === 'specs' }"
            @click="activeTab = 'specs'">
            参数
          </button>
          <button
            type="button"
            :class="{ active: activeTab === 'faq' }"
            @click="activeTab = 'faq'">
            声明 FAQ
          </button>
        </div>

        <div class="tab-body">
          <div v-if="activeTab === 'description'" class="description">
            <template v-if="detailBlocks.length">
              <template v-for="(block, index) in detailBlocks" :key="index">
                <hr v-if="block.type === 'heading' && index > 0" class="detail-rule" />
                <h2 v-if="block.type === 'heading'" class="detail-heading">{{ block.text }}</h2>
                <p v-else-if="block.type === 'text'" class="detail-text">{{ block.text }}</p>
                <figure v-else-if="block.type === 'image'" class="detail-figure">
                  <img
                    :src="asset(block.src)"
                    :alt="block.alt || title"
                    loading="lazy"
                    @click="openZoom(asset(block.src))" />
                  <figcaption v-if="block.caption">{{ block.caption }}</figcaption>
                </figure>
                <figure v-else-if="block.type === 'video'" class="detail-figure detail-video">
                  <video
                    :src="asset(block.src)"
                    :poster="block.poster ? asset(block.poster) : undefined"
                    controls
                    playsinline
                    preload="metadata"></video>
                  <figcaption v-if="block.caption">{{ block.caption }}</figcaption>
                </figure>
              </template>
            </template>
            <p v-else>
              {{
                product.description ||
                '加泡泡哥微信或 QQ 获取实时价格、口味与物流方案。泡泡哥只做正品，支持扫码验证，不同国家与地区的配送方式由泡泡哥一对一确认。'
              }}
            </p>
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
              <p>本店郑重承诺：上架所有款式提供正品保障。</p>
              <p>
                收到货后扫描包装上的防伪二维码，在品牌官方渠道验证。有疑问把包装正面、防伪码和查询结果拍给客服核对。
              </p>
            </details>
            <details>
              <summary>发货时间？</summary>
              <p>通常24小时内发货，部分48小时内发货，特殊72小时内发货。</p>
            </details>
            <details>
              <summary>电子烟小知识</summary>
              <p>强击喉感：高尼古丁（盐碱）+ 高PG + 凉味剂 +高功率（如一次性小烟）。</p>
              <p>柔和口感：低尼古丁 + 高VG + 低温雾化（如开放式大烟）。</p>
              <p>PG：丙二醇，高PG（如70%PG）增强击喉感和风味清晰度，但烟雾量小。</p>
              <p>
                VG：植物甘油，高VG（如80%VG）烟雾量大、口感绵柔，但击喉感弱（常见于大烟设备）
              </p>
              <p>
                感官误导：凉味剂（薄荷醇）或高PG的刺痛感（击喉感）可能让用户误以为“劲大=安全”，因电子烟的便捷性，可能会导致无意识连续摄入，忽视尼古丁摄入过多风险，建议误短频多次
              </p>
              <p>
                英国公共卫生部（PHE）：电子烟尼古丁吸收效率约为纸烟的50–70%，但高浓度产品可能逆转这一差距。
              </p>
              <p>健康建议：选择低尼古丁浓度（如3–6mg/mL）和PG/VG平衡的品质烟油</p>
              <p>口吸：类似吸烟的吸入方式，气流经过喉咙更集中，击喉感明显。</p>
              <p>肺吸：直接入肺，烟雾分散，击喉感较弱（常见于大烟雾设备）。</p>
              <p>重复注油：检测金属数据严重超标，健康建议选择一次性品牌产品。</p>
            </details>
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
            bordered />
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
          :src="detailZoomSrc || activeImage || image"
          :alt="title"
          @click="toggleZoom" />
        <span class="zoom-tip"
          >{{ zoomed ? '点击图片缩小' : '点击图片放大' }} · ESC 关闭</span
        >
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
  transition:
    color 0.18s ease,
    border-color 0.18s ease,
    background 0.18s ease;
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
  gap: 12px;
  margin-top: 14px;
  font-size: 10px;
  color: #aaaaaa;
}

.info h1 {
  margin-bottom: 11px;
  font-size: 27.2px;
  font-weight: 700;
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
  line-height: 24px;
  color: #111111;
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
  font-size: 14.4px;
  font-weight: 700;
  color: #111111;
}

.option-row select {
  flex: 1;
  height: 40px;
  padding: 10px 15px;
  margin: 8px 0 15px;
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
  color: #111111;
}

.variation-stock {
  margin: 4px 0 15px;
  font-size: 13px;
  color: #008000;
}

.variation-stock.out {
  color: #008000;
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

.add-cart.is-unavailable {
  color: #ffffff;
  background: #6d6d6d;
}

.add-cart.is-unavailable:hover {
  background: #6d6d6d;
}

.add-cart:disabled {
  color: #ffffff;
  background: #000000;
  opacity: 0.6;
  cursor: not-allowed;
}

.form-error {
  margin: 8px 0 10px;
  font-size: 12.8px;
  font-weight: 600;
  color: #b20000;
}

.meta {
  padding: 15px 0;
  font-size: 12.8px;
  line-height: 1.2;
  color: #777777;
  border-top: 1px dotted #d9d9d9;
  border-bottom: 1px dotted #d9d9d9;
}

.meta p {
  padding: 5px 0;
  margin: 0;
  line-height: 15.36px;
}

.meta a {
  color: #334862;
  text-decoration: none;
}

.meta a:hover {
  color: #111111;
}

.meta-sep {
  white-space: pre;
}

.meta span {
  color: #999999;
}

.product-tabs {
  padding: 23px 15px 0;
}

.tab-head {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding-bottom: 16px;
}

.tab-head button {
  height: 34px;
  padding: 0 20px;
  font-size: 12px;
  font-weight: 600;
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
  padding: 20px;
  border: 1px solid #eeeeee;
  border-radius: 10px;
}

.description p,
.notice p {
  font-size: 16px;
  line-height: 1.9;
  color: #666666;
  white-space: pre-line;
}

.description .detail-rule {
  height: 0;
  margin: 15px 0;
  border: 0;
  border-top: 1px solid #e5e5e5;
}

.description .detail-heading {
  margin: 0 0 12.8px;
  font-size: 22px;
  font-weight: 700;
  line-height: 1.6;
  color: #555555;
}

.description .detail-heading:first-child {
  margin-top: 0;
}

.description .detail-figure {
  margin: 14px 0;
}

.description .detail-figure:first-child {
  margin-top: 0;
}

.description .detail-figure img {
  display: block;
  width: 100%;
  height: auto;
  background: #f7f7f7;
  border-radius: 10px;
  cursor: zoom-in;
}

.description .detail-video video {
  display: block;
  width: 100%;
  max-height: 70vh;
  background: #000000;
  border-radius: 10px;
}

.description .detail-figure figcaption {
  margin-top: 6px;
  font-size: 12px;
  line-height: 1.6;
  color: #999999;
  text-align: center;
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
  gap: 12px;
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

  .description .detail-heading {
    margin-bottom: 9.6px;
    font-size: 19.2px;
  }

  .product-tabs {
    padding: 23px 0 0;
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
    display: none;
  }

  .gallery-brand-logo {
    max-height: 20px;
  }

  .info h1 {
    font-size: 22.4px;
    font-weight: 700;
    line-height: 29.12px;
    margin-bottom: 11px;
  }

  .price,
  .variation-price {
    font-size: 24px;
    line-height: 24px;
  }

  .option-row label {
    padding-right: 18px;
    font-size: 14px;
    font-weight: 700;
    color: #111111;
  }

  .option-row select {
    padding: 10px 15px;
    font-size: 16px;
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
    padding: 20px;
    border-radius: 10px;
  }

  .product-grid-3 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px;
    margin: 0 -10px;
  }

  .tab-head button {
    padding: 0 12px;
    font-size: 10px;
  }
}
</style>
