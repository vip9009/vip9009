<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { site } from '@/data'
import { asset } from '@/utils'
import AppIcon from '@/components/AppIcon.vue'

const route = useRoute()
const menuOpen = ref(false)
const contactOpen = ref(false)
const copied = ref(false)
const isCheckout = computed(() => ['/checkout', '/cart'].includes(route.path))

let copyTimer = null

function closeAll() {
  menuOpen.value = false
  contactOpen.value = false
}

async function copyQQ() {
  const number = site.contacts.qq?.number
  if (!number) return
  try {
    await navigator.clipboard.writeText(number)
    copied.value = true
    clearTimeout(copyTimer)
    copyTimer = setTimeout(() => {
      copied.value = false
    }, 1600)
  } catch {
    copied.value = false
  }
}

function onKeydown(event) {
  if (event.key === 'Escape') closeAll()
}

watch(contactOpen, (open) => {
  document.body.style.overflow = open ? 'hidden' : ''
})

onMounted(() => {
  document.addEventListener('keydown', onKeydown)
})

onBeforeUnmount(() => {
  document.removeEventListener('keydown', onKeydown)
  document.body.style.overflow = ''
  clearTimeout(copyTimer)
})
</script>

<template>
  <div class="dock" :class="{ 'is-hidden': isCheckout }">
    <Transition name="menu">
      <div v-if="menuOpen" class="dock-menu">
        <button type="button" @click="contactOpen = true; menuOpen = false">在线客服</button>
        <RouterLink to="/contact" @click="closeAll">联系方式</RouterLink>
      </div>
    </Transition>

    <button
      class="dock-fab"
      type="button"
      :aria-label="menuOpen ? '收起菜单' : '打开客服菜单'"
      :aria-expanded="menuOpen"
      @click="menuOpen = !menuOpen"
    >
      <AppIcon :name="menuOpen ? 'close' : 'chat'" :size="24" />
    </button>
  </div>

  <Teleport to="body">
    <Transition name="fade">
      <div v-if="contactOpen" class="contact-modal" role="dialog" aria-modal="true" aria-label="在线客服">
        <button class="contact-mask" type="button" aria-label="关闭" @click="contactOpen = false" />
        <div class="contact-card">
          <div class="contact-head">
            <div>
              <b>{{ site.contacts.wechat.name }}</b>
              <span>{{ site.contacts.wechat.tagline }}</span>
            </div>
            <button type="button" aria-label="关闭" @click="contactOpen = false">
              <AppIcon name="close" :size="20" />
            </button>
          </div>

          <img
            class="contact-avatar"
            :src="asset(site.contacts.wechat.avatar)"
            alt="泡泡哥"
            width="56"
            height="56"
          />
          <img
            class="contact-qr"
            :src="asset(site.contacts.wechat.image)"
            width="210"
            height="210"
            alt="泡泡哥微信二维码"
          />

          <p class="contact-tip">扫码加微信，或直接加 QQ 咨询口味、价格和物流。</p>

          <button class="contact-qq" type="button" @click="copyQQ">
            <span>{{ site.contacts.qq?.label || '泡泡哥 QQ' }}</span>
            <b>{{ site.contacts.qq?.number }}</b>
            <em>{{ copied ? '已复制' : '点击复制' }}</em>
          </button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.dock {
  position: fixed;
  right: 22px;
  bottom: 34px;
  z-index: 120;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 10px;
}

.dock.is-hidden {
  display: none;
}

.dock-fab {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 54px;
  height: 54px;
  color: #ffffff;
  background: var(--color-primary);
  border-radius: 50%;
  box-shadow: 0 14px 30px rgba(230, 0, 126, 0.32);
  transition: transform 0.2s ease, background 0.2s ease;
}

.dock-fab:hover {
  background: #c2006a;
  transform: translateY(-2px);
}

.dock-menu {
  display: flex;
  flex-direction: column;
  min-width: 128px;
  padding: 6px;
  background: #ffffff;
  border: 1px solid #eeeeee;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.16);
}

.dock-menu a,
.dock-menu button {
  padding: 10px 14px;
  font-size: 13px;
  text-align: left;
  color: #444444;
}

.dock-menu a:hover,
.dock-menu button:hover {
  color: #ffffff;
  background: var(--color-primary);
}

.contact-modal {
  position: fixed;
  inset: 0;
  z-index: 300;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.contact-mask {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.58);
}

.contact-card {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: min(100%, 360px);
  padding: 22px;
  background: #ffffff;
  border-radius: 4px;
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.3);
}

.contact-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  width: 100%;
  padding-bottom: 12px;
  margin-bottom: 14px;
  border-bottom: 1px solid #eeeeee;
}

.contact-head b {
  display: block;
  font-size: 15px;
  color: #242125;
}

.contact-head span {
  display: block;
  margin-top: 3px;
  font-size: 11px;
  color: #999999;
}

.contact-head button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  color: #666666;
}

.contact-avatar {
  width: 56px;
  height: 56px;
  margin-bottom: 10px;
  object-fit: cover;
  border-radius: 50%;
}

.contact-qr {
  width: 210px;
  height: 210px;
  object-fit: contain;
}

.contact-tip {
  margin: 10px 0 14px;
  font-size: 12px;
  line-height: 1.6;
  text-align: center;
  color: #777777;
}

.contact-qq {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 10px 12px;
  margin-bottom: 8px;
  background: #f7f7f7;
  border: 1px solid #eeeeee;
}

.contact-qq span {
  font-size: 11px;
  color: #999999;
}

.contact-qq b {
  flex: 1;
  font-size: 14px;
  color: #242125;
  text-align: left;
}

.contact-qq em {
  font-size: 10px;
  font-style: normal;
  color: var(--color-primary);
}

.contact-order {
  width: 100%;
  padding: 11px;
  font-size: 12px;
  font-weight: 700;
  text-align: center;
  color: #ffffff;
  background: #242125;
}

.contact-order:hover {
  background: var(--color-primary);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.menu-enter-active,
.menu-leave-active {
  transition: opacity 0.18s ease, transform 0.18s ease;
}

.menu-enter-from,
.menu-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

@media (max-width: 640px) {
  .dock {
    right: 14px;
    bottom: calc(18px + env(safe-area-inset-bottom));
  }

  .dock-fab {
    width: 50px;
    height: 50px;
  }
}
</style>
