<script setup>
import { computed } from "vue"
import { useI18n } from "vue-i18n"

const { t } = useI18n()

const props = defineProps({
  score: {
    type: Object,
    required: true,
  },
})

// =====================================================
// SCORE
// =====================================================

const creditScore = computed(() =>
  Number(
    props.score.score || 0,
  ),
)

const risk = computed(() =>
  props.score.risk || "UNKNOWN",
)

// =====================================================
// COLOR
// =====================================================

const scoreColor = computed(() => {
  switch (risk.value) {
    case "A":
    case "A1":
    case "A2":
      return "#16a34a"

    case "B":
    case "B1":
    case "B2":
      return "#22c55e"

    case "C":
    case "C1":
    case "C2":
      return "#f59e0b"

    case "C3":
    case "D":
    case "D1":
    case "D2":
      return "#ef4444"

    default:
      return "#64748b"
  }
})

// =====================================================
// TEXT
// =====================================================

const riskText = computed(() => {
  switch (risk.value) {
    case "A":
    case "A1":
    case "A2":
      return t("scoreCard.risk.minimal")

    case "B":
    case "B1":
    case "B2":
      return t("scoreCard.risk.low")

    case "C":
    case "C1":
    case "C2":
      return t("scoreCard.risk.medium")

    case "C3":
      return t("scoreCard.risk.elevated")

    case "D":
    case "D1":
    case "D2":
      return t("scoreCard.risk.high")

    default:
      return t("scoreCard.risk.noData")
  }
})

// =====================================================
// PROGRESS
// =====================================================

const progress = computed(() => {
  const score = creditScore.value

  return Math.max(
    0,
    Math.min(
      100,
      (score / 1000) * 100,
    ),
  )
})
</script>

<template>
  <div class="card">
    <div class="header">
      <h2>
        ⭐ {{ t("scoreCard.title") }}
      </h2>

      <span class="badge">
        InfoKredit
      </span>
    </div>

    <div
      class="score"
      :style="{
        color: scoreColor,
      }"
    >
      {{ creditScore }}
    </div>

    <div
      class="risk"
      :style="{
        color: scoreColor,
      }"
    >
      {{ risk }}
    </div>

    <div class="description">
      {{ riskText }}
    </div>

    <div class="progress">
      <div
        class="fill"
        :style="{
          width: progress + '%',
          background: scoreColor,
        }"
      />
    </div>

    <div class="footer">
      <div>
        {{ t("scoreCard.rating") }}
      </div>

      <strong>
        {{ progress }}%
      </strong>
    </div>
  </div>
</template>

<style scoped>
.card {
  background: #ffffff;
  border-radius: 24px;
  padding: 32px;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
  height: 100%;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
}

.badge {
  background: #dbeafe;
  color: #2563eb;
  padding: 8px 16px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 700;
}

.score {
  font-size: 72px;
  font-weight: 800;
  line-height: 1;
}

.risk {
  margin-top: 12px;
  font-size: 28px;
  font-weight: 700;
}

.description {
  margin-top: 8px;
  color: #64748b;
  font-size: 15px;
}

.progress {
  margin-top: 28px;
  height: 14px;
  background: #e2e8f0;
  border-radius: 999px;
  overflow: hidden;
}

.fill {
  height: 100%;
  transition: 0.35s;
}

.footer {
  margin-top: 22px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 15px;
}

.footer strong {
  font-size: 18px;
}

@media (max-width: 768px) {
  .card {
    padding: 24px;
  }

  .score {
    font-size: 58px;
  }

  .risk {
    font-size: 24px;
  }
}
</style>