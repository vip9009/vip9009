<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { site } from '@/data'
import { asset } from '@/utils'
import AppIcon from '@/components/AppIcon.vue'

const route = useRoute()
const collapsed = ref(true)
const sheetOpen = ref(false)
const hidden = ref(false)
const isContactPage = computed(() => route.path === '/contact')
let observer = null

function onKeydown(event) {
  if (event.key === 'Escape' && sheetOpen.value) {
    sheetOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('keydown', onKeydown)
  const footer = document.querySelector('.footer') || document.querySelector('.footer-bottom-bar')
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
  document.removeEventListener('keydown', onKeydown)
  document.body.style.overflow = ''
})

watch(sheetOpen, (open) => {
  document.body.style.overflow = open ? 'hidden' : ''
})
</script>

<template>
  <aside
    class="contact-dock"
    :class="{ 'is-hidden': hidden || isContactPage }"
    aria-label="在线客服"
  >
    <div class="contact-dock__bar">
      <button type="button" class="dock-btn dock-btn--wx" @click="sheetOpen = true">
        <AppIcon name="chat" :size="18" />
        微信咨询
      </button>
      <RouterLink class="dock-btn dock-btn--shop" to="/category/hot">
        <AppIcon name="blocks" :size="18" />
        全部商品
      </RouterLink>
    </div>

    <div class="contact-panel" :class="{ 'is-collapsed': collapsed }">
      <button
        class="contact-panel__toggle"
        type="button"
        :aria-expanded="!collapsed"
        aria-controls="contact-panel-body"
        @click="collapsed = !collapsed"
      >
        {{ collapsed ? '联系泡泡哥' : '收起' }}
      </button>

      <div id="contact-panel-body" class="contact-panel__body">
        <div class="contact-panel__head">
          <img
            class="contact-panel__avatar"
            :src="asset(site.contacts.wechat.avatar)"
            alt="泡泡哥"
            width="36"
            height="36"
          />
          <span>{{ site.contacts.wechat.name }}</span>
        </div>
        <img
          class="contact-panel__qr"
          :src="asset(site.contacts.wechat.image)"
          width="116"
          height="116"
          alt="泡泡哥微信二维码"
          loading="lazy"
        />
        <span class="contact-panel__tagline">{{ site.contacts.wechat.tagline }}</span>
        <div v-if="site.contacts.qq?.number" class="contact-panel__qq">
          <span>{{ site.contacts.qq.label }}</span>
          <b>{{ site.contacts.qq.number }}</b>
        </div>
      </div>
    </div>
  </aside>

  <Teleport to="body">
    <Transition name="sheet">
      <div v-if="sheetOpen" class="contact-sheet" role="dialog" aria-modal="true" aria-label="微信咨询">
        <button class="contact-sheet__mask" type="button" aria-label="关闭" @click="sheetOpen = false" />
        <div class="contact-sheet__panel">
          <div class="contact-sheet__head">
            <span>加泡泡哥微信</span>
            <button type="button" aria-label="关闭" @click="sheetOpen = false">
              <AppIcon name="close" :size="20" />
            </button>
          </div>
          <div class="contact-sheet__body">
            <img
              class="contact-sheet__avatar"
              :src="asset(site.contacts.wechat.avatar)"
              alt="泡泡哥"
              width="52"
              height="52"
            />
            <b>{{ site.contacts.wechat.name }}</b>
            <img
              class="contact-sheet__qr"
              :src="asset(site.contacts.wechat.image)"
              width="200"
              height="200"
              alt="泡泡哥微信二维码"
            />
            <p>{{ site.contacts.wechat.tagline }}</p>
            <div v-if="site.contacts.qq?.number" class="contact-sheet__qq">
              <span>{{ site.contacts.qq.label }}</span>
              <b>{{ site.contacts.qq.number }}</b>
            </div>
            <button class="contact-sheet__done" type="button" @click="sheetOpen = false">
              我加好了
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.contact-dock {
  position: fixed;
  right: 18px;
  bottom: 24px;
  z-index: 99;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
  transition: opacity 0.22s ease, transform 0.22s ease, visibility 0.22s;
}

.contact-dock.is-hidden {
  visibility: hidden;
  opacity: 0;
  pointer-events: none;
  transform: translateY(14px);
}

.contact-dock__bar {
  display: none;
}

.contact-panel {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
  width: 148px;
}

.contact-panel__toggle {
  min-width: 84px;
  padding: 10px 14px;
  font-family: var(--font-heading);
  font-size: 13px;
  font-weight: 600;
  line-height: 1.2;
  color: var(--color-on-accent);
  background: var(--color-accent);
  border-radius: 12px;
  box-shadow: 0 12px 26px rgba(232, 93, 4, 0.28);
  transition: background 0.16s ease, transform 0.16s ease;
}

.contact-panel__toggle:hover {
  background: #f97316;
  transform: translateY(-1px);
}

.contact-panel.is-collapsed .contact-panel__body {
  display: none;
}

.contact-panel__body {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  width: 148px;
  padding: 10px;
  text-align: center;
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  box-shadow: var(--shadow-card);
}

.contact-panel__head {
  display: flex;
  align-items: center;
  gap: 7px;
  width: 100%;
  padding: 0 2px 8px;
  border-bottom: 1px solid var(--color-border);
}

.contact-panel__avatar {
  display: block;
  flex: 0 0 30px;
  width: 30px;
  height: 30px;
  object-fit: cover;
  border-radius: 50%;
}

.contact-panel__head span {
  font-family: var(--font-heading);
  font-size: 12px;
  font-weight: 600;
  color: var(--color-foreground);
}

.contact-panel__qr {
  display: block;
  width: 118px;
  height: 118px;
  object-fit: contain;
  background: #fff;
  border-radius: 8px;
}

.contact-panel__tagline {
  font-size: 12px;
  font-weight: 600;
  line-height: 1.4;
  color: var(--color-accent);
}

.contact-panel__qq {
  display: flex;
  flex-direction: column;
  gap: 1px;
  width: 100%;
  padding: 7px 8px;
  color: #ffffff;
  background: var(--color-primary);
  border-radius: 10px;
  user-select: all;
}

.contact-panel__qq span {
  font-size: 9px;
  letter-spacing: 0.06em;
  opacity: 0.8;
}

.contact-panel__qq b {
  font-family: var(--font-heading);
  font-size: 13px;
  line-height: 1.2;
}

/* Mobile bottom dock */
@media (max-width: 960px) {
  .contact-dock {
    right: 12px;
    bottom: calc(10px + env(safe-area-inset-bottom));
    left: 12px;
    align-items: stretch;
  }

  .contact-panel {
    display: none;
  }

  .contact-dock__bar {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    padding: 8px;
    background: rgba(247, 243, 234, 0.94);
    border: 1px solid var(--color-border);
    border-radius: 16px;
    box-shadow: 0 14px 34px rgba(11, 61, 46, 0.18);
    backdrop-filter: blur(10px);
  }

  .dock-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 7px;
    min-height: 46px;
    font-family: var(--font-heading);
    font-size: 14px;
    font-weight: 600;
    border-radius: 11px;
  }

  .dock-btn--wx {
    color: #ffffff;
    background: var(--color-primary);
  }

  .dock-btn--shop {
    color: var(--color-foreground);
    background: var(--color-card);
    border: 1px solid var(--color-border);
  }
}

/* Mobile QR sheet */
.contact-sheet {
  position: fixed;
  inset: 0;
  z-index: 210;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

.contact-sheet__mask {
  position: absolute;
  inset: 0;
  background: rgba(8, 25, 19, 0.6);
}

.contact-sheet__panel {
  position: relative;
  width: 100%;
  max-width: 520px;
  padding: 18px 20px calc(20px + env(safe-area-inset-bottom));
  background: var(--color-card);
  border-radius: 24px 24px 0 0;
  box-shadow: 0 -18px 50px rgba(8, 25, 19, 0.28);
}

.contact-sheet__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 12px;
  font-family: var(--font-heading);
  font-size: 16px;
  font-weight: 600;
  border-bottom: 1px solid var(--color-border);
}

.contact-sheet__head button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  color: var(--color-foreground);
  background: var(--color-muted);
  border-radius: 10px;
}

.contact-sheet__body {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding-top: 16px;
}

.contact-sheet__avatar {
  width: 52px;
  height: 52px;
  object-fit: cover;
  border: 2px solid var(--color-border);
  border-radius: 50%;
}

.contact-sheet__body > b {
  font-family: var(--font-heading);
  font-size: 15px;
  color: var(--color-foreground);
}

.contact-sheet__qr {
  width: 200px;
  height: 200px;
  margin: 4px 0;
  object-fit: contain;
  border-radius: 12px;
}

.contact-sheet__body p {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-accent);
}

.contact-sheet__qq {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  color: var(--color-muted-foreground);
  background: var(--color-muted);
  border-radius: 999px;
  user-select: all;
}

.contact-sheet__qq b {
  font-family: var(--font-heading);
  color: var(--color-foreground);
}

.contact-sheet__done {
  width: 100%;
  min-height: 48px;
  margin-top: 8px;
  font-family: var(--font-heading);
  font-size: 15px;
  font-weight: 600;
  color: #ffffff;
  background: var(--color-primary);
  border-radius: 12px;
}

.sheet-enter-active,
.sheet-leave-active {
  transition: opacity 0.22s ease;
}

.sheet-enter-active .contact-sheet__panel,
.sheet-leave-active .contact-sheet__panel {
  transition: transform 0.24s ease;
}

.sheet-enter-from,
.sheet-leave-to {
  opacity: 0;
}

.sheet-enter-from .contact-sheet__panel,
.sheet-leave-to .contact-sheet__panel {
  transform: translateY(100%);
}
</style>
