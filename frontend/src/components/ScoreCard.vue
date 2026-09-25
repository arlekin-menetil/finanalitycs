<template>

  <div class="score-card">

    <!-- ===================================== -->
    <!-- 💣 EMPTY -->
    <!-- ===================================== -->
    <div
      v-if="!hasScore"
      class="empty-state"
    >

      <div class="empty-icon">
        📊
      </div>

      <h3>
        Скоринг пока недоступен
      </h3>

      <p>
        Заполните профиль и выполните
        анализ, чтобы получить
        персональный кредитный рейтинг
      </p>

    </div>


    <!-- ===================================== -->
    <!-- 💣 CONTENT -->
    <!-- ===================================== -->
    <template v-else>

      <!-- =================================== -->
      <!-- 💣 HEADER -->
      <!-- =================================== -->
      <div class="score-header">

        <div class="score-info">

          <span class="score-label">

            {{ $t("dashboard.score") }}

          </span>

          <div class="score-value">

            {{ normalizedScore }}

          </div>

          <div class="score-subtitle">

            из 850 возможных

          </div>

        </div>


        <!-- ================================= -->
        <!-- 💣 RISK -->
        <!-- ================================= -->
        <div
          :class="[
            'risk-badge',
            riskClass
          ]"
        >

          <span class="risk-dot"></span>

          {{ riskLabel }}

        </div>

      </div>


      <!-- =================================== -->
      <!-- 💣 PROGRESS -->
      <!-- =================================== -->
      <div class="progress-section">

        <div class="progress-top">

          <span>
            Кредитный рейтинг
          </span>

          <span>
            {{ scorePercent }}%
          </span>

        </div>

        <div class="progress-track">

          <div
            class="progress-fill"
            :style="{
              width:
                scorePercent + '%'
            }"
          />

        </div>

      </div>


      <!-- =================================== -->
      <!-- 💣 STATS -->
      <!-- =================================== -->
      <div class="stats-grid">

        <!-- =============================== -->
        <!-- 💣 APPROVAL -->
        <!-- =============================== -->
        <div class="stat-card">

          <div class="stat-icon success">
            ✓
          </div>

          <div class="stat-content">

            <span class="stat-label">
              Одобрение
            </span>

            <strong class="stat-value">
              {{ approvalPercent }}%
            </strong>

          </div>

        </div>


        <!-- =============================== -->
        <!-- 💣 RISK -->
        <!-- =============================== -->
        <div class="stat-card">

          <div class="stat-icon warning">
            ⚠
          </div>

          <div class="stat-content">

            <span class="stat-label">
              Риск
            </span>

            <strong class="stat-value">
              {{ riskLabel }}
            </strong>

          </div>

        </div>


        <!-- =============================== -->
        <!-- 💣 SCORE -->
        <!-- =============================== -->
        <div class="stat-card">

          <div class="stat-icon info">
            📈
          </div>

          <div class="stat-content">

            <span class="stat-label">
              Уровень
            </span>

            <strong class="stat-value">
              {{ scoreLevel }}
            </strong>

          </div>

        </div>

      </div>


      <!-- =================================== -->
      <!-- 💣 EXPLANATION -->
      <!-- =================================== -->
      <div class="explanation-card">

        <div class="explanation-title">

          AI Анализ

        </div>

        <div class="explanation-text">

          {{ scoreExplanation }}

        </div>

      </div>


      <!-- =================================== -->
      <!-- 💣 RECOMMENDATION -->
      <!-- =================================== -->
      <div
        v-if="recommendationText"
        class="recommendation-box"
      >

        <div class="recommendation-title">

          Рекомендация

        </div>

        <p>

          {{ recommendationText }}

        </p>

      </div>

    </template>

  </div>

</template>

<script setup>

import {
  computed
} from "vue"

// ==========================================
// 💣 PROPS
// ==========================================
const props = defineProps({

  score: {
    type: Object,
    default: null,
  },
})

// ==========================================
// 💣 HAS SCORE
// ==========================================
const hasScore = computed(() => {

  return !!props.score
})

// ==========================================
// 💣 SCORE
// ==========================================
const normalizedScore = computed(() => {

  return Number(

    props.score?.credit_score ||

    props.score?.score ||

    0
  )
})

// ==========================================
// 💣 RISK CLASS
// ==========================================
const riskClass = computed(() => {

  const risk = (

    props.score?.risk_category ||

    "medium"
  )

    .toLowerCase()

  if (
    risk.includes("low")
  ) {
    return "low"
  }

  if (
    risk.includes("high")
  ) {
    return "high"
  }

  return "medium"
})

// ==========================================
// 💣 RISK LABEL
// ==========================================
const riskLabel = computed(() => {

  const risk = (

    props.score?.risk_category ||

    ""
  ).toLowerCase()

  if (
    risk.includes("low")
  ) {
    return "Низкий"
  }

  if (
    risk.includes("high")
  ) {
    return "Высокий"
  }

  return "Средний"
})

// ==========================================
// 💣 APPROVAL
// ==========================================
const approvalPercent = computed(() => {

  const raw = Number(

    props.score?.approval_probability ||

    0
  )

  if (raw <= 1) {

    return Math.round(raw * 100)
  }

  return Math.round(raw)
})

// ==========================================
// 💣 PERCENT
// ==========================================
const scorePercent = computed(() => {

  const value = (

    normalizedScore.value / 850
  ) * 100

  return Math.min(
    100,
    Math.max(0, value)
  )
})

// ==========================================
// 💣 SCORE LEVEL
// ==========================================
const scoreLevel = computed(() => {

  const s = normalizedScore.value

  if (s >= 800) {

    return "Отличный"
  }

  if (s >= 700) {

    return "Хороший"
  }

  if (s >= 600) {

    return "Средний"
  }

  return "Низкий"
})

// ==========================================
// 💣 EXPLANATION
// ==========================================
const scoreExplanation = computed(() => {

  const s = normalizedScore.value

  if (s >= 800) {

    return `
      У вас очень высокий кредитный рейтинг.
      Банки с высокой вероятностью
      предложат лучшие процентные ставки,
      увеличенные лимиты и быстрое одобрение.
    `
  }

  if (s >= 700) {

    return `
      Ваш профиль выглядит надёжным.
      Большинство банков готовы
      одобрить кредит на хороших условиях.
    `
  }

  if (s >= 600) {

    return `
      Ваш рейтинг находится
      на среднем уровне.
      Некоторые банки могут
      запросить дополнительные данные.
    `
  }

  return `
    Ваш рейтинг пока низкий.
    Рекомендуется улучшить
    финансовую нагрузку,
    снизить обязательства
    и увеличить стабильность дохода.
  `
})

// ==========================================
// 💣 RECOMMENDATION
// ==========================================
const recommendationText = computed(() => {

  const s = normalizedScore.value

  if (s >= 750) {

    return `
      Вам доступны ипотека,
      автокредиты и premium-продукты
      с минимальными ставками.
    `
  }

  if (s >= 650) {

    return `
      Рекомендуются потребительские
      кредиты и микрозаймы
      со средней финансовой нагрузкой.
    `
  }

  return `
    Лучше начать с небольших
    микрозаймов и онлайн-кредитов,
    чтобы постепенно улучшить
    кредитную историю.
  `
})

</script>

<style scoped>

.score-card{

  position:relative;

  overflow:hidden;

  background:
    linear-gradient(
      145deg,
      rgba(255,255,255,.08),
      rgba(255,255,255,.03)
    );

  backdrop-filter:blur(24px);

  border-radius:32px;

  padding:34px;

  border:1px solid rgba(255,255,255,.08);

  box-shadow:
    0 10px 40px rgba(0,0,0,.12);
}


/* ==========================================
💣 EMPTY
========================================== */

.empty-state{

  text-align:center;

  padding:50px 20px;
}

.empty-icon{

  font-size:72px;

  margin-bottom:18px;
}

.empty-state h3{

  margin:0;

  font-size:28px;

  font-weight:800;
}

.empty-state p{

  margin-top:14px;

  color:#94a3b8;

  line-height:1.7;

  max-width:520px;

  margin-inline:auto;
}


/* ==========================================
💣 HEADER
========================================== */

.score-header{

  display:flex;

  justify-content:space-between;

  align-items:flex-start;

  gap:24px;
}

.score-label{

  font-size:14px;

  text-transform:uppercase;

  letter-spacing:.08em;

  color:#94a3b8;
}

.score-value{

  font-size:76px;

  font-weight:900;

  line-height:1;

  margin-top:12px;
}

.score-subtitle{

  margin-top:10px;

  color:#94a3b8;

  font-size:14px;
}


/* ==========================================
💣 RISK
========================================== */

.risk-badge{

  display:flex;

  align-items:center;

  gap:10px;

  padding:12px 18px;

  border-radius:999px;

  font-weight:800;

  font-size:14px;

  text-transform:uppercase;
}

.risk-dot{

  width:10px;

  height:10px;

  border-radius:50%;
}

.low{

  background:
    rgba(16,185,129,.15);

  color:#10b981;
}

.low .risk-dot{

  background:#10b981;
}

.medium{

  background:
    rgba(245,158,11,.15);

  color:#f59e0b;
}

.medium .risk-dot{

  background:#f59e0b;
}

.high{

  background:
    rgba(239,68,68,.15);

  color:#ef4444;
}

.high .risk-dot{

  background:#ef4444;
}


/* ==========================================
💣 PROGRESS
========================================== */

.progress-section{

  margin-top:34px;
}

.progress-top{

  display:flex;

  justify-content:space-between;

  margin-bottom:10px;

  font-size:14px;

  color:#cbd5e1;
}

.progress-track{

  width:100%;

  height:16px;

  background:
    rgba(255,255,255,.06);

  border-radius:999px;

  overflow:hidden;
}

.progress-fill{

  height:100%;

  border-radius:999px;

  background:
    linear-gradient(
      90deg,
      #10b981,
      #3b82f6
    );

  transition:.4s ease;
}


/* ==========================================
💣 STATS
========================================== */

.stats-grid{

  display:grid;

  grid-template-columns:
    repeat(3,1fr);

  gap:18px;

  margin-top:34px;
}

.stat-card{

  display:flex;

  gap:14px;

  align-items:center;

  padding:18px;

  border-radius:22px;

  background:
    rgba(255,255,255,.04);

  border:1px solid rgba(255,255,255,.05);
}

.stat-icon{

  width:48px;

  height:48px;

  border-radius:16px;

  display:flex;

  align-items:center;

  justify-content:center;

  font-size:20px;

  font-weight:700;
}

.stat-icon.success{

  background:
    rgba(16,185,129,.15);

  color:#10b981;
}

.stat-icon.warning{

  background:
    rgba(245,158,11,.15);

  color:#f59e0b;
}

.stat-icon.info{

  background:
    rgba(59,130,246,.15);

  color:#3b82f6;
}

.stat-content{

  display:flex;

  flex-direction:column;
}

.stat-label{

  font-size:13px;

  color:#94a3b8;
}

.stat-value{

  margin-top:6px;

  font-size:18px;

  font-weight:800;
}


/* ==========================================
💣 EXPLANATION
========================================== */

.explanation-card{

  margin-top:30px;

  padding:24px;

  border-radius:24px;

  background:
    rgba(255,255,255,.04);

  border:1px solid rgba(255,255,255,.05);
}

.explanation-title{

  font-size:15px;

  font-weight:800;

  margin-bottom:14px;
}

.explanation-text{

  line-height:1.8;

  color:#cbd5e1;
}


/* ==========================================
💣 RECOMMENDATION
========================================== */

.recommendation-box{

  margin-top:24px;

  padding:22px;

  border-radius:24px;

  background:
    linear-gradient(
      135deg,
      rgba(59,130,246,.15),
      rgba(37,99,235,.08)
    );

  border:1px solid rgba(59,130,246,.18);
}

.recommendation-title{

  font-size:15px;

  font-weight:800;

  margin-bottom:10px;
}

.recommendation-box p{

  margin:0;

  line-height:1.7;

  color:#dbeafe;
}


/* ==========================================
💣 MOBILE
========================================== */

@media(max-width:900px){

  .score-card{

    padding:24px;
  }

  .score-header{

    flex-direction:column;
  }

  .score-value{

    font-size:54px;
  }

  .stats-grid{

    grid-template-columns:1fr;
  }
}

</style>