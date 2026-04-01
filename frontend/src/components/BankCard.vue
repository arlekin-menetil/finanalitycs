<template>
  <div class="card">

    <!-- 🏦 БАНК -->
    <div class="header">
      <h4>{{ bank.name }}</h4>
      <span class="bank">{{ bank.bank }}</span>
    </div>

    <!-- 💣 СТАВКА -->
    <div class="rate">
      {{ bank.interest_rate }}%
    </div>

    <!-- 💣 SCORE -->
    <div class="score">
      <span>Подходит:</span>
      <b>{{ Math.round(bank.score * 100) }}%</b>
    </div>

    <!-- 💬 ПРИЧИНЫ -->
    <ul class="reasons">
      <li v-for="(reason, i) in bank.reasons" :key="i">
        ✔ {{ reason }}
      </li>
    </ul>

    <!-- 🔥 КНОПКИ -->
    <div class="actions">
      <button class="apply" @click="handleClick">
        Оформить
      </button>

      <button class="details">
        Подробнее
      </button>
    </div>

  </div>
</template>

<script setup>
import { useRecommendationsStore } from "@/stores/recommendations"

const props = defineProps({
  bank: Object,
})

const recommendations = useRecommendationsStore()

const handleClick = async () => {
  await recommendations.click(props.bank.id)
}
</script>

<style scoped>
.card {
  background: white;
  padding: 20px;
  border-radius: 16px;
  margin-bottom: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06);
  transition: 0.2s ease;
}

.card:hover {
  transform: translateY(-3px);
}

/* 🏦 header */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.bank {
  font-size: 12px;
  color: #6b7280;
}

/* 💣 ставка */
.rate {
  font-size: 28px;
  font-weight: bold;
  margin: 12px 0;
}

/* 💣 score */
.score {
  font-size: 14px;
  margin-bottom: 10px;
}

/* 💬 причины */
.reasons {
  list-style: none;
  padding: 0;
  margin: 10px 0;
}

.reasons li {
  font-size: 13px;
  color: #374151;
  margin-bottom: 4px;
}

/* 🔥 кнопки */
.actions {
  display: flex;
  gap: 10px;
  margin-top: 12px;
}

.apply {
  flex: 1;
  padding: 10px;
  background: #111827;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
}

.details {
  flex: 1;
  padding: 10px;
  background: #f3f4f6;
  border: none;
  border-radius: 10px;
  cursor: pointer;
}
</style>