<script setup>
import { asset } from '@/utils'

const paymentIcons = [1, 2, 3, 4, 5].map((index) => `/images/ui/payment/payment-${index}.svg`)
</script>

<template>
  <footer class="footer">
    <div class="wrapper footer-inner">
      <p class="footer-copy">Copyright 2026 © VAPEPU</p>
      <div class="pay-marks" aria-label="支付方式">
        <span v-for="icon in paymentIcons" :key="icon" class="pay-icon">
          <img :src="asset(icon)" alt="" />
        </span>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  margin-top: 60px;
  color: rgba(255, 255, 255, 0.5);
  background: #5b5b5b;
}

.footer-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  min-height: 74px;
  padding: 10px 0 15px;
  font-size: 14.4px;
}

.footer-copy {
  font-size: 14.4px;
  color: rgba(255, 255, 255, 0.5);
}

.pay-marks {
  display: flex;
  align-items: center;
  gap: 6px;
}

.pay-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 31px;
}

.pay-icon img {
  display: block;
  width: 40px;
  height: 20px;
  object-fit: contain;
}

@media (max-width: 640px) {
  .footer {
    margin-top: 10px;
  }

  .footer-inner {
    flex-direction: column-reverse;
    justify-content: center;
    gap: 8px;
    min-height: 0;
    padding: 10px 0 15px;
    text-align: center;
  }

  .footer-copy {
    font-size: 14.4px;
  }

  .pay-marks {
    justify-content: center;
    margin-top: 10px;
  }
}
</style>
