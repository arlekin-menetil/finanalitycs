<script setup>
import { useI18n } from "vue-i18n"
const { t } = useI18n()
</script>

<template>
  <section class="hero">
    <div class="hero__content">
      <h1 class="hero__title">
        {{ t("hero.title") }}
      </h1>

      <p class="hero__subtitle">
        {{ t("hero.subtitle") }}
      </p>
    </div>
  </section>
</template>

<style scoped>
.hero {
  padding: 100px 20px 120px;
  margin-top: 10px;

  background: linear-gradient(135deg, #e0f2fe, #eef2ff);
  border-radius: 20px;

  display: flex;
  align-items: center;
}

/* CONTENT */
.hero__content {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}

/* TITLE */
.hero__title {
  font-size: 42px;
  font-weight: 700;
  margin-bottom: 16px;
  color: #0f172a;
}

/* SUBTITLE */
.hero__subtitle {
  font-size: 18px;
  color: #475569;
  line-height: 1.6;
}

/* 📱 MOBILE */
@media (max-width: 768px) {
  .hero {
    padding: 50px 15px;
  }

  .hero__title {
    font-size: 24px;
  }

  .hero__subtitle {
    font-size: 14px;
  }
}
</style>