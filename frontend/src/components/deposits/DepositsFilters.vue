<script setup>

import { computed } from "vue"
import { useI18n } from "vue-i18n"
import { useDepositsStore } from "@/stores/deposits"

const { t } = useI18n()

const store = useDepositsStore()

const availableBanks = computed(() => {

  return store.banks

})

const setCurrency = (value) => {

  store.filters.currency = value

}

const setRate = (value) => {

  store.filters.rate = value

}

const setBank = (event) => {

  const value =
    event.target.value

  store.filters.bank =

    value === "all"
      ? null
      : value

}

</script>

<template>

  <div class="filters">

    <button
      class="chip"
      :class="{
        active:
          store.filters.currency === 'all'
      }"
      @click="setCurrency('all')"
    >
      🔥 {{ t("deposits.filters.all") }}
    </button>

    <button
      class="chip"
      :class="{
        active:
          store.filters.currency === 'uzs'
      }"
      @click="setCurrency('uzs')"
    >
      💵 UZS
    </button>

    <button
      class="chip"
      :class="{
        active:
          store.filters.currency === 'usd'
      }"
      @click="setCurrency('usd')"
    >
      💲 USD
    </button>

    <button
      class="chip"
      :class="{
        active:
          store.filters.rate === 'high'
      }"
      @click="setRate('high')"
    >
      📈 {{ t("deposits.filters.highRate") }}
    </button>

    <select
      class="bank-select"
      @change="setBank"
    >

      <option value="all">
        🏦 {{ t("deposits.filters.allBanks") }}
      </option>

      <option
        v-for="bank in availableBanks"
        :key="bank.name"
        :value="bank.name"
      >
        {{ bank.name }}
      </option>

    </select>

  </div>

</template>

<style scoped>

.filters{

  display:flex;

  gap:12px;

  flex-wrap:wrap;

  align-items:center;

  margin:24px 0;

}

.chip{

  border:none;

  padding:12px 18px;

  border-radius:999px;

  cursor:pointer;

  background:white;

  border:1px solid #e5e7eb;

  font-weight:600;

  transition:.2s ease;

}

.chip:hover{

  background:#f8fafc;

}

.active{

  background:#2563eb;

  color:white;

  border-color:#2563eb;

}

.bank-select{

  border:none;

  padding:12px 18px;

  border-radius:999px;

  cursor:pointer;

  background:white;

  border:1px solid #e5e7eb;

  font-weight:600;

  min-width:220px;

  transition:.2s ease;

}

.bank-select:focus{

  outline:none;

  border-color:#2563eb;

}

@media(max-width:768px){

  .filters{

    flex-direction:column;

    align-items:stretch;

  }

  .bank-select{

    width:100%;

  }

}

</style>