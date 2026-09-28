<script setup>

import { computed } from "vue"
import { useI18n } from "vue-i18n"

const props = defineProps({
  product: {
    type: Object,
    default: () => ({})
  }
})

defineEmits([
  "back"
])

const { t } = useI18n()

// ==========================================
// 🏦 LOGO
// ==========================================
const logo = computed(() => {

  const bank = (
    props.product?.bank?.name ||
    props.product?.bank_name ||
    ""
  )
    .toLowerCase()
    .replace(/\s+/g, "")

  return `/banks/${bank}.png`

})

</script>

<template>

<div>

  <!-- BACK -->

  <div class="back-wrapper">

    <button
      class="back-btn"
      @click="$emit('back')"
    >
      ← {{ t("common.back") }}
    </button>

  </div>

  <!-- HERO -->

  <div
    v-if="product"
    class="hero"
  >

    <img
      :src="logo"
      class="hero-logo"
      :alt="
        product.bank?.name ||
        product.bank_name ||
        t('recommendations.bank')
      "
    />

    <div class="hero-content">

      <div class="bank">

        {{
          product.bank?.name ||
          product.bank_name ||
          t("common.unknownBank")
        }}

      </div>

      <h1>

        {{
          product.name ||
          t("recommendations.product")
        }}

      </h1>

    </div>

  </div>

  <div
    v-else
    class="loading"
  >

    {{ t("common.loading") }}

  </div>

</div>

</template>

<style scoped>

/* ==========================================
   BACK
========================================== */

.back-wrapper{

  margin-bottom:20px;
}

.back-btn{

  border:none;

  background:transparent;

  color:#2563eb;

  font-size:15px;

  font-weight:700;

  cursor:pointer;

  padding:0;
}

.back-btn:hover{

  color:#1d4ed8;
}

/* ==========================================
   HERO
========================================== */

.hero{

  background:white;

  border:1px solid #e5e7eb;

  border-radius:24px;

  padding:28px;

  margin-bottom:24px;

  display:flex;

  align-items:center;

  gap:20px;
}

.hero-logo{

  width:72px;

  height:72px;

  object-fit:contain;

  background:#f8fafc;

  border-radius:16px;

  padding:6px;

  flex-shrink:0;
}

.hero-content{

  flex:1;
}

.bank{

  color:#64748b;

  font-size:14px;

  font-weight:600;

  margin-bottom:8px;
}

.hero h1{

  margin:0;

  color:#111827;

  font-size:30px;

  font-weight:800;

  line-height:1.3;
}

/* ==========================================
   LOADING
========================================== */

.loading{

  color:#94a3b8;
}

/* ==========================================
   MOBILE
========================================== */

@media(max-width:768px){

  .hero{

    flex-direction:column;

    align-items:flex-start;
  }

  .hero-logo{

    width:64px;

    height:64px;
  }

  .hero h1{

    font-size:24px;
  }

}

</style>