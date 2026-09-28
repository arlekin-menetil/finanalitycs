<script setup>
import { useI18n } from "vue-i18n"

const { t } = useI18n()

defineProps({
  selectedBank: {
    type: String,
    default: "Все банки",
  },

  uniqueBanks: {
    type: Array,
    default: () => [],
  },
})

defineEmits([
  "update:selectedBank",
])
</script>

<template>

<div class="filter">

<label class="filter-label">
  {{ t("analytics.selectBank") }}
</label>

  <div class="select-wrapper">

<select
  class="bank-select"
  :value="selectedBank"
  @change="
    $emit(
      'update:selectedBank',
      $event.target.value
    )
  "
>

  <option
    v-for="bank in uniqueBanks"
    :key="bank"
    :value="bank"
  >
    {{ bank }}
  </option>

</select>

<span class="select-icon">
  ▼
</span>

  </div>

</div>

</template>

<style scoped>

.filter{
  margin-bottom:24px;
}

.filter-label{
  display:block;

  margin-bottom:8px;

  font-size:14px;
  font-weight:600;

  color:#64748b;
}

.select-wrapper{
  position:relative;

  width:320px;
  max-width:100%;
}

.bank-select{

  width:100%;
  height:48px;

  padding:0 44px 0 16px;

  border:1px solid #e2e8f0;
  border-radius:12px;

  background:#fff;

  font-size:14px;
  font-weight:500;

  color:#0f172a;

  outline:none;

  appearance:none;
  -webkit-appearance:none;
  -moz-appearance:none;

  transition:all .25s ease;

  cursor:pointer;
}

.bank-select:hover{

  border-color:#94a3b8;

}

.bank-select:focus{

  border-color:#2563eb;

  box-shadow:
    0 0 0 4px
    rgba(37,99,235,.12);

}

.select-icon{

  position:absolute;

  top:50%;
  right:16px;

  transform:translateY(-50%);

  pointer-events:none;

  font-size:12px;

  color:#64748b;
}

</style>
