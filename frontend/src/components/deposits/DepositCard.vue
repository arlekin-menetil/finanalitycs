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


// ==========================================
// 💣 OPEN DEPOSIT
// ==========================================

function openProduct() {

  if (!props.item?.id) {

    console.error(
      "INVALID DEPOSIT ID"
    )

    return
  }

  router.push(
    `/app/deposit/${props.item.id}`
  )
}


// ==========================================
// 💣 BANK NAME
// ==========================================

const bankName = computed(() => {

  return (
    props.item.bank_name ||
    props.item.bank?.name ||
    t("common.bank")
  )

})


// ==========================================
// 💣 PRODUCT NAME
// ==========================================

const productName = computed(() => {

  return (
    props.item.product_name ||
    props.item.name ||
    t("deposits.product")
  )

})


// ==========================================
// 💣 BANK LOGO
// ==========================================

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


// ==========================================
// 💣 RATE
// ==========================================

const rate = computed(() => {

  const value =
    props.item.interest_rate

  if (
    value === null ||
    value === undefined
  ) {
    return "—"
  }

  return `${value}%`

})


// ==========================================
// 💣 TERM
// ==========================================

const term = computed(() => {

  const value = Number(
    props.item.term
  )

  if (
    !value ||
    value <= 0
  ) {
    return "—"
  }


  if (value < 12) {

    if (value === 1) {
      return `1 ${t("deposits.month")}`
    }

    return `${value} ${t("deposits.months")}`
  }


  if (value === 12) {
    return `1 ${t("deposits.year")}`
  }


  const years = Math.floor(
    value / 12
  )

  const months =
    value % 12


  let yearsText = ""

  if (years === 1) {

    yearsText =
      `1 ${t("deposits.year")}`

  } else {

    yearsText =
      `${years} ${t("deposits.years")}`

  }


  if (!months) {
    return yearsText
  }


  const monthsText =
    months === 1
      ? `1 ${t("deposits.month")}`
      : `${months} ${t("deposits.months")}`


  return `${yearsText} ${monthsText}`

})


// ==========================================
// 💣 ONLINE
// ==========================================

const isOnline = computed(() => {

  return Boolean(
    props.item.is_online
  )

})

</script>


<template>

  <div class="card">


    <!-- ===================================== -->
    <!-- 💣 HEADER -->
    <!-- ===================================== -->

    <div class="header">

      <img
        :src="logo"
        class="logo"
        :alt="bankName"
      />


      <div class="header-info">

        <div class="bank-name">
          {{ bankName }}
        </div>

      </div>

    </div>


    <!-- ===================================== -->
    <!-- 💣 TITLE -->
    <!-- ===================================== -->

    <h3 class="title">
      {{ productName }}
    </h3>


    <!-- ===================================== -->
    <!-- 💣 TAGS -->
    <!-- ===================================== -->

    <div
      v-if="isOnline"
      class="tags"
    >

      <span class="tag online">
        {{ t("deposits.online") }}
      </span>

    </div>


    <!-- ===================================== -->
    <!-- 💣 STATS -->
    <!-- ===================================== -->

    <div class="stats">


      <div class="stat">

        <span>
          {{ t("deposits.interest") }}
        </span>

        <strong>
          {{ rate }}
        </strong>

      </div>


      <div class="stat">

        <span>
          {{ t("deposits.term") }}
        </span>

        <strong>
          {{ term }}
        </strong>

      </div>


      <div class="stat">

        <span>
          {{ t("deposits.currency") }}
        </span>

        <strong>
          {{
            item.currency ||
            item.raw_data?.currency ||
            "—"
          }}
        </strong>

      </div>


      <div class="stat">

        <span>
          {{ t("deposits.applicationMethod") }}
        </span>

        <strong>
          {{
            isOnline
              ? t("deposits.online")
              : t("deposits.branch")
          }}
        </strong>

      </div>


    </div>


    <!-- ===================================== -->
    <!-- 💣 ACTION -->
    <!-- ===================================== -->

    <div class="actions">

      <button
        class="btn"
        @click="openProduct"
      >
        {{ t("deposits.details") }}
      </button>

    </div>


  </div>

</template>


<style scoped>

.card {

  background: white;

  border-radius: 24px;

  padding: 24px;

  border: 1px solid #e5e7eb;

  display: flex;

  flex-direction: column;

  gap: 20px;

  transition: all .2s ease;
}

.card:hover {

  transform: translateY(-3px);

  box-shadow:
    0 12px 28px rgba(
      0,
      0,
      0,
      0.08
    );
}

.header {

  display: flex;

  align-items: center;

  gap: 14px;
}

.logo {

  width: 56px;

  height: 56px;

  object-fit: contain;

  flex-shrink: 0;

  background: #f8fafc;

  border-radius: 12px;

  padding: 4px;
}

.header-info {

  flex: 1;
}

.bank-name {

  font-size: 16px;

  font-weight: 700;

  color: #111827;
}

.title {

  margin: 0;

  font-size: 18px;

  font-weight: 700;

  line-height: 1.45;

  color: #0f172a;
}

.tags {

  display: flex;

  gap: 8px;

  flex-wrap: wrap;
}

.tag {

  padding: 6px 12px;

  border-radius: 999px;

  font-size: 12px;

  font-weight: 700;
}

.tag.online {

  background: #dcfce7;

  color: #166534;
}

.stats {

  display: grid;

  grid-template-columns: repeat(
    2,
    1fr
  );

  gap: 12px;
}

.stat {

  background: #f8fafc;

  border-radius: 16px;

  padding: 16px;
}

.stat span {

  display: block;

  font-size: 12px;

  color: #64748b;

  margin-bottom: 6px;
}

.stat strong {

  display: block;

  font-size: 18px;

  font-weight: 800;

  color: #111827;
}

.actions {

  margin-top: auto;
}

.btn {

  width: 100%;

  border: none;

  border-radius: 14px;

  background: #2563eb;

  color: white;

  padding: 14px;

  font-size: 14px;

  font-weight: 700;

  cursor: pointer;

  transition: .2s;
}

.btn:hover {

  background: #1d4ed8;
}

@media (max-width: 768px) {

  .card {

    padding: 20px;
  }

  .title {

    font-size: 16px;
  }

  .stats {

    grid-template-columns: 1fr;
  }
}

</style>