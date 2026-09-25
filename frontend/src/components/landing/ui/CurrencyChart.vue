<script setup>
import {
  ref,
  onMounted,
  watch,
  onBeforeUnmount,
  computed,
  nextTick
} from "vue"

import { useI18n } from "vue-i18n"
import Chart from "chart.js/auto"

import api from "@/api/axios"

const { t, locale } = useI18n()

const chartRef = ref(null)

let chart = null

const rates = ref({})
const history = ref({})

const activeCurrency = ref("USD")

const loading = ref(true)
const error = ref(false)


/* ---------------------------------
   CURRENCIES
--------------------------------- */

const currencies = computed(() => {
  return Object.entries(
    rates.value || {}
  ).map(([code, data]) => ({
    code,
    value: Number(data?.rate || 0),
    change: Number(data?.diff || 0)
  }))
})


/* ---------------------------------
   ACTIVE RATE
--------------------------------- */

const activeRate = computed(() => {
  return Number(
    rates.value?.[
      activeCurrency.value
    ]?.rate || 0
  )
})


/* ---------------------------------
   ACTIVE CHANGE
--------------------------------- */

const activeChange = computed(() => {
  return Number(
    rates.value?.[
      activeCurrency.value
    ]?.diff || 0
  )
})


/* ---------------------------------
   ACTIVE HISTORY
--------------------------------- */

const activeHistory = computed(() => {
  return (
    history.value?.[
      activeCurrency.value
    ] || []
  )
})


/* ---------------------------------
   FORMAT NUMBER
--------------------------------- */

const formatNumber = (
  value,
  digits = 2
) => {
  return Number(
    value || 0
  ).toLocaleString(
    locale.value,
    {
      minimumFractionDigits:
        digits,

      maximumFractionDigits:
        digits
    }
  )
}


/* ---------------------------------
   FORMAT DATE
--------------------------------- */

const formatDate = (
  dateString
) => {

  if (!dateString) {
    return ""
  }

  const date =
    new Date(
      `${dateString}T00:00:00`
    )

  return date.toLocaleDateString(
    locale.value,
    {
      day: "2-digit",
      month: "2-digit"
    }
  )
}


/* ---------------------------------
   TOOLTIP DATE
--------------------------------- */

const getDateLabel = (
  dateString
) => {

  if (!dateString) {
    return ""
  }

  const date =
    new Date(
      `${dateString}T00:00:00`
    )

  return date.toLocaleDateString(
    locale.value,
    {
      day: "2-digit",
      month: "long",
      year: "numeric"
    }
  )
}


/* ---------------------------------
   CHART LABELS
--------------------------------- */

const getLabels = (
  currency = activeCurrency.value
) => {

  return (
    history.value?.[currency] || []
  ).map(
    item =>
      formatDate(item.date)
  )
}


/* ---------------------------------
   CHART DATA
--------------------------------- */

const getChartData = (
  currency = activeCurrency.value
) => {

  return (
    history.value?.[currency] || []
  ).map(
    item =>
      Number(item.rate)
  )
}


/* ---------------------------------
   UPDATE EXISTING CHART
--------------------------------- */

const updateChart = () => {

  if (!chart) {
    return
  }

  chart.data.labels =
    getLabels(
      activeCurrency.value
    )

  chart.data.datasets[0].data =
    getChartData(
      activeCurrency.value
    )

  chart.update()
}


/* ---------------------------------
   CHANGE CURRENCY
--------------------------------- */

const changeCurrency = (
  code
) => {

  if (!code) {
    return
  }

  activeCurrency.value = code

  updateChart()
}


/* ---------------------------------
   LOAD DATA
--------------------------------- */

const loadData = async () => {

  loading.value = true
  error.value = false

  try {

    const [
      ratesRes,
      historyRes
    ] = await Promise.all([

      api.get(
        "/banks/currency-rates/"
      ),

      api.get(
        "/banks/currency-history/"
      )

    ])


    /* CURRENT RATES */

    rates.value =
      ratesRes.data || {}


    /* HISTORY */

    history.value =
      historyRes.data || {}


    /*
     * Если USD отсутствует,
     * выбираем первую доступную валюту.
     */

    if (
      !rates.value[
        activeCurrency.value
      ]
    ) {

      const firstCurrency =
        Object.keys(
          rates.value
        )[0]

      if (firstCurrency) {
        activeCurrency.value =
          firstCurrency
      }

    }


    /*
     * Очень важно:
     *
     * сначала выключаем loading,
     * чтобы Vue создал canvas.
     */

    loading.value = false


    /*
     * Ждём следующий DOM-цикл Vue.
     *
     * После этого:
     *
     * chartRef.value
     *
     * уже содержит <canvas>.
     */

    await nextTick()


    /*
     * Теперь создаём Chart.js.
     */

    createChart()

  } catch (err) {

    console.error(
      "Ошибка загрузки валют",
      err
    )

    error.value = true
    loading.value = false

  }

}


/* ---------------------------------
   CREATE CHART
--------------------------------- */

const createChart = () => {

  /*
   * Canvas ещё не существует.
   */

  if (!chartRef.value) {
    return
  }


  /*
   * Уничтожаем старый график,
   * если он существует.
   */

  if (chart) {

    chart.destroy()

    chart = null

  }


  const data =
    getChartData(
      activeCurrency.value
    )


  const labels =
    getLabels(
      activeCurrency.value
    )


  /*
   * Если история отсутствует,
   * не создаём пустой график.
   */

  if (!data.length) {
    return
  }


  chart = new Chart(
    chartRef.value,
    {

      type: "line",


      /* ---------------------------------
         DATA
      --------------------------------- */

      data: {

        labels,

        datasets: [

          {

            data,

            borderColor:
              "#2563eb",

            backgroundColor:
              "rgba(37, 99, 235, 0.10)",

            fill: true,

            tension: 0.4,

            borderWidth: 2,

            pointRadius: 3,

            pointHoverRadius: 6,

            pointBorderWidth: 2,

            pointBackgroundColor:
              "#ffffff",

            pointBorderColor:
              "#2563eb"

          }

        ]

      },


      /* ---------------------------------
         OPTIONS
      --------------------------------- */

      options: {

        responsive: true,

        maintainAspectRatio: false,


        interaction: {

          intersect: false,

          mode: "index"

        },


        plugins: {

          legend: {

            display: false

          },


          tooltip: {

            displayColors: false,

            padding: 12,


            callbacks: {


              title: (
                items
              ) => {

                const index =
                  items?.[0]
                    ?.dataIndex


                const item =
                  activeHistory.value[
                    index
                  ]


                return item
                  ? getDateLabel(
                      item.date
                    )
                  : ""

              },


              label: (
                context
              ) => {

                return (
                  `${activeCurrency.value}: ` +
                  `${formatNumber(
                    context.parsed.y
                  )}`
                )

              }

            }

          }

        },


        /* ---------------------------------
           SCALES
        --------------------------------- */

        scales: {


          x: {

            grid: {

              display: false

            },

            border: {

              display: false

            },

            ticks: {

              color:
                "#64748b",

              font: {

                size: 11

              }

            }

          },


          y: {

            grid: {

              color:
                "rgba(148, 163, 184, 0.15)"

            },

            border: {

              display: false

            },

            ticks: {

              color:
                "#64748b",

              font: {

                size: 11

              },

              callback: (
                value
              ) => {

                return Number(
                  value
                ).toLocaleString(
                  locale.value
                )

              }

            }

          }

        }

      }

    }

  )

}


/* ---------------------------------
   MOUNT
--------------------------------- */

onMounted(() => {

  loadData()

})


/* ---------------------------------
   LANGUAGE CHANGE
--------------------------------- */

watch(
  locale,
  async () => {

    /*
     * Если график уже существует,
     * достаточно обновить его.
     */

    if (chart) {

      updateChart()

      return

    }


    /*
     * Если графика ещё нет,
     * ждём DOM и создаём его.
     */

    await nextTick()

    createChart()

  }
)


/* ---------------------------------
   DESTROY
--------------------------------- */

onBeforeUnmount(() => {

  if (chart) {

    chart.destroy()

    chart = null

  }

})
</script>


<template>

  <div class="chart">

    <!-- HEADER -->

    <div class="chart__header">

      <div>

        <h2 class="chart__title">

          {{ t("chart.title") }}

          <span>
            {{ activeCurrency }}
          </span>

        </h2>


        <div
          v-if="
            !loading &&
            !error
          "
          class="chart__current"
        >

          <strong>

            {{
              formatNumber(
                activeRate
              )
            }}

          </strong>


          <span
            :class="
              activeChange >= 0
                ? 'up'
                : 'down'
            "
          >

            {{
              activeChange >= 0
                ? "+"
                : ""
            }}

            {{
              formatNumber(
                activeChange
              )
            }}

          </span>

        </div>

      </div>

    </div>


    <!-- LOADING -->

    <div
      v-if="loading"
      class="chart__state"
    >

      <div
        class="chart__loader"
      ></div>


      <span>
        {{ t("chart.loading") }}
      </span>

    </div>


    <!-- ERROR -->

    <div
      v-else-if="error"
      class="
        chart__state
        chart__state--error
      "
    >

      <span>
        {{ t("chart.error") }}
      </span>


      <button
        type="button"
        class="chart__retry"
        @click="loadData"
      >

        {{ t("chart.retry") }}

      </button>

    </div>


    <!-- CHART -->

    <template v-else>

      <div class="chart__inner">

        <canvas
          ref="chartRef"
        ></canvas>

      </div>


      <!-- CURRENCY SWITCH -->

      <div class="chart__switch">

        <button
          v-for="
            currency in currencies
          "
          :key="currency.code"

          type="button"

          :class="[
            'chart__btn',
            {
              active:
                activeCurrency ===
                currency.code
            }
          ]"

          @click="
            changeCurrency(
              currency.code
            )
          "
        >

          <span
            class="chart__code"
          >

            {{ currency.code }}

          </span>


          <span
            class="chart__value"
          >

            {{
              formatNumber(
                currency.value
              )
            }}

          </span>


          <span
            :class="
              currency.change >= 0
                ? 'up'
                : 'down'
            "
          >

            {{
              currency.change >= 0
                ? "+"
                : ""
            }}

            {{
              formatNumber(
                currency.change
              )
            }}

          </span>

        </button>

      </div>

    </template>

  </div>

</template>


<style scoped>

.chart {

  width: 100%;

  background:
    #ffffff;

  padding:
    20px;

  border-radius:
    20px;

  box-shadow:
    0 10px 30px
    rgba(
      15,
      23,
      42,
      0.06
    );

  display:
    flex;

  flex-direction:
    column;

  gap:
    16px;

}


/* ---------------------------------
   HEADER
--------------------------------- */

.chart__header {

  display:
    flex;

  align-items:
    flex-start;

  justify-content:
    space-between;

}


.chart__title {

  margin:
    0;

  font-size:
    18px;

  line-height:
    1.3;

  font-weight:
    600;

  color:
    #0f172a;

}


.chart__title span {

  color:
    #2563eb;

}


.chart__current {

  display:
    flex;

  align-items:
    center;

  gap:
    10px;

  margin-top:
    5px;

}


.chart__current strong {

  font-size:
    20px;

  font-weight:
    700;

  color:
    #0f172a;

}


.chart__current span {

  font-size:
    12px;

  font-weight:
    600;

}


/* ---------------------------------
   CHART
--------------------------------- */

.chart__inner {

  position:
    relative;

  width:
    100%;

  height:
    210px;

}


.chart__inner canvas {

  position:
    absolute !important;

  inset:
    0;

  width:
    100% !important;

  height:
    100% !important;

}


/* ---------------------------------
   CURRENCY SWITCH
--------------------------------- */

.chart__switch {

  display:
    grid;

  grid-template-columns:
    repeat(
      5,
      minmax(
        0,
        1fr
      )
    );

  gap:
    8px;

}


.chart__btn {

  min-width:
    0;

  padding:
    10px 7px;

  border-radius:
    12px;

  border:
    1px solid
    #e2e8f0;

  background:
    #ffffff;

  cursor:
    pointer;

  display:
    flex;

  flex-direction:
    column;

  align-items:
    center;

  gap:
    3px;

  transition:
    background
    0.2s ease,

    border-color
    0.2s ease,

    transform
    0.2s ease,

    box-shadow
    0.2s ease;

}


.chart__btn:hover {

  background:
    #f8fafc;

  border-color:
    #cbd5e1;

  transform:
    translateY(
      -1px
    );

}


.chart__btn.active {

  background:
    #2563eb;

  border-color:
    #2563eb;

  box-shadow:
    0 5px 15px
    rgba(
      37,
      99,
      235,
      0.20
    );

}


/* ---------------------------------
   CURRENCY CODE
--------------------------------- */

.chart__code {

  font-size:
    12px;

  font-weight:
    700;

  color:
    #0f172a;

}


.chart__value {

  font-size:
    10px;

  color:
    #64748b;

  white-space:
    nowrap;

}


.chart__btn.active
.chart__code,

.chart__btn.active
.chart__value {

  color:
    #ffffff;

}


/* ---------------------------------
   CHANGE
--------------------------------- */

.chart__btn .up,

.chart__btn .down {

  font-size:
    10px;

  font-weight:
    600;

}


.up {

  color:
    #16a34a;

}


.down {

  color:
    #dc2626;

}


.chart__btn.active
.up,

.chart__btn.active
.down {

  color:
    #ffffff;

}


/* ---------------------------------
   LOADING
--------------------------------- */

.chart__state {

  min-height:
    210px;

  display:
    flex;

  flex-direction:
    column;

  align-items:
    center;

  justify-content:
    center;

  gap:
    10px;

  color:
    #64748b;

  font-size:
    13px;

}


.chart__loader {

  width:
    28px;

  height:
    28px;

  border-radius:
    50%;

  border:
    3px solid
    #e2e8f0;

  border-top-color:
    #2563eb;

  animation:
    chart-spin
    0.8s
    linear
    infinite;

}


@keyframes chart-spin {

  to {

    transform:
      rotate(
        360deg
      );

  }

}


/* ---------------------------------
   ERROR
--------------------------------- */

.chart__state--error {

  color:
    #dc2626;

}


.chart__retry {

  border:
    none;

  background:
    #2563eb;

  color:
    #ffffff;

  padding:
    8px 14px;

  border-radius:
    8px;

  cursor:
    pointer;

  font-size:
    12px;

  font-weight:
    600;

  transition:
    background
    0.2s ease;

}


.chart__retry:hover {

  background:
    #1d4ed8;

}


/* ---------------------------------
   TABLET / MOBILE
--------------------------------- */

@media (max-width: 768px) {

  .chart {

    padding:
      16px;

    border-radius:
      16px;

  }


  .chart__title {

    font-size:
      16px;

  }


  .chart__current strong {

    font-size:
      18px;

  }


  .chart__inner {

    height:
      180px;

  }


  .chart__switch {

    grid-template-columns:
      repeat(
        3,
        1fr
      );

  }


  .chart__btn {

    padding:
      9px 5px;

  }

}


/* ---------------------------------
   SMALL MOBILE
--------------------------------- */

@media (max-width: 420px) {

  .chart__switch {

    grid-template-columns:
      repeat(
        2,
        1fr
      );

  }

}

</style>