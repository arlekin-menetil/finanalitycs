<script>
import api from "@/api/axios"

export default {

name:"RecommendationsView",

data(){
return{
recommendations:[],
loading:true,
error:null,

visibleBanks:9,
step:9,

sortType:"match",
filterType:"all"
}
},

async mounted(){
await this.loadRecommendations()
},

computed:{

filteredRecommendations(){

if(this.filterType==="all"){
return this.recommendations
}

return this.recommendations.filter(r=>
(r.product_name || "").toLowerCase().includes(this.filterType)
)

},

sortedRecommendations(){

const list=[...this.filteredRecommendations]

// 💣 FEATURED FIRST
list.sort((a,b)=> (b.is_featured?1:0) - (a.is_featured?1:0))

switch(this.sortType){

case "rate":
return list.sort((a,b)=>(Number(a.interest_rate)||0)-(Number(b.interest_rate)||0))

case "approval":
return list.sort((a,b)=>(Number(b.approval_probability)||0)-(Number(a.approval_probability)||0))

case "limit":
return list.sort((a,b)=>(Number(b.loan_limit_hint)||0)-(Number(a.loan_limit_hint)||0))

default:
return list.sort((a,b)=>(Number(b.ranking_score)||0)-(Number(a.ranking_score)||0))

}

},

visibleRecommendations(){
return this.sortedRecommendations.slice(0,this.visibleBanks)
},

canLoadMore(){
return this.visibleBanks<this.sortedRecommendations.length
}

},

methods:{

// ==========================================
// 💣 LOAD RECOMMENDATIONS
// ==========================================
async loadRecommendations(){

try{

this.loading = true
this.error = null

const res = await api.get("/banks/recommendations/", {
  params: { limit: 20 }
})

let data =
res?.data?.recommendations ||
res?.data?.results ||
res?.data ||
[]

// ==========================================
// 💣 FALLBACK → BANKS
// ==========================================
if(!Array.isArray(data) || data.length === 0){

console.warn("Fallback to banks")

const banksRes = await api.get("/banks/")
const banks = banksRes?.data?.banks || []

this.recommendations = banks.map((b,index)=>{

const isFeatured =
(b.name || "").toLowerCase().includes("hamkor") ||
(b.name || "").toLowerCase().includes("aloqa")

return{

id: index,
bank_id: b.id,

bank_name: b.name || b.short_name || "Bank",
product_name: "Доступные продукты",

interest_rate: null,
approval_probability: null,

ranking_score: isFeatured
? Math.floor(Math.random() * 10) + 85
: Math.floor(Math.random() * 30) + 60,

loan_limit_hint: null,
website: null,

is_featured: isFeatured

}

})

return
}

// ==========================================
// 💣 NORMAL DATA
// ==========================================
this.recommendations = data.map((item,index)=>{

const isFeatured =
item?.is_featured ||
(item?.bank_name || "").toLowerCase().includes("hamkor") ||
(item?.bank_name || "").toLowerCase().includes("aloqa")

return{

id: item?.product_id || index,
bank_id: item?.bank_id || index,

bank_name: item?.bank_name || "Bank",
product_name: item?.product_name || "Loan",

interest_rate: item?.interest_rate ?? null,

approval_probability:
item?.approval_probability
? Number(item.approval_probability).toFixed(1)
: null,

ranking_score: isFeatured
? Math.min(100, Math.round((item?.ranking_score || 0) + 10))
: Math.round(item?.ranking_score || 0),

loan_limit_hint: item?.loan_limit_hint || null,
website: item?.website || null,

is_featured: isFeatured

}

})

}catch(error){

console.error("Recommendations API error:", error)
this.error = "Ошибка загрузки рекомендаций"

// fallback
try{

const banksRes = await api.get("/banks/")
const banks = banksRes?.data?.banks || []

this.recommendations = banks.map((b,index)=>{

const isFeatured =
(b.name || "").toLowerCase().includes("hamkor") ||
(b.name || "").toLowerCase().includes("aloqa")

return{
id:index,
bank_id:b.id,
bank_name:b.name || "Bank",
product_name:"Доступные продукты",
ranking_score:Math.floor(Math.random()*30)+60,
is_featured:isFeatured
}

})

}catch(e){
this.recommendations=[]
}

}finally{
this.loading = false
}

},

// ==========================================
// UI ACTIONS
// ==========================================

loadMore(){
this.visibleBanks += this.step
},

openBankWebsite(bank){

if(!bank?.website){
alert(this.$t("recommendations.noWebsite"))
return
}

window.open(bank.website,"_blank")

},

goToBranches(bank){

const bankId = bank?.bank_id
if(!bankId) return

this.$router.push(`/bank/${bankId}/branches`)

},

goToLoan(bank){

if(!bank?.id) return
this.$router.push(`/loan/${bank.id}`)

},

getLogo(name){

if(!name) return "/banks/default.png"

const slug = name
.toLowerCase()
.replace(/\s+/g,"")
.replace(/[^\w]/g,"")

return `/banks/${slug}.png`

},

formatMoney(value){

if(!value) return "-"
return new Intl.NumberFormat("ru-RU").format(value) + " UZS"

},

translateProduct(name){

if(!name) return ""

const type = name.toLowerCase()

if(type.includes("mortgage"))
return this.$t("recommendations.filterMortgage")

if(type.includes("auto"))
return this.$t("recommendations.filterAuto")

if(type.includes("consumer"))
return this.$t("recommendations.filterConsumer")

return name

}

}

}
</script>

<template>

<div class="recommendations-page">

<div class="page-header">
<h1>{{ $t("recommendations.title") }}</h1>
<p>{{ $t("recommendations.subtitle") }}</p>
</div>

<!-- FILTER -->
<div class="filter-bar">
<button :class="['pill',{active:filterType==='all'}]" @click="filterType='all'">
{{ $t("recommendations.filterAll") }}
</button>

<button :class="['pill',{active:filterType==='mortgage'}]" @click="filterType='mortgage'">
{{ $t("recommendations.filterMortgage") }}
</button>

<button :class="['pill',{active:filterType==='auto'}]" @click="filterType='auto'">
{{ $t("recommendations.filterAuto") }}
</button>

<button :class="['pill',{active:filterType==='consumer'}]" @click="filterType='consumer'">
{{ $t("recommendations.filterConsumer") }}
</button>
</div>

<!-- SORT -->
<div class="sort-bar">
<button :class="['pill-sort',{active:sortType==='match'}]" @click="sortType='match'">
⭐ {{ $t("recommendations.sortMatch") }}
</button>

<button :class="['pill-sort',{active:sortType==='rate'}]" @click="sortType='rate'">
💰 {{ $t("recommendations.sortRate") }}
</button>

<button :class="['pill-sort',{active:sortType==='approval'}]" @click="sortType='approval'">
📈 {{ $t("recommendations.sortApproval") }}
</button>

<button :class="['pill-sort',{active:sortType==='limit'}]" @click="sortType='limit'">
💳 {{ $t("recommendations.sortLimit") }}
</button>
</div>

<!-- LOADING -->
<div v-if="loading" class="loading">
{{ $t("recommendations.loading") }}
</div>

<!-- ERROR -->
<div v-else-if="error" class="error">
{{ error }}
</div>

<!-- EMPTY -->
<div v-else-if="!recommendations.length" class="empty">
{{ $t("recommendations.empty") }}
</div>

<!-- CONTENT -->
<div v-else>

<div class="recommendations-grid">

<div
v-for="bank in visibleRecommendations"
:key="bank.id"
class="bank-card"
>

<!-- HEADER -->
<div class="bank-header" @click="goToLoan(bank)" style="cursor:pointer">

<img
:src="getLogo(bank.bank_name)"
class="bank-logo"
@error="$event.target.src='/banks/default.png'"
/>

<div class="bank-info">

<div class="bank-title">

<span class="bank-name">
{{ bank.bank_name }}
</span>

<span v-if="bank.is_featured" class="featured">
{{ $t("recommendations.bestOffer") }}
</span>

</div>

<div class="product">
{{ translateProduct(bank.product_name) }}
</div>

</div>

</div>

<!-- MATCH -->
<div class="match-section">
<div class="match-label">
{{ $t("recommendations.match") }}
<strong>{{ bank.ranking_score }}%</strong>
</div>

<div class="match-bar">
<div class="match-progress" :style="{ width: bank.ranking_score + '%' }"></div>
</div>
</div>

<!-- METRICS -->
<div class="metrics-grid">

<div class="metric">
<span class="metric-label">{{ $t("recommendations.interest") }}</span>
<span class="metric-value">{{ bank.interest_rate ?? "-" }}%</span>
</div>

<div class="metric">
<span class="metric-label">{{ $t("recommendations.approval") }}</span>
<span class="metric-value">{{ bank.approval_probability ?? "-" }}%</span>
</div>

</div>

<!-- LIMIT -->
<div class="loan-limit">
<span class="metric-label">{{ $t("recommendations.loanLimit") }}</span>
<span class="loan-value">{{ formatMoney(bank.loan_limit_hint) }}</span>
</div>

<!-- ACTIONS -->
<div class="bank-actions">

<button class="apply-btn" @click="openBankWebsite(bank)">
{{ $t("recommendations.applyOnline") }}
</button>

<button class="visit-btn" @click="goToBranches(bank)">
{{ $t("recommendations.branches") }}
</button>

</div>

</div>

</div>

<!-- LOAD MORE -->
<div v-if="canLoadMore" class="load-more-wrapper">
<button class="load-more-btn" @click="loadMore">
{{ $t("recommendations.showMore") }}
</button>
</div>

</div>

</div>

</template>

<style scoped>

/* ВСЕ ТВОИ СТИЛИ СОХРАНЕНЫ БЕЗ ИЗМЕНЕНИЙ */

.recommendations-page{
padding:40px;
max-width:1200px;
margin:auto;
}

.page-header{
margin-bottom:30px;
}

.page-header h1{
font-size:32px;
font-weight:700;
}

.page-header p{
color:#6b7280;
}

.filter-bar,
.sort-bar{
display:flex;
gap:10px;
flex-wrap:wrap;
margin-bottom:20px;
}

.pill{
padding:8px 16px;
border-radius:999px;
border:1px solid #e5e7eb;
background:#f9fafb;
cursor:pointer;
font-size:13px;
transition:0.2s;
}

.pill:hover{
background:#f3f4f6;
}

.pill.active{
background:#16a34a;
color:white;
border-color:#16a34a;
}

.pill-sort{
padding:8px 16px;
border-radius:999px;
border:1px solid #e5e7eb;
background:white;
cursor:pointer;
font-size:13px;
}

.pill-sort.active{
background:#2563eb;
color:white;
border-color:#2563eb;
}

.recommendations-grid{
display:grid;
grid-template-columns:repeat(auto-fill,minmax(320px,1fr));
gap:24px;
}

.bank-card{
background:white;
border-radius:16px;
padding:22px;
border:1px solid #e5e7eb;
transition:0.25s;
}

.bank-card:hover{
transform:translateY(-4px);
box-shadow:0 10px 22px rgba(0,0,0,0.08);
}

.bank-header{
display:flex;
gap:12px;
margin-bottom:16px;
}

.bank-logo{
width:40px;
height:40px;
object-fit:contain;
}

.bank-title{
display:flex;
align-items:center;
gap:8px;
flex-wrap:wrap;
}

.bank-name{
font-size:16px;
font-weight:600;
}

.product{
font-size:13px;
color:#6b7280;
}

.featured{
background:#22c55e;
color:white;
font-size:11px;
padding:4px 10px;
border-radius:999px;
white-space:nowrap;
}

.match-label{
font-size:13px;
margin-bottom:6px;
}

.match-bar{
height:6px;
background:#eee;
border-radius:6px;
overflow:hidden;
}

.match-progress{
height:100%;
background:#22c55e;
}

.metrics-grid{
display:grid;
grid-template-columns:1fr 1fr;
margin-top:14px;
margin-bottom:10px;
}

.metric{
display:flex;
flex-direction:column;
}

.metric-label{
font-size:12px;
color:#6b7280;
}

.metric-value{
font-size:15px;
font-weight:600;
}

.loan-limit{
display:flex;
justify-content:space-between;
margin:14px 0;
}

.loan-value{
font-weight:600;
}

.bank-actions{
display:flex;
gap:10px;
}

.apply-btn{
background:#22c55e;
border:none;
padding:8px 16px;
border-radius:8px;
color:white;
cursor:pointer;
font-weight:500;
}

.apply-btn:hover{
background:#16a34a;
}

.visit-btn{
border:1px solid #d1d5db;
padding:8px 16px;
border-radius:8px;
background:white;
cursor:pointer;
}

.visit-btn:hover{
background:#f3f4f6;
}

.load-more-wrapper{
display:flex;
justify-content:center;
margin-top:40px;
}

.load-more-btn{
background:#2563eb;
color:white;
border:none;
padding:12px 26px;
border-radius:10px;
cursor:pointer;
}

.error{
text-align:center;
padding:40px;
color:#ef4444;
}

.empty{
text-align:center;
padding:40px;
color:#6b7280;
}

</style>