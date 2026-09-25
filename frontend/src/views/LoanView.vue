<script setup>

import {
  ref,
  onMounted,
  computed
} from "vue"

import {
  useRoute,
  useRouter
} from "vue-router"

import api from "@/api/axios"

import LoanHeader from "@/components/loan/LoanHeader.vue"
import LoanStats from "@/components/loan/LoanStats.vue"
import LoanInfo from "@/components/loan/LoanInfo.vue"
import LoanDescription from "@/components/loan/LoanDescription.vue"
import LoanRequirements from "@/components/loan/LoanRequirements.vue"
import LoanBranches from "@/components/loan/LoanBranches.vue"
import LoanActions from "@/components/loan/LoanActions.vue"


// ==========================================
// 🔥 ROUTER
// ==========================================
const route = useRoute()
const router = useRouter()


// ==========================================
// 🔥 STATE
// ==========================================
const loading = ref(true)

const error = ref(false)

const product = ref(null)

const branches = ref([])


// ==========================================
// 🚀 LOAD PRODUCT + BRANCHES
// ==========================================
onMounted(async () => {

  try {

    const id = route.params.id

    if (!id) {

      throw new Error(
        "Product ID missing"
      )

    }

    // ======================================
    // PRODUCT
    // ======================================
    const res = await api.get(
      `/banks/products/${id}/`
    )

    product.value = res.data

    console.log(
      "PRODUCT:",
      product.value
    )

    console.log(
      "RANKING SCORE:",
      product.value?.ranking_score
    )

    console.log(
      "APPROVAL PROBABILITY:",
      product.value?.approval_probability
    )

    // ======================================
    // ONLINE PRODUCTS
    // ======================================
    if (
      product.value?.is_online
    ) {

      console.log(
        "ONLINE PRODUCT - SKIP BRANCHES"
      )

      return

    }

    // ======================================
    // BRANCHES
    // ======================================
    const bankId =

      product.value?.bank?.id ||

      product.value?.bank_id

    console.log(
      "BANK ID:",
      bankId
    )

    if (!bankId) {

      return

    }

    try {

      const branchRes =
        await api.get(
          `/banks/${bankId}/branches/`
        )

      console.log(
        "BRANCH RESPONSE:",
        branchRes.data
      )

      branches.value =

        branchRes.data?.branches ||

        branchRes.data?.results ||

        []

      console.log(
        "BRANCHES LOADED:",
        branches.value.length
      )

    }

    catch (branchErr) {

      console.warn(
        "Branches load error:",
        branchErr
      )

      branches.value = []

    }

  }

  catch (err) {

    console.error(
      "Loan load error:",
      err
    )

    error.value = true

  }

  finally {

    loading.value = false

  }

})


// ==========================================
// 🔙 BACK
// ==========================================
function goBack() {

  router.back()

}


// ==========================================
// 💰 FORMAT MONEY
// ==========================================
function formatMoney(value) {

  if (
    value === null ||
    value === undefined
  ) {

    return "-"

  }

  return (

    new Intl.NumberFormat(
      "ru-RU"
    ).format(value)

    + " UZS"

  )

}


// ==========================================
// ⭐ RATING
// ==========================================
const rating = computed(() => {

  const score = Number(
    product.value?.ranking_score
  )

  if (
    Number.isNaN(score)
  ) {

    return 50

  }

  return Math.max(
    0,
    Math.min(
      100,
      Math.round(score)
    )
  )

})


// ==========================================
// 🔥 APPLY
// ==========================================
function apply() {

  if (!product.value) {

    console.warn(
      "Product not loaded"
    )

    return

  }

  const url =

    product.value?.source_url ||

    product.value?.website ||

    product.value?.bank_url ||

    null

  console.log(
    "OPEN URL:",
    url
  )

  if (!url) {

    alert(
      "Ссылка на оформление кредита отсутствует"
    )

    return

  }

  window.open(
    url,
    "_blank",
    "noopener,noreferrer"
  )

}


// ==========================================
// 📄 MORE OFFERS
// ==========================================
function goToRecommendations() {

  router.push(
    "/app/recommendations"
  )

}

</script>

<template>

<div class="loan-page">

  <!-- ===================================== -->
  <!-- 🔥 LOADING -->
  <!-- ===================================== -->

  <div
    v-if="loading"
    class="state"
  >
    Загрузка кредита...
  </div>


  <!-- ===================================== -->
  <!-- ❌ ERROR -->
  <!-- ===================================== -->

  <div
    v-else-if="error"
    class="state error"
  >
    Ошибка загрузки продукта
  </div>


  <!-- ===================================== -->
  <!-- 📭 EMPTY -->
  <!-- ===================================== -->

  <div
    v-else-if="!product"
    class="state"
  >
    Продукт не найден
  </div>


  <!-- ===================================== -->
  <!-- ✅ CONTENT -->
  <!-- ===================================== -->

  <template v-else>

    <!-- HEADER -->
    <LoanHeader
      :product="product"
      @back="goBack"
    />

    <!-- STATS -->
    <LoanStats
      :product="product"
      :rating="rating"
      :format-money="formatMoney"
    />

    <!-- INFO -->
    <LoanInfo
      :product="product"
    />

    <!-- DESCRIPTION -->
    <LoanDescription
      :product="product"
    />

    <!-- REQUIREMENTS -->
    <LoanRequirements
      :product="product"
    />

    <!-- BRANCHES -->
    <LoanBranches
      :product="product"
      :branches="branches"
    />

    <!-- ACTIONS -->
    <LoanActions
      @apply="apply"
      @more="goToRecommendations"
    />

  </template>

</div>

</template>


<style scoped>

.loan-page{

  width:100%;

  max-width:1100px;

  margin:0 auto;

  padding:40px 24px 80px;
}


.state{

  padding:80px 20px;

  text-align:center;

  font-size:18px;

  color:#64748b;
}


.error{

  color:#ef4444;
}


/* ==========================================
🔥 MOBILE
========================================== */

@media (max-width:768px){

  .loan-page{

    padding:20px 14px 50px;
  }

  .state{

    padding:50px 10px;

    font-size:16px;
  }
}

</style>