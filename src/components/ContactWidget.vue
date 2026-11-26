<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { site } from '@/data'
import { asset } from '@/utils'

const route = useRoute()
const collapsed = ref(false)
const hidden = ref(false)
const isContactPage = computed(() => route.path === '/contact')
let observer = null

onMounted(() => {
  if (window.matchMedia('(max-width: 960px)').matches) {
    collapsed.value = true
  }

  const footer = document.querySelector('.footer-bottom-bar')
  if (footer && 'IntersectionObserver' in window) {
    observer = new IntersectionObserver(
      ([entry]) => {
        hidden.value = entry.isIntersecting
      },
      { rootMargin: '0px 0px -8% 0px' }
    )
    observer.observe(footer)
  }
})

onBeforeUnmount(() => {
  observer?.disconnect()
})
</script>

<template>
  <aside
    class="laovape-contact-qr"
    :class="{ 'is-collapsed': collapsed, 'is-hidden': hidden || isContactPage }"
    aria-label="在线客服"
  >
    <button
      class="laovape-contact-qr__toggle"
      type="button"
      :aria-expanded="!collapsed"
      aria-controls="laovape-contact-qr-list"
      :aria-label="collapsed ? '展开联系方式' : '收起联系方式'"
      @click="collapsed = !collapsed"
    >
      <span class="laovape-contact-qr__toggle-open">收起</span>
      <span class="laovape-contact-qr__toggle-closed">联系客服</span>
    </button>

    <div id="laovape-contact-qr-list" class="laovape-contact-qr__list">
      <div class="laovape-contact-qr__wechat">
        <div class="laovape-contact-qr__wechat-head">
          <img
            class="laovape-contact-qr__avatar"
            :src="asset(site.contacts.wechat.avatar)"
            alt="泡泡哥"
            width="36"
            height="36"
          />
          <span class="laovape-contact-qr__wechat-name">{{ site.contacts.wechat.name }}</span>
        </div>
        <img
          class="laovape-contact-qr__qr"
          :src="asset(site.contacts.wechat.image)"
          width="116"
          height="116"
          alt="泡泡哥微信二维码"
          loading="lazy"
        />
        <span>{{ site.contacts.wechat.tagline }}</span>
      </div>

      <div v-if="site.contacts.qq?.number" class="laovape-contact-qr__qq">
        <span class="laovape-contact-qr__qq-label">{{ site.contacts.qq.label }}</span>
        <span class="laovape-contact-qr__qq-number">{{ site.contacts.qq.number }}</span>
      </div>
    </div>
  </aside>
</template>

<style scoped>
.laovape-contact-qr {
  position: fixed;
  right: 18px;
  bottom: 88px;
  z-index: 99;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
  width: 136px;
  transition: opacity 0.22s ease, transform 0.22s ease, visibility 0.22s;
}

.laovape-contact-qr.is-hidden {
  visibility: hidden;
  opacity: 0;
  pointer-events: none;
  transform: translateY(14px);
}

.laovape-contact-qr__toggle {
  min-width: 62px;
  padding: 7px 12px;
  font-size: 13px;
  font-weight: 700;
  line-height: 1.2;
  color: #fff;
  cursor: pointer;
  background: #e95c0c;
  border: 0;
  border-radius: 20px;
  box-shadow: 0 6px 16px rgba(233, 92, 12, 0.25);
  transition: background 160ms ease, transform 160ms ease, box-shadow 160ms ease;
}

.laovape-contact-qr__toggle:hover {
  color: #fff;
  background: #c94a05;
  transform: translateY(-1px);
  box-shadow: 0 8px 20px rgba(233, 92, 12, 0.3);
}

.laovape-contact-qr__toggle-closed {
  display: none;
}

.laovape-contact-qr__list {
  display: flex;
  flex-direction: column;
  gap: 9px;
  width: 136px;
}

.laovape-contact-qr__wechat {
  box-sizing: border-box;
  width: 136px;
  padding: 9px 9px 10px;
  text-align: center;
  background: rgba(255, 255, 255, 0.98);
  border: 1px solid rgba(32, 37, 42, 0.14);
  border-radius: 16px;
  box-shadow: 0 12px 30px rgba(28, 32, 36, 0.14), 0 2px 8px rgba(28, 32, 36, 0.08);
}

.laovape-contact-qr__wechat-head {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 0 2px 7px;
  margin-bottom: 7px;
  border-bottom: 1px solid var(--color-border);
}

.laovape-contact-qr__avatar {
  display: block;
  flex: 0 0 34px;
  width: 34px;
  height: 34px;
  margin: 0;
  object-fit: cover;
  border: 2px solid var(--color-border);
  border-radius: 50%;
}

.laovape-contact-qr__wechat-name {
  font-family: var(--font-heading);
  font-size: 12px;
  font-weight: 700;
  color: var(--color-foreground);
}

.laovape-contact-qr__wechat .laovape-contact-qr__qr {
  display: block;
  width: 116px;
  height: 116px;
  margin: 0 auto;
  object-fit: contain;
  background: #fff;
  border-radius: 8px;
}

.laovape-contact-qr__wechat > span {
  display: block;
  margin-top: 8px;
  font-size: 14px;
  font-weight: 700;
  line-height: 1.35;
  color: #e95c0c;
}

.laovape-contact-qr.is-collapsed {
  width: auto;
}

.laovape-contact-qr.is-collapsed .laovape-contact-qr__list {
  display: none;
}

.laovape-contact-qr.is-collapsed .laovape-contact-qr__toggle-open {
  display: none;
}

.laovape-contact-qr.is-collapsed .laovape-contact-qr__toggle-closed {
  display: inline;
}

@media (max-width: 960px) {
  .laovape-contact-qr {
    right: 8px;
    bottom: calc(72px + env(safe-area-inset-bottom));
    width: 92px;
  }

  .laovape-contact-qr__toggle {
    min-width: 56px;
    padding: 6px 10px;
    font-size: 12px;
  }

  .laovape-contact-qr__list {
    width: 92px;
    gap: 7px;
  }

  .laovape-contact-qr__wechat {
    width: 92px;
    padding: 6px 6px 7px;
    border-radius: 12px;
  }

  .laovape-contact-qr__wechat-head {
    gap: 5px;
    padding-bottom: 5px;
    margin-bottom: 5px;
  }

  .laovape-contact-qr__avatar {
    flex-basis: 26px;
    width: 26px;
    height: 26px;
  }

  .laovape-contact-qr__wechat-name {
    font-size: 10px;
  }

  .laovape-contact-qr__wechat .laovape-contact-qr__qr {
    width: 78px;
    height: 78px;
    border-radius: 6px;
  }

  .laovape-contact-qr__wechat > span {
    margin-top: 5px;
    font-size: 11px;
  }

.laovape-contact-qr__direct-icon {
    display: none;
  }
}
</style>

<style scoped>
/* UI UX Pro Max design system overrides */
.laovape-contact-qr__toggle {
  min-width: 72px;
  padding: 9px 14px;
  font-family: var(--font-heading);
  font-size: 13px;
  color: var(--color-on-accent);
  background: var(--color-accent);
  border-radius: 12px;
  box-shadow: 0 12px 26px rgba(234, 88, 12, 0.28);
}

.laovape-contact-qr__toggle:hover {
  color: var(--color-on-accent);
  background: #f97316;
  box-shadow: 0 16px 32px rgba(234, 88, 12, 0.34);
}

.laovape-contact-qr__wechat {
  border: 2px solid var(--color-border);
  border-radius: 18px;
  box-shadow: var(--shadow-card);
}

.laovape-contact-qr__wechat > span {
  font-family: var(--font-heading);
  color: var(--color-primary);
}

.laovape-contact-qr__qq {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1px;
  width: 136px;
  min-height: 52px;
  padding: 8px 10px;
  color: #000000;
  background: linear-gradient(135deg, #fb923c, #ea580c);
  border-radius: 14px;
  box-shadow: 0 8px 18px rgba(234, 88, 12, 0.22);
  cursor: text;
  user-select: all;
}

.laovape-contact-qr__qq-label {
  font-family: var(--font-heading);
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.06em;
}

.laovape-contact-qr__qq-number {
  font-family: var(--font-heading);
  font-size: 15px;
  font-weight: 700;
  line-height: 1.2;
}

@media (max-width: 960px) {
  .laovape-contact-qr__toggle {
    min-width: 64px;
    padding: 8px 12px;
    font-size: 12px;
  }

  .laovape-contact-qr__qq {
    width: 92px;
    min-height: 46px;
    padding: 6px 4px;
    border-radius: 10px;
  }

  .laovape-contact-qr__qq-label {
    font-size: 9px;
  }

  .laovape-contact-qr__qq-number {
    font-size: 11px;
  }
}
</style>
