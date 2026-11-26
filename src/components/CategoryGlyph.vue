<script setup>
defineProps({
  name: { type: String, default: 'disposable' }
})
</script>

<template>
  <svg class="glyph" viewBox="0 0 120 120" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <ellipse cx="60" cy="102" rx="28" ry="5" fill="rgba(0,0,0,0.06)" stroke="none" />

    <g v-if="name === 'disposable'">
      <rect x="48" y="28" width="24" height="62" rx="7" />
      <path d="M52 28v-6h16v6" />
      <path d="M52 82h16" />
      <path d="M42 90c8 4 28 4 36 0" />
      <path d="M54 44h12M54 50h8" />
    </g>

    <g v-else-if="name === 'pod'">
      <rect x="34" y="30" width="20" height="58" rx="6" />
      <rect x="66" y="30" width="20" height="58" rx="6" />
      <path d="M39 30v-6h10v6M71 30v-6h10v6" />
      <path d="M38 46h12M70 46h12" />
      <path d="M30 88c12 4 48 4 60 0" />
    </g>

    <g v-else-if="name === 'box'">
      <rect x="42" y="26" width="34" height="64" rx="8" />
      <rect x="52" y="18" width="14" height="10" rx="4" />
      <circle cx="59" cy="54" r="6" />
      <path d="M48 70h22" />
      <path d="M34 90c14 4 38 4 52 0" />
    </g>

    <g v-else-if="name === 'gbxl'">
      <rect x="36" y="26" width="48" height="64" rx="4" />
      <rect x="44" y="38" width="32" height="14" rx="2" />
      <path d="M44 60h32M44 66h32M44 72h20" />
      <path d="M44 82h32" />
      <path d="M32 90c16 4 40 4 56 0" />
    </g>

    <g v-else-if="name === 'device'">
      <rect x="52" y="18" width="16" height="70" rx="8" />
      <path d="M56 18v-6h8v6" />
      <path d="M55 40h10M55 46h6" />
      <path d="M40 92c10 4 30 4 40 0" />
    </g>

    <g v-else-if="name === 'liquid'">
      <path d="M50 34h20v8l6 8v38a6 6 0 0 1-6 6H50a6 6 0 0 1-6-6V50l6-8v-8Z" />
      <path d="M52 30h16v4H52z" />
      <path d="M48 60h24M48 68h16" />
      <path d="M38 92c12 4 32 4 44 0" />
    </g>

    <g v-else-if="name === 'combo'">
      <path d="M36 52 58 40l24 12-24 12-22-12Z" />
      <path d="M36 52v22l22 12V64" />
      <path d="M82 52v22L60 86V64" />
      <path d="M52 34l10 6M66 30l12 8" />
      <path d="M30 92c16 4 44 4 60 0" />
    </g>

    <g v-else-if="name === 'promo'" class="promo">
      <path d="M62 22c14 4 26 16 30 30l-18 6-18 18-6-18-6-18 18-18Z" />
      <circle cx="70" cy="44" r="6" />
      <path d="M50 70l-12 12 16-2 2 16 10-14" />
      <path d="M30 30l4 8M24 44l8 3M44 24l3 8" />
    </g>
  </svg>
</template>

<style scoped>
.glyph {
  display: block;
  width: 100%;
  height: 100%;
  color: #242125;
}

.promo {
  color: var(--color-primary);
}
</style>
