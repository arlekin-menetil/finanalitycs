<template>

  <div class="card">

    <!-- ===================================== -->
    <!-- 💣 TOP -->
    <!-- ===================================== -->
    <div class="top">

      <!-- =================================== -->
      <!-- 💣 BANK -->
      <!-- =================================== -->
      <div class="bank-info">

        <div class="logo-wrapper">

          <img
            :src="bankLogo"
            class="logo"
            alt="bank"
          />

        </div>

        <div>

          <h3 class="bank-name">

            {{ bankName }}

          </h3>

          <p class="product-name">

            {{ productName }}

          </p>

        </div>

      </div>


      <!-- =================================== -->
      <!-- 💣 SCORE -->
      <!-- =================================== -->
      <div class="score-circle">

        <div class="score-number">

          {{ approvalPercent }}%

        </div>

      </div>

    </div>


    <!-- ===================================== -->
    <!-- 💣 TAGS -->
    <!-- ===================================== -->
    <div class="tags">

      <span
        v-if="bank.is_online"
        class="tag online"
      >
        ⚡ {{ t("recommendations.online") }}
      </span>

      <span class="tag type">

        {{ productTypeLabel }}

      </span>

    </div>


    <!-- ===================================== -->
    <!-- 💣 RATE -->
    <!-- ===================================== -->
    <div class="rate-block">

      <div class="rate-value">

        {{ interestRate }}

      </div>

      <div class="rate-label">

        {{ t("recommendations.interest") }}

      </div>

    </div>


    <!-- ===================================== -->
    <!-- 💣 STATS -->
    <!-- ===================================== -->
    <div class="stats">

      <div class="stat">

        <span>
          {{ t("recommendations.approval") }}
        </span>

        <strong>
          {{ approvalPercent }}%
        </strong>

      </div>

      <div class="stat">

        <span>
          {{ t("recommendations.loanLimit") }}
        </span>

        <strong>
          {{ formattedLimit }}
        </strong>

      </div>

      <div class="stat">

        <span>
          {{ t("recommendations.term") }}
        </span>

        <strong>
          {{ bank.term || "—" }}
        </strong>

      </div>

    </div>


    <!-- ===================================== -->
    <!-- 💣 REASONS -->
    <!-- ===================================== -->
    <div
      v-if="reasons.length"
      class="reasons"
    >

      <div
        v-for="(
          reason,
          index
        ) in reasons"

        :key="index"

        class="reason"
      >

        ✔ {{ reason }}

      </div>

    </div>


    <!-- ===================================== -->
    <!-- 💣 ACTIONS -->
    <!-- ===================================== -->
    <div class="actions">

      <button
        class="apply-btn"
        @click="handleApply"
      >
        {{ t("recommendations.applyOnline") }}
      </button>

      <button
        class="details-btn"
        @click="openDetails"
      >
        {{ t("recommendations.details") }}
      </button>

    </div>

  </div>

</template>

<script setup>

import {
  computed
} from "vue"

import {
  useRouter
} from "vue-router"

import {
  useI18n
} from "vue-i18n"

import {
  useRecommendationsStore
} from "@/stores/recommendations"

// ==========================================
// 💣 I18N
// ==========================================
const {
  t,
  locale
} = useI18n()

// ==========================================
// 💣 PROPS
// ==========================================
const props = defineProps({

  bank: {
    type: Object,
    required: true,
  },
})

// ==========================================
// 💣 STORE
// ==========================================
const recommendations =
  useRecommendationsStore()

const router = useRouter()

// ==========================================
// 💣 BANK NAME
// ==========================================
const bankName = computed(() => {

  return (

    props.bank.bank_name ||

    props.bank.bank ||

    t("common.bank")
  )
})

// ==========================================
// 💣 PRODUCT NAME
// ==========================================
const productName = computed(() => {

  return (

    props.bank.product_name ||

    props.bank.name ||

    t("recommendations.product")
  )
})

// ==========================================
// 💣 LOGO
// ==========================================
const bankLogo = computed(() => {

  const slug = bankName.value

    .toLowerCase()

    .replace(/\s+/g, "")

  return `/banks/${slug}.png`
})

// ==========================================
// 💣 RATE
// ==========================================
const interestRate = computed(() => {

  if (
    props.bank.interest_rate === null ||
    props.bank.interest_rate === undefined
  ) {

    return "—"
  }

  return `${props.bank.interest_rate}%`
})

// ==========================================
// 💣 APPROVAL
// ==========================================
const approvalPercent = computed(() => {

  const raw = Number(

    props.bank.approval_probability ||

    props.bank.score ||

    0
  )

  if (raw <= 1) {

    return Math.round(raw * 100)
  }

  return Math.round(raw)
})

// ==========================================
// 💣 LIMIT
// ==========================================
const formattedLimit = computed(() => {

  const value = (

    props.bank.loan_limit_hint ||

    props.bank.max_amount ||

    0
  )

  if (!value) {

    return "—"
  }

  const localeMap = {
    ru: "ru-RU",
    en: "en-US",
    uz: "uz-UZ",
  }

  return new Intl.NumberFormat(

    localeMap[locale.value] || "ru-RU"

  ).format(value)
})

// ==========================================
// 💣 REASONS
// ==========================================
const reasons = computed(() => {

  return (

    props.bank.reasons ||

    props.bank.explanations ||

    []
  )
})

// ==========================================
// 💣 TYPE LABEL
// ==========================================
const productTypeLabel = computed(() => {

  const type = (

    props.bank.product_type ||

    ""
  ).toLowerCase()

  if (type === "mortgage") {

    return `🏠 ${t("recommendations.filters.mortgage")}`
  }

  if (type === "micro") {

    return `💸 ${t("recommendations.filters.micro")}`
  }

  if (type === "auto") {

    return `🚗 ${t("recommendations.filters.auto")}`
  }

  if (
    type === "business" ||
    type === "business_credit"
  ) {

    return `🏢 ${t("recommendations.filters.businessCredit")}`
  }

  return `💳 ${t("recommendations.filters.loans")}`
})

// ==========================================
// 💣 APPLY
// ==========================================
const handleApply = async () => {

  try {

    await recommendations.apply(
      props.bank.id
    )

    if (props.bank.website) {

      window.open(
        props.bank.website,
        "_blank"
      )
    }

  } catch(err){

    console.error(
      "Apply error:",
      err
    )
  }
}

// ==========================================
// 💣 DETAILS
// ==========================================
const openDetails = () => {

  if (!props.bank?.id) {

    console.error(
      "INVALID PRODUCT ID"
    )

    return
  }

  router.push(
    `/app/loan/${props.bank.id}`
  )
}

</script>

<style scoped>

.card{

  position:relative;

  background:white;

  border-radius:28px;

  padding:24px;

  border:1px solid #e5e7eb;

  box-shadow:
    0 10px 30px rgba(0,0,0,.05);

  transition:.25s ease;

  overflow:hidden;
}

.card:hover{

  transform:translateY(-4px);

  box-shadow:
    0 16px 40px rgba(0,0,0,.08);
}


/* ==========================================
💣 TOP
========================================== */

.top{

  display:flex;

  justify-content:space-between;

  gap:18px;
}

.bank-info{

  display:flex;

  gap:14px;

  align-items:center;
}

.logo-wrapper{

  width:60px;

  height:60px;

  border-radius:18px;

  background:#f8fafc;

  display:flex;

  align-items:center;

  justify-content:center;
}

.logo{

  width:42px;

  height:42px;

  object-fit:contain;
}

.bank-name{

  margin:0;

  font-size:20px;

  font-weight:800;
}

.product-name{

  margin-top:6px;

  color:#64748b;

  font-size:14px;

  line-height:1.5;
}


/* ==========================================
💣 SCORE
========================================== */

.score-circle{

  width:72px;

  height:72px;

  border-radius:50%;

  background:
    linear-gradient(
      135deg,
      #2563eb,
      #1d4ed8
    );

  display:flex;

  align-items:center;

  justify-content:center;

  flex-shrink:0;
}

.score-number{

  color:white;

  font-weight:900;

  font-size:18px;
}


/* ==========================================
💣 TAGS
========================================== */

.tags{

  display:flex;

  gap:10px;

  flex-wrap:wrap;

  margin-top:20px;
}

.tag{

  padding:8px 12px;

  border-radius:999px;

  font-size:12px;

  font-weight:700;
}

.online{

  background:#dcfce7;

  color:#166534;
}

.type{

  background:#eff6ff;

  color:#1d4ed8;
}


/* ==========================================
💣 RATE
========================================== */

.rate-block{

  margin-top:24px;
}

.rate-value{

  font-size:48px;

  font-weight:900;

  line-height:1;
}

.rate-label{

  margin-top:8px;

  color:#64748b;

  font-size:14px;
}


/* ==========================================
💣 STATS
========================================== */

.stats{

  display:grid;

  grid-template-columns:
    repeat(3,1fr);

  gap:14px;

  margin-top:24px;
}

.stat{

  background:#f8fafc;

  padding:16px;

  border-radius:18px;
}

.stat span{

  display:block;

  font-size:12px;

  color:#64748b;

  margin-bottom:8px;
}

.stat strong{

  font-size:16px;

  font-weight:800;
}


/* ==========================================
💣 REASONS
========================================== */

.reasons{

  display:flex;

  flex-wrap:wrap;

  gap:10px;

  margin-top:24px;
}

.reason{

  padding:10px 14px;

  border-radius:14px;

  background:#f1f5f9;

  font-size:13px;

  font-weight:600;

  color:#334155;
}


/* ==========================================
💣 ACTIONS
========================================== */

.actions{

  display:flex;

  gap:12px;

  margin-top:28px;
}

.apply-btn{

  flex:1;

  border:none;

  background:
    linear-gradient(
      135deg,
      #2563eb,
      #1d4ed8
    );

  color:white;

  padding:14px;

  border-radius:16px;

  font-weight:800;

  cursor:pointer;

  transition:.2s;
}

.apply-btn:hover{

  opacity:.9;
}

.details-btn{

  flex:1;

  border:none;

  background:#f1f5f9;

  color:#0f172a;

  padding:14px;

  border-radius:16px;

  font-weight:800;

  cursor:pointer;

  transition:.2s;
}

.details-btn:hover{

  background:#e2e8f0;
}


/* ==========================================
💣 MOBILE
========================================== */

@media(max-width:768px){

  .card{

    padding:20px;
  }

  .top{

    flex-direction:column;
  }

  .score-circle{

    width:64px;

    height:64px;
  }

  .rate-value{

    font-size:38px;
  }

  .stats{

    grid-template-columns:1fr;
  }

  .actions{

    flex-direction:column;
  }
}

</style>