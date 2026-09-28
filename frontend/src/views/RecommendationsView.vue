<script setup>

import {
  computed,
  onMounted,
  ref,
} from "vue"

import { useI18n } from "vue-i18n"

import { useRecommendationsStore } from "@/stores/recommendations"

import RecommendationsFilters
  from "@/components/recommendations/RecommendationsFilters.vue"

import RecommendationsGrid
  from "@/components/recommendations/RecommendationsGrid.vue"

import RecommendationsEmpty
  from "@/components/recommendations/RecommendationsEmpty.vue"

const { t } = useI18n()

const store = useRecommendationsStore()

// ==========================================
// FILTER STATE
// ==========================================

const filterType = ref("all")

const sortType = ref("match")

const onlineOnly = ref(false)

const bankFilter = ref("all")

// ==========================================
// LOAD RECOMMENDATIONS
// ==========================================

onMounted(async () => {

  try {

    await store.loadTopBanks(true)

  } catch {

    // Loading errors are handled by the store.
    // No console output here.
  }

})

// ==========================================
// CATEGORY MAP
// ==========================================

const categoryMap = {

  loan: [
    "loan",
  ],

  businessCredit: [
    "business_credit",
    "business",
  ],

  micro: [
    "micro",
  ],

  mortgage: [
    "mortgage",
  ],

  auto: [
    "auto",
  ],

  education: [
    "education",
  ],

  green: [
    "green",
  ],

  overdraft: [
    "overdraft",
  ],

  installment: [
    "installment",
  ],

}

// ==========================================
// FILTERED PRODUCTS
// ==========================================

const filteredItems = computed(() => {

  let items = [
    ...(store.recommendations || [])
  ]

  // ========================================
  // EXCLUDE NON-LOAN PRODUCTS
  // ========================================

  items = items.filter((item) => {

    const productType = String(
      item.product_type || ""
    ).toLowerCase()

    return ![
      "card",
      "credit_card",
      "debit_card",
      "deposit",
    ].includes(productType)

  })

  // ========================================
  // CATEGORY FILTER
  // ========================================

  if (filterType.value !== "all") {

    const allowedTypes =
      categoryMap[filterType.value] || []

    items = items.filter((item) => {

      const productType = String(
        item.product_type || ""
      ).toLowerCase()

      const loanType = String(
        item.loan_type || ""
      ).toLowerCase()

      return (
        allowedTypes.includes(productType) ||
        allowedTypes.includes(loanType)
      )

    })

  }

  // ========================================
  // ONLINE ONLY
  // ========================================

  if (onlineOnly.value) {

    items = items.filter(
      (item) => Boolean(item.is_online)
    )

  }

  // ========================================
  // BANK FILTER
  // ========================================

  if (bankFilter.value !== "all") {

    items = items.filter((item) => {

      const bankName =
        item.bank_name ||
        item.bank?.name ||
        ""

      return bankName === bankFilter.value

    })

  }

  // ========================================
  // SORTING
  // ========================================

  if (sortType.value === "rate") {

    items.sort(
      (a, b) =>
        Number(a.interest_rate ?? 999) -
        Number(b.interest_rate ?? 999)
    )

  } else if (sortType.value === "approval") {

    items.sort(
      (a, b) =>
        Number(b.approval_probability ?? 0) -
        Number(a.approval_probability ?? 0)
    )

  } else if (sortType.value === "limit") {

    items.sort(
      (a, b) =>
        Number(b.loan_limit_hint ?? 0) -
        Number(a.loan_limit_hint ?? 0)
    )

  } else {

    // Keep backend ranking order.
    items.sort(
      (a, b) =>
        Number(b.ranking_score ?? 0) -
        Number(a.ranking_score ?? 0)
    )

  }

  return items

})

// ==========================================
// VISIBLE RECOMMENDATIONS
// ==========================================

const visibleRecommendations = computed(() => {

  return filteredItems.value

})

// ==========================================
// RECOMMENDED BANKS
// ==========================================

const recommendedBanks = computed(() => {

  return (store.topBanks || [])

    .slice(0, 5)

    .map((bank) => ({

      ...bank,

      bank_name:
        bank.bank_name ||
        bank.bank ||
        bank.name ||
        "",

      ranking_score: Number(

        bank.ranking_score ??
        bank.score ??
        0

      ),

    }))

    .filter(
      (bank) => bank.bank_name
    )

})

// ==========================================
// AVAILABLE BANKS
// ==========================================

const availableBanks = computed(() => {

  return [

    ...new Set(

      (store.recommendations || [])

        .map(
          (item) =>
            item.bank_name ||
            item.bank?.name ||
            ""
        )

        .filter(Boolean)

    ),

  ].sort(
    (a, b) =>
      a.localeCompare(
        b,
        undefined,
        {
          sensitivity: "base",
        }
      )
  )

})

// ==========================================
// TOTAL BANKS
// ==========================================

const totalBanks = computed(() => {

  return (
    Number(store.totalBanks || 0) ||
    availableBanks.value.length
  )

})

// ==========================================
// TOTAL PRODUCTS
// ==========================================

const totalProducts = computed(() => {

  return filteredItems.value.length

})

</script>

<template>

  <div class="recommendations-page">

    <!-- ===================================== -->
    <!-- HERO -->
    <!-- ===================================== -->

    <section class="hero">

      <div class="hero-content">

        <div class="hero-left">

          <span class="hero-badge">

            🤖 {{ t("recommendations.hero.badge") }}

          </span>

          <h1>

            {{ t("recommendations.hero.title") }}

          </h1>

          <p>

            {{ t("recommendations.hero.description") }}

          </p>

        </div>


        <div class="hero-stats">

          <div class="stat">

            <strong>
              {{ totalProducts }}
            </strong>

            <span>
              {{ t("recommendations.stats.products") }}
            </span>

          </div>


          <div class="stat">

            <strong>
              {{ totalBanks }}
            </strong>

            <span>
              {{ t("recommendations.stats.banks") }}
            </span>

          </div>

        </div>

      </div>

    </section>


    <!-- ===================================== -->
    <!-- PERSONAL AI RECOMMENDED BANKS -->
    <!-- ===================================== -->

    <section
      v-if="recommendedBanks.length"
      class="top-banks"
    >

      <div class="section-head">

        <h2>

          🤖
          {{ t("recommendations.sections.recommendedBanks") }}

        </h2>

      </div>


      <div class="banks-row">

        <div
          v-for="bank in recommendedBanks"
          :key="`recommended-${bank.bank_name}`"
          class="bank-chip recommended-bank"
        >

          <div class="bank-chip-content">

            <span class="bank-chip-name">

              {{ bank.bank_name }}

            </span>

            <span class="bank-chip-offers">

              {{ t("recommendations.aiRating") }}:

              {{ Math.round(bank.ranking_score) }}

            </span>

          </div>

        </div>

      </div>

    </section>


    <!-- ===================================== -->
    <!-- FILTERS -->
    <!-- ===================================== -->

    <RecommendationsFilters

      v-model:filterType="filterType"

      v-model:sortType="sortType"

      v-model:onlineOnly="onlineOnly"

      v-model:bankFilter="bankFilter"

      :availableBanks="availableBanks"

    />


    <!-- ===================================== -->
    <!-- EMPTY -->
    <!-- ===================================== -->

    <RecommendationsEmpty

      v-if="
        !store.loading.recommendations &&
        !visibleRecommendations.length
      "

      :title="t('recommendations.empty')"

      :description="
        t(
          'recommendations.recommendationsGrid.emptyDescription'
        )
      "

      icon="🏦"

    />


    <!-- ===================================== -->
    <!-- GRID -->
    <!-- ===================================== -->

    <RecommendationsGrid

      v-else

      :items="visibleRecommendations"

      :loading="store.loading.recommendations"

    />

  </div>

</template>

<style scoped>

.recommendations-page {
  padding: 32px;
}

/* ==========================================
   HERO
========================================== */

.hero {
  margin-bottom: 38px;
}

.hero-content {
  position: relative;
  overflow: hidden;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 30px;
  padding: 42px;
  border-radius: 36px;
  background:
    linear-gradient(
      135deg,
      #2563eb,
      #1d4ed8,
      #1e40af
    );
  color: white;
}

.hero-content::before {
  content: "";
  position: absolute;
  inset: 0;
  background:
    radial-gradient(
      circle at top right,
      rgba(255, 255, 255, .15),
      transparent 35%
    );
}

.hero-left {
  position: relative;
  z-index: 2;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border-radius: 999px;
  background:
    rgba(255, 255, 255, .12);
  font-size: 12px;
  font-weight: 800;
  letter-spacing: .08em;
  backdrop-filter: blur(10px);
}

.hero h1 {
  margin: 20px 0 0;
  font-size: 52px;
  font-weight: 900;
  line-height: 1;
}

.hero p {
  margin-top: 18px;
  font-size: 17px;
  opacity: .92;
  max-width: 760px;
  line-height: 1.8;
}

/* ==========================================
   STATS
========================================== */

.hero-stats {
  position: relative;
  z-index: 2;
  display: flex;
  gap: 18px;
}

.stat {
  min-width: 140px;
  padding: 24px;
  border-radius: 26px;
  background:
    rgba(255, 255, 255, .12);
  backdrop-filter: blur(12px);
  border:
    1px solid
    rgba(255, 255, 255, .12);
}

.stat strong {
  display: block;
  font-size: 34px;
  font-weight: 900;
  margin-bottom: 10px;
}

.stat span {
  font-size: 14px;
  opacity: .9;
}

/* ==========================================
   TOP BANKS
========================================== */

.top-banks {
  margin-bottom: 32px;
}

.section-head {
  margin-bottom: 18px;
}

.section-head h2 {
  margin: 0;
  font-size: 26px;
  font-weight: 900;
}

.banks-row {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
}

.bank-chip {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 18px;
  border-radius: 20px;
  background: white;
  border:
    1px solid
    #e2e8f0;
  box-shadow:
    0 8px 20px
    rgba(0, 0, 0, .04);
  transition: .2s ease;
}

.bank-chip:hover {
  transform:
    translateY(-2px);
  box-shadow:
    0 12px 24px
    rgba(0, 0, 0, .08);
}

/* ==========================================
   PERSONAL AI BANK
========================================== */

.recommended-bank {
  border:
    1px solid
    rgba(37, 99, 235, .16);
  box-shadow:
    0 10px 24px
    rgba(37, 99, 235, .08);
}

.recommended-bank:hover {
  border-color:
    rgba(37, 99, 235, .30);
  box-shadow:
    0 14px 28px
    rgba(37, 99, 235, .12);
}

.bank-chip-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.bank-chip-name {
  font-weight: 800;
  color: #0f172a;
  font-size: 15px;
}

.bank-chip-offers {
  font-size: 12px;
  color: #64748b;
  font-weight: 700;
}

/* ==========================================
   MOBILE
========================================== */

@media (max-width: 900px) {

  .recommendations-page {
    padding: 18px;
  }

  .hero-content {
    padding: 28px;
    flex-direction: column;
    align-items: flex-start;
  }

  .hero h1 {
    font-size: 38px;
  }

  .hero-stats {
    width: 100%;
  }

  .stat {
    flex: 1;
  }

  .banks-row {
    gap: 10px;
  }

  .bank-chip {
    width: 100%;
  }

}

</style>