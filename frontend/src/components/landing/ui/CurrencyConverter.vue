<script setup>
import {
  ref,
  computed,
  onMounted
} from "vue"

import { useI18n } from "vue-i18n"

import api from "@/api/axios"

const {
  t,
  locale
} = useI18n()

const amount = ref(100)

const from = ref("USD")

const to = ref("UZS")

const rates = ref({
  UZS: 1
})

const loading = ref(true)

const error = ref(false)


/* ---------------------------------
   CURRENCY LIST
--------------------------------- */

const currencyList = computed(() => {
  return Object.keys(rates.value)
})


/* ---------------------------------
   FORMAT NUMBER
--------------------------------- */

const formatNumber = (
  value,
  digits = 2
) => {
  return Number(value).toLocaleString(
    locale.value,
    {
      minimumFractionDigits: digits,
      maximumFractionDigits: digits
    }
  )
}


/* ---------------------------------
   LOAD RATES
--------------------------------- */

const loadRates = async () => {

  loading.value = true
  error.value = false

  try {

    const response =
      await api.get(
        "/banks/currency-rates/"
      )

    const apiRates = {
      UZS: 1
    }

    Object.entries(
      response.data || {}
    ).forEach(
      ([code, data]) => {

        const rate =
          Number(data?.rate)

        if (
          Number.isFinite(rate) &&
          rate > 0
        ) {
          apiRates[code] = rate
        }

      }
    )

    rates.value = apiRates


    /*
     * Если выбранной валюты больше нет
     * в API — возвращаемся к USD/UZS.
     */

    if (
      !rates.value[from.value]
    ) {
      from.value =
        rates.value.USD
          ? "USD"
          : "UZS"
    }

    if (
      !rates.value[to.value]
    ) {
      to.value = "UZS"
    }

  } catch (err) {

    console.error(
      "Ошибка загрузки курсов",
      err
    )

    error.value = true

  } finally {

    loading.value = false

  }

}


/* ---------------------------------
   NORMALIZED AMOUNT
--------------------------------- */

const normalizedAmount = computed(() => {

  const value =
    Number(amount.value)

  if (
    !Number.isFinite(value) ||
    value < 0
  ) {
    return 0
  }

  return value

})


/* ---------------------------------
   CONVERTED VALUE
--------------------------------- */

const converted = computed(() => {

  const value =
    normalizedAmount.value

  const fromRate =
    Number(
      rates.value[from.value]
    )

  const toRate =
    Number(
      rates.value[to.value]
    )

  if (
    !fromRate ||
    !toRate
  ) {
    return 0
  }

  /*
   * Все курсы выражены
   * относительно UZS.
   *
   * Например:
   *
   * 100 USD
   * × 11830.87
   * = UZS
   *
   * UZS / EUR rate
   * = EUR
   */

  const inUZS =
    value * fromRate

  return (
    inUZS / toRate
  )

})


/* ---------------------------------
   DISPLAYED RESULT
--------------------------------- */

const formattedConverted =
  computed(() => {

    if (
      !Number.isFinite(
        converted.value
      )
    ) {
      return "0"
    }

    return formatNumber(
      converted.value,
      converted.value >= 100
        ? 0
        : 2
    )

  })


/* ---------------------------------
   DIRECT RATE
--------------------------------- */

const directRate = computed(() => {

  const fromRate =
    Number(
      rates.value[from.value]
    )

  const toRate =
    Number(
      rates.value[to.value]
    )

  if (
    !fromRate ||
    !toRate
  ) {
    return 0
  }

  return fromRate / toRate

})


/* ---------------------------------
   SWAP
--------------------------------- */

const swapCurrencies = () => {

  const temp =
    from.value

  from.value =
    to.value

  to.value =
    temp

}


/* ---------------------------------
   MOUNT
--------------------------------- */

onMounted(() => {

  loadRates()

})
</script>


<template>

  <div class="converter">

    <!-- HEADER -->

    <div class="converter__header">

      <div>

        <h2 class="converter__title">
          {{ t("converter.title") }}
        </h2>

        <p class="converter__subtitle">
          {{ from }}
          →
          {{ to }}
        </p>

      </div>

    </div>


    <!-- LOADING -->

    <div
      v-if="loading"
      class="converter__state"
    >

      <div
        class="converter__loader"
      ></div>

      <span>
        {{ t("converter.loading") }}
      </span>

    </div>


    <!-- ERROR -->

    <div
      v-else-if="error"
      class="
        converter__state
        converter__state--error
      "
    >

      <span>
        {{ t("converter.error") }}
      </span>

      <button
        type="button"
        class="converter__retry"
        @click="loadRates"
      >
        {{ t("converter.retry") }}
      </button>

    </div>


    <!-- CONVERTER -->

    <template v-else>

      <!-- FROM -->

      <div class="converter__group">

        <label class="converter__label">
          {{ t("converter.from") }}
        </label>

        <div class="converter__row">

          <input
            v-model="amount"
            type="number"
            min="0"
            step="any"
            inputmode="decimal"
            class="converter__input"
          />

          <select
            v-model="from"
            class="converter__select"
          >

            <option
              v-for="
                currency
                in currencyList
              "
              :key="currency"
              :value="currency"
            >
              {{ currency }}
            </option>

          </select>

        </div>

      </div>


      <!-- SWAP -->

      <div class="converter__swap-wrapper">

        <button
          type="button"
          class="converter__swap"
          :aria-label="
            t('converter.swap')
          "
          @click="swapCurrencies"
        >

          <span>
            ⇅
          </span>

        </button>

      </div>


      <!-- TO -->

      <div class="converter__group">

        <label class="converter__label">
          {{ t("converter.to") }}
        </label>

        <div class="converter__row">

          <div
            class="
              converter__result
            "
          >
            {{ formattedConverted }}
          </div>

          <select
            v-model="to"
            class="converter__select"
          >

            <option
              v-for="
                currency
                in currencyList
              "
              :key="currency"
              :value="currency"
            >
              {{ currency }}
            </option>

          </select>

        </div>

      </div>


      <!-- RATE -->

      <div class="converter__rate">

        <span>
          1 {{ from }}
        </span>

        <span>
          =
        </span>

        <strong>
          {{
            formatNumber(
              directRate
            )
          }}
          {{ to }}
        </strong>

      </div>

    </template>

  </div>

</template>


<style scoped>

.converter {
  width: 100%;

  background: #ffffff;

  padding: 20px;

  border-radius: 20px;

  box-shadow:
    0 10px 30px
    rgba(15, 23, 42, 0.06);

  display: flex;

  flex-direction: column;

  gap: 14px;
}


/* HEADER */

.converter__header {
  display: flex;

  align-items: flex-start;

  justify-content: space-between;
}

.converter__title {
  margin: 0;

  font-size: 18px;

  line-height: 1.3;

  font-weight: 600;

  color: #0f172a;
}

.converter__subtitle {
  margin: 4px 0 0;

  font-size: 12px;

  color: #64748b;
}


/* GROUP */

.converter__group {
  display: flex;

  flex-direction: column;

  gap: 7px;
}

.converter__label {
  font-size: 11px;

  font-weight: 600;

  color: #64748b;

  text-transform: uppercase;

  letter-spacing: 0.04em;
}


/* ROW */

.converter__row {
  display: flex;

  gap: 8px;

  width: 100%;
}


/* INPUT */

.converter__input,
.converter__result {
  flex: 1;

  min-width: 0;

  height: 46px;

  padding:
    0 13px;

  border-radius: 12px;

  border: 1px solid #e2e8f0;

  background: #ffffff;

  color: #0f172a;

  font-size: 15px;

  font-weight: 600;

  outline: none;

  box-sizing: border-box;
}

.converter__input {
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}

.converter__input:focus {
  border-color: #2563eb;

  box-shadow:
    0 0 0 3px
    rgba(37, 99, 235, 0.10);
}


/* RESULT */

.converter__result {
  display: flex;

  align-items: center;

  background: #f8fafc;

  border-color: #e2e8f0;

  overflow: hidden;

  white-space: nowrap;

  text-overflow: ellipsis;
}


/* SELECT */

.converter__select {
  width: 92px;

  height: 46px;

  padding:
    0 9px;

  border-radius: 12px;

  border: 1px solid #e2e8f0;

  background: #ffffff;

  color: #0f172a;

  font-size: 13px;

  font-weight: 600;

  cursor: pointer;

  outline: none;

  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}

.converter__select:focus {
  border-color: #2563eb;

  box-shadow:
    0 0 0 3px
    rgba(37, 99, 235, 0.10);
}


/* SWAP */

.converter__swap-wrapper {
  display: flex;

  justify-content: center;

  height: 0;

  position: relative;

  z-index: 2;
}

.converter__swap {
  width: 38px;

  height: 38px;

  margin-top: -5px;

  border-radius: 50%;

  border: 4px solid #ffffff;

  background: #2563eb;

  color: #ffffff;

  cursor: pointer;

  display: flex;

  align-items: center;

  justify-content: center;

  font-size: 19px;

  line-height: 1;

  box-shadow:
    0 5px 15px
    rgba(37, 99, 235, 0.25);

  transition:
    transform 0.2s ease,
    background 0.2s ease,
    box-shadow 0.2s ease;
}

.converter__swap:hover {
  transform:
    rotate(180deg);

  background: #1d4ed8;

  box-shadow:
    0 7px 18px
    rgba(37, 99, 235, 0.30);
}

.converter__swap:active {
  transform:
    rotate(180deg)
    scale(0.94);
}


/* RATE */

.converter__rate {
  margin-top: 4px;

  padding:
    11px 13px;

  border-radius: 12px;

  background: #f8fafc;

  border: 1px solid #f1f5f9;

  display: flex;

  align-items: center;

  gap: 5px;

  flex-wrap: wrap;

  font-size: 12px;

  color: #64748b;
}

.converter__rate strong {
  color: #2563eb;

  font-weight: 700;
}


/* STATES */

.converter__state {
  min-height: 230px;

  display: flex;

  flex-direction: column;

  align-items: center;

  justify-content: center;

  gap: 10px;

  color: #64748b;

  font-size: 13px;
}

.converter__loader {
  width: 28px;

  height: 28px;

  border-radius: 50%;

  border:
    3px solid #e2e8f0;

  border-top-color:
    #2563eb;

  animation:
    converter-spin
    0.8s
    linear
    infinite;
}

@keyframes converter-spin {

  to {
    transform: rotate(360deg);
  }

}


/* ERROR */

.converter__state--error {
  color: #dc2626;
}

.converter__retry {
  border: none;

  background: #2563eb;

  color: #ffffff;

  padding:
    8px 14px;

  border-radius: 8px;

  cursor: pointer;

  font-size: 12px;

  font-weight: 600;

  transition:
    background 0.2s ease;
}

.converter__retry:hover {
  background: #1d4ed8;
}


/* MOBILE */

@media (max-width: 768px) {

  .converter {
    padding: 16px;

    border-radius: 16px;
  }

  .converter__title {
    font-size: 16px;
  }

  .converter__input,
  .converter__result {
    height: 44px;

    font-size: 14px;
  }

  .converter__select {
    height: 44px;

    width: 82px;
  }

}

@media (max-width: 380px) {

  .converter__select {
    width: 76px;
  }

  .converter__input,
  .converter__result {
    padding:
      0 10px;
  }

}

</style>