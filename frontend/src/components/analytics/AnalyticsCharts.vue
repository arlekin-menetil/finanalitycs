<script setup>
import {
  Bar,
  Line,
} from "vue-chartjs"

import { useI18n } from "vue-i18n"

import "chart.js/auto"

const { t } = useI18n()

// =====================================================
// PROPS
// =====================================================

defineProps({

  // ---------------------------------------------------
  // Процентные ставки
  // ---------------------------------------------------

  interestData: {
    type: Object,
    required: true,
  },

  // ---------------------------------------------------
  // Кредитные лимиты
  // ---------------------------------------------------

  loanData: {
    type: Object,
    required: true,
  },

  // ---------------------------------------------------
  // AI-рейтинг
  // ---------------------------------------------------

  scoreData: {
    type: Object,
    required: true,
  },

  // ---------------------------------------------------
  // Количество продуктов
  // ---------------------------------------------------

  productCountData: {
    type: Object,
    required: true,
  },

  // ---------------------------------------------------
  // Способы оформления
  // ---------------------------------------------------

  openingMethodsData: {
    type: Object,
    required: true,
  },

  // ---------------------------------------------------
  // Общие настройки
  // ---------------------------------------------------

  chartOptions: {
    type: Object,
    required: true,
  },

})
</script>


<template>

  <div class="charts-grid">


    <!-- ================================================= -->
    <!-- ПРОЦЕНТНЫЕ СТАВКИ -->
    <!-- ================================================= -->

    <section class="chart-card">

      <div class="chart-header">

        <div class="chart-icon">
          %
        </div>

        <div>

          <h2>
            {{ t("analytics.charts.interestTitle") }}
          </h2>

          <p>
            {{ t("analytics.charts.interestDescription") }}
          </p>

        </div>

      </div>


      <div class="chart-container">

        <Bar
          :data="interestData"
          :options="chartOptions"
        />

      </div>

    </section>


    <!-- ================================================= -->
    <!-- КРЕДИТНЫЕ ЛИМИТЫ -->
    <!-- ================================================= -->

    <section class="chart-card">

      <div class="chart-header">

        <div class="chart-icon">
          ₿
        </div>

        <div>

          <h2>
            {{ t("analytics.charts.limitsTitle") }}
          </h2>

          <p>
            {{ t("analytics.charts.limitsDescription") }}
          </p>

        </div>

      </div>


      <div class="chart-container">

        <Bar
          :data="loanData"
          :options="chartOptions"
        />

      </div>

    </section>


    <!-- ================================================= -->
    <!-- AI-РЕЙТИНГ -->
    <!-- ================================================= -->

    <section class="chart-card">

      <div class="chart-header">

        <div class="chart-icon">
          AI
        </div>

        <div>

          <h2>
            {{ t("analytics.charts.aiTitle") }}
          </h2>

          <p>
            {{ t("analytics.charts.aiDescription") }}
          </p>

        </div>

      </div>


      <div class="chart-container">

        <Bar
          :data="scoreData"
          :options="chartOptions"
        />

      </div>

    </section>


    <!-- ================================================= -->
    <!-- КОЛИЧЕСТВО ПРОДУКТОВ -->
    <!-- ================================================= -->

    <section class="chart-card">

      <div class="chart-header">

        <div class="chart-icon">
          #
        </div>

        <div>

          <h2>
            {{ t("analytics.charts.productsTitle") }}
          </h2>

          <p>
            {{ t("analytics.charts.productsDescription") }}
          </p>

        </div>

      </div>


      <div class="chart-container">

        <Bar
          :data="productCountData"
          :options="chartOptions"
        />

      </div>

    </section>


    <!-- ================================================= -->
    <!-- СПОСОБЫ ОФОРМЛЕНИЯ -->
    <!-- ================================================= -->

    <section class="chart-card full-width">

      <div class="chart-header">

        <div class="chart-icon">
          ↗
        </div>

        <div>

          <h2>
            {{ t("analytics.charts.openingTitle") }}
          </h2>

          <p>
            {{ t("analytics.charts.openingDescription") }}
          </p>

        </div>

      </div>


      <div class="chart-container large">

        <Bar
          :data="openingMethodsData"
          :options="chartOptions"
        />

      </div>

    </section>


  </div>

</template>


<style scoped>

/* =====================================================
   GRID
===================================================== */

.charts-grid {

  display: grid;

  grid-template-columns:
    repeat(
      2,
      minmax(
        0,
        1fr
      )
    );

  gap: 20px;

  width: 100%;
}


/* =====================================================
   CARD
===================================================== */

.chart-card {

  min-width: 0;

  background: #ffffff;

  border:
    1px solid
    #e5e7eb;

  border-radius: 18px;

  padding: 20px;

  box-sizing: border-box;

  overflow: hidden;

  transition:
    transform
    0.2s
    ease,

    box-shadow
    0.2s
    ease;
}


.chart-card:hover {

  transform:
    translateY(-1px);

  box-shadow:
    0 8px 24px
    rgba(
      15,
      23,
      42,
      0.06
    );
}


.full-width {

  grid-column:
    1 / -1;
}


/* =====================================================
   HEADER
===================================================== */

.chart-header {

  display: flex;

  align-items: flex-start;

  gap: 12px;

  margin-bottom: 18px;
}


.chart-icon {

  flex:
    0 0
    38px;

  width: 38px;

  height: 38px;

  display: flex;

  align-items: center;

  justify-content: center;

  border-radius: 10px;

  background:
    #eff6ff;

  color:
    #2563eb;

  font-size: 13px;

  font-weight: 800;

  box-sizing: border-box;
}


.chart-header h2 {

  margin: 0;

  font-size: 18px;

  line-height: 1.3;

  font-weight: 750;

  color:
    #111827;
}


.chart-header p {

  margin:
    5px 0 0;

  color:
    #6b7280;

  font-size: 13px;

  line-height: 1.4;
}


/* =====================================================
   CHART
===================================================== */

.chart-container {

  position: relative;

  width: 100%;

  height: 320px;

  min-width: 0;
}


.chart-container.large {

  height: 380px;
}


/* =====================================================
   RESPONSIVE
===================================================== */

@media (max-width: 1100px) {

  .charts-grid {

    grid-template-columns:
      1fr;
  }

  .full-width {

    grid-column:
      auto;
  }

}


@media (max-width: 700px) {

  .charts-grid {

    gap: 16px;
  }


  .chart-card {

    padding: 16px;

    border-radius: 15px;
  }


  .chart-header h2 {

    font-size: 16px;
  }


  .chart-header p {

    font-size: 12px;
  }


  .chart-container {

    height: 280px;
  }


  .chart-container.large {

    height: 300px;
  }

}

</style>