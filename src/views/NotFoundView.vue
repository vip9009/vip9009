<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="not-found">
    <div class="wrapper">
      <div class="content-card not-found-card">
        <p class="code">404</p>
        <h1>页面不存在</h1>
        <p class="desc">你访问的页面可能已经被删除、移动，或者链接地址有误。</p>
        <div class="actions">
          <RouterLink class="btn btn-primary" to="/">返回首页</RouterLink>
          <RouterLink class="btn btn-ghost" to="/category/hot">浏览热门产品</RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.not-found-card {
  padding: 64px 24px;
  text-align: center;
}

.code {
  margin-bottom: 8px;
  font-size: 64px;
  font-weight: 700;
  line-height: 1;
  color: rgba(252, 60, 45, 0.16);
}

.not-found-card h1 {
  margin-bottom: 10px;
  font-size: 24px;
  font-weight: 600;
}

.desc {
  margin-bottom: 22px;
  font-size: 13px;
  color: #999;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
}

@media (max-width: 768px) {
  .not-found-card {
    padding: 40px 16px;
  }

  .code {
    font-size: 48px;
  }

  .not-found-card h1 {
    font-size: 20px;
  }
}

/* UI UX Pro Max design system overrides */
.not-found-card {
  padding: 80px 24px;
  border-radius: 28px;
}

.code {
  color: var(--color-primary);
  font-family: var(--font-heading);
  font-size: 88px;
  opacity: 0.22;
}

.not-found-card h1 {
  font-family: var(--font-heading);
  font-size: 36px;
  color: var(--color-foreground);
}

.desc {
  color: var(--color-muted-foreground);
}

@media (max-width: 768px) {
  .not-found-card {
    padding: 48px 18px;
    border-radius: 20px;
  }

  .code {
    font-size: 64px;
  }

  .not-found-card h1 {
    font-size: 26px;
  }
}
</style>
