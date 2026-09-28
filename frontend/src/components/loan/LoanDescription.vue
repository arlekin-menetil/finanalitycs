<script setup>

import { computed } from "vue"
import { useI18n } from "vue-i18n"

const props = defineProps({
  product: {
    type: Object,
    default: () => ({})
  }
})

const { t } = useI18n()

// ==========================================
// 📄 CLEAN DESCRIPTION
// ==========================================

const description = computed(() => {

  let text =
    props.product?.description || ""

  const cutMarkers = [

    "Предложение по кредитам",

    "Все кредиты",

    "О банке",

    "Вы также смотрели",

    "Все продукты на Bank.uz",

  ]

  for (const marker of cutMarkers) {

    if (text.includes(marker)) {

      text = text.split(marker)[0]

      break
    }
  }

  return text
    .replace(/\r/g, "")
    .trim()

})

// ==========================================
// 📄 PARSE FIELDS
// ==========================================

const labels = [

  "Последнее обновление информации",

  "Процентная ставка (%)",

  "Сумма",

  "Срок",

  "Уплата процентов",

  "Валюта",

  "Льготный период",

  "Первоначальный взнос",

  "Открытие",

  "Обеспечение по кредиту",

  "Возможные формы обеспечения",

  "Необходимые документы"

]

const escapedLabels = labels.map(
  label =>
    label.replace(
      /[.*+?^${}()|[\]\\]/g,
      "\\$&"
    )
)

const fields = computed(() => {

  const text =
    description.value

  if (!text) {
    return []
  }

  const result = []

  for (
    let i = 0;
    i < labels.length;
    i++
  ) {

    const currentLabel =
      labels[i]

    const currentEscaped =
      escapedLabels[i]

    const nextLabels =
      escapedLabels
        .slice(i + 1)
        .join("|")

    const regex =
      new RegExp(
        `${currentEscaped}\\s*:\\s*(.*?)${
          nextLabels
            ? `(?=(?:${nextLabels})\\s*:|$)`
            : "$"
        }`,
        "is"
      )

    const match =
      text.match(regex)

    if (!match) {
      continue
    }

    let value =
      match[1]
        .replace(/[ \t]+/g, " ")
        .replace(/\n+/g, " ")
        .trim()

    if (!value) {
      continue
    }

    value = value
      .replace(
        /\bО кредите\b/gi,
        ""
      )
      .trim()

    // ======================================
    // 💰 FORMAT AMOUNT
    // ======================================

    if (
      currentLabel === "Сумма"
    ) {

      value = value.replace(
        /до\s+(\d[\d\s]*)\s*сум/gi,
        (_, amount) => {

          const number =
            Number(
              amount.replace(
                /\s/g,
                ""
              )
            )

          if (
            Number.isNaN(number)
          ) {
            return _
          }

          return (
            "до " +
            number.toLocaleString(
              "ru-RU"
            ) +
            " сум"
          )

        }
      )
    }

    result.push({

      label:
        currentLabel,

      value

    })

  }

  return result

})

// ==========================================
// 📄 TRANSLATED LABELS
// ==========================================

const translatedFields = computed(() => {

  return fields.value.map(item => {

    const labelMap = {

      "Последнее обновление информации":
        "lastUpdate",

      "Процентная ставка (%)":
        "interestRate",

      "Сумма":
        "amount",

      "Срок":
        "term",

      "Уплата процентов":
        "interestPayment",

      "Валюта":
        "currency",

      "Льготный период":
        "gracePeriod",

      "Первоначальный взнос":
        "downPayment",

      "Открытие":
        "opening",

      "Обеспечение по кредиту":
        "collateral",

      "Возможные формы обеспечения":
        "collateralTypes",

      "Необходимые документы":
        "requiredDocuments",

    }

    const key =
      labelMap[item.label]

    return {

      ...item,

      label: key
        ? t(`loanDescription.fields.${key}`)
        : item.label,

    }

  })

})

// ==========================================
// 📄 HELPERS
// ==========================================

const hasFields = computed(() => {

  return (
    translatedFields.value.length > 0
  )

})

const shortDescription = computed(() => {

  if (
    !description.value
  ) {
    return ""
  }

  if (
    description.value.length <= 1000
  ) {
    return description.value
  }

  return (
    description.value.slice(
      0,
      1000
    ) + "..."
  )

})

</script>

<template>

<div class="card">

  <h3>
    📋 {{ t("loanDescription.title") }}
  </h3>

  <div
    v-if="hasFields"
    class="details-grid"
  >

    <div
      v-for="item in translatedFields"
      :key="item.label"
      class="detail-item"
    >

      <span>
        {{ item.label }}
      </span>

      <strong>
        {{ item.value }}
      </strong>

    </div>

  </div>

  <div
    v-else-if="shortDescription"
    class="raw-description"
  >

    {{ shortDescription }}

  </div>

  <div
    v-else
    class="empty-description"
  >

    {{ t("loanDescription.empty") }}

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

  margin:0 0 18px;

  font-size:20px;

  font-weight:700;

  color:#111827;

}

/* ==========================================
   DETAILS GRID
========================================== */

.details-grid{

  display:grid;

  grid-template-columns:
    repeat(
      auto-fit,
      minmax(260px,1fr)
    );

  gap:16px;

}

.detail-item{

  background:#f8fafc;

  border:1px solid #e5e7eb;

  border-radius:16px;

  padding:18px;

  transition:all .2s ease;

}

.detail-item:hover{

  transform:translateY(-2px);

  border-color:#cbd5e1;

}

.detail-item span{

  display:block;

  color:#64748b;

  font-size:13px;

  margin-bottom:8px;

}

.detail-item strong{

  display:block;

  color:#111827;

  font-size:16px;

  font-weight:700;

  line-height:1.5;

  word-break:break-word;

}

/* ==========================================
   RAW DESCRIPTION
========================================== */

.raw-description{

  white-space:pre-wrap;

  line-height:1.8;

  color:#334155;

  font-size:15px;

  word-break:break-word;

}

/* ==========================================
   EMPTY
========================================== */

.empty-description{

  color:#94a3b8;

  line-height:1.7;

  text-align:center;

  padding:24px 0;

}

/* ==========================================
   MOBILE
========================================== */

@media (max-width:768px){

  .details-grid{

    grid-template-columns:1fr;

  }

}

</style>