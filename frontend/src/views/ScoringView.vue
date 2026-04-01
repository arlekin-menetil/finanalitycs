<script setup>

import { ref, onMounted, computed } from "vue"
import { useI18n } from "vue-i18n"
import api from "@/api/axios"
import "chart.js/auto"
import { Line } from "vue-chartjs"

const { t } = useI18n()

const loading = ref(false)
const error = ref(null)

const latest = ref(null)
const history = ref([])

const showToast = ref(false)
const toastMessage = ref("")
const toastType = ref("success")

let cooldown = false

/* ================= API ================= */

async function loadLatest() {
  try {
    const res = await api.get("/scoring/latest/")
    latest.value = res.data
  } catch (e) {
    console.error("Latest scoring error:", e)
  }
}

async function loadHistory() {
  try {
    const res = await api.get("/scoring/history/")
    history.value = res.data || []
  } catch (e) {
    console.error("History error:", e)
    history.value = []
  }
}

async function calculateScore() {

  if (loading.value || cooldown) return

  loading.value = true
  cooldown = true

  setTimeout(() => (cooldown = false), 1200)

  try {

    await api.post("/scoring/calculate/")
    await Promise.all([loadLatest(), loadHistory()])

    toastMessage.value = t("scoring.toastSuccess")
    toastType.value = "success"

  } catch {

    toastMessage.value = t("scoring.toastError")
    toastType.value = "error"

  } finally {

    showToast.value = true
    loading.value = false

    setTimeout(() => (showToast.value = false), 3000)
  }

}

onMounted(async () => {

  try {

    await Promise.all([loadLatest(), loadHistory()])

  } catch {

    error.value = "Ошибка загрузки скоринга"

  }

})

/* ================= COMPUTED ================= */

const approvalWidth = computed(() =>
  latest.value
    ? `${latest.value.approval_probability || 0}%`
    : "0%"
)

const riskColor = computed(() => {

  if (!latest.value) return "#2563eb"

  switch (latest.value.risk_category) {
    case "LOW": return "#22c55e"
    case "MEDIUM": return "#f59e0b"
    case "HIGH": return "#ef4444"
    default: return "#2563eb"
  }

})

const trendData = computed(() => ({

  labels: history.value.map(i =>
    new Date(i.created_at).toLocaleDateString()
  ),

  datasets: [
    {
      data: history.value.map(i => i.score || 0),
      borderColor: riskColor.value,
      backgroundColor: "rgba(37,99,235,0.08)",
      tension: 0.5,
      fill: true
    }
  ]

}))

const trendOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } }
}

/* ================= HELPERS ================= */

function formatDate(date) {
  return new Date(date).toLocaleDateString()
}

function formatTime(date) {
  return new Date(date).toLocaleTimeString()
}

</script>

<template>

<div class="scoring-page">

<!-- ERROR -->
<div v-if="error" class="error">
{{ error }}
</div>

<!-- HEADER -->
<div class="page-header">

<div>
<h1 class="title">{{ t("scoring.title") }}</h1>
<p class="subtitle">{{ t("scoring.subtitle") }}</p>
</div>

<button
class="primary-btn"
@click="calculateScore"
:disabled="loading"
>
<span v-if="loading" class="spinner"></span>
{{ loading ? t("scoring.processing") : t("scoring.recalc") }}
</button>

</div>

<!-- EMPTY -->
<div v-if="!latest && !loading" class="empty">
Нет данных скоринга — нажмите "Рассчитать"
</div>

<!-- KPI -->
<div v-if="latest" class="kpi-grid">

<div class="kpi-card">
<div class="kpi-label">{{ t("scoring.creditScore") }}</div>
<div class="kpi-value big">{{ latest.score }}</div>
</div>

<div class="kpi-card">
<div class="kpi-label">{{ t("scoring.riskLevel") }}</div>
<div class="kpi-value" :style="{ color: riskColor }">
{{ t(`dashboard.riskLevels.${latest.risk_category}`) }}
</div>
</div>

<div class="kpi-card">
<div class="kpi-label">{{ t("scoring.approval") }}</div>
<div class="kpi-value">
{{ latest.approval_probability || 0 }}%
</div>

<div class="progress">
<div
class="progress-bar"
:style="{ width: approvalWidth, background: riskColor }"
></div>
</div>

</div>

<div class="kpi-card">
<div class="kpi-label">{{ t("scoring.model") }}</div>
<div class="kpi-value">
v{{ latest.profile_version || 1 }}
</div>
</div>

</div>

<!-- CHART -->
<div v-if="history.length" class="chart-card">

<h2>{{ t("scoring.trend") }}</h2>

<div class="chart-container">
<Line :data="trendData" :options="trendOptions" />
</div>

</div>

<!-- HISTORY -->
<div v-if="history.length" class="table-card">

<h2>{{ t("scoring.history") }}</h2>

<div class="table-scroll">

<table>

<thead>
<tr>
<th>{{ t("scoring.date") }}</th>
<th>{{ t("scoring.time") }}</th>
<th>{{ t("scoring.score") }}</th>
<th>{{ t("scoring.approval") }}</th>
<th>{{ t("scoring.riskLevel") }}</th>
</tr>
</thead>

<tbody>

<tr v-for="item in history" :key="item.id">

<td>{{ formatDate(item.created_at) }}</td>
<td>{{ formatTime(item.created_at) }}</td>

<td class="bold">{{ item.score }}</td>

<td>{{ item.approval_probability || 0 }}%</td>

<td>
<span
class="risk-badge"
:style="{
background:
item.risk_category==='LOW' ? '#22c55e' :
item.risk_category==='MEDIUM' ? '#f59e0b' :
'#ef4444'
}"
>
{{ t(`dashboard.riskLevels.${item.risk_category}`) }}
</span>
</td>

</tr>

</tbody>

</table>

</div>

</div>

<!-- TOAST -->
<div
v-if="showToast"
class="toast"
:class="toastType"
>
{{ toastMessage }}
</div>

</div>

</template>

<style scoped>

/* ВСЕ СТИЛИ СОХРАНЕНЫ + МЕЛКИЕ УЛУЧШЕНИЯ */

.scoring-page {
max-width: 1150px;
}

/* HEADER */
.page-header {
display: flex;
justify-content: space-between;
align-items: center;
margin-bottom: 40px;
flex-wrap: wrap;
gap: 20px;
}

.title {
font-size: 28px;
font-weight: 700;
}

.subtitle {
color: #64748b;
margin-top: 6px;
}

/* BUTTON */
.primary-btn {
background: #2563eb;
color: white;
border: none;
padding: 10px 18px;
border-radius: 12px;
font-weight: 500;
cursor: pointer;
}

.primary-btn:hover {
background: #1d4ed8;
}

.primary-btn:disabled {
opacity: 0.6;
cursor: not-allowed;
}

/* KPI */
.kpi-grid {
display: grid;
grid-template-columns: repeat(4,1fr);
gap: 20px;
margin-bottom: 40px;
}

.kpi-card {
background: white;
padding: 25px;
border-radius: 18px;
box-shadow: 0 8px 25px rgba(15,23,42,0.06);
}

.kpi-label {
font-size: 13px;
color: #64748b;
margin-bottom: 10px;
}

.kpi-value.big {
font-size: 48px;
font-weight: 800;
}

/* PROGRESS */
.progress {
height: 6px;
background: #e2e8f0;
border-radius: 6px;
margin-top: 10px;
}

.progress-bar {
height: 100%;
}

/* CHART */
.chart-card {
background: white;
padding: 30px;
border-radius: 20px;
box-shadow: 0 8px 30px rgba(15,23,42,0.06);
margin-bottom: 40px;
}

.chart-container {
height: 260px;
}

/* TABLE */
.table-card {
background: white;
padding: 30px;
border-radius: 20px;
box-shadow: 0 8px 30px rgba(15,23,42,0.06);
}

.table-scroll {
max-height: 320px;
overflow-y: auto;
margin-top: 20px;
}

table {
width: 100%;
border-collapse: collapse;
}

th {
text-align: left;
font-size: 12px;
color: #64748b;
padding-bottom: 12px;
}

td {
padding: 12px 0;
border-top: 1px solid #f1f5f9;
}

.bold {
font-weight: 600;
}

.risk-badge {
color: white;
padding: 4px 10px;
border-radius: 999px;
font-size: 12px;
}

/* STATES */

.error {
padding: 40px;
color: #ef4444;
text-align: center;
}

.empty {
padding: 40px;
text-align: center;
color: #6b7280;
}

/* TOAST */
.toast {
position: fixed;
top: 25px;
right: 25px;
padding: 14px 22px;
border-radius: 14px;
color: white;
font-weight: 500;
box-shadow: 0 15px 40px rgba(0,0,0,0.15);
animation: slideIn 0.3s ease;
z-index: 9999;
}

.toast.success {
background: linear-gradient(135deg,#22c55e,#16a34a);
}

.toast.error {
background: linear-gradient(135deg,#ef4444,#dc2626);
}

@keyframes slideIn {
from { transform: translateX(40px); opacity: 0; }
to { transform: translateX(0); opacity: 1; }
}

</style>