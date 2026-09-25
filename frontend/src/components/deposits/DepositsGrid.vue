<script setup>

import {
  computed,
  ref,
  watch,
  nextTick
} from "vue"

import { storeToRefs } from "pinia"

import { useDepositsStore }
from "@/stores/deposits"

import DepositCard
from "./DepositCard.vue"

const store = useDepositsStore()

const {
  filteredDeposits,
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
// 💰 FILTERS + SORT
// ==========================================

const deposits = computed(() => {

  const data = [
    ...filteredDeposits.value
  ]

  data.sort((a, b) => {

    const aBank =
      a.bank_name || ""

    const bBank =
      b.bank_name || ""

    const aPriority =
      priorityBanks.indexOf(aBank)

    const bPriority =
      priorityBanks.indexOf(bBank)

    if (
      aPriority !== -1 &&
      bPriority !== -1
    ) {

      if (
        aPriority !== bPriority
      ) {

        return (
          aPriority -
          bPriority
        )
      }

      return (
        Number(
          b.interest_rate || 0
        ) -
        Number(
          a.interest_rate || 0
        )
      )
    }

    if (
      aPriority !== -1
    ) {
      return -1
    }

    if (
      bPriority !== -1
    ) {
      return 1
    }

    return (
      Number(
        b.interest_rate || 0
      ) -
      Number(
        a.interest_rate || 0
      )
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
      deposits.value.length /
      perPage
    )
  )
})

const paginatedDeposits = computed(() => {

  const start =
    (currentPage.value - 1) *
    perPage

  const end =
    start + perPage

  return deposits.value.slice(
    start,
    end
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
      current - 2
    )

  const end =
    Math.min(
      total - 1,
      current + 2
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
    !deposits.value.length
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
    deposits.value.length
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

    store.filters.rate,

    store.filters.currency,

    store.filters.bank,

    store.filters.term,

    store.sort

  ],
  async () => {

    currentPage.value = 1

    await scrollToGrid()
  }
)

</script>

<template>

  <div>

    <!-- GRID -->

    <div
      ref="gridRef"
      class="grid"
    >

      <DepositCard
        v-for="item in paginatedDeposits"
        :key="item.id"
        :item="item"
      />

    </div>

    <!-- PAGINATION -->

    <div
      v-if="totalPages > 1"
      class="pagination-wrapper"
    >

      <div class="pagination-info">

        Показано
        {{ startItem }}
        –
        {{ endItem }}
        из
        {{ deposits.length }}
        вкладов

      </div>

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
                page === currentPage
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

/* ==========================================
💰 GRID
========================================== */

.grid {

  display: grid;

  gap: 24px;

  grid-template-columns:
    repeat(
      auto-fill,
      minmax(350px,1fr)
    );
}

/* ==========================================
📄 PAGINATION
========================================== */

.pagination-wrapper {

  display: flex;

  flex-direction: column;

  align-items: center;

  gap: 16px;

  margin-top: 40px;
}

.pagination-info {

  color: #64748b;

  font-size: 14px;

  font-weight: 500;
}

.pagination {

  display: flex;

  justify-content: center;

  align-items: center;

  gap: 10px;

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

  transition: all .2s ease;
}

.page-btn:hover {

  border-color: #2563eb;

  color: #2563eb;

  transform: translateY(-1px);
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

.dots {

  display: flex;

  align-items: center;

  justify-content: center;

  min-width: 32px;

  height: 42px;

  color: #94a3b8;

  font-weight: 700;

  user-select: none;
}

/* ==========================================
📱 MOBILE
========================================== */

@media (max-width: 768px) {

  .grid {

    grid-template-columns:
      1fr;
  }

  .pagination {

    gap: 8px;
  }

  .page-btn {

    min-width: 38px;

    height: 38px;
  }

  .dots {

    height: 38px;
  }
}

</style>