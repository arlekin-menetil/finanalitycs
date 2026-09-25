<script setup>

import {
  Bar,
  Line
} from "vue-chartjs"

defineProps({

  installsData: {
    type: Object,
    required: true
  },

  ratingData: {
    type: Object,
    required: true
  },

  chartOptions: {
    type: Object,
    required: true
  }

})

</script>

<template>

<div class="grid">

  <!-- СКАЧИВАНИЯ -->

  <div class="card">

    <h3>
      📱 Скачивания мобильных приложений
    </h3>

    <div class="chart-container">

      <Bar
        :data="installsData"
        :options="chartOptions"
      />

    </div>

  </div>

  <!-- РЕЙТИНГ -->

  <div class="card">

    <h3>
      ⭐ Рейтинг мобильных приложений
    </h3>

    <div class="chart-container">

      <Line
        :data="ratingData"
        :options="chartOptions"
      />

    </div>

  </div>

</div>

</template>

<style scoped>

.grid {

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

  margin-top: 20px;

}

.card {

  background: #ffffff;

  padding: 20px;

  border-radius: 16px;

  box-shadow:
    0 2px 10px
    rgba(
      15,
      23,
      42,
      0.06
    );

  display: flex;

  flex-direction: column;

}

.chart-container {

  position: relative;

  height: 350px;

}

h3 {

  margin: 0 0 16px;

  font-size: 18px;

  font-weight: 700;

  color: #0f172a;

}

@media (max-width: 900px) {

  .grid {

    grid-template-columns: 1fr;

  }

  .chart-container {

    height: 320px;

  }

}

</style>