<template>
  <div class="scoring-page">
    <!-- ================================================================ -->
    <!-- ERROR -->
    <!-- ================================================================ -->

    <transition name="fade">
      <div v-if="error" class="error-banner">
        <div class="error-icon">!</div>

        <div class="error-content">
          <strong>{{ t("common.error") }}</strong>
          <span>{{ error }}</span>
        </div>

        <button
          class="error-close"
          type="button"
          @click="error = null"
        >
          ×
        </button>
      </div>
    </transition>

    <!-- ================================================================ -->
    <!-- HEADER -->
    <!-- ================================================================ -->

    <header class="page-header">
      <div class="header-main">
        <div class="eyebrow">
          <span class="eyebrow-dot"></span>
          AI CREDIT ANALYTICS
        </div>

        <h1>{{ t("scoring.title") }}</h1>

        <p>
          {{ t("scoring.subtitle") }}
        </p>
      </div>

      <div class="header-actions">
        <div
          v-if="lastCalculated"
          class="last-calculated"
        >
          <span class="status-dot"></span>

          <div>
            <small>
              {{ t("scoring.lastCalculation") }}
            </small>

            <strong>
              {{ formatDateTime(lastCalculated) }}
            </strong>
          </div>
        </div>

        <button
          type="button"
          class="recalculate-btn"
          :disabled="loading"
          @click="calculateScore"
        >
          <svg
            v-if="!loading"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M20 11a8.1 8.1 0 0 0-15.5-3" />
            <path d="M4 4v4h4" />
            <path d="M4 13a8.1 8.1 0 0 0 15.5 3" />
            <path d="M20 20v-4h-4" />
          </svg>

          <span
            v-else
            class="spinner"
          ></span>

          {{
            loading
              ? t("scoring.processing")
              : t("scoring.recalc")
          }}
        </button>
      </div>
    </header>

    <!-- ================================================================ -->
    <!-- EMPTY STATE -->
    <!-- ================================================================ -->

    <section
      v-if="!latest && !loading"
      class="empty-state"
    >
      <div class="empty-icon">
        ◎
      </div>

      <h2>
        {{ t("scoring.noData") }}
      </h2>

      <p>
        {{ t("scoring.noDataDescription") }}
      </p>

      <button
        type="button"
        class="recalculate-btn"
        @click="calculateScore"
      >
        {{ t("scoring.recalc") }}
      </button>
    </section>

    <!-- ================================================================ -->
    <!-- LOADING -->
    <!-- ================================================================ -->

    <section
      v-if="loading && !latest"
      class="loading-state"
    >
      <div class="loading-spinner"></div>

      <span>
        {{ t("scoring.processing") }}
      </span>
    </section>

    <!-- ================================================================ -->
    <!-- MAIN -->
    <!-- ================================================================ -->

    <template v-if="latest">
      <!-- ============================================================ -->
      <!-- HERO SCORE -->
      <!-- ============================================================ -->

      <section class="score-hero">
        <div class="score-hero-main">
          <div class="hero-label">
            <span class="hero-label-icon">✦</span>

            {{ t("scoring.currentScore") }}
          </div>

          <div class="score-main-row">
            <div class="score-number">
              {{ currentScore }}
            </div>

            <div class="score-meta">
              <div
                class="risk-badge"
                :class="`risk-${normalizedRisk.toLowerCase()}`"
              >
                <span class="risk-dot"></span>

                {{ riskLabel }}
              </div>

              <span class="score-description">
                {{ t("scoring.scoreDescription") }}
              </span>
            </div>
          </div>

          <div class="score-progress">
            <div
              class="score-progress-fill"
              :style="{
                width: scoreProgress + '%'
              }"
            ></div>
          </div>

          <div class="score-scale">
            <span>{{ scoreScaleMin }}</span>

            <span>
              {{ t("scoring.creditScore") }}
            </span>

            <span>{{ scoreScaleMax }}</span>
          </div>
        </div>

        <div class="score-hero-side">
          <div class="hero-stat">
            <span class="hero-stat-label">
              {{ t("scoring.approval") }}
            </span>

            <strong>
              {{ approvalPercent }}%
            </strong>

            <div class="mini-progress">
              <div
                class="mini-progress-fill"
                :style="{
                  width: approvalPercent + '%'
                }"
              ></div>
            </div>
          </div>

          <div class="hero-divider"></div>

          <div class="hero-stat">
            <span class="hero-stat-label">
              {{ t("scoring.recommendedLimit") }}
            </span>

            <strong class="limit-value">
              {{ formatMoney(latest.recommended_limit) }}
            </strong>
          </div>
        </div>
      </section>

      <!-- ============================================================ -->
      <!-- KPI -->
      <!-- ============================================================ -->

      <section class="kpi-grid">
        <!-- SCORE -->

        <article class="kpi-card">
          <div class="kpi-icon blue">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
            >
              <path d="M4 19V5" />
              <path d="M4 19h16" />
              <path d="m7 15 3-4 3 2 5-7" />
            </svg>
          </div>

          <div class="kpi-content">
            <span>
              {{ t("scoring.creditScore") }}
            </span>

            <strong>
              {{ currentScore }}
            </strong>

            <small>
              {{ t("scoring.aiScore") }}
            </small>
          </div>
        </article>

        <!-- APPROVAL -->

        <article class="kpi-card">
          <div class="kpi-icon green">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
            >
              <path d="M20 6 9 17l-5-5" />
            </svg>
          </div>

          <div class="kpi-content">
            <span>
              {{ t("scoring.approval") }}
            </span>

            <strong>
              {{ approvalPercent }}%
            </strong>

            <small>
              {{ t("scoring.estimatedProbability") }}
            </small>
          </div>
        </article>

        <!-- LIMIT -->

        <article class="kpi-card">
          <div class="kpi-icon purple">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
            >
              <rect
                x="3"
                y="5"
                width="18"
                height="14"
                rx="2"
              />

              <path d="M3 10h18" />
            </svg>
          </div>

          <div class="kpi-content">
            <span>
              {{ t("scoring.recommendedLimit") }}
            </span>

            <strong class="limit-kpi">
              {{ formatMoneyShort(latest.recommended_limit) }}
            </strong>

            <small>
              {{ t("scoring.limitDescription") }}
            </small>
          </div>
        </article>

        <!-- RISK -->

        <article class="kpi-card">
          <div class="kpi-icon orange">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
            >
              <path d="M12 3v18" />
              <path
                d="M5 8h10.5a3.5 3.5 0 0 1 0 7H7"
              />
            </svg>
          </div>

          <div class="kpi-content">
            <span>
              {{ t("scoring.riskLevel") }}
            </span>

            <strong>
              {{ riskLabel }}
            </strong>

            <small>
              {{ t("scoring.currentRisk") }}
            </small>
          </div>
        </article>
      </section>

      <!-- ============================================================ -->
      <!-- ANALYTICS GRID -->
      <!-- ============================================================ -->

      <section class="analytics-grid">
        <!-- ========================================================== -->
        <!-- SCORE TREND -->
        <!-- ========================================================== -->

        <article class="panel trend-panel">
          <div class="panel-header trend-header">
            <div>
              <span class="panel-eyebrow">
                PERFORMANCE
              </span>

              <h2>
                {{ t("scoring.trend") }}
              </h2>

              <p>
                {{ t("scoring.trendDescription") }}
              </p>
            </div>

            <div class="trend-header-right">
              <div class="trend-current">
                <span>
                  {{ t("scoring.currentScore") }}
                </span>

                <strong>
                  {{ currentScore }}
                </strong>

                <small
                  v-if="periodChange !== null"
                  :class="
                    periodChange >= 0
                      ? 'positive'
                      : 'negative'
                  "
                >
                  {{
                    periodChange >= 0
                      ? "↑"
                      : "↓"
                  }}

                  {{ absolutePeriodChange }}
                </small>
              </div>
            </div>
          </div>

          <!-- PERIOD SELECTOR -->

          <div class="trend-controls">
            <button
              v-for="period in periods"
              :key="period"
              type="button"
              class="period-btn"
              :class="{
                active:
                  selectedPeriod === period
              }"
              @click="selectedPeriod = period"
            >
              {{ period }}
            </button>
          </div>

          <!-- CHART -->

          <div
            v-if="trendPoints.length"
            class="chart-wrapper"
          >
            <Line
              :data="trendData"
              :options="trendOptions"
            />
          </div>

          <div
            v-else
            class="chart-empty"
          >
            <span>⌁</span>

            <p>
              {{ t("scoring.noHistory") }}
            </p>
          </div>

          <!-- STATS -->

          <div
            v-if="trendPoints.length"
            class="trend-stats"
          >
            <div class="trend-stat">
              <span>
                {{ t("scoring.periodChange") }}
              </span>

              <strong
                :class="
                  periodChange >= 0
                    ? 'positive'
                    : 'negative'
                "
              >
                {{
                  periodChange === null
                    ? "-"
                    : (
                        periodChange >= 0
                          ? "+"
                          : ""
                      ) + periodChange
                }}
              </strong>
            </div>

            <div class="trend-stat">
              <span>
                {{ t("scoring.average") }}
              </span>

              <strong>
                {{ averageScore }}
              </strong>
            </div>

            <div class="trend-stat">
              <span>
                {{ t("scoring.minimum") }}
              </span>

              <strong>
                {{ minimumScore }}
              </strong>
            </div>

            <div class="trend-stat">
              <span>
                {{ t("scoring.maximum") }}
              </span>

              <strong>
                {{ maximumScore }}
              </strong>
            </div>
          </div>
        </article>

        <!-- ========================================================== -->
        <!-- BREAKDOWN -->
        <!-- ========================================================== -->

        <article class="panel breakdown-panel">
          <div class="panel-header">
            <div>
              <span class="panel-eyebrow">
                AI MODEL
              </span>

              <h2>
                {{ t("scoring.aiBreakdown") }}
              </h2>

              <p>
                {{ t("scoring.breakdownDescription") }}
              </p>
            </div>

            <div class="model-badge">
              {{
                latest.model_version ||
                "AI"
              }}
            </div>
          </div>

          <div class="factor-list">
            <div
              v-for="factor in factors"
              :key="factor.key"
              class="factor-row"
            >
              <div
                class="factor-icon"
                :class="factor.color"
              >
                {{ factor.icon }}
              </div>

              <div class="factor-info">
                <div class="factor-top">
                  <span>
                    {{ factor.label }}
                  </span>

                  <strong>
                    {{ factor.value }}
                  </strong>
                </div>

                <div class="factor-progress">
                  <div
                    class="factor-progress-fill"
                    :class="factor.color"
                    :style="{
                      width:
                        factor.percent +
                        '%'
                    }"
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </article>
      </section>

      <!-- ============================================================ -->
      <!-- HISTORY -->
      <!-- ============================================================ -->

      <section class="panel history-panel">
        <div class="panel-header history-header">
          <div>
            <span class="panel-eyebrow">
              AUDIT TRAIL
            </span>

            <h2>
              {{ t("scoring.history") }}
            </h2>

            <p>
              {{ t("scoring.historyDescription") }}
            </p>
          </div>

          <div class="history-badge">
            <strong>
              {{ visibleHistory.length }}
            </strong>

            <span>
              /
              {{ history.length }}
            </span>
          </div>
        </div>

        <!-- SCROLL WINDOW -->

        <div
          v-if="visibleHistory.length"
          class="history-window"
        >
          <div class="history-list">
            <div
              v-for="(item, index) in visibleHistory"
              :key="item.id || index"
              class="history-row"
            >
              <!-- DATE -->

              <div class="history-date">
                <strong>
                  {{
                    formatHistoryDate(
                      item.created_at ||
                      item.created
                    )
                  }}
                </strong>

                <span>
                  {{
                    formatTime(
                      item.created_at ||
                      item.created
                    )
                  }}
                </span>
              </div>

              <!-- SCORE -->

              <div class="history-score">
                <span>
                  {{ t("scoring.score") }}
                </span>

                <strong>
                  {{
                    item.score ??
                    item.credit_score ??
                    "-"
                  }}
                </strong>
              </div>

              <!-- CHANGE -->

              <div class="history-change">
                <span>
                  {{ t("scoring.change") }}
                </span>

                <strong
                  :class="
                    historyChange(
                      index
                    ) >= 0
                      ? 'positive'
                      : 'negative'
                  "
                >
                  {{
                    historyChangeText(
                      index
                    )
                  }}
                </strong>
              </div>

              <!-- APPROVAL -->

              <div class="history-approval">
                <span>
                  {{ t("scoring.approval") }}
                </span>

                <strong>
                  {{
                    formatApproval(
                      item.approval_probability
                    )
                  }}
                </strong>
              </div>

              <!-- RISK -->

              <div class="history-risk">
                <span
                  class="table-risk"
                  :class="
                    `risk-${normalizeRisk(
                      item.risk_category ||
                      item.risk
                    ).toLowerCase()}`
                  "
                >
                  <span class="risk-dot"></span>

                  {{
                    riskLabelFor(
                      item.risk_category ||
                      item.risk
                    )
                  }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div
          v-else
          class="history-empty"
        >
          <span>◎</span>

          <p>
            {{ t("scoring.noHistory") }}
          </p>
        </div>
      </section>
    </template>

    <!-- ================================================================ -->
    <!-- TOAST -->
    <!-- ================================================================ -->

    <transition name="toast">
      <div
        v-if="showToast"
        class="toast"
        :class="toastType"
      >
        <span class="toast-icon">
          {{
            toastType === "success"
              ? "✓"
              : "!"
          }}
        </span>

        <span>
          {{ toastMessage }}
        </span>
      </div>
    </transition>
  </div>
</template>

<script setup>
import {
  computed,
  onMounted,
  ref,
} from "vue"

import { useI18n } from "vue-i18n"

import {
  Line,
} from "vue-chartjs"

import "chart.js/auto"

import api from "@/api/axios"

const {
  t,
  locale,
} = useI18n()

/* ========================================================================== */
/* STATE                                                                      */
/* ========================================================================== */

const loading = ref(false)

const error = ref(null)

const latest = ref(null)

const history = ref([])

const showToast = ref(false)

const toastMessage = ref("")

const toastType = ref("success")

const lastCalculated = ref(null)

const selectedPeriod = ref(20)

/* ========================================================================== */
/* CONSTANTS                                                                  */
/* ========================================================================== */

const periods = [
  7,
  14,
  20,
]

const scoreScaleMin = 300

const scoreScaleMax = 900

const localeMap = {
  ru: "ru-RU",
  en: "en-US",
  uz: "uz-UZ",
}

/* ========================================================================== */
/* LOCALE                                                                     */
/* ========================================================================== */

function currentLocale() {
  return (
    localeMap[locale.value] ||
    "ru-RU"
  )
}

/* ========================================================================== */
/* API                                                                        */
/* ========================================================================== */

async function loadDashboard() {
  const response = await api.get(
    "/scoring/dashboard/"
  )

  const data =
    response.data || {}

  latest.value =
    data.scoring || null

  if (
    latest.value?.created_at
  ) {
    lastCalculated.value =
      latest.value.created_at
  }
}

async function loadHistory() {
  const response = await api.get(
    "/scoring/history/"
  )

  const data =
    response.data

  if (Array.isArray(data)) {
    history.value = data
  } else {
    history.value =
      data?.results || []
  }
}

async function loadData() {
  loading.value = true

  error.value = null

  try {
    await Promise.all([
      loadDashboard(),
      loadHistory(),
    ])
  } catch (err) {
    console.error(err)

    error.value =
      err?.response?.data?.detail ||
      err?.response?.data?.message ||
      t("scoring.loadError")
  } finally {
    loading.value = false
  }
}

/* ========================================================================== */
/* CALCULATE                                                                  */
/* ========================================================================== */

async function calculateScore() {
  if (loading.value) {
    return
  }

  loading.value = true

  error.value = null

  try {
    const response =
      await api.post(
        "/scoring/calculate/"
      )

    if (
      response.data?.scoring
    ) {
      latest.value =
        response.data.scoring
    }

    await Promise.all([
      loadDashboard(),
      loadHistory(),
    ])

    lastCalculated.value =
      latest.value?.created_at ||
      new Date().toISOString()

    showToastMessage(
      t("scoring.toastSuccess"),
      "success"
    )
  } catch (err) {
    console.error(err)

    const message =
      err?.response?.data?.detail ||
      err?.response?.data?.message ||
      t("scoring.toastError")

    showToastMessage(
      message,
      "error"
    )
  } finally {
    loading.value = false
  }
}

/* ========================================================================== */
/* SCORE                                                                      */
/* ========================================================================== */

const currentScore = computed(() => {
  return Number(
    latest.value?.score ??
    latest.value?.credit_score ??
    0
  )
})

const scoreProgress = computed(() => {
  if (!currentScore.value) {
    return 0
  }

  const value =
    (
      (currentScore.value -
        scoreScaleMin) /
      (scoreScaleMax -
        scoreScaleMin)
    ) * 100

  return Math.min(
    100,
    Math.max(0, value)
  )
})

const approvalPercent = computed(() => {
  const value = Number(
    latest.value
      ?.approval_probability ??
      0
  )

  return Math.round(
    value <= 1
      ? value * 100
      : value
  )
})

/* ========================================================================== */
/* RISK                                                                       */
/* ========================================================================== */

function normalizeRisk(value) {
  const normalized =
    String(value || "")
      .trim()
      .toUpperCase()

  if (normalized === "LOW") {
    return "LOW"
  }

  if (
    normalized === "MEDIUM"
  ) {
    return "MEDIUM"
  }

  if (
    normalized === "HIGH"
  ) {
    return "HIGH"
  }

  if (
    normalized === "REJECT" ||
    normalized === "CRITICAL"
  ) {
    return "REJECT"
  }

  return "MEDIUM"
}

const normalizedRisk =
  computed(() => {
    return normalizeRisk(
      latest.value
        ?.risk_category ||
      latest.value?.risk ||
      "MEDIUM"
    )
  })

function riskLabelFor(value) {
  const risk =
    normalizeRisk(value)

  const labels = {
    LOW: t(
      "scoring.risk.low"
    ),

    MEDIUM: t(
      "scoring.risk.medium"
    ),

    HIGH: t(
      "scoring.risk.high"
    ),

    REJECT: t(
      "scoring.risk.reject"
    ),
  }

  return labels[risk]
}

const riskLabel = computed(() => {
  return riskLabelFor(
    normalizedRisk.value
  )
})

/* ========================================================================== */
/* FACTORS                                                                    */
/* ========================================================================== */

function factorPercent(
  value,
  max = 100
) {
  const number =
    Number(value ?? 0)

  if (number <= 0) {
    return 0
  }

  return Math.min(
    100,
    Math.max(
      0,
      (number / max) * 100
    )
  )
}

const factors = computed(() => {
  const item =
    latest.value || {}

  return [
    {
      key: "income",

      label: t(
        "scoring.income"
      ),

      value:
        item.income_score ??
        0,

      percent:
        factorPercent(
          item.income_score,
          100
        ),

      icon: "₿",

      color: "blue",
    },

    {
      key: "dti",

      label: t(
        "scoring.dti"
      ),

      value:
        item.dti_score ??
        0,

      percent:
        factorPercent(
          item.dti_score,
          150
        ),

      icon: "%",

      color: "green",
    },

    {
      key: "employment",

      label: t(
        "scoring.employment"
      ),

      value:
        item.employment_score ??
        0,

      percent:
        factorPercent(
          item.employment_score,
          100
        ),

      icon: "◈",

      color: "purple",
    },

    {
      key: "history",

      label: t(
        "scoring.creditHistory"
      ),

      value:
        item.history_score ??
        0,

      percent:
        factorPercent(
          item.history_score,
          100
        ),

      icon: "↗",

      color: "orange",
    },

    {
      key: "profile",

      label: t(
        "scoring.profile"
      ),

      value:
        item.profile_score ??
        0,

      percent:
        factorPercent(
          item.profile_score,
          100
        ),

      icon: "◎",

      color: "cyan",
    },
  ]
})

/* ========================================================================== */
/* HISTORY                                                                     */
/* ========================================================================== */

/*
 * В интерфейсе показываем максимум 20 последних записей.
 *
 * Старые записи НЕ удаляются из БД.
 * Они просто не отображаются в этом окне.
 */

const visibleHistory =
  computed(() => {
    return history.value
      .slice()
      .sort(
        (
          a,
          b
        ) => {
          const dateA =
            new Date(
              a.created_at ||
              a.created ||
              0
            ).getTime()

          const dateB =
            new Date(
              b.created_at ||
              b.created ||
              0
            ).getTime()

          return dateB - dateA
        }
      )
      .slice(0, 20)
  })

function getHistoryScore(
  item
) {
  return Number(
    item?.score ??
    item?.credit_score ??
    0
  )
}

/*
 * Для каждой строки сравниваем score
 * с предыдущим более старым расчётом.
 */

function historyChange(index) {
  const current =
    getHistoryScore(
      visibleHistory.value[
        index
      ]
    )

  const previous =
    visibleHistory.value[
      index + 1
    ]

  if (!previous) {
    return 0
  }

  return (
    current -
    getHistoryScore(previous)
  )
}

function historyChangeText(
  index
) {
  if (
    index ===
    visibleHistory.value
      .length -
      1
  ) {
    return "-"
  }

  const change =
    historyChange(index)

  if (change > 0) {
    return `+${change}`
  }

  return String(change)
}

/* ========================================================================== */
/* TREND                                                                      */
/* ========================================================================== */

const trendPoints =
  computed(() => {
    return visibleHistory.value
      .slice(0, selectedPeriod.value)
      .reverse()
  })

const trendScores =
  computed(() => {
    return trendPoints.value.map(
      (item) =>
        getHistoryScore(item)
    )
  })

const averageScore =
  computed(() => {
    if (
      !trendScores.value.length
    ) {
      return 0
    }

    const total =
      trendScores.value.reduce(
        (
          sum,
          score
        ) => sum + score,
        0
      )

    return Math.round(
      total /
        trendScores.value.length
    )
  })

const minimumScore =
  computed(() => {
    if (
      !trendScores.value.length
    ) {
      return 0
    }

    return Math.min(
      ...trendScores.value
    )
  })

const maximumScore =
  computed(() => {
    if (
      !trendScores.value.length
    ) {
      return 0
    }

    return Math.max(
      ...trendScores.value
    )
  })

const periodChange =
  computed(() => {
    if (
      trendScores.value.length <
      2
    ) {
      return null
    }

    return (
      trendScores.value[
        trendScores.value.length -
          1
      ] -
      trendScores.value[0]
    )
  })

const absolutePeriodChange =
  computed(() => {
    if (
      periodChange.value ===
      null
    ) {
      return "-"
    }

    return Math.abs(
      periodChange.value
    )
  })

/* ========================================================================== */
/* CHART DATA                                                                 */
/* ========================================================================== */

const trendData =
  computed(() => {
    const scores =
      trendScores.value

    const average =
      averageScore.value

    return {
      labels:
        trendPoints.value.map(
          (item) =>
            formatShortDate(
              item.created_at ||
              item.created
            )
        ),

      datasets: [
        {
          label: t(
            "scoring.creditScore"
          ),

          data: scores,

          borderColor:
            "#2563eb",

          backgroundColor:
            "rgba(37, 99, 235, 0.10)",

          fill: true,

          tension: 0.42,

          borderWidth: 3,

          pointRadius: 0,

          pointHoverRadius: 6,

          pointHoverBackgroundColor:
            "#ffffff",

          pointHoverBorderColor:
            "#2563eb",

          pointHoverBorderWidth: 3,
        },

        {
          label: t(
            "scoring.average"
          ),

          data: scores.map(
            () => average
          ),

          borderColor:
            "rgba(148, 163, 184, 0.7)",

          borderDash: [
            6,
            6,
          ],

          borderWidth: 1.5,

          pointRadius: 0,

          fill: false,

          tension: 0,
        },
      ],
    }
  })

const trendOptions =
  computed(() => {
    const scores =
      trendScores.value

    let min =
      scores.length
        ? Math.min(
            ...scores
          )
        : scoreScaleMin

    let max =
      scores.length
        ? Math.max(
            ...scores
          )
        : scoreScaleMax

    const padding = 20

    min = Math.max(
      scoreScaleMin,
      min - padding
    )

    max = Math.min(
      scoreScaleMax,
      max + padding
    )

    if (min === max) {
      min -= 20
      max += 20
    }

    return {
      responsive: true,

      maintainAspectRatio: false,

      interaction: {
        intersect: false,

        mode: "index",
      },

      animation: {
        duration: 700,

        easing: "easeOutQuart",
      },

      plugins: {
        legend: {
          display: false,
        },

        tooltip: {
          displayColors: false,

          backgroundColor:
            "#0f172a",

          titleColor:
            "#cbd5e1",

          bodyColor:
            "#ffffff",

          borderColor:
            "rgba(255,255,255,0.08)",

          borderWidth: 1,

          padding: 12,

          callbacks: {
            title(items) {
              return (
                items[0]
                  ?.label || ""
              )
            },

            label(context) {
              if (
                context.datasetIndex ===
                1
              ) {
                return `${t(
                  "scoring.average"
                )}: ${Math.round(
                  context.parsed.y
                )}`
              }

              return `${t(
                "scoring.score"
              )}: ${context.parsed.y}`
            },
          },
        },
      },

      scales: {
        x: {
          grid: {
            display: false,
          },

          border: {
            display: false,
          },

          ticks: {
            color:
              "#94a3b8",

            font: {
              size: 10,
            },

            maxTicksLimit: 7,
          },
        },

        y: {
          min,

          max,

          grid: {
            color:
              "rgba(148, 163, 184, 0.12)",

            drawTicks: false,
          },

          border: {
            display: false,
          },

          ticks: {
            color:
              "#94a3b8",

            font: {
              size: 10,
            },

            padding: 8,

            precision: 0,
          },
        },
      },
    }
  })

/* ========================================================================== */
/* FORMATTING                                                                 */
/* ========================================================================== */

function formatMoney(
  value
) {
  const amount =
    Number(value || 0)

  return (
    new Intl.NumberFormat(
      currentLocale(),
      {
        maximumFractionDigits: 0,
      }
    ).format(amount) +
    " " +
    t("currency.uzs")
  )
}

function formatMoneyShort(
  value
) {
  const amount =
    Number(value || 0)

  if (
    amount >=
    1_000_000_000
  ) {
    const number =
      amount /
      1_000_000_000

    return (
      number.toFixed(
        amount %
          1_000_000_000 ===
          0
          ? 0
          : 1
      ) +
      " " +
      t("currency.uzs")
    )
  }

  if (
    amount >=
    1_000_000
  ) {
    const number =
      amount /
      1_000_000

    return (
      number.toFixed(
        amount %
          1_000_000 ===
          0
          ? 0
          : 1
      ) +
      " " +
      t("currency.uzs")
    )
  }

  if (
    amount >=
    1_000
  ) {
    const number =
      amount / 1_000

    return (
      number.toFixed(
        amount %
          1_000 ===
          0
          ? 0
          : 1
      ) +
      "K " +
      t("currency.uzs")
    )
  }

  return formatMoney(
    amount
  )
}

function formatDate(
  value
) {
  if (!value) {
    return "-"
  }

  const date =
    new Date(value)

  if (
    Number.isNaN(
      date.getTime()
    )
  ) {
    return "-"
  }

  return date.toLocaleDateString(
    currentLocale(),
    {
      day: "2-digit",
      month: "short",
      year: "numeric",
    }
  )
}

function formatHistoryDate(
  value
) {
  if (!value) {
    return "-"
  }

  const date =
    new Date(value)

  if (
    Number.isNaN(
      date.getTime()
    )
  ) {
    return "-"
  }

  return date.toLocaleDateString(
    currentLocale(),
    {
      day: "2-digit",
      month: "short",
    }
  )
}

function formatShortDate(
  value
) {
  if (!value) {
    return "-"
  }

  const date =
    new Date(value)

  if (
    Number.isNaN(
      date.getTime()
    )
  ) {
    return "-"
  }

  return date.toLocaleDateString(
    currentLocale(),
    {
      day: "2-digit",
      month: "short",
    }
  )
}

function formatTime(
  value
) {
  if (!value) {
    return "-"
  }

  const date =
    new Date(value)

  if (
    Number.isNaN(
      date.getTime()
    )
  ) {
    return "-"
  }

  return date.toLocaleTimeString(
    currentLocale(),
    {
      hour: "2-digit",
      minute: "2-digit",
    }
  )
}

function formatDateTime(
  value
) {
  if (!value) {
    return "-"
  }

  return `${formatDate(
    value
  )}, ${formatTime(value)}`
}

function formatApproval(
  value
) {
  const number =
    Number(value ?? 0)

  const percent =
    number <= 1
      ? number * 100
      : number

  return `${Math.round(
    percent
  )}%`
}

/* ========================================================================== */
/* TOAST                                                                      */
/* ========================================================================== */

let toastTimer = null

function showToastMessage(
  message,
  type = "success"
) {
  toastMessage.value =
    message

  toastType.value =
    type

  showToast.value =
    true

  clearTimeout(
    toastTimer
  )

  toastTimer =
    setTimeout(() => {
      showToast.value =
        false
    }, 3500)
}

/* ========================================================================== */
/* INIT                                                                       */
/* ========================================================================== */

onMounted(() => {
  loadData()
})
</script>

<style scoped>
/* ==========================================================================
   PAGE
   ========================================================================== */

.scoring-page {
  width: 100%;
  max-width: 1320px;
  margin: 0 auto;
  padding: 32px 32px 60px;
  color: #0f172a;
}

/* ==========================================================================
   ERROR
   ========================================================================== */

.error-banner {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 24px;
  padding: 14px 18px;
  border: 1px solid #fecaca;
  border-radius: 16px;
  background: #fff7f7;
  color: #991b1b;
}

.error-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  flex: 0 0 32px;
  border-radius: 50%;
  background: #fee2e2;
  font-weight: 800;
}

.error-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}

.error-content strong {
  font-size: 14px;
}

.error-content span {
  font-size: 13px;
  color: #b91c1c;
}

.error-close {
  border: 0;
  background: transparent;
  color: #991b1b;
  font-size: 24px;
  line-height: 1;
  cursor: pointer;
}

/* ==========================================================================
   HEADER
   ========================================================================== */

.page-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 28px;
}

.header-main {
  min-width: 0;
}

.eyebrow {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
  color: #2563eb;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.16em;
}

.eyebrow-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #2563eb;
  box-shadow:
    0 0 0 5px
    rgba(37, 99, 235, 0.1);
}

.page-header h1 {
  margin: 0;
  color: #0f172a;
  font-size: 34px;
  line-height: 1.1;
  font-weight: 800;
  letter-spacing: -0.035em;
}

.page-header p {
  margin: 9px 0 0;
  color: #64748b;
  font-size: 14px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.last-calculated {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 9px 13px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  background: #fff;
}

.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #22c55e;
  box-shadow:
    0 0 0 4px
    rgba(34, 197, 94, 0.1);
}

.last-calculated div {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.last-calculated small {
  color: #94a3b8;
  font-size: 9px;
}

.last-calculated strong {
  color: #334155;
  font-size: 11px;
}

.recalculate-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  min-height: 44px;
  padding: 0 17px;
  border: 0;
  border-radius: 12px;
  background: #2563eb;
  color: #fff;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  box-shadow:
    0 8px 22px
    rgba(37, 99, 235, 0.2);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    opacity 0.2s ease;
}

.recalculate-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow:
    0 12px 28px
    rgba(37, 99, 235, 0.26);
}

.recalculate-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.recalculate-btn svg {
  width: 16px;
  height: 16px;
}

.spinner {
  width: 15px;
  height: 15px;
  border: 2px solid
    rgba(255, 255, 255, 0.35);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* ==========================================================================
   LOADING
   ========================================================================== */

.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  min-height: 400px;
  gap: 15px;
  border: 1px solid #e2e8f0;
  border-radius: 22px;
  background: #fff;
  color: #64748b;
  font-size: 13px;
}

.loading-spinner {
  width: 35px;
  height: 35px;
  border: 3px solid #e2e8f0;
  border-top-color: #2563eb;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

/* ==========================================================================
   SCORE HERO
   ========================================================================== */

.score-hero {
  display: grid;
  grid-template-columns:
    minmax(0, 1fr)
    320px;
  overflow: hidden;
  margin-bottom: 18px;
  border: 1px solid #dbe4f0;
  border-radius: 24px;
  background:
    radial-gradient(
      circle at 85% 15%,
      rgba(59, 130, 246, 0.13),
      transparent 32%
    ),
    linear-gradient(
      135deg,
      #f8fbff 0%,
      #fff 65%
    );
  box-shadow:
    0 15px 40px
    rgba(15, 23, 42, 0.06);
}

.score-hero-main {
  padding: 30px 32px 27px;
}

.hero-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #64748b;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.13em;
  text-transform: uppercase;
}

.hero-label-icon {
  color: #2563eb;
  font-size: 15px;
}

.score-main-row {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-top: 13px;
}

.score-number {
  color: #0f172a;
  font-size: 72px;
  line-height: 0.95;
  font-weight: 850;
  letter-spacing: -0.07em;
}

.score-meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.risk-badge {
  display: inline-flex;
  align-items: center;
  align-self: flex-start;
  gap: 7px;
  padding: 7px 11px;
  border-radius: 999px;
  font-size: 10px;
  font-weight: 800;
}

.risk-dot {
  width: 7px;
  height: 7px;
  flex: 0 0 7px;
  border-radius: 50%;
  background: currentColor;
}

.risk-low {
  background: #ecfdf5;
  color: #16a34a;
}

.risk-medium {
  background: #fffbeb;
  color: #d97706;
}

.risk-high {
  background: #fef2f2;
  color: #dc2626;
}

.risk-reject {
  background: #fef2f2;
  color: #991b1b;
}

.score-description {
  max-width: 270px;
  color: #64748b;
  font-size: 12px;
  line-height: 1.5;
}

.score-progress {
  height: 8px;
  margin-top: 28px;
  overflow: hidden;
  border-radius: 999px;
  background: #e2e8f0;
}

.score-progress-fill {
  height: 100%;
  border-radius: inherit;
  background:
    linear-gradient(
      90deg,
      #60a5fa,
      #2563eb,
      #4f46e5
    );
  transition: width 0.8s ease;
}

.score-scale {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  color: #94a3b8;
  font-size: 9px;
}

.score-scale span:nth-child(2) {
  color: #64748b;
  font-weight: 700;
}

.score-hero-side {
  display: flex;
  justify-content: center;
  flex-direction: column;
  gap: 21px;
  padding: 28px;
  border-left: 1px solid #e2e8f0;
  background: rgba(255, 255, 255, 0.55);
}

.hero-stat {
  display: flex;
  flex-direction: column;
  gap: 7px;
}

.hero-stat-label {
  color: #94a3b8;
  font-size: 9px;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.hero-stat strong {
  color: #0f172a;
  font-size: 30px;
  font-weight: 800;
  letter-spacing: -0.04em;
}

.hero-stat .limit-value {
  font-size: 21px;
}

.hero-divider {
  height: 1px;
  background: #e2e8f0;
}

.mini-progress {
  height: 6px;
  overflow: hidden;
  border-radius: 999px;
  background: #e2e8f0;
}

.mini-progress-fill {
  height: 100%;
  border-radius: inherit;
  background: #22c55e;
  transition: width 0.8s ease;
}

/* ==========================================================================
   KPI
   ========================================================================== */

.kpi-grid {
  display: grid;
  grid-template-columns:
    repeat(4, minmax(0, 1fr));
  gap: 14px;
  margin-bottom: 18px;
}

.kpi-card {
  display: flex;
  align-items: center;
  gap: 13px;
  min-width: 0;
  padding: 18px;
  border: 1px solid #e2e8f0;
  border-radius: 18px;
  background: #fff;
  box-shadow:
    0 8px 25px
    rgba(15, 23, 42, 0.035);
}

.kpi-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  flex: 0 0 42px;
  border-radius: 12px;
}

.kpi-icon svg {
  width: 19px;
  height: 19px;
  stroke-width: 1.8;
}

.kpi-icon.blue {
  color: #2563eb;
  background: #eff6ff;
}

.kpi-icon.green {
  color: #16a34a;
  background: #f0fdf4;
}

.kpi-icon.purple {
  color: #7c3aed;
  background: #f5f3ff;
}

.kpi-icon.orange {
  color: #ea580c;
  background: #fff7ed;
}

.kpi-content {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.kpi-content > span {
  overflow: hidden;
  color: #64748b;
  font-size: 10px;
  font-weight: 600;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.kpi-content strong {
  margin-top: 3px;
  overflow: hidden;
  color: #0f172a;
  font-size: 20px;
  font-weight: 800;
  letter-spacing: -0.03em;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.kpi-content small {
  margin-top: 2px;
  color: #94a3b8;
  font-size: 9px;
}

.limit-kpi {
  font-size: 17px !important;
}

/* ==========================================================================
   ANALYTICS
   ========================================================================== */

.analytics-grid {
  display: grid;
  grid-template-columns:
    minmax(0, 1.35fr)
    minmax(380px, 0.65fr);
  gap: 18px;
  margin-bottom: 18px;
}

.panel {
  min-width: 0;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  background: #fff;
  box-shadow:
    0 8px 25px
    rgba(15, 23, 42, 0.035);
}

.panel-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  padding: 21px 22px 0;
}

.panel-eyebrow {
  display: block;
  margin-bottom: 5px;
  color: #94a3b8;
  font-size: 8px;
  font-weight: 800;
  letter-spacing: 0.14em;
}

.panel-header h2 {
  margin: 0;
  color: #0f172a;
  font-size: 18px;
  font-weight: 800;
  letter-spacing: -0.025em;
}

.panel-header p {
  margin: 5px 0 0;
  color: #94a3b8;
  font-size: 10px;
  line-height: 1.5;
}

/* ==========================================================================
   TREND
   ========================================================================== */

.trend-panel {
  overflow: hidden;
}

.trend-header {
  align-items: flex-start;
}

.trend-header-right {
  display: flex;
  align-items: flex-start;
}

.trend-current {
  display: flex;
  align-items: flex-end;
  flex-direction: column;
  gap: 2px;
}

.trend-current span {
  color: #94a3b8;
  font-size: 8px;
}

.trend-current strong {
  color: #2563eb;
  font-size: 25px;
  line-height: 1;
  font-weight: 850;
  letter-spacing: -0.04em;
}

.trend-current small {
  margin-top: 4px;
  font-size: 10px;
  font-weight: 800;
}

.positive {
  color: #16a34a !important;
}

.negative {
  color: #dc2626 !important;
}

.trend-controls {
  display: flex;
  justify-content: flex-end;
  gap: 4px;
  padding: 16px 22px 0;
}

.period-btn {
  min-width: 35px;
  height: 28px;
  padding: 0 9px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #fff;
  color: #94a3b8;
  font-size: 9px;
  font-weight: 800;
  cursor: pointer;
  transition:
    color 0.2s ease,
    background 0.2s ease,
    border 0.2s ease;
}

.period-btn:hover {
  border-color: #bfdbfe;
  color: #2563eb;
}

.period-btn.active {
  border-color: #2563eb;
  background: #2563eb;
  color: #fff;
}

.chart-wrapper {
  height: 285px;
  padding: 10px 18px 0;
}

.chart-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  height: 285px;
  color: #94a3b8;
}

.chart-empty span {
  color: #cbd5e1;
  font-size: 34px;
}

.chart-empty p {
  margin: 8px 0 0;
  font-size: 11px;
}

.trend-stats {
  display: grid;
  grid-template-columns:
    repeat(4, 1fr);
  margin-top: 8px;
  border-top: 1px solid #f1f5f9;
}

.trend-stat {
  display: flex;
  flex-direction: column;
  gap: 5px;
  padding: 13px 17px;
  border-right: 1px solid #f1f5f9;
}

.trend-stat:last-child {
  border-right: 0;
}

.trend-stat span {
  color: #94a3b8;
  font-size: 8px;
  font-weight: 700;
}

.trend-stat strong {
  color: #334155;
  font-size: 14px;
  font-weight: 800;
}

/* ==========================================================================
   BREAKDOWN
   ========================================================================== */

.breakdown-panel {
  overflow: hidden;
}

.model-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 27px;
  padding: 0 9px;
  border: 1px solid #dbe4f0;
  border-radius: 8px;
  background: #f8fafc;
  color: #64748b;
  font-size: 9px;
  font-weight: 800;
}

.factor-list {
  display: flex;
  flex-direction: column;
  gap: 3px;
  padding: 18px 22px 20px;
}

.factor-row {
  display: flex;
  align-items: center;
  gap: 11px;
  padding: 8px 0;
}

.factor-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 33px;
  height: 33px;
  flex: 0 0 33px;
  border-radius: 9px;
  font-size: 12px;
  font-weight: 800;
}

.factor-icon.blue {
  color: #2563eb;
  background: #eff6ff;
}

.factor-icon.green {
  color: #16a34a;
  background: #f0fdf4;
}

.factor-icon.purple {
  color: #7c3aed;
  background: #f5f3ff;
}

.factor-icon.orange {
  color: #ea580c;
  background: #fff7ed;
}

.factor-icon.cyan {
  color: #0891b2;
  background: #ecfeff;
}

.factor-info {
  min-width: 0;
  flex: 1;
}

.factor-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 6px;
}

.factor-top span {
  color: #475569;
  font-size: 11px;
  font-weight: 600;
}

.factor-top strong {
  color: #0f172a;
  font-size: 11px;
  font-weight: 800;
}

.factor-progress {
  height: 5px;
  overflow: hidden;
  border-radius: 999px;
  background: #f1f5f9;
}

.factor-progress-fill {
  height: 100%;
  border-radius: inherit;
  transition: width 0.7s ease;
}

.factor-progress-fill.blue {
  background: #3b82f6;
}

.factor-progress-fill.green {
  background: #22c55e;
}

.factor-progress-fill.purple {
  background: #8b5cf6;
}

.factor-progress-fill.orange {
  background: #f97316;
}

.factor-progress-fill.cyan {
  background: #06b6d4;
}

/* ==========================================================================
   HISTORY
   ========================================================================== */

.history-panel {
  overflow: hidden;
}

.history-header {
  align-items: center;
}

.history-badge {
  display: flex;
  align-items: baseline;
  gap: 2px;
  padding: 7px 11px;
  border: 1px solid #dbe4f0;
  border-radius: 10px;
  background: #f8fafc;
}

.history-badge strong {
  color: #2563eb;
  font-size: 14px;
  font-weight: 800;
}

.history-badge span {
  color: #94a3b8;
  font-size: 10px;
}

.history-window {
  max-height: 455px;
  margin-top: 17px;
  overflow-y: auto;
  border-top: 1px solid #f1f5f9;
}

.history-window::-webkit-scrollbar {
  width: 6px;
}

.history-window::-webkit-scrollbar-track {
  background: #f8fafc;
}

.history-window::-webkit-scrollbar-thumb {
  border-radius: 999px;
  background: #cbd5e1;
}

.history-list {
  width: 100%;
}

.history-row {
  display: grid;
  grid-template-columns:
    minmax(115px, 1.2fr)
    minmax(80px, 0.8fr)
    minmax(80px, 0.8fr)
    minmax(90px, 0.8fr)
    minmax(110px, 0.9fr);
  align-items: center;
  min-height: 65px;
  padding: 0 22px;
  border-bottom: 1px solid #f1f5f9;
  transition:
    background 0.18s ease;
}

.history-row:hover {
  background: #fafcff;
}

.history-row:last-child {
  border-bottom: 0;
}

.history-date {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.history-date strong {
  color: #334155;
  font-size: 11px;
  font-weight: 700;
}

.history-date span {
  color: #94a3b8;
  font-size: 9px;
}

.history-score,
.history-change,
.history-approval {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.history-score span,
.history-change span,
.history-approval span {
  color: #94a3b8;
  font-size: 8px;
  font-weight: 700;
}

.history-score strong {
  color: #0f172a;
  font-size: 16px;
  font-weight: 850;
}

.history-change strong,
.history-approval strong {
  font-size: 11px;
  font-weight: 800;
}

.history-risk {
  display: flex;
  justify-content: flex-start;
}

.table-risk {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 9px;
  border-radius: 999px;
  font-size: 9px;
  font-weight: 800;
}

/* ==========================================================================
   EMPTY
   ========================================================================== */

.empty-state {
  display: flex;
  align-items: center;
  flex-direction: column;
  padding: 80px 20px;
  border: 1px solid #e2e8f0;
  border-radius: 22px;
  background: #fff;
  text-align: center;
}

.empty-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 70px;
  height: 70px;
  margin-bottom: 18px;
  border-radius: 22px;
  background: #eff6ff;
  color: #2563eb;
  font-size: 35px;
}

.empty-state h2 {
  margin: 0;
  color: #0f172a;
  font-size: 21px;
}

.empty-state p {
  max-width: 430px;
  margin: 9px 0 20px;
  color: #64748b;
  font-size: 13px;
  line-height: 1.6;
}

.history-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  min-height: 180px;
  color: #94a3b8;
}

.history-empty span {
  color: #cbd5e1;
  font-size: 34px;
}

.history-empty p {
  margin: 8px 0 0;
  font-size: 11px;
}

/* ==========================================================================
   TOAST
   ========================================================================== */

.toast {
  position: fixed;
  right: 24px;
  bottom: 24px;
  z-index: 100;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 13px 17px;
  border: 1px solid #dbe4f0;
  border-radius: 13px;
  background: #fff;
  box-shadow:
    0 18px 40px
    rgba(15, 23, 42, 0.14);
  color: #334155;
  font-size: 12px;
  font-weight: 700;
}

.toast.success {
  border-color: #bbf7d0;
}

.toast.error {
  border-color: #fecaca;
}

.toast-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 23px;
  height: 23px;
  border-radius: 50%;
  background: #ecfdf5;
  color: #16a34a;
  font-size: 12px;
}

.toast.error .toast-icon {
  background: #fef2f2;
  color: #dc2626;
}

/* ==========================================================================
   TRANSITIONS
   ========================================================================== */

.fade-enter-active,
.fade-leave-active,
.toast-enter-active,
.toast-leave-active {
  transition: all 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-5px);
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

/* ==========================================================================
   RESPONSIVE
   ========================================================================== */

@media (max-width: 1150px) {
  .analytics-grid {
    grid-template-columns: 1fr;
  }

  .kpi-grid {
    grid-template-columns:
      repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 900px) {
  .scoring-page {
    padding: 24px 20px 45px;
  }

  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .header-actions {
    width: 100%;
    justify-content: space-between;
  }

  .score-hero {
    grid-template-columns: 1fr;
  }

  .score-hero-side {
    display: grid;
    grid-template-columns:
      1fr auto 1fr;
    align-items: center;
    border-top: 1px solid #e2e8f0;
    border-left: 0;
  }

  .hero-divider {
    width: 1px;
    height: 50px;
  }

  .history-row {
    grid-template-columns:
      1.2fr
      0.8fr
      0.8fr
      0.8fr;
    gap: 10px;
    padding: 14px 18px;
  }

  .history-risk {
    grid-column: 1 / -1;
  }
}

@media (max-width: 640px) {
  .scoring-page {
    padding: 18px 14px 35px;
  }

  .page-header h1 {
    font-size: 28px;
  }

  .header-actions {
    align-items: stretch;
    flex-direction: column;
  }

  .last-calculated,
  .recalculate-btn {
    width: 100%;
  }

  .score-hero-main {
    padding: 24px 20px;
  }

  .score-main-row {
    align-items: flex-start;
    flex-direction: column;
    gap: 12px;
  }

  .score-number {
    font-size: 60px;
  }

  .score-hero-side {
    display: flex;
    padding: 22px 20px;
  }

  .hero-divider {
    width: 100%;
    height: 1px;
  }

  .kpi-grid {
    grid-template-columns: 1fr;
  }

  .panel-header {
    padding-right: 17px;
    padding-left: 17px;
  }

  .trend-controls {
    padding-right: 17px;
    padding-left: 17px;
  }

  .chart-wrapper {
    height: 240px;
    padding-right: 10px;
    padding-left: 10px;
  }

  .trend-stats {
    grid-template-columns:
      repeat(2, 1fr);
  }

  .trend-stat:nth-child(2) {
    border-right: 0;
  }

  .trend-stat:nth-child(-n + 2) {
    border-bottom: 1px solid #f1f5f9;
  }

  .history-row {
    grid-template-columns:
      1fr 1fr;
    gap: 12px;
    padding: 14px 16px;
  }

  .history-date,
  .history-score,
  .history-change,
  .history-approval,
  .history-risk {
    grid-column: auto;
  }

  .history-risk {
    grid-column: 1 / -1;
  }

  .toast {
    right: 14px;
    bottom: 14px;
    left: 14px;
  }
}
</style>