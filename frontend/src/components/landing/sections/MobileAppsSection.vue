<script setup>
import { ref, computed, onMounted } from "vue"
import { Bar, Line } from "vue-chartjs"
import api from "@/api/axios"

const mobileData = ref([])
const loading = ref(true)
const error = ref("")

const loadMobileData = async () => {
  loading.value = true
  error.value = ""

  try {
    const response = await api.get("/banks/mobile-analytics/")

    mobileData.value = Array.isArray(response.data?.banks)
      ? response.data.banks
      : []
  } catch (err) {
    console.error("Ошибка загрузки мобильной аналитики:", err)

    error.value = "Не удалось загрузить данные Google Play"
    mobileData.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadMobileData()
})

/*
|--------------------------------------------------------------------------
| Helpers
|--------------------------------------------------------------------------
*/

const formatInstalls = (value) => {
  const installs = Number(value) || 0

  if (installs >= 1_000_000) {
    const millions = installs / 1_000_000

    return `${Number.isInteger(millions) ? millions : millions.toFixed(1)} млн+`
  }

  if (installs >= 1_000) {
    const thousands = installs / 1_000

    return `${Number.isInteger(thousands) ? thousands : thousands.toFixed(1)} тыс.+`
  }

  return `${installs}+`
}

const formatReviews = (value) => {
  const reviews = Number(value) || 0

  return new Intl.NumberFormat("ru-RU").format(reviews)
}

const formatRating = (value) => {
  const rating = Number(value)

  if (!Number.isFinite(rating)) {
    return "—"
  }

  return rating.toFixed(2)
}

/*
|--------------------------------------------------------------------------
| Total statistics
|--------------------------------------------------------------------------
*/

const totalBanks = computed(() => {
  return mobileData.value.length
})

const totalReviews = computed(() => {
  return mobileData.value.reduce(
    (sum, item) => sum + (Number(item.reviews) || 0),
    0
  )
})

const averageRating = computed(() => {
  const ratings = mobileData.value
    .map(item => Number(item.rating))
    .filter(value => Number.isFinite(value))

  if (!ratings.length) {
    return 0
  }

  return (
    ratings.reduce((sum, value) => sum + value, 0) /
    ratings.length
  )
})

/*
|--------------------------------------------------------------------------
| Install chart
|--------------------------------------------------------------------------
*/

const installsData = computed(() => ({
  labels: mobileData.value.map(item => item.bank),

  datasets: [
    {
      label: "Установки",

      data: mobileData.value.map(
        item => Number(item.installs_value) || 0
      ),

      borderRadius: 8,

      borderSkipped: false,

      barThickness: 34,
    },
  ],
}))

/*
|--------------------------------------------------------------------------
| Rating chart
|--------------------------------------------------------------------------
*/

const ratingData = computed(() => ({
  labels: mobileData.value.map(item => item.bank),

  datasets: [
    {
      label: "Рейтинг",

      data: mobileData.value.map(
        item => Number(item.rating) || 0
      ),

      borderWidth: 3,

      pointRadius: 4,

      pointHoverRadius: 6,

      tension: 0.35,

      fill: false,
    },
  ],
}))

/*
|--------------------------------------------------------------------------
| Chart options
|--------------------------------------------------------------------------
*/

const installsOptions = {
  responsive: true,

  maintainAspectRatio: false,

  plugins: {
    legend: {
      display: false,
    },

    tooltip: {
      callbacks: {
        label: (context) => {
          return ` ${formatInstalls(context.raw)}`
        },
      },
    },
  },

  scales: {
    y: {
      beginAtZero: true,

      ticks: {
        callback: (value) => {
          if (value >= 1_000_000) {
            return `${value / 1_000_000} млн`
          }

          if (value >= 1_000) {
            return `${value / 1_000} тыс.`
          }

          return value
        },
      },
    },

    x: {
      grid: {
        display: false,
      },
    },
  },
}

const ratingOptions = {
  responsive: true,

  maintainAspectRatio: false,

  plugins: {
    legend: {
      display: false,
    },

    tooltip: {
      callbacks: {
        label: (context) => {
          return ` ${formatRating(context.raw)} / 5`
        },
      },
    },
  },

  scales: {
    y: {
      min: 0,

      max: 5,

      ticks: {
        stepSize: 1,
      },
    },

    x: {
      grid: {
        display: false,
      },
    },
  },
}
</script>

<template>
  <section class="mobile-apps">
    <div class="mobile-apps__container">

      <!-- HEADER -->
      <div class="mobile-apps__header">

        <div class="mobile-apps__badge">
          <span>▶</span>
          Google Play
        </div>

        <h2 class="mobile-apps__title">
          Мониторинг мобильных приложений
        </h2>

        <p class="mobile-apps__subtitle">
          Актуальные показатели банковских приложений:
          установки, рейтинг и количество оценок.
        </p>

      </div>

      <!-- LOADING -->
      <div
        v-if="loading"
        class="mobile-apps__state"
      >
        <div class="mobile-apps__loader"></div>

        <span>
          Загрузка данных Google Play...
        </span>
      </div>

      <!-- ERROR -->
      <div
        v-else-if="error"
        class="mobile-apps__state mobile-apps__state--error"
      >
        <span class="mobile-apps__state-icon">
          !
        </span>

        <span>
          {{ error }}
        </span>

        <button
          class="mobile-apps__retry"
          @click="loadMobileData"
        >
          Повторить
        </button>
      </div>

      <!-- CONTENT -->
      <template v-else>

        <!-- KPI -->
        <div class="mobile-apps__stats">

          <div class="mobile-stat">

            <div class="mobile-stat__icon">
              🏦
            </div>

            <div>
              <span class="mobile-stat__label">
                Приложений
              </span>

              <strong class="mobile-stat__value">
                {{ totalBanks }}
              </strong>
            </div>

          </div>

          <div class="mobile-stat">

            <div class="mobile-stat__icon">
              ⭐
            </div>

            <div>
              <span class="mobile-stat__label">
                Средний рейтинг
              </span>

              <strong class="mobile-stat__value">
                {{ averageRating.toFixed(2) }}
                <small>/ 5</small>
              </strong>
            </div>

          </div>

          <div class="mobile-stat">

            <div class="mobile-stat__icon">
              💬
            </div>

            <div>
              <span class="mobile-stat__label">
                Всего оценок
              </span>

              <strong class="mobile-stat__value">
                {{ formatReviews(totalReviews) }}
              </strong>
            </div>

          </div>

        </div>

        <!-- CHARTS -->
        <div class="mobile-apps__charts">

          <!-- INSTALLS -->
          <article class="mobile-chart-card">

            <div class="mobile-chart-card__header">

              <div>
                <h3>
                  📥 Установки приложений
                </h3>

                <p>
                  Данные из Google Play
                </p>
              </div>

              <span class="mobile-chart-card__source">
                LIVE
              </span>

            </div>

            <div class="mobile-chart">
              <Bar
                :data="installsData"
                :options="installsOptions"
              />
            </div>

          </article>

          <!-- RATING -->
          <article class="mobile-chart-card">

            <div class="mobile-chart-card__header">

              <div>
                <h3>
                  ⭐ Рейтинг приложений
                </h3>

                <p>
                  Средняя оценка пользователей
                </p>
              </div>

              <span class="mobile-chart-card__source">
                LIVE
              </span>

            </div>

            <div class="mobile-chart">
              <Line
                :data="ratingData"
                :options="ratingOptions"
              />
            </div>

          </article>

        </div>

        <!-- BANK CARDS -->
        <div class="mobile-banks">

          <div
            v-for="item in mobileData"
            :key="item.bank"
            class="mobile-bank"
          >

            <div class="mobile-bank__top">

              <div class="mobile-bank__logo">
                {{ item.bank.charAt(0) }}
              </div>

              <div class="mobile-bank__name">
                <h3>
                  {{ item.bank }}
                </h3>

                <span>
                  Google Play
                </span>
              </div>

            </div>

            <div class="mobile-bank__metrics">

              <div class="mobile-bank__metric">

                <span>
                  Установки
                </span>

                <strong>
                  {{ item.installs || formatInstalls(item.installs_value) }}
                </strong>

              </div>

              <div class="mobile-bank__metric">

                <span>
                  Рейтинг
                </span>

                <strong>
                  ⭐ {{ formatRating(item.rating) }}
                </strong>

              </div>

              <div class="mobile-bank__metric">

                <span>
                  Оценки
                </span>

                <strong>
                  {{ formatReviews(item.reviews) }}
                </strong>

              </div>

            </div>

          </div>

        </div>

        <!-- FOOTER -->
        <div class="mobile-apps__footer">

          <span class="mobile-apps__footer-dot"></span>

          <span>
            Данные получены из Google Play
          </span>

          <span>
            Обновляются автоматически
          </span>

        </div>

      </template>

    </div>
  </section>
</template>

<style scoped>
/* =========================================================
   SECTION
========================================================= */

.mobile-apps {
  padding: 90px 20px;

  background:
    radial-gradient(
      circle at 10% 10%,
      rgba(37, 99, 235, 0.05),
      transparent 30%
    ),
    radial-gradient(
      circle at 90% 90%,
      rgba(14, 165, 233, 0.05),
      transparent 30%
    ),
    #f8fafc;
}

.mobile-apps__container {
  width: 100%;
  max-width: 1180px;
  margin: 0 auto;
}

/* =========================================================
   HEADER
========================================================= */

.mobile-apps__header {
  max-width: 720px;
  margin: 0 auto 40px;
  text-align: center;
}

.mobile-apps__badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;

  padding: 7px 13px;
  margin-bottom: 15px;

  border: 1px solid #e2e8f0;
  border-radius: 999px;

  background: #fff;

  color: #334155;

  font-size: 12px;
  font-weight: 700;
}

.mobile-apps__title {
  margin: 0 0 13px;

  color: #0f172a;

  font-size: clamp(28px, 4vw, 38px);
  line-height: 1.15;
  font-weight: 800;

  letter-spacing: -0.03em;
}

.mobile-apps__subtitle {
  max-width: 650px;

  margin: 0 auto;

  color: #64748b;

  font-size: 15px;
  line-height: 1.7;
}

/* =========================================================
   KPI
========================================================= */

.mobile-apps__stats {
  display: grid;

  grid-template-columns: repeat(3, 1fr);

  gap: 16px;

  margin-bottom: 20px;
}

.mobile-stat {
  display: flex;
  align-items: center;
  gap: 13px;

  padding: 18px;

  background: #fff;

  border: 1px solid #e2e8f0;
  border-radius: 18px;

  box-shadow:
    0 4px 20px rgba(15, 23, 42, 0.04);
}

.mobile-stat__icon {
  width: 44px;
  height: 44px;

  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 13px;

  background: #f1f5f9;

  font-size: 20px;
}

.mobile-stat__label {
  display: block;

  margin-bottom: 3px;

  color: #94a3b8;

  font-size: 11px;
  font-weight: 600;
}

.mobile-stat__value {
  display: block;

  color: #0f172a;

  font-size: 22px;
  line-height: 1;

  font-weight: 800;
}

.mobile-stat__value small {
  color: #94a3b8;

  font-size: 11px;
  font-weight: 600;
}

/* =========================================================
   CHARTS
========================================================= */

.mobile-apps__charts {
  display: grid;

  grid-template-columns: repeat(2, 1fr);

  gap: 20px;
}

.mobile-chart-card {
  padding: 22px;

  background: #fff;

  border: 1px solid #e2e8f0;
  border-radius: 22px;

  box-shadow:
    0 4px 25px rgba(15, 23, 42, 0.04);
}

.mobile-chart-card__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;

  margin-bottom: 18px;
}

.mobile-chart-card__header h3 {
  margin: 0 0 4px;

  color: #0f172a;

  font-size: 16px;
  font-weight: 750;
}

.mobile-chart-card__header p {
  margin: 0;

  color: #94a3b8;

  font-size: 11px;
}

.mobile-chart-card__source {
  padding: 5px 8px;

  border-radius: 7px;

  background: #f0fdf4;

  color: #16a34a;

  font-size: 9px;
  font-weight: 800;
}

.mobile-chart {
  height: 300px;
}

/* =========================================================
   BANK CARDS
========================================================= */

.mobile-banks {
  display: grid;

  grid-template-columns: repeat(5, 1fr);

  gap: 12px;

  margin-top: 20px;
}

.mobile-bank {
  padding: 17px;

  background: #fff;

  border: 1px solid #e2e8f0;
  border-radius: 17px;

  transition:
    transform 0.25s ease,
    box-shadow 0.25s ease;
}

.mobile-bank:hover {
  transform: translateY(-3px);

  box-shadow:
    0 12px 30px rgba(15, 23, 42, 0.07);
}

.mobile-bank__top {
  display: flex;
  align-items: center;
  gap: 9px;

  margin-bottom: 17px;
}

.mobile-bank__logo {
  width: 34px;
  height: 34px;

  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 10px;

  background: #f1f5f9;

  color: #334155;

  font-size: 13px;
  font-weight: 800;
}

.mobile-bank__name {
  min-width: 0;
}

.mobile-bank__name h3 {
  margin: 0 0 2px;

  overflow: hidden;

  color: #0f172a;

  font-size: 12px;
  font-weight: 750;

  text-overflow: ellipsis;
  white-space: nowrap;
}

.mobile-bank__name span {
  color: #94a3b8;

  font-size: 9px;
}

.mobile-bank__metrics {
  display: flex;
  flex-direction: column;
  gap: 9px;
}

.mobile-bank__metric {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.mobile-bank__metric span {
  color: #94a3b8;

  font-size: 9px;
}

.mobile-bank__metric strong {
  color: #334155;

  font-size: 12px;
  font-weight: 750;
}

/* =========================================================
   FOOTER
========================================================= */

.mobile-apps__footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 9px;

  margin-top: 22px;

  color: #94a3b8;

  font-size: 10px;
}

.mobile-apps__footer-dot {
  width: 6px;
  height: 6px;

  border-radius: 50%;

  background: #22c55e;
}

/* =========================================================
   STATES
========================================================= */

.mobile-apps__state {
  min-height: 250px;

  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;

  color: #64748b;

  font-size: 13px;
}

.mobile-apps__state--error {
  flex-direction: column;
}

.mobile-apps__state-icon {
  width: 38px;
  height: 38px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 50%;

  background: #fef2f2;

  color: #dc2626;

  font-weight: 800;
}

.mobile-apps__retry {
  padding: 8px 14px;

  border: 0;
  border-radius: 9px;

  background: #0f172a;

  color: #fff;

  cursor: pointer;

  font-size: 11px;
  font-weight: 700;
}

/* =========================================================
   LOADER
========================================================= */

.mobile-apps__loader {
  width: 18px;
  height: 18px;

  border: 2px solid #e2e8f0;
  border-top-color: #2563eb;

  border-radius: 50%;

  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* =========================================================
   TABLET
========================================================= */

@media (max-width: 1050px) {
  .mobile-banks {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 850px) {
  .mobile-apps {
    padding: 70px 20px;
  }

  .mobile-apps__charts {
    grid-template-columns: 1fr;
  }

  .mobile-apps__stats {
    grid-template-columns: 1fr;
  }
}

/* =========================================================
   MOBILE
========================================================= */

@media (max-width: 600px) {
  .mobile-apps {
    padding: 55px 16px;
  }

  .mobile-apps__title {
    font-size: 28px;
  }

  .mobile-apps__subtitle {
    font-size: 14px;
  }

  .mobile-banks {
    grid-template-columns: 1fr;
  }

  .mobile-chart-card {
    padding: 17px;
  }

  .mobile-chart {
    height: 250px;
  }

  .mobile-apps__footer {
    flex-wrap: wrap;
  }
}
</style>