<script setup>

import { useI18n } from "vue-i18n"

defineProps({
  product: {
    type: Object,
    default: () => ({})
  }
})

const { t, locale } = useI18n()

// ==========================================
// LOAN TYPE
// ==========================================

function getLoanType(type) {

  const map = {
    micro: "micro",
    consumer: "consumer",
    mortgage: "mortgage",
    auto: "auto",
    business: "business",
    business_credit: "business",
    education: "education",
    green: "green",
    overdraft: "overdraft",
    loan: "loan"
  }

  const key = map[type]

  if (!key) {
    return type || t("loanInfo.notSpecified")
  }

  return t(`loanInfo.loanTypes.${key}`)
}

// ==========================================
// FORMAT AMOUNT
// ==========================================

function formatAmount(value) {

  const amount = Number(value)

  if (
    !amount ||
    amount <= 0
  ) {
    return t("loanInfo.amountNotSpecified")
  }

  const localeMap = {
    ru: "ru-RU",
    en: "en-US",
    uz: "uz-UZ"
  }

  const currentLocale =
    localeMap[locale.value] || "ru-RU"

  return (
    new Intl.NumberFormat(
      currentLocale
    ).format(amount)
    + " UZS"
  )
}

// ==========================================
// FORMAT TERM
// ==========================================

function formatTerm(term) {

  if (
    term === null ||
    term === undefined ||
    term === ""
  ) {
    return t("loanInfo.notSpecified")
  }

  const months = Number(term)

  if (
    Number.isNaN(months)
  ) {
    return term
  }

  if (months < 12) {
    return `${months} ${t("loanInfo.months")}`
  }

  if (months % 12 === 0) {

    const years = months / 12

    if (years === 1) {
      return `1 ${t("loanInfo.year")}`
    }

    return `${years} ${t("loanInfo.years")}`
  }

  return `${months} ${t("loanInfo.months")}`
}

</script>

<template>

<div class="card">

  <h3>
    📋 {{ t("loanInfo.title") }}
  </h3>

  <div class="grid">

    <!-- ======================================
         LOAN TYPE
    ======================================= -->

    <div class="item">

      <div class="icon">
        💳
      </div>

      <div class="label">
        {{ t("loanInfo.loanType") }}
      </div>

      <div class="value">
        {{
          getLoanType(
            product?.loan_type
          )
        }}
      </div>

    </div>

    <!-- ======================================
         BANK
    ======================================= -->

    <div class="item">

      <div class="icon">
        🏦
      </div>

      <div class="label">
        {{ t("loanInfo.bank") }}
      </div>

      <div class="value">
        {{
          product?.bank?.name ||
          product?.bank_name ||
          t("loanInfo.notSpecified")
        }}
      </div>

    </div>

    <!-- ======================================
         MAXIMUM AMOUNT
    ======================================= -->

    <div class="item">

      <div class="icon">
        💰
      </div>

      <div class="label">
        {{ t("loanInfo.maxAmount") }}
      </div>

      <div class="value">
        {{
          formatAmount(
            product?.max_amount ||
            product?.loan_limit_hint
          )
        }}
      </div>

    </div>

    <!-- ======================================
         SOURCE
    ======================================= -->

    <div class="item">

      <div class="icon">
        🌐
      </div>

      <div class="label">
        {{ t("loanInfo.source") }}
      </div>

      <div class="value">
        {{
          product?.source_name ||
          t("loanInfo.notSpecified")
        }}
      </div>

    </div>

  </div>

</div>

</template>

<style scoped>

.card{

  background:#fff;

  padding:24px;

  border-radius:20px;

  border:1px solid #e5e7eb;

  margin-bottom:24px;

}

h3{

  margin:0 0 20px;

  font-size:18px;

  font-weight:700;

}

.grid{

  display:grid;

  grid-template-columns:
    repeat(
      auto-fit,
      minmax(220px,1fr)
    );

  gap:16px;

}

.item{

  border:1px solid #e2e8f0;

  border-radius:16px;

  padding:18px;

  background:#fafafa;

}

.icon{

  font-size:24px;

  margin-bottom:10px;

}

.label{

  font-size:13px;

  color:#64748b;

  margin-bottom:6px;

}

.value{

  font-size:16px;

  font-weight:700;

  color:#0f172a;

  word-break:break-word;

}

@media (max-width:768px){

  .grid{

    grid-template-columns:1fr;

  }

}

</style>