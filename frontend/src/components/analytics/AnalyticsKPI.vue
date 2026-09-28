<script setup>

import { computed } from "vue"
import { useI18n } from "vue-i18n"

const { t, locale } = useI18n()

const props = defineProps({

  productsLabel: {
    type: String,
    default: "",
  },

  totalProducts: {
    type: Number,
    default: 0,
  },

  avgInterest: {
    type: [Number, String],
    default: 0,
  },

  bestBank: {
    type: String,
    default: "",
  },

  totalLoanVolume: {
    type: Number,
    default: 0,
  },

  featuredBanks: {
    type: Array,
    default: () => [],
  },

})


// =====================================================
// ALL BANKS
// =====================================================

const allBanksLabel = computed(() => {
  return t("analytics.allBanks")
})


// =====================================================
// PRODUCTS LABEL
// =====================================================

const productsTitle = computed(() => {
  return props.productsLabel || t("analytics.kpi.totalProducts")
})


// =====================================================
// LOCALE
// =====================================================

const numberLocale = computed(() => {

  const locales = {
    ru: "ru-RU",
    en: "en-US",
    uz: "uz-UZ",
  }

  return locales[locale.value] || "ru-RU"

})


// =====================================================
// FORMATTED LIMIT
// =====================================================

const formattedLimit = computed(() => {

  const value =
    Number(props.totalLoanVolume || 0)

  if (!value) {
    return "0"
  }


  if (value >= 1000000000) {

    const billions =
      value / 1000000000

    return Number.isInteger(billions)
      ? `${billions} ${t("analytics.units.billion")}`
      : `${billions.toFixed(1)} ${t("analytics.units.billion")}`

  }


  return `${Math.round(
    value / 1000000
  )} ${t("analytics.units.million")}`

})


// =====================================================
// ALL BANKS CHECK
// =====================================================

const isAllBanks = computed(() => {

  return (
    !props.bestBank ||
    props.bestBank === allBanksLabel.value
  )

})

</script>


<template>

  <div class="kpi-grid">


    <!-- ================================================= -->
    <!-- ПРОДУКТЫ -->
    <!-- ================================================= -->

    <div class="kpi">

      <h4>
        {{ productsTitle }}
      </h4>

      <p>
        {{ totalProducts }}
      </p>

    </div>


    <!-- ================================================= -->
    <!-- СРЕДНЯЯ СТАВКА -->
    <!-- ================================================= -->

    <div class="kpi">

      <h4>
        {{ t("analytics.kpi.averageRate") }}
      </h4>

      <p>
        {{ avgInterest }}%
      </p>

    </div>


    <!-- ================================================= -->
    <!-- РЕКОМЕНДУЕМЫЕ БАНКИ -->
    <!-- ================================================= -->

    <div class="kpi">

      <h4>

        {{
          isAllBanks
            ? t("analytics.kpi.recommendedBanks")
            : t("analytics.kpi.recommendedBank")
        }}

      </h4>


      <div class="featured-banks">

        <template v-if="isAllBanks">

          <span
            v-for="bank in featuredBanks"
            :key="bank"
            class="bank-badge"
          >
            {{ bank }}
          </span>

        </template>


        <template v-else>

          <span class="bank-badge">
            {{ bestBank }}
          </span>

        </template>

      </div>

    </div>


    <!-- ================================================= -->
    <!-- МАКСИМАЛЬНЫЙ ЛИМИТ -->
    <!-- ================================================= -->

    <div class="kpi">

      <h4>
        {{ t("analytics.kpi.maximumLimit") }}
      </h4>

      <p>
        {{ formattedLimit }}
      </p>

    </div>


  </div>

</template>


<style scoped>

.kpi-grid {

  display: grid;

  grid-template-columns:
    repeat(
      auto-fit,
      minmax(
        240px,
        1fr
      )
    );

  gap: 16px;

  margin-bottom: 24px;

}


.kpi {

  background: #ffffff;

  padding: 24px;

  border-radius: 16px;

  box-shadow:
    0 2px 8px
    rgba(
      15,
      23,
      42,
      .05
    );

  transition:
    transform .2s ease,
    box-shadow .2s ease;

}


.kpi:hover {

  transform:
    translateY(-2px);

  box-shadow:
    0 8px 20px
    rgba(
      15,
      23,
      42,
      .08
    );

}


.kpi h4 {

  margin: 0 0 10px;

  color: #64748b;

  font-size: 14px;

  font-weight: 600;

}


.kpi p {

  margin: 0;

  font-size: 36px;

  font-weight: 800;

  color: #0f172a;

  line-height: 1.1;

}


.featured-banks {

  display: flex;

  flex-wrap: wrap;

  gap: 10px;

  margin-top: 8px;

}


.bank-badge {

  display: inline-flex;

  align-items: center;

  justify-content: center;

  padding: 8px 14px;

  border-radius: 999px;

  background: #fef3c7;

  color: #92400e;

  font-weight: 700;

  font-size: 14px;

  border: 1px solid #fde68a;

  white-space: nowrap;

}


@media (max-width: 768px) {

  .kpi-grid {

    grid-template-columns: 1fr;

  }


  .kpi p {

    font-size: 28px;

  }

}

</style>