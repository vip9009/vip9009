<script setup>
import { RouterLink } from 'vue-router'
import { site } from '@/data'
import AppIcon from '@/components/AppIcon.vue'
</script>

<template>
  <footer class="footer">
    <div class="footer-main">
      <div class="wrapper footer-grid">
        <div class="footer-brand">
          <RouterLink class="footer-logo" to="/">
            泡泡哥雾化<span class="footer-logo-dot" />
          </RouterLink>
          <p class="footer-tagline">泡泡哥雾化 · 专业电子烟分类目录，正品可验证。所有商品由泡泡哥亲自选品发货。</p>
          <RouterLink class="footer-cta" to="/contact">
            加泡泡哥微信
            <AppIcon name="arrow-right" :size="16" />
          </RouterLink>
          <div class="footer-social">
            <RouterLink to="/contact">加泡泡哥微信</RouterLink>
            <span class="footer-qq">QQ：{{ site.contacts.qq.number }}</span>
          </div>
        </div>

        <section v-for="widget in site.footerWidgets" :key="widget.title" class="footer-widget">
          <h2 class="widget-title">{{ widget.title }}</h2>
          <ul>
            <li v-for="link in widget.links" :key="link.label">
              <RouterLink v-if="link.to" :to="link.to">{{ link.label }}</RouterLink>
              <a v-else-if="link.href" :href="link.href" target="_blank" rel="noopener noreferrer">{{ link.label }}</a>
              <span v-else class="footer-static-link">{{ link.label }}</span>
            </li>
          </ul>
        </section>
      </div>
    </div>

    <div class="footer-bottom-bar">
      <div class="wrapper footer-bottom">
        <div class="footer-bottom-left">
          Copyright &copy; 2026 <RouterLink to="/">泡泡哥雾化</RouterLink>
        </div>
        <div class="footer-bottom-right">
          <span>正品保障 · 全球直邮</span>
          <RouterLink to="/sitemap">网站地图</RouterLink>
          <RouterLink to="/contact">联系我们</RouterLink>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  color: #d1fae5;
  background: var(--color-foreground);
}

.footer-main {
  padding: 56px 0 48px;
}

.footer-grid {
  display: grid;
  grid-template-columns: 1.45fr repeat(4, minmax(0, 1fr));
  gap: 32px;
}

.footer-logo {
  display: inline-flex;
  align-items: flex-start;
  gap: 6px;
  margin-bottom: 14px;
  font-family: var(--font-heading);
  font-size: 30px;
  font-weight: 700;
  line-height: 1;
  color: #ffffff;
  letter-spacing: -0.04em;
}

.footer-logo-dot {
  width: 8px;
  height: 8px;
  background: var(--color-accent);
  border-radius: 50%;
}

.footer-tagline {
  max-width: 280px;
  margin-bottom: 20px;
  font-size: 13px;
  line-height: 1.8;
  color: #a7f3d0;
}

.footer-cta {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 42px;
  padding: 0 16px;
  font-family: var(--font-heading);
  font-size: 13px;
  font-weight: 600;
  color: var(--color-on-accent);
  background: var(--color-accent);
  border-radius: 10px;
  transition: background 0.22s ease, transform 0.22s ease;
}

.footer-cta:hover {
  background: #f97316;
  transform: translateY(-2px);
}

.footer-social {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 16px;
}

.footer-social a,
.footer-qq {
  padding: 6px 10px;
  font-size: 11px;
  color: #a7f3d0;
  border: 1px solid rgba(167, 243, 208, 0.32);
  border-radius: 999px;
  transition: color 0.2s ease, border-color 0.2s ease;
}

.footer-social a:hover {
  color: #ffffff;
  border-color: #ffffff;
}

.footer-qq {
  cursor: text;
  user-select: all;
}

.footer-static-link {
  font-size: 13px;
  color: #d1fae5;
  user-select: all;
}

.widget-title {
  padding-bottom: 14px;
  margin-bottom: 6px;
  font-size: 14px;
  font-weight: 600;
  color: #ffffff;
  border-bottom: 1px solid rgba(167, 243, 208, 0.26);
}

.footer-widget li {
  padding: 9px 0;
}

.footer-widget a {
  font-size: 13px;
  color: #a7f3d0;
  transition: color 0.18s ease;
}

.footer-widget a:hover {
  color: #ffffff;
}

.footer-bottom-bar {
  background: #043a2c;
}

.footer-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  min-height: 68px;
  font-size: 12px;
  color: #a7f3d0;
}

.footer-bottom a {
  color: #ffffff;
}

.footer-bottom a:hover {
  color: var(--color-secondary);
}

.footer-bottom-left a {
  font-weight: 600;
}

.footer-bottom-right {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 18px;
}

@media (max-width: 1024px) {
  .footer-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 36px 24px;
  }

  .footer-brand {
    grid-column: 1 / -1;
  }
}

@media (max-width: 768px) {
  .footer-main {
    padding: 36px 16px 28px;
  }

  .footer-grid {
    gap: 28px 16px;
  }

  .footer-logo {
    font-size: 26px;
  }

  .footer-tagline {
    max-width: none;
  }

  .footer-bottom {
    flex-direction: column;
    align-items: flex-start;
    min-height: 0;
    padding: 18px 16px;
    gap: 10px;
  }

  .footer-bottom-right {
    gap: 14px;
  }
}
</style>
