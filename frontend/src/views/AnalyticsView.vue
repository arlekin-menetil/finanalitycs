<script setup>

import { ref, computed, onMounted } from "vue"
import { useI18n } from "vue-i18n"
import api from "@/api/axios"

import { Bar, Doughnut, Line } from "vue-chartjs"
import "chart.js/auto"

const { t } = useI18n()

// ==========================================
// ⚙️ STATE
// ==========================================

const loading = ref(true)
const error = ref(null)

const banks = ref([])
const mobileData = ref([])

const selectedBank = ref(null)


// ==========================================
// 🚀 LOAD DATA
// ==========================================

onMounted(async () => {
  try {
    loading.value = true
    error.value = null

    const [productsRes, mobileRes] = await Promise.all([
      api.get("/banks/products/"),
      api.get("/banks/mobile-analytics/")
    ])

    banks.value = productsRes.data || []
    mobileData.value = mobileRes.data?.banks || []

  } catch (e) {
    console.error("Analytics API error:", e)
    error.value = "Ошибка загрузки аналитики"
  } finally {
    loading.value = false
  }
})


// ==========================================
// 🧠 FILTER
// ==========================================

const filteredBanks = computed(() => {
  if (!selectedBank.value) return banks.value
  return banks.value.filter(b => b.bank_name === selectedBank.value)
})


// ==========================================
// 🏆 FEATURED
// ==========================================

const featuredBanks = computed(() => {
  return banks.value
    .filter(b => b.priority_weight > 1)
    .map(b => b.bank_name)
})


// ==========================================
// 📊 KPI
// ==========================================

const avgInterest = computed(() => {
  if (!filteredBanks.value.length) return 0
  const sum = filteredBanks.value.reduce((a,b)=>a+(b.interest_rate||0),0)
  return (sum / filteredBanks.value.length).toFixed(2)
})

const avgApproval = computed(() => {
  if (!filteredBanks.value.length) return 0
  const sum = filteredBanks.value.reduce((a,b)=>a+(b.approval_probability||0),0)
  return (sum / filteredBanks.value.length).toFixed(1)
})

const bestBank = computed(() => {
  if (!filteredBanks.value.length) return "—"
  return filteredBanks.value.sort((a,b)=>
    (b.ranking_score||0)-(a.ranking_score||0)
  )[0]?.bank_name || "—"
})

const totalLoanVolume = computed(() => {
  return filteredBanks.value.reduce((a,b)=>a+(b.max_amount||0),0)
})


// ==========================================
// 🧰 HELPERS
// ==========================================

const formatMillions = (v)=> v ? (v/1000000).toFixed(0) : 0

const labels = computed(() =>
  filteredBanks.value.map(b => b.bank_name || "—")
)


// ==========================================
// 📈 CHARTS
// ==========================================

const interestData = computed(() => ({
  labels: labels.value,
  datasets:[{
    label: t("analytics.interestRates"),
    data: filteredBanks.value.map(b => b.interest_rate || 0),
  }]
}))

const loanData = computed(() => ({
  labels: labels.value,
  datasets:[{
    label: t("analytics.loanLimits"),
    data: filteredBanks.value.map(b =>
      formatMillions(b.max_amount || b.loan_limit_hint)
    ),
  }]
}))

const scoreData = computed(() => ({
  labels: labels.value,
  datasets:[{
    label: t("analytics.rankingScores"),
    data: filteredBanks.value.map(b => b.ranking_score || 0),
    tension:0.35,
    fill:true
  }]
}))

const approvalData = computed(() => {

  let high=0, medium=0, low=0

  filteredBanks.value.forEach(b => {
    const p = b.approval_probability || 0

    if (p > 70) high++
    else if (p > 40) medium++
    else low++
  })

  return {
    labels:[
      t("analytics.high"),
      t("analytics.medium"),
      t("analytics.low")
    ],
    datasets:[{
      data:[high,medium,low]
    }]
  }
})


// ==========================================
// 📱 MOBILE ANALYTICS
// ==========================================

const installsData = computed(() => ({
  labels: mobileData.value.map(b => b.bank || "—"),
  datasets:[{
    label: t("analytics.mobileDownloads"),
    data: mobileData.value.map(b => b.installs_value || 0),
  }]
}))

const ratingData = computed(() => ({
  labels: mobileData.value.map(b => b.bank || "—"),
  datasets:[{
    label: t("analytics.mobileRatings"),
    data: mobileData.value.map(b => b.rating || 0),
    tension:0.35,
    fill:true
  }]
}))


// ==========================================
// ⚙️ OPTIONS
// ==========================================

const chartOptions = {
  responsive:true,
  maintainAspectRatio:false,
  plugins:{
    legend:{position:"top"}
  },
  scales:{
    y:{beginAtZero:true}
  }
}

</script>


<template>

<section class="analytics">

<h1>{{ t("analytics.title") }}</h1>

<!-- LOADING -->
<div v-if="loading" class="loading">
⏳ {{ t("analytics.loading") }}
</div>

<!-- ERROR -->
<div v-else-if="error" class="error">
{{ error }}
</div>

<!-- EMPTY -->
<div v-else-if="!banks.length" class="empty">
Нет данных для анализа
</div>

<!-- CONTENT -->
<div v-else>

<!-- FILTER -->
<div class="filter">
<select v-model="selectedBank">
<option :value="null">Все банки</option>

<option
v-for="b in banks"
:key="b.id"
:value="b.bank_name"
>
{{ b.bank_name }}
</option>

</select>
</div>

<!-- KPI -->
<div class="kpi-grid">

<div class="kpi">
<h4>{{ t("analytics.totalBanks") }}</h4>
<p>{{ filteredBanks.length }}</p>
</div>

<div class="kpi">
<h4>{{ t("analytics.averageInterest") }}</h4>
<p>{{ avgInterest }}%</p>
</div>

<div class="kpi">
<h4>{{ t("analytics.averageApproval") }}</h4>
<p>{{ avgApproval }}%</p>
</div>

<div class="kpi">
<h4>{{ t("analytics.bestBank") }}</h4>
<p>
{{ bestBank }}
<span
v-if="featuredBanks.includes(bestBank)"
class="featured"
>
⭐
</span>
</p>
</div>

<div class="kpi">
<h4>Общий объём кредитов</h4>
<p>{{ (totalLoanVolume / 1000000000).toFixed(1) }} млрд</p>
</div>

</div>

<!-- CHARTS -->
<div class="grid">

<div class="card">
<h3>{{ t("analytics.interestRates") }}</h3>
<div class="chart-container">
<Bar :data="interestData" :options="chartOptions"/>
</div>
</div>

<div class="card">
<h3>{{ t("analytics.approvalProbability") }}</h3>
<div class="chart-container">
<Doughnut :data="approvalData" :options="chartOptions"/>
</div>
</div>

<div class="card">
<h3>{{ t("analytics.loanLimits") }}</h3>
<div class="chart-container">
<Bar :data="loanData" :options="chartOptions"/>
</div>
</div>

<div class="card">
<h3>{{ t("analytics.rankingScores") }}</h3>
<div class="chart-container">
<Line :data="scoreData" :options="chartOptions"/>
</div>
</div>

<div class="card">
<h3>{{ t("analytics.mobileDownloads") }}</h3>
<div class="chart-container">
<Bar :data="installsData" :options="chartOptions"/>
</div>
</div>

<div class="card">
<h3>{{ t("analytics.mobileRatings") }}</h3>
<div class="chart-container">
<Line :data="ratingData" :options="chartOptions"/>
</div>
</div>

</div>

</div>

</section>

</template>


<style scoped>

.analytics{
padding:20px;
}

.loading{
padding:40px;
font-size:18px;
text-align:center;
}

.error{
color:#ef4444;
padding:20px;
text-align:center;
}

.empty{
padding:40px;
text-align:center;
}

/* KPI */

.kpi-grid{
display:grid;
grid-template-columns:repeat(auto-fit,minmax(180px,1fr));
gap:16px;
margin-bottom:20px;
}

.kpi{
background:white;
padding:20px;
border-radius:14px;
font-weight:600;
box-shadow:0 2px 6px rgba(0,0,0,0.05);
}

.featured{
margin-left:6px;
color:#f59e0b;
}

/* GRID */

.grid{
display:grid;
grid-template-columns:1fr 1fr;
gap:20px;
}

.card{
background:white;
padding:20px;
border-radius:16px;
box-shadow:0 2px 6px rgba(0,0,0,0.05);
height:420px;
display:flex;
flex-direction:column;
}

.chart-container{
flex:1;
position:relative;
}

.filter{
margin-bottom:20px;
}

select{
padding:10px;
border-radius:8px;
}

@media (max-width:900px){
.grid{
grid-template-columns:1fr;
}
}

</style>