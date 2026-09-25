<script setup>
import { onMounted } from "vue"

import { useCardsStore } from "@/stores/cards"

import CardsHero from "@/components/cards/CardsHero.vue"
import CardsBanks from "@/components/cards/CardsBanks.vue"
import CardsFilters from "@/components/cards/CardsFilters.vue"
import CardsSort from "@/components/cards/CardsSort.vue"
import CardsGrid from "@/components/cards/CardsGrid.vue"

const store = useCardsStore()

onMounted(async () => {
  await store.load()
})
</script>

<template>

  <div class="cards-page">

    <!-- ===================================== -->
    <!-- 💳 HERO -->
    <!-- ===================================== -->
    <CardsHero />

    <!-- ===================================== -->
    <!-- 🏦 POPULAR BANKS -->
    <!-- ===================================== -->
    <CardsBanks />

    <!-- ===================================== -->
    <!-- 🔥 FILTERS + SORT -->
    <!-- ===================================== -->
    <div class="toolbar">

      <CardsFilters />

      <CardsSort />

    </div>

    <!-- ===================================== -->
    <!-- 💳 CARDS -->
    <!-- ===================================== -->
    <CardsGrid />

  </div>

</template>

<style scoped>

.cards-page {

  width: 100%;

  padding: 24px;

  display: flex;

  flex-direction: column;

  gap: 24px;
}

.toolbar {

  display: flex;

  justify-content: space-between;

  align-items: flex-start;

  gap: 20px;

  flex-wrap: wrap;
}

@media (max-width: 768px) {

  .cards-page {

    padding: 16px;
  }

  .toolbar {

    flex-direction: column;

    align-items: stretch;
  }
}

</style>