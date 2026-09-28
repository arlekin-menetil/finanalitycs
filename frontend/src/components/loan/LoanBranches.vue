<script setup>

import { computed } from "vue"
import { useI18n } from "vue-i18n"
import BankMap from "@/components/banks/BankMap.vue"

const props = defineProps({

  product: {
    type: Object,
    default: () => ({})
  },

  branches: {
    type: Array,
    default: () => []
  }

})

const { t } = useI18n()

// ==========================================
// 🌐 ONLINE PRODUCT
// ==========================================

const isOnlineProduct = computed(() => {

  return Boolean(
    props.product?.is_online
  )

})

</script>

<template>

<div class="card">

  <div class="header">

    <h3>
      📍 {{ t("loanBranches.title") }}
    </h3>

    <div class="bank-name">
      {{
        product?.bank?.name ||
        product?.bank_name ||
        t("loanBranches.bank")
      }}
    </div>

  </div>


  <!-- ===================================== -->
  <!-- 🌐 ONLINE PRODUCT -->
  <!-- ===================================== -->

  <div
    v-if="isOnlineProduct"
    class="online-block"
  >

    <div class="online-icon">
      🌐
    </div>

    <div class="online-title">
      {{ t("loanBranches.online.title") }}
    </div>

    <div class="online-text">

      {{ t("loanBranches.online.description") }}

    </div>

  </div>


  <!-- ===================================== -->
  <!-- 🏦 OFFLINE PRODUCT -->
  <!-- ===================================== -->

  <template v-else>

    <template v-if="branches.length">

      <BankMap
        :points="branches"
        height="500px"
      />

      <div class="branches-count">

        {{ t("loanBranches.found") }}:

        <strong>
          {{ branches.length }}
        </strong>

      </div>

    </template>

    <div
      v-else
      class="empty"
    >

      <div class="empty-icon">
        🏦
      </div>

      <div class="empty-title">
        {{ t("loanBranches.empty.title") }}
      </div>

      <div class="empty-text">

        {{ t("loanBranches.empty.description") }}

      </div>

    </div>

  </template>

</div>

</template>

<style scoped>

.card{

  background:#ffffff;

  border:1px solid #e5e7eb;

  border-radius:24px;

  padding:24px;

  margin-bottom:24px;

  box-shadow:
    0 4px 14px rgba(
      15,
      23,
      42,
      .04
    );

}

.header{

  display:flex;

  justify-content:space-between;

  align-items:center;

  margin-bottom:22px;

}

h3{

  margin:0;

  font-size:20px;

  font-weight:800;

  color:#0f172a;

}

.bank-name{

  font-size:14px;

  font-weight:600;

  color:#64748b;

}

.branches-count{

  margin-top:18px;

  padding-top:16px;

  border-top:1px solid #f1f5f9;

  color:#64748b;

  font-size:14px;

}

.branches-count strong{

  color:#0f172a;

  font-weight:800;

}


/* ===================================== */
/* 🌐 ONLINE */
/* ===================================== */

.online-block{

  min-height:260px;

  display:flex;

  flex-direction:column;

  align-items:center;

  justify-content:center;

  text-align:center;

}

.online-icon{

  width:88px;

  height:88px;

  display:flex;

  align-items:center;

  justify-content:center;

  border-radius:50%;

  background:#eff6ff;

  font-size:42px;

  margin-bottom:20px;

}

.online-title{

  font-size:22px;

  font-weight:800;

  color:#0f172a;

  margin-bottom:12px;

}

.online-text{

  max-width:480px;

  color:#64748b;

  line-height:1.7;

  font-size:15px;

}


/* ===================================== */
/* 🏦 EMPTY */
/* ===================================== */

.empty{

  min-height:260px;

  display:flex;

  flex-direction:column;

  align-items:center;

  justify-content:center;

  text-align:center;

}

.empty-icon{

  width:88px;

  height:88px;

  display:flex;

  align-items:center;

  justify-content:center;

  border-radius:50%;

  background:#f8fafc;

  font-size:42px;

  margin-bottom:18px;

}

.empty-title{

  font-size:20px;

  font-weight:800;

  color:#0f172a;

  margin-bottom:10px;

}

.empty-text{

  max-width:460px;

  color:#64748b;

  line-height:1.7;

}


/* ===================================== */
/* MAP */
/* ===================================== */

:deep(.leaflet-container){

  border-radius:18px;

  overflow:hidden;

}


/* ===================================== */
/* MOBILE */
/* ===================================== */

@media(max-width:768px){

  .header{

    flex-direction:column;

    align-items:flex-start;

    gap:8px;

  }

  .card{

    padding:20px;

  }

  .online-block,

  .empty{

    min-height:220px;

  }

}

</style>