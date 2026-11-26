<script setup>
import { RouterLink } from 'vue-router'
import LottieBox from '@/components/LottieBox.vue'
import { asset } from '@/utils'
</script>

<template>
  <div class="wrapper activity-page">
    <div class="sale-anim">
      <LottieBox src="/animations/sale-tag.json" label="优惠活动 SALE 动画" />
    </div>

    <div class="activity-title">
      <span />
      <h1>优惠活动</h1>
      <span />
    </div>

    <div class="activity-banners">
      <RouterLink class="banner" to="/category/disposables">
        <img :src="asset('/images/activity/2pack.webp')" alt="2 支包邮，混搭满 ¥138 包邮" />
      </RouterLink>
      <RouterLink class="banner" to="/category/combo">
        <img :src="asset('/images/activity/combo.webp')" alt="组合专区立减 50%" />
      </RouterLink>
    </div>
  </div>
</template>

<style scoped>
.activity-page {
  padding-top: 30px;
  padding-bottom: 40px;
}

.sale-anim {
  width: 100%;
  height: 300px;
}

.activity-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  max-width: 1050px;
  margin: 0 auto 30px;
}

.activity-title span {
  flex: 1;
  height: 1px;
  background: #e2e2e2;
}

.activity-title h1 {
  font-size: 18px;
  font-weight: 400;
  color: #666666;
  white-space: nowrap;
}

.activity-banners {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 20px;
  max-width: 1050px;
  margin: 0 auto;
}

.banner {
  display: block;
  border: 1px solid #cfcfcf;
  background: #ffffff;
  transition: border-color 0.18s ease, transform 0.18s ease;
}

.banner:hover {
  border-color: var(--color-primary);
  transform: translateY(-2px);
}

.banner img {
  display: block;
  width: 100%;
  height: auto;
}

@media (max-width: 900px) {
  .activity-page {
    padding-top: 18px;
  }

  .sale-anim {
    height: 150px;
  }

  .activity-title {
    margin-bottom: 18px;
  }

  .activity-banners {
    grid-template-columns: minmax(0, 1fr);
    gap: 12px;
  }
}
</style>
