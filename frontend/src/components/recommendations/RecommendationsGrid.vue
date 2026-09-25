<script setup>

import {
  computed,
  ref,
  nextTick
} from "vue"

import RecommendationCard from "./RecommendationCard.vue"

const props = defineProps({

  items: {
    type: Array,
    default: () => [],
  },

  loading: {
    type: Boolean,
    default: false,
  },
})

// ======================================
// 📄 PAGINATION
// ======================================

const currentPage = ref(1)

const perPage = 9

const gridRef = ref(null)

// ======================================
// 📄 TOTAL PAGES
// ======================================

const totalPages = computed(() => {

  return Math.max(
    1,
    Math.ceil(
      props.items.length / perPage
    )
  )
})

// ======================================
// 📄 CURRENT PAGE ITEMS
// ======================================

const paginatedItems = computed(() => {

  const start =
    (currentPage.value - 1) * perPage

  const end =
    start + perPage

  return props.items.slice(
    start,
    end
  )
})

// ======================================
// 📄 PAGINATION RANGE
// ======================================

const visiblePages = computed(() => {

  const total = totalPages.value
  const current = currentPage.value

  const pages = []

  if (total <= 7) {

    for (let i = 1; i <= total; i++) {
      pages.push(i)
    }

    return pages
  }

  pages.push(1)

  if (current > 4) {
    pages.push("...")
  }

  const start =
    Math.max(2, current - 2)

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
    current < total - 3
  ) {
    pages.push("...")
  }

  pages.push(total)

  return pages
})

// ======================================
// 📄 INFO
// ======================================

const startItem = computed(() => {

  if (!props.items.length) {
    return 0
  }

  return (
    (currentPage.value - 1) *
    perPage +
    1
  )
})

const endItem = computed(() => {

  return Math.min(
    currentPage.value * perPage,
    props.items.length
  )
})

// ======================================
// 🔝 SCROLL TO GRID
// ======================================

async function scrollToGrid() {

  await nextTick()

  gridRef.value?.scrollIntoView({
    behavior: "smooth",
    block: "start"
  })
}

// ======================================
// 📄 PAGE CHANGE
// ======================================

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

</script>

<template>

  <!-- ====================================== -->
  <!-- 💣 LOADING -->
  <!-- ====================================== -->

  <div
    v-if="loading"
    class="loading-grid"
  >

    <div
      v-for="n in 6"
      :key="n"
      class="skeleton-card"
    />

  </div>

  <!-- ====================================== -->
  <!-- 💣 EMPTY -->
  <!-- ====================================== -->

  <div
    v-else-if="!items.length"
    class="empty"
  >

    <div class="empty-icon">
      🏦
    </div>

    <h2>
      Ничего не найдено
    </h2>

    <p>
      Попробуйте изменить фильтры
    </p>

  </div>

  <!-- ====================================== -->
  <!-- 💣 GRID -->
  <!-- ====================================== -->

  <div v-else>

    <div
      ref="gridRef"
      class="grid"
    >

      <RecommendationCard
        v-for="item in paginatedItems"
        :key="item.id"
        :item="item"
      />

    </div>

    <!-- ====================================== -->
    <!-- 📄 PAGINATION -->
    <!-- ====================================== -->

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
        {{ items.length }}
        продуктов

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

/* ======================================
💣 GRID
====================================== */

.grid {

  display: grid;

  grid-template-columns:
    repeat(
      auto-fill,
      minmax(340px,1fr)
    );

  gap: 22px;
}

/* ======================================
💣 LOADING
====================================== */

.loading-grid {

  display: grid;

  grid-template-columns:
    repeat(
      auto-fill,
      minmax(340px,1fr)
    );

  gap: 22px;
}

.skeleton-card {

  height: 320px;

  border-radius: 24px;

  background:
    linear-gradient(
      90deg,
      #f1f5f9 25%,
      #e2e8f0 50%,
      #f1f5f9 75%
    );

  background-size: 200% 100%;

  animation:
    skeleton 1.2s infinite;
}

@keyframes skeleton {

  0% {

    background-position:
      200% 0;
  }

  100% {

    background-position:
      -200% 0;
  }
}

/* ======================================
💣 EMPTY
====================================== */

.empty {

  padding: 80px 20px;

  text-align: center;

  border-radius: 28px;

  background: white;

  border:
    1px solid #e2e8f0;
}

.empty-icon {

  font-size: 64px;

  margin-bottom: 20px;
}

.empty h2 {

  margin: 0;

  font-size: 28px;

  font-weight: 800;
}

.empty p {

  margin-top: 12px;

  color: #64748b;

  font-size: 16px;
}

/* ======================================
📄 PAGINATION
====================================== */

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

/* ======================================
📱 MOBILE
====================================== */

@media (max-width: 768px) {

  .grid {

    grid-template-columns:
      1fr;
  }

  .loading-grid {

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