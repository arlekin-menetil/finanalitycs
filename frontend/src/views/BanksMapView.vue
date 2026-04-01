<script setup>

import { useRouter } from "vue-router"
import { useI18n } from "vue-i18n"
import BankMap from "@/components/banks/BankMap.vue"

const router = useRouter()
const { t } = useI18n()

// ==========================================
// 🚀 ACTIONS
// ==========================================

const goToRecommendations = () => {
  router.push("/recommendations")
}

const goToAnalytics = () => {
  router.push("/analytics")
}

</script>


<template>

<div class="page">

  <!-- HEADER -->
  <div class="header">

    <h1>
      🗺 {{ t("map.title") || "Карта банков" }}
    </h1>

    <p class="subtitle">
      {{ t("map.subtitle") || "Найдите ближайшие филиалы и выберите лучший продукт" }}
    </p>

    <!-- 💣 ACTIONS -->
    <div class="actions">

      <button class="primary" @click="goToRecommendations">
        🔥 {{ t("map.findBest") || "Лучшие предложения" }}
      </button>

      <button class="secondary" @click="goToAnalytics">
        📊 {{ t("map.analytics") || "Аналитика" }}
      </button>

    </div>

  </div>

  <!-- MAP -->
  <div class="map-wrapper">
    <BankMap/>
  </div>

</div>

</template>


<style scoped>

/* PAGE */
.page{
max-width:1200px;
margin:auto;
padding:40px;
}

/* HEADER */
.header{
margin-bottom:30px;
}

h1{
font-size:32px;
margin-bottom:8px;
}

.subtitle{
color:#6b7280;
margin-bottom:16px;
font-size:14px;
}

/* ACTIONS */
.actions{
display:flex;
gap:12px;
flex-wrap:wrap;
}

/* BUTTONS */
.primary{
background:#111827;
color:white;
padding:10px 16px;
border:none;
border-radius:10px;
cursor:pointer;
transition:.2s;
}

.primary:hover{
background:#1f2937;
}

.secondary{
background:white;
border:1px solid #d1d5db;
padding:10px 16px;
border-radius:10px;
cursor:pointer;
transition:.2s;
}

.secondary:hover{
background:#f3f4f6;
}

/* MAP */
.map-wrapper{
border-radius:16px;
overflow:hidden;
border:1px solid #e5e7eb;
}

/* MOBILE */
@media (max-width:768px){

.page{
padding:20px;
}

h1{
font-size:24px;
}

}

</style>