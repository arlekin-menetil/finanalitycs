<script setup>
import {
  ref,
  computed,
  onMounted,
  onBeforeUnmount,
} from "vue"

import { useI18n } from "vue-i18n"
import api from "@/api/axios"

import {
  Bar,
  Line,
} from "vue-chartjs"

import "chart.js/auto"


/* =========================================================
   I18N
========================================================= */

const { t, locale } = useI18n()


/* =========================================================
   STATE
========================================================= */

const loading = ref(true)
const refreshing = ref(false)
const error = ref(null)
const lastUpdated = ref(null)

const sectionErrors = ref({
  alerts: null,
  ranking: null,
  rates: null,
  forecast: null,
  competition: null,
  recommendations: null,
})

const alerts = ref([])
const ranking = ref([])
const rates = ref([])
const forecast = ref([])

/*
 * competition = market information
 *
 * recommendations = PERSONALIZED Recommendation Engine
 *
 * approval_probability / recommended_limit used in UI
 * MUST come from recommendations.
 */
const competition = ref([])
const recommendations = ref([])

let refreshTimer = null


/* =========================================================
   ENDPOINTS
========================================================= */

const ENDPOINTS = {
  alerts: "/banks/monitoring/alerts/",
  ranking: "/banks/monitoring/digital-ranking/",
  rates: "/banks/monitoring/interest-monitor/",
  forecast: "/banks/monitoring/forecast/",
  competition: "/banks/monitoring/competition-map/",
  recommendations: "/banks/recommendations/",
}


/* =========================================================
   LOCAL TEXT
========================================================= */

const localText = {
  ru: {
    alerts: "Алерты",
    banks: "Банков",
    rates: "Ставок",
    competition: "Точек рынка",

    competitionMap: "Карта конкуренции",
    personalized: "Персональные рекомендации",

    bank: "Банк",
    product: "Продукт",
    rate: "Ставка",
    approval: "Одобрение",
    limit: "Лимит",
    score: "AI-рейтинг",

    noData: "Нет данных",
    noAlerts: "Нет активных предупреждений",
    noRanking: "Нет данных рейтинга банков",
    noRates: "Нет данных по процентным ставкам",
    noForecast: "Нет данных прогноза",
    noCompetition: "Нет данных по конкуренции",
    noRecommendations: "Нет персональных рекомендаций",

    loadError: "Не удалось загрузить данные",
    partialError: "Некоторые данные временно недоступны",

    retry: "Повторить",
    refresh: "Обновить",
    refreshing: "Обновление…",

    lastUpdated: "Обновлено",

    current: "Текущая",
    forecast30: "Прогноз 30 дней",
    forecast90: "Прогноз 90 дней",

    rateDrop: "Снижение процентной ставки",
    growth: "Рост показателя",
    rating: "Изменение рейтинга",

    unknownBank: "Неизвестный банк",
    unknownProduct: "Неизвестный продукт",

    personalizedApproval:
      "Персональное одобрение",
    personalizedLimit:
      "Персональный лимит",
  },

  en: {
    alerts: "Alerts",
    banks: "Banks",
    rates: "Rates",
    competition: "Market points",

    competitionMap: "Competition map",
    personalized: "Personal recommendations",

    bank: "Bank",
    product: "Product",
    rate: "Rate",
    approval: "Approval",
    limit: "Limit",
    score: "AI rating",

    noData: "No data",
    noAlerts: "No active alerts",
    noRanking: "No bank ranking data",
    noRates: "No interest rate data",
    noForecast: "No forecast data",
    noCompetition: "No competition data",
    noRecommendations: "No personal recommendations",

    loadError: "Failed to load data",
    partialError: "Some data is temporarily unavailable",

    retry: "Retry",
    refresh: "Refresh",
    refreshing: "Refreshing…",

    lastUpdated: "Updated",

    current: "Current",
    forecast30: "30-day forecast",
    forecast90: "90-day forecast",

    rateDrop: "Interest rate decrease",
    growth: "Indicator growth",
    rating: "Rating change",

    unknownBank: "Unknown bank",
    unknownProduct: "Unknown product",

    personalizedApproval:
      "Personal approval",
    personalizedLimit:
      "Personal limit",
  },

  uz: {
    alerts: "Ogohlantirishlar",
    banks: "Banklar",
    rates: "Stavkalar",
    competition: "Bozor nuqtalari",

    competitionMap: "Raqobat xaritasi",
    personalized: "Shaxsiy tavsiyalar",

    bank: "Bank",
    product: "Mahsulot",
    rate: "Stavka",
    approval: "Tasdiqlash",
    limit: "Limit",
    score: "AI reyting",

    noData: "Ma'lumot yo'q",
    noAlerts: "Faol ogohlantirishlar yo'q",
    noRanking: "Bank reytingi ma'lumotlari yo'q",
    noRates: "Foiz stavkalari ma'lumotlari yo'q",
    noForecast: "Prognoz ma'lumotlari yo'q",
    noCompetition: "Raqobat ma'lumotlari yo'q",
    noRecommendations:
      "Shaxsiy tavsiyalar mavjud emas",

    loadError:
      "Ma'lumotlarni yuklab bo'lmadi",

    partialError:
      "Ba'zi ma'lumotlar vaqtincha mavjud emas",

    retry: "Qayta urinish",
    refresh: "Yangilash",
    refreshing: "Yangilanmoqda…",

    lastUpdated: "Yangilandi",

    current: "Joriy",
    forecast30: "30 kunlik prognoz",
    forecast90: "90 kunlik prognoz",

    rateDrop:
      "Foiz stavkasining pasayishi",

    growth:
      "Ko'rsatkich o'sishi",

    rating:
      "Reyting o'zgarishi",

    unknownBank: "Noma'lum bank",
    unknownProduct: "Noma'lum mahsulot",

    personalizedApproval:
      "Shaxsiy tasdiqlash",

    personalizedLimit:
      "Shaxsiy limit",
  },
}

function text(key, fallback = "") {
  const lang = locale.value || "ru"

  return (
    localText[lang]?.[key] ??
    localText.ru[key] ??
    fallback
  )
}


/* =========================================================
   HELPERS
========================================================= */

function isObject(value) {
  return (
    value !== null &&
    typeof value === "object" &&
    !Array.isArray(value)
  )
}


function toNumber(value, fallback = 0) {
  if (
    value === null ||
    value === undefined ||
    value === ""
  ) {
    return fallback
  }

  if (typeof value === "number") {
    return Number.isFinite(value)
      ? value
      : fallback
  }

  const normalized = String(value)
    .replace(/\s/g, "")
    .replace(",", ".")
    .replace("%", "")

  const parsed = Number(normalized)

  return Number.isFinite(parsed)
    ? parsed
    : fallback
}


function toNullableNumber(value) {
  if (
    value === null ||
    value === undefined ||
    value === ""
  ) {
    return null
  }

  const parsed = toNumber(value, NaN)

  return Number.isFinite(parsed)
    ? parsed
    : null
}


function toStringValue(value, fallback = "") {
  if (
    value === null ||
    value === undefined
  ) {
    return fallback
  }

  return String(value).trim() || fallback
}


function clamp(
  value,
  min = 0,
  max = 100,
) {
  return Math.min(
    max,
    Math.max(
      min,
      toNumber(value, min),
    ),
  )
}


function normalizeProbability(value) {
  const number = toNullableNumber(value)

  if (number === null) {
    return null
  }

  /*
   * Backend can return:
   *
   * 0.32
   * 32
   * 32.5
   */
  if (
    number >= 0 &&
    number <= 1
  ) {
    return clamp(number * 100)
  }

  return clamp(number)
}


function formatNumber(
  value,
  maximumFractionDigits = 0,
) {
  const number = toNullableNumber(value)

  if (number === null) {
    return "—"
  }

  return new Intl.NumberFormat(
    locale.value || "ru",
    {
      maximumFractionDigits,
      minimumFractionDigits: 0,
    },
  ).format(number)
}


function formatPercent(
  value,
  maximumFractionDigits = 1,
) {
  const number = toNullableNumber(value)

  if (number === null) {
    return "—"
  }

  return `${formatNumber(
    number,
    maximumFractionDigits,
  )}%`
}


function pickFirst(
  object,
  keys,
  fallback = null,
) {
  if (!isObject(object)) {
    return fallback
  }

  for (const key of keys) {
    if (
      object[key] !== undefined &&
      object[key] !== null &&
      object[key] !== ""
    ) {
      return object[key]
    }
  }

  return fallback
}


function extractArray(
  payload,
  keys = [],
) {
  if (Array.isArray(payload)) {
    return payload
  }

  if (!isObject(payload)) {
    return []
  }

  for (const key of keys) {
    if (Array.isArray(payload[key])) {
      return payload[key]
    }
  }

  if (Array.isArray(payload.data)) {
    return payload.data
  }

  if (isObject(payload.data)) {
    for (const key of keys) {
      if (
        Array.isArray(
          payload.data[key],
        )
      ) {
        return payload.data[key]
      }
    }
  }

  return []
}


/* =========================================================
   NORMALIZERS
========================================================= */

function normalizeAlert(item) {
  if (!isObject(item)) {
    return null
  }

  const type = toStringValue(
    pickFirst(
      item,
      [
        "type",
        "alert_type",
        "category",
      ],
      "info",
    ),
    "info",
  )
    .toLowerCase()
    .replace(/\s+/g, "_")

  const rawSeverity = toStringValue(
    pickFirst(
      item,
      [
        "severity",
        "level",
        "priority",
      ],
      "low",
    ),
    "low",
  ).toLowerCase()

  let severity = "low"

  if (
    [
      "high",
      "critical",
      "danger",
    ].includes(rawSeverity)
  ) {
    severity = "high"
  } else if (
    [
      "medium",
      "warning",
      "moderate",
    ].includes(rawSeverity)
  ) {
    severity = "medium"
  }

  const bank = toStringValue(
    pickFirst(
      item,
      [
        "bank",
        "bank_name",
        "name",
      ],
      "",
    ),
  )

  const message = toStringValue(
    pickFirst(
      item,
      [
        "message",
        "text",
        "description",
        "title",
      ],
      "",
    ),
  )

  return {
    ...item,

    id:
      item.id ??
      item.alert_id ??
      `${bank}-${type}-${message}`,

    type,
    severity,

    bank:
      bank ||
      text(
        "unknownBank",
        "Неизвестный банк",
      ),

    message:
      message ||
      text(
        "rateDrop",
        "Информация",
      ),
  }
}


function normalizeRanking(item) {
  if (!isObject(item)) {
    return null
  }

  const bank = toStringValue(
    pickFirst(
      item,
      [
        "bank",
        "bank_name",
        "name",
      ],
      "",
    ),
  )

  const score = clamp(
    pickFirst(
      item,
      [
        "digital_score",
        "ranking_score",
        "score",
        "rating",
      ],
      0,
    ),
  )

  return {
    ...item,

    bank:
      bank ||
      text(
        "unknownBank",
        "Неизвестный банк",
      ),

    digital_score: score,
  }
}


function normalizeRate(item) {
  if (!isObject(item)) {
    return null
  }

  const bank = toStringValue(
    pickFirst(
      item,
      [
        "bank",
        "bank_name",
        "name",
      ],
      "",
    ),
  )

  const product = toStringValue(
    pickFirst(
      item,
      [
        "product",
        "product_name",
        "name",
        "title",
      ],
      "",
    ),
  )

  const interestRate =
    toNullableNumber(
      pickFirst(
        item,
        [
          "interest_rate",
          "rate",
          "percentage",
          "interest",
        ],
        null,
      ),
    )

  if (
    interestRate === null ||
    interestRate <= 0 ||
    interestRate > 100
  ) {
    return null
  }

  return {
    ...item,

    bank:
      bank ||
      text(
        "unknownBank",
        "Неизвестный банк",
      ),

    product:
      product ||
      text(
        "unknownProduct",
        "Неизвестный продукт",
      ),

    interest_rate: interestRate,
  }
}


function normalizeForecast(item) {
  if (!isObject(item)) {
    return null
  }

  const product = toStringValue(
    pickFirst(
      item,
      [
        "product",
        "product_name",
        "name",
        "title",
      ],
      "",
    ),
  )

  const current = toNullableNumber(
    pickFirst(
      item,
      [
        "current_avg",
        "current",
        "current_rate",
        "interest_rate",
      ],
      null,
    ),
  )

  const forecast30 =
    toNullableNumber(
      pickFirst(
        item,
        [
          "forecast_30d",
          "forecast30",
          "30d",
          "forecast_30",
        ],
        null,
      ),
    )

  const forecast90 =
    toNullableNumber(
      pickFirst(
        item,
        [
          "forecast_90d",
          "forecast90",
          "90d",
          "forecast_90",
        ],
        null,
      ),
    )

  if (
    current === null &&
    forecast30 === null &&
    forecast90 === null
  ) {
    return null
  }

  return {
    ...item,

    product:
      product ||
      text(
        "unknownProduct",
        "Неизвестный продукт",
      ),

    current_avg: current,
    forecast_30d: forecast30,
    forecast_90d: forecast90,
  }
}


/*
 * Market competition item.
 *
 * IMPORTANT:
 * We intentionally DO NOT trust its
 * approval_probability / loan_limit.
 *
 * Those values are replaced from
 * Recommendation Engine below.
 */
function normalizeCompetition(item) {
  if (!isObject(item)) {
    return null
  }

  const bank = toStringValue(
    pickFirst(
      item,
      [
        "bank",
        "bank_name",
        "name",
      ],
      "",
    ),
  )

  const product = toStringValue(
    pickFirst(
      item,
      [
        "product",
        "product_name",
        "title",
        "name",
      ],
      "",
    ),
  )

  const interestRate =
    toNullableNumber(
      pickFirst(
        item,
        [
          "interest_rate",
          "rate",
          "percentage",
        ],
        null,
      ),
    )

  return {
    ...item,

    bank:
      bank ||
      text(
        "unknownBank",
        "Неизвестный банк",
      ),

    product:
      product ||
      text(
        "unknownProduct",
        "Неизвестный продукт",
      ),

    interest_rate: interestRate,

    /*
     * Deliberately null here.
     *
     * They are filled from
     * Recommendation Engine.
     */
    approval_probability: null,
    recommended_limit: null,
    ranking_score: null,
  }
}


/*
 * Recommendation Engine normalization.
 */
function normalizeRecommendation(item) {
  if (!isObject(item)) {
    return null
  }

  const bank = toStringValue(
    pickFirst(
      item,
      [
        "bank_name",
        "bank",
        "bankName",
      ],
      "",
    ),
  )

  const product = toStringValue(
    pickFirst(
      item,
      [
        "product_name",
        "product",
        "name",
        "title",
      ],
      "",
    ),
  )

  const approval = normalizeProbability(
    pickFirst(
      item,
      [
        "approval_probability",
        "approval",
        "approval_rate",
        "probability",
      ],
      null,
    ),
  )

  const limit = toNullableNumber(
    pickFirst(
      item,
      [
        "recommended_limit",
        "loan_limit",
        "limit",
        "max_amount",
        "maximum_amount",
      ],
      null,
    ),
  )

  const rankingScore =
    toNullableNumber(
      pickFirst(
        item,
        [
          "ranking_score",
          "score",
        ],
        null,
      ),
    )

  const interestRate =
    toNullableNumber(
      pickFirst(
        item,
        [
          "interest_rate",
          "rate",
          "percentage",
        ],
        null,
      ),
    )

  return {
    ...item,

    bank:
      bank ||
      text(
        "unknownBank",
        "Неизвестный банк",
      ),

    product:
      product ||
      text(
        "unknownProduct",
        "Неизвестный продукт",
      ),

    approval_probability: approval,
    recommended_limit: limit,
    ranking_score: rankingScore,
    interest_rate: interestRate,
  }
}


/* =========================================================
   ALERT TRANSLATION
========================================================= */

function translateAlert(alert) {
  const icons = {
    rate_drop: "📉",
    growth: "📈",
    rating: "⭐",
    info: "ℹ️",
  }

  const icon =
    icons[alert?.type] ||
    icons.info

  if (alert?.message) {
    return `${icon} ${alert.message}`
  }

  const typeText = {
    rate_drop: text(
      "rateDrop",
      "Снижение процентной ставки",
    ),

    growth: text(
      "growth",
      "Рост показателя",
    ),

    rating: text(
      "rating",
      "Изменение рейтинга",
    ),
  }

  return `${icon} ${
    typeText[alert?.type] ||
    text("rateDrop", "Информация")
  }`
}


/* =========================================================
   API LOADING
========================================================= */

async function loadSection(
  name,
  request,
  extract,
  normalize,
) {
  try {
    sectionErrors.value[name] = null

    const response = await request()
    const payload =
      response?.data ?? response

    const items = extractArray(
      payload,
      extract,
    )

    return items
      .map(normalize)
      .filter(Boolean)
  } catch (err) {
    console.error(
      `Monitoring ${name} error:`,
      err,
    )

    sectionErrors.value[name] =
      err?.response?.data?.detail ||
      err?.message ||
      text(
        "loadError",
        "Не удалось загрузить данные",
      )

    return []
  }
}


/* =========================================================
   RECOMMENDATION MATCHING
========================================================= */

function normalizeKey(value) {
  return toStringValue(value)
    .toLowerCase()
    .replace(/[«»"'`]/g, "")
    .replace(/\s+/g, " ")
    .trim()
}


function findRecommendation(
  competitionItem,
) {
  const bankKey =
    normalizeKey(
      competitionItem.bank,
    )

  const productKey =
    normalizeKey(
      competitionItem.product,
    )

  /*
   * 1. Exact bank + product
   */
  let match =
    recommendations.value.find(
      item =>
        normalizeKey(item.bank) ===
          bankKey &&
        normalizeKey(item.product) ===
          productKey,
    )

  if (match) {
    return match
  }

  /*
   * 2. Exact product.
   *
   * Useful if bank names differ slightly.
   */
  match =
    recommendations.value.find(
      item =>
        normalizeKey(item.product) ===
        productKey,
    )

  if (match) {
    return match
  }

  /*
   * 3. Product substring match.
   *
   * We only use it when the product
   * names are sufficiently long.
   */
  if (productKey.length >= 8) {
    match =
      recommendations.value.find(
        item => {
          const itemProduct =
            normalizeKey(
              item.product,
            )

          return (
            itemProduct.includes(productKey) ||
            productKey.includes(itemProduct)
          )
        },
      )
  }

  return match || null
}


/*
 * Merge market data + personalized
 * Recommendation Engine data.
 */
function mergePersonalizedData(
  marketItems,
) {
  return marketItems.map(item => {
    const recommendation =
      findRecommendation(item)

    if (!recommendation) {
      return {
        ...item,

        /*
         * Do NOT invent values.
         */
        approval_probability: null,
        recommended_limit: null,
        ranking_score: null,
        personalized: false,
      }
    }

    return {
      ...item,

      approval_probability:
        recommendation.approval_probability,

      recommended_limit:
        recommendation.recommended_limit,

      ranking_score:
        recommendation.ranking_score,

      personalized: true,

      /*
       * Keep recommendation fields
       * available for debugging/details.
       */
      recommendation,
    }
  })
}


/* =========================================================
   LOAD MONITORING
========================================================= */

async function loadMonitoring(
  options = {},
) {
  const silent =
    options.silent === true

  if (silent) {
    refreshing.value = true
  } else {
    loading.value = true
  }

  error.value = null

  sectionErrors.value = {
    alerts: null,
    ranking: null,
    rates: null,
    forecast: null,
    competition: null,
    recommendations: null,
  }

  try {
    /*
     * Every endpoint is independent.
     */
    const [
      alertsResult,
      rankingResult,
      ratesResult,
      forecastResult,
      competitionResult,
      recommendationsResult,
    ] = await Promise.all([
      loadSection(
        "alerts",
        () =>
          api.get(
            ENDPOINTS.alerts,
          ),
        [
          "alerts",
          "data",
          "results",
        ],
        normalizeAlert,
      ),

      loadSection(
        "ranking",
        () =>
          api.get(
            ENDPOINTS.ranking,
          ),
        [
          "ranking",
          "digital_ranking",
          "data",
          "results",
        ],
        normalizeRanking,
      ),

      loadSection(
        "rates",
        () =>
          api.get(
            ENDPOINTS.rates,
          ),
        [
          "interest_monitor",
          "interest_rates",
          "rates",
          "data",
          "results",
        ],
        normalizeRate,
      ),

      loadSection(
        "forecast",
        () =>
          api.get(
            ENDPOINTS.forecast,
          ),
        [
          "forecast",
          "forecasts",
          "data",
          "results",
        ],
        normalizeForecast,
      ),

      loadSection(
        "competition",
        () =>
          api.get(
            ENDPOINTS.competition,
          ),
        [
          "competition_map",
          "competition",
          "data",
          "results",
        ],
        normalizeCompetition,
      ),

      loadSection(
        "recommendations",
        () =>
          api.get(
            ENDPOINTS.recommendations,
          ),
        [
          "recommendations",
          "products",
          "data",
          "results",
        ],
        normalizeRecommendation,
      ),
    ])

    alerts.value = alertsResult
    ranking.value = rankingResult
    rates.value = ratesResult
    forecast.value = forecastResult
    recommendations.value =
      recommendationsResult

    /*
     * THIS IS THE IMPORTANT PART.
     *
     * Market competition data is merged
     * with personalized Recommendation Engine
     * data.
     */
    competition.value =
      mergePersonalizedData(
        competitionResult,
      )

    const hasAnyData =
      alerts.value.length > 0 ||
      ranking.value.length > 0 ||
      rates.value.length > 0 ||
      forecast.value.length > 0 ||
      competition.value.length > 0 ||
      recommendations.value.length > 0

    const hasErrors =
      Object.values(
        sectionErrors.value,
      ).some(Boolean)

    if (!hasAnyData && hasErrors) {
      error.value = text(
        "loadError",
        "Не удалось загрузить данные",
      )
    } else if (hasErrors) {
      error.value = text(
        "partialError",
        "Некоторые данные временно недоступны",
      )
    } else {
      error.value = null
    }

    lastUpdated.value = new Date()
  } catch (err) {
    console.error(
      "Monitoring load error:",
      err,
    )

    error.value =
      err?.response?.data?.detail ||
      err?.message ||
      text(
        "loadError",
        "Не удалось загрузить данные",
      )
  } finally {
    loading.value = false
    refreshing.value = false
  }
}


/* =========================================================
   REFRESH
========================================================= */

async function refreshMonitoring() {
  await loadMonitoring({
    silent: true,
  })
}


/* =========================================================
   AUTO REFRESH
========================================================= */

function startAutoRefresh() {
  stopAutoRefresh()

  refreshTimer =
    window.setInterval(
      () => {
        refreshMonitoring()
      },
      5 * 60 * 1000,
    )
}


function stopAutoRefresh() {
  if (refreshTimer) {
    window.clearInterval(
      refreshTimer,
    )

    refreshTimer = null
  }
}


/* =========================================================
   KPI
========================================================= */

const monitoringStats = computed(
  () => ({
    alerts:
      alerts.value.length,

    banks:
      ranking.value.length,

    products:
      rates.value.length,

    competition:
      competition.value.length,
  }),
)


const hasAnyMonitoringData =
  computed(() =>
    monitoringStats.value.alerts > 0 ||
    monitoringStats.value.banks > 0 ||
    monitoringStats.value.products > 0 ||
    monitoringStats.value.competition > 0 ||
    forecast.value.length > 0 ||
    recommendations.value.length > 0,
  )


const hasPartialErrors =
  computed(() =>
    Object.values(
      sectionErrors.value,
    ).some(Boolean),
  )


/* =========================================================
   TOP RATES
========================================================= */

const topRates = computed(() =>
  [...rates.value]
    .filter(
      item =>
        toNumber(
          item.interest_rate,
          0,
        ) > 0,
    )
    .sort(
      (a, b) =>
        toNumber(
          b.interest_rate,
          0,
        ) -
        toNumber(
          a.interest_rate,
          0,
        ),
    )
    .slice(0, 15),
)


/* =========================================================
   TOP RANKING
========================================================= */

const topRanking = computed(() =>
  [...ranking.value]
    .sort(
      (a, b) =>
        toNumber(
          b.digital_score,
          0,
        ) -
        toNumber(
          a.digital_score,
          0,
        ),
    )
    .slice(0, 15),
)


/* =========================================================
   PERSONALIZED COMPETITION
========================================================= */

const topCompetition = computed(() =>
  [...competition.value]
    .sort((a, b) => {
      const approvalA =
        toNumber(
          a.approval_probability,
          -1,
        )

      const approvalB =
        toNumber(
          b.approval_probability,
          -1,
        )

      if (
        approvalB !== approvalA
      ) {
        return (
          approvalB -
          approvalA
        )
      }

      const scoreA =
        toNumber(
          a.ranking_score,
          -1,
        )

      const scoreB =
        toNumber(
          b.ranking_score,
          -1,
        )

      if (
        scoreB !== scoreA
      ) {
        return scoreB - scoreA
      }

      return (
        toNumber(
          a.interest_rate,
          999,
        ) -
        toNumber(
          b.interest_rate,
          999,
        )
      )
    })
    .slice(0, 20),
)


/* =========================================================
   ALERT COUNTS
========================================================= */

const alertCounts = computed(() => {
  const result = {
    high: 0,
    medium: 0,
    low: 0,
  }

  for (
    const alert of alerts.value
  ) {
    if (
      Object.prototype.hasOwnProperty.call(
        result,
        alert.severity,
      )
    ) {
      result[
        alert.severity
      ]++
    }
  }

  return result
})


/* =========================================================
   CHART OPTIONS
========================================================= */

const chartOptions = computed(
  () => ({
    responsive: true,

    maintainAspectRatio: false,

    animation: {
      duration: 500,
    },

    plugins: {
      legend: {
        position: "top",

        labels: {
          usePointStyle: true,
          boxWidth: 10,
          padding: 16,
        },
      },

      tooltip: {
        intersect: false,
        mode: "index",
      },
    },

    interaction: {
      intersect: false,
      mode: "index",
    },

    scales: {
      x: {
        ticks: {
          maxRotation: 45,
          minRotation: 0,
          autoSkip: true,
          maxTicksLimit: 12,
        },

        grid: {
          display: false,
        },
      },

      y: {
        beginAtZero: true,

        ticks: {
          precision: 0,
        },

        grid: {
          color:
            "rgba(148,163,184,0.15)",
        },
      },
    },
  }),
)


/* =========================================================
   RANKING CHART
========================================================= */

const rankingChart = computed(
  () => ({
    labels:
      topRanking.value.map(
        item =>
          item.bank ||
          text(
            "unknownBank",
            "Неизвестный банк",
          ),
      ),

    datasets: [
      {
        label:
          t(
            "analytics.rankingScores",
            "Digital score",
          ),

        data:
          topRanking.value.map(
            item =>
              clamp(
                item.digital_score,
              ),
          ),

        backgroundColor:
          "rgba(37, 99, 235, 0.75)",

        borderColor:
          "rgba(37, 99, 235, 1)",

        borderWidth: 1,
        borderRadius: 8,
      },
    ],
  }),
)


/* =========================================================
   INTEREST CHART
========================================================= */

const interestChart = computed(
  () => ({
    labels:
      topRates.value.map(
        item =>
          item.bank ||
          text(
            "unknownBank",
            "Неизвестный банк",
          ),
      ),

    datasets: [
      {
        label:
          t(
            "analytics.interestRates",
            text(
              "rates",
              "Ставки",
            ),
          ),

        data:
          topRates.value.map(
            item =>
              toNumber(
                item.interest_rate,
                0,
              ),
          ),

        backgroundColor:
          "rgba(16, 185, 129, 0.75)",

        borderColor:
          "rgba(16, 185, 129, 1)",

        borderWidth: 1,
        borderRadius: 8,
      },
    ],
  }),
)


/* =========================================================
   FORECAST CHART
========================================================= */

const forecastChart = computed(
  () => ({
    labels:
      forecast.value.map(
        item =>
          item.product ||
          text(
            "unknownProduct",
            "Неизвестный продукт",
          ),
      ),

    datasets: [
      {
        label:
          t(
            "analytics.current",
            text(
              "current",
              "Текущая",
            ),
          ),

        data:
          forecast.value.map(
            item =>
              toNumber(
                item.current_avg,
                0,
              ),
          ),

        borderColor: "#3b82f6",
        backgroundColor:
          "rgba(59, 130, 246, 0.08)",

        tension: 0.3,
        fill: false,

        pointRadius: 3,
        pointHoverRadius: 5,
      },

      {
        label:
          t(
            "analytics.forecast30",
            text(
              "forecast30",
              "Прогноз 30 дней",
            ),
          ),

        data:
          forecast.value.map(
            item =>
              toNumber(
                item.forecast_30d,
                0,
              ),
          ),

        borderColor: "#f59e0b",
        backgroundColor:
          "rgba(245, 158, 11, 0.08)",

        tension: 0.3,
        fill: false,

        pointRadius: 3,
        pointHoverRadius: 5,
      },

      {
        label:
          t(
            "analytics.forecast90",
            text(
              "forecast90",
              "Прогноз 90 дней",
            ),
          ),

        data:
          forecast.value.map(
            item =>
              toNumber(
                item.forecast_90d,
                0,
              ),
          ),

        borderColor: "#ef4444",
        backgroundColor:
          "rgba(239, 68, 68, 0.08)",

        tension: 0.3,
        fill: false,

        pointRadius: 3,
        pointHoverRadius: 5,
      },
    ],
  }),
)


/* =========================================================
   LAST UPDATED
========================================================= */

const formattedLastUpdated =
  computed(() => {
    if (!lastUpdated.value) {
      return ""
    }

    return new Intl.DateTimeFormat(
      locale.value || "ru",
      {
        dateStyle: "short",
        timeStyle: "short",
      },
    ).format(
      lastUpdated.value,
    )
  })


/* =========================================================
   LIFECYCLE
========================================================= */

onMounted(async () => {
  await loadMonitoring()
  startAutoRefresh()
})


onBeforeUnmount(() => {
  stopAutoRefresh()
})
</script>


<template>
  <section class="monitoring">

    <!-- HEADER -->
    <header class="monitoring-header">
      <div>
        <h1>
          {{
            $t(
              "analytics.marketMonitoring",
              "Market Monitoring",
            )
          }}
        </h1>

        <p
          v-if="formattedLastUpdated"
          class="last-updated"
        >
          {{ text("lastUpdated", "Обновлено") }}:
          {{ formattedLastUpdated }}
        </p>
      </div>

      <button
        class="refresh-button"
        type="button"
        :disabled="refreshing"
        @click="refreshMonitoring"
      >
        <span
          class="refresh-icon"
          :class="{
            spinning: refreshing,
          }"
        >
          ↻
        </span>

        {{
          refreshing
            ? text(
                "refreshing",
                "Обновление…",
              )
            : text(
                "refresh",
                "Обновить",
              )
        }}
      </button>
    </header>


    <!-- LOADING -->
    <div
      v-if="loading"
      class="loading-state"
    >
      <div class="loading-spinner"></div>

      <div>
        {{
          $t(
            "analytics.loading",
            "Загрузка мониторинга...",
          )
        }}
      </div>
    </div>


    <!-- GLOBAL ERROR -->
    <div
      v-else-if="
        error &&
        !hasAnyMonitoringData
      "
      class="error-state"
    >
      <div class="error-icon">
        ⚠️
      </div>

      <h3>
        {{ error }}
      </h3>

      <button
        type="button"
        class="retry-button"
        @click="loadMonitoring"
      >
        {{
          text(
            "retry",
            "Повторить",
          )
        }}
      </button>
    </div>


    <!-- CONTENT -->
    <div
      v-else
      class="monitoring-content"
    >

      <!-- PARTIAL ERROR -->
      <div
        v-if="
          hasPartialErrors &&
          hasAnyMonitoringData
        "
        class="partial-warning"
      >
        <span>⚠️</span>

        <span>
          {{
            text(
              "partialError",
              "Некоторые данные временно недоступны",
            )
          }}
        </span>

        <button
          type="button"
          @click="refreshMonitoring"
        >
          {{
            text(
              "retry",
              "Повторить",
            )
          }}
        </button>
      </div>


      <!-- KPI -->
      <div class="stats">

        <div class="stat-card">
          <div
            class="stat-icon alert-icon"
          >
            ⚠️
          </div>

          <strong>
            {{ monitoringStats.alerts }}
          </strong>

          <small>
            {{
              text(
                "alerts",
                "Алертов",
              )
            }}
          </small>

          <div
            v-if="alerts.length"
            class="stat-meta"
          >
            <span>
              🔴 {{ alertCounts.high }}
            </span>

            <span>
              🟠 {{ alertCounts.medium }}
            </span>

            <span>
              🔵 {{ alertCounts.low }}
            </span>
          </div>
        </div>


        <div class="stat-card">
          <div
            class="stat-icon bank-icon"
          >
            🏦
          </div>

          <strong>
            {{ monitoringStats.banks }}
          </strong>

          <small>
            {{
              text(
                "banks",
                "Банков",
              )
            }}
          </small>
        </div>


        <div class="stat-card">
          <div
            class="stat-icon rate-icon"
          >
            📈
          </div>

          <strong>
            {{ monitoringStats.products }}
          </strong>

          <small>
            {{
              text(
                "rates",
                "Ставок",
              )
            }}
          </small>
        </div>


        <div class="stat-card">
          <div
            class="stat-icon competition-icon"
          >
            🎯
          </div>

          <strong>
            {{ monitoringStats.competition }}
          </strong>

          <small>
            {{
              text(
                "competition",
                "Точек рынка",
              )
            }}
          </small>
        </div>

      </div>


      <!-- ALERTS -->
      <section class="section">

        <div class="section-heading">
          <h2>
            ⚠️
            {{
              text(
                "alerts",
                "Алерты",
              )
            }}
          </h2>

          <span
            v-if="alerts.length"
            class="section-count"
          >
            {{ alerts.length }}
          </span>
        </div>


        <div
          v-if="alerts.length"
          class="alerts"
        >
          <article
            v-for="alert in alerts"
            :key="alert.id"
            class="alert"
            :class="alert.severity"
          >
            <div class="alert-top">
              <strong>
                {{ alert.bank }}
              </strong>

              <span
                class="severity-badge"
              >
                {{ alert.severity }}
              </span>
            </div>

            <p>
              {{ translateAlert(alert) }}
            </p>
          </article>
        </div>


        <div
          v-else
          class="empty-block"
        >
          <span>🔔</span>

          <p>
            {{
              text(
                "noAlerts",
                "Нет активных предупреждений",
              )
            }}
          </p>
        </div>

      </section>


      <!-- GRID -->
      <div class="grid">

        <!-- DIGITAL RANKING -->
        <section class="card">

          <div class="card-header">
            <div>
              <h3>
                {{
                  $t(
                    "analytics.digitalRanking",
                    "Digital ranking",
                  )
                }}
              </h3>

              <p>
                {{ topRanking.length }}
              </p>
            </div>

            <span class="card-icon">
              🏦
            </span>
          </div>


          <div
            v-if="topRanking.length"
            class="chart"
          >
            <Bar
              :data="rankingChart"
              :options="chartOptions"
            />
          </div>


          <div
            v-else
            class="chart-empty"
          >
            <span>📊</span>

            <p>
              {{
                text(
                  "noRanking",
                  "Нет данных рейтинга банков",
                )
              }}
            </p>
          </div>

        </section>


        <!-- INTEREST MONITOR -->
        <section class="card">

          <div class="card-header">
            <div>
              <h3>
                {{
                  $t(
                    "analytics.interestMonitor",
                    "Interest monitor",
                  )
                }}
              </h3>

              <p>
                {{ topRates.length }}
              </p>
            </div>

            <span class="card-icon">
              📈
            </span>
          </div>


          <div
            v-if="topRates.length"
            class="chart"
          >
            <Bar
              :data="interestChart"
              :options="chartOptions"
            />
          </div>


          <div
            v-else
            class="chart-empty"
          >
            <span>📈</span>

            <p>
              {{
                text(
                  "noRates",
                  "Нет данных по процентным ставкам",
                )
              }}
            </p>
          </div>

        </section>


        <!-- FORECAST -->
        <section class="card wide">

          <div class="card-header">
            <div>
              <h3>
                {{
                  $t(
                    "analytics.marketForecast",
                    "Market forecast",
                  )
                }}
              </h3>

              <p>
                {{ forecast.length }}
              </p>
            </div>

            <span class="card-icon">
              🔮
            </span>
          </div>


          <div
            v-if="forecast.length"
            class="chart forecast-chart"
          >
            <Line
              :data="forecastChart"
              :options="chartOptions"
            />
          </div>


          <div
            v-else
            class="chart-empty"
          >
            <span>🔮</span>

            <p>
              {{
                text(
                  "noForecast",
                  "Нет данных прогноза",
                )
              }}
            </p>
          </div>

        </section>


        <!-- PERSONALIZED COMPETITION -->
        <section class="card wide">

          <div class="card-header">

            <div>
              <h3>
                🏆
                {{
                  text(
                    "competitionMap",
                    "Карта конкуренции",
                  )
                }}
              </h3>

              <p>
                {{
                  text(
                    "personalized",
                    "Персональные рекомендации",
                  )
                }}
              </p>
            </div>

            <span class="card-icon">
              🎯
            </span>

          </div>


          <div
            v-if="topCompetition.length"
            class="competition-table"
          >
            <table>

              <thead>
                <tr>
                  <th>
                    {{
                      text(
                        "bank",
                        "Банк",
                      )
                    }}
                  </th>

                  <th>
                    {{
                      text(
                        "product",
                        "Продукт",
                      )
                    }}
                  </th>

                  <th>
                    {{
                      text(
                        "rate",
                        "Ставка",
                      )
                    }}
                  </th>

                  <th>
                    {{
                      text(
                        "approval",
                        "Одобрение",
                      )
                    }}
                  </th>

                  <th>
                    {{
                      text(
                        "limit",
                        "Лимит",
                      )
                    }}
                  </th>

                  <th>
                    {{
                      text(
                        "score",
                        "AI-рейтинг",
                      )
                    }}
                  </th>
                </tr>
              </thead>


              <tbody>

                <tr
                  v-for="(
                    item,
                    index
                  ) in topCompetition"
                  :key="
                    `competition-${index}-${item.bank}-${item.product}`
                  "
                >

                  <td>
                    <strong>
                      {{ item.bank }}
                    </strong>
                  </td>


                  <td>
                    <span
                      class="product-name"
                      :title="item.product"
                    >
                      {{ item.product }}
                    </span>
                  </td>


                  <td>
                    <span
                      v-if="
                        item.interest_rate !==
                        null
                      "
                      class="rate-value"
                    >
                      {{
                        formatPercent(
                          item.interest_rate,
                          2,
                        )
                      }}
                    </span>

                    <span
                      v-else
                      class="muted"
                    >
                      —
                    </span>
                  </td>


                  <!--
                    IMPORTANT:
                    This value is from
                    Recommendation Engine.
                  -->
                  <td>
                    <span
                      v-if="
                        item.approval_probability !==
                        null
                      "
                      class="approval-value"
                    >
                      {{
                        formatPercent(
                          item.approval_probability,
                          1,
                        )
                      }}
                    </span>

                    <span
                      v-else
                      class="muted"
                    >
                      —
                    </span>
                  </td>


                  <!--
                    IMPORTANT:
                    This value is from
                    Recommendation Engine.
                  -->
                  <td>
                    <span
                      v-if="
                        item.recommended_limit !==
                        null
                      "
                      class="limit-value"
                    >
                      {{
                        formatNumber(
                          item.recommended_limit,
                        )
                      }}
                      UZS
                    </span>

                    <span
                      v-else
                      class="muted"
                    >
                      —
                    </span>
                  </td>


                  <td>
                    <span
                      v-if="
                        item.ranking_score !==
                        null
                      "
                      class="score-value"
                    >
                      {{
                        formatNumber(
                          item.ranking_score,
                          1,
                        )
                      }}
                    </span>

                    <span
                      v-else
                      class="muted"
                    >
                      —
                    </span>
                  </td>

                </tr>

              </tbody>

            </table>
          </div>


          <div
            v-else
            class="chart-empty"
          >
            <span>🎯</span>

            <p>
              {{
                text(
                  "noCompetition",
                  "Нет данных по конкуренции",
                )
              }}
            </p>
          </div>

        </section>

      </div>


      <!-- GLOBAL EMPTY -->
      <div
        v-if="
          !hasAnyMonitoringData
        "
        class="global-empty"
      >
        <div
          class="global-empty-icon"
        >
          📊
        </div>

        <h3>
          {{
            text(
              "noData",
              "Нет данных",
            )
          }}
        </h3>

        <p>
          {{
            text(
              "loadError",
              "Не удалось загрузить данные",
            )
          }}
        </p>

        <button
          type="button"
          class="retry-button"
          @click="loadMonitoring"
        >
          {{
            text(
              "retry",
              "Повторить",
            )
          }}
        </button>
      </div>

    </div>

  </section>
</template>


<style scoped>

/* =========================================================
   PAGE
========================================================= */

.monitoring {
  min-height: 100vh;
  padding: 24px;

  background:
    linear-gradient(
      180deg,
      #f8fafc 0%,
      #f1f5f9 100%
    );

  color: #0f172a;
}


/* =========================================================
   HEADER
========================================================= */

.monitoring-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;

  gap: 20px;
  margin-bottom: 24px;
}

.monitoring h1 {
  margin: 0;

  font-size: 32px;
  line-height: 1.2;

  font-weight: 800;
  letter-spacing: -0.02em;

  color: #0f172a;
}

.last-updated {
  margin: 7px 0 0;

  color: #64748b;
  font-size: 13px;
}


/* =========================================================
   BUTTONS
========================================================= */

.refresh-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;

  gap: 8px;

  min-height: 42px;
  padding: 0 16px;

  border: 1px solid #dbeafe;
  border-radius: 12px;

  background: #fff;
  color: #1d4ed8;

  font-size: 14px;
  font-weight: 700;

  cursor: pointer;

  transition:
    transform .2s ease,
    box-shadow .2s ease,
    background .2s ease;
}

.refresh-button:hover:not(:disabled) {
  transform: translateY(-1px);

  background: #eff6ff;

  box-shadow:
    0 8px 20px
    rgba(37, 99, 235, .10);
}

.refresh-button:disabled {
  opacity: .65;
  cursor: not-allowed;
}

.refresh-icon {
  display: inline-flex;
  font-size: 18px;
  line-height: 1;
}

.refresh-icon.spinning {
  animation:
    monitoring-spin
    .8s
    linear
    infinite;
}


/* =========================================================
   LOADING / ERROR
========================================================= */

.loading-state {
  min-height: 360px;

  display: flex;
  flex-direction: column;

  align-items: center;
  justify-content: center;

  gap: 16px;

  color: #64748b;
  font-size: 16px;
}

.loading-spinner {
  width: 42px;
  height: 42px;

  border: 4px solid #dbeafe;
  border-top-color: #2563eb;

  border-radius: 50%;

  animation:
    monitoring-spin
    .8s
    linear
    infinite;
}

.error-state {
  min-height: 320px;

  display: flex;
  flex-direction: column;

  align-items: center;
  justify-content: center;

  gap: 12px;

  padding: 40px;

  text-align: center;

  border: 1px solid #fecaca;
  border-radius: 20px;

  background: #fff7f7;
  color: #991b1b;
}

.error-icon {
  font-size: 42px;
}

.error-state h3 {
  margin: 0;
  font-size: 18px;
}

.retry-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;

  min-height: 40px;
  padding: 0 16px;

  border: 0;
  border-radius: 10px;

  background: #2563eb;
  color: #fff;

  font-size: 14px;
  font-weight: 700;

  cursor: pointer;

  transition:
    transform .2s ease,
    background .2s ease;
}

.retry-button:hover {
  background: #1d4ed8;
  transform: translateY(-1px);
}


/* =========================================================
   CONTENT
========================================================= */

.monitoring-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}


/* =========================================================
   PARTIAL WARNING
========================================================= */

.partial-warning {
  display: flex;
  align-items: center;

  gap: 10px;

  padding: 12px 16px;

  border: 1px solid #fde68a;
  border-radius: 12px;

  background: #fffbeb;
  color: #92400e;

  font-size: 14px;
  font-weight: 600;
}

.partial-warning button {
  margin-left: auto;

  border: 0;
  background: transparent;

  color: #92400e;

  font-weight: 800;
  cursor: pointer;

  text-decoration: underline;
}


/* =========================================================
   KPI
========================================================= */

.stats {
  display: grid;

  grid-template-columns:
    repeat(4, minmax(0, 1fr));

  gap: 18px;
}

.stat-card {
  min-width: 0;

  padding: 22px;

  border:
    1px solid
    rgba(226, 232, 240, .9);

  border-radius: 18px;

  background: #fff;

  box-shadow:
    0 5px 18px
    rgba(15, 23, 42, .05);

  text-align: center;

  transition:
    transform .2s ease,
    box-shadow .2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);

  box-shadow:
    0 12px 28px
    rgba(15, 23, 42, .08);
}

.stat-icon {
  display: inline-flex;

  align-items: center;
  justify-content: center;

  width: 46px;
  height: 46px;

  margin-bottom: 8px;

  border-radius: 14px;

  font-size: 24px;
}

.alert-icon {
  background: #fff7ed;
}

.bank-icon {
  background: #eff6ff;
}

.rate-icon {
  background: #ecfdf5;
}

.competition-icon {
  background: #fef3c7;
}

.stat-card strong {
  display: block;

  margin-top: 4px;

  font-size: 30px;
  line-height: 1;

  font-weight: 800;

  color: #0f172a;
}

.stat-card small {
  display: block;

  margin-top: 8px;

  color: #64748b;

  font-size: 13px;
  font-weight: 600;
}

.stat-meta {
  display: flex;
  justify-content: center;

  gap: 10px;

  margin-top: 12px;

  color: #64748b;
  font-size: 12px;
}


/* =========================================================
   SECTIONS
========================================================= */

.section {
  width: 100%;
}

.section-heading {
  display: flex;
  align-items: center;

  gap: 10px;
  margin-bottom: 12px;
}

.section-heading h2 {
  margin: 0;

  font-size: 20px;
  font-weight: 800;

  color: #0f172a;
}

.section-count {
  display: inline-flex;

  align-items: center;
  justify-content: center;

  min-width: 26px;
  height: 26px;

  padding: 0 7px;

  border-radius: 999px;

  background: #e0e7ff;
  color: #3730a3;

  font-size: 12px;
  font-weight: 800;
}


/* =========================================================
   ALERTS
========================================================= */

.alerts {
  display: grid;

  grid-template-columns:
    repeat(
      auto-fit,
      minmax(260px, 1fr)
    );

  gap: 14px;
}

.alert {
  min-width: 0;

  padding: 16px 18px;

  border-radius: 16px;

  color: #fff;

  box-shadow:
    0 6px 16px
    rgba(15, 23, 42, .08);
}

.alert.low {
  background:
    linear-gradient(
      135deg,
      #2563eb,
      #3b82f6
    );
}

.alert.medium {
  background:
    linear-gradient(
      135deg,
      #d97706,
      #f59e0b
    );
}

.alert.high {
  background:
    linear-gradient(
      135deg,
      #dc2626,
      #ef4444
    );
}

.alert-top {
  display: flex;
  align-items: center;
  justify-content: space-between;

  gap: 10px;
}

.alert strong {
  min-width: 0;

  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;

  font-size: 15px;
}

.alert p {
  margin: 8px 0 0;

  font-size: 13px;
  line-height: 1.5;

  opacity: .95;
}

.severity-badge {
  flex-shrink: 0;

  padding: 3px 7px;

  border-radius: 999px;

  background:
    rgba(255, 255, 255, .18);

  font-size: 10px;
  font-weight: 800;

  text-transform: uppercase;
}


/* =========================================================
   EMPTY
========================================================= */

.empty-block {
  min-height: 130px;

  display: flex;
  flex-direction: column;

  align-items: center;
  justify-content: center;

  gap: 8px;

  padding: 20px;

  border:
    1px dashed
    #cbd5e1;

  border-radius: 16px;

  background:
    rgba(255, 255, 255, .65);

  color: #64748b;

  text-align: center;
}

.empty-block span {
  font-size: 26px;
}

.empty-block p {
  margin: 0;
  font-size: 14px;
}


/* =========================================================
   GRID
========================================================= */

.grid {
  display: grid;

  grid-template-columns:
    repeat(2, minmax(0, 1fr));

  gap: 22px;
}

.card {
  min-width: 0;

  padding: 22px;

  border:
    1px solid
    rgba(226, 232, 240, .9);

  border-radius: 18px;

  background: #fff;

  box-shadow:
    0 5px 18px
    rgba(15, 23, 42, .05);
}

.card.wide {
  grid-column: span 2;
}

.card-header {
  display: flex;
  align-items: flex-start;

  justify-content: space-between;

  gap: 15px;

  margin-bottom: 16px;
}

.card-header h3 {
  margin: 0;

  color: #0f172a;

  font-size: 18px;
  font-weight: 800;
}

.card-header p {
  margin: 5px 0 0;

  color: #64748b;

  font-size: 12px;
  font-weight: 600;
}

.card-icon {
  display: inline-flex;

  align-items: center;
  justify-content: center;

  width: 40px;
  height: 40px;

  flex-shrink: 0;

  border-radius: 12px;

  background: #f8fafc;

  font-size: 20px;
}


/* =========================================================
   CHART
========================================================= */

.chart {
  width: 100%;
  height: 360px;

  position: relative;
}

.forecast-chart {
  height: 390px;
}

.chart-empty {
  min-height: 360px;

  display: flex;
  flex-direction: column;

  align-items: center;
  justify-content: center;

  gap: 10px;

  border:
    1px dashed
    #cbd5e1;

  border-radius: 14px;

  background: #f8fafc;

  color: #64748b;

  text-align: center;
}

.chart-empty span {
  font-size: 32px;
}

.chart-empty p {
  margin: 0;

  max-width: 300px;

  font-size: 14px;
}


/* =========================================================
   COMPETITION TABLE
========================================================= */

.competition-table {
  width: 100%;

  overflow-x: auto;

  border:
    1px solid
    #e2e8f0;

  border-radius: 14px;
}

.competition-table table {
  width: 100%;

  min-width: 900px;

  border-collapse: collapse;
}

.competition-table thead {
  background: #f8fafc;
}

.competition-table th {
  padding: 13px 14px;

  text-align: left;

  white-space: nowrap;

  border-bottom:
    2px solid
    #e2e8f0;

  color: #334155;

  font-size: 12px;
  font-weight: 800;

  text-transform: uppercase;
  letter-spacing: .02em;
}

.competition-table td {
  padding: 14px;

  border-bottom:
    1px solid
    #e2e8f0;

  color: #334155;

  font-size: 14px;

  vertical-align: middle;
}

.competition-table tbody tr {
  transition:
    background .2s ease;
}

.competition-table tbody tr:last-child td {
  border-bottom: 0;
}

.competition-table tbody tr:hover {
  background: #f8fafc;
}

.product-name {
  display: inline-block;

  max-width: 360px;

  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;

  color: #475569;
}

.rate-value {
  font-weight: 800;
  color: #dc2626;
}

.approval-value {
  font-weight: 800;
  color: #059669;
}

.limit-value {
  font-weight: 700;
  color: #1d4ed8;
}

.score-value {
  font-weight: 800;
  color: #7c3aed;
}

.muted {
  color: #94a3b8;
}


/* =========================================================
   GLOBAL EMPTY
========================================================= */

.global-empty {
  min-height: 280px;

  display: flex;
  flex-direction: column;

  align-items: center;
  justify-content: center;

  gap: 10px;

  padding: 40px;

  border:
    1px dashed
    #cbd5e1;

  border-radius: 18px;

  background:
    rgba(255, 255, 255, .7);

  text-align: center;
}

.global-empty-icon {
  font-size: 48px;
}

.global-empty h3 {
  margin: 0;

  color: #0f172a;

  font-size: 20px;
}

.global-empty p {
  margin: 0 0 8px;

  color: #64748b;

  font-size: 14px;
}


/* =========================================================
   RESPONSIVE
========================================================= */

@media (max-width: 1100px) {
  .stats {
    grid-template-columns:
      repeat(2, minmax(0, 1fr));
  }

  .grid {
    grid-template-columns: 1fr;
  }

  .card.wide {
    grid-column: span 1;
  }
}


@media (max-width: 800px) {
  .monitoring {
    padding: 18px;
  }

  .monitoring-header {
    flex-direction: column;
  }

  .refresh-button {
    width: 100%;
  }

  .alerts {
    grid-template-columns: 1fr;
  }
}


@media (max-width: 640px) {
  .monitoring {
    padding: 14px;
  }

  .monitoring h1 {
    font-size: 25px;
  }

  .stats {
    grid-template-columns: 1fr;
  }

  .stat-card {
    padding: 18px;
  }

  .card {
    padding: 16px;
  }

  .chart {
    height: 300px;
  }

  .forecast-chart {
    height: 320px;
  }

  .partial-warning {
    align-items: flex-start;
    flex-wrap: wrap;
  }

  .partial-warning button {
    width: 100%;
    margin-left: 0;
    text-align: left;
  }
}


/* =========================================================
   ANIMATION
========================================================= */

@keyframes monitoring-spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

</style>