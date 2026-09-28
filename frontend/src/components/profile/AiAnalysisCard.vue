<script setup>

import {
  computed,
} from "vue"

import { useI18n } from "vue-i18n"

const { t } = useI18n()


const props = defineProps({

  profile: {
    type: Object,
    required: true,
  },

  score: {
    type: Object,
    required: true,
  },

  recommendations: {
    type: Array,
    default: () => [],
  },

})


// =====================================================
// DATA
// =====================================================

const creditScore = computed(() =>
  Number(props.score.score || 0)
)


const risk = computed(() =>
  props.score.risk || "UNKNOWN"
)


const income = computed(() =>
  Number(props.profile.income || 0)
)


const totalDebt = computed(() =>
  Number(props.profile.totalDebt || 0)
)


const overdueDebt = computed(() =>
  Number(props.profile.overdueDebt || 0)
)


const contracts = computed(() =>
  Number(props.profile.contractsCount || 0)
)


const dti = computed(() => {

  if (!income.value)
    return 0

  return Math.round(
    (totalDebt.value / income.value) * 100
  )

})


// =====================================================
// POSITIVE
// =====================================================

const positives = computed(() => {

  const list = []

  if (creditScore.value >= 700) {
    list.push(
      t("aiAnalysis.positives.highScore")
    )
  }

  if (overdueDebt.value === 0) {
    list.push(
      t("aiAnalysis.positives.noOverdue")
    )
  }

  if (dti.value <= 35) {
    list.push(
      t("aiAnalysis.positives.lowDebtLoad")
    )
  }

  if (!list.length) {
    list.push(
      t("aiAnalysis.positives.few")
    )
  }

  return list

})


// =====================================================
// WARNINGS
// =====================================================

const warnings = computed(() => {

  const list = []

  if (creditScore.value < 500) {
    list.push(
      t("aiAnalysis.warnings.lowScore")
    )
  }

  if (overdueDebt.value > 0) {
    list.push(
      t("aiAnalysis.warnings.overdue")
    )
  }

  if (dti.value > 50) {
    list.push(
      t("aiAnalysis.warnings.highDebtLoad")
    )
  }

  if (contracts.value > 5) {
    list.push(
      t("aiAnalysis.warnings.manyContracts")
    )
  }

  if (!list.length) {
    list.push(
      t("aiAnalysis.warnings.noCritical")
    )
  }

  return list

})


// =====================================================
// RECOMMENDATIONS
// =====================================================

const advice = computed(() => {

  const list = []

  if (overdueDebt.value > 0) {
    list.push(
      t("aiAnalysis.advice.payOverdue")
    )
  }

  if (dti.value > 40) {
    list.push(
      t("aiAnalysis.advice.reduceDebtLoad")
    )
  }

  if (creditScore.value < 600) {
    list.push(
      t("aiAnalysis.advice.newLoans")
    )
  }

  if (
    props.recommendations.length &&
    props.recommendations[0]?.bank
  ) {

    list.push(
      `${t("aiAnalysis.advice.recommendedBank")}: ${props.recommendations[0].bank}`
    )

  }

  if (!list.length) {
    list.push(
      t("aiAnalysis.advice.stable")
    )
  }

  return list

})

</script>


<template>

  <div class="card">

    <div class="header">

      <h2>
        🤖 {{ t("aiAnalysis.title") }}
      </h2>

      <span class="badge">
        {{ t("aiAnalysis.badge") }}
      </span>

    </div>


    <!-- STRONG SIDES -->

    <div class="section">

      <h3>
        ✅ {{ t("aiAnalysis.strongSides") }}
      </h3>

      <ul>

        <li
          v-for="item in positives"
          :key="item"
        >
          {{ item }}
        </li>

      </ul>

    </div>


    <!-- RISKS -->

    <div class="section">

      <h3>
        ⚠ {{ t("aiAnalysis.risks") }}
      </h3>

      <ul>

        <li
          v-for="item in warnings"
          :key="item"
        >
          {{ item }}
        </li>

      </ul>

    </div>


    <!-- RECOMMENDATIONS -->

    <div class="section">

      <h3>
        💡 {{ t("aiAnalysis.recommendations") }}
      </h3>

      <ul>

        <li
          v-for="item in advice"
          :key="item"
        >
          {{ item }}
        </li>

      </ul>

    </div>

  </div>

</template>


<style scoped>

.card{

    background:#ffffff;

    border-radius:24px;

    padding:32px;

    box-shadow:0 10px 30px rgba(15,23,42,.08);

    height:100%;

}

.header{

    display:flex;

    justify-content:space-between;

    align-items:center;

    margin-bottom:28px;

}

h2{

    margin:0;

    font-size:24px;

    font-weight:700;

}

.badge{

    background:#ede9fe;

    color:#7c3aed;

    padding:8px 16px;

    border-radius:999px;

    font-size:13px;

    font-weight:700;

}

.section{

    margin-top:20px;

    padding:18px;

    background:#f8fafc;

    border-radius:18px;

    border:1px solid #e2e8f0;

}

.section h3{

    margin:0 0 14px;

    font-size:16px;

    color:#0f172a;

}

ul{

    margin:0;

    padding-left:20px;

}

li{

    margin-bottom:10px;

    color:#334155;

    line-height:1.6;

}

li:last-child{

    margin-bottom:0;

}

@media(max-width:768px){

    .card{

        padding:24px;

    }

    .header{

        flex-direction:column;

        align-items:flex-start;

        gap:16px;

    }

}

</style>