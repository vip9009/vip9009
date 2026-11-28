<script setup>
import { computed, ref, watch } from 'vue'
import { RouterLink } from 'vue-router'
import { site } from '@/data'
import { useCart } from '@/stores/cart'
import { formatPrice } from '@/utils'
import { buildOrderText, copyToClipboard } from '@/utils/orderText'

const cart = useCart()
const address = ref('')
const copied = ref(false)
const finished = ref(false)
const error = ref('')

const freeOver = computed(() => Number(site.shipping?.freeOver ?? 138))
const fee = computed(() => Number(site.shipping?.fee ?? 8))
const shippingFee = computed(() =>
  cart.items.length && cart.subtotal.value < freeOver.value ? fee.value : 0
)
const total = computed(() => cart.subtotal.value + shippingFee.value)
const orderText = computed(() =>
  buildOrderText({
    items: cart.items,
    subtotal: cart.subtotal.value,
    shippingFee: shippingFee.value,
    total: total.value,
    address: address.value
  })
)

watch(address, (value) => {
  if (value.trim()) error.value = ''
})

async function copyOrder() {
  error.value = ''
  if (!cart.items.length) {
    error.value = '购物车是空的。'
    return
  }
  if (!address.value.trim()) {
    error.value = '请先填写收货信息（收件人、手机号和完整地址）。'
    return
  }
  const ok = await copyToClipboard(orderText.value)
  if (!ok) {
    error.value = '复制失败，请展开下方订单信息手动复制。'
    return
  }
  copied.value = true
}

function finishOrder() {
  cart.clear()
  finished.value = true
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<template>
  <div class="wrapper page">
    <nav class="steps" aria-label="购物流程">
      <RouterLink to="/cart">购物车</RouterLink>
      <i>›</i>
      <span class="active">填写信息</span>
      <i>›</i>
      <span>发给客服</span>
    </nav>

    <div v-if="finished" class="order-done">
      <span class="done-mark">✓</span>
      <h1>购物车已清空</h1>
      <p>订单信息已复制。请把订单信息发给客服，等待客服确认商品、运费和付款方式。</p>
      <div class="done-actions">
        <RouterLink class="black-btn" to="/">继续购物</RouterLink>
        <RouterLink class="ghost-btn" to="/contact">联系客服</RouterLink>
      </div>
    </div>

    <div v-else-if="!cart.items.length" class="empty-cart">
      <p>您的购物车目前是空的。</p>
      <RouterLink class="black-btn" to="/category/disposables">返回商店</RouterLink>
    </div>

    <div v-else class="checkout-layout">
      <div class="checkout-main">
        <p class="checkout-tip">填写收货信息 → 复制订单信息 → 加客服微信 / QQ，把信息发过去确认付款方式。</p>

        <h2>收货信息</h2>
        <textarea
          v-model="address"
          class="field"
          rows="3"
          placeholder="收件人 + 手机号 + 省 + 市 + 街道 + 备注（可选）"
        />

        <details class="order-preview">
          <summary>查看要发送的订单信息</summary>
          <pre>{{ orderText }}</pre>
        </details>

        <p class="checkout-tip">※ 本站不提供在线支付，请加客服微信 / QQ 确认商品、运费和付款方式后再付款。</p>
      </div>

      <aside class="order-box">
        <h2>您的订单</h2>
        <div class="order-items">
          <div v-for="item in cart.items" :key="item.key" class="order-item">
            <img :src="item.image" :alt="item.title" />
            <div>
              <b>{{ item.title }}</b>
              <small v-if="item.option">{{ item.option }}</small>
              <span>× {{ item.qty }}</span>
            </div>
            <em>{{ formatPrice(item.price * item.qty) }}</em>
          </div>
        </div>

        <div class="order-row"><span>小计</span><b>{{ formatPrice(cart.subtotal.value) }}</b></div>
        <div class="order-row">
          <span>运费</span>
          <b>{{ shippingFee ? formatPrice(shippingFee) : '免运费' }}</b>
        </div>
        <p class="order-note">满 {{ formatPrice(freeOver) }} 包邮</p>
        <div class="order-total"><span>合计</span><b>{{ formatPrice(total) }}</b></div>

        <h3>联系客服付款</h3>
        <div class="pay-contact">
          <p><b>微信：</b>{{ site.contacts.wechat?.name || '客服微信' }}</p>
          <p><b>QQ：</b>{{ site.contacts.qq?.number }}</p>
          <p class="pay-note">
            本站不提供在线支付。请加客服微信或 QQ，确认商品、运费和付款方式后再付款。
          </p>
          <RouterLink to="/contact">查看微信二维码 / QQ 联系方式 →</RouterLink>
        </div>

        <button class="place-order" type="button" @click="copyOrder">
          {{ copied ? '已复制，请发给客服' : '复制订单信息发给客服' }}
        </button>
        <p v-if="error" class="error">{{ error }}</p>
        <p v-if="copied" class="copy-success">
          订单信息已复制。请加客服微信 / QQ，把订单信息发过去确认付款方式。
        </p>
        <button v-if="copied" class="clear-cart-btn" type="button" @click="finishOrder">
          我已发给客服，清空购物车
        </button>
      </aside>
    </div>
  </div>
</template>

<style scoped>

.clear-cart-btn {
  width: 100%;
  height: 42px;
  margin-top: 10px;
  font-size: 13px;
  font-weight: 600;
  color: #555555;
  background: #ffffff;
  border: 1px solid #dddddd;
  border-radius: 4px;
}

.clear-cart-btn:hover {
  color: #111111;
  border-color: #111111;
}

.order-done {
  max-width: 560px;
  padding: 60px 20px;
  margin: 0 auto;
  text-align: center;
}

.done-mark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 54px;
  height: 54px;
  margin-bottom: 14px;
  font-size: 24px;
  color: #ffffff;
  background: #242125;
  border-radius: 50%;
}

.order-done h1 {
  margin-bottom: 10px;
  font-size: 24px;
}

.order-done p {
  margin-bottom: 20px;
  font-size: 13px;
  line-height: 1.8;
  color: #777777;
}

.done-actions {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.page {
  padding-top: 34px;
  padding-bottom: 30px;
}

.steps {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 14px;
  padding-bottom: 34px;
  font-size: 20px;
  color: #cccccc;
}

.steps a {
  color: #cccccc;
}

.steps .active {
  color: #242125;
}

.steps i {
  font-style: normal;
}

.checkout-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 420px;
  gap: 40px;
}

.checkout-tip {
  margin-bottom: 18px;
  font-size: 11px;
  color: #c0392b;
}

.checkout-main h2 {
  margin: 18px 0 8px;
  font-size: 15px;
}

.field {
  width: 100%;
  padding: 12px;
  font-size: 13px;
  color: #333333;
  background: #ffffff;
  border: 1px solid #dddddd;
  border-radius: 2px;
  outline: none;
  resize: vertical;
}

.field:focus {
  border-color: var(--color-primary);
}

.order-preview {
  margin-top: 12px;
}

.order-preview summary {
  font-size: 12px;
  color: #3372a2;
  cursor: pointer;
}

.order-preview pre {
  max-height: 320px;
  padding: 12px;
  margin-top: 8px;
  overflow: auto;
  font-family: inherit;
  font-size: 11px;
  line-height: 1.7;
  color: #555555;
  white-space: pre-wrap;
  word-break: break-word;
  background: #fafafa;
  border: 1px solid #eeeeee;
}

.order-box {
  align-self: start;
  padding: 22px;
  border: 1px solid #242125;
  border-radius: 10px;
}

.order-box h2 {
  padding-bottom: 12px;
  margin-bottom: 10px;
  font-size: 15px;
  border-bottom: 1px solid #eeeeee;
}

.order-items {
  padding-bottom: 8px;
}

.order-item {
  display: grid;
  grid-template-columns: 48px 1fr auto;
  gap: 10px;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f2f2f2;
}

.order-item img {
  width: 48px;
  height: 48px;
  object-fit: contain;
}

.order-item b {
  display: block;
  font-size: 12px;
  color: #333333;
}

.order-item small {
  display: block;
  margin-top: 2px;
  font-size: 10px;
  color: #999999;
}

.order-item span {
  font-size: 10px;
  color: #999999;
}

.order-item em {
  font-size: 12px;
  font-style: normal;
  font-weight: 700;
}

.order-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 0;
  font-size: 12px;
  color: #777777;
}

.order-row b {
  color: #242125;
}

.order-note {
  padding-bottom: 8px;
  font-size: 10px;
  color: #999999;
  border-bottom: 1px solid #eeeeee;
}

.order-total {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 0;
  font-size: 14px;
  font-weight: 700;
}

.order-total b {
  font-size: 18px;
}

.order-box h3 {
  padding: 10px 0 8px;
  font-size: 12px;
  border-top: 1px solid #eeeeee;
}

.pay-contact {
  padding: 12px;
  background: #fafafa;
  border: 1px solid #eeeeee;
  border-radius: 4px;
}

.pay-contact p {
  margin: 0 0 6px;
  font-size: 12px;
  line-height: 1.6;
  color: #242125;
}

.pay-contact b {
  font-weight: 700;
}

.pay-contact .pay-note {
  margin: 8px 0;
  font-size: 11px;
  color: #999999;
}

.pay-contact a {
  font-size: 12px;
  color: #3372a2;
}

.pay-contact a:hover {
  color: var(--color-primary);
}

.error {
  margin: 8px 0;
  font-size: 12px;
  color: #c0392b;
}

.copy-success {
  margin-top: 10px;
  font-size: 11px;
  line-height: 1.6;
  color: #008000;
}

.place-order {
  width: 100%;
  height: 46px;
  font-size: 14px;
  font-weight: 700;
  color: #ffffff;
  background: #242125;
}

.place-order:hover {
  background: var(--color-primary);
}

.empty-cart {
  padding: 70px 20px 110px;
  text-align: center;
}

.empty-cart p {
  margin-bottom: 18px;
  font-size: 15px;
  color: #c0392b;
}

.black-btn,
.ghost-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 40px;
  padding: 0 20px;
  font-size: 12px;
  font-weight: 700;
}

.black-btn {
  color: #ffffff;
  background: #242125;
}

.ghost-btn {
  color: #555555;
  border: 1px solid #dddddd;
}

.black-btn:hover {
  background: var(--color-primary);
}

.ghost-btn:hover {
  color: var(--color-primary);
  border-color: var(--color-primary);
}

@media (max-width: 900px) {
  .steps {
    gap: 8px;
    padding-bottom: 22px;
    font-size: 15px;
  }

  .checkout-layout {
    grid-template-columns: minmax(0, 1fr);
    gap: 26px;
  }

  .order-box {
    padding: 16px;
  }
}
</style>
