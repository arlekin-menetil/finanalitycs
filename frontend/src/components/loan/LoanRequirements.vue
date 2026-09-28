<script setup>
import { computed } from "vue"
import { useI18n } from "vue-i18n"
import { useRouter } from "vue-router"

const props = defineProps({
  product: {
    type: Object,
    default: () => ({}),
  },
})

const { t } = useI18n()
const router = useRouter()

// ==========================================
// ONLINE PRODUCT
// ==========================================

const isOnline = computed(() => {
  const value =
    props.product?.is_online_credit ??
    props.product?.is_online ??
    props.product?.online

  if (typeof value === "boolean") {
    return value
  }

  if (typeof value === "number") {
    return value === 1
  }

  if (typeof value === "string") {
    return [
      "true",
      "1",
      "yes",
      "online",
      "on",
    ].includes(value.trim().toLowerCase())
  }

  return false
})

// ==========================================
// BANK URL
// ==========================================

const bankUrl = computed(() => {
  return (
    props.product?.application_url ||
    props.product?.apply_url ||
    props.product?.url ||
    props.product?.website ||
    props.product?.bank?.website ||
    props.product?.bank?.url ||
    null
  )
})

const hasBankUrl = computed(() => {
  return Boolean(bankUrl.value)
})

// ==========================================
// BANK ID
// ==========================================

const bankId = computed(() => {
  return (
    props.product?.bank_id ||
    props.product?.bank?.id ||
    null
  )
})

// ==========================================
// OPEN BANK
// ==========================================

const openBank = () => {
  if (!bankUrl.value) {
    return
  }

  window.open(
    bankUrl.value,
    "_blank",
    "noopener,noreferrer",
  )
}

// ==========================================
// OPEN BRANCHES
// ==========================================

const openBranches = () => {
  if (!bankId.value) {
    return
  }

  router.push(
    `/app/bank/${bankId.value}/branches`,
  )
}
</script>

<template>
  <div class="card">

    <!-- ==========================================
         TITLE
    =========================================== -->

    <h3>
      📋 {{ t("loanRequirements.title") }}
    </h3>

    <!-- ==========================================
         DOCUMENT
    =========================================== -->

    <div class="requirement">

      <div class="icon">
        🪪
      </div>

      <div>
        <strong>
          {{ t("loanRequirements.document.title") }}
        </strong>

        <p>
          {{ t("loanRequirements.document.description") }}
        </p>
      </div>

    </div>

    <!-- ==========================================
         CITIZENSHIP
    =========================================== -->

    <div class="requirement">

      <div class="icon">
        🇺🇿
      </div>

      <div>
        <strong>
          {{ t("loanRequirements.citizenship.title") }}
        </strong>

        <p>
          {{ t("loanRequirements.citizenship.description") }}
        </p>
      </div>

    </div>

    <!-- ==========================================
         SOLVENCY
    =========================================== -->

    <div class="requirement">

      <div class="icon">
        💳
      </div>

      <div>
        <strong>
          {{ t("loanRequirements.solvency.title") }}
        </strong>

        <p>
          {{ t("loanRequirements.solvency.description") }}
        </p>
      </div>

    </div>

    <!-- ==========================================
         BANK DECISION
    =========================================== -->

    <div class="requirement">

      <div class="icon">
        🏦
      </div>

      <div>
        <strong>
          {{ t("loanRequirements.decision.title") }}
        </strong>

        <p>
          {{ t("loanRequirements.decision.description") }}
        </p>
      </div>

    </div>

    <!-- ==========================================
         ACTION
    =========================================== -->

    <div class="action">

      <!-- ========================================
           ONLINE + BANK URL
      ========================================= -->

      <template v-if="isOnline && hasBankUrl">

        <div class="action-info">

          <div class="action-icon">
            🌐
          </div>

          <div>
            <strong>
              {{ t("loanRequirements.online.title") }}
            </strong>

            <p>
              {{ t("loanRequirements.online.description") }}
            </p>
          </div>

        </div>

        <button
          type="button"
          class="action-button"
          @click="openBank"
        >
          {{ t("loanRequirements.online.button") }}

          <span>
            ↗
          </span>
        </button>

      </template>

      <!-- ========================================
           ONLINE WITHOUT URL
      ========================================= -->

      <template v-else-if="isOnline">

        <div class="action-info">

          <div class="action-icon">
            🌐
          </div>

          <div>
            <strong>
              {{ t("loanRequirements.online.title") }}
            </strong>

            <p>
              {{ t("loanRequirements.online.noUrl") }}
            </p>
          </div>

        </div>

      </template>

      <!-- ========================================
           OFFLINE / BANK BRANCH
      ========================================= -->

      <template v-else>

        <div class="action-info">

          <div class="action-icon">
            🏦
          </div>

          <div>
            <strong>
              {{ t("loanRequirements.offline.title") }}
            </strong>

            <p>
              {{ t("loanRequirements.offline.description") }}
            </p>
          </div>

        </div>

        <button
          v-if="bankId"
          type="button"
          class="action-button secondary"
          @click="openBranches"
        >
          {{ t("loanRequirements.offline.button") }}

          <span>
            →
          </span>
        </button>

      </template>

    </div>

  </div>
</template>

<style scoped>

.card {
  background: #fff;
  padding: 24px;
  border-radius: 18px;
  border: 1px solid #e5e7eb;
  margin-bottom: 24px;
}

h3 {
  margin: 0 0 20px;
  font-size: 18px;
  font-weight: 700;
}

.requirement {
  display: flex;
  gap: 16px;
  align-items: flex-start;
  padding: 14px 0;
  border-bottom: 1px solid #f1f5f9;
}

.requirement:last-of-type {
  border-bottom: none;
}

.icon {
  font-size: 22px;
  flex-shrink: 0;
}

strong {
  display: block;
  margin-bottom: 4px;
}

p {
  margin: 0;
  color: #64748b;
  line-height: 1.5;
}

.action {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e5e7eb;

  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.action-info {
  display: flex;
  align-items: flex-start;
  gap: 14px;
}

.action-icon {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: #f1f5f9;

  display: flex;
  align-items: center;
  justify-content: center;

  font-size: 20px;
  flex-shrink: 0;
}

.action-info strong {
  font-size: 15px;
}

.action-info p {
  font-size: 13px;
}

.action-button {
  border: none;
  background: #111827;
  color: #fff;

  padding: 11px 18px;
  border-radius: 10px;

  font-size: 14px;
  font-weight: 600;

  cursor: pointer;

  display: flex;
  align-items: center;
  gap: 8px;

  white-space: nowrap;

  transition:
    transform 0.2s ease,
    opacity 0.2s ease;
}

.action-button:hover {
  transform: translateY(-1px);
  opacity: 0.9;
}

.action-button.secondary {
  background: #f1f5f9;
  color: #111827;
}

@media (max-width: 640px) {

  .card {
    padding: 18px;
  }

  .action {
    flex-direction: column;
    align-items: stretch;
  }

  .action-button {
    width: 100%;
    justify-content: center;
  }

}

</style>