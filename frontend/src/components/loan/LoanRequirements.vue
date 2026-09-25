<script setup>

defineProps({
  product: {
    type: Object,
    default: () => ({})
  }
})

</script>

<template>

<div class="card">

  <h3>
    📋 Основные требования
  </h3>

  <div class="requirement">

    <div class="icon">
      🪪
    </div>

    <div>
      <strong>
        Документ
      </strong>

      <p>
        Паспорт или ID-карта
      </p>
    </div>

  </div>

  <div class="requirement">

    <div class="icon">
      🇺🇿
    </div>

    <div>
      <strong>
        Гражданство
      </strong>

      <p>
        Республика Узбекистан
      </p>
    </div>

  </div>

  <div class="requirement">

    <div class="icon">
      💳
    </div>

    <div>
      <strong>
        Платёжеспособность
      </strong>

      <p>
        Подтверждённый источник дохода
      </p>
    </div>

  </div>

  <div class="requirement">

    <div class="icon">
      🏦
    </div>

    <div>
      <strong>
        Решение банка
      </strong>

      <p>
        Окончательное решение принимает банк
      </p>
    </div>

  </div>

</div>

</template>

<style scoped>

.card{
  background:#fff;
  padding:24px;
  border-radius:18px;
  border:1px solid #e5e7eb;
  margin-bottom:24px;
}

h3{
  margin:0 0 20px;
  font-size:18px;
  font-weight:700;
}

.requirement{
  display:flex;
  gap:16px;
  align-items:flex-start;
  padding:14px 0;
  border-bottom:1px solid #f1f5f9;
}

.requirement:last-child{
  border-bottom:none;
}

.icon{
  font-size:22px;
}

strong{
  display:block;
  margin-bottom:4px;
}

p{
  margin:0;
  color:#64748b;
}

</style>