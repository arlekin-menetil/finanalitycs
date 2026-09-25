<script setup>

defineProps({
  product: {
    type: Object,
    default: () => ({})
  }
})

function getLoanType(type) {

  const map = {
    micro: "Микрозайм",
    consumer: "Потребительский кредит",
    mortgage: "Ипотека",
    auto: "Автокредит",
    business: "Бизнес-кредит",
    education: "Образовательный кредит",
    green: "Зелёный кредит",
    overdraft: "Овердрафт",
    loan: "Кредит"
  }

  return map[type] || type || "Не указан"

}

function formatAmount(value) {

  const amount = Number(value)

  if (
    !amount ||
    amount <= 0
  ) {
    return "Не указана"
  }

  return (
    new Intl.NumberFormat(
      "ru-RU"
    ).format(amount)
    + " UZS"
  )

}

function formatTerm(term) {

  if (
    term === null ||
    term === undefined ||
    term === ""
  ) {
    return "Не указан"
  }

  const months = Number(term)

  if (
    Number.isNaN(months)
  ) {
    return term
  }

  if (months < 12) {
    return `${months} мес.`
  }

  if (months % 12 === 0) {

    const years = months / 12

    if (years === 1) {
      return "1 год"
    }

    if (years >= 2 && years <= 4) {
      return `${years} года`
    }

    return `${years} лет`

  }

  return `${months} мес.`

}

</script>

<template>

<div class="card">

  <h3>
    📋 Основные параметры
  </h3>

  <div class="grid">

    <div class="item">

      <div class="icon">
        💳
      </div>

      <div class="label">
        Тип кредита
      </div>

      <div class="value">
        {{ getLoanType(product?.loan_type) }}
      </div>

    </div>

    <div class="item">

      <div class="icon">
        🏦
      </div>

      <div class="label">
        Банк
      </div>

      <div class="value">
        {{
          product?.bank?.name ||
          product?.bank_name ||
          "Не указан"
        }}
      </div>

    </div>

    <div class="item">

      <div class="icon">
        💰
      </div>

      <div class="label">
        Максимальная сумма
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

    <div class="item">

      <div class="icon">
        🌐
      </div>

      <div class="label">
        Источник
      </div>

      <div class="value">
        {{
          product?.source_name ||
          "Не указан"
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