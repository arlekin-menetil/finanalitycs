<script setup>
import { useI18n } from "vue-i18n"
import { useDepositsStore } from "@/stores/deposits"

const { t } = useI18n()

const store = useDepositsStore()
</script>

<template>

  <select
    v-model="store.sort"
    class="sort"
  >

    <option value="rate">
      💰 {{ t("deposits.sort.maxRate") }}
    </option>

    <option value="term">
      📅 {{ t("deposits.sort.term") }}
    </option>

    <option value="bank">
      🏦 {{ t("deposits.sort.bank") }}
    </option>

  </select>

</template>

<style scoped>
.sort {
  padding: 12px 16px;
  border-radius: 16px;
  border: 1px solid #dbe2ea;
}
</style>