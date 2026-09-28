<script setup>

import { ref, onMounted, computed } from "vue"

import {
  useRoute,
  useRouter,
} from "vue-router"

import { useI18n } from "vue-i18n"

import api from "@/api/axios"

const { t } = useI18n()

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const error = ref(null)

const deposit = ref(null)

// ==========================================
// 💣 RAW DATA
// ==========================================

const raw = computed(() => {
  return deposit.value?.raw_data || {}
})

// ==========================================
// 💣 FORMATTED TERM
// ==========================================

const formattedTerm = computed(() => {

  const term = Number(
    deposit.value?.term
  )

  if (!term) {
    return "-"
  }

  if (term < 12) {

    if (term === 1) {
      return `1 ${t("depositDetail.month")}`
    }

    return `${term} ${t("depositDetail.months")}`
  }

  if (term === 12) {
    return `1 ${t("depositDetail.year")}`
  }

  const years = Math.floor(
    term / 12
  )

  const months = term % 12

  let yearsText = ""

  if (years === 1) {
    yearsText = `1 ${t("depositDetail.year")}`
  } else {
    yearsText = `${years} ${t("depositDetail.years")}`
  }

  if (!months) {
    return yearsText
  }

  const monthsText =
    months === 1
      ? `1 ${t("depositDetail.month")}`
      : `${months} ${t("depositDetail.months")}`

  return `${yearsText} ${monthsText}`
})

// ==========================================
// 💣 BACK
// ==========================================

function goBack() {
  router.back()
}

// ==========================================
// 💣 BANK LOGO
// ==========================================

const logo = computed(() => {

  const bank = (
    deposit.value?.bank_name || ""
  )
    .toLowerCase()
    .replace(/\s+/g, "")

  return `/banks/${bank}.png`
})

// ==========================================
// 💣 EXTRACT FIELD
// ==========================================

function extractField(text, field) {

  if (!text) {
    return "-"
  }

  const escapedField = field.replace(
    /[.*+?^${}()|[\]\\]/g,
    "\\$&"
  )

  const regex = new RegExp(
    `${escapedField}:\\s*(.+?)(?=\\s+[А-ЯЁA-Z][^:]{1,50}:|$)`,
    "iu"
  )

  const match = text.match(regex)

  if (!match?.[1]) {
    return "-"
  }

  return match[1]
    .replace(/\s+/g, " ")
    .trim()
}

// ==========================================
// 💣 PARSED DESCRIPTION
// ==========================================

const depositFields = computed(() => {

  const text =
    deposit.value?.description || ""

  return {

    updated:
      raw.value.updated_at ||
      extractField(
        text,
        "Последнее обновление информации"
      ),

    rate:
      deposit.value?.interest_rate ||
      extractField(
        text,
        "Ставка (%)"
      ),

    minAmount:
      raw.value.amount_min ||
      extractField(
        text,
        "Мин. сумма"
      ),

    maxAmount:
      raw.value.amount_max ||
      extractField(
        text,
        "Макс. сумма"
      ),

    payout:
      raw.value.payment_type ||
      extractField(
        text,
        "Уплата процентов"
      ),

    accrual: extractField(
      text,
      "Начисление процентов"
    ),

    capitalization: extractField(
      text,
      "Капитализация"
    ),

    refill: extractField(
      text,
      "Пополнение вклада"
    ),

    earlyClose: extractField(
      text,
      "Досрочное расторжение"
    ),

    opening: extractField(
      text,
      "Открытие вклада"
    ),

    currency:
      deposit.value?.currency ||
      raw.value.currency ||
      extractField(
        text,
        "Валюта"
      ),
  }
})

// ==========================================
// 💣 LOAD DEPOSIT
// ==========================================

async function loadDeposit() {

  try {

    loading.value = true

    const { data } = await api.get(
      `/banks/products/${route.params.id}/`
    )

    deposit.value = data

    console.log(
      "💰 DEPOSIT:",
      data
    )

    console.log(
      "💰 CURRENCY:",
      data.currency
    )

    console.log(
      "💰 RAW:",
      data.raw_data
    )

  } catch (err) {

    console.error(err)

    error.value =
      err?.response?.data?.detail ||
      t("depositDetail.loadError")

  } finally {

    loading.value = false

  }
}

onMounted(() => {
  loadDeposit()
})

</script>

<template>

  <div class="deposit-detail-page">

    <!-- LOADING -->

    <div
      v-if="loading"
      class="loading"
    >
      {{ t("depositDetail.loading") }}
    </div>

    <!-- ERROR -->

    <div
      v-else-if="error"
      class="error"
    >
      {{ error }}
    </div>

    <!-- NOT FOUND -->

    <div
      v-else-if="!deposit"
      class="error"
    >
      {{ t("depositDetail.notFound") }}
    </div>

    <!-- CONTENT -->

    <template v-else>

      <!-- BACK -->

      <div class="back-wrapper">

        <button
          class="back-btn"
          @click="goBack"
        >
          ← {{ t("common.back") }}
        </button>

      </div>

      <!-- HERO -->

      <div class="hero">

        <img
          :src="logo"
          class="hero-logo"
          alt="bank"
        />

        <div class="hero-content">

          <div class="bank">
            {{ deposit.bank_name }}
          </div>

          <h1>
            {{ deposit.name }}
          </h1>

        </div>

      </div>

      <!-- STATS -->

      <div class="stats">

        <div class="stat-card">

          <span>
            {{ t("depositDetail.interest") }}
          </span>

          <strong>
            {{ deposit.interest_rate || "-" }}%
          </strong>

        </div>

        <div class="stat-card">

          <span>
            {{ t("depositDetail.term") }}
          </span>

          <strong>
            {{ formattedTerm }}
          </strong>

        </div>

        <div class="stat-card">

          <span>
            {{ t("depositDetail.bank") }}
          </span>

          <strong>
            {{ deposit.bank_name }}
          </strong>

        </div>

      </div>

      <!-- CONDITIONS -->

      <div class="section">

        <h2>
          {{ t("depositDetail.conditions") }}
        </h2>

        <div class="details-grid">

          <div class="detail-item">

            <span>
              {{ t("depositDetail.minAmount") }}
            </span>

            <strong>
              {{ raw.amount_min || depositFields.minAmount || "-" }}
            </strong>

          </div>

          <div class="detail-item">

            <span>
              {{ t("depositDetail.currency") }}
            </span>

            <strong>
              {{ depositFields.currency || "-" }}
            </strong>

          </div>

          <div class="detail-item">

            <span>
              {{ t("depositDetail.payout") }}
            </span>

            <strong>
              {{ raw.payment_type || depositFields.payout || "-" }}
            </strong>

          </div>

          <div class="detail-item">

            <span>
              {{ t("depositDetail.accrual") }}
            </span>

            <strong>
              {{ depositFields.accrual }}
            </strong>

          </div>

          <div class="detail-item">

            <span>
              {{ t("depositDetail.capitalization") }}
            </span>

            <strong>
              {{ depositFields.capitalization }}
            </strong>

          </div>

          <div class="detail-item">

            <span>
              {{ t("depositDetail.refill") }}
            </span>

            <strong>
              {{ depositFields.refill }}
            </strong>

          </div>

          <div class="detail-item">

            <span>
              {{ t("depositDetail.earlyClose") }}
            </span>

            <strong>
              {{ depositFields.earlyClose }}
            </strong>

          </div>

          <div class="detail-item">

            <span>
              {{ t("depositDetail.opening") }}
            </span>

            <strong>
              {{ depositFields.opening }}
            </strong>

          </div>

          <div class="detail-item">

            <span>
              {{ t("depositDetail.updated") }}
            </span>

            <strong>
              {{ raw.updated_at || depositFields.updated || "-" }}
            </strong>

          </div>

        </div>

      </div>

      <!-- SOURCE -->

      <div
        v-if="deposit.source_url"
        class="section"
      >

        <h2>
          {{ t("depositDetail.source") }}
        </h2>

        <a
          :href="deposit.source_url"
          target="_blank"
          class="link"
        >
          {{ t("depositDetail.goToProduct") }}
        </a>

      </div>

      <!-- BANK -->

      <div
        v-if="deposit.bank_url"
        class="section"
      >

        <h2>
          {{ t("depositDetail.bankPage") }}
        </h2>

        <a
          :href="deposit.bank_url"
          target="_blank"
          class="link"
        >
          {{ t("depositDetail.openBankWebsite") }}
        </a>

      </div>

    </template>

  </div>

</template>

<style scoped>

.deposit-detail-page {

  max-width: 1200px;

  margin: 0 auto;

  padding: 24px;
}

/* ==========================================
   BACK
========================================== */

.back-wrapper {

  margin-bottom: 20px;
}

.back-btn {

  border: none;

  background: transparent;

  color: #2563eb;

  font-size: 15px;

  font-weight: 700;

  cursor: pointer;

  padding: 0;
}

.back-btn:hover {

  color: #1d4ed8;
}

/* ==========================================
   HERO
========================================== */

.hero {

  background: white;

  border: 1px solid #e5e7eb;

  border-radius: 24px;

  padding: 28px;

  margin-bottom: 24px;

  display: flex;

  align-items: center;

  gap: 20px;
}

.hero-logo {

  width: 72px;

  height: 72px;

  object-fit: contain;

  background: #f8fafc;

  border-radius: 16px;

  padding: 6px;

  flex-shrink: 0;
}

.hero-content {

  flex: 1;
}

.bank {

  color: #64748b;

  font-size: 14px;

  font-weight: 600;

  margin-bottom: 8px;
}

.hero h1 {

  margin: 0;

  color: #111827;

  font-size: 30px;

  font-weight: 800;

  line-height: 1.3;
}

/* ==========================================
   STATS
========================================== */

.stats {

  display: grid;

  grid-template-columns:
    repeat(
      auto-fit,
      minmax(220px,1fr)
    );

  gap: 16px;

  margin-bottom: 24px;
}

.stat-card {

  background: white;

  border: 1px solid #e5e7eb;

  border-radius: 20px;

  padding: 20px;
}

.stat-card span {

  display: block;

  color: #64748b;

  font-size: 13px;

  margin-bottom: 8px;
}

.stat-card strong {

  display: block;

  font-size: 22px;

  font-weight: 800;

  color: #111827;
}

/* ==========================================
   SECTION
========================================== */

.section {

  background: white;

  border: 1px solid #e5e7eb;

  border-radius: 20px;

  padding: 24px;

  margin-bottom: 20px;
}

.section h2 {

  margin: 0 0 16px;

  color: #111827;

  font-size: 20px;

  font-weight: 700;
}

/* ==========================================
   PROPERTIES
========================================== */

.properties {

  display: grid;

  grid-template-columns:
    repeat(
      auto-fit,
      minmax(280px,1fr)
    );

  gap: 16px;
}

.property {

  background: #f8fafc;

  border: 1px solid #e5e7eb;

  border-radius: 16px;

  padding: 16px;
}

.property span {

  display: block;

  color: #64748b;

  font-size: 13px;

  margin-bottom: 8px;
}

.property strong {

  display: block;

  color: #111827;

  font-weight: 700;

  line-height: 1.5;
}

/* ==========================================
   DESCRIPTION
========================================== */

.description {

  white-space: pre-wrap;

  line-height: 1.8;

  color: #334155;
}

/* ==========================================
   LINKS
========================================== */

.link {

  color: #2563eb;

  text-decoration: none;

  font-weight: 600;
}

.link:hover {

  text-decoration: underline;
}

/* ==========================================
   LOADING
========================================== */

.loading,
.error {

  text-align: center;

  padding: 80px;

  font-size: 18px;
}

.error {

  color: #dc2626;
}

/* ==========================================
   DETAILS GRID
========================================== */

.details-grid {

  display: grid;

  grid-template-columns:
    repeat(
      auto-fit,
      minmax(260px, 1fr)
    );

  gap: 16px;
}

.detail-item {

  background: #f8fafc;

  border: 1px solid #e5e7eb;

  border-radius: 16px;

  padding: 18px;

  transition: all .2s ease;
}

.detail-item:hover {

  transform: translateY(-2px);

  border-color: #cbd5e1;
}

.detail-item span {

  display: block;

  color: #64748b;

  font-size: 13px;

  margin-bottom: 8px;
}

.detail-item strong {

  display: block;

  color: #111827;

  font-size: 16px;

  font-weight: 700;

  line-height: 1.5;

  word-break: break-word;
}

/* ==========================================
   MOBILE
========================================== */

@media (max-width: 768px) {

  .deposit-detail-page {

    padding: 16px;
  }

  .hero {

    flex-direction: column;

    align-items: flex-start;
  }

  .hero-logo {

    width: 64px;

    height: 64px;
  }

  .hero h1 {

    font-size: 24px;
  }

  .stats {

    grid-template-columns: 1fr;
  }

  .properties {

    grid-template-columns: 1fr;
  }
}

</style>