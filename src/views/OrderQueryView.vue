<script setup>
import { computed, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { site } from '@/data'
import { findOrder, listOrders } from '@/stores/orders'
import { asset, formatPrice } from '@/utils'

const keyword = ref('')
const result = ref(null)
const searched = ref(false)
const recent = ref(listOrders().slice(0, 5))

const paymentQr = computed(() => site.payment?.qr || '')

function search() {
  result.value = findOrder(keyword.value)
  searched.value = true
}

function formatDate(value) {
  if (!value) return ''
  const date = new Date(value)
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString('zh-CN')
}

function useOrder(id) {
  keyword.value = id
  search()
}
</script>

<template>
  <div class="wrapper page">
    <nav class="breadcrumb">
      <RouterLink to="/">首页</RouterLink>
      <span>/</span>
      <span>我的订单</span>
    </nav>

    <div class="order-query">
      <h1>订单查询</h1>
      <p class="hint">输入下单后生成的订单号，例如 PP202611261234。</p>
      <form class="search-form" @submit.prevent="search">
        <input v-model="keyword" type="text" placeholder="输入订单号" />
        <button type="submit">查询</button>
      </form>

      <div v-if="result" class="order-card">
        <div class="order-head">
          <div>
            <span>订单号</span>
            <b>{{ result.id }}</b>
          </div>
          <span class="status">{{ result.status }}</span>
        </div>
        <div class="order-meta">
          <span>下单时间：{{ formatDate(result.createdAt) }}</span>
          <span>支付方式：{{ result.payment }}</span>
        </div>

        <div class="order-products">
          <div v-for="item in result.items" :key="item.key" class="order-product">
            <img :src="item.image" :alt="item.title" />
            <div>
              <b>{{ item.title }}</b>
              <small v-if="item.option">{{ item.option }}</small>
              <span>× {{ item.qty }}</span>
            </div>
            <em>{{ formatPrice(item.price * item.qty) }}</em>
          </div>
        </div>

        <div class="order-total">
          <span>合计</span>
          <b>{{ formatPrice(result.total) }}</b>
        </div>

        <div v-if="result.status === '待付款'" class="order-pay">
          <div class="pay-qr">
            <img v-if="paymentQr" :src="asset(paymentQr)" alt="收款二维码" />
            <span v-else>收款二维码待上传</span>
          </div>
          <div>
            <b>扫码支付</b>
            <p>{{ site.payment?.note }}</p>
            <p>付款后把截图发给客服 QQ：{{ site.contacts.qq?.number }}</p>
          </div>
        </div>
      </div>

      <div v-else-if="searched" class="not-found">
        <p>没有找到这个订单，请检查订单号是否正确。</p>
        <p class="hint">订单只保存在下单时的浏览器里；换设备或清理缓存后可能查不到，请直接联系客服。</p>
      </div>

      <div v-if="recent.length && !result" class="recent">
        <b>最近订单</b>
        <button v-for="item in recent" :key="item.id" type="button" @click="useOrder(item.id)">
          {{ item.id }}
          <span>{{ item.status }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page {
  padding-top: 26px;
  padding-bottom: 40px;
}

.breadcrumb {
  display: flex;
  gap: 8px;
  padding-bottom: 22px;
  font-size: 12px;
  color: #999999;
}

.breadcrumb a:hover {
  color: var(--color-primary);
}

.order-query {
  max-width: 720px;
  margin: 0 auto;
}

.order-query h1 {
  margin-bottom: 6px;
  font-size: 26px;
}

.hint {
  font-size: 12px;
  line-height: 1.7;
  color: #999999;
}

.search-form {
  display: flex;
  height: 44px;
  margin: 18px 0 24px;
  border: 1px solid #dddddd;
}

.search-form input {
  flex: 1;
  min-width: 0;
  padding: 0 14px;
  font-size: 13px;
  border: 0;
  outline: none;
}

.search-form button {
  width: 96px;
  font-size: 13px;
  font-weight: 700;
  color: #ffffff;
  background: #242125;
}

.search-form button:hover {
  background: var(--color-primary);
}

.order-card {
  border: 1px solid #242125;
}

.order-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 18px;
  border-bottom: 1px solid #eeeeee;
}

.order-head span {
  display: block;
  font-size: 10px;
  color: #999999;
}

.order-head b {
  font-size: 15px;
  color: #242125;
}

.status {
  padding: 4px 9px;
  font-size: 11px;
  color: #ffffff !important;
  background: var(--color-primary);
}

.order-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 24px;
  padding: 10px 18px;
  font-size: 11px;
  color: #999999;
  background: #fafafa;
}

.order-products {
  padding: 8px 18px;
}

.order-product {
  display: grid;
  grid-template-columns: 52px 1fr auto;
  gap: 10px;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #f2f2f2;
}

.order-product img {
  width: 52px;
  height: 52px;
  object-fit: contain;
}

.order-product b {
  display: block;
  font-size: 12px;
}

.order-product small {
  display: block;
  margin-top: 2px;
  font-size: 10px;
  color: #999999;
}

.order-product span {
  font-size: 10px;
  color: #999999;
}

.order-product em {
  font-size: 12px;
  font-style: normal;
  font-weight: 700;
}

.order-total {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 18px;
  font-size: 13px;
  font-weight: 700;
  border-top: 1px solid #eeeeee;
}

.order-total b {
  font-size: 18px;
}

.order-pay {
  display: grid;
  grid-template-columns: 140px 1fr;
  gap: 16px;
  align-items: center;
  padding: 16px 18px;
  border-top: 1px solid #eeeeee;
}

.pay-qr {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 140px;
  height: 140px;
  font-size: 10px;
  color: #999999;
  border: 1px solid #eeeeee;
}

.pay-qr img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.order-pay b {
  font-size: 13px;
}

.order-pay p {
  margin-top: 5px;
  font-size: 11px;
  line-height: 1.6;
  color: #777777;
}

.not-found {
  padding: 24px;
  background: #fafafa;
  border: 1px solid #eeeeee;
}

.not-found p {
  margin-bottom: 6px;
  font-size: 13px;
  color: #777777;
}

.recent {
  padding-top: 22px;
}

.recent > b {
  display: block;
  margin-bottom: 8px;
  font-size: 12px;
  color: #999999;
}

.recent button {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 10px 12px;
  margin-bottom: 6px;
  font-size: 12px;
  text-align: left;
  color: #333333;
  background: #fafafa;
  border: 1px solid #eeeeee;
}

.recent button span {
  color: var(--color-primary);
}

@media (max-width: 640px) {
  .order-pay {
    grid-template-columns: 1fr;
  }

  .pay-qr {
    margin: 0 auto;
  }
}
</style>
