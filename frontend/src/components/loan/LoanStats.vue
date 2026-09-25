<script setup>

defineProps({
  product: {
    type: Object,
    default: () => ({})
  },

  formatMoney: {
    type: Function,
    default: (v) => v ?? "-"
  }
})

function formatTerm(term) {

  const months = Number(term)

  if (!months) {
    return "-"
  }

  if (months < 12) {
    return `${months} мес.`
  }

  if (months % 12 === 0) {

    const years = months / 12

    if (years === 1) {
      return "1 год"
    }

    if (years >= 2 && years <= 4) {
      return `${years} года`
    }

    return `${years} лет`
  }

  return `${months} мес.`
}

</script>

<template>

<div class="stats">

  <!-- СТАВКА -->

  <div class="stat-card">

    <span>
      Ставка
    </span>

    <strong>
      {{ product?.interest_rate || "-" }}%
    </strong>

  </div>

  <!-- СРОК -->

  <div class="stat-card">

    <span>
      Срок
    </span>

    <strong>
      {{
        formatTerm(
          product?.term
        )
      }}
    </strong>

  </div>

  <!-- БАНК -->

  <div class="stat-card">

    <span>
      Банк
    </span>

    <strong>
      {{
        product?.bank?.name ||
        product?.bank_name ||
        "-"
      }}
    </strong>

  </div>

</div>

</template>

<style scoped>

.stats{

  display:grid;

  grid-template-columns:
    repeat(
      auto-fit,
      minmax(240px,1fr)
    );

  gap:20px;

  margin-bottom:28px;

}

.stat-card{

  background:#ffffff;

  border:1px solid #e5e7eb;

  border-radius:24px;

  padding:24px;

  transition:.25s ease;

  box-shadow:
    0 4px 14px rgba(
      15,
      23,
      42,
      .04
    );

}

.stat-card:hover{

  transform:translateY(-2px);

  box-shadow:
    0 10px 30px rgba(
      15,
      23,
      42,
      .08
    );

}

.stat-card span{

  display:block;

  color:#64748b;

  font-size:13px;

  font-weight:600;

  text-transform:uppercase;

  letter-spacing:.04em;

  margin-bottom:10px;

}

.stat-card strong{

  display:block;

  color:#0f172a;

  font-size:28px;

  font-weight:800;

  line-height:1.2;

  word-break:break-word;

}

@media(max-width:768px){

  .stats{

    grid-template-columns:1fr;

    gap:14px;

  }

  .stat-card{

    padding:20px;

  }

  .stat-card strong{

    font-size:24px;

  }

}

</style>