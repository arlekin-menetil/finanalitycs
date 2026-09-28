<script setup>

import { computed } from "vue"
import { storeToRefs } from "pinia"
import { useI18n } from "vue-i18n"

import { useCardsStore } from "@/stores/cards"

const { t } = useI18n()

const store = useCardsStore()

const {
  banks,
} = storeToRefs(store)

// ==========================================
// 🏦 PRIORITY BANKS
// ==========================================

const priorityBanks = [

  "Hamkorbank",

  "Aloqabank",

  "Kapitalbank",

  "SQB",

  "NBU",

  "Ipak Yuli Bank",

  "Uzum Bank",

]

// ==========================================
// 🏦 SORTED BANKS
// ==========================================

const sortedBanks = computed(() => {

  return [...banks.value].sort(
    (a, b) => {

      const aPriority =
        priorityBanks.indexOf(
          a.name
        )

      const bPriority =
        priorityBanks.indexOf(
          b.name
        )

      // оба банка приоритетные
      if (
        aPriority !== -1 &&
        bPriority !== -1
      ) {

        return (
          aPriority -
          bPriority
        )
      }

      // только A приоритетный
      if (
        aPriority !== -1
      ) {
        return -1
      }

      // только B приоритетный
      if (
        bPriority !== -1
      ) {
        return 1
      }

      // остальные по количеству карт
      return (
        b.count -
        a.count
      )
    }
  )
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
    <!-- 🏦 POPULAR -->
    <!-- =================================== -->

    <div class="section">

      <h2 class="section-title">
        🏦 {{ t("cards.popularBanks") }}
      </h2>

      <div class="banks">

        <div
          v-for="bank in topBanks"
          :key="bank.name"
          class="bank-card"
        >

          <strong>
            {{ bank.name }}
          </strong>

          <div class="bank-count">
            {{ bank.count }} {{ t("cards.cardsCount") }}
          </div>

        </div>

      </div>

    </div>

  </div>

</template>

<style scoped>

.banks-wrapper {

  display: flex;

  flex-direction: column;

  gap: 28px;
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

  transition: .2s ease;
}

.bank-card:hover {

  transform: translateY(-2px);
}

.recommended {

  border: 2px solid #2563eb;

  background: #eff6ff;
}

.recommended strong {

  color: #1d4ed8;
}

.bank-score {

  margin-top: 8px;

  font-size: 14px;

  font-weight: 600;

  color: #2563eb;
}

.bank-count {

  margin-top: 6px;

  color: #6b7280;

  font-size: 13px;
}

</style>