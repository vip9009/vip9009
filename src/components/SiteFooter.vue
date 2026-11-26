<script setup>
import { site } from '@/data'
</script>

<template>
  <footer class="footer">
    <div class="wrapper footer-inner">
      <p>Copyright 2026 © VAPEPU</p>
      <div class="pay-marks" aria-label="支付方式">
        <span>微信支付</span>
        <span>支付宝</span>
        <span>银行转账</span>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  margin-top: 48px;
  background: #6d6d6d;
  color: rgba(255, 255, 255, 0.82);
}

.footer-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  min-height: 74px;
  font-size: 12px;
}

.pay-marks {
  display: flex;
  align-items: center;
  gap: 8px;
}

.pay-marks span {
  display: inline-flex;
  align-items: center;
  height: 26px;
  padding: 0 10px;
  font-size: 11px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.35);
  border-radius: 2px;
}

@media (max-width: 640px) {
  .footer-inner {
    flex-direction: column;
    justify-content: center;
    gap: 10px;
    padding: 18px 0;
    text-align: center;
  }
}
</style>
