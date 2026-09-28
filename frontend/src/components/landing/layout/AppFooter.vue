<script setup>

import { useI18n } from "vue-i18n"

const { t } = useI18n()

</script>

<template>

<footer class="footer">

  <div class="footer__content">

    <div class="footer__left">

      <h3 class="footer__logo">

        FinAnalytics

      </h3>

      <p class="footer__text">

        {{ t("footer.description") }}

      </p>

    </div>

    <div class="footer__right">

      <h4>

        {{ t("footer.contacts") }}

      </h4>

      <p>

        info@finanalytics.uz

      </p>

      <p>

        {{ t("footer.location") }}

      </p>

    </div>

  </div>

  <div class="footer__bottom">

    © 2026 FinAnalytics.

    {{ t("footer.rights") }}

  </div>

</footer>

</template>

<style scoped>
.footer {
  margin-top: 80px;
  background: #0f172a;
  color: #cbd5f5;
}

/* КОНТЕНТ */
.footer__content {
  max-width: 1200px;
  margin: auto;
  padding: 50px 20px;

  display: flex;
  justify-content: space-between;
  gap: 40px;
}

/* ЛЕВАЯ ЧАСТЬ */
.footer__left {
  max-width: 600px;
}

.footer__logo {
  font-size: 20px;
  font-weight: 700;
  color: #22c55e;
  margin-bottom: 12px;
}

.footer__text {
  font-size: 14px;
  color: #94a3b8;
  line-height: 1.7;
}

/* ПРАВАЯ ЧАСТЬ */
.footer__right h4 {
  color: white;
  margin-bottom: 10px;
  font-size: 14px;
}

.footer__right p {
  font-size: 13px;
  color: #94a3b8;
  margin-bottom: 6px;
}

/* НИЖНЯЯ ЛИНИЯ */
.footer__bottom {
  text-align: center;
  padding: 20px;
  font-size: 12px;
  color: #64748b;

  border-top: 1px solid rgba(255,255,255,0.05);
}

/* 📱 MOBILE */
@media (max-width: 768px) {
  .footer__content {
    flex-direction: column;
    text-align: center;
  }

  .footer__left {
    max-width: 100%;
  }
}
</style>