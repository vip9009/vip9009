<script setup>
import { computed, watchEffect } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { site } from '@/data'

const route = useRoute()

const page = computed(() => site.infoPages[route.params.slug] || null)
const others = computed(() =>
  Object.entries(site.infoPages)
    .filter(([slug]) => slug !== route.params.slug)
    .map(([slug, item]) => ({ slug, title: item.title }))
)

watchEffect(() => {
  document.title = page.value ? `${page.value.title} - 泡泡哥雾化` : '页面不存在 - 泡泡哥雾化'
})
</script>

<template>
  <div class="info-page">
    <div class="wrapper">
      <nav class="breadcrumb" aria-label="面包屑">
        <RouterLink to="/">首页</RouterLink>
        <span class="sep">/</span>
        <span>{{ page ? page.title : '帮助中心' }}</span>
      </nav>

      <article v-if="page" class="content-card info-card">
        <h1>{{ page.title }}</h1>
        <p v-for="(paragraph, index) in page.paragraphs" :key="index">{{ paragraph }}</p>

        <div class="info-chips">
          <RouterLink v-for="item in others" :key="item.slug" :to="`/info/${item.slug}`">
            {{ item.title }}
          </RouterLink>
        </div>
      </article>

      <div v-else class="empty-state">
        <h3>页面不存在</h3>
        <p>该帮助页面可能已经调整。</p>
        <div class="empty-actions">
          <RouterLink class="btn btn-primary" to="/">返回首页</RouterLink>
          <RouterLink class="btn btn-ghost" to="/contact">联系我们</RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.info-card h1 {
  margin-bottom: 18px;
  font-size: 26px;
  font-weight: 600;
}

.info-card p {
  margin-bottom: 14px;
  font-size: 14px;
  line-height: 2;
  color: #555;
}

.info-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding-top: 16px;
  margin-top: 8px;
  border-top: 1px solid #f2f2f2;
}

.info-chips a {
  display: inline-flex;
  align-items: center;
  height: 32px;
  padding: 0 14px;
  font-size: 12px;
  color: #666;
  background: #f8f9fa;
  border-radius: 20px;
  transition: color 0.18s ease, background 0.18s ease;
}

.info-chips a:hover {
  color: var(--accent);
  background: rgba(252, 60, 45, 0.06);
}

@media (max-width: 768px) {
  .info-card h1 {
    font-size: 20px;
  }

  .info-card p {
    font-size: 13px;
  }
}

/* UI UX Pro Max design system overrides */
.info-card {
  padding: 40px;
  border-radius: 28px;
}

.info-card h1 {
  margin-bottom: 20px;
  font-family: var(--font-heading);
  font-size: clamp(28px, 3.2vw, 40px);
  color: var(--color-foreground);
}

.info-card p {
  margin-bottom: 16px;
  font-size: 15px;
  line-height: 2;
  color: var(--color-muted-foreground);
}

.info-chips {
  gap: 10px;
  padding-top: 20px;
  margin-top: 12px;
  border-top-color: var(--color-border);
}

.info-chips a {
  height: 36px;
  padding: 0 14px;
  color: var(--color-foreground);
  background: var(--color-muted);
  border-radius: 999px;
}

.info-chips a:hover {
  color: var(--color-primary-strong, #047857);
  background: var(--color-border);
}

@media (max-width: 768px) {
  .info-card {
    padding: 20px 18px;
    border-radius: 20px;
  }

  .info-card h1 {
    font-size: 24px;
  }

  .info-card p {
    font-size: 14px;
  }
}
</style>
