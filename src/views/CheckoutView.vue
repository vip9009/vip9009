<script setup>
import { computed, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { site } from '@/data'
import { useCart } from '@/stores/cart'
import { createOrder } from '@/stores/orders'
import { asset, formatPrice } from '@/utils'

const cart = useCart()
const address = ref('')
const agree = ref(false)
const error = ref('')
const order = ref(null)

const freeOver = computed(() => Number(site.shipping?.freeOver ?? 138))
const fee = computed(() => Number(site.shipping?.fee ?? 8))
const shippingFee = computed(() =>
  cart.items.length && cart.subtotal.value < freeOver.value ? fee.value : 0
)
const total = computed(() => cart.subtotal.value + shippingFee.value)
const paymentQr = computed(() => site.payment?.qr || '')

function placeOrder() {
  error.value = ''
  if (!cart.items.length) {
    error.value = '购物车是空的。'
    return
  }
  if (!address.value.trim()) {
    error.value = '请填写收件人、手机号和完整地址。'
    return
  }
  if (!agree.value) {
    error.value = '请先阅读并同意条款和条件。'
    return
  }
  order.value = createOrder({
    items: cart.items.map((item) => ({ ...item })),
    subtotal: cart.subtotal.value,
    shippingFee: shippingFee.value,
    total: total.value,
    address: address.value.trim(),
    payment: '扫码支付'
  })
  cart.clear()
}
</script>

<template>
  <div class="wrapper page">
    <nav class="steps" aria-label="购物流程">
      <RouterLink to="/cart">购物车</RouterLink>
      <i>›</i>
      <span class="active">付款详情</span>
      <i>›</i>
      <span>订单完成</span>
    </nav>

    <div v-if="order" class="success">
      <span class="success-mark">✓</span>
      <h1>订单已提交</h1>
      <p>订单号：<b>{{ order.id }}</b></p>
      <p class="success-note">{{ site.payment?.note }}</p>
      <div class="success-qr">
        <img v-if="paymentQr" :src="asset(paymentQr)" alt="收款二维码" />
        <span v-else>收款二维码待上传</span>
      </div>
      <p class="success-qq">
        付款后把截图发给 {{ site.contacts.qq?.label || '客服' }}：
        <b>{{ site.contacts.qq?.number }}</b>
      </p>
      <div class="success-actions">
        <RouterLink class="black-btn" to="/order-query">查询订单</RouterLink>
        <RouterLink class="ghost-btn" to="/category/hot">继续购物</RouterLink>
      </div>
    </div>

    <div v-else-if="!cart.items.length" class="empty-cart">
      <p>您的购物车目前是空的。</p>
      <RouterLink class="black-btn" to="/category/hot">返回商店</RouterLink>
    </div>

    <div v-else class="checkout-layout">
      <div class="checkout-main">
        <p class="checkout-tip">※ 订单查询 → 右下角菜单 → 我的订单</p>

        <h2>收货信息</h2>
        <textarea
          v-model="address"
          class="field"
          rows="3"
          placeholder="收件人 + 手机号 + 省 + 市 + 街道 + 备注（可选）"
        />

        <p class="checkout-tip">※ 「扫码支付」需提供付款截图</p>
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

        <h3>[扫码支付]</h3>
        <div class="method-qr">
          <img v-if="paymentQr" :src="asset(paymentQr)" alt="收款二维码" />
          <span v-else>收款二维码待上传</span>
        </div>
        <p class="method-note">{{ site.payment?.note }}</p>
        <p class="method-qq">
          客服 QQ：{{ site.contacts.qq?.number }}
        </p>

        <label class="agree">
          <input v-model="agree" type="checkbox" />
          <span>我已经读了并同意本网站的 <RouterLink to="/info/returns">条款和条件</RouterLink> *</span>
        </label>

        <p v-if="error" class="error">{{ error }}</p>
        <button class="place-order" type="button" @click="placeOrder">下单</button>
      </aside>
    </div>
  </div>
</template>

<style scoped>
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

.order-box {
  align-self: start;
  padding: 22px;
  border: 1px solid #242125;
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

.method-qr {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 160px;
  height: 160px;
  margin-bottom: 8px;
  font-size: 11px;
  color: #999999;
  background: #fafafa;
  border: 1px solid #eeeeee;
}

.method-qr img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.method-note {
  margin-bottom: 4px;
  font-size: 10px;
  line-height: 1.5;
  color: #999999;
}

.method-qq {
  margin-bottom: 12px;
  font-size: 11px;
  color: #242125;
}

.agree {
  display: flex;
  align-items: flex-start;
  gap: 7px;
  margin-bottom: 12px;
  font-size: 11px;
  line-height: 1.5;
  color: #777777;
}

.agree a {
  color: var(--color-primary);
}

.error {
  margin-bottom: 8px;
  font-size: 11px;
  color: #c0392b;
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

.success {
  max-width: 520px;
  padding: 30px 20px;
  margin: 0 auto;
  text-align: center;
}

.success-mark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 54px;
  height: 54px;
  margin-bottom: 14px;
  font-size: 24px;
  color: #ffffff;
  background: var(--color-primary);
  border-radius: 50%;
}

.success h1 {
  margin-bottom: 10px;
  font-size: 24px;
}

.success p {
  margin-bottom: 8px;
  font-size: 13px;
  color: #777777;
}

.success-note {
  font-size: 11px;
  color: #999999;
}

.success-qr {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 200px;
  height: 200px;
  margin: 16px auto;
  color: #999999;
  border: 1px solid #eeeeee;
}

.success-qr img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.success-qq {
  color: #242125 !important;
}

.success-actions {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 18px;
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
