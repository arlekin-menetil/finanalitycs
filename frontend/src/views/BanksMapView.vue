<script setup>

import {
  ref,
  computed,
  onMounted,
} from "vue"

import { useRouter } from "vue-router"

import { useI18n } from "vue-i18n"

import api from "@/api/axios"

import BankMap from "@/components/banks/BankMap.vue"


// ==========================================
// 🔥 ROUTER / I18N
// ==========================================
const router = useRouter()

const { t } = useI18n()


// ==========================================
// 🔥 STATE
// ==========================================
const branches = ref([])

const loading = ref(true)

const error = ref(false)

const selectedBank = ref("")

const search = ref("")

const selectedBranchId = ref(null)


// ==========================================
// 🔥 STATS
// ==========================================
const totalBranches = computed(() => {

  return branches.value.length
})


const totalBanks = computed(() => {

  const unique = new Set()

  branches.value.forEach(branch => {

    const name =
      branch.bank_name
      || branch.bank
      || ""

    if (name) {
      unique.add(name)
    }
  })

  return unique.size
})


// ==========================================
// 🔥 BANKS LIST
// ==========================================
const banks = computed(() => {

  const unique = new Set()

  branches.value.forEach(branch => {

    const name =
      branch.bank_name
      || branch.bank

    if (name) {
      unique.add(name)
    }
  })

  return Array.from(unique)
    .sort((a, b) => a.localeCompare(b))
})


// ==========================================
// 🔥 FILTERED BRANCHES
// ==========================================
const filteredBranches = computed(() => {

  // 💣 SAFE ARRAY
  let items = Array.isArray(branches.value)
    ? [...branches.value]
    : []

  // ==========================================
  // 🔥 BANK FILTER
  // ==========================================
  if (selectedBank.value) {

    items = items.filter(branch => {

      const name =
        branch.bank_name
        || branch.bank
        || ""

      return (
        name === selectedBank.value
      )
    })
  }

  // ==========================================
  // 🔥 SEARCH
  // ==========================================
  if (search.value.trim()) {

    const q = search.value
      .toLowerCase()
      .trim()

    items = items.filter(branch => {

      return (

        String(
          branch.address || ""
        )
          .toLowerCase()
          .includes(q)

        ||

        String(
          branch.city || ""
        )
          .toLowerCase()
          .includes(q)

        ||

        String(
          branch.bank_name
          || branch.bank
          || ""
        )
          .toLowerCase()
          .includes(q)
      )
    })
  }

  return items
})


// ==========================================
// 🔥 LOAD DATA
// ==========================================
onMounted(async () => {

  await loadBranches()
})


// ==========================================
// 🔥 LOAD BRANCHES
// ==========================================
async function loadBranches(){

  loading.value = true

  error.value = false

  try {

    const res = await api.get(
      "/banks/branches/"
    )

    // ==========================================
    // 🔥 SAFE RESPONSE
    // ==========================================
    let items = []

    if (
      Array.isArray(res.data)
    ) {

      items = res.data

    } else {

      items =
        res.data?.results
        || []
    }

    // ==========================================
    // 🔥 NORMALIZE
    // ==========================================
    branches.value = items.map(
      (item, index) => ({

        id:
          item.id
          || index,

        bank_id:
          item.bank_id
          || null,

        bank_name:
          item.bank_name
          || item.bank
          || "Банк",

        bank:
          item.bank
          || item.bank_name
          || "Банк",

        name:
          item.name
          || null,

        city:
          item.city
          || null,

        address:
          item.address
          || null,

        phone:
          item.phone
          || null,

        working_hours:
          item.working_hours
          || null,

        latitude:
          Number(
            item.latitude
            || item.lat
          ),

        longitude:
          Number(
            item.longitude
            || item.lng
          ),

        lat:
          Number(
            item.lat
            || item.latitude
          ),

        lng:
          Number(
            item.lng
            || item.longitude
          ),
      })
    )

    // ==========================================
    // 🔥 DEBUG
    // ==========================================
    console.log(
      "🗺 BRANCHES:",
      branches.value.length
    )

    console.log(
      "🗺 SAMPLE:",
      branches.value[0]
    )

  } catch (e) {

    console.error(
      "Map load error:",
      e
    )

    error.value = true

  } finally {

    loading.value = false
  }
}


// ==========================================
// 🔥 ACTIONS
// ==========================================
function goToRecommendations(){

  router.push(
    "/app/recommendations"
  )
}


function goToAnalytics(){

  router.push(
    "/app/analytics"
  )
}


// ==========================================
// 🔥 RESET FILTERS
// ==========================================
function resetFilters(){

  selectedBank.value = ""

  search.value = ""
}


// ==========================================
// 🔥 OPEN BRANCH
// ==========================================
function focusBranch(branch){

  selectedBranchId.value =
    branch.id
}


// ==========================================
// 🔥 FORMATTERS
// ==========================================
function getBankName(branch){

  return (
    branch.bank_name
    || branch.bank
    || "Банк"
  )
}


function getBranchAddress(branch){

  return (
    branch.address
    || "Адрес не указан"
  )
}


function getBranchCity(branch){

  return (
    branch.city
    || "Город не указан"
  )
}

</script>


<template>

<div class="page">

  <!-- ==========================================
  🔥 HEADER
  =========================================== -->
  <div class="hero">

    <div class="hero-top">

      <div>

        <h1>
          🗺
          {{
            t("map.title")
            || "Карта банков"
          }}
        </h1>

        <p class="subtitle">

          {{
            t("map.subtitle")
            || "Найдите ближайшие филиалы и выберите лучший банковский продукт"
          }}

        </p>

      </div>

      <!-- STATS -->
      <div class="stats">

        <div class="stat-card">

          <div class="stat-value">
            {{ totalBranches }}
          </div>

          <div class="stat-label">
            Филиалов
          </div>

        </div>

        <div class="stat-card">

          <div class="stat-value">
            {{ totalBanks }}
          </div>

          <div class="stat-label">
            Банков
          </div>

        </div>

      </div>

    </div>

    <!-- ACTIONS -->
    <div class="actions">

      <button
        class="primary"
        @click="goToRecommendations"
      >
        🔥
        {{
          t("map.findBest")
          || "Лучшие предложения"
        }}
      </button>

      <button
        class="secondary"
        @click="goToAnalytics"
      >
        📊
        {{
          t("map.analytics")
          || "Аналитика"
        }}
      </button>

    </div>

  </div>


  <!-- ==========================================
  🔥 FILTERS
  =========================================== -->
  <div class="filters">

    <input
      v-model="search"
      type="text"
      placeholder="Поиск по адресу, городу или банку..."
      class="search-input"
    />

    <select
      v-model="selectedBank"
      class="bank-select"
    >

      <option value="">
        Все банки
      </option>

      <option
        v-for="bank in banks"
        :key="bank"
        :value="bank"
      >
        {{ bank }}
      </option>

    </select>

    <button
      class="reset-btn"
      @click="resetFilters"
    >
      Сбросить
    </button>

  </div>


  <!-- ==========================================
  🔥 STATES
  =========================================== -->
  <div
    v-if="loading"
    class="state"
  >
    Загрузка карты...
  </div>

  <div
    v-else-if="error"
    class="state error"
  >
    Ошибка загрузки карты
  </div>


  <!-- ==========================================
  🔥 CONTENT
  =========================================== -->
  <div
    v-else
    class="content-grid"
  >

    <!-- ==========================================
    🔥 SIDEBAR
    =========================================== -->
    <div class="sidebar">

      <div class="sidebar-header">

        <h3>
          Филиалы
        </h3>

        <span>
          {{ filteredBranches.length }}
        </span>

      </div>

      <div class="branch-list">

        <button
          v-for="branch in filteredBranches"
          :key="branch.id"
          class="branch-card"
          @click="focusBranch(branch)"
        >

          <div class="branch-bank">
            🏦
            {{ getBankName(branch) }}
          </div>

          <div class="branch-city">
            📍
            {{ getBranchCity(branch) }}
          </div>

          <div class="branch-address">
            {{ getBranchAddress(branch) }}
          </div>

          <div
            v-if="branch.phone"
            class="branch-phone"
          >
            ☎ {{ branch.phone }}
          </div>

        </button>

      </div>

    </div>


    <!-- ==========================================
    🔥 MAP
    =========================================== -->
    <div class="map-container">

      <BankMap
        :points="filteredBranches"
        :selectedBranchId="selectedBranchId"
        height="760px"
      />

    </div>

  </div>

</div>

</template>


<style scoped>

/* ==========================================
🔥 PAGE
========================================== */

.page{

  max-width:1600px;

  margin:auto;

  padding:40px;
}


/* ==========================================
🔥 HERO
========================================== */

.hero{

  margin-bottom:24px;
}

.hero-top{

  display:flex;

  justify-content:space-between;

  gap:20px;

  align-items:flex-start;

  margin-bottom:20px;
}

h1{

  font-size:38px;

  line-height:1.1;

  margin-bottom:10px;

  font-weight:800;

  color:#111827;
}

.subtitle{

  color:#6b7280;

  font-size:15px;

  max-width:700px;

  line-height:1.6;
}


/* ==========================================
🔥 STATS
========================================== */

.stats{

  display:flex;

  gap:14px;
}

.stat-card{

  background:white;

  border:1px solid #e5e7eb;

  border-radius:18px;

  padding:18px 22px;

  min-width:120px;

  box-shadow:
    0 8px 24px rgba(0,0,0,0.05);
}

.stat-value{

  font-size:26px;

  font-weight:800;

  color:#111827;

  margin-bottom:6px;
}

.stat-label{

  font-size:13px;

  color:#6b7280;
}


/* ==========================================
🔥 ACTIONS
========================================== */

.actions{

  display:flex;

  gap:12px;

  flex-wrap:wrap;
}

.primary{

  background:#2563eb;

  color:white;

  border:none;

  border-radius:12px;

  padding:12px 18px;

  cursor:pointer;

  font-weight:600;

  transition:all .2s ease;
}

.primary:hover{

  background:#1d4ed8;
}

.secondary{

  background:white;

  border:1px solid #d1d5db;

  border-radius:12px;

  padding:12px 18px;

  cursor:pointer;

  font-weight:600;

  transition:all .2s ease;
}

.secondary:hover{

  background:#f9fafb;
}


/* ==========================================
🔥 FILTERS
========================================== */

.filters{

  display:flex;

  gap:12px;

  margin-bottom:24px;

  flex-wrap:wrap;
}

.search-input{

  flex:1;

  min-width:260px;

  background:white;

  border:1px solid #d1d5db;

  border-radius:14px;

  padding:13px 16px;

  outline:none;

  font-size:14px;
}

.search-input:focus{

  border-color:#2563eb;
}

.bank-select{

  min-width:220px;

  background:white;

  border:1px solid #d1d5db;

  border-radius:14px;

  padding:13px 16px;

  outline:none;

  font-size:14px;
}

.reset-btn{

  border:none;

  background:#ef4444;

  color:white;

  border-radius:14px;

  padding:13px 18px;

  cursor:pointer;

  font-weight:600;
}


/* ==========================================
🔥 CONTENT GRID
========================================== */

.content-grid{

  display:grid;

  grid-template-columns:
    360px
    1fr;

  gap:20px;

  align-items:start;
}


/* ==========================================
🔥 SIDEBAR
========================================== */

.sidebar{

  background:white;

  border:1px solid #e5e7eb;

  border-radius:22px;

  overflow:hidden;

  height:760px;

  display:flex;

  flex-direction:column;

  box-shadow:
    0 10px 30px rgba(0,0,0,0.05);
}

.sidebar-header{

  padding:20px;

  border-bottom:1px solid #f3f4f6;

  display:flex;

  justify-content:space-between;

  align-items:center;

  font-weight:700;
}

.branch-list{

  overflow:auto;

  flex:1;

  padding:14px;
}


/* ==========================================
🔥 BRANCH CARD
========================================== */

.branch-card{

  width:100%;

  text-align:left;

  border:none;

  background:#fff;

  border-radius:18px;

  padding:16px;

  margin-bottom:12px;

  cursor:pointer;

  transition:all .2s ease;

  border:1px solid #eef2f7;
}

.branch-card:hover{

  transform:translateY(-2px);

  border-color:#bfdbfe;

  box-shadow:
    0 10px 20px rgba(37,99,235,0.08);
}

.branch-bank{

  font-size:15px;

  font-weight:700;

  color:#111827;

  margin-bottom:8px;
}

.branch-city{

  color:#2563eb;

  font-size:13px;

  margin-bottom:8px;
}

.branch-address{

  font-size:13px;

  line-height:1.5;

  color:#4b5563;

  margin-bottom:8px;
}

.branch-phone{

  font-size:12px;

  color:#6b7280;
}


/* ==========================================
🔥 MAP
========================================== */

.map-container{

  min-width:0;

  height:760px;

  border-radius:22px;

  overflow:hidden;

  background:white;

  border:1px solid #e5e7eb;

  box-shadow:
    0 10px 30px rgba(0,0,0,0.05);
}


/* ==========================================
🔥 STATES
========================================== */

.state{

  text-align:center;

  padding:60px;

  font-size:15px;
}

.error{

  color:#ef4444;
}


/* ==========================================
🔥 MOBILE
========================================== */

@media (max-width:1100px){

  .content-grid{

    grid-template-columns:1fr;
  }

  .sidebar{

    height:420px;
  }

  .map-container{

    height:600px;
  }
}

@media (max-width:768px){

  .page{

    padding:20px;
  }

  .hero-top{

    flex-direction:column;
  }

  h1{

    font-size:28px;
  }

  .stats{

    width:100%;
  }

  .stat-card{

    flex:1;
  }

  .filters{

    flex-direction:column;
  }

  .search-input,
  .bank-select,
  .reset-btn{

    width:100%;
  }

  .sidebar{

    height:360px;
  }

  .map-container{

    height:500px;
  }
}

</style>