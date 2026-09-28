<script setup>

import {
  computed,
} from "vue"

import {
  useI18n,
} from "vue-i18n"


const {
  t,
  locale,
} = useI18n()


const props = defineProps({

  profile: {

    type: Object,

    required: true,

  },

})


// ==========================================
// FORMAT MONEY
// ==========================================

function formatMoney(value) {

  const number = Number(value ?? 0)

  if (!number) {

    return t(
      "financialInfo.values.notSpecified",
    )

  }


  const localeMap = {

    ru: "ru-RU",

    en: "en-US",

    uz: "uz-UZ",

  }


  const formatted =
    number.toLocaleString(

      localeMap[locale.value] ||
      "ru-RU",

      {

        minimumFractionDigits: 2,

        maximumFractionDigits: 2,

      },

    )


  return `${formatted} UZS`

}


// ==========================================
// FINANCIAL DATA
// ==========================================

const income = computed(() =>

  Number(
    props.profile?.income ?? 0
  )

)


const expenses = computed(() =>

  Number(
    props.profile?.expenses ?? 0
  )

)


const totalDebt = computed(() =>

  Number(
    props.profile?.totalDebt ?? 0
  )

)


const overdueDebt = computed(() =>

  Number(
    props.profile?.overdueDebt ?? 0
  )

)


const contractsCount = computed(() =>

  Number(
    props.profile?.contractsCount ?? 0
  )

)


const netBalance = computed(() =>

  Number(

    props.profile?.profile?.net_balance ??

    props.profile?.net_balance ??

    income.value - expenses.value

  )

)


const dti = computed(() => {

  const value = Number(

    props.profile?.profile?.dti ??

    props.profile?.dti ??

    0

  )


  return value > 0

    ? Math.round(value)

    : null

})


// ==========================================
// FINANCIAL STATUS
// ==========================================

const financialStatus = computed(() => {

  if (dti.value === null) {

    return {

      text: t(
        "financialInfo.status.insufficientData",
      ),

      color: "#94a3b8",

    }

  }


  if (dti.value <= 35) {

    return {

      text: t(
        "financialInfo.status.stable",
      ),

      color: "#16a34a",

    }

  }


  if (dti.value <= 50) {

    return {

      text: t(
        "financialInfo.status.moderate",
      ),

      color: "#f59e0b",

    }

  }


  return {

    text: t(
      "financialInfo.status.high",
    ),

    color: "#ef4444",

  }

})


// ==========================================
// SUMMARY
// ==========================================

const summary = computed(() => ({

  income: formatMoney(
    income.value
  ),

  expenses: formatMoney(
    expenses.value
  ),

  debt: formatMoney(
    totalDebt.value
  ),

  overdue: formatMoney(
    overdueDebt.value
  ),

  balance: formatMoney(
    netBalance.value
  ),

  contracts: contractsCount.value,

  dti:

    dti.value !== null

      ? `${dti.value}%`

      : t(
          "financialInfo.values.empty"
        ),

}))

</script>


<template>

  <div class="card">

    <div class="card-header">

      <div>

        <h2>
          💰 {{ t("financialInfo.title") }}
        </h2>

        <p>
          {{ t("financialInfo.description") }}
        </p>

      </div>


      <span class="badge">
        {{ t("financialInfo.updated") }}
      </span>

    </div>


    <div class="items">


      <!-- ДОХОД -->

      <div class="item">

        <div class="label">
          💵 {{ t("financialInfo.income") }}
        </div>

        <div class="value income">
          {{ summary.income }}
        </div>

      </div>


      <!-- РАСХОДЫ -->

      <div class="item">

        <div class="label">
          💸 {{ t("financialInfo.expenses") }}
        </div>

        <div class="value">
          {{ summary.expenses }}
        </div>

      </div>


      <!-- СВОБОДНЫЙ ОСТАТОК -->

      <div class="item">

        <div class="label">
          💰 {{ t("financialInfo.balance") }}
        </div>

        <div
          class="value"
          :class="
            netBalance >= 0
              ? 'income'
              : 'debt'
          "
        >

          {{ summary.balance }}

        </div>

      </div>


      <!-- ОБЩАЯ ЗАДОЛЖЕННОСТЬ -->

      <div class="item">

        <div class="label">
          🏦 {{ t("financialInfo.totalDebt") }}
        </div>

        <div class="value debt">

          {{ summary.debt }}

        </div>

      </div>


      <!-- ПРОСРОЧКА -->

      <div class="item">

        <div class="label">
          ⚠ {{ t("financialInfo.overdue") }}
        </div>

        <div
          class="value"
          :class="
            overdueDebt > 0
              ? 'overdue'
              : 'income'
          "
        >

          {{
            overdueDebt > 0
              ? summary.overdue
              : t(
                  "financialInfo.values.absent"
                )
          }}

        </div>

      </div>


      <!-- ДОГОВОРЫ -->

      <div class="item">

        <div class="label">
          📄 {{ t("financialInfo.contracts") }}
        </div>

        <div class="value">

          {{ summary.contracts }}

        </div>

      </div>


      <!-- DTI -->

      <div class="item">

        <div class="label">
          📊 Debt-to-Income
        </div>

        <div class="value">

          {{ summary.dti }}

        </div>

      </div>


      <!-- ФИНАНСОВОЕ СОСТОЯНИЕ -->

      <div class="item">

        <div class="label">
          📈 {{ t("financialInfo.financialStatus") }}
        </div>

        <div
          class="status"
          :style="{
            backgroundColor:
              financialStatus.color
          }"
        >

          {{ financialStatus.text }}

        </div>

      </div>


    </div>

  </div>

</template>


<style scoped>

.card{

    background:#ffffff;

    border-radius:24px;

    padding:30px;

    box-shadow:0 12px 32px rgba(15,23,42,.08);

    height:100%;

}

.card-header{

    display:flex;

    justify-content:space-between;

    align-items:center;

    margin-bottom:26px;

}

h2{

    margin:0;

    font-size:26px;

    font-weight:700;

    color:#0f172a;

}

.badge{

    background:#dbeafe;

    color:#2563eb;

    padding:7px 14px;

    border-radius:999px;

    font-size:12px;

    font-weight:700;

}

/* ====================================== */
/* LIST */
/* ====================================== */

.items{

    display:flex;

    flex-direction:column;

    gap:0;

}

.item{

    display:flex;

    justify-content:space-between;

    align-items:center;

    padding:18px 0;

    border-bottom:1px solid #eef2f7;

    transition:.2s;

}

.item:last-child{

    border-bottom:none;

}

.item:hover{

    padding-left:8px;

}

/* ====================================== */

.label{

    display:flex;

    align-items:center;

    gap:8px;

    font-size:15px;

    font-weight:500;

    color:#64748b;

}

.value{

    font-size:18px;

    font-weight:700;

    color:#0f172a;

    text-align:right;

    white-space:nowrap;

}

.income{

    color:#16a34a;

}

.debt{

    color:#2563eb;

}

.overdue{

    color:#ef4444;

}

.status{

    padding:8px 16px;

    border-radius:999px;

    color:white;

    font-size:13px;

    font-weight:700;

}

/* ====================================== */

@media(max-width:768px){

.card{

    padding:22px;

}

.card-header{

    flex-direction:column;

    align-items:flex-start;

    gap:14px;

}

.item{

    flex-direction:column;

    align-items:flex-start;

    gap:8px;

}

.value{

    text-align:left;

    font-size:20px;

}

}

</style>