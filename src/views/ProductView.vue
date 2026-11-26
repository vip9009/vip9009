<script setup>
import { computed, ref, watchEffect } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { site, productsData } from '@/data'
import VpProductCard from '@/components/VpProductCard.vue'
import AppIcon from '@/components/AppIcon.vue'
import { useCart } from '@/stores/cart'
import { useWishlist } from '@/stores/wishlist'
import { asset, decodeEntities, detectBrand, formatPrice } from '@/utils'

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
const badges = computed(() => {
  const list = Array.isArray(product.value?.badges) ? [...product.value.badges] : []
  if (product.value?.recommend && !list.includes('店长推荐')) list.push('店长推荐')
  return list.slice(0, 4)
})
const isHot = computed(
  () =>
    product.value?.hot === true ||
    badges.value.some((badge) => String(badge).toUpperCase() === 'HOT')
)
const stock = computed(() => product.value?.stock !== false)
const options = computed(() => {
  const list = Array.isArray(product.value?.options) ? product.value.options : []
  return list
    .map((entry) =>
      typeof entry === 'string'
        ? { label: entry, price: product.value?.price }
        : { label: entry.label || entry.name || '', price: entry.price ?? product.value?.price }
    )
    .filter((entry) => entry.label)
})
const priceLabel = computed(() => {
  const price = Number(product.value?.price)
  const max = Number(product.value?.priceMax)
  if (Number.isFinite(max) && max > price) return `${formatPrice(price)} – ${formatPrice(max)}`
  return formatPrice(product.value?.price)
})
const activePrice = computed(() => {
  const match = options.value.find((entry) => entry.label === option.value)
  return match ? Number(match.price) : Number(product.value?.price)
})
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
  if (!stock.value) return
  if (options.value.length && !option.value) {
    error.value = '请先选择口味/规格。'
    return
  }
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

watchEffect(() => {
  if (!activeImage.value && image.value) activeImage.value = image.value
  if (product.value) document.title = `${title.value} - 泡泡哥雾化`
})
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
        <span>/</span>
        <span>{{ title }}</span>
      </nav>

      <div class="product-main">
        <div class="gallery">
          <img v-if="brandLogo" class="gallery-brand-logo" :src="asset(brandLogo)" :alt="brand" />
          <span v-else class="gallery-brand">{{ brand }}</span>
          <div class="gallery-tags">
            <span v-for="badge in badges" :key="badge">{{ badge }}</span>
          </div>
          <div class="gallery-image">
            <img :src="activeImage || image" :alt="title" />
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
          <div class="gallery-hint">
            <AppIcon name="scan" :size="14" />
            图片为实拍参考，批次不同包装可能略有差异
          </div>
        </div>

        <div class="info">
          <h1>{{ title }}</h1>
          <div class="price">{{ priceLabel }}</div>

          <div v-if="options.length" class="option-row">
            <label for="option">口味</label>
            <select id="option" v-model="option">
              <option value="">选择一个选项</option>
              <option v-for="entry in options" :key="entry.label" :value="entry.label">
                {{ entry.label }}
              </option>
            </select>
          </div>

          <div class="buy-row">
            <div class="qty">
              <button type="button" aria-label="减少" @click="changeQty(-1)">−</button>
              <input :value="quantity" readonly aria-label="数量" />
              <button type="button" aria-label="增加" @click="changeQty(1)">＋</button>
            </div>
            <button class="add-cart" type="button" :disabled="!stock" @click="addToCart">
              {{ stock ? (added ? '已加入购物车' : '加入购物车') : '无货' }}
            </button>
          </div>

          <p v-if="error" class="form-error">{{ error }}</p>

          <div class="sub-actions">
            <span v-if="isHot" class="hot-mark">HOT</span>
            <button class="wish-btn" type="button" :class="{ active: wishlist.has(sectionId, productIndex) }" @click="toggleWishlist">
              <AppIcon name="heart" :size="16" />
              {{ wishlist.has(sectionId, productIndex) ? '已收藏' : '加入收藏' }}
            </button>
          </div>

          <div class="meta">
            <p><span>分类：</span>{{ section?.title }}<template v-if="product.subcategory && site.categories[product.subcategory]">，{{ site.categories[product.subcategory].title }}</template></p>
            <p v-if="badges.length"><span>标签：</span>{{ badges.join('，') }}</p>
            <p v-if="brand"><span>品牌：</span>{{ brand }}</p>
            <p><span>库存：</span>{{ stock ? '现货，确认后发出' : '暂时无货，可联系客服' }}</p>
          </div>

          <div class="service-strip">
            <span>扫码验真</span>
            <span>物流可查</span>
            <span>一对一售后</span>
            <span>QQ {{ site.contacts.qq?.number }}</span>
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
          />
        </div>
      </section>
    </template>

    <div v-else class="empty-state">
      <h1>没有找到这个商品</h1>
      <p>商品可能已经下架，返回首页看看当前在售的商品。</p>
      <RouterLink class="black-btn" to="/">返回首页</RouterLink>
    </div>
  </div>
</template>

<style scoped>
.product-page {
  padding-top: 20px;
  padding-bottom: 50px;
}

.breadcrumb {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  padding-bottom: 18px;
  font-size: 12px;
  color: #999999;
}

.breadcrumb a:hover {
  color: var(--color-primary);
}

.product-main {
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(0, 0.95fr);
  gap: 54px;
  padding: 10px 0 30px;
}

.gallery {
  position: relative;
}

.gallery-brand {
  display: block;
  margin-bottom: 6px;
  font-family: var(--font-heading);
  font-size: 11px;
  font-weight: 900;
  letter-spacing: 0.08em;
  color: #242125;
}

.gallery-brand-logo {
  display: block;
  max-width: 110px;
  max-height: 26px;
  margin-bottom: 8px;
  object-fit: contain;
  object-position: left center;
}

.gallery-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-bottom: 10px;
}

.gallery-tags span {
  padding: 2px 7px;
  font-size: 9px;
  color: #ffffff;
  background: var(--color-primary);
}

.gallery-image {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 520px;
}

.gallery-image img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  filter: drop-shadow(0 30px 24px rgba(0, 0, 0, 0.12));
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
  font-size: 30px;
  line-height: 1.2;
  color: #242125;
}

.price {
  padding-bottom: 16px;
  margin-bottom: 16px;
  font-size: 22px;
  font-weight: 700;
  border-bottom: 1px solid #eeeeee;
}

.option-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 14px;
}

.option-row label {
  font-size: 12px;
  color: #777777;
}

.option-row select {
  flex: 1;
  height: 40px;
  padding: 0 10px;
  font-size: 12px;
  color: #555555;
  background: #ffffff;
  border: 1px solid #dddddd;
  border-radius: 2px;
}

.option-row select:focus,
.option-row select:focus-visible {
  outline: none;
  border-color: #dddddd;
  box-shadow: none;
}

.buy-row {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
}

.qty {
  display: inline-flex;
  align-items: center;
  height: 44px;
  border: 1px solid #dddddd;
}

.qty button {
  width: 34px;
  height: 100%;
  font-size: 15px;
  color: #555555;
}

.qty input {
  width: 42px;
  height: 100%;
  text-align: center;
  border: 0;
  border-right: 1px solid #eeeeee;
  border-left: 1px solid #eeeeee;
  outline: none;
}

.add-cart {
  flex: 1;
  height: 44px;
  font-size: 14px;
  font-weight: 700;
  color: #ffffff;
  background: #6d6d6d;
}

.add-cart:hover {
  background: var(--color-primary);
}

.add-cart:disabled {
  color: #cccccc;
  background: #f5f5f5;
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

.hot-mark {
  padding: 3px 8px;
  font-size: 9px;
  font-weight: 900;
  color: #ffffff;
  background: #242125;
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

.service-strip {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding-top: 12px;
}

.service-strip span {
  padding: 4px 8px;
  font-size: 10px;
  color: #777777;
  background: #f7f7f7;
  border: 1px solid #eeeeee;
}

.product-tabs {
  padding-top: 10px;
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
  padding-top: 44px;
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
  gap: 16px;
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

@media (max-width: 900px) {
  .product-main {
    grid-template-columns: minmax(0, 1fr);
    gap: 24px;
  }

  .gallery-image {
    height: 330px;
  }

  .info h1 {
    font-size: 22px;
  }

  .price {
    font-size: 18px;
  }

  .tab-body {
    padding: 16px;
  }

  .product-grid-3 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
  }

  .tab-head button {
    padding: 0 12px;
    font-size: 10px;
  }
}
</style>
