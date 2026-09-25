<script setup>
import { ref, computed, onMounted } from "vue"
import api from "@/api/axios"

import AnalyticsFilter from "@/components/analytics/AnalyticsFilter.vue"

import { Bar, Line } from "vue-chartjs"
import "chart.js/auto"

// =====================================================
// STATE
// =====================================================

const loading = ref(true)
const error = ref(null)

const products = ref([])
const recommendations = ref([])

const selectedBank = ref("Все банки")

const recommendationsLoaded = ref(false)
const recommendationsError = ref(null)


// =====================================================
// GENERIC HELPERS
// =====================================================

const number = (value, fallback = 0) => {
  if (
    value === null ||
    value === undefined ||
    value === ""
  ) {
    return fallback
  }

  const parsed = Number(value)

  return Number.isFinite(parsed)
    ? parsed
    : fallback
}


const nullableNumber = value => {
  if (
    value === null ||
    value === undefined ||
    value === ""
  ) {
    return null
  }

  const parsed = Number(value)

  return Number.isFinite(parsed)
    ? parsed
    : null
}


const text = (value, fallback = "") => {
  if (
    value === null ||
    value === undefined
  ) {
    return fallback
  }

  return String(value).trim() || fallback
}


const normalizeText = value => {
  return text(value)
    .toLowerCase()
    .replace(/\s+/g, " ")
    .replace(/[«»"']/g, "")
    .trim()
}


// =====================================================
// API RESPONSE HELPERS
// =====================================================

const extractArray = (data, keys = []) => {
  if (Array.isArray(data)) {
    return data
  }

  if (!data || typeof data !== "object") {
    return []
  }

  for (const key of keys) {
    if (Array.isArray(data[key])) {
      return data[key]
    }
  }

  if (data.data && typeof data.data === "object") {
    if (Array.isArray(data.data)) {
      return data.data
    }

    for (const key of keys) {
      if (Array.isArray(data.data[key])) {
        return data.data[key]
      }
    }
  }

  return []
}


// =====================================================
// PRODUCT HELPERS
// =====================================================

const bankName = product => {
  return text(
    product?.bank_name ||
    product?.bank?.name ||
    product?.bankName ||
    product?.bank_title,
    "Неизвестный банк"
  )
}


const productName = product => {
  return text(
    product?.product_name ||
    product?.name ||
    product?.title ||
    product?.product?.name,
    "Без названия"
  )
}


const productId = product => {
  return (
    product?.id ??
    product?.product_id ??
    product?.productId ??
    product?.bank_product_id ??
    null
  )
}


const interestRate = product => {
  const value =
    product?.interest_rate ??
    product?.rate ??
    product?.interest

  return nullableNumber(value)
}


const maxAmount = product => {
  return number(
    product?.max_amount ??
    product?.max_limit ??
    product?.amount_max ??
    product?.maximum_amount ??
    0
  )
}


// =====================================================
// OPENING METHODS
// =====================================================

const isOnline = product => {
  if (product?.is_online !== undefined) {
    return Boolean(product.is_online)
  }

  if (product?.real_online !== undefined) {
    return Boolean(product.real_online)
  }

  if (product?.online !== undefined) {
    return Boolean(product.online)
  }

  if (Array.isArray(product?.open_methods)) {
    return product.open_methods.includes("online")
  }

  if (Array.isArray(product?.opening_methods)) {
    return product.opening_methods.includes("online")
  }

  return false
}


const isBranch = product => {
  if (Array.isArray(product?.open_methods)) {
    return product.open_methods.includes("branch")
  }

  if (Array.isArray(product?.opening_methods)) {
    return product.opening_methods.includes("branch")
  }

  if (product?.is_branch !== undefined) {
    return Boolean(product.is_branch)
  }

  return !isOnline(product)
}


// =====================================================
// RECOMMENDATION NORMALIZATION
// =====================================================

const normalizeScore = value => {
  const parsed = nullableNumber(value)

  if (parsed === null) {
    return null
  }

  // 0.87 -> 87
  if (parsed >= 0 && parsed <= 1) {
    return parsed * 100
  }

  return parsed
}


const normalizeProbability = value => {
  const parsed = nullableNumber(value)

  if (parsed === null) {
    return null
  }

  // 0.32 -> 32
  if (parsed >= 0 && parsed <= 1) {
    return parsed * 100
  }

  return parsed
}


const recommendationBankName = recommendation => {
  return text(
    recommendation?.bank_name ||
    recommendation?.bank?.name ||
    recommendation?.bankName ||
    recommendation?.bank_title,
    ""
  )
}


const recommendationProductName = recommendation => {
  return text(
    recommendation?.product_name ||
    recommendation?.name ||
    recommendation?.title ||
    recommendation?.product?.name,
    ""
  )
}


const recommendationProductId = recommendation => {
  return (
    recommendation?.product_id ??
    recommendation?.productId ??
    recommendation?.bank_product_id ??
    recommendation?.id ??
    null
  )
}


const recommendationRankingScore = recommendation => {
  return normalizeScore(
    recommendation?.ranking_score ??
    recommendation?.rankingScore ??
    recommendation?.score ??
    null
  )
}


const recommendationApproval = recommendation => {
  return normalizeProbability(
    recommendation?.approval_probability ??
    recommendation?.approvalProbability ??
    null
  )
}


const recommendationLimit = recommendation => {
  return nullableNumber(
    recommendation?.loan_limit_hint ??
    recommendation?.recommended_limit ??
    recommendation?.recommended_limit_hint ??
    recommendation?.limit_hint ??
    null
  )
}


// =====================================================
// RECOMMENDATION MATCHING
// =====================================================

const findRecommendation = product => {
  if (!recommendations.value.length) {
    return null
  }

  const pId = productId(product)

  const pBank = normalizeText(bankName(product))
  const pName = normalizeText(productName(product))

  // ---------------------------------------------------
  // 1. Exact product ID
  // ---------------------------------------------------

  if (pId !== null && pId !== undefined) {
    const byId = recommendations.value.find(item => {
      const rId = recommendationProductId(item)

      return (
        rId !== null &&
        rId !== undefined &&
        String(rId) === String(pId)
      )
    })

    if (byId) {
      return byId
    }
  }

  // ---------------------------------------------------
  // 2. Exact bank + exact product
  // ---------------------------------------------------

  const exact = recommendations.value.find(item => {
    const rBank = normalizeText(
      recommendationBankName(item)
    )

    const rName = normalizeText(
      recommendationProductName(item)
    )

    return (
      rBank === pBank &&
      rName === pName
    )
  })

  if (exact) {
    return exact
  }

  // ---------------------------------------------------
  // 3. Exact product name if unique
  // ---------------------------------------------------

  const exactProducts = recommendations.value.filter(item => {
    const rName = normalizeText(
      recommendationProductName(item)
    )

    return (
      rName &&
      pName &&
      rName === pName
    )
  })

  if (exactProducts.length === 1) {
    return exactProducts[0]
  }

  // ---------------------------------------------------
  // 4. Same bank + one name contains the other
  // ---------------------------------------------------

  if (pName.length >= 8) {
    const candidates = recommendations.value.filter(item => {
      const rBank = normalizeText(
        recommendationBankName(item)
      )

      const rName = normalizeText(
        recommendationProductName(item)
      )

      if (!rBank || !rName) {
        return false
      }

      if (rBank !== pBank) {
        return false
      }

      return (
        rName.includes(pName) ||
        pName.includes(rName)
      )
    })

    if (candidates.length === 1) {
      return candidates[0]
    }
  }

  return null
}


// =====================================================
// MERGED PRODUCT DATA
// =====================================================

const mergedProducts = computed(() => {
  return products.value.map(product => {
    const recommendation =
      findRecommendation(product)

    return {
      ...product,

      // -------------------------------------------------
      // MARKET DATA
      // -------------------------------------------------

      market_max_amount: maxAmount(product),

      market_interest_rate:
        interestRate(product),

      // -------------------------------------------------
      // PERSONALIZED AI DATA
      // -------------------------------------------------

      recommendation_found:
        Boolean(recommendation),

      ai_ranking_score:
        recommendation
          ? recommendationRankingScore(recommendation)
          : null,

      approval_probability:
        recommendation
          ? recommendationApproval(recommendation)
          : null,

      recommended_limit:
        recommendation
          ? recommendationLimit(recommendation)
          : null,

      recommendation_priority:
        recommendation
          ? nullableNumber(
              recommendation?.priority
            )
          : null,

      recommendation_featured:
        recommendation
          ? Boolean(
              recommendation?.featured
            )
          : false
    }
  })
})


// =====================================================
// LOAD ANALYTICS
// =====================================================

const loadAnalytics = async () => {
  try {
    loading.value = true
    error.value = null
    recommendationsError.value = null

    recommendationsLoaded.value = false

    // -------------------------------------------------
    // Market data + Recommendation Engine
    // -------------------------------------------------

    const results = await Promise.allSettled([
      api.get("/banks/products/", {
        params: {
          limit: 500
        }
      }),

      api.get("/banks/recommendations/", {
        params: {
          limit: 500
        }
      })
    ])

    // -------------------------------------------------
    // PRODUCTS
    // -------------------------------------------------

    const productsResult = results[0]

    if (
      productsResult.status === "fulfilled"
    ) {
      products.value = extractArray(
        productsResult.value.data,
        [
          "results",
          "products",
          "items"
        ]
      )
    } else {
      console.error(
        "Products loading error:",
        productsResult.reason
      )

      products.value = []

      throw (
        productsResult.reason ||
        new Error(
          "Ошибка загрузки банковских продуктов"
        )
      )
    }

    // -------------------------------------------------
    // RECOMMENDATIONS
    // -------------------------------------------------

    const recommendationsResult = results[1]

    if (
      recommendationsResult.status === "fulfilled"
    ) {
      recommendations.value = extractArray(
        recommendationsResult.value.data,
        [
          "recommendations",
          "results",
          "products",
          "items"
        ]
      )

      recommendationsLoaded.value = true
    } else {
      console.error(
        "Recommendations loading error:",
        recommendationsResult.reason
      )

      recommendations.value = []

      recommendationsLoaded.value = false

      recommendationsError.value =
        recommendationsResult.reason?.response?.data?.detail ||
        "Не удалось загрузить персональные данные Recommendation Engine"
    }

  } catch (err) {
    console.error(
      "Analytics loading error:",
      err
    )

    error.value =
      err?.response?.data?.detail ||
      err?.message ||
      "Ошибка загрузки аналитики"

    products.value = []
    recommendations.value = []

  } finally {
    loading.value = false
  }
}


onMounted(() => {
  loadAnalytics()
})


// =====================================================
// BANK ANALYTICS
// =====================================================

const bankAnalytics = computed(() => {
  const grouped = {}

  mergedProducts.value.forEach(product => {
    const name = bankName(product)

    if (!grouped[name]) {
      grouped[name] = {
        bank_name: name,

        products: 0,

        interest_sum: 0,
        interest_count: 0,

        score_sum: 0,
        score_count: 0,

        approval_sum: 0,
        approval_count: 0,

        recommended_limit_max: 0,
        recommended_limit_sum: 0,
        recommended_limit_count: 0,

        personalized_products: 0,

        online_products: 0,
        branch_products: 0,
        both_products: 0,

        max_limit: 0
      }
    }

    const bank = grouped[name]

    bank.products += 1

    // -------------------------------------------------
    // MARKET INTEREST
    // -------------------------------------------------

    const rate = interestRate(product)

    if (rate !== null) {
      bank.interest_sum += rate
      bank.interest_count += 1
    }

    // -------------------------------------------------
    // PERSONALIZED AI RANKING
    // -------------------------------------------------

    const score =
      product.ai_ranking_score

    if (
      score !== null &&
      score !== undefined &&
      score > 0
    ) {
      bank.score_sum += score
      bank.score_count += 1
    }

    // -------------------------------------------------
    // PERSONALIZED APPROVAL
    // -------------------------------------------------

    const approval =
      product.approval_probability

    if (
      approval !== null &&
      approval !== undefined
    ) {
      bank.approval_sum += approval
      bank.approval_count += 1
    }

    // -------------------------------------------------
    // PERSONALIZED LIMIT
    // -------------------------------------------------

    const recommendedLimit =
      product.recommended_limit

    if (
      recommendedLimit !== null &&
      recommendedLimit !== undefined &&
      recommendedLimit > 0
    ) {
      bank.recommended_limit_sum +=
        recommendedLimit

      bank.recommended_limit_count += 1

      if (
        recommendedLimit >
        bank.recommended_limit_max
      ) {
        bank.recommended_limit_max =
          recommendedLimit
      }
    }

    // -------------------------------------------------
    // PERSONALIZED PRODUCT COUNT
    // -------------------------------------------------

    if (product.recommendation_found) {
      bank.personalized_products += 1
    }

    // -------------------------------------------------
    // OPENING METHODS
    // -------------------------------------------------

    const online = isOnline(product)
    const branch = isBranch(product)

    if (online && branch) {
      bank.both_products += 1
    } else if (online) {
      bank.online_products += 1
    } else {
      bank.branch_products += 1
    }

    // -------------------------------------------------
    // MARKET MAX LIMIT
    // -------------------------------------------------

    const limit = maxAmount(product)

    if (limit > bank.max_limit) {
      bank.max_limit = limit
    }
  })

  return Object.values(grouped)
    .map(bank => ({
      bank_name: bank.bank_name,

      products: bank.products,

      avg_interest:
        bank.interest_count > 0
          ? bank.interest_sum /
            bank.interest_count
          : 0,

      avg_score:
        bank.score_count > 0
          ? bank.score_sum /
            bank.score_count
          : null,

      avg_approval:
        bank.approval_count > 0
          ? bank.approval_sum /
            bank.approval_count
          : null,

      max_recommended_limit:
        bank.recommended_limit_max,

      avg_recommended_limit:
        bank.recommended_limit_count > 0
          ? bank.recommended_limit_sum /
            bank.recommended_limit_count
          : null,

      personalized_products:
        bank.personalized_products,

      online_products:
        bank.online_products,

      branch_products:
        bank.branch_products,

      both_products:
        bank.both_products,

      max_limit:
        bank.max_limit
    }))
    .sort((a, b) => {
      if (b.products !== a.products) {
        return b.products - a.products
      }

      return a.bank_name.localeCompare(
        b.bank_name
      )
    })
})


// =====================================================
// FILTER
// =====================================================

const filteredProducts = computed(() => {
  if (
    !selectedBank.value ||
    selectedBank.value === "Все банки"
  ) {
    return mergedProducts.value
  }

  return mergedProducts.value.filter(
    product =>
      bankName(product) ===
      selectedBank.value
  )
})


const filteredBanks = computed(() => {
  if (
    !selectedBank.value ||
    selectedBank.value === "Все банки"
  ) {
    return bankAnalytics.value
  }

  return bankAnalytics.value.filter(
    bank =>
      bank.bank_name ===
      selectedBank.value
  )
})


// =====================================================
// UNIQUE BANKS
// =====================================================

const uniqueBanks = computed(() => {
  const list = [
    ...new Set(
      bankAnalytics.value.map(
        bank => bank.bank_name
      )
    )
  ].sort((a, b) =>
    a.localeCompare(b)
  )

  return [
    "Все банки",
    ...list
  ]
})


// =====================================================
// KPI
// =====================================================

const totalProducts = computed(() => {
  return filteredProducts.value.length
})


const productsLabel = computed(() => {
  return selectedBank.value === "Все банки"
    ? "Всего продуктов"
    : "Продуктов банка"
})


const averageInterest = computed(() => {
  const rates = filteredProducts.value
    .map(product =>
      interestRate(product)
    )
    .filter(rate => rate !== null)

  if (!rates.length) {
    return "0.00"
  }

  const average =
    rates.reduce(
      (sum, rate) =>
        sum + rate,
      0
    ) / rates.length

  return average.toFixed(2)
})


const maximumLimit = computed(() => {
  if (!filteredProducts.value.length) {
    return 0
  }

  return Math.max(
    ...filteredProducts.value.map(
      product =>
        maxAmount(product)
    )
  )
})


const onlineProducts = computed(() => {
  return filteredProducts.value.filter(
    product =>
      isOnline(product)
  ).length
})


const branchProducts = computed(() => {
  return filteredProducts.value.filter(
    product =>
      isBranch(product) &&
      !isOnline(product)
  ).length
})


const bothProducts = computed(() => {
  return filteredProducts.value.filter(
    product =>
      isOnline(product) &&
      isBranch(product)
  ).length
})


// =====================================================
// PERSONALIZED DATA KPI
// =====================================================

const personalizedProducts = computed(() => {
  return filteredProducts.value.filter(
    product =>
      product.recommendation_found
  ).length
})


const averageRanking = computed(() => {
  const values = filteredProducts.value
    .map(product =>
      product.ai_ranking_score
    )
    .filter(
      value =>
        value !== null &&
        value !== undefined &&
        value > 0
    )

  if (!values.length) {
    return "—"
  }

  const average =
    values.reduce(
      (sum, value) =>
        sum + value,
      0
    ) / values.length

  return Math.round(average)
})


const averageApproval = computed(() => {
  const values = filteredProducts.value
    .map(product =>
      product.approval_probability
    )
    .filter(
      value =>
        value !== null &&
        value !== undefined
    )

  if (!values.length) {
    return "—"
  }

  const average =
    values.reduce(
      (sum, value) =>
        sum + value,
      0
    ) / values.length

  return `${Math.round(average)}%`
})


const maximumRecommendedLimit = computed(() => {
  const values = filteredProducts.value
    .map(product =>
      product.recommended_limit
    )
    .filter(
      value =>
        value !== null &&
        value !== undefined &&
        value > 0
    )

  if (!values.length) {
    return 0
  }

  return Math.max(...values)
})


// =====================================================
// TOP BANKS
// =====================================================

const topBanksByProducts = computed(() => {
  const data =
    selectedBank.value === "Все банки"
      ? bankAnalytics.value
      : filteredBanks.value

  return [...data]
    .sort(
      (a, b) =>
        b.products -
        a.products
    )
    .slice(0, 10)
})


const topBanksByRate = computed(() => {
  const data =
    selectedBank.value === "Все банки"
      ? bankAnalytics.value
      : filteredBanks.value

  return [...data]
    .filter(
      bank =>
        bank.avg_interest > 0
    )
    .sort(
      (a, b) =>
        b.avg_interest -
        a.avg_interest
    )
    .slice(0, 10)
})


const topBanksByLimit = computed(() => {
  const data =
    selectedBank.value === "Все банки"
      ? bankAnalytics.value
      : filteredBanks.value

  return [...data]
    .filter(
      bank =>
        bank.max_limit > 0
    )
    .sort(
      (a, b) =>
        b.max_limit -
        a.max_limit
    )
    .slice(0, 10)
})


const topBanksByAI = computed(() => {
  const data =
    selectedBank.value === "Все банки"
      ? bankAnalytics.value
      : filteredBanks.value

  return [...data]
    .filter(
      bank =>
        bank.avg_score !== null &&
        bank.avg_score > 0
    )
    .sort(
      (a, b) =>
        b.avg_score -
        a.avg_score
    )
    .slice(0, 10)
})


// =====================================================
// FORMAT
// =====================================================

const formatMillions = value => {
  const amount = number(value)

  if (!amount) {
    return 0
  }

  return Math.round(
    amount / 1_000_000
  )
}


const formatMoney = value => {
  const amount = number(value)

  if (!amount) {
    return "0"
  }

  return new Intl.NumberFormat(
    "ru-RU"
  ).format(amount)
}


const formatPercent = value => {
  if (
    value === null ||
    value === undefined
  ) {
    return "—"
  }

  return `${Math.round(value)}%`
}


// =====================================================
// CHART DATA
// =====================================================

const interestData = computed(() => {
  // ---------------------------------------------------
  // ALL BANKS
  // ---------------------------------------------------

  if (
    !selectedBank.value ||
    selectedBank.value === "Все банки"
  ) {
    return {
      labels:
        topBanksByRate.value.map(
          bank =>
            bank.bank_name
        ),

      datasets: [
        {
          label:
            "Средняя ставка (%)",

          data:
            topBanksByRate.value.map(
              bank =>
                Number(
                  bank.avg_interest.toFixed(
                    2
                  )
                )
            )
        }
      ]
    }
  }

  // ---------------------------------------------------
  // ONE BANK
  // ---------------------------------------------------

  const bankProducts =
    filteredProducts.value.filter(
      product =>
        interestRate(product) !== null
    )

  return {
    labels:
      bankProducts.map(product => {
        const name =
          productName(product)

        return name.length > 35
          ? `${name.slice(0, 35)}...`
          : name
      }),

    datasets: [
      {
        label:
          "Процентная ставка (%)",

        data:
          bankProducts.map(
            product =>
              interestRate(product)
          )
      }
    ]
  }
})


const loanData = computed(() => {
  // ---------------------------------------------------
  // ALL BANKS
  // ---------------------------------------------------

  if (
    !selectedBank.value ||
    selectedBank.value === "Все банки"
  ) {
    return {
      labels:
        topBanksByLimit.value.map(
          bank =>
            bank.bank_name
        ),

      datasets: [
        {
          label:
            "Максимальный лимит продукта (млн сум)",

          data:
            topBanksByLimit.value.map(
              bank =>
                formatMillions(
                  bank.max_limit
                )
            )
        }
      ]
    }
  }

  // ---------------------------------------------------
  // ONE BANK
  // ---------------------------------------------------

  const bankProducts =
    filteredProducts.value.filter(
      product =>
        maxAmount(product) > 0
    )

  return {
    labels:
      bankProducts.map(product => {
        const name =
          productName(product)

        return name.length > 35
          ? `${name.slice(0, 35)}...`
          : name
      }),

    datasets: [
      {
        label:
          "Лимит продукта (млн сум)",

        data:
          bankProducts.map(
            product =>
              formatMillions(
                maxAmount(product)
              )
          )
      }
    ]
  }
})


const scoreData = computed(() => {
  const data =
    topBanksByAI.value

  return {
    labels:
      data.map(
        bank =>
          bank.bank_name
      ),

    datasets: [
      {
        label:
          "Средний AI-рейтинг",

        data:
          data.map(
            bank =>
              Number(
                bank.avg_score.toFixed(
                  1
                )
              )
          ),

        tension: 0.35,

        fill: false
      }
    ]
  }
})


// =====================================================
// MARKET STRUCTURE
// =====================================================

const productCountData = computed(() => {
  const data =
    selectedBank.value === "Все банки"
      ? topBanksByProducts.value
      : filteredBanks.value

  return {
    labels:
      data.map(
        bank =>
          bank.bank_name
      ),

    datasets: [
      {
        label:
          "Количество продуктов",

        data:
          data.map(
            bank =>
              bank.products
          )
      }
    ]
  }
})


const openingMethodsData = computed(() => {
  const data =
    selectedBank.value === "Все банки"
      ? topBanksByProducts.value
      : filteredBanks.value

  return {
    labels:
      data.map(
        bank =>
          bank.bank_name
      ),

    datasets: [
      {
        label:
          "Онлайн",

        data:
          data.map(
            bank =>
              bank.online_products
          )
      },

      {
        label:
          "В отделении",

        data:
          data.map(
            bank =>
              bank.branch_products
          )
      },

      {
        label:
          "Онлайн + отделение",

        data:
          data.map(
            bank =>
              bank.both_products
          )
      }
    ]
  }
})


// =====================================================
// CHART OPTIONS
// =====================================================

const chartOptions = {
  responsive: true,

  maintainAspectRatio: false,

  plugins: {
    legend: {
      position: "top"
    }
  },

  scales: {
    x: {
      ticks: {
        maxRotation: 45,
        minRotation: 0
      }
    },

    y: {
      beginAtZero: true
    }
  }
}


// =====================================================
// REFRESH
// =====================================================

const refresh = () => {
  loadAnalytics()
}
</script>


<template>
  <section class="analytics">

    <!-- ================================================= -->
    <!-- HEADER -->
    <!-- ================================================= -->

    <div class="analytics-header">

      <div>
        <h1>
          Аналитика банков
        </h1>

        <p class="analytics-subtitle">
          Анализ банковских продуктов,
          процентных ставок, лимитов
          и персональных показателей
          Recommendation Engine
        </p>
      </div>

      <button
        class="refresh-button"
        type="button"
        @click="refresh"
        :disabled="loading"
      >
        ↻ Обновить
      </button>

    </div>


    <!-- ================================================= -->
    <!-- FILTER -->
    <!-- ================================================= -->

    <AnalyticsFilter
      v-model:selectedBank="selectedBank"
      :uniqueBanks="uniqueBanks"
    />


    <!-- ================================================= -->
    <!-- RECOMMENDATION STATUS -->
    <!-- ================================================= -->

    <div
      v-if="!loading && recommendationsError"
      class="recommendation-warning"
    >
      <div>
        <strong>
          Персональная AI-аналитика временно недоступна
        </strong>

        <span>
          Рыночные данные загружены,
          но ranking score и вероятность одобрения
          для продуктов не рассчитаны.
        </span>
      </div>

      <button
        type="button"
        @click="refresh"
      >
        Повторить
      </button>
    </div>


    <div
      v-else-if="
        !loading &&
        recommendationsLoaded
      "
      class="recommendation-status"
    >
      <span class="status-dot"></span>

      Персональные данные Recommendation Engine:
      {{ personalizedProducts }}
      из {{ totalProducts }}
      продуктов
    </div>


    <!-- ================================================= -->
    <!-- KPI -->
    <!-- ================================================= -->

    <div class="kpi-grid">

      <!-- PRODUCTS -->

      <div class="kpi-card">

        <div class="kpi-label">
          {{ productsLabel }}
        </div>

        <div class="kpi-value">
          {{ totalProducts }}
        </div>

        <div class="kpi-description">
          доступных продуктов
        </div>

      </div>


      <!-- INTEREST -->

      <div class="kpi-card">

        <div class="kpi-label">
          Средняя ставка
        </div>

        <div class="kpi-value">
          {{ averageInterest }}%
        </div>

        <div class="kpi-description">
          по доступным продуктам
        </div>

      </div>


      <!-- MARKET LIMIT -->

      <div class="kpi-card">

        <div class="kpi-label">
          Максимальный лимит
        </div>

        <div class="kpi-value">
          {{ formatMillions(maximumLimit) }}
          млн
        </div>

        <div class="kpi-description">
          максимальная сумма продукта
        </div>

      </div>


      <!-- AI RANKING -->

      <div class="kpi-card">

        <div class="kpi-label">
          AI-рейтинг
        </div>

        <div class="kpi-value">
          {{ averageRanking }}
        </div>

        <div class="kpi-description">
          средний ranking score Recommendation Engine
        </div>

      </div>


      <!-- APPROVAL -->

      <div class="kpi-card">

        <div class="kpi-label">
          Вероятность одобрения
        </div>

        <div class="kpi-value">
          {{ averageApproval }}
        </div>

        <div class="kpi-description">
          персональный прогноз Recommendation Engine
        </div>

      </div>


      <!-- PERSONALIZED LIMIT -->

      <div class="kpi-card">

        <div class="kpi-label">
          Рекомендуемый лимит
        </div>

        <div class="kpi-value">
          {{
            maximumRecommendedLimit
              ? `${formatMillions(maximumRecommendedLimit)} млн`
              : "—"
          }}
        </div>

        <div class="kpi-description">
          максимальный персональный лимит
        </div>

      </div>


      <!-- ONLINE -->

      <div class="kpi-card">

        <div class="kpi-label">
          Онлайн-продукты
        </div>

        <div class="kpi-value">
          {{ onlineProducts }}
        </div>

        <div class="kpi-description">
          доступны онлайн
        </div>

      </div>

    </div>


    <!-- ================================================= -->
    <!-- CHARTS -->
    <!-- ================================================= -->

    <div class="charts-grid">

      <!-- =============================================== -->
      <!-- INTEREST -->
      <!-- =============================================== -->

      <div class="chart-card">

        <div class="chart-header">

          <h2>
            Процентные ставки
          </h2>

          <p>
            Сравнение процентных ставок
            банковских продуктов
          </p>

        </div>

        <div class="chart-container">

          <Bar
            :data="interestData"
            :options="chartOptions"
          />

        </div>

      </div>


      <!-- =============================================== -->
      <!-- LIMIT -->
      <!-- =============================================== -->

      <div class="chart-card">

        <div class="chart-header">

          <h2>
            Кредитные лимиты
          </h2>

          <p>
            Максимальные рыночные суммы
            банковских продуктов
          </p>

        </div>

        <div class="chart-container">

          <Bar
            :data="loanData"
            :options="chartOptions"
          />

        </div>

      </div>


      <!-- =============================================== -->
      <!-- AI RANKING -->
      <!-- =============================================== -->

      <div class="chart-card">

        <div class="chart-header">

          <h2>
            AI-рейтинг банков
          </h2>

          <p>
            Средний ranking score
            Recommendation Engine
          </p>

        </div>

        <div class="chart-container">

          <Line
            :data="scoreData"
            :options="chartOptions"
          />

        </div>

      </div>


      <!-- =============================================== -->
      <!-- PRODUCT COUNT -->
      <!-- =============================================== -->

      <div class="chart-card">

        <div class="chart-header">

          <h2>
            Банковские продукты
          </h2>

          <p>
            Количество доступных
            продуктов по банкам
          </p>

        </div>

        <div class="chart-container">

          <Bar
            :data="productCountData"
            :options="chartOptions"
          />

        </div>

      </div>


      <!-- =============================================== -->
      <!-- OPENING METHODS -->
      <!-- =============================================== -->

      <div class="chart-card chart-card-wide">

        <div class="chart-header">

          <h2>
            Способы оформления
          </h2>

          <p>
            Онлайн, отделение
            или оба варианта
          </p>

        </div>

        <div class="chart-container">

          <Bar
            :data="openingMethodsData"
            :options="chartOptions"
          />

        </div>

      </div>

    </div>


    <!-- ================================================= -->
    <!-- BANK TABLE -->
    <!-- ================================================= -->

    <section class="bank-section">

      <div class="section-header">

        <div>

          <h2>
            Аналитика банков
          </h2>

          <p>
            Рыночные и персональные показатели
            по банковским продуктам
          </p>

        </div>

      </div>


      <div
        v-if="filteredBanks.length"
        class="table-wrapper"
      >

        <table class="analytics-table">

          <thead>

            <tr>

              <th>
                Банк
              </th>

              <th>
                Продуктов
              </th>

              <th>
                Средняя ставка
              </th>

              <th>
                AI-рейтинг
              </th>

              <th>
                Одобрение
              </th>

              <th>
                AI продуктов
              </th>

              <th>
                Онлайн
              </th>

              <th>
                Отделение
              </th>

              <th>
                Макс. лимит
              </th>

              <th>
                Рек. лимит
              </th>

            </tr>

          </thead>


          <tbody>

            <tr
              v-for="bank in filteredBanks"
              :key="bank.bank_name"
            >

              <!-- BANK -->

              <td class="bank-name">
                {{ bank.bank_name }}
              </td>


              <!-- PRODUCTS -->

              <td>
                {{ bank.products }}
              </td>


              <!-- INTEREST -->

              <td>
                {{
                  bank.avg_interest
                    ? bank.avg_interest.toFixed(2)
                    : "—"
                }}%
              </td>


              <!-- AI SCORE -->

              <td>

                {{
                  bank.avg_score !== null &&
                  bank.avg_score !== undefined
                    ? bank.avg_score.toFixed(1)
                    : "—"
                }}

              </td>


              <!-- APPROVAL -->

              <td>

                {{
                  bank.avg_approval !== null
                    ? `${Math.round(
                        bank.avg_approval
                      )}%`
                    : "—"
                }}

              </td>


              <!-- PERSONALIZED PRODUCTS -->

              <td>

                <span
                  v-if="
                    bank.personalized_products > 0
                  "
                  class="ai-badge"
                >
                  {{ bank.personalized_products }}
                </span>

                <span v-else>
                  —
                </span>

              </td>


              <!-- ONLINE -->

              <td>
                {{ bank.online_products }}
              </td>


              <!-- BRANCH -->

              <td>
                {{ bank.branch_products }}
              </td>


              <!-- MARKET LIMIT -->

              <td>

                {{
                  bank.max_limit
                    ? `${formatMillions(
                        bank.max_limit
                      )} млн`
                    : "—"
                }}

              </td>


              <!-- PERSONALIZED LIMIT -->

              <td>

                {{
                  bank.max_recommended_limit
                    ? `${formatMillions(
                        bank.max_recommended_limit
                      )} млн`
                    : "—"
                }}

              </td>

            </tr>

          </tbody>

        </table>

      </div>


      <div
        v-else
        class="empty-state"
      >
        Нет данных для отображения
      </div>

    </section>


    <!-- ================================================= -->
    <!-- LOADING -->
    <!-- ================================================= -->

    <div
      v-if="loading"
      class="state loading"
    >

      <div class="loader"></div>

      <span>
        Загрузка аналитики...
      </span>

    </div>


    <!-- ================================================= -->
    <!-- ERROR -->
    <!-- ================================================= -->

    <div
      v-else-if="error"
      class="state error"
    >

      <div>
        {{ error }}
      </div>

      <button
        type="button"
        @click="refresh"
      >
        Повторить
      </button>

    </div>

  </section>
</template>


<style scoped>
.analytics {
  width: 100%;
  padding: 24px;
  box-sizing: border-box;
}


/* =====================================================
   HEADER
===================================================== */

.analytics-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  margin-bottom: 24px;
}


.analytics-header h1 {
  margin: 0;
  font-size: 30px;
  font-weight: 800;
  color: #111827;
}


.analytics-subtitle {
  margin: 8px 0 0;
  color: #6b7280;
  font-size: 14px;
  line-height: 1.5;
  max-width: 720px;
}


.refresh-button {
  border: 1px solid #dbe2ea;
  background: #ffffff;
  color: #1f2937;
  border-radius: 10px;
  padding: 10px 16px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s ease;
}


.refresh-button:hover {
  transform: translateY(-1px);
  box-shadow:
    0 5px 14px rgba(0, 0, 0, 0.06);
}


.refresh-button:disabled {
  opacity: 0.6;
  cursor: default;
}


/* =====================================================
   RECOMMENDATION STATUS
===================================================== */

.recommendation-status {
  display: flex;
  align-items: center;
  gap: 8px;

  margin-top: 16px;
  padding: 10px 14px;

  border-radius: 10px;

  background: #f0fdf4;
  border: 1px solid #bbf7d0;

  color: #166534;

  font-size: 13px;
  font-weight: 600;
}


.status-dot {
  width: 8px;
  height: 8px;
  flex: 0 0 8px;

  border-radius: 50%;

  background: #22c55e;
}


.recommendation-warning {
  display: flex;
  align-items: center;
  justify-content: space-between;

  gap: 16px;

  margin-top: 16px;
  padding: 14px 16px;

  border-radius: 12px;

  background: #fffbeb;
  border: 1px solid #fde68a;

  color: #92400e;
}


.recommendation-warning > div {
  display: flex;
  flex-direction: column;
  gap: 4px;
}


.recommendation-warning strong {
  font-size: 13px;
}


.recommendation-warning span {
  font-size: 12px;
  color: #a16207;
}


.recommendation-warning button {
  flex: 0 0 auto;

  border: 1px solid #fcd34d;
  background: #ffffff;
  color: #92400e;

  border-radius: 8px;

  padding: 8px 12px;

  cursor: pointer;
  font-weight: 600;
}


/* =====================================================
   KPI
===================================================== */

.kpi-grid {
  display: grid;

  grid-template-columns:
    repeat(4, minmax(0, 1fr));

  gap: 16px;

  margin-top: 24px;
  margin-bottom: 24px;
}


.kpi-card {
  background: #ffffff;

  border: 1px solid #e5e7eb;
  border-radius: 16px;

  padding: 20px;

  min-height: 130px;

  box-sizing: border-box;
}


.kpi-label {
  color: #6b7280;
  font-size: 13px;
  font-weight: 600;
}


.kpi-value {
  margin-top: 10px;

  font-size: 28px;
  line-height: 1;

  font-weight: 800;

  color: #111827;
}


.kpi-description {
  margin-top: 10px;

  color: #9ca3af;

  font-size: 12px;
  line-height: 1.4;
}


/* =====================================================
   CHARTS
===================================================== */

.charts-grid {
  display: grid;

  grid-template-columns:
    repeat(2, minmax(0, 1fr));

  gap: 20px;
}


.chart-card {
  background: #ffffff;

  border: 1px solid #e5e7eb;
  border-radius: 18px;

  padding: 20px;

  min-width: 0;
}


.chart-card-wide {
  grid-column: 1 / -1;
}


.chart-header {
  margin-bottom: 16px;
}


.chart-header h2 {
  margin: 0;

  font-size: 18px;
  font-weight: 750;

  color: #111827;
}


.chart-header p {
  margin: 6px 0 0;

  color: #6b7280;

  font-size: 13px;
}


.chart-container {
  position: relative;
  height: 320px;
}


/* =====================================================
   TABLE
===================================================== */

.bank-section {
  margin-top: 24px;

  background: #ffffff;

  border: 1px solid #e5e7eb;
  border-radius: 18px;

  overflow: hidden;
}


.section-header {
  padding: 20px;

  border-bottom:
    1px solid #e5e7eb;
}


.section-header h2 {
  margin: 0;

  font-size: 20px;
  font-weight: 750;

  color: #111827;
}


.section-header p {
  margin: 6px 0 0;

  color: #6b7280;

  font-size: 13px;
}


.table-wrapper {
  width: 100%;
  overflow-x: auto;
}


.analytics-table {
  width: 100%;
  min-width: 1150px;

  border-collapse: collapse;
}


.analytics-table th,
.analytics-table td {
  padding: 14px 16px;

  text-align: left;

  border-bottom:
    1px solid #f0f2f5;

  font-size: 13px;

  white-space: nowrap;
}


.analytics-table th {
  background: #f9fafb;

  color: #6b7280;

  font-size: 12px;
  font-weight: 700;
}


.analytics-table td {
  color: #374151;
}


.analytics-table tbody tr:hover {
  background: #fafafa;
}


.analytics-table tbody tr:last-child td {
  border-bottom: none;
}


.analytics-table .bank-name {
  font-weight: 700;
  color: #111827;
}


.ai-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;

  min-width: 26px;
  height: 24px;

  padding: 0 7px;

  border-radius: 999px;

  background: #eef2ff;
  color: #4338ca;

  font-size: 12px;
  font-weight: 700;
}


/* =====================================================
   STATES
===================================================== */

.state {
  margin-top: 24px;

  padding: 24px;

  border-radius: 16px;

  text-align: center;
}


.loading {
  display: flex;

  justify-content: center;
  align-items: center;

  gap: 12px;

  background: #f9fafb;

  color: #6b7280;
}


.loader {
  width: 18px;
  height: 18px;

  border:
    2px solid #d1d5db;

  border-top-color:
    #374151;

  border-radius: 50%;

  animation:
    spin 0.8s linear infinite;
}


@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}


.error {
  background: #fef2f2;

  color: #b91c1c;

  display: flex;

  align-items: center;
  justify-content: center;

  gap: 16px;
}


.error button {
  border: 1px solid #fecaca;

  background: #ffffff;

  color: #b91c1c;

  border-radius: 8px;

  padding: 8px 14px;

  cursor: pointer;
}


/* =====================================================
   EMPTY
===================================================== */

.empty-state {
  padding: 40px 20px;

  text-align: center;

  color: #9ca3af;
}


/* =====================================================
   RESPONSIVE
===================================================== */

@media (max-width: 1200px) {
  .kpi-grid {
    grid-template-columns:
      repeat(3, minmax(0, 1fr));
  }
}


@media (max-width: 1100px) {
  .kpi-grid {
    grid-template-columns:
      repeat(2, minmax(0, 1fr));
  }

  .charts-grid {
    grid-template-columns: 1fr;
  }

  .chart-card-wide {
    grid-column: auto;
  }
}


@media (max-width: 700px) {
  .analytics {
    padding: 16px;
  }


  .analytics-header {
    flex-direction: column;
  }


  .analytics-header h1 {
    font-size: 24px;
  }


  .refresh-button {
    width: 100%;
  }


  .recommendation-warning {
    flex-direction: column;
    align-items: stretch;
  }


  .recommendation-warning button {
    width: 100%;
  }


  .kpi-grid {
    grid-template-columns: 1fr;
  }


  .kpi-card {
    min-height: auto;
  }


  .chart-card {
    padding: 16px;
  }


  .chart-container {
    height: 280px;
  }


  .analytics-table {
    min-width: 1150px;
  }
}
</style>