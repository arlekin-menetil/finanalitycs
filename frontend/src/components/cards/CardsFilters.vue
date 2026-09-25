<script setup>

import { computed } from "vue"
import { useCardsStore } from "@/stores/cards"

const store = useCardsStore()

const availableBanks = computed(() => {

  return store.banks

})

function setCurrency(value) {

  store.filters.currency = value

}

function setSystem(value) {

  store.filters.system =
    store.filters.system === value
      ? "all"
      : value

}

function toggleOnline() {

  store.filters.online =
    !store.filters.online

}

function setBank(event) {

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

    <!-- ВАЛЮТА -->

    <button
      class="chip"
      :class="{
        active:
          store.filters.currency === 'all'
      }"
      @click="setCurrency('all')"
    >
      🔥 Все
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

    <!-- СИСТЕМЫ -->

    <button
      class="chip"
      :class="{
        active:
          store.filters.system === 'VISA'
      }"
      @click="setSystem('VISA')"
    >
      💳 Visa
    </button>

    <button
      class="chip"
      :class="{
        active:
          store.filters.system === 'MASTERCARD'
      }"
      @click="setSystem('MASTERCARD')"
    >
      💳 MasterCard
    </button>

    <button
      class="chip"
      :class="{
        active:
          store.filters.system === 'HUMO'
      }"
      @click="setSystem('HUMO')"
    >
      🇺🇿 HUMO
    </button>

    <button
      class="chip"
      :class="{
        active:
          store.filters.system === 'UZCARD'
      }"
      @click="setSystem('UZCARD')"
    >
      🇺🇿 UZCARD
    </button>

    <!-- ОНЛАЙН -->

    <button
      class="chip"
      :class="{
        active:
          store.filters.online
      }"
      @click="toggleOnline"
    >
      🌐 Онлайн оформление
    </button>

    <!-- БАНК -->

    <select
      class="bank-select"
      @change="setBank"
    >

      <option value="all">
        🏦 Все банки
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

.filters {

  display:flex;

  flex-wrap:wrap;

  gap:12px;

  margin:24px 0;
}

.chip {

  display:flex;

  align-items:center;

  gap:6px;

  padding:12px 18px;

  border-radius:999px;

  border:1px solid #e5e7eb;

  background:white;

  color:#334155;

  font-size:14px;

  font-weight:600;

  cursor:pointer;

  transition:all .2s ease;
}

.chip:hover {

  border-color:#2563eb;

  color:#2563eb;

  transform:translateY(-1px);
}

.chip.active {

  background:#2563eb;

  border-color:#2563eb;

  color:white;
}

.bank-select {

  padding:12px 18px;

  border-radius:999px;

  border:1px solid #e5e7eb;

  background:white;

  color:#334155;

  font-size:14px;

  font-weight:600;

  cursor:pointer;

  transition:.2s ease;

  min-width:220px;
}

.bank-select:hover {

  border-color:#2563eb;
}

.bank-select:focus {

  outline:none;

  border-color:#2563eb;

  box-shadow:
    0 0 0 4px
    rgba(37,99,235,.12);
}

@media (max-width:768px) {

  .filters {

    gap:8px;
  }

  .chip {

    padding:10px 14px;

    font-size:13px;
  }

  .bank-select {

    width:100%;
  }
}

</style>