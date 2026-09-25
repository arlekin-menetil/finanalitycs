<script>
export default {

  name: "RecommendationsFilters",

  props: {

    filterType: {
      type: String,
      default: "all",
    },

    sortType: {
      type: String,
      default: "match",
    },

    onlineOnly: {
      type: Boolean,
      default: false,
    },

    bankFilter: {
      type: String,
      default: "all",
    },

    availableBanks: {
      type: Array,
      default: () => [],
    },
  },

  emits: [

    "update:filterType",

    "update:sortType",

    "update:onlineOnly",

    "update:bankFilter",
  ],

  methods: {

    // ==========================================
    // 💣 CATEGORY
    // ==========================================
    setFilter(type) {

      this.$emit(
        "update:filterType",
        type
      )
    },

    // ==========================================
    // ⚡ ONLINE
    // ==========================================
    toggleOnline() {

      this.$emit(
        "update:onlineOnly",
        !this.onlineOnly
      )
    },

    // ==========================================
    // 🏦 BANK
    // ==========================================
    updateBank(event) {

      this.$emit(
        "update:bankFilter",
        event.target.value
      )
    },

    // ==========================================
    // 📊 SORT
    // ==========================================
    updateSort(event) {

      this.$emit(
        "update:sortType",
        event.target.value
      )
    },
  },
}
</script>

<template>

<div class="filters">

  <!-- ===================================== -->
  <!-- 💣 CATEGORY -->
  <!-- ===================================== -->

  <div class="filter-group category-group">

    <button
      :class="[
        'pill',
        {
          active: filterType === 'all'
        }
      ]"
      @click="setFilter('all')"
    >
      🔥 Все
    </button>

    <button
      :class="[
        'pill',
        {
          active: filterType === 'loan'
        }
      ]"
      @click="setFilter('loan')"
    >
      💳 Кредиты
    </button>

    <button
      :class="[
        'pill',
        {
          active: filterType === 'micro'
        }
      ]"
      @click="setFilter('micro')"
    >
      💸 Микрозаймы
    </button>

    <button
      :class="[
        'pill',
        {
          active: filterType === 'mortgage'
        }
      ]"
      @click="setFilter('mortgage')"
    >
      🏠 Ипотека
    </button>

    <button
      :class="[
        'pill',
        {
          active: filterType === 'auto'
        }
      ]"
      @click="setFilter('auto')"
    >
      🚗 Автокредиты
    </button>

    <button
      :class="[
        'pill',
        {
          active: filterType === 'education'
        }
      ]"
      @click="setFilter('education')"
    >
      🎓 Образование
    </button>

    <button
      :class="[
        'pill',
        {
          active: filterType === 'green'
        }
      ]"
      @click="setFilter('green')"
    >
      🌱 Green
    </button>

    <button
      :class="[
        'pill',
        {
          active: filterType === 'overdraft'
        }
      ]"
      @click="setFilter('overdraft')"
    >
      💰 Овердрафт
    </button>

  </div>

  <!-- ===================================== -->
  <!-- 💣 EXTRA -->
  <!-- ===================================== -->

  <div class="bottom-row">

    <!-- =================================== -->
    <!-- ⚡ ONLINE -->
    <!-- =================================== -->

    <div class="filter-group">

      <button
        :class="[
          'pill',
          'online-pill',
          {
            active: onlineOnly
          }
        ]"
        @click="toggleOnline"
      >
        ⚡ Только онлайн
      </button>

    </div>

    <!-- =================================== -->
    <!-- 🏦 BANK -->
    <!-- =================================== -->

    <div class="filter-group">

      <select
        :value="bankFilter"
        class="sort-select"
        @change="updateBank"
      >

        <option value="all">
          🏦 Все банки
        </option>

        <option
          v-for="bank in availableBanks"
          :key="bank"
          :value="bank"
        >
          {{ bank }}
        </option>

      </select>

    </div>

    <!-- =================================== -->
    <!-- 📊 SORT -->
    <!-- =================================== -->

    <div class="filter-group sort-wrapper">

      <select
        :value="sortType"
        class="sort-select"
        @change="updateSort"
      >

        <option value="match">
          🔥 Лучшее совпадение
        </option>

        <option value="rate">
          📉 Минимальная ставка
        </option>

        <option value="approval">
          ✅ Шанс одобрения
        </option>

        <option value="limit">
          💰 Максимальная сумма
        </option>

      </select>

    </div>

  </div>

</div>

</template>

<style scoped>

.filters{

  display:flex;

  flex-direction:column;

  gap:20px;

  margin-bottom:34px;
}


/* ==========================================
💣 GROUPS
========================================== */

.filter-group{

  display:flex;

  gap:12px;

  flex-wrap:wrap;
}

.category-group{

  overflow-x:auto;

  scrollbar-width:none;

  padding-bottom:4px;
}

.category-group::-webkit-scrollbar{
display:none;
}


/* ==========================================
💣 BOTTOM
========================================== */

.bottom-row{

  display:flex;

  justify-content:space-between;

  align-items:center;

  gap:20px;

  flex-wrap:wrap;
}


/* ==========================================
💣 PILLS
========================================== */

.pill{

  border:none;

  background:#f8fafc;

  padding:12px 18px;

  border-radius:999px;

  cursor:pointer;

  font-weight:700;

  font-size:14px;

  color:#334155;

  transition:.25s ease;

  white-space:nowrap;

  border:1px solid #e2e8f0;
}

.pill:hover{

  background:#eff6ff;

  border-color:#bfdbfe;

  transform:translateY(-1px);
}

.pill.active{

  background:
    linear-gradient(
      135deg,
      #2563eb,
      #1d4ed8
    );

  color:white;

  border-color:transparent;

  box-shadow:
    0 8px 20px rgba(37,99,235,.22);
}


/* ==========================================
💣 ONLINE
========================================== */

.online-pill{

  background:#ecfeff;

  color:#0f766e;

  border-color:#a5f3fc;
}

.online-pill.active{

  background:
    linear-gradient(
      135deg,
      #06b6d4,
      #0891b2
    );

  color:white;
}


/* ==========================================
💣 SORT
========================================== */

.sort-wrapper{

  margin-left:auto;
}

.sort-select{

  min-width:260px;

  padding:13px 16px;

  border-radius:18px;

  border:1px solid #cbd5e1;

  background:white;

  font-weight:700;

  font-size:14px;

  color:#0f172a;

  outline:none;

  transition:.2s ease;

  cursor:pointer;
}

.sort-select:focus{

  border-color:#2563eb;

  box-shadow:
    0 0 0 4px rgba(37,99,235,.12);
}


/* ==========================================
💣 MOBILE
========================================== */

@media(max-width:900px){

  .bottom-row{

    flex-direction:column;

    align-items:stretch;
  }

  .sort-wrapper{

    width:100%;

    margin-left:0;
  }

  .sort-select{

    width:100%;
  }

  .category-group{

    flex-wrap:nowrap;
  }
}

</style>