<script setup>
import { useI18n } from "vue-i18n"

const { t } = useI18n()

const integrations = [
  {
    icon: "🏦",
    key: "bank",
    name: "Bank.uz",
    class: "bank",
  },
  {
    icon: "💰",
    key: "deposit",
    name: "Deposit.uz",
    class: "deposit",
  },
  {
    icon: "📊",
    key: "analytics",
    name: "BankXizmatlari",
    class: "analytics",
  },
  {
    icon: "🪪",
    key: "gov",
    name: "MyGov",
    class: "gov",
  },
  {
    icon: "📈",
    key: "credit",
    name: "Infokredit",
    class: "credit",
  },
]
</script>

<template>
  <section class="integrations">
    <div class="integrations__container">

      <!-- HEADER -->
      <div class="integrations__header">
        <div class="integrations__badge">
          <span class="integrations__badge-icon">🔗</span>
          <span>{{ t("data.badge") }}</span>
        </div>

        <h2 class="integrations__title">
          {{ t("data.title") }}
        </h2>

        <p class="integrations__desc">
          {{ t("data.desc") }}
        </p>
      </div>

      <!-- CARDS -->
      <div class="integrations__grid">
        <article
          v-for="item in integrations"
          :key="item.key"
          class="integration-card"
          :class="`integration-card--${item.class}`"
        >
          <div class="integration-card__top">
            <div class="integration-card__icon">
              {{ item.icon }}
            </div>

            <div class="integration-card__status">
              <span class="integration-card__status-dot"></span>
              {{ t("data.connected") }}
            </div>
          </div>

          <div class="integration-card__content">
            <h3 class="integration-card__title">
              {{ item.name }}
            </h3>

            <p class="integration-card__description">
              {{ t(`data.${item.key}`) }}
            </p>
          </div>

          <div class="integration-card__footer">
            <span class="integration-card__source">
              {{ t("data.source") }}
            </span>

            <span class="integration-card__arrow">
              →
            </span>
          </div>
        </article>
      </div>

      <!-- UPDATE INFO -->
      <div class="integrations__update">
        <div class="integrations__update-icon">
          ↻
        </div>

        <div>
          <strong>
            {{ t("data.updateTitle") }}
          </strong>

          <p>
            {{ t("data.updateDesc") }}
          </p>
        </div>
      </div>

    </div>
  </section>
</template>

<style scoped>
.integrations {
  position: relative;
  padding: 80px 20px;
  background:
    radial-gradient(
      circle at 10% 20%,
      rgba(37, 99, 235, 0.05),
      transparent 32%
    ),
    radial-gradient(
      circle at 90% 80%,
      rgba(14, 165, 233, 0.05),
      transparent 32%
    ),
    #f8fafc;
}

.integrations__container {
  width: 100%;
  max-width: 1180px;
  margin: 0 auto;
}

/* =========================
   HEADER
========================= */

.integrations__header {
  max-width: 720px;
  margin: 0 auto 42px;
  text-align: center;
}

.integrations__badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 7px 13px;
  margin-bottom: 16px;

  border: 1px solid #dbeafe;
  border-radius: 999px;

  background: #eff6ff;
  color: #2563eb;

  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.02em;
}

.integrations__badge-icon {
  font-size: 14px;
}

.integrations__title {
  margin: 0 0 14px;

  color: #0f172a;

  font-size: clamp(28px, 4vw, 38px);
  line-height: 1.15;
  font-weight: 800;
  letter-spacing: -0.03em;
}

.integrations__desc {
  max-width: 650px;
  margin: 0 auto;

  color: #64748b;

  font-size: 15px;
  line-height: 1.7;
}

/* =========================
   GRID
========================= */

.integrations__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

/* =========================
   CARD
========================= */

.integration-card {
  position: relative;

  min-height: 220px;
  padding: 22px;

  display: flex;
  flex-direction: column;

  overflow: hidden;

  background: rgba(255, 255, 255, 0.9);

  border: 1px solid #e2e8f0;
  border-radius: 20px;

  box-shadow:
    0 4px 20px rgba(15, 23, 42, 0.04);

  transition:
    transform 0.25s ease,
    box-shadow 0.25s ease,
    border-color 0.25s ease;
}

.integration-card::before {
  content: "";

  position: absolute;
  top: 0;
  left: 0;
  right: 0;

  height: 3px;

  background: #2563eb;

  opacity: 0;

  transition: opacity 0.25s ease;
}

.integration-card:hover {
  transform: translateY(-5px);

  border-color: #cbd5e1;

  box-shadow:
    0 18px 45px rgba(15, 23, 42, 0.09);
}

.integration-card:hover::before {
  opacity: 1;
}

/* =========================
   CARD TOP
========================= */

.integration-card__top {
  display: flex;
  align-items: center;
  justify-content: space-between;

  margin-bottom: 24px;
}

.integration-card__icon {
  width: 52px;
  height: 52px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 15px;

  background: #f1f5f9;

  font-size: 25px;

  transition:
    transform 0.25s ease,
    background 0.25s ease;
}

.integration-card:hover .integration-card__icon {
  transform: scale(1.07);
}

/* =========================
   STATUS
========================= */

.integration-card__status {
  display: inline-flex;
  align-items: center;
  gap: 6px;

  padding: 5px 9px;

  border-radius: 999px;

  background: #f0fdf4;
  color: #15803d;

  font-size: 11px;
  font-weight: 700;
}

.integration-card__status-dot {
  width: 6px;
  height: 6px;

  border-radius: 50%;

  background: #22c55e;

  box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.12);
}

/* =========================
   CONTENT
========================= */

.integration-card__content {
  flex: 1;
}

.integration-card__title {
  margin: 0 0 8px;

  color: #0f172a;

  font-size: 18px;
  font-weight: 750;
  letter-spacing: -0.01em;
}

.integration-card__description {
  margin: 0;

  color: #64748b;

  font-size: 13px;
  line-height: 1.65;
}

/* =========================
   FOOTER
========================= */

.integration-card__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;

  padding-top: 18px;
  margin-top: 18px;

  border-top: 1px solid #f1f5f9;
}

.integration-card__source {
  color: #94a3b8;

  font-size: 11px;
  font-weight: 600;
}

.integration-card__arrow {
  color: #94a3b8;

  font-size: 18px;

  transition:
    transform 0.25s ease,
    color 0.25s ease;
}

.integration-card:hover .integration-card__arrow {
  color: #2563eb;
  transform: translateX(4px);
}

/* =========================
   DIFFERENT CARD COLORS
========================= */

.integration-card--bank:hover::before {
  background: #2563eb;
}

.integration-card--deposit:hover::before {
  background: #16a34a;
}

.integration-card--analytics:hover::before {
  background: #7c3aed;
}

.integration-card--gov:hover::before {
  background: #0891b2;
}

.integration-card--credit:hover::before {
  background: #ea580c;
}

/* =========================
   UPDATE BLOCK
========================= */

.integrations__update {
  max-width: 680px;

  display: flex;
  align-items: center;
  gap: 14px;

  margin: 28px auto 0;
  padding: 15px 18px;

  border: 1px solid #e2e8f0;
  border-radius: 15px;

  background: rgba(255, 255, 255, 0.75);
}

.integrations__update-icon {
  width: 38px;
  height: 38px;

  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 11px;

  background: #eff6ff;
  color: #2563eb;

  font-size: 19px;
  font-weight: 700;
}

.integrations__update strong {
  display: block;

  margin-bottom: 2px;

  color: #334155;

  font-size: 12px;
}

.integrations__update p {
  margin: 0;

  color: #94a3b8;

  font-size: 11px;
  line-height: 1.5;
}

/* =========================
   TABLET
========================= */

@media (max-width: 900px) {
  .integrations {
    padding: 65px 20px;
  }

  .integrations__grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* =========================
   MOBILE
========================= */

@media (max-width: 600px) {
  .integrations {
    padding: 50px 16px;
  }

  .integrations__header {
    margin-bottom: 30px;
  }

  .integrations__title {
    font-size: 28px;
  }

  .integrations__desc {
    font-size: 14px;
  }

  .integrations__grid {
    grid-template-columns: 1fr;
    gap: 14px;
  }

  .integration-card {
    min-height: 195px;
    padding: 18px;
  }

  .integration-card__top {
    margin-bottom: 20px;
  }

  .integrations__update {
    align-items: flex-start;
  }
}
</style>