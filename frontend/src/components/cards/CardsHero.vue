<script setup>
import { computed } from "vue"
import { storeToRefs } from "pinia"

import { useCardsStore } from "@/stores/cards"

const store = useCardsStore()

const {
  items,
  totalCount
} = storeToRefs(store)

const totalBanks = computed(() => {

  const banks = new Set()

  items.value.forEach((card) => {

    if (card.bank_name) {
      banks.add(card.bank_name)
    }

  })

  return banks.size
})
</script>

<template>

  <section class="hero">

    <div class="hero-content">

      <div class="hero-left">

        <span class="hero-badge">
          CARD ENGINE
        </span>

        <h1>
          Банковские карты
        </h1>

        <p>
          Подбор дебетовых, кредитных
          и международных карт
          банков Узбекистана
        </p>

      </div>

      <div class="hero-stats">

        <div class="stat">

          <strong>
            {{ totalCount }}
          </strong>

          <span>
            Карт
          </span>

        </div>

        <div class="stat">

          <strong>
            {{ totalBanks }}
          </strong>

          <span>
            Банков
          </span>

        </div>

      </div>

    </div>

  </section>

</template>

<style scoped>

/* ==========================================
💳 HERO
========================================== */

.hero {

  margin-bottom: 38px;
}

.hero-content {

  position: relative;

  overflow: hidden;

  display: flex;

  justify-content: space-between;

  align-items: center;

  gap: 30px;

  padding: 42px;

  border-radius: 36px;

  background:
    linear-gradient(
      135deg,
      #2563eb,
      #1d4ed8,
      #1e40af
    );

  color: white;
}

.hero-content::before {

  content: "";

  position: absolute;

  inset: 0;

  background:
    radial-gradient(
      circle at top right,
      rgba(255,255,255,.15),
      transparent 35%
    );
}

.hero-left {

  position: relative;

  z-index: 2;
}

.hero-badge {

  display: inline-flex;

  align-items: center;

  padding: 10px 14px;

  border-radius: 999px;

  background:
    rgba(255,255,255,.12);

  font-size: 12px;

  font-weight: 800;

  letter-spacing: .08em;

  backdrop-filter: blur(10px);
}

.hero h1 {

  margin: 20px 0 0;

  font-size: 52px;

  font-weight: 900;

  line-height: 1;
}

.hero p {

  margin-top: 18px;

  font-size: 17px;

  opacity: .92;

  max-width: 700px;

  line-height: 1.8;
}

/* ==========================================
💳 STATS
========================================== */

.hero-stats {

  position: relative;

  z-index: 2;

  display: flex;

  gap: 18px;
}

.stat {

  min-width: 140px;

  padding: 24px;

  border-radius: 26px;

  background:
    rgba(255,255,255,.12);

  backdrop-filter: blur(12px);

  border: 1px solid rgba(255,255,255,.12);
}

.stat strong {

  display: block;

  font-size: 34px;

  font-weight: 900;

  margin-bottom: 10px;
}

.stat span {

  font-size: 14px;

  opacity: .9;
}

/* ==========================================
📱 MOBILE
========================================== */

@media (max-width: 900px) {

  .hero-content {

    flex-direction: column;

    align-items: flex-start;

    padding: 28px;
  }

  .hero h1 {

    font-size: 38px;
  }

  .hero-stats {

    width: 100%;
  }

  .stat {

    flex: 1;
  }
}

</style>