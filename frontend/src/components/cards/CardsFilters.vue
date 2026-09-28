<script setup>

import { computed } from "vue"
import { useI18n } from "vue-i18n"
import { useCardsStore } from "@/stores/cards"

const { t } = useI18n()

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

    <!-- ========================================== -->
    <!-- 💰 CURRENCY -->
    <!-- ========================================== -->

    <button
      class="chip"
      :class="{
        active:
          store.filters.currency === 'all'
      }"
      @click="setCurrency('all')"
    >
      🔥 {{ t("cards.filters.all") }}
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


    <!-- ========================================== -->
    <!-- 💳 CARD SYSTEMS -->
    <!-- ========================================== -->

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


    <!-- ========================================== -->
    <!-- 🌐 ONLINE -->
    <!-- ========================================== -->

    <button
      class="chip"
      :class="{
        active:
          store.filters.online
      }"
      @click="toggleOnline"
    >
      🌐 {{ t("cards.filters.online") }}
    </button>


    <!-- ========================================== -->
    <!-- 🏦 BANK -->
    <!-- ========================================== -->

    <div class="bank-select-wrapper">

      <span class="bank-icon">
        🏦
      </span>


      <select
        class="bank-select"
        :value="
          store.filters.bank || 'all'
        "
        @change="setBank"
      >

        <option value="all">
          {{ t("cards.filters.allBanks") }}
        </option>


        <option
          v-for="bank in availableBanks"
          :key="bank.name"
          :value="bank.name"
        >
          {{ bank.name }}
        </option>

      </select>


      <!-- CUSTOM ARROW -->

      <span
        class="select-arrow"
        aria-hidden="true"
      >

        <svg
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >

          <path
            d="M6 9L12 15L18 9"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />

        </svg>

      </span>

    </div>

  </div>

</template>


<style scoped>

/* ========================================== */
/* 🎛 FILTERS */
/* ========================================== */

.filters {

  display: flex;

  flex-wrap: wrap;

  align-items: center;

  gap: 12px;

  margin: 24px 0;

}


/* ========================================== */
/* 🔘 CHIP */
/* ========================================== */

.chip {

  display: flex;

  align-items: center;

  justify-content: center;

  gap: 6px;

  min-height: 42px;

  padding: 12px 18px;

  border-radius: 999px;

  border: 1px solid #e5e7eb;

  background: white;

  color: #334155;

  font-size: 14px;

  font-weight: 600;

  cursor: pointer;

  transition:
    border-color .2s ease,
    color .2s ease,
    background .2s ease,
    transform .2s ease,
    box-shadow .2s ease;

}


.chip:hover {

  border-color: #2563eb;

  color: #2563eb;

  transform: translateY(-1px);

}


.chip.active {

  background: #2563eb;

  border-color: #2563eb;

  color: white;

  box-shadow:
    0 4px 12px
    rgba(37, 99, 235, .16);

}


/* ========================================== */
/* 🏦 BANK SELECT WRAPPER */
/* ========================================== */

.bank-select-wrapper {

  position: relative;

  display: flex;

  align-items: center;

  min-width: 220px;

  height: 42px;

}


/* ========================================== */
/* 🏦 BANK ICON */
/* ========================================== */

.bank-icon {

  position: absolute;

  left: 17px;

  top: 50%;

  z-index: 2;

  display: flex;

  align-items: center;

  justify-content: center;

  transform: translateY(-50%);

  pointer-events: none;

  font-size: 14px;

}


/* ========================================== */
/* 🏦 BANK SELECT */
/* ========================================== */

.bank-select {

  width: 100%;

  height: 42px;

  padding:
    0 42px
    0 42px;

  border: 1px solid #e5e7eb;

  border-radius: 999px;

  background: white;

  color: #334155;

  font-family: inherit;

  font-size: 14px;

  font-weight: 600;

  cursor: pointer;

  appearance: none;

  -webkit-appearance: none;

  -moz-appearance: none;

  outline: none;

  transition:
    border-color .2s ease,
    box-shadow .2s ease,
    transform .2s ease;

}


/* ========================================== */
/* ✨ HOVER */
/* ========================================== */

.bank-select:hover {

  border-color: #2563eb;

  transform: translateY(-1px);

}


/* ========================================== */
/* 🎯 FOCUS */
/* ========================================== */

.bank-select:focus {

  border-color: #2563eb;

  box-shadow:
    0 0 0 4px
    rgba(37, 99, 235, .12);

}


/* ========================================== */
/* 🔽 CUSTOM ARROW */
/* ========================================== */

.select-arrow {

  position: absolute;

  right: 16px;

  top: 50%;

  z-index: 2;

  display: flex;

  align-items: center;

  justify-content: center;

  width: 18px;

  height: 18px;

  transform:
    translateY(-50%);

  color: #64748b;

  pointer-events: none;

  transition:
    color .2s ease,
    transform .2s ease;

}


.select-arrow svg {

  width: 17px;

  height: 17px;

}


/* ========================================== */
/* 🔵 HOVER ARROW */
/* ========================================== */

.bank-select-wrapper:hover
.select-arrow {

  color: #2563eb;

}


/* ========================================== */
/* 📱 MOBILE */
/* ========================================== */

@media (max-width: 768px) {

  .filters {

    gap: 8px;

  }


  .chip {

    min-height: 40px;

    padding:
      10px 14px;

    font-size: 13px;

  }


  .bank-select-wrapper {

    width: 100%;

    min-width: 0;

  }


  .bank-select {

    width: 100%;

  }

}

</style>