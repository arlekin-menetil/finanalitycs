💣 ВОТ ТВОЙ ПОЛНЫЙ ОБНОВЛЁННЫЙ КОД
<script setup>
import { ref, computed, onMounted, watch } from "vue"
import { useI18n } from "vue-i18n"
import { useRouter } from "vue-router" // 🔥 ДОБАВИЛ
import Chart from "chart.js/auto"

/* 🌍 i18n */
const { t, locale } = useI18n()

/* 🔥 ROUTER */
const router = useRouter()

const goToLogin = () => {
  router.push("/login")
}

const changeLang = (l) => {
  locale.value = l
  localStorage.setItem("lang", l)
}

/* ---------------- GRAPH ---------------- */

const chartRef = ref(null)
let chart = null

const currencies = ref([
  { code: "USD", value: "12 210", change: 15 },
  { code: "RUB", value: "150", change: 0.6 },
  { code: "EUR", value: "14 036", change: -13 },
  { code: "GBP", value: "16 162", change: -66 },
  { code: "KZT", value: "25.39", change: 0.16 }
])

const activeCurrency = ref("USD")

const dataMap = {
  USD: [12100,12200,12350,12280,12400,12550,12380],
  RUB: [140,145,150,148,149,151,150],
  EUR: [13900,14000,14100,14050,14200,14300,14036],
  GBP: [16000,16100,16200,16150,16250,16300,16162],
  KZT: [24,25,26,25.5,25.7,25.9,25.39]
}

/* 🔥 LABELS */
const getChartLabels = () => [
  t("chart.mon"),
  t("chart.tue"),
  t("chart.wed"),
  t("chart.thu"),
  t("chart.fri"),
  t("chart.sat"),
  t("chart.sun")
]

const changeCurrency = (code) => {
  activeCurrency.value = code
  if (chart) {
    chart.data.datasets[0].data = dataMap[code] || dataMap["USD"]
    chart.update()
  }
}

/* ---------------- CONVERTER ---------------- */

const currencyList = ["USD","EUR","RUB","GBP","KZT","CNY","UZS"]

const amount = ref(100)
const from = ref("USD")
const to = ref("UZS")

const rates = {
  USD: 12200,
  EUR: 13200,
  RUB: 135,
  GBP: 16100,
  KZT: 25,
  CNY: 1700,
  UZS: 1
}

const converted = computed(() => {
  const inUZS = amount.value * rates[from.value]
  return Math.round(inUZS / rates[to.value])
})

const swapCurrencies = () => {
  const temp = from.value
  from.value = to.value
  to.value = temp
}

/* ---------------- INIT ---------------- */

onMounted(() => {
  chart = new Chart(chartRef.value, {
    type: "line",
    data: {
      labels: getChartLabels(),
      datasets: [{
        data: dataMap[activeCurrency.value],
        borderColor: "#2563eb",
        backgroundColor: "rgba(37,99,235,0.1)",
        fill: true,
        tension: 0.4,
        pointRadius: 3
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false } },
        y: {
          ticks: {
            callback: (val) => val.toLocaleString()
          }
        }
      }
    }
  })
})

watch(locale, () => {
  if (chart) {
    chart.data.labels = getChartLabels()
    chart.update()
  }
})
</script>

<template>
  <div class="landing">

    <!-- HEADER -->
    <header class="header">
      <div class="logo">FinAnalytics</div>

      <div class="header-right">
        <div class="langs">
          <span @click="changeLang('ru')">🇷🇺</span>
          <span @click="changeLang('en')">🇬🇧</span>
          <span @click="changeLang('uz')">🇺🇿</span>
        </div>

        <!-- 🔥 ВОТ ФИКС -->
        <button class="login" @click="goToLogin">
          {{ t("common.login") }}
        </button>
      </div>
    </header>

    <!-- HERO -->
    <section class="hero">
      <div class="hero-left">
        <h1>{{ t("hero.title") }}</h1>
        <p>{{ t("hero.subtitle") }}</p>
      </div>
    </section>

    <!-- дальше ВСЁ БЕЗ ИЗМЕНЕНИЙ -->
    <!-- я ничего не резал, не трогал -->

    <!-- STATS -->
    <section class="stats">
      <div class="stat">
        <h2>32</h2>
        <p>{{ t("stats.banks") }}</p>
      </div>
      <div class="stat">
        <h2>147</h2>
        <p>{{ t("stats.products") }}</p>
      </div>
      <div class="stat">
        <h2> 3 </h2>
        <p>{{ t("stats.speed") }}</p>
      </div>
    </section>

    <!-- DATA -->
    <section class="section">
      <h2>{{ t("data.title") }}</h2>

      <p class="section-desc">
        {{ t("data.desc") }}
      </p>

      <div class="grid">
        <div class="card">
          <h3>🏦 Bank.uz</h3>
          <p>{{ t("data.bank") }}</p>
        </div>

        <div class="card">
          <h3>💰 Deposit.uz</h3>
          <p>{{ t("data.deposit") }}</p>
        </div>

        <div class="card">
          <h3>📊 BankXizmatlari</h3>
          <p>{{ t("data.analytics") }}</p>
        </div>

        <div class="card">
          <h3>🪪 MyGov</h3>
          <p>{{ t("data.gov") }}</p>
        </div>

        <div class="card">
          <h3>📈 Infokredit</h3>
          <p>{{ t("data.credit") }}</p>
        </div>
      </div>
    </section>

    <!-- BENEFITS -->
    <section class="section">
      <h2>{{ t("benefits.title") }}</h2>

      <div class="grid">
        <div class="card">
          <h3>📊 {{ t("benefits.analytics") }}</h3>
          <p>{{ t("benefits.analyticsDesc") }}</p>
        </div>

        <div class="card">
          <h3>🤖 {{ t("benefits.ai") }}</h3>
          <p>{{ t("benefits.aiDesc") }}</p>
        </div>

        <div class="card">
          <h3>⚡ {{ t("benefits.speed") }}</h3>
          <p>{{ t("benefits.speedDesc") }}</p>
        </div>

        <div class="card">
          <h3>🔒 {{ t("benefits.security") }}</h3>
          <p>{{ t("benefits.securityDesc") }}</p>
        </div>
      </div>
    </section>

    <!-- GRAPH + CONVERTER -->
    <section class="converter-section">
      <div class="converter-wrapper">

        <div class="chart-box">
          <h2>{{ t("chart.title") }} ({{ activeCurrency }})</h2>

          <div class="chart-inner">
            <canvas ref="chartRef"></canvas>
          </div>

          <div class="currency-switch">
            <button
              v-for="c in currencies"
              :key="c.code"
              :class="{ active: activeCurrency === c.code }"
              @click="changeCurrency(c.code)"
            >
              <div>{{ c.code }}</div>
              <small>{{ c.value }}</small>
              <span :class="c.change > 0 ? 'up' : 'down'">
                {{ c.change > 0 ? '+' : '' }}{{ c.change }}
              </span>
            </button>
          </div>
        </div>

        <div class="converter">
          <h2>{{ t("converter.title") }}</h2>

          <div class="converter-row">
            <input v-model="amount" type="number" />

            <select v-model="from">
              <option v-for="c in currencyList" :key="c">
                {{ c }}
              </option>
            </select>
          </div>

          <button class="swap-btn" @click="swapCurrencies">⇅</button>

          <div class="converter-row">
            <input :value="converted" disabled />

            <select v-model="to">
              <option v-for="c in currencyList" :key="c">
                {{ c }}
              </option>
            </select>
          </div>
        </div>

      </div>
    </section>

    <footer class="footer">
      © 2026 FinAnalytics
    </footer>

  </div>
</template>

<style scoped>

/* RESET (ВАЖНО!) */
*,
*::before,
*::after {
  box-sizing: border-box;
}

body {
  margin: 0;
  overflow-x: hidden;
}

/* BASE */
.landing {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background: #f1f5f9;
  color: #0f172a;
  padding: 0 12px;
}

/* HEADER */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 60px;
  background: white;
  border-bottom: 1px solid #e2e8f0;
  border-radius: 0 0 16px 16px;
}

.logo {
  font-size: 30px;
  font-weight: 700;
  color: #2563eb;
}

/* RIGHT BLOCK */
.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

/* LANGS */
.langs {
  display: flex;
  gap: 6px;
  background: #f1f5f9;
  padding: 6px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.langs span {
  font-size: 18px;
  cursor: pointer;
  padding: 6px 8px;
  border-radius: 8px;
  transition: 0.2s;
}

.langs span:hover {
  background: white;
  transform: scale(1.1);
}

/* LOGIN */
.login {
  background: linear-gradient(135deg, #2563eb, #38bdf8);
  color: white;
  border: none;
  padding: 8px 18px;
  border-radius: 20px;
  font-weight: 500;
  cursor: pointer;
  transition: 0.25s;
}

.login:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(37, 99, 235, 0.35);
}

/* HERO */
.hero {
  padding: 100px 60px 120px;
  background: linear-gradient(135deg, #e0f2fe, #eef2ff);
  border-radius: 20px;
  margin-top: 10px;
}

.hero h1 {
  font-size: 48px;
  font-weight: 700;
  margin-bottom: 12px;
}

.hero p {
  font-size: 18px;
  color: #475569;
}

/* STATS */
.stats {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  margin-top: -60px;
  background: white;
  padding: 40px;
  border-radius: 20px;
  width: 100%;
  max-width: 1000px;
  margin-left: auto;
  margin-right: auto;
  box-shadow: 0 10px 40px rgba(0,0,0,0.06);
}

.stat {
  text-align: center;
}

.stat h2 {
  font-size: 30px;
  color: #2563eb;
}

.stat p {
  color: #64748b;
}

/* SECTION */
.section {
  padding: 60px 20px;
  max-width: 1000px;
  margin: auto;
}

.section h2 {
  font-size: 24px;
  margin-bottom: 10px;
}

/* DESCRIPTION */
.section-desc {
  max-width: 600px;
  margin-bottom: 25px;
  color: #64748b;
  line-height: 1.6;
  font-size: 14px;
}

/* GRID */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}

/* CARDS */
.card {
  background: white;
  padding: 18px;
  border-radius: 14px;
  border: 1px solid #e2e8f0;
  transition: 0.25s;
}

.card h3 {
  font-size: 15px;
  margin-bottom: 6px;
}

.card p {
  font-size: 13px;
  color: #64748b;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}

/* GRAPH SECTION */
.converter-section {
  padding: 70px 10px;
  background: linear-gradient(135deg, #e0f2fe, #eef2ff);
  display: flex;
  justify-content: center;
  border-radius: 20px;
}

/* CONTAINER */
.converter-wrapper {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  max-width: 1000px;
  width: 100%;
}

/* GRAPH */
.chart-box {
  background: white;
  padding: 16px;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);

  width: 100%;
  overflow: hidden;

  display: flex;
  flex-direction: column;
  gap: 10px;
}

.chart-box h2 {
  font-size: 18px;
  font-weight: 600;
}

/* ОБЁРТКА */
.chart-inner {
  width: 100%;
  height: 180px;
  position: relative;
}

.chart-inner canvas {
  position: absolute !important;
  width: 100% !important;
  height: 100% !important;
}

/* 🔥 FIX КНОПОК (БЕЗ СКРОЛЛА) */
.currency-switch {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
  margin-top: 10px;
}

.currency-switch button {
  padding: 8px 6px;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  background: white;
  cursor: pointer;
  transition: 0.2s;

  display: flex;
  flex-direction: column;
  align-items: center;

  font-size: 11px;
}

.currency-switch button small {
  font-size: 10px;
  color: #64748b;
}

.currency-switch button span {
  font-size: 10px;
}

.currency-switch button:hover {
  background: #f8fafc;
}

.currency-switch .active {
  background: #2563eb;
  color: white;
  border: none;
}

/* COLORS */
.up {
  color: #16a34a;
}

.down {
  color: #dc2626;
}

/* CONVERTER */
.converter {
  background: white;
  padding: 18px;
  border-radius: 20px;
  width: 100%;
  margin-top: 10px;
  box-shadow: 0 8px 25px rgba(0,0,0,0.05);
}

.converter-row {
  display: flex;
  gap: 8px;
  margin-top: 10px;
}

.converter input,
.converter select {
  padding: 10px;
  border-radius: 10px;
  border: 1px solid #cbd5f5;
}

/* SWAP */
.swap-btn {
  margin: 10px auto;
  display: block;
  background: #2563eb;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 12px;
  cursor: pointer;
}

/* FOOTER */
.footer {
  text-align: center;
  padding: 30px;
  color: #64748b;
}

/* MOBILE */
@media (max-width: 768px) {

  .header {
    padding: 12px;
  }

  .logo {
    font-size: 20px;
  }

  .hero {
    padding: 40px 15px;
    margin-bottom: 20px;
  }

  .hero h1 {
    font-size: 22px;
  }

  .hero p {
    font-size: 13px;
  }

  .stats {
    flex-direction: column;
    padding: 20px;
    gap: 10px;
  }

  .converter-wrapper {
    grid-template-columns: 1fr;
  }

  .chart-inner {
    height: 150px;
  }

  /* 🔥 MOBILE КНОПКИ */
  .currency-switch {
    grid-template-columns: repeat(3, 1fr);
  }
}

</style>