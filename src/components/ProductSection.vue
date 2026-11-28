<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import AppIcon from '@/components/AppIcon.vue'
import ProductCard from '@/components/ProductCard.vue'

const props = defineProps({
  section: { type: Object, required: true },
  moreTo: { type: String, required: true }
})

const labels = {
  disposables: 'DISPOSABLES',
  jimu: 'CREATOR KITS',
  pods: 'PODS'
}

const eyebrow = computed(() => labels[props.section.id] || 'COLLECTION')
</script>

<template>
  <section class="product-section home-row">
    <div class="wrapper">
      <div class="section-head">
        <div class="section-heading">
          <span class="section-eyebrow">{{ eyebrow }}</span>
          <h2 class="section-title">{{ section.title }}</h2>
        </div>
        <RouterLink class="more-link" :to="moreTo">
          <span>查看全部</span>
          <span class="more-arrow"><AppIcon name="arrow-right" :size="15" /></span>
        </RouterLink>
      </div>

      <div class="product-grid">
        <ProductCard
          v-for="(product, index) in section.products"
          :key="`${section.id}-${index}`"
          :product="product"
          :section-id="section.id"
          :index="index"
        />
      </div>
    </div>
  </section>
</template>

<style scoped>
.section-head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 24px;
}

.section-heading {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.section-eyebrow {
  font-family: var(--font-heading);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.14em;
  color: var(--color-primary-strong);
}

.section-title {
  font-size: clamp(28px, 3.4vw, 40px);
  font-weight: 600;
  line-height: 1.1;
  color: var(--color-foreground);
}

.more-link {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  flex: 0 0 auto;
  height: 44px;
  padding: 0 8px 0 18px;
  font-family: var(--font-heading);
  font-size: 13px;
  font-weight: 600;
  color: var(--color-foreground);
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 999px;
  transition: color 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease;
}

.more-link:hover {
  color: var(--color-primary-strong);
  border-color: var(--color-primary);
  box-shadow: 0 10px 24px rgba(5, 150, 105, 0.12);
}

.more-arrow {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  color: var(--color-on-accent);
  background: var(--color-accent);
  border-radius: 50%;
}

@media (max-width: 768px) {
  .section-head {
    align-items: center;
    margin-bottom: 16px;
  }

  .section-title {
    font-size: 26px;
  }

  .more-link {
    height: 38px;
    padding: 0 6px 0 12px;
    font-size: 12px;
  }

  .more-arrow {
    width: 24px;
    height: 24px;
  }
}
</style>
