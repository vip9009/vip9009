<script setup>
defineProps({
  name: { type: String, default: 'tag' },
  size: { type: [Number, String], default: 12 },
})
</script>

<template>
  <svg
    class="tag-icon"
    :width="size"
    :height="size"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    stroke-width="2"
    stroke-linecap="round"
    stroke-linejoin="round"
    aria-hidden="true"
  >
    <template v-if="name === 'hot'">
      <circle cx="12" cy="12" r="9" />
      <path d="M8 14s1.5 2 4 2 4-2 4-2" />
      <path d="M9 9h.01M15 9h.01" />
    </template>
    <template v-else-if="name === 'smile'">
      <circle cx="12" cy="12" r="9" />
      <path d="M8 14s1.5 2 4 2 4-2 4-2" />
      <path d="m8 9 2 2M16 9l-2 2" />
    </template>
    <template v-else-if="name === 'bulb'">
      <path d="M9 18h6M10 21h4" />
      <path d="M12 3a6 6 0 0 0-3.5 10.9c.5.4.5 1 .5 1.6V17h6v-1.5c0-.6 0-1.2.5-1.6A6 6 0 0 0 12 3Z" />
    </template>
    <template v-else-if="name === 'seedling'">
      <path d="M12 21v-7" />
      <path d="M12 14c0-4 3-7 7-7 0 4-3 7-7 7Z" />
      <path d="M12 16C8 16 5 13 5 9c4 0 7 3 7 7Z" />
    </template>
    <template v-else-if="name === 'refresh'">
      <path d="M20 12a8 8 0 1 1-2.3-5.7" />
      <path d="M20 4v4h-4" />
    </template>
    <template v-else-if="name === 'snow'">
      <path d="M12 2v20M4.2 7l15.6 10M19.8 7 4.2 17" />
      <path d="m9 4 3 2 3-2M9 20l3-2 3 2" />
      <path d="m4 10 3 1-1 3M20 10l-3 1 1 3" />
    </template>
    <template v-else-if="name === 'fingerprint'">
      <path d="M12 11a2 2 0 0 1 2 2c0 3-.8 5-1.4 7" />
      <path d="M8.5 17c.2-4 1.2-8 3.5-8s3.5 4 3.5 8" />
      <path d="M5 14c.5-6 2.7-10 7-10s6.5 4 7 10" />
    </template>
    <template v-else-if="name === 'target'">
      <circle cx="12" cy="12" r="8" />
      <circle cx="12" cy="12" r="3" />
    </template>
    <template v-else-if="name === 'rocket'">
      <path d="M5 15 3 21l6-2" />
      <path d="M14 4c4 1 6 3 7 7l-7 7-5-5 5-9Z" />
      <circle cx="15" cy="8" r="1.5" />
    </template>
    <template v-else-if="name === 'chip'">
      <rect x="7" y="7" width="10" height="10" rx="2" />
      <path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3" />
    </template>
    <template v-else-if="name === 'globe'">
      <circle cx="12" cy="12" r="9" />
      <path d="M3 12h18M12 3c2.5 2.5 3.8 5.6 3.8 9S14.5 18.5 12 21c-2.5-2.5-3.8-5.6-3.8-9S9.5 5.5 12 3Z" />
    </template>
    <template v-else-if="name === 'gamepad'">
      <path d="M6 8h12a4 4 0 0 1 4 4v1a4 4 0 0 1-7.2 2.4L14 14h-4l-.8 1.4A4 4 0 0 1 2 13v-1a4 4 0 0 1 4-4Z" />
      <path d="M7 11v2M6 12h2M16 11h.01M18 13h.01" />
    </template>
    <template v-else-if="name === 'breath'">
      <circle cx="12" cy="12" r="2.5" />
      <path d="M6.3 6.3a8 8 0 0 0 0 11.4M17.7 6.3a8 8 0 0 1 0 11.4" />
      <path d="M9 9a4 4 0 0 0 0 6M15 9a4 4 0 0 1 0 6" />
    </template>
    <template v-else-if="name === 'swap'">
      <path d="M4 8h13l-3-3M20 16H7l3 3" />
    </template>
    <template v-else-if="name === 'dice'">
      <rect x="4" y="4" width="16" height="16" rx="3" />
      <circle cx="12" cy="12" r="1.2" fill="currentColor" stroke="none" />
    </template>
    <template v-else-if="name === 'battery'">
      <rect x="3" y="7" width="16" height="10" rx="2" />
      <path d="M21 10v4" />
      <path d="M6 10h8v4H6z" fill="currentColor" stroke="none" />
    </template>
    <template v-else-if="name === 'transfer'">
      <path d="M4 8h12l-3-3M20 16H8l3 3" />
      <path d="M4 12h16" />
    </template>
    <template v-else-if="name === 'lines'">
      <rect x="9" y="3" width="6" height="18" rx="3" />
      <path d="M12 7v2" />
    </template>
    <template v-else>
      <path d="M20 13 13 20l-9-9V4h7l9 9Z" />
      <circle cx="8.5" cy="8.5" r="1.5" />
    </template>
  </svg>
</template>

<style scoped>
.tag-icon {
  display: block;
  flex: none;
}
</style>
