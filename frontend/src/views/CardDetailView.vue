<script setup>
import {
  ref,
  computed,
  onMounted,
} from "vue"

import {
  useRoute,
  useRouter,
} from "vue-router"

import api from "@/api/axios"

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const error = ref(null)

const card = ref(null)

// ==========================================
// 💳 RAW
// ==========================================
const raw = computed(() => {
  return card.value?.raw_data || {}
})

// ==========================================
// 💳 STRUCTURED
// ==========================================
const structured = computed(() => {
  return raw.value?.structured || {}
})

// ==========================================
// 🏦 BANK LOGO
// ==========================================
const logo = computed(() => {

  const bank = (
    card.value?.bank_name || ""
  )
    .toLowerCase()
    .replace(/\s+/g, "")

  return `/banks/${bank}.png`
})

// ==========================================
// 💳 CARD TYPE
// ==========================================
const cardSystem = computed(() => {

  return (
    raw.value?.card_system ||
    structured.value?.card_system ||
    "Card"
  )
})

// ==========================================
// 💰 ISSUE COST
// ==========================================
const issueCost = computed(() => {

  return (
    raw.value?.issue_cost ||
    structured.value?.issue_cost ||
    "—"
  )
})

// ==========================================
// 🌍 CURRENCY
// ==========================================
const currency = computed(() => {

  return (
    card.value?.currency ||
    structured.value?.currency ||
    "—"
  )
})

// ==========================================
// 📅 VALIDITY
// ==========================================
const validity = computed(() => {

  return (
    raw.value?.validity_period ||
    structured.value?.validity_period ||
    "—"
  )
})

// ==========================================
// 🚀 LOAD CARD
// ==========================================
async function loadCard() {

  try {

    loading.value = true

    const { data } = await api.get(
      `/products/${route.params.id}/`
    )

    card.value = data

    console.log(
      "💳 CARD:",
      data
    )

  } catch (err) {

    console.error(err)

    error.value =
      err?.response?.data?.detail ||
      "Не удалось загрузить карту"

  } finally {

    loading.value = false
  }
}

// ==========================================
// 🔙 BACK
// ==========================================
function goBack() {
  router.back()
}

// ==========================================
// 🚀 INIT
// ==========================================
onMounted(() => {
  loadCard()
})
</script>

<template>

  <div class="card-detail-page">

    <div
      v-if="loading"
      class="loading"
    >
      Загрузка карты...
    </div>

    <div
      v-else-if="error"
      class="error"
    >
      {{ error }}
    </div>

    <template v-else>

      <!-- BACK -->

      <button
        class="back-btn"
        @click="goBack"
      >
        ← Назад
      </button>

      <!-- HERO -->

      <div class="hero">

        <img
          :src="logo"
          class="logo"
          alt="bank"
        />

        <div class="hero-content">

          <div class="bank">
            {{ card.bank_name }}
          </div>

          <h1>
            {{ card.name }}
          </h1>

        </div>

      </div>

      <!-- STATS -->

      <div class="stats">

        <div class="stat">

          <span>Валюта</span>

          <strong>
            {{ currency }}
          </strong>

        </div>

        <div class="stat">

          <span>Платёжная система</span>

          <strong>
            {{ cardSystem }}
          </strong>

        </div>

        <div class="stat">

          <span>Срок действия</span>

          <strong>
            {{ validity }}
          </strong>

        </div>

        <div class="stat">

          <span>Стоимость выпуска</span>

          <strong>
            {{ issueCost }}
          </strong>

        </div>

      </div>

      <!-- CONDITIONS -->

      <div class="conditions">

        <h2>
          Условия карты
        </h2>

        <div class="conditions-grid">

          <div
            v-if="raw.documents_required"
            class="condition-item"
          >

            <span>Документы</span>

            <strong>
              {{ raw.documents_required }}
            </strong>

          </div>

          <div class="condition-item">

            <span>Онлайн оформление</span>

            <strong>
              {{ card.is_online ? "Да" : "Нет" }}
            </strong>

          </div>

          <div
            v-if="raw.open_methods?.length"
            class="condition-item"
          >

            <span>Способ открытия</span>

            <strong>
              {{ raw.open_methods.join(", ") }}
            </strong>

          </div>

          <div
            v-if="structured.updated_at"
            class="condition-item"
          >

            <span>Последнее обновление</span>

            <strong>
              {{ structured.updated_at }}
            </strong>

          </div>

        </div>

      </div>

      <!-- SOURCE -->

      <div class="source-card">

        <h2>
          Источник
        </h2>

        <div class="source-links">

          <a
            v-if="card.source_url"
            :href="card.source_url"
            target="_blank"
          >
            Перейти к продукту
          </a>

          <a
            v-if="card.bank_url"
            :href="card.bank_url"
            target="_blank"
          >
            Сайт банка
          </a>

        </div>

      </div>

    </template>

  </div>

</template>

<style scoped>

.card-detail-page {

  max-width: 1200px;

  margin: 0 auto;

  display: flex;

  flex-direction: column;

  gap: 24px;
}

/* ===================================== */
/* BACK */
/* ===================================== */

.back-btn {

  width: fit-content;

  background: transparent;

  border: none;

  color: #2563eb;

  font-size: 16px;

  font-weight: 600;

  cursor: pointer;

  padding: 0;
}

/* ===================================== */
/* HERO */
/* ===================================== */

.hero {

  background: white;

  border: 1px solid #e5e7eb;

  border-radius: 24px;

  padding: 32px;

  display: flex;

  align-items: center;

  gap: 24px;
}

.logo {

  width: 72px;

  height: 72px;

  border-radius: 16px;

  object-fit: contain;

  background: #f8fafc;

  padding: 8px;
}

.hero-content {

  display: flex;

  flex-direction: column;

  gap: 8px;
}

.bank {

  color: #64748b;

  font-size: 15px;

  font-weight: 600;
}

.hero h1 {

  margin: 0;

  font-size: 24px;

  font-weight: 700;

  color: #0f172a;
}

/* ===================================== */
/* STATS */
/* ===================================== */

.stats {

  display: grid;

  grid-template-columns: repeat(4, 1fr);

  gap: 16px;
}

.stat {

  background: white;

  border: 1px solid #e5e7eb;

  border-radius: 20px;

  padding: 24px;

  display: flex;

  flex-direction: column;

  gap: 10px;
}

.stat span {

  color: #64748b;

  font-size: 14px;
}

.stat strong {

  font-size: 20px;

  color: #0f172a;
}

/* ===================================== */
/* CONDITIONS */
/* ===================================== */

.conditions {

  background: white;

  border: 1px solid #e5e7eb;

  border-radius: 24px;

  padding: 24px;
}

.conditions h2 {

  margin: 0 0 24px;

  font-size: 20px;

  font-weight: 700;
}

.conditions-grid {

  display: grid;

  grid-template-columns:
    repeat(auto-fit, minmax(240px, 1fr));

  gap: 16px;
}

.condition-item {

  background: #f8fafc;

  border: 1px solid #e5e7eb;

  border-radius: 16px;

  padding: 18px;

  display: flex;

  flex-direction: column;

  gap: 10px;
}

.condition-item span {

  color: #64748b;

  font-size: 14px;
}

.condition-item strong {

  color: #0f172a;

  font-size: 16px;

  font-weight: 700;
}

/* ===================================== */
/* DESCRIPTION */
/* ===================================== */

.description-card {

  background: white;

  border: 1px solid #e5e7eb;

  border-radius: 24px;

  padding: 24px;
}

.description-card h2 {

  margin: 0 0 20px;

  font-size: 20px;

  font-weight: 700;
}

.description {

  margin: 0;

  line-height: 1.8;

  color: #334155;

  white-space: pre-line;
}

/* ===================================== */
/* SOURCE */
/* ===================================== */

.source-card {

  background: white;

  border: 1px solid #e5e7eb;

  border-radius: 24px;

  padding: 24px;
}

.source-card h2 {

  margin: 0 0 20px;

  font-size: 20px;

  font-weight: 700;
}

.source-links {

  display: flex;

  gap: 24px;

  flex-wrap: wrap;
}

.source-links a {

  color: #2563eb;

  text-decoration: none;

  font-weight: 600;
}

.source-links a:hover {

  text-decoration: underline;
}

.hero-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 12px;
  color: #64748b;
  font-size: 15px;
  font-weight: 500;
  flex-wrap: wrap;
}

/* ===================================== */
/* LOADING */
/* ===================================== */

.loading,
.error {

  background: white;

  border-radius: 24px;

  padding: 32px;

  text-align: center;
}

/* ===================================== */
/* MOBILE */
/* ===================================== */

@media (max-width: 992px) {

  .stats {

    grid-template-columns:
      repeat(2, 1fr);
  }
}

@media (max-width: 768px) {

  .hero {

    flex-direction: column;

    align-items: flex-start;
  }

  .stats {

    grid-template-columns: 1fr;
  }

  .conditions-grid {

    grid-template-columns: 1fr;
  }

  .source-links {

    flex-direction: column;
  }

  .hero h1 {

    font-size: 22px;
  }
}

</style>