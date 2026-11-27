<template>
  <div class="wrapper page">
    <nav class="steps" aria-label="购物流程">
      <span class="active">购物车</span>
      <i>›</i>
      <span>付款详情</span>
      <i>›</i>
      <span>订单完成</span>
    </nav>

    <div v-if="!cart.items.length" class="empty-cart">
      <p>您的购物车目前是空的。</p>
      <RouterLink class="black-btn" to="/category/hot">返回商店</RouterLink>
    </div>

    <div v-else class="cart-layout">
      <div class="cart-main">
        <table class="cart-table">
          <thead>
            <tr>
              <th>产品</th>
              <th>价格</th>
              <th>数量</th>
              <th>小计</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in cart.items" :key="item.key">
              <td class="product-cell">
                <button class="remove" type="button" aria-label="删除" @click="cart.remove(item.key)">×</button>
                <img :src="item.image" :alt="item.title" />
                <div>
                  <RouterLink :to="`/product/${item.sectionId}/${item.index}`">{{ item.title }}</RouterLink>
                  <small v-if="item.option">{{ item.option }}</small>
                </div>
              </td>
              <td data-label="价格">{{ formatPrice(item.price) }}</td>
              <td data-label="数量">
                <div class="qty">
                  <button type="button" @click="cart.updateQty(item.key, item.qty - 1)">−</button>
                  <input :value="item.qty" readonly />
                  <button type="button" @click="cart.updateQty(item.key, item.qty + 1)">＋</button>
                </div>
              </td>
              <td data-label="小计" class="subtotal">{{ formatPrice(item.price * item.qty) }}</td>
            </tr>
          </tbody>
        </table>

        <div class="cart-actions">
          <RouterLink class="ghost-btn" to="/category/hot">← 继续购物</RouterLink>
        </div>
      </div>

      <aside class="summary">
        <h2>购物车总计</h2>
        <div class="summary-row"><span>小计</span><b>{{ formatPrice(cart.subtotal.value) }}</b></div>
        <div class="summary-row">
          <span>包裹</span>
          <b>{{ shippingFee ? formatPrice(shippingFee) : '免运费' }}</b>
        </div>
        <p class="summary-note">满 {{ formatPrice(freeOver) }} 包邮</p>
        <div class="summary-total"><span>合计</span><b>{{ formatPrice(total) }}</b></div>
        <RouterLink class="checkout-btn" to="/checkout">去结算</RouterLink>
        <p class="summary-tip">支持扫码支付，付款后把截图发给泡泡哥。</p>
      </aside>
    </div>
  </div>
</template>
<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { site } from '@/data'
import { useCart } from '@/stores/cart'
import { asset, formatPrice } from '@/utils'

const cart = useCart()

const freeOver = computed(() => Number(site.shipping?.freeOver ?? 138))
const fee = computed(() => Number(site.shipping?.fee ?? 8))
const shippingFee = computed(() =>
  cart.items.length && cart.subtotal.value < freeOver.value ? fee.value : 0
)
const total = computed(() => cart.subtotal.value + shippingFee.value)
</script>
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

.steps .active {
  color: #242125;
}

.steps i {
  font-style: normal;
  color: #cccccc;
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
.checkout-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 42px;
  padding: 0 22px;
  font-size: 13px;
  font-weight: 700;
  color: #ffffff;
  background: #242125;
}

.black-btn:hover,
.checkout-btn:hover {
  background: var(--color-primary);
}

.cart-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 330px;
  gap: 36px;
  padding-right: 20px;
}

.cart-table {
  width: 100%;
  border-collapse: collapse;
  border-top: 1px solid #eeeeee;
}

.cart-table th {
  padding: 10px 8px;
  font-size: 11px;
  font-weight: 400;
  text-align: left;
  color: #999999;
  border-bottom: 1px solid #eeeeee;
}

.cart-table td {
  padding: 14px 8px;
  font-size: 13px;
  vertical-align: middle;
  border-bottom: 1px solid #f2f2f2;
}

.product-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.product-cell img {
  width: 64px;
  height: 64px;
  object-fit: contain;
  border: 1px solid #eeeeee;
}

.product-cell a {
  display: block;
  font-size: 13px;
  color: #3372a2;
}

.product-cell small {
  display: block;
  margin-top: 3px;
  font-size: 11px;
  color: #999999;
}

.remove {
  width: 20px;
  height: 20px;
  font-size: 16px;
  color: #999999;
}

.qty {
  display: inline-flex;
  align-items: center;
  height: 32px;
  border: 1px solid #dddddd;
}

.qty button {
  width: 30px;
  height: 100%;
  font-size: 14px;
  color: #555555;
}

.qty input {
  width: 34px;
  height: 100%;
  text-align: center;
  border: 0;
  border-right: 1px solid #eeeeee;
  border-left: 1px solid #eeeeee;
  outline: none;
}

.subtotal {
  font-weight: 700;
}

.cart-actions {
  padding-top: 18px;
}

.ghost-btn {
  display: inline-flex;
  align-items: center;
  height: 38px;
  padding: 0 16px;
  font-size: 12px;
  color: #555555;
  border: 1px solid #dddddd;
}

.ghost-btn:hover {
  color: var(--color-primary);
  border-color: var(--color-primary);
}

.summary {
  align-self: start;
  padding: 22px;
  border: 1px solid #242125;
}

.summary h2 {
  padding-bottom: 12px;
  margin-bottom: 12px;
  font-size: 15px;
  border-bottom: 1px solid #eeeeee;
}

.summary-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 7px 0;
  font-size: 13px;
  color: #777777;
}

.summary-row b {
  color: #242125;
}

.summary-note {
  padding-bottom: 10px;
  font-size: 11px;
  color: #999999;
  border-bottom: 1px solid #eeeeee;
}

.summary-total {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 0;
  font-size: 14px;
  font-weight: 700;
}

.summary-total b {
  font-size: 18px;
}

.checkout-btn {
  width: 100%;
  height: 46px;
}

.summary-tip {
  padding-top: 10px;
  font-size: 10px;
  line-height: 1.6;
  color: #999999;
}

@media (max-width: 900px) {
  .page {
    padding-top: 22px;
    padding-bottom: 40px;
  }

  .steps {
    gap: 8px;
    padding-bottom: 20px;
    font-size: 14px;
  }

  .cart-layout {
    grid-template-columns: minmax(0, 1fr);
    gap: 22px;
    padding-right: 0;
  }

  .cart-table {
    border-top: 0;
  }

  .cart-table thead {
    display: none;
  }

  .cart-table,
  .cart-table tbody {
    display: block;
    width: 100%;
  }

  .cart-table tr {
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    align-items: center;
    gap: 6px 10px;
    padding: 12px;
    margin-bottom: 12px;
    background: #ffffff;
    border: 1px solid #eeeeee;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  }

  .cart-table tr:last-child {
    margin-bottom: 0;
  }

  .cart-table td {
    display: block;
    width: auto;
    padding: 0;
    font-size: 13px;
    border: 0;
  }

  .cart-table .product-cell {
    position: relative;
    display: flex;
    grid-column: 1 / -1;
    align-items: center;
    gap: 12px;
    padding: 0 28px 0 0;
  }

  .product-cell img {
    flex: 0 0 auto;
    width: 64px;
    height: 64px;
    background: #fafafa;
    border-radius: 6px;
  }

  .product-cell > div {
    min-width: 0;
  }

  .product-cell a {
    display: -webkit-box;
    overflow: hidden;
    font-size: 13px;
    line-height: 1.45;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
  }

  .product-cell small {
    margin-top: 4px;
  }

  .remove {
    position: absolute;
    top: 0;
    right: 0;
    width: 24px;
    height: 24px;
    font-size: 18px;
    line-height: 1;
  }

  .cart-table td[data-label]::before {
    display: none;
  }

  .cart-table td[data-label='价格'] {
    grid-row: 2 / span 2;
    grid-column: 1;
    align-self: center;
    font-size: 13px;
    color: #666666;
    white-space: nowrap;
  }

  .cart-table td[data-label='数量'] {
    grid-row: 2;
    grid-column: 2;
    align-self: center;
    justify-self: end;
    white-space: nowrap;
  }

  .cart-table td[data-label='小计'] {
    grid-row: 3;
    grid-column: 2;
    align-self: center;
    justify-self: end;
    font-size: 15px;
    font-weight: 700;
    color: #242125;
    white-space: nowrap;
  }

  .cart-table td[data-label='小计']::before {
    content: '小计';
    display: inline;
    margin-right: 4px;
    font-size: 10px;
    font-weight: 400;
    color: #999999;
  }

  .qty {
    height: 30px;
  }

  .qty button {
    width: 28px;
  }

  .qty input {
    width: 30px;
  }

  .cart-actions {
    padding-top: 14px;
  }

  .ghost-btn {
    height: 36px;
    padding: 0 14px;
  }

  .summary {
    padding: 18px;
    border-color: #e5e5e5;
    border-radius: 10px;
  }

  .summary h2 {
    font-size: 14px;
  }

  .checkout-btn {
    height: 44px;
  }
}
</style>
