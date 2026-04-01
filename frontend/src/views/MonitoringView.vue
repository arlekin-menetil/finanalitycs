<script setup>

import { ref, onMounted, computed } from "vue"
import { useI18n } from "vue-i18n"
import api from "@/api/axios"

import { Bar, Line } from "vue-chartjs"
import "chart.js/auto"

const { t } = useI18n()

/* ================= STATE ================= */

const loading = ref(true)
const error = ref(null)

const alerts = ref([])
const ranking = ref([])
const rates = ref([])
const forecast = ref([])
const competition = ref([])

/* ================= ALERT TRANSLATOR ================= */

function translateAlert(a){

  if(a.type){
    return `${a.bank} ${t(`alerts.${a.type}`, { value:a.value })}`
  }

  if(!a.message) return ""

  const msg = a.message.toLowerCase()

  if(msg.includes("lowered interest rate")){
    const value = a.message.match(/\d+(\.\d+)?/)
    return `${a.bank} ${t("alerts.interest_drop",{value:value?.[0]})}`
  }

  if(msg.includes("mobile installs")){
    return `${a.bank} ${t("alerts.installs_growth")}`
  }

  if(msg.includes("rating increased")){
    const value = a.message.match(/\d+(\.\d+)?/)
    return `${a.bank} ${t("alerts.rating_growth",{value:value?.[0]})}`
  }

  return a.message
}

/* ================= LOAD DATA ================= */

async function loadMonitoring() {

  try {

    loading.value = true
    error.value = null

    const [
      alertsRes,
      rankingRes,
      rateRes,
      forecastRes,
      competitionRes
    ] = await Promise.all([

      api.get("/recommendations/monitoring/alerts/"),
      api.get("/recommendations/monitoring/digital-ranking/"),
      api.get("/recommendations/monitoring/interest-monitor/"),
      api.get("/recommendations/monitoring/forecast/"),
      api.get("/recommendations/monitoring/competition-map/")

    ])

    alerts.value = alertsRes.data?.alerts || []
    ranking.value = rankingRes.data?.ranking || []
    rates.value = rateRes.data?.interest_monitor || []
    forecast.value = forecastRes.data?.forecast || []
    competition.value = competitionRes.data?.competition_map || []

  } catch (error) {

    console.error("Monitoring load error:", error)
    error.value = "Ошибка загрузки мониторинга"

  } finally {

    loading.value = false

  }

}

onMounted(loadMonitoring)

/* ================= CHART OPTIONS ================= */

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: "top" }
  },
  scales: {
    y: { beginAtZero: true }
  }
}

/* ================= DIGITAL RANKING CHART ================= */

const rankingChart = computed(() => ({

  labels: ranking.value.map(b => b.bank),

  datasets: [
    {
      label: t("analytics.rankingScores"),
      data: ranking.value.map(b => b.digital_score || 0),
    }
  ]

}))

/* ================= INTEREST RATE CHART ================= */

const interestChart = computed(() => ({

  labels: rates.value.slice(0,15).map(r => r.bank),

  datasets: [
    {
      label: t("analytics.interestRates"),
      data: rates.value.slice(0,15).map(r => r.interest_rate || 0),
    }
  ]

}))

/* ================= FORECAST CHART ================= */

const forecastChart = computed(() => ({

  labels: forecast.value.map(f => f.product),

  datasets: [

    {
      label: t("analytics.current"),
      data: forecast.value.map(f => f.current_avg || 0),
      borderColor: "#3b82f6",
      tension: 0.3
    },

    {
      label: t("analytics.forecast30"),
      data: forecast.value.map(f => f.forecast_30d || 0),
      borderColor: "#f59e0b",
      tension: 0.3
    },

    {
      label: t("analytics.forecast90"),
      data: forecast.value.map(f => f.forecast_90d || 0),
      borderColor: "#ef4444",
      tension: 0.3
    }

  ]

}))

</script>


<template>

<section class="monitoring">

<h1>{{ $t("analytics.marketMonitoring") }}</h1>

<!-- LOADING -->
<div v-if="loading" class="loading">
{{ $t("analytics.loading") }}
</div>

<!-- ERROR -->
<div v-else-if="error" class="error">
{{ error }}
</div>

<!-- CONTENT -->
<div v-else>

<!-- ALERTS -->
<div v-if="alerts.length" class="alerts">

<div
v-for="(a,index) in alerts"
:key="index"
class="alert"
:class="a.severity"
>

<strong>{{ a.bank }}</strong>
<p>{{ translateAlert(a) }}</p>

</div>

</div>

<!-- EMPTY -->
<div v-if="!alerts.length && !ranking.length && !rates.length" class="empty">
Нет данных мониторинга
</div>

<!-- GRID -->
<div v-else class="grid">

<!-- DIGITAL RANKING -->
<div class="card">

<h3>{{ $t("analytics.digitalRanking") }}</h3>

<div class="chart">
<Bar :data="rankingChart" :options="chartOptions"/>
</div>

</div>

<!-- INTEREST MONITOR -->
<div class="card">

<h3>{{ $t("analytics.interestMonitor") }}</h3>

<div class="chart">
<Bar :data="interestChart" :options="chartOptions"/>
</div>

</div>

<!-- FORECAST -->
<div class="card wide">

<h3>{{ $t("analytics.marketForecast") }}</h3>

<div class="chart">
<Line :data="forecastChart" :options="chartOptions"/>
</div>

</div>

</div>

</div>

</section>

</template>


<style scoped>

.monitoring{
padding:20px;
}

.loading{
padding:40px;
font-size:18px;
}

.error{
padding:40px;
color:#ef4444;
font-size:16px;
text-align:center;
}

.empty{
padding:40px;
text-align:center;
color:#6b7280;
}

/* ALERTS */

.alerts{
display:flex;
flex-wrap:wrap;
gap:12px;
margin-bottom:20px;
}

.alert{
padding:12px 16px;
border-radius:10px;
color:white;
font-size:14px;
}

.alert.low{
background:#3b82f6;
}

.alert.medium{
background:#f59e0b;
}

.alert.high{
background:#ef4444;
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
box-shadow:0 2px 8px rgba(0,0,0,0.06);
}

.card.wide{
grid-column:span 2;
}

.chart{
height:360px;
}

@media (max-width:900px){

.grid{
grid-template-columns:1fr;
}

.card.wide{
grid-column:span 1;
}

}

</style>