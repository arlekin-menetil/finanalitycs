<script setup>

import { ref, computed, onMounted, watch } from "vue"
import { useI18n } from "vue-i18n"

import api from "@/api/axios"



import AnalyticsFilter from "@/components/analytics/AnalyticsFilter.vue"



import { Bar, Line } from "vue-chartjs"

import "chart.js/auto"

const { t, locale } = useI18n()



// =====================================================

// STATE

// =====================================================



const loading = ref(true)

const error = ref(null)



const products = ref([])

const recommendations = ref([])



const allBanksLabel = computed(() => t("analytics.allBanks"))
const selectedBank = ref(allBanksLabel.value)

watch(locale, (newLocale, oldLocale) => {
  const labels = {
    ru: "Все банки",
    en: "All Banks",
    uz: "Barcha banklar",
  }

  if (selectedBank.value === labels[oldLocale]) {
    selectedBank.value = labels[newLocale] || allBanksLabel.value
  }
})



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

    t("analytics.unknownBank")

  )

}





const productName = product => {

  return text(

    product?.product_name ||

    product?.name ||

    product?.title ||

    product?.product?.name,

    t("analytics.untitled")

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



const toBoolean = value => {
  if (typeof value === "boolean") {
    return value
  }

  if (typeof value === "number") {
    return value !== 0
  }

  if (typeof value === "string") {
    const normalized = value.trim().toLowerCase()

    if (["true", "1", "yes", "y", "on", "online"].includes(normalized)) {
      return true
    }

    if (["false", "0", "no", "n", "off", "offline", ""].includes(normalized)) {
      return false
    }
  }

  return Boolean(value)
}


const isOnline = product => {
  if (product?.is_online_credit !== undefined) {
    return toBoolean(product.is_online_credit)
  }

  if (product?.is_online !== undefined) {
    return toBoolean(product.is_online)
  }

  if (product?.real_online !== undefined) {
    return toBoolean(product.real_online)
  }

  if (product?.online !== undefined) {
    return toBoolean(product.online)
  }

  const methods = [
    ...(Array.isArray(product?.open_methods) ? product.open_methods : []),
    ...(Array.isArray(product?.opening_methods) ? product.opening_methods : []),
  ].map(value => String(value).trim().toLowerCase())

  return methods.some(method =>
    ["online", "onlayn", "онлайн"].includes(method)
  )
}


const isBranch = product => {
  const methods = [
    ...(Array.isArray(product?.open_methods) ? product.open_methods : []),
    ...(Array.isArray(product?.opening_methods) ? product.opening_methods : []),
  ].map(value => String(value).trim().toLowerCase())

  if (
    methods.some(method =>
      ["branch", "office", "offline", "filial", "отделение"].includes(method)
    )
  ) {
    return true
  }

  if (product?.is_branch !== undefined) {
    return toBoolean(product.is_branch)
  }

  if (product?.is_offline !== undefined) {
    return toBoolean(product.is_offline)
  }

  if (product?.offline !== undefined) {
    return toBoolean(product.offline)
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

          limit: 1000

        }

      }),



      api.get("/banks/recommendations/", {

        params: {

          limit: 1000

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



      products.value = []



      throw (

        productsResult.reason ||

        new Error(

          t("analytics.errors.products")

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



      recommendations.value = []



      recommendationsLoaded.value = false



      recommendationsError.value =

        recommendationsResult.reason?.response?.data?.detail ||

        t("analytics.errors.recommendations")

    }



  } catch (err) {



    error.value =

      err?.response?.data?.detail ||

      err?.message ||

      t("analytics.errors.analytics")



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

    selectedBank.value === allBanksLabel.value

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

    selectedBank.value === allBanksLabel.value

  ) {

    return bankAnalytics.value

  }



  return bankAnalytics.value.filter(

    bank =>

      bank.bank_name ===

      selectedBank.value

  )

})





const totalBanks = computed(() => {
  return bankAnalytics.value.length
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

    allBanksLabel.value,

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

  return selectedBank.value === allBanksLabel.value

    ? t("analytics.kpi.totalProducts")

    : t("analytics.kpi.bankProducts")

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

    selectedBank.value === allBanksLabel.value

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

    selectedBank.value === allBanksLabel.value

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

    selectedBank.value === allBanksLabel.value

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

    selectedBank.value === allBanksLabel.value

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



  const localeMap = {
    ru: "ru-RU",
    en: "en-US",
    uz: "uz-UZ",
  }

  return new Intl.NumberFormat(
    localeMap[locale.value] || "ru-RU"
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

    selectedBank.value === allBanksLabel.value

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

            t("analytics.charts.avgRate"),



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

          t("analytics.charts.rate"),



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

    selectedBank.value === allBanksLabel.value

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

            t("analytics.charts.maxProductLimit"),



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

          t("analytics.charts.productLimit"),



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

          t("analytics.charts.avgAiRating"),



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

    selectedBank.value === allBanksLabel.value

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

          t("analytics.charts.productCount"),



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

    selectedBank.value === allBanksLabel.value

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

          t("analytics.opening.online"),



        data:

          data.map(

            bank =>

              bank.online_products

          )

      },



      {

        label:

          t("analytics.opening.branch"),



        data:

          data.map(

            bank =>

              bank.branch_products

          )

      },



      {

        label:

          t("analytics.opening.both"),



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

  animation: {
    duration: 350,
  },

  interaction: {
    intersect: false,
    mode: "index",
  },

  plugins: {
    legend: {
      position: "top",
    },
  },

  scales: {
    x: {
      ticks: {
        autoSkip: true,
        maxTicksLimit: 10,
        maxRotation: 45,
        minRotation: 0,
      },
    },

    y: {
      beginAtZero: true,
      ticks: {
        precision: 0,
      },
    },
  },
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

          {{ t("analytics.title") }}

        </h1>



        <p class="analytics-subtitle">
          {{ t("analytics.subtitle") }}
        </p>

      </div>



      <button

        class="refresh-button"

        type="button"

        @click="refresh"

        :disabled="loading"

      >

        ↻ {{ t("analytics.refresh") }}

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

          {{ t("analytics.warning.title") }}

        </strong>



        <span>
          {{ t("analytics.warning.description") }}
        </span>

      </div>



      <button

        type="button"

        @click="refresh"

      >

        {{ t("analytics.retry") }}

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



      {{ t("analytics.recommendationStatus.title") }}

      {{ personalizedProducts }}

      {{ t("analytics.recommendationStatus.of") }} {{ totalProducts }}

      {{ t("analytics.recommendationStatus.products") }}

    </div>





    <!-- ================================================= -->

    <!-- KPI -->

    <!-- ================================================= -->



    <div class="kpi-grid">

      <!-- BANKS -->
      <div class="kpi-card">
        <div class="kpi-label">
          {{ t("analytics.totalBanks") }}
        </div>

        <div class="kpi-value">
          {{ totalBanks }}
        </div>

        <div class="kpi-description">
          {{ t("analytics.marketMonitoring") }}
        </div>
      </div>



      <!-- PRODUCTS -->



      <div class="kpi-card">



        <div class="kpi-label">

          {{ productsLabel }}

        </div>



        <div class="kpi-value">

          {{ totalProducts }}

        </div>



        <div class="kpi-description">

          {{ t("analytics.kpi.availableProducts") }}

        </div>



      </div>





      <!-- INTEREST -->



      <div class="kpi-card">



        <div class="kpi-label">

          {{ t("analytics.table.averageRate") }}

        </div>



        <div class="kpi-value">

          {{ averageInterest }}%

        </div>



        <div class="kpi-description">

          {{ t("analytics.kpi.byAvailableProducts") }}

        </div>



      </div>





      <!-- MARKET LIMIT -->



      <div class="kpi-card">



        <div class="kpi-label">

          {{ t("analytics.kpi.maximumLimit") }}

        </div>



        <div class="kpi-value">

          {{ formatMillions(maximumLimit) }}

          {{ t("analytics.units.million") }}

        </div>



        <div class="kpi-description">

          {{ t("analytics.kpi.maximumProductAmount") }}

        </div>



      </div>





      <!-- AI RANKING -->



      <div class="kpi-card">



        <div class="kpi-label">

          {{ t("analytics.kpi.aiRating") }}

        </div>



        <div class="kpi-value">

          {{ averageRanking }}

        </div>



        <div class="kpi-description">

          {{ t("analytics.kpi.averageRanking") }}

        </div>



      </div>





      <!-- APPROVAL -->



      <div class="kpi-card">



        <div class="kpi-label">

          {{ t("analytics.kpi.approvalProbability") }}

        </div>



        <div class="kpi-value">

          {{ averageApproval }}

        </div>



        <div class="kpi-description">

          {{ t("analytics.kpi.personalApproval") }}

        </div>



      </div>





      <!-- PERSONALIZED LIMIT -->



      <div class="kpi-card">



        <div class="kpi-label">

          {{ t("analytics.kpi.recommendedLimit") }}

        </div>



        <div class="kpi-value">

          {{

            maximumRecommendedLimit

              ? `${formatMillions(maximumRecommendedLimit)} ${t("analytics.units.million")}`

              : "—"

          }}

        </div>



        <div class="kpi-description">

          {{ t("analytics.kpi.maximumPersonalLimit") }}

        </div>



      </div>





      <!-- ONLINE -->



      <div class="kpi-card">



        <div class="kpi-label">

          {{ t("analytics.kpi.onlineProducts") }}

        </div>



        <div class="kpi-value">

          {{ onlineProducts }}

        </div>



        <div class="kpi-description">

          {{ t("analytics.kpi.availableOnline") }}

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

            {{ t("analytics.charts.interestTitle") }}

          </h2>



          <p>
            {{ t("analytics.charts.interestDescription") }}
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

            {{ t("analytics.charts.limitsTitle") }}

          </h2>



          <p>
            {{ t("analytics.charts.limitsDescription") }}
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

            {{ t("analytics.charts.aiTitle") }}

          </h2>



          <p>
            {{ t("analytics.charts.aiDescription") }}
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

            {{ t("analytics.charts.productsTitle") }}

          </h2>



          <p>
            {{ t("analytics.charts.productsDescription") }}
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
            {{ t("analytics.charts.openingTitle") }}
          </h2>

          <p>
            {{ t("analytics.charts.openingDescription") }}
          </p>
        </div>

        <div class="chart-container opening-chart-container">
          <Bar
            :data="openingMethodsData"
            :options="chartOptions"
          />
        </div>

        <div class="opening-summary">
          <div class="opening-summary-item">
            <span class="opening-summary-label">
              {{ t("analytics.opening.online") }}
            </span>
            <strong>{{ onlineProducts }}</strong>
          </div>

          <div class="opening-summary-item">
            <span class="opening-summary-label">
              {{ t("analytics.opening.branch") }}
            </span>
            <strong>{{ branchProducts }}</strong>
          </div>

          <div class="opening-summary-item">
            <span class="opening-summary-label">
              {{ t("analytics.opening.both") }}
            </span>
            <strong>{{ bothProducts }}</strong>
          </div>
        </div>
      </div>


    </div>


      <div class="analytics-section-heading">
        <div>
          <h2>{{ t("analytics.bankComparison") }}</h2>
          <p>{{ t("analytics.table.description") }}</p>
        </div>

        <span class="analytics-section-count">
          {{ filteredBanks.length }}
        </span>
      </div>


      <div

        v-if="filteredBanks.length"

        class="table-wrapper"

      >



        <table class="analytics-table">



          <thead>



            <tr>



              <th>

                {{ t("analytics.table.bank") }}

              </th>



              <th>

                {{ t("analytics.table.products") }}

              </th>



              <th>

                {{ t("analytics.table.averageRate") }}

              </th>



              <th>

                {{ t("analytics.kpi.aiRating") }}

              </th>



              <th>

                {{ t("analytics.table.approval") }}

              </th>



              <th>

                {{ t("analytics.table.aiProducts") }}

              </th>



              <th>

                {{ t("analytics.table.online") }}

              </th>



              <th>

                {{ t("analytics.table.branch") }}

              </th>



              <th>

                {{ t("analytics.opening.both") }}

              </th>



              <th>

                {{ t("analytics.table.maxLimit") }}

              </th>



              <th>

                {{ t("analytics.table.recommendedLimit") }}

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





              <!-- BOTH -->



              <td>

                {{ bank.both_products }}

              </td>





              <!-- MARKET LIMIT -->



              <td>



                {{

                  bank.max_limit

                    ? `${formatMillions(

                        bank.max_limit

                       )} ${t("analytics.units.million")}`

                    : "—"

                }}



              </td>





              <!-- PERSONALIZED LIMIT -->



              <td>



                {{

                  bank.max_recommended_limit

                    ? `${formatMillions(

                        bank.max_recommended_limit

                       )} ${t("analytics.units.million")}`

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

        {{ t("analytics.empty") }}

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

        {{ t("analytics.loading") }}

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

        {{ t("analytics.retry") }}

      </button>



    </div>

</template>





<style scoped>

.analytics {

  width: 100%;

  padding: 24px;

  box-sizing: border-box;

}





/* =====================================================

   HEADER

\===================================================== \*/



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

\===================================================== \*/



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

\===================================================== \*/



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

\===================================================== \*/



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

\===================================================== \*/



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





.opening-chart-container {
  height: 320px;
}

.opening-summary {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin-top: 14px;
}

.opening-summary-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 12px 14px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  background: #f8fafc;
}

.opening-summary-label {
  color: #6b7280;
  font-size: 13px;
  font-weight: 600;
}

.opening-summary-item strong {
  color: #111827;
  font-size: 18px;
  font-weight: 800;
}

.analytics-section-heading {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 16px;
  margin: 24px 0 12px;
}

.analytics-section-heading h2 {
  margin: 0;
  color: #111827;
  font-size: 20px;
  font-weight: 800;
}

.analytics-section-heading p {
  margin: 5px 0 0;
  color: #6b7280;
  font-size: 13px;
}

.analytics-section-count {
  flex: 0 0 auto;
  padding: 7px 10px;
  border-radius: 999px;
  background: #f3f4f6;
  color: #4b5563;
  font-size: 12px;
  font-weight: 700;
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

\===================================================== \*/



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

    \#374151;



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

\===================================================== \*/



.empty-state {

  padding: 40px 20px;



  text-align: center;



  color: #9ca3af;

}





/* =====================================================

   RESPONSIVE

\===================================================== \*/



@media (max-width: 1200px) {

  .kpi-grid {

    grid-template-columns:

      repeat(3, minmax(0, 1fr));

  }

}


/* =========================================================
   СРАВНЕНИЕ БАНКОВ
   ========================================================= */

.analytics-section-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;

  margin: 24px 0 0;
  padding: 18px 20px;

  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-bottom: none;
  border-radius: 14px 14px 0 0;
}

.analytics-section-heading h2 {
  margin: 0;

  font-size: 18px;
  font-weight: 700;
  line-height: 1.3;
  color: #111827;
}

.analytics-section-heading p {
  margin: 5px 0 0;

  font-size: 12px;
  line-height: 1.5;
  color: #6b7280;
}

.analytics-section-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;

  min-width: 34px;
  height: 28px;
  padding: 0 10px;

  border-radius: 999px;

  background: #eff6ff;
  color: #2563eb;

  font-size: 12px;
  font-weight: 700;
}

/* =========================================================
   ТАБЛИЦА
   ========================================================= */

.table-wrapper {
  width: 100%;

  overflow-x: auto;
  overflow-y: hidden;

  background: #ffffff;

  border: 1px solid #e5e7eb;
  border-radius: 0 0 14px 14px;

  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);

  scrollbar-width: thin;
}

/* =========================================================
   HEADER ТАБЛИЦЫ
   ========================================================= */

.analytics-table {
  width: 100%;
  min-width: 1100px;

  border-collapse: collapse;
}

.analytics-table th {
  position: sticky;
  top: 0;
  z-index: 2;

  padding: 12px 14px;

  background: #f8fafc;

  border-bottom: 1px solid #e5e7eb;

  color: #64748b;

  font-size: 11px;
  font-weight: 700;

  text-align: left;
  white-space: nowrap;
}

/* =========================================================
   ЯЧЕЙКИ
   ========================================================= */

.analytics-table td {
  padding: 13px 14px;

  border-bottom: 1px solid #f1f5f9;

  color: #334155;

  font-size: 12px;

  white-space: nowrap;
}

.analytics-table tbody tr {
  transition: background 0.15s ease;
}

.analytics-table tbody tr:hover {
  background: #f5f8ff;
}

.analytics-table tbody tr:last-child td {
  border-bottom: none;
}

/* =========================================================
   НАЗВАНИЕ БАНКА
   ========================================================= */

.analytics-table .bank-name {
  color: #111827;
  font-weight: 700;
}

/* =========================================================
   AI-ПРОДУКТЫ
   ========================================================= */

.analytics-table .ai-products {
  color: #4f46e5;
  font-weight: 700;
}

/* =========================================================
   МОБИЛЬНАЯ ВЕРСИЯ
   ========================================================= */

@media (max-width: 700px) {
  .analytics-section-heading {
    align-items: flex-start;
    padding: 16px;

    border-radius: 12px 12px 0 0;
  }

  .analytics-section-heading h2 {
    font-size: 16px;
  }

  .analytics-section-heading p {
    font-size: 11px;
  }

  .analytics-section-count {
    flex-shrink: 0;
  }

  .table-wrapper {
    border-radius: 0 0 12px 12px;
  }

  .analytics-table {
    min-width: 1000px;
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
