<script setup>

import { useI18n } from "vue-i18n"

const { t } = useI18n()

defineEmits([
  "apply",
  "more"
])

</script>

<template>

<div class="actions">

  <button
    class="apply"
    @click="$emit('apply')"
  >
    🔥 {{ t("loanActions.apply") }}
  </button>

  <button
    class="secondary"
    @click="$emit('more')"
  >
    {{ t("loanActions.more") }}
  </button>

</div>

</template>

<style scoped>

.actions{

  display:grid;

  grid-template-columns:
    repeat(
      2,
      minmax(0,1fr)
    );

  gap:16px;

  margin-top:28px;

}

.apply{

  border:none;

  cursor:pointer;

  padding:18px 24px;

  border-radius:18px;

  font-size:15px;

  font-weight:800;

  color:white;

  background:
    linear-gradient(
      135deg,
      #16a34a,
      #15803d
    );

  transition:.25s ease;

  box-shadow:
    0 10px 24px rgba(
      22,
      163,
      74,
      .25
    );

}

.apply:hover{

  transform:
    translateY(-2px);

  box-shadow:
    0 14px 32px rgba(
      22,
      163,
      74,
      .35
    );

}

.secondary{

  border:1px solid #e5e7eb;

  cursor:pointer;

  padding:18px 24px;

  border-radius:18px;

  font-size:15px;

  font-weight:700;

  color:#0f172a;

  background:white;

  transition:.25s ease;

}

.secondary:hover{

  background:#f8fafc;

  border-color:#cbd5e1;

  transform:
    translateY(-2px);

}

@media(max-width:768px){

  .actions{

    grid-template-columns:1fr;

  }

}

</style>