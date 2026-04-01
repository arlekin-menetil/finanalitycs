<script setup>

import { ref, onMounted, computed } from "vue"
import { useI18n } from "vue-i18n"
import { useRecommendationsStore } from "@/stores/recommendations"
import { useScoringStore } from "@/stores/scoring"
import { useAuthStore } from "@/stores/auth"

import "chart.js/auto"
import { Bar, Line, Doughnut } from "vue-chartjs"

const { t } = useI18n()

const recommendationsStore = useRecommendationsStore()
const scoringStore = useScoringStore()
const auth = useAuthStore()

const loading = ref(true)
const error = ref(false)

// ==========================================
// 🚀 LOAD
// ==========================================
onMounted(async () => {
  try {

    await scoringStore.calculate()
    await recommendationsStore.loadRecommendations(5)

  } catch (e) {

    error.value = true
    console.error(e)

  } finally {

    loading.value = false

  }
})

// ==========================================
// 🧠 SCORING
// ==========================================

const creditScore = computed(() => scoringStore.creditScore)

const approvalPercent = computed(() =>
  Math.round(scoringStore.approvalProbability * 100)
)

const riskKey = computed(() =>
  scoringStore.riskCategory?.toLowerCase() || ""
)

const riskLabel = computed(() =>
  riskKey.value
    ? t(`dashboard.riskLevels.${riskKey.value}`)
    : "—"
)

const riskClass = computed(() => {
  switch (riskKey.value) {
    case "low": return "green"
    case "medium": return "orange"
    case "high": return "red"
    default: return ""
  }
})

// ==========================================
// 💣 PROFILE DATA
// ==========================================

const monthlyIncome = computed(() =>
  auth.profile?.income || 0
)

const monthlyObligations = computed(() =>
  auth.profile?.obligations || 0
)

const dtiRatio = computed(() =>
  monthlyIncome.value
    ? +(monthlyObligations.value / monthlyIncome.value).toFixed(2)
    : 0
)

// ==========================================
// 💰 FORMAT
// ==========================================

function formatMoney(v) {
  return new Intl.NumberFormat("ru-RU").format(v) + " UZS"
}

// ==========================================
// 💣 APPLY
// ==========================================

async function apply(bank) {

  try {

    await recommendationsStore.click(
      bank.product_id,
      bank.ranking_score
    )

    await recommendationsStore.apply(bank.product_id)

    if (bank.website) {
      window.open(bank.website, "_blank")
    }

  } catch (e) {

    console.error("Apply error:", e)

  }

}

// ==========================================
// 📊 CHARTS
// ==========================================

const barData = computed(() => ({
  labels: [t("dashboard.income"), t("dashboard.obligations")],
  datasets: [{
    data: [monthlyIncome.value, monthlyObligations.value],
    backgroundColor: ["#16a34a", "#ef4444"],
    borderRadius: 12,
    borderSkipped: false,
    maxBarThickness: 60
  }]
}))

const barOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } }
}

const lineData = {
  labels: ["Jan","Feb","Mar","Apr","May"],
  datasets: [{
    data: [15,22,28,24,29],
    borderColor: "#2563eb",
    backgroundColor: "rgba(37,99,235,0.12)",
    fill: true,
    tension: 0.4,
    borderWidth: 3,
    pointRadius: 4
  }]
}

const lineOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } }
}

const donutData = computed(() => ({
  labels: [t("dashboard.obligations"), t("dashboard.available")],
  datasets: [{
    data: [
      monthlyObligations.value,
      Math.max(0, monthlyIncome.value - monthlyObligations.value)
    ],
    backgroundColor: ["#ef4444", "#e5e7eb"],
    borderWidth: 0,
    cutout: "70%"
  }]
}))

const donutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } }
}

</script>

<template>

<div class="dashboard">
<div class="page">

<!-- LOADING -->
<div v-if="loading" class="state">
{{ t("dashboard.loading") }}
</div>

<!-- ERROR -->
<div v-else-if="error" class="state error">
{{ t("dashboard.error") }}
</div>

<!-- CONTENT -->
<div v-else>

<div class="main-status">

<div>
<h1 :class="riskClass">{{ riskLabel }}</h1>
<p>{{ t("dashboard.approval") }}:
<strong>{{ approvalPercent }}%</strong></p>
</div>

<div class="score-box">
<span>{{ t("dashboard.score") }}</span>
<h2>{{ creditScore }}</h2>
</div>

</div>

<div class="card top-banks">

<div class="card-title">
{{ t("dashboard.topBanks") }}
</div>

<div v-if="recommendationsStore.loading" class="mini-state">
{{ t("dashboard.loadingRecommendations") }}
</div>

<div v-else-if="recommendationsStore.recommendations?.length" class="bank-list">

<div
v-for="(bank, index) in recommendationsStore.recommendations"
:key="bank.product_id"
class="bank-card"
>

<div class="bank-left">

<div class="bank-rank">
#{{ index + 1 }}
</div>

<div class="bank-logo">
{{ bank.bank_name?.charAt(0) || "B" }}
</div>

<div class="bank-info">

<div class="bank-name">
{{ bank.bank_name }}
</div>

<div class="bank-product">
{{ bank.product_name }}
</div>

<div v-if="index === 0" class="best-badge">
{{ t("dashboard.bestMatch") }}
</div>

</div>

</div>

<div class="bank-middle">

<div class="rate-box">

<div class="rate-label">
{{ t("dashboard.rate") }}
</div>

<div class="rate-value">
{{ bank.interest_rate ?? "-" }}%
</div>

</div>

<div class="match-box">

<div class="match-label">
{{ t("dashboard.match") }} {{ Math.round(bank.ranking_score) }}%
</div>

<div class="match-bar">

<div
class="match-fill"
:style="{ width: Math.round(bank.ranking_score) + '%' }"
></div>

</div>

</div>

</div>

<div class="bank-right">

<button
class="apply-btn"
@click="apply(bank)"
>
{{ t("dashboard.apply") }}
</button>

</div>

</div>

</div>

<div v-else class="mini-state">
{{ t("dashboard.noRecommendations") }}
</div>

</div>

<div class="grid">

<div class="card span-4 center">

<div class="card-title">
{{ t("dashboard.debtLoad") }}
</div>

<div class="donut-wrapper">

<Doughnut
:data="donutData"
:options="donutOptions"
/>

<div class="donut-center">
{{ dtiRatio * 100 }}%
</div>

</div>

</div>

<div class="card span-4">

<div class="card-title">
{{ t("dashboard.income") }}
</div>

<h3 class="green">
{{ formatMoney(monthlyIncome) }}
</h3>

</div>

<div class="card span-4">

<div class="card-title">
{{ t("dashboard.obligations") }}
</div>

<h3 class="red">
{{ formatMoney(monthlyObligations) }}
</h3>

</div>

<div class="card span-8">

<div class="card-title">
{{ t("dashboard.incomeVsObligations") }}
</div>

<Bar
:data="barData"
:options="barOptions"
/>

</div>

<div class="card span-4">

<div class="card-title">
{{ t("dashboard.trend") }}
</div>

<Line
:data="lineData"
:options="lineOptions"
/>

</div>

</div>

</div>
</div>
</div>

</template>

<style scoped>

.dashboard{
height:100%;
}

.page{
max-width:1200px;
margin:0 auto;
padding:20px;
}

.state{
padding:40px;
text-align:center;
color:#6b7280;
}

.error{
color:#ef4444;
}

.main-status{
display:flex;
justify-content:space-between;
align-items:center;
margin-bottom:24px;
padding:24px;
background:#ffffff;
border-radius:20px;
border:1px solid #eef1f6;
flex-wrap:wrap;
gap:20px;
}

.score-box span{
font-size:11px;
text-transform:uppercase;
color:#9ca3af;
}

.score-box h2{
margin-top:6px;
font-size:32px;
}

.top-banks{
margin-bottom:24px;
}

.bank-list{
display:flex;
flex-direction:column;
gap:14px;
}

.bank-card{
display:flex;
justify-content:space-between;
align-items:center;
padding:18px;
border-radius:16px;
background:#f9fafb;
transition:0.2s;
flex-wrap:wrap;
gap:20px;
}

.bank-card:hover{
background:#eef2ff;
}

.bank-left{
display:flex;
align-items:center;
gap:16px;
}

.bank-rank{
font-weight:700;
font-size:18px;
width:30px;
}

.bank-logo{
width:42px;
height:42px;
border-radius:10px;
background:#2563eb;
color:white;
display:flex;
align-items:center;
justify-content:center;
font-weight:700;
}

.bank-name{
font-weight:600;
}

.bank-product{
font-size:12px;
color:#6b7280;
}

.best-badge{
margin-top:4px;
font-size:11px;
background:#16a34a;
color:white;
padding:2px 6px;
border-radius:6px;
display:inline-block;
}

.bank-middle{
width:250px;
}

.rate-label{
font-size:11px;
color:#6b7280;
}

.rate-value{
font-size:18px;
font-weight:700;
}

.match-label{
font-size:12px;
margin-top:6px;
}

.match-bar{
height:6px;
background:#e5e7eb;
border-radius:4px;
margin-top:4px;
}

.match-fill{
height:6px;
background:#2563eb;
border-radius:4px;
}

.apply-btn{
background:#2563eb;
color:white;
border:none;
padding:10px 18px;
border-radius:10px;
cursor:pointer;
font-weight:500;
}

.apply-btn:hover{
background:#1e40af;
}

.grid{
display:grid;
grid-template-columns:repeat(12,1fr);
grid-auto-rows:260px;
gap:20px;
}

.span-8{
grid-column:span 8;
}

.span-4{
grid-column:span 4;
}

.card{
background:#ffffff;
border-radius:20px;
padding:20px;
border:1px solid #eef1f6;
display:flex;
flex-direction:column;
box-shadow:0 4px 14px rgba(16,24,40,0.04);
}

.donut-wrapper{
position:relative;
width:180px;
height:180px;
margin:0 auto;
padding-top:15px;
}

.donut-wrapper canvas{
width:100%!important;
height:100%!important;
}

.donut-center{
position:absolute;
top:50%;
left:50%;
transform:translate(-50%,-50%);
font-weight:600;
font-size:18px;
}

.green{color:#16a34a}
.orange{color:#f59e0b}
.red{color:#ef4444}

/* ===================== */
/* TABLET */
/* ===================== */

@media (max-width:1024px){

.grid{
grid-template-columns:repeat(6,1fr);
}

.span-8{
grid-column:span 6;
}

.span-4{
grid-column:span 3;
}

}

/* ===================== */
/* MOBILE */
/* ===================== */

@media (max-width:768px){

.main-status{
flex-direction:column;
align-items:flex-start;
}

.bank-middle{
width:100%;
}

.grid{
grid-template-columns:1fr;
grid-auto-rows:auto;
}

.span-8,
.span-4{
grid-column:span 1;
}

.card{
min-height:220px;
}

}

</style>