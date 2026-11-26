<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { site } from '@/data'
import { asset } from '@/utils'
import AppIcon from '@/components/AppIcon.vue'

const copied = ref(false)
let timer = null

async function copyQQ() {
  const number = site.contacts.qq?.number
  if (!number) return
  try {
    await navigator.clipboard.writeText(number)
    copied.value = true
    clearTimeout(timer)
    timer = setTimeout(() => {
      copied.value = false
    }, 1600)
  } catch {
    copied.value = false
  }
}
</script>

<template>
  <div class="wrapper contact-page">
    <nav class="breadcrumb">
      <RouterLink to="/">首页</RouterLink>
      <span>/</span>
      <span>联系泡泡哥</span>
    </nav>

    <div class="contact-head">
      <h1>联系泡泡哥</h1>
      <p>口味、价格、库存、物流，直接问；不留言，不用等邮件。</p>
    </div>

    <div class="contact-grid">
      <section class="wechat-card">
        <div class="card-head">
          <img :src="asset(site.contacts.wechat.avatar)" alt="泡泡哥" width="56" height="56" />
          <div>
            <b>{{ site.contacts.wechat.name }}</b>
            <span>{{ site.contacts.wechat.tagline }}</span>
          </div>
        </div>
        <img class="qr" :src="asset(site.contacts.wechat.image)" alt="泡泡哥微信二维码" />
        <p>扫码加微信，发我你常抽的口味和预算。</p>
      </section>

      <section class="qq-card">
        <span class="qq-label">{{ site.contacts.qq?.label || '泡泡哥 QQ' }}</span>
        <b class="qq-number">{{ site.contacts.qq?.number }}</b>
        <p>不方便加微信？直接加 QQ，备注“看货”。</p>
        <button type="button" class="copy-btn" @click="copyQQ">
          <AppIcon name="copy" :size="15" />
          {{ copied ? '已复制' : '复制 QQ 号' }}
        </button>
        <div class="qq-points">
          <span>真人回复</span>
          <span>按口味推荐</span>
          <span>物流可查</span>
        </div>
      </section>
    </div>

    <section class="service-row">
      <div>
        <b>扫码验真</b>
        <span>收到货先验再抽</span>
      </div>
      <div>
        <b>多国可发</b>
        <span>运费与时效微信确认</span>
      </div>
      <div>
        <b>一对一售后</b>
        <span>不合适帮你调整方案</span>
      </div>
      <div>
        <b>订单可查</b>
        <span>右下角菜单 → 我的订单</span>
      </div>
    </section>

    <div class="contact-links">
      <RouterLink to="/info/payment">付款方式</RouterLink>
      <RouterLink to="/info/delivery">配送说明</RouterLink>
      <RouterLink to="/info/returns">退换政策</RouterLink>
      <RouterLink to="/info/verification">真假验证</RouterLink>
    </div>
  </div>
</template>

<style scoped>
.contact-page {
  padding-top: 26px;
  padding-bottom: 50px;
}

.breadcrumb {
  display: flex;
  gap: 7px;
  padding-bottom: 20px;
  font-size: 12px;
  color: #999999;
}

.breadcrumb a:hover {
  color: var(--color-primary);
}

.contact-head {
  padding-bottom: 24px;
  border-bottom: 1px solid #eeeeee;
}

.contact-head h1 {
  font-size: 30px;
}

.contact-head p {
  margin-top: 6px;
  font-size: 13px;
  color: #888888;
}

.contact-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 20px;
  padding: 30px 0;
}

.wechat-card,
.qq-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 26px;
  text-align: center;
  border: 1px solid #e5e5e5;
}

.card-head {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding-bottom: 14px;
  margin-bottom: 14px;
  text-align: left;
  border-bottom: 1px solid #eeeeee;
}

.card-head img {
  width: 56px;
  height: 56px;
  object-fit: cover;
  border-radius: 50%;
}

.card-head b {
  display: block;
  font-size: 15px;
}

.card-head span {
  display: block;
  margin-top: 3px;
  font-size: 11px;
  color: #999999;
}

.qr {
  width: 210px;
  height: 210px;
  object-fit: contain;
}

.wechat-card > p {
  margin-top: 10px;
  font-size: 12px;
  color: #888888;
}

.qq-card {
  justify-content: center;
  color: #ffffff;
  background: #111111;
  border-color: #111111;
}

.qq-label {
  font-size: 11px;
  letter-spacing: 0.12em;
  color: rgba(255, 255, 255, 0.55);
}

.qq-number {
  margin: 8px 0;
  font-family: var(--font-heading);
  font-size: 40px;
  font-weight: 900;
  letter-spacing: 0.02em;
  color: #ffffff;
}

.qq-card > p {
  margin-bottom: 16px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
}

.copy-btn {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  height: 40px;
  padding: 0 18px;
  font-size: 12px;
  font-weight: 700;
  color: #ffffff;
  background: var(--color-primary);
}

.copy-btn:hover {
  background: #c2006a;
}

.qq-points {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
  margin-top: 18px;
}

.qq-points span {
  padding: 3px 8px;
  font-size: 10px;
  color: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.22);
}

.service-row {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1px;
  background: #eeeeee;
  border: 1px solid #eeeeee;
}

.service-row div {
  padding: 18px 14px;
  text-align: center;
  background: #ffffff;
}

.service-row b {
  display: block;
  margin-bottom: 4px;
  font-size: 13px;
}

.service-row span {
  font-size: 10px;
  color: #999999;
}

.contact-links {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px 26px;
  padding-top: 24px;
}

.contact-links a {
  font-size: 12px;
  color: #777777;
}

.contact-links a:hover {
  color: var(--color-primary);
}

@media (max-width: 900px) {
  .contact-grid {
    grid-template-columns: minmax(0, 1fr);
    gap: 14px;
    padding: 20px 0;
  }

  .service-row {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .contact-head h1 {
    font-size: 24px;
  }

  .qq-number {
    font-size: 34px;
  }
}
</style>
