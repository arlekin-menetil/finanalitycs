<template>
  <div class="score-card">

    <!-- ❌ если нет данных -->
    <div v-if="!score" class="empty">
      Заполните профиль, чтобы увидеть скоринг
    </div>

    <!-- ✅ если есть -->
    <template v-else>

      <!-- 🔝 TOP -->
      <div class="score-top">
        <div>
          <div class="label">{{ $t("dashboard.score") }}</div>
          <div class="score-number">{{ score.credit_score }}</div>
        </div>

        <div :class="['risk-badge', riskClass]">
          {{ score.risk_category }}
        </div>
      </div>

      <!-- 💣 PROGRESS BAR -->
      <div class="progress-wrapper">
        <div class="progress-bar">
          <div
            class="progress-fill"
            :style="{ width: scorePercent + '%' }"
          />
        </div>
        <div class="progress-label">
          {{ score.credit_score }} / 850
        </div>
      </div>

      <!-- 💬 APPROVAL -->
      <div class="approval">
        Вероятность одобрения:
        <strong>{{ Math.round(score.approval_probability * 100) }}%</strong>
      </div>

      <!-- 💬 ПОЯСНЕНИЕ -->
      <div class="hint">
        {{ scoreExplanation }}
      </div>

    </template>
  </div>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
  score: Object,
})

const riskClass = computed(() => {
  if (!props.score) return ""
  return props.score.risk_category.toLowerCase()
})

// 💣 % от 850
const scorePercent = computed(() => {
  if (!props.score) return 0
  return (props.score.credit_score / 850) * 100
})

// 💣 пояснение
const scoreExplanation = computed(() => {
  if (!props.score) return ""

  const s = props.score.credit_score

  if (s > 750) return "Отличный рейтинг — лучшие условия"
  if (s > 650) return "Хороший рейтинг — высокий шанс одобрения"
  if (s > 550) return "Средний рейтинг — возможны ограничения"
  return "Низкий рейтинг — требуется улучшение профиля"
})
</script>

<style scoped>
.score-card {
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(14px);
  border-radius: 20px;
  padding: 36px;
  margin-bottom: 40px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* пусто */
.empty {
  text-align: center;
  opacity: 0.7;
}

/* header */
.score-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.label {
  font-size: 14px;
  opacity: 0.7;
}

.score-number {
  font-size: 64px;
  font-weight: 700;
  margin-top: 10px;
}

/* риск */
.risk-badge {
  padding: 8px 18px;
  border-radius: 30px;
  font-weight: 600;
  text-transform: uppercase;
}

/* цвета */
.low {
  background: #10b981;
  color: white;
}

.medium {
  background: #f59e0b;
  color: white;
}

.high {
  background: #ef4444;
  color: white;
}

/* 💣 progress */
.progress-wrapper {
  margin-top: 20px;
}

.progress-bar {
  width: 100%;
  height: 10px;
  background: rgba(255,255,255,0.1);
  border-radius: 20px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #10b981, #3b82f6);
  transition: 0.4s ease;
}

.progress-label {
  margin-top: 6px;
  font-size: 12px;
  opacity: 0.7;
}

/* approval */
.approval {
  margin-top: 20px;
  font-size: 16px;
}

/* пояснение */
.hint {
  margin-top: 10px;
  font-size: 14px;
  opacity: 0.7;
}
</style>