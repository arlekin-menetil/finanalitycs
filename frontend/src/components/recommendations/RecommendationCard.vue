<script setup>

import { computed } from "vue"
import { useRouter } from "vue-router"

const props = defineProps({

    item: {
        type: Object,
        required: true,
    },

})

const router = useRouter()

// ==========================================
// LOGO
// ==========================================

const logo = computed(() => {

    if (props.item.bank_logo) {

        return props.item.bank_logo

    }

    const bank = String(

        props.item.bank_name || ""

    )

        .toLowerCase()

        .replace(/\s+/g, "")

        .replace(/-/g, "")

    return `/banks/${bank}.png`

})

// ==========================================
// LINKS
// ==========================================

const bankUrl = computed(() =>

    props.item.bank_url ||

    props.item.website ||

    null

)

const sourceUrl = computed(() =>

    props.item.source_url ||

    null

)

// ==========================================
// RATE
// ==========================================

const rate = computed(() => {

    const value = props.item.interest_rate

    if (
        value === null ||
        value === undefined
    ) {
        return "—"
    }

    return `${value}%`

})

// ==========================================
// LIMIT
// ==========================================

const limit = computed(() => {

    const value =

        props.item.loan_limit_hint ||

        props.item.max_amount

    if (!value) {

        return "Не указано"

    }

    return new Intl.NumberFormat(

        "ru-RU"

    ).format(value)

})

// ==========================================
// APPROVAL
// ==========================================

const approval = computed(() =>

    props.item.approval_probability || 0

)

// ==========================================
// DETAIL
// ==========================================

function openDetail() {

    if (!props.item?.id) {

        console.error("INVALID PRODUCT ID")

        return

    }

    router.push(

        `/app/loan/${props.item.id}`

    )

}

// ==========================================
// OPEN BANK
// ==========================================

function openBank() {

    if (!bankUrl.value) {

        return

    }

    window.open(

        bankUrl.value,

        "_blank"

    )

}

// ==========================================
// OPEN SOURCE
// ==========================================

function openSource() {

    if (!sourceUrl.value) {

        return

    }

    window.open(

        sourceUrl.value,

        "_blank"

    )

}

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
      alt="bank"
    />

    <div class="bank-info">

      <h3>
        {{ item.bank_name }}
      </h3>

      <p>
        {{ item.product_name }}
      </p>

    </div>

  </div>


  <!-- ===================================== -->
  <!-- 💣 TAGS -->
  <!-- ===================================== -->
  <div class="tags">

    <span
      v-if="item.is_online"
      class="tag online"
    >
      Онлайн
    </span>

    <span class="tag">

      {{ item.product_type }}

    </span>

  </div>


  <!-- ===================================== -->
  <!-- 💣 STATS -->
  <!-- ===================================== -->
  <div class="stats">

    <div class="stat">

      <span>
        Ставка
      </span>

      <strong>
        {{ rate }}
      </strong>

    </div>

    <div class="stat">

      <span>
        Сумма
      </span>

      <strong>
        {{ limit }}
      </strong>

    </div>

    <div class="stat">

      <span>
        Одобрение
      </span>

      <strong>
        {{ approval }}%
      </strong>

    </div>

  </div>


  <!-- ===================================== -->
  <!-- 💣 EXPLANATIONS -->
  <!-- ===================================== -->
  <div
    v-if="item.explanations?.length"
    class="explanations"
  >

    <div
      v-for="(
        explanation,
        index
      ) in item.explanations"

      :key="index"

      class="explanation"
    >

      {{ explanation }}

    </div>

  </div>


  <!-- ===================================== -->
  <!-- 💣 ACTIONS -->
  <!-- ===================================== -->
  <div class="actions">

    <button
      class="details-btn"
      @click="openDetail"
    >
      Подробнее
    </button>

  </div>

</div>

</template>

<style scoped>

.card{
background:white;
border-radius:24px;
padding:24px;
box-shadow:0 4px 20px rgba(0,0,0,.05);
display:flex;
flex-direction:column;
gap:20px;
transition:.25s;
border:1px solid #e2e8f0;
}

.card:hover{
transform:translateY(-4px);
box-shadow:0 10px 30px rgba(0,0,0,.08);
}

.header{
display:flex;
gap:16px;
align-items:center;
}

.logo{
width:56px;
height:56px;
border-radius:14px;
object-fit:contain;
background:#f8fafc;
padding:6px;
}

.bank-info h3{
margin:0;
font-size:18px;
font-weight:800;
}

.bank-info p{
margin:4px 0 0;
color:#64748b;
font-size:14px;
}

.tags{
display:flex;
gap:8px;
flex-wrap:wrap;
}

.tag{
padding:6px 10px;
border-radius:999px;
background:#eff6ff;
font-size:12px;
font-weight:700;
color:#1d4ed8;
}

.tag.online{
background:#dcfce7;
color:#166534;
}

.stats{
display:grid;
grid-template-columns:repeat(3,1fr);
gap:14px;
}

.stat{
background:#f8fafc;
padding:14px;
border-radius:16px;
}

.stat span{
display:block;
font-size:12px;
color:#64748b;
margin-bottom:6px;
}

.stat strong{
font-size:16px;
font-weight:800;
}

.explanations{
display:flex;
flex-wrap:wrap;
gap:8px;
}

.explanation{
padding:8px 12px;
border-radius:12px;
background:#f1f5f9;
font-size:13px;
font-weight:600;
}

.actions{
display:flex;
justify-content:flex-end;
}

.details-btn{
border:none;
background:#2563eb;
color:white;
padding:12px 18px;
border-radius:14px;
font-weight:700;
cursor:pointer;
transition:.2s;
}

.details-btn:hover{
background:#1d4ed8;
}

@media(max-width:768px){

.stats{
grid-template-columns:1fr;
}

}

</style>