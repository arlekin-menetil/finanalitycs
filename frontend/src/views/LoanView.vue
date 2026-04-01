<script setup>

import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useI18n } from "vue-i18n"
import api from "@/api/axios"
import { useRecommendationsStore } from "@/stores/recommendations"

const route = useRoute()
const router = useRouter()
const { t } = useI18n()

const recommendationsStore = useRecommendationsStore()

const loading = ref(true)
const error = ref(false)

const product = ref(null)


// ==========================================
// 🚀 LOAD
// ==========================================
onMounted(async () => {
  try {

    const id = route.params.id

    const res = await api.get(`/banks/products/${id}/`)
    product.value = res.data

  } catch (e) {

    console.error("Loan load error:", e)
    error.value = true

  } finally {

    loading.value = false

  }
})


// ==========================================
// 💣 APPLY
// ==========================================
async function apply(){

  if(!product.value) return

  try{

    await recommendationsStore.click(
      product.value.id,
      product.value.ranking_score || 0
    )

    await recommendationsStore.apply(product.value.id)

    if(product.value.website){
      window.open(product.value.website, "_blank")
    }

  }catch(e){
    console.error("Apply error:", e)
  }

}


// ==========================================
// 🔙 BACK
// ==========================================
function goBack(){
  router.back()
}


// ==========================================
// 💰 FORMAT
// ==========================================
function formatMoney(v){
  if(!v) return "-"
  return new Intl.NumberFormat("ru-RU").format(v) + " UZS"
}

</script>


<template>

<div class="loan-page">

<!-- LOADING -->
<div v-if="loading" class="state">
{{ t("loan.loading") || "Загрузка..." }}
</div>

<!-- ERROR -->
<div v-else-if="error" class="state error">
{{ t("loan.error") || "Ошибка загрузки продукта" }}
</div>

<!-- CONTENT -->
<div v-else-if="product">

<!-- HEADER -->
<div class="header">

<button class="back" @click="goBack">
← {{ t("loan.back") || "Назад" }}
</button>

<h1>
{{ product.product_name }}
</h1>

<p class="bank">
🏦 {{ product.bank_name }}
</p>

</div>


<!-- MAIN GRID -->
<div class="grid">

<!-- LEFT -->
<div class="card main">

<div class="rate">
{{ product.interest_rate ?? "-" }}%
</div>

<div class="label">
{{ t("loan.interestRate") || "Процентная ставка" }}
</div>

<div class="match">

{{ t("loan.match") || "Подходит" }}:
<strong>{{ Math.round(product.ranking_score || 0) }}%</strong>

</div>

</div>


<!-- RIGHT -->
<div class="card">

<div class="info-row">
<span>{{ t("loan.limit") || "Лимит" }}</span>
<strong>{{ formatMoney(product.max_amount || product.loan_limit_hint) }}</strong>
</div>

<div class="info-row">
<span>{{ t("loan.term") || "Срок" }}</span>
<strong>{{ product.term || "-" }} {{ t("loan.months") || "мес" }}</strong>
</div>

<div class="info-row">
<span>{{ t("loan.approval") || "Одобрение" }}</span>
<strong>{{ product.approval_probability ?? "-" }}%</strong>
</div>

</div>

</div>


<!-- DESCRIPTION -->
<div class="card">

<h3>{{ t("loan.description") || "Описание" }}</h3>

<p>
{{ product.description || "Описание продукта отсутствует" }}
</p>

</div>


<!-- ACTIONS -->
<div class="actions">

<button class="apply" @click="apply">
🔥 {{ t("loan.apply") || "Оформить онлайн" }}
</button>

<button class="secondary" @click="router.push('/recommendations')">
{{ t("loan.more") || "Другие предложения" }}
</button>

</div>

</div>

</div>

</template>


<style scoped>

.loan-page{
max-width:1000px;
margin:auto;
padding:40px;
}

/* STATE */

.state{
padding:40px;
text-align:center;
}

.error{
color:#ef4444;
}

/* HEADER */

.header{
margin-bottom:30px;
}

.back{
background:none;
border:none;
cursor:pointer;
margin-bottom:10px;
}

.bank{
color:#6b7280;
margin-top:6px;
}

/* GRID */

.grid{
display:grid;
grid-template-columns:1fr 1fr;
gap:20px;
margin-bottom:20px;
}

.card{
background:white;
padding:20px;
border-radius:16px;
border:1px solid #e5e7eb;
}

.main{
text-align:center;
}

.rate{
font-size:42px;
font-weight:700;
}

.label{
font-size:13px;
color:#6b7280;
margin-top:6px;
}

.match{
margin-top:10px;
font-size:14px;
}

/* INFO */

.info-row{
display:flex;
justify-content:space-between;
margin-bottom:12px;
}

/* ACTIONS */

.actions{
display:flex;
gap:10px;
margin-top:20px;
}

.apply{
flex:1;
background:#16a34a;
color:white;
border:none;
padding:12px;
border-radius:10px;
cursor:pointer;
}

.apply:hover{
background:#15803d;
}

.secondary{
flex:1;
background:#f3f4f6;
border:none;
padding:12px;
border-radius:10px;
cursor:pointer;
}

/* MOBILE */

@media (max-width:768px){

.grid{
grid-template-columns:1fr;
}

.loan-page{
padding:20px;
}

}

</style>