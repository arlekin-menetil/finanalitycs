<script setup>

import {
  computed,
  ref,
  watch,
  nextTick,
} from "vue"

import { storeToRefs } from "pinia"
import { useI18n } from "vue-i18n"

import { useCardsStore } from "@/stores/cards"
import CardCard from "./CardCard.vue"

const { t } = useI18n()

const store = useCardsStore()

const {
  filteredCards,
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
// 💳 SORTED CARDS
// ==========================================

const cards = computed(() => {

  const data = [
    ...filteredCards.value,
  ]

  data.sort((a, b) => {

    const aBank =
      a.bank_name ||
      a.bank?.name ||
      ""

    const bBank =
      b.bank_name ||
      b.bank?.name ||
      ""

    const aPriority =
      priorityBanks.indexOf(
        aBank,
      )

    const bPriority =
      priorityBanks.indexOf(
        bBank,
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


    // остальные по алфавиту

    return aBank.localeCompare(
      bBank,
    )

  })

  return data

})


// ==========================================
// 📄 PAGINATION
// ==========================================

const currentPage = ref(1)

const perPage = 9

const gridRef = ref(null)

const totalPages = computed(() => {

  return Math.max(
    1,
    Math.ceil(
      cards.value.length /
      perPage,
    ),
  )

})


const paginatedCards = computed(() => {

  const start =
    (currentPage.value - 1) *
    perPage

  const end =
    start + perPage

  return cards.value.slice(
    start,
    end,
  )

})


// ==========================================
// 📄 VISIBLE PAGES
// ==========================================

const visiblePages = computed(() => {

  const total =
    totalPages.value

  const current =
    currentPage.value

  const pages = []


  if (total <= 7) {

    for (
      let i = 1;
      i <= total;
      i++
    ) {

      pages.push(i)

    }

    return pages

  }


  pages.push(1)


  if (current > 4) {

    pages.push("...")

  }


  const start =
    Math.max(
      2,
      current - 2,
    )


  const end =
    Math.min(
      total - 1,
      current + 2,
    )


  for (
    let i = start;
    i <= end;
    i++
  ) {

    pages.push(i)

  }


  if (
    current <
    total - 3
  ) {

    pages.push("...")

  }


  pages.push(total)

  return pages

})


// ==========================================
// 📄 PAGE INFO
// ==========================================

const startItem = computed(() => {

  if (
    !cards.value.length
  ) {

    return 0

  }

  return (
    (
      currentPage.value - 1
    ) *
      perPage +
    1
  )

})


const endItem = computed(() => {

  return Math.min(
    currentPage.value *
      perPage,
    cards.value.length,
  )

})


// ==========================================
// 🔝 SCROLL TO GRID
// ==========================================

async function scrollToGrid() {

  await nextTick()

  gridRef.value?.scrollIntoView({

    behavior: "smooth",

    block: "start",

  })

}


// ==========================================
// 📄 PAGE CHANGE
// ==========================================

async function goToPage(page) {

  if (
    page < 1 ||
    page > totalPages.value
  ) {

    return

  }

  currentPage.value = page

  await scrollToGrid()

}


// ==========================================
// 🔄 RESET PAGE
// ==========================================

watch(
  () => [

    store.filters.currency,

    store.filters.system,

    store.filters.online,

    store.filters.bank,

    store.sort,

  ],

  async () => {

    currentPage.value = 1

    await scrollToGrid()

  },
)

</script>


<template>

  <div>

    <!-- GRID -->

    <div
      ref="gridRef"
      class="grid"
    >

      <CardCard
        v-for="item in paginatedCards"
        :key="item.id"
        :item="item"
      />

    </div>


    <!-- PAGINATION -->

    <div
      v-if="totalPages > 1"
      class="pagination-wrapper"
    >

      <!-- PAGINATION INFO -->

      <div class="pagination-info">

        {{ t("cards.pagination.showing") }}

        {{ startItem }}

        –

        {{ endItem }}

        {{ t("cards.pagination.of") }}

        {{ cards.length }}

        {{ t("cards.pagination.cards") }}

      </div>


      <!-- PAGINATION BUTTONS -->

      <div class="pagination">

        <button
          class="page-btn"
          :disabled="currentPage === 1"
          @click="goToPage(currentPage - 1)"
        >

          ←

        </button>


        <template
          v-for="page in visiblePages"
          :key="`${page}`"
        >

          <span
            v-if="page === '...'"
            class="dots"
          >

            ...

          </span>


          <button
            v-else
            class="page-btn"
            :class="{
              active:
                page === currentPage,
            }"
            @click="goToPage(page)"
          >

            {{ page }}

          </button>

        </template>


        <button
          class="page-btn"
          :disabled="
            currentPage === totalPages
          "
          @click="goToPage(currentPage + 1)"
        >

          →

        </button>

      </div>

    </div>

  </div>

</template>


<style scoped>

.grid {

  display: grid;

  gap: 24px;

  grid-template-columns:
    repeat(
      auto-fill,
      minmax(350px, 1fr)
    );

}


/* ==========================================
📄 PAGINATION
========================================== */

.pagination-wrapper {

  width: 100%;

  display: flex;

  flex-direction: column;

  align-items: center;

  justify-content: center;

  margin-top: 40px;

}


.pagination-info {

  width: 100%;

  display: flex;

  justify-content: center;

  align-items: center;

  text-align: center;

  margin-bottom: 20px;

}


.pagination {

  display: flex;

  justify-content: center;

  align-items: center;

  gap: 10px;

  width: 100%;

  flex-wrap: wrap;

}


.page-btn {

  min-width: 42px;

  height: 42px;

  padding: 0 12px;

  border: 1px solid #e5e7eb;

  border-radius: 12px;

  background: white;

  cursor: pointer;

  font-weight: 600;

  transition: .2s;

}


.page-btn:hover {

  border-color: #2563eb;

  color: #2563eb;

}


.page-btn.active {

  background: #2563eb;

  border-color: #2563eb;

  color: white;

}


.page-btn:disabled {

  opacity: .4;

  cursor: not-allowed;

}

</style>