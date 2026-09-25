<script setup>

import { computed } from "vue"

const props = defineProps({

  productsLabel: {
    type: String,
    default: "Всего продуктов"
  },

  totalProducts: {
    type: Number,
    default: 0
  },

  avgInterest: {
    type: [Number, String],
    default: 0
  },

  bestBank: {
    type: String,
    default: "Все банки"
  },

  totalLoanVolume: {
    type: Number,
    default: 0
  },

  featuredBanks: {
    type: Array,
    default: () => []
  }

})

const formattedLimit = computed(() => {

  const value =
    Number(props.totalLoanVolume || 0)

  if (!value) {
    return "0"
  }

  if (value >= 1000000000) {

    const billions =
      value / 1000000000

    return Number.isInteger(
      billions
    )
      ? `${billions} млрд`
      : `${billions.toFixed(1)} млрд`

  }

  return `${Math.round(
    value / 1000000
  )} млн`

})

const isAllBanks = computed(() => {

  return (
    props.bestBank === "Все банки" ||
    !props.bestBank
  )

})

</script>

<template>

  <div class="kpi-grid">

    <!-- Продукты -->

    <div class="kpi">

      <h4>
        {{ productsLabel }}
      </h4>

      <p>
        {{ totalProducts }}
      </p>

    </div>

    <!-- Средняя ставка -->

    <div class="kpi">

      <h4>
        Средняя ставка
      </h4>

      <p>
        {{ avgInterest }}%
      </p>

    </div>

    <!-- Рекомендуемые банки -->

    <div class="kpi">

      <h4>

        {{
          isAllBanks
            ? "Рекомендуемые банки"
            : "Рекомендуемый банк"
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

    <!-- Максимальный лимит -->

    <div class="kpi">

      <h4>
        Максимальный лимит
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