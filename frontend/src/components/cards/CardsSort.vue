<script setup>

import { useI18n } from "vue-i18n"
import { useCardsStore } from "@/stores/cards"

const { t } = useI18n()

const store = useCardsStore()

</script>


<template>

  <div class="sort-wrapper">

    <select
      v-model="store.sort"
      class="sort"
    >

      <option value="rate">
        💰 {{ t("cards.sort.maxRate") }}
      </option>

      <option value="term">
        📅 {{ t("cards.sort.term") }}
      </option>

      <option value="bank">
        🏦 {{ t("cards.sort.bank") }}
      </option>

    </select>


    <!-- CUSTOM ARROW -->

    <span
      class="sort-arrow"
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

</template>


<style scoped>

/* ========================================== */
/* 🔽 SORT WRAPPER */
/* ========================================== */

.sort-wrapper {

  position: relative;

  display: inline-flex;

  align-items: center;

  min-width: 220px;

  height: 42px;

}


/* ========================================== */
/* 🔽 SELECT */
/* ========================================== */

.sort {

  width: 100%;

  height: 42px;

  padding:
    0 44px
    0 16px;

  border: 1px solid #dbe2ea;

  border-radius: 999px;

  background: white;

  color: #334155;

  font-family: inherit;

  font-size: 14px;

  font-weight: 600;

  cursor: pointer;

  outline: none;

  appearance: none;

  -webkit-appearance: none;

  -moz-appearance: none;

  transition:
    border-color .2s ease,
    box-shadow .2s ease,
    transform .2s ease;

}


/* ========================================== */
/* ✨ HOVER */
/* ========================================== */

.sort:hover {

  border-color: #2563eb;

  transform: translateY(-1px);

}


/* ========================================== */
/* 🎯 FOCUS */
/* ========================================== */

.sort:focus {

  border-color: #2563eb;

  box-shadow:
    0 0 0 4px
    rgba(37, 99, 235, .12);

}


/* ========================================== */
/* 🔽 CUSTOM ARROW */
/* ========================================== */

.sort-arrow {

  position: absolute;

  right: 15px;

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


.sort-arrow svg {

  width: 17px;

  height: 17px;

}


/* ========================================== */
/* 🔵 HOVER ARROW */
/* ========================================== */

.sort-wrapper:hover
.sort-arrow {

  color: #2563eb;

}


/* ========================================== */
/* 📱 MOBILE */
/* ========================================== */

@media (max-width: 768px) {

  .sort-wrapper {

    width: 100%;

    min-width: 0;

  }

  .sort {

    width: 100%;

  }

}

</style>