<script setup>
import { computed } from "vue"
import { useRouter } from "vue-router"
import { useI18n } from "vue-i18n"

const { t } = useI18n()

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
})

const router = useRouter()

function openProduct() {

  if (!props.item?.id) {
    return
  }

  router.push(
    `/app/card/${props.item.id}`
  )
}

const bankName = computed(() => {
  return (
    props.item.bank_name ||
    props.item.bank?.name ||
    t("common.bank")
  )
})

const currency = computed(() => {
  return (
    props.item.currency ||
    "—"
  )
})

const cardSystem = computed(() => {
  return (
    props.item.card_system ||
    props.item.raw_data?.card_system ||
    "—"
  )
})

const validity = computed(() => {
  return (
    props.item.validity_period ||
    props.item.raw_data?.validity_period ||
    "—"
  )
})

const issueCost = computed(() => {
  return (
    props.item.issue_cost ||
    props.item.raw_data?.issue_cost ||
    "—"
  )
})

const logo = computed(() => {

  const bank = (
    props.item.bank_name ||
    props.item.bank?.name ||
    ""
  )
    .toLowerCase()
    .replace(/\s+/g, "")

  return `/banks/${bank}.png`
})
</script>

<template>

  <div class="card">

    <!-- HEADER -->

    <div class="card-header">

      <img
        :src="logo"
        class="logo"
        alt="bank"
      />

      <div class="header-content">

        <div class="bank">
          {{ bankName }}
        </div>

        <h3 class="title">
          {{ item.name }}
        </h3>

      </div>

    </div>

    <!-- TAGS -->

    <div class="tags">

      <span class="tag">
        {{ cardSystem }}
      </span>

      <span class="tag">
        {{ currency }}
      </span>

      <span
        v-if="item.is_online"
        class="tag online"
      >
        {{ t("cards.online") }}
      </span>

    </div>

    <!-- STATS -->

    <div class="stats">

      <div class="stat">

        <span>
          {{ t("cards.currency") }}
        </span>

        <strong>
          {{ currency }}
        </strong>

      </div>

      <div class="stat">

        <span>
          {{ t("cards.system") }}
        </span>

        <strong>
          {{ cardSystem }}
        </strong>

      </div>

      <div class="stat">

        <span>
          {{ t("cards.term") }}
        </span>

        <strong>
          {{ validity }}
        </strong>

      </div>

      <div class="stat">

        <span>
          {{ t("cards.issue") }}
        </span>

        <strong>
          {{ issueCost }}
        </strong>

      </div>

    </div>

    <!-- BUTTON -->

    <button
      class="btn"
      @click="openProduct"
    >
      {{ t("cards.details") }}
    </button>

  </div>

</template>

<style scoped>

.card {
  background: white;
  border-radius: 28px;
  padding: 24px;
  border: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  gap: 18px;
  transition: .25s;
  min-height: 320px;
}

.card:hover {
  transform: translateY(-3px);
  box-shadow:
    0 10px 25px rgba(0,0,0,.08);
}

/* HEADER */

.card-header {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.logo {
  width: 56px;
  height: 56px;
  object-fit: contain;
  border-radius: 14px;
  background: white;
  border: 1px solid #e5e7eb;
  padding: 6px;
  flex-shrink: 0;
}

.header-content {
  flex: 1;
}

.bank {
  color: #64748b;
  font-size: 14px;
  margin-bottom: 4px;
}

.title {
  font-size: 20px;
  font-weight: 700;
  line-height: 1.3;
  margin: 0;
}

/* TAGS */

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  padding: 6px 12px;
  border-radius: 999px;
  background: #f1f5f9;
  font-size: 12px;
  font-weight: 600;
  color: #334155;
}

.online {
  background: #dcfce7;
  color: #166534;
}

/* STATS */

.stats {
  display: grid;
  grid-template-columns:
    repeat(2,1fr);
  gap: 12px;
}

.stat {
  background: #f8fafc;
  border-radius: 16px;
  padding: 14px;
}

.stat span {
  display: block;
  color: #64748b;
  font-size: 12px;
  margin-bottom: 6px;
}

.stat strong {
  font-size: 18px;
  font-weight: 700;
}

/* BUTTON */

.btn {
  margin-top: auto;
  height: 44px;
  border: none;
  border-radius: 14px;
  background: #2563eb;
  color: white;
  font-weight: 700;
  cursor: pointer;
  transition: .2s;
}

.btn:hover {
  background: #1d4ed8;
}

</style>