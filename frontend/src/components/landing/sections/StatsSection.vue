<script setup>
import { useI18n } from "vue-i18n"
const { t } = useI18n()
</script>

<template>
  <section class="stats">
    <div class="stats__item">
      <h2>32</h2>
      <p>{{ t("stats.banks") }}</p>
    </div>

    <div class="stats__item">
      <h2>147</h2>
      <p>{{ t("stats.products") }}</p>
    </div>

    <div class="stats__item">
      <h2>3</h2>
      <p>{{ t("stats.speed") }}</p>
    </div>
  </section>
</template>

<style scoped>
.stats {
  display: flex;
  justify-content: space-between;
  gap: 20px;

  margin-top: -60px;
  padding: 40px;

  background: white;
  border-radius: 20px;

  max-width: 1000px;
  margin-left: auto;
  margin-right: auto;

  box-shadow: 0 10px 40px rgba(0,0,0,0.06);
}

/* ITEM */
.stats__item {
  text-align: center;
  flex: 1;
}

.stats__item h2 {
  font-size: 30px;
  color: #2563eb;
  margin-bottom: 6px;
}

.stats__item p {
  color: #64748b;
  font-size: 14px;
}

/* 📱 MOBILE */
@media (max-width: 768px) {
  .stats {
    flex-direction: column;
    margin-top: 0;
    padding: 20px;
    gap: 12px;
  }
}
</style>