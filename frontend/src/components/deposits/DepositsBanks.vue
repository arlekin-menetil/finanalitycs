<script setup>

import { computed } from "vue"
import { storeToRefs } from "pinia"
import { useI18n } from "vue-i18n"

import { useDepositsStore } from "@/stores/deposits"

const { t } = useI18n()

const store = useDepositsStore()

const {
  banks,
  recommendedBanks,
} = storeToRefs(store)


// ==========================================
// 🏦 SORTED BANKS
// ==========================================

const sortedBanks = computed(() => {

  const result = [...banks.value]

  result.sort((a, b) => {

    if (
      Number(b.count || 0) !==
      Number(a.count || 0)
    ) {

      return (
        Number(b.count || 0) -
        Number(a.count || 0)
      )

    }

    return String(
      a.name || ""
    ).localeCompare(
      String(
        b.name || ""
      )
    )

  })

  return result

})


// ==========================================
// 🔟 TOP BANKS
// ==========================================

const topBanks = computed(() => {

  return sortedBanks.value.slice(
    0,
    10
  )

})

</script>


<template>

  <div class="banks-wrapper">

    <!-- =================================== -->
    <!-- 🤖 RECOMMENDED -->
    <!-- =================================== -->

    <section
      v-if="recommendedBanks.length"
      class="section"
    >

      <h2 class="section-title">
        {{ t("deposits.banks.recommended") }}
      </h2>

      <div class="banks">

        <div
          v-for="bank in recommendedBanks"
          :key="`recommended-${bank.name}`"
          class="bank-card recommended"
        >

          <strong class="bank-name">
            {{ bank.name }}
          </strong>

          <div class="bank-score">

            {{ t("deposits.banks.match") }}
            {{ bank.score }}%

          </div>

          <div
            v-if="bank.best_rate"
            class="bank-rate"
          >

            {{ t("deposits.banks.rateTo") }}
            {{ bank.best_rate }}%

          </div>

          <div class="bank-count">

            {{ bank.count }}
            {{ t("deposits.banks.deposits") }}

          </div>

        </div>

      </div>

    </section>


    <!-- =================================== -->
    <!-- 🏦 POPULAR -->
    <!-- =================================== -->

    <section
      v-if="topBanks.length"
      class="section"
    >

      <h2 class="section-title">
        {{ t("deposits.banks.popular") }}
      </h2>

      <div class="banks">

        <div
          v-for="bank in topBanks"
          :key="bank.name"
          class="bank-card"
        >

          <strong class="bank-name">
            {{ bank.name }}
          </strong>

          <div
            v-if="bank.count"
            class="bank-count"
          >

            {{ bank.count }}
            {{ t("deposits.banks.deposits") }}

          </div>

        </div>

      </div>

    </section>

  </div>

</template>


<style scoped>

.banks-wrapper {

  display: flex;

  flex-direction: column;

  gap: 28px;

}


.section {

  width: 100%;
}


.banks {

  display: flex;

  gap: 12px;

  flex-wrap: wrap;

}


.bank-card {

  background: white;

  border-radius: 16px;

  padding: 16px;

  min-width: 180px;

  border: 1px solid #e5e7eb;

  transition:
    transform .2s ease,
    box-shadow .2s ease;

}


.bank-card:hover {

  transform: translateY(-2px);

  box-shadow:
    0 8px 20px
    rgba(0, 0, 0, 0.06);

}


.recommended {

  border: 2px solid #2563eb;

  background: #eff6ff;

}


.recommended strong {

  color: #1d4ed8;

}


.bank-name {

  display: block;

  font-size: 16px;

  font-weight: 700;

}


.bank-score {

  margin-top: 8px;

  font-size: 14px;

  font-weight: 600;

  color: #2563eb;

}


.bank-rate {

  margin-top: 6px;

  font-size: 13px;

  font-weight: 600;

  color: #059669;

}


.bank-count {

  margin-top: 6px;

  color: #6b7280;

  font-size: 13px;

}

</style>