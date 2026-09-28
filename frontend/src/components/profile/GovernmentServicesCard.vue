<script setup>
import { useI18n } from "vue-i18n"

const { t } = useI18n()

function openGov() {
  window.open(
    "https://my.gov.uz/ru/service/411",
    "_blank",
  )
}

function openInfo() {
  window.open(
    "https://portal.infokredit.uz/login",
    "_blank",
  )
}
</script>

<template>
  <div class="card">
    <div class="header">
      <h2>
        🏛 {{ t("governmentServices.title") }}
      </h2>

      <p>
        {{ t("governmentServices.description") }}
      </p>
    </div>

    <button @click="openGov">
      🏛 {{ t("governmentServices.myGov") }}
    </button>

    <button @click="openInfo">
      📊 {{ t("governmentServices.infokredit") }}
    </button>
  </div>
</template>

<style scoped>
.card {
  background: #fff;
  margin-top: 20px;
  padding: 30px;
  border-radius: 24px;
  box-shadow: 0 12px 32px rgba(15, 23, 42, 0.08);
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.header h2 {
  margin: 0;
  font-size: 26px;
  font-weight: 700;
  color: #0f172a;
}

.header p {
  margin-top: 8px;
  font-size: 15px;
  line-height: 1.6;
  color: #64748b;
}

button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 15px;
  border: none;
  border-radius: 14px;
  background: #2563eb;
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.25s;
}

button:hover {
  background: #1d4ed8;
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(37, 99, 235, 0.25);
}
</style>