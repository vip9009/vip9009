<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { site } from '@/data'

const categories = computed(() =>
  Object.entries(site.categories)
    .filter(([, item]) => !item.parent && item.section)
    .sort((a, b) => (a[1].sort ?? 999) - (b[1].sort ?? 999))
    .map(([id, item]) => ({
      id,
      title: item.title,
      children: (item.children || [])
        .map((childId) => [childId, site.categories[childId]])
        .filter(([, child]) => Boolean(child))
        .sort((a, b) => (a[1].sort ?? 999) - (b[1].sort ?? 999))
        .map(([childId, child]) => ({
          id: childId,
          title: child.title,
          to: `/category/${id}?sub=${childId}`
        }))
    }))
)
const infoPages = computed(() =>
  Object.entries(site.infoPages).map(([slug, item]) => ({ slug, title: item.title }))
)
</script>

<template>
  <div class="sitemap-page">
    <div class="wrapper">
      <nav class="breadcrumb" aria-label="面包屑">
        <RouterLink to="/">首页</RouterLink>
        <span class="sep">/</span>
        <span>网站地图</span>
      </nav>

      <div class="page-head">
        <div>
          <h1 class="page-title">网站地图</h1>
          <p class="page-subtitle">快速找到商品分类与帮助页面</p>
        </div>
      </div>

      <div class="sitemap-grid">
        <section class="content-card">
          <h2>商品分类</h2>
          <ul>
            <li v-for="item in categories" :key="item.id">
              <RouterLink :to="`/category/${item.id}`">{{ item.title }}</RouterLink>
              <ul v-if="item.children.length" class="sitemap-sub">
                <li v-for="child in item.children" :key="child.id">
                  <RouterLink :to="child.to">{{ child.title }}</RouterLink>
                </li>
              </ul>
            </li>
          </ul>
        </section>

        <section class="content-card">
          <h2>帮助中心</h2>
          <ul>
            <li v-for="item in infoPages" :key="item.slug">
              <RouterLink :to="`/info/${item.slug}`">{{ item.title }}</RouterLink>
            </li>
            <li>
              <RouterLink to="/contact">联系我们</RouterLink>
            </li>
          </ul>
        </section>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sitemap-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.content-card h2 {
  padding-bottom: 12px;
  margin-bottom: 6px;
  font-size: 18px;
  font-weight: 600;
  border-bottom: 1px solid #f2f2f2;
}

.content-card li {
  padding: 10px 0;
  border-bottom: 1px dashed #f2f2f2;
}

.sitemap-sub {
  margin: 6px 0 0 16px;
}

.sitemap-sub li {
  padding: 6px 0;
  border-bottom: 0;
}

.sitemap-sub a {
  font-size: 12px;
  color: var(--color-muted-foreground);
}

.content-card li:last-child {
  border-bottom: 0;
}

.content-card a {
  font-size: 13px;
  color: #666;
}

.content-card a:hover {
  color: var(--accent);
}

@media (max-width: 768px) {
  .sitemap-grid {
    grid-template-columns: minmax(0, 1fr);
    gap: 8px;
  }
}

/* UI UX Pro Max design system overrides */
.sitemap-grid {
  gap: 20px;
}

.content-card {
  padding: 28px;
}

.content-card h2 {
  padding-bottom: 14px;
  margin-bottom: 8px;
  font-family: var(--font-heading);
  font-size: 22px;
  color: var(--color-foreground);
  border-bottom-color: var(--color-border);
}

.content-card li {
  padding: 11px 0;
  border-bottom-color: var(--color-border);
}

.content-card a {
  font-size: 14px;
  color: var(--color-muted-foreground);
}

.content-card a:hover {
  color: var(--color-primary-strong, #047857);
}

@media (max-width: 768px) {
  .content-card {
    padding: 20px 18px;
    border-radius: 18px;
  }

  .content-card h2 {
    font-size: 19px;
  }
}
</style>
