<script setup>
import CurrencyChart from "../ui/CurrencyChart.vue"
import CurrencyConverter from "../ui/CurrencyConverter.vue"
</script>

<template>

  <section class="converter">

    <div class="converter__wrapper">

      <div class="converter__chart">
        <CurrencyChart />
      </div>

      <div class="converter__calculator">
        <CurrencyConverter />
      </div>

    </div>

  </section>

</template>

<style scoped>

.converter {
  width: 100%;

  padding:
    60px 20px;

  margin-top: 40px;

  background:
    linear-gradient(
      135deg,
      #e0f2fe 0%,
      #eef2ff 100%
    );

  border-radius: 24px;

  box-sizing: border-box;

  display: flex;

  justify-content: center;
}


/* MAIN GRID */

.converter__wrapper {
  width: 100%;

  max-width: 1100px;

  display: grid;

  grid-template-columns:
    minmax(0, 2fr)
    minmax(300px, 1fr);

  gap: 20px;

  align-items: stretch;
}


/* CHILDREN */

.converter__chart,
.converter__calculator {
  min-width: 0;

  display: flex;
}


/*
 * CurrencyChart / CurrencyConverter
 * сами отвечают за свои карточки.
 */

.converter__chart > :deep(.chart),
.converter__calculator > :deep(.converter) {
  width: 100%;
}


/* TABLET */

@media (max-width: 900px) {

  .converter {
    padding:
      50px 16px;
  }

  .converter__wrapper {
    grid-template-columns:
      minmax(0, 1.6fr)
      minmax(280px, 1fr);

    gap: 16px;
  }

}


/* MOBILE */

@media (max-width: 768px) {

  .converter {
    padding:
      35px 12px;

    margin-top: 30px;

    border-radius: 20px;
  }

  .converter__wrapper {
    grid-template-columns: 1fr;

    gap: 16px;
  }

}


/* SMALL MOBILE */

@media (max-width: 420px) {

  .converter {
    padding:
      24px 8px;

    border-radius: 16px;
  }

  .converter__wrapper {
    gap: 12px;
  }

}

</style>