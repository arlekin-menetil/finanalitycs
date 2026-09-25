<script setup>
import { useDepositsStore } from "@/stores/deposits"

const store = useDepositsStore()
</script>

<template>

  <select
    v-model="store.sort"
    class="sort"
  >
    <option value="rate">
      💰 Максимальная ставка
    </option>

    <option value="term">
      📅 Срок
    </option>

    <option value="bank">
      🏦 Банк
    </option>
  </select>

</template>

<style scoped>
.sort{
  padding:12px 16px;
  border-radius:16px;
  border:1px solid #dbe2ea;
}
</style>