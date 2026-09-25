<script setup>
import { computed } from "vue"
import { useI18n } from "vue-i18n"
import { Line, Bar } from "vue-chartjs"

const { t } = useI18n()

/*
|--------------------------------------------------------------------------
| Monitoring data
|--------------------------------------------------------------------------
| Пока используются демонстрационные значения для визуализации.
| Позже сюда можно подключить реальные данные API.
|--------------------------------------------------------------------------
*/

const monitoringItems = computed(() => [
  {
    key: "analytics",
    icon: "📊",
    title: t("benefits.analytics"),
    description: t("benefits.analyticsDesc"),
    value: "82%",
    label: "Активность",
    change: "+12.4%",
    positive: true,
    type: "line",
    data: [42, 48, 46, 55, 58, 64, 61, 69, 74, 82],
  },

  {
    key: "ai",
    icon: "🤖",
    title: t("benefits.ai"),
    description: t("benefits.aiDesc"),
    value: "87%",
    label: "Точность",
    change: "+8.7%",
    positive: true,
    type: "bar",
    data: [58, 63, 61, 70, 74, 72, 79, 82, 84, 87],
  },

  {
    key: "speed",
    icon: "⚡",
    title: t("benefits.speed"),
    description: t("benefits.speedDesc"),
    value: "2.4 сек",
    label: "Среднее время",
    change: "-18.2%",
    positive: true,
    type: "line",
    data: [4.1, 3.8, 3.7, 3.4, 3.3, 3.1, 2.9, 2.7, 2.6, 2.4],
  },

  {
    key: "security",
    icon: "🔒",
    title: t("benefits.security"),
    description: t("benefits.securityDesc"),
    value: "99.8%",
    label: "Надёжность",
    change: "+1.6%",
    positive: true,
    type: "line",
    data: [96.2, 96.8, 97.1, 97.4, 97.8, 98.1, 98.5, 98.9, 99.3, 99.8],
  },
])

const chartLabels = [
  "1",
  "2",
  "3",
  "4",
  "5",
  "6",
  "7",
  "8",
  "9",
  "10",
]

const getChartData = (item) => {
  return {
    labels: chartLabels,

    datasets: [
      {
        data: item.data,

        borderWidth: 2,

        pointRadius: 0,

        pointHoverRadius: 4,

        tension: 0.4,

        fill: true,
      },
    ],
  }
}

const getChartOptions = (item) => {
  return {
    responsive: true,

    maintainAspectRatio: false,

    plugins: {
      legend: {
        display: false,
      },

      tooltip: {
        enabled: true,

        displayColors: false,

        callbacks: {
          label: (context) => {
            return `${context.parsed.y}`
          },
        },
      },
    },

    scales: {
      x: {
        display: false,

        grid: {
          display: false,
        },
      },

      y: {
        display: false,

        grid: {
          display: false,
        },
      },
    },

    interaction: {
      intersect: false,

      mode: "index",
    },
  }
}
</script>

<template>
  <section class="monitoring">
    <div class="monitoring__container">

      <!-- HEADER -->
      <div class="monitoring__header">

        <div class="monitoring__badge">
          <span class="monitoring__badge-icon">
            ◉
          </span>

          <span>
            {{ t("benefits.badge") }}
          </span>
        </div>

        <h2 class="monitoring__title">
          {{ t("benefits.title") }}
        </h2>

        <p class="monitoring__description">
          {{ t("benefits.description") }}
        </p>

      </div>

      <!-- MONITORING GRID -->
      <div class="monitoring__grid">

        <article
          v-for="item in monitoringItems"
          :key="item.key"
          class="monitoring-card"
        >

          <!-- CARD HEADER -->
          <div class="monitoring-card__header">

            <div class="monitoring-card__identity">

              <div class="monitoring-card__icon">
                {{ item.icon }}
              </div>

              <div>
                <h3 class="monitoring-card__title">
                  {{ item.title }}
                </h3>

                <p class="monitoring-card__description">
                  {{ item.description }}
                </p>
              </div>

            </div>

            <div class="monitoring-card__status">
              <span></span>
            </div>

          </div>

          <!-- VALUE -->
          <div class="monitoring-card__metrics">

            <div class="monitoring-card__main">

              <span class="monitoring-card__value">
                {{ item.value }}
              </span>

              <span class="monitoring-card__label">
                {{ item.label }}
              </span>

            </div>

            <div
              class="monitoring-card__change"
              :class="{
                'monitoring-card__change--negative':
                  !item.positive
              }"
            >
              <span>
                {{ item.positive ? "↗" : "↘" }}
              </span>

              {{ item.change }}
            </div>

          </div>

          <!-- CHART -->
          <div class="monitoring-card__chart">

            <Line
              v-if="item.type === 'line'"
              :data="getChartData(item)"
              :options="getChartOptions(item)"
            />

            <Bar
              v-else
              :data="getChartData(item)"
              :options="getChartOptions(item)"
            />

          </div>

          <!-- FOOTER -->
          <div class="monitoring-card__footer">

            <span>
              {{ t("benefits.monitoringPeriod") }}
            </span>

            <span>
              {{ t("benefits.live") }}
            </span>

          </div>

        </article>

      </div>

      <!-- BOTTOM INFO -->
      <div class="monitoring__bottom">

        <div class="monitoring__bottom-icon">
          ↻
        </div>

        <div class="monitoring__bottom-content">

          <strong>
            {{ t("benefits.monitoringTitle") }}
          </strong>

          <p>
            {{ t("benefits.monitoringDesc") }}
          </p>

        </div>

        <div class="monitoring__bottom-status">
          <span></span>

          {{ t("benefits.active") }}
        </div>

      </div>

    </div>
  </section>
</template>

<style scoped>

/* =========================================================
   SECTION
========================================================= */

.monitoring {
  position: relative;

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

.monitoring__container {
  width: 100%;
  max-width: 1180px;

  margin: 0 auto;
}

/* =========================================================
   HEADER
========================================================= */

.monitoring__header {
  max-width: 700px;

  margin: 0 auto 45px;

  text-align: center;
}

.monitoring__badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;

  padding: 7px 13px;

  margin-bottom: 16px;

  border: 1px solid #dbeafe;

  border-radius: 999px;

  background: #eff6ff;

  color: #2563eb;

  font-size: 12px;

  font-weight: 700;
}

.monitoring__badge-icon {
  font-size: 12px;
}

.monitoring__title {
  margin: 0 0 14px;

  color: #0f172a;

  font-size: clamp(28px, 4vw, 38px);

  line-height: 1.15;

  font-weight: 800;

  letter-spacing: -0.03em;
}

.monitoring__description {
  max-width: 640px;

  margin: 0 auto;

  color: #64748b;

  font-size: 15px;

  line-height: 1.7;
}

/* =========================================================
   GRID
========================================================= */

.monitoring__grid {
  display: grid;

  grid-template-columns: repeat(2, 1fr);

  gap: 20px;
}

/* =========================================================
   CARD
========================================================= */

.monitoring-card {
  position: relative;

  min-height: 330px;

  padding: 24px;

  overflow: hidden;

  background: rgba(255, 255, 255, 0.94);

  border: 1px solid #e2e8f0;

  border-radius: 22px;

  box-shadow:
    0 4px 25px rgba(15, 23, 42, 0.04);

  transition:
    transform 0.25s ease,
    box-shadow 0.25s ease,
    border-color 0.25s ease;
}

.monitoring-card:hover {
  transform: translateY(-5px);

  border-color: #cbd5e1;

  box-shadow:
    0 20px 50px rgba(15, 23, 42, 0.09);
}

/* =========================================================
   CARD HEADER
========================================================= */

.monitoring-card__header {
  display: flex;

  align-items: flex-start;

  justify-content: space-between;

  margin-bottom: 25px;
}

.monitoring-card__identity {
  display: flex;

  align-items: center;

  gap: 13px;
}

.monitoring-card__icon {
  width: 48px;
  height: 48px;

  flex-shrink: 0;

  display: flex;

  align-items: center;

  justify-content: center;

  border-radius: 14px;

  background: #f1f5f9;

  font-size: 23px;
}

.monitoring-card__title {
  margin: 0 0 4px;

  color: #0f172a;

  font-size: 17px;

  font-weight: 750;
}

.monitoring-card__description {
  max-width: 230px;

  margin: 0;

  color: #94a3b8;

  font-size: 11px;

  line-height: 1.45;
}

.monitoring-card__status {
  width: 9px;
  height: 9px;

  display: flex;

  align-items: center;

  justify-content: center;

  border-radius: 50%;

  background: #dcfce7;
}

.monitoring-card__status span {
  width: 5px;
  height: 5px;

  border-radius: 50%;

  background: #22c55e;
}

/* =========================================================
   METRICS
========================================================= */

.monitoring-card__metrics {
  display: flex;

  align-items: flex-end;

  justify-content: space-between;

  margin-bottom: 12px;
}

.monitoring-card__main {
  display: flex;

  flex-direction: column;

  gap: 2px;
}

.monitoring-card__value {
  color: #0f172a;

  font-size: 30px;

  line-height: 1;

  font-weight: 800;

  letter-spacing: -0.03em;
}

.monitoring-card__label {
  color: #94a3b8;

  font-size: 11px;

  font-weight: 600;
}

.monitoring-card__change {
  display: inline-flex;

  align-items: center;

  gap: 4px;

  padding: 5px 9px;

  border-radius: 8px;

  background: #f0fdf4;

  color: #16a34a;

  font-size: 11px;

  font-weight: 700;
}

.monitoring-card__change--negative {
  background: #fef2f2;

  color: #dc2626;
}

/* =========================================================
   CHART
========================================================= */

.monitoring-card__chart {
  height: 125px;

  margin: 10px -5px 0;
}

/* =========================================================
   FOOTER
========================================================= */

.monitoring-card__footer {
  display: flex;

  align-items: center;

  justify-content: space-between;

  padding-top: 14px;

  margin-top: 5px;

  border-top: 1px solid #f1f5f9;

  color: #94a3b8;

  font-size: 10px;

  font-weight: 600;
}

.monitoring-card__footer span:last-child {
  color: #16a34a;
}

/* =========================================================
   BOTTOM
========================================================= */

.monitoring__bottom {
  display: flex;

  align-items: center;

  gap: 14px;

  max-width: 760px;

  margin: 28px auto 0;

  padding: 16px 18px;

  background: rgba(255, 255, 255, 0.8);

  border: 1px solid #e2e8f0;

  border-radius: 16px;
}

.monitoring__bottom-icon {
  width: 40px;
  height: 40px;

  flex-shrink: 0;

  display: flex;

  align-items: center;

  justify-content: center;

  border-radius: 11px;

  background: #eff6ff;

  color: #2563eb;

  font-size: 19px;
}

.monitoring__bottom-content {
  flex: 1;
}

.monitoring__bottom-content strong {
  display: block;

  margin-bottom: 3px;

  color: #334155;

  font-size: 12px;
}

.monitoring__bottom-content p {
  margin: 0;

  color: #94a3b8;

  font-size: 11px;

  line-height: 1.5;
}

.monitoring__bottom-status {
  display: inline-flex;

  align-items: center;

  gap: 6px;

  color: #16a34a;

  font-size: 11px;

  font-weight: 700;
}

.monitoring__bottom-status span {
  width: 6px;
  height: 6px;

  border-radius: 50%;

  background: #22c55e;
}

/* =========================================================
   TABLET
========================================================= */

@media (max-width: 850px) {
  .monitoring {
    padding: 70px 20px;
  }

  .monitoring__grid {
    grid-template-columns: 1fr;
  }
}

/* =========================================================
   MOBILE
========================================================= */

@media (max-width: 600px) {
  .monitoring {
    padding: 55px 16px;
  }

  .monitoring__header {
    margin-bottom: 30px;
  }

  .monitoring__title {
    font-size: 28px;
  }

  .monitoring__description {
    font-size: 14px;
  }

  .monitoring-card {
    min-height: 310px;

    padding: 19px;
  }

  .monitoring-card__value {
    font-size: 27px;
  }

  .monitoring-card__chart {
    height: 115px;
  }

  .monitoring__bottom {
    align-items: flex-start;

    flex-wrap: wrap;
  }

  .monitoring__bottom-status {
    margin-left: 54px;
  }
}
</style>