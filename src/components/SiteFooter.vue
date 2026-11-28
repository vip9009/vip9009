<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <footer class="footer">
    <div class="wrapper footer-inner">
      <p class="footer-copy">Copyright 2026 © VAPEPU</p>
      <RouterLink class="footer-contact" to="/contact">微信 / QQ 联系客服</RouterLink>
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

.footer-contact {
  font-size: 14.4px;
  color: rgba(255, 255, 255, 0.5);
}

.footer-contact:hover {
  color: #ffffff;
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

  .footer-copy,
  .footer-contact {
    font-size: 14.4px;
  }
}
</style>
