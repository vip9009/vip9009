<script setup>
import { RouterLink } from 'vue-router'
import { site } from '@/data'
import AppIcon from '@/components/AppIcon.vue'
import { asset } from '@/utils'

const features = [
  { icon: 'shield', title: '正品保证', text: '支持官方防伪扫码验证' },
  { icon: 'globe', title: '多国可发', text: '运费与时效微信确认' },
  { icon: 'truck', title: '物流可查', text: '发出后给单号' },
  { icon: 'scan', title: '扫码验证', text: '收到货后可核对真伪' }
]
</script>

<template>
  <div class="contact-page">
    <div class="wrapper">
      <nav class="breadcrumb" aria-label="面包屑">
        <RouterLink to="/">首页</RouterLink>
        <span class="sep">/</span>
        <span>联系我们</span>
      </nav>

      <div class="page-head">
        <div>
          <h1 class="page-title">联系我们</h1>
          <p class="page-subtitle">产品咨询、价格确认与物流问题，欢迎随时联系</p>
        </div>
      </div>

      <div class="seller-intro">
        <img
          class="seller-photo"
          :src="asset('/images/paopao-avatar-600.jpg')"
          alt="泡泡哥"
          width="180"
          height="180"
        />
        <div class="seller-copy">
          <span class="seller-eyebrow">泡泡哥雾化 · 主理人</span>
          <h2>你好，我是泡泡哥</h2>
          <p>
            站内所有商品由我亲自选品、验货、发货。网站只做分类与价格展示，
            选好产品后加我微信或 QQ，我帮你确认口味、价格和物流。
          </p>
        </div>
      </div>

      <div class="contact-grid">
        <div class="contact-card contact-wechat">
          <div class="wechat-seller">
            <img
              class="wechat-avatar"
              :src="asset(site.contacts.wechat.avatar)"
              alt="泡泡哥"
              width="56"
              height="56"
            />
            <div>
              <b>{{ site.contacts.wechat.name }}</b>
              <small>主理人 · 亲自选品发货</small>
            </div>
          </div>
          <img
            class="wechat-qr"
            :src="asset(site.contacts.wechat.image)"
            alt="泡泡哥微信二维码"
            width="150"
            height="150"
          />
          <h2>{{ site.contacts.wechat.label }}</h2>
          <p>{{ site.contacts.wechat.tagline }}。扫码加我，获取最新价格、口味与报价。</p>
        </div>

        <div v-if="site.contacts.qq?.number" class="contact-card contact-qq">
          <span class="direct-icon">Q</span>
          <h2>{{ site.contacts.qq.label }}</h2>
          <p>QQ：{{ site.contacts.qq.number }}</p>
          <p>添加泡泡哥 QQ，直接沟通产品、价格与下单。</p>
        </div>
      </div>

      <div class="feature-card">
        <ul>
          <li v-for="feature in features" :key="feature.title">
            <span class="feature-icon"><AppIcon :name="feature.icon" :size="22" /></span>
            <b>{{ feature.title }}</b>
            <small>{{ feature.text }}</small>
          </li>
        </ul>
      </div>

      <div class="notice-card">
        <h2>购买说明</h2>
        <p>
          本站为电子烟产品信息展示站点，不提供在线下单与在线支付。所有商品信息与价格以客服实时确认为准。
          如需了解配送范围、付款方式或退换政策，请先与客服沟通。
        </p>
        <div class="notice-links">
          <RouterLink to="/info/payment">付款方式</RouterLink>
          <RouterLink to="/info/delivery">配送说明</RouterLink>
          <RouterLink to="/info/returns">退换政策</RouterLink>
          <RouterLink to="/info/verification">真假验证</RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.contact-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  margin-bottom: 16px;
}

.contact-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 28px 20px;
  text-align: center;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(17, 58, 93, 0.05);
}

.contact-wechat .wechat-qr {
  display: block;
  width: 150px;
  height: 150px;
  margin-bottom: 16px;
  object-fit: contain;
  border-radius: 8px;
}

.contact-card h2 {
  margin-bottom: 6px;
  font-size: 18px;
  font-weight: 600;
}

.contact-card p {
  font-size: 12px;
  line-height: 1.8;
  color: #999;
}

.direct-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  margin-bottom: 16px;
  font-size: 28px;
  font-weight: 800;
  background: rgba(255, 255, 255, 0.18);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
}

.feature-card {
  padding: 24px;
  margin-bottom: 16px;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(17, 58, 93, 0.05);
}

.feature-card ul {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
}

.feature-card li {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.feature-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  margin-bottom: 10px;
  color: var(--accent);
  background: rgba(252, 60, 45, 0.07);
  border-radius: 50%;
}

.feature-card b {
  font-size: 14px;
  font-weight: 600;
}

.feature-card small {
  margin-top: 2px;
  font-size: 11px;
  color: #999;
}

.notice-card {
  padding: 24px;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(17, 58, 93, 0.05);
}

.notice-card h2 {
  margin-bottom: 10px;
  font-size: 18px;
  font-weight: 600;
}

.notice-card p {
  font-size: 13px;
  line-height: 1.9;
  color: #666;
}

.notice-links {
  display: flex;
  flex-wrap: wrap;
  gap: 18px;
  margin-top: 14px;
  font-size: 12px;
  color: var(--accent);
}

.notice-links a:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .contact-grid {
    grid-template-columns: minmax(0, 1fr);
    gap: 8px;
  }

  .contact-card {
    padding: 20px 16px;
  }

  .feature-card ul {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 18px 8px;
  }

  .notice-card {
    padding: 16px;
  }
}

/* UI UX Pro Max design system overrides */
.seller-intro {
  display: flex;
  align-items: center;
  gap: 28px;
  padding: 28px;
  margin-bottom: 24px;
  color: #ffffff;
  background: linear-gradient(135deg, var(--color-foreground), #0b7a5f);
  border-radius: 28px;
  box-shadow: 0 30px 70px rgba(6, 78, 59, 0.22);
}

.seller-photo {
  flex: 0 0 180px;
  width: 180px;
  height: 180px;
  object-fit: cover;
  border: 3px solid rgba(255, 255, 255, 0.22);
  border-radius: 24px;
}

.seller-copy {
  flex: 1;
  min-width: 0;
}

.seller-eyebrow {
  display: block;
  margin-bottom: 8px;
  font-family: var(--font-heading);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.14em;
  color: #cbe3d6;
}

.seller-copy h2 {
  margin-bottom: 10px;
  font-size: clamp(26px, 3vw, 36px);
  color: #ffffff;
}

.seller-copy p {
  max-width: 680px;
  font-size: 14px;
  line-height: 1.9;
  color: #e7efe9;
}

.contact-grid {
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.wechat-seller {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  margin-bottom: 14px;
  text-align: left;
}

.wechat-avatar {
  flex: 0 0 56px;
  width: 56px;
  height: 56px;
  object-fit: cover;
  border: 2px solid var(--color-border);
  border-radius: 50%;
}

.wechat-seller b {
  display: block;
  font-family: var(--font-heading);
  font-size: 18px;
  color: var(--color-foreground);
}

.wechat-seller small {
  display: block;
  margin-top: 2px;
  font-size: 11px;
  color: var(--color-muted-foreground);
}

.wechat-qr {
  display: block;
  width: 150px;
  height: 150px;
  padding: 6px;
  margin: 0 auto 12px;
  object-fit: contain;
  background: #ffffff;
  border: 1px solid var(--color-border);
  border-radius: 14px;
}

.contact-card {
  padding: 32px 24px;
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 24px;
  box-shadow: var(--shadow-card);
}

.contact-wechat .wechat-qr {
  padding: 8px;
  background: #ffffff;
  border: 1px solid var(--color-border);
  border-radius: 16px;
}

.contact-card h2 {
  font-family: var(--font-heading);
  font-size: 20px;
  color: var(--color-foreground);
}

.contact-card p {
  color: var(--color-muted-foreground);
}

.contact-qq {
  justify-content: center;
  color: var(--color-on-accent);
  background: linear-gradient(135deg, #fb923c, #ea580c);
}

.contact-qq .direct-icon {
  width: 84px;
  height: 84px;
  margin-bottom: 18px;
  font-size: 34px;
  color: var(--color-on-accent);
  border-color: rgba(0, 0, 0, 0.16);
  background: rgba(0, 0, 0, 0.08);
}

.contact-qq h2,
.contact-qq p {
  color: var(--color-on-accent);
}

.contact-qq p:first-of-type {
  font-family: var(--font-heading);
  font-size: 22px;
  font-weight: 700;
}

.contact-qq p + p {
  margin-top: 2px;
}

.feature-card {
  padding: 32px;
  margin-bottom: 20px;
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 24px;
  box-shadow: var(--shadow-card);
}

.feature-icon {
  color: var(--color-primary);
  background: var(--color-muted);
}

.feature-card b {
  font-family: var(--font-heading);
  color: var(--color-foreground);
}

.feature-card small {
  color: var(--color-muted-foreground);
}

.notice-card {
  padding: 32px;
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 24px;
  box-shadow: var(--shadow-card);
}

.notice-card h2 {
  font-family: var(--font-heading);
  font-size: 24px;
  color: var(--color-foreground);
}

.notice-card p {
  color: var(--color-muted-foreground);
}

.notice-links {
  gap: 10px;
  margin-top: 18px;
}

.notice-links a {
  display: inline-flex;
  align-items: center;
  min-height: 34px;
  padding: 0 12px;
  color: var(--color-foreground);
  background: var(--color-muted);
  border-radius: 999px;
}

.notice-links a:hover {
  color: var(--color-primary-strong, #047857);
  text-decoration: none;
}

@media (max-width: 768px) {
  .contact-card,
  .feature-card,
  .notice-card {
    padding: 20px 16px;
    border-radius: 18px;
  }

  .seller-intro {
    flex-direction: column;
    gap: 16px;
    padding: 20px;
    text-align: center;
    border-radius: 20px;
  }

  .seller-photo {
    flex: 0 0 120px;
    width: 120px;
    height: 120px;
    border-radius: 18px;
  }

  .seller-copy h2 {
    font-size: 22px;
  }

  .seller-copy p {
    font-size: 13px;
  }

  .wechat-seller {
    justify-content: center;
  }

  .contact-wechat .wechat-qr {
    width: 130px;
    height: 130px;
  }

  .notice-card h2 {
    font-size: 20px;
  }
}
</style>
