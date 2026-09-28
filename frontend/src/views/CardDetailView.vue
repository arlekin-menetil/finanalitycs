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

import { useI18n } from "vue-i18n"

import api from "@/api/axios"

const route = useRoute()
const router = useRouter()

const { t, te } = useI18n()

const loading = ref(true)
const error = ref(null)

const card = ref(null)

// ==========================================
// 💳 RAW DATA
// ==========================================
const raw = computed(() => {
  return card.value?.raw_data || {}
})

// ==========================================
// 💳 STRUCTURED DATA
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
// 💳 CARD SYSTEM
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
// 🌍 TRANSLATE CURRENCY
// ==========================================
const translateCurrency = (value) => {
  if (!value || String(value).trim() === "—") {
    return t("cards.cardDetail.values.empty")
  }

  const key = String(value)
    .trim()
    .toUpperCase()

  const translationKey =
    `cards.cardDetail.values.currencies.${key}`

  return te(translationKey)
    ? t(translationKey)
    : value
}

// ==========================================
// 💳 TRANSLATE CARD SYSTEM
// ==========================================
const translateCardSystem = (value) => {
  if (!value || String(value).trim() === "—") {
    return t("cards.cardDetail.values.empty")
  }

  const key = String(value)
    .trim()
    .toUpperCase()

  const translationKey =
    `cards.cardDetail.values.cardSystems.${key}`

  return te(translationKey)
    ? t(translationKey)
    : value
}

// ==========================================
// 📅 TRANSLATE SIMPLE VALUE
// ==========================================
const translateValue = (value) => {
  if (
    !value ||
    String(value).trim() === "—"
  ) {
    return t("cards.cardDetail.values.empty")
  }

  return value
}

// ==========================================
// 🚪 TRANSLATE OPEN METHODS
// ==========================================
const translateOpenMethods = (methods) => {
  if (!methods?.length) {
    return t(
      "cards.cardDetail.values.notSpecified"
    )
  }

  return methods
    .map((method) => {
      const normalized = String(method)
        .trim()
        .toLowerCase()

      if (normalized === "online") {
        return t(
          "cards.cardDetail.values.online"
        )
      }

      if (
        normalized === "branch" ||
        normalized === "office"
      ) {
        return t(
          "cards.cardDetail.values.branch"
        )
      }

      return method
    })
    .join(", ")
}

// ==========================================
// 📄 TRANSLATE DOCUMENTS
// ==========================================
const translateDocuments = (value) => {
  if (!value) {
    return t(
      "cards.cardDetail.values.notSpecified"
    )
  }

  const text = String(value)
    .trim()
    .toLowerCase()

  if (
    text.includes("паспорт") ||
    text.includes("руз") ||
    text.includes("гражданина")
  ) {
    return t(
      "cards.cardDetail.values.documents.passportUzbekistan"
    )
  }

  return value
}

// ==========================================
// 🚀 LOAD CARD
// ==========================================
async function loadCard() {
  try {
    loading.value = true
    error.value = null

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
      t("cards.cardDetail.loadError")
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

    <!-- LOADING -->

    <div
      v-if="loading"
      class="loading"
    >
      {{ t("cards.cardDetail.loading") }}
    </div>

    <!-- ERROR -->

    <div
      v-else-if="error"
      class="error"
    >
      {{ error }}
    </div>

    <!-- CONTENT -->

    <template v-else>

      <!-- BACK -->

      <button
        class="back-btn"
        @click="goBack"
      >
        ← {{ t("common.back") }}
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

        <!-- CURRENCY -->

        <div class="stat">

          <span>
            {{ t("cards.cardDetail.currency") }}
          </span>

          <strong>
            {{ translateCurrency(currency) }}
          </strong>

        </div>

        <!-- CARD SYSTEM -->

        <div class="stat">

          <span>
            {{ t("cards.cardDetail.cardSystem") }}
          </span>

          <strong>
            {{ translateCardSystem(cardSystem) }}
          </strong>

        </div>

        <!-- VALIDITY -->

        <div class="stat">

          <span>
            {{ t("cards.cardDetail.validity") }}
          </span>

          <strong>
            {{ translateValue(validity) }}
          </strong>

        </div>

        <!-- ISSUE COST -->

        <div class="stat">

          <span>
            {{ t("cards.cardDetail.issueCost") }}
          </span>

          <strong>
            {{ issueCost }}
          </strong>

        </div>

      </div>

      <!-- CONDITIONS -->

      <div class="conditions">

        <h2>
          {{ t("cards.cardDetail.conditions") }}
        </h2>

        <div class="conditions-grid">

          <!-- DOCUMENTS -->

          <div
            v-if="raw.documents_required"
            class="condition-item"
          >

            <span>
              {{ t("cards.cardDetail.documents") }}
            </span>

            <strong>
              {{
                translateDocuments(
                  raw.documents_required
                )
              }}
            </strong>

          </div>

          <!-- ONLINE APPLICATION -->

          <div class="condition-item">

            <span>
              {{ t("cards.cardDetail.onlineApplication") }}
            </span>

            <strong>
              {{
                card.is_online
                  ? t(
                      "cards.cardDetail.values.yes"
                    )
                  : t(
                      "cards.cardDetail.values.no"
                    )
              }}
            </strong>

          </div>

          <!-- OPEN METHODS -->

          <div
            v-if="raw.open_methods?.length"
            class="condition-item"
          >

            <span>
              {{ t("cards.cardDetail.openMethod") }}
            </span>

            <strong>
              {{
                translateOpenMethods(
                  raw.open_methods
                )
              }}
            </strong>

          </div>

          <!-- UPDATED -->

          <div
            v-if="structured.updated_at"
            class="condition-item"
          >

            <span>
              {{ t("cards.cardDetail.updated") }}
            </span>

            <strong>
              {{ structured.updated_at }}
            </strong>

          </div>

        </div>

      </div>

      <!-- SOURCE -->

      <div class="source-card">

        <h2>
          {{ t("cards.cardDetail.source") }}
        </h2>

        <div class="source-links">

          <a
            v-if="card.source_url"
            :href="card.source_url"
            target="_blank"
            rel="noopener noreferrer"
          >
            {{ t("cards.cardDetail.goToProduct") }}
          </a>

          <a
            v-if="card.bank_url"
            :href="card.bank_url"
            target="_blank"
            rel="noopener noreferrer"
          >
            {{ t("cards.cardDetail.bankWebsite") }}
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