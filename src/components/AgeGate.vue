<script setup>
import { ref } from 'vue'

const STORAGE_KEY = 'paopao-age-ok'
const visible = ref(false)

try {
  visible.value = localStorage.getItem(STORAGE_KEY) !== '1'
} catch {
  visible.value = true
}

function confirmAge() {
  visible.value = false
  try {
    localStorage.setItem(STORAGE_KEY, '1')
  } catch {
    /* ignore */
  }
}

function underAge() {
  alert('本站仅面向已满 18 周岁的成年人。未成年人请立即关闭页面。')
  window.location.href = 'about:blank'
}
</script>

<template>
  <Teleport to="body">
    <Transition name="age-fade">
      <div v-if="visible" class="age-gate" role="dialog" aria-modal="true" aria-label="年龄验证">
        <div class="age-card">
          <span class="age-mark">18+</span>
          <h2>🔞 电子雾化产品</h2>
          <p>本站仅面向已满 18 周岁的成年人。<br />未成年禁止购买和使用。</p>
          <button class="age-confirm" type="button" @click="confirmAge">我已满 18 岁</button>
          <button class="age-deny" type="button" @click="underAge">未满 18 岁，离开</button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.age-gate {
  position: fixed;
  inset: 0;
  z-index: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: rgba(0, 0, 0, 0.72);
}

.age-card {
  width: min(100%, 380px);
  padding: 34px 28px 26px;
  text-align: center;
  background: #ffffff;
  border-top: 6px solid var(--color-primary);
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.35);
}

.age-mark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 62px;
  height: 62px;
  margin-bottom: 14px;
  font-size: 20px;
  font-weight: 900;
  color: #ffffff;
  background: #242125;
  border-radius: 50%;
}

.age-card h2 {
  margin-bottom: 10px;
  font-size: 20px;
  color: #242125;
}

.age-card p {
  margin-bottom: 22px;
  font-size: 13px;
  line-height: 1.7;
  color: #777777;
}

.age-confirm {
  width: 100%;
  height: 46px;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 700;
  color: #ffffff;
  background: var(--color-primary);
}

.age-confirm:hover {
  background: #c2006a;
}

.age-deny {
  width: 100%;
  height: 38px;
  font-size: 12px;
  color: #888888;
}

.age-fade-enter-active,
.age-fade-leave-active {
  transition: opacity 0.25s ease;
}

.age-fade-enter-from,
.age-fade-leave-to {
  opacity: 0;
}
</style>
