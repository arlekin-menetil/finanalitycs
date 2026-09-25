<script setup>
import { onMounted } from "vue"

import { useDepositsStore } from "@/stores/deposits"

import DepositsHero from "@/components/deposits/DepositsHero.vue"
import DepositsBanks from "@/components/deposits/DepositsBanks.vue"
import DepositsFilters from "@/components/deposits/DepositsFilters.vue"
import DepositsSort from "@/components/deposits/DepositsSort.vue"
import DepositsGrid from "@/components/deposits/DepositsGrid.vue"

const store = useDepositsStore()

onMounted(async () => {
  await store.load()
})
</script>

<template>

  <div class="deposits-page">

    <!-- ===================================== -->
    <!-- 🏦 HERO -->
    <!-- ===================================== -->
    <DepositsHero />

    <!-- ===================================== -->
    <!-- 🏦 POPULAR BANKS -->
    <!-- ===================================== -->
    <DepositsBanks />

    <!-- ===================================== -->
    <!-- 🔥 FILTERS + SORT -->
    <!-- ===================================== -->
    <div class="toolbar">

      <DepositsFilters />

      <DepositsSort />

    </div>

    <!-- ===================================== -->
    <!-- 📦 PRODUCTS -->
    <!-- ===================================== -->
    <DepositsGrid />

  </div>

</template>

<style scoped>

.deposits-page {

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

  .deposits-page {

    padding: 16px;
  }

  .toolbar {

    flex-direction: column;

    align-items: stretch;
  }
}

</style>