<template>

    <section class="dashboard-kpi">

        <div class="kpi-card">

            <div class="kpi-label">

                Ежемесячный доход

            </div>

            <div class="kpi-value">

                {{ formatMoney(income) }}

            </div>

        </div>

        <div class="kpi-card">

            <div class="kpi-label">

                Ежемесячные обязательства

            </div>

            <div class="kpi-value">

                {{ formatMoney(obligations) }}

            </div>

        </div>

        <div class="kpi-card">

            <div class="kpi-label">

                Свободный остаток

            </div>

            <div class="kpi-value">

                {{ formatMoney(balance) }}

            </div>

        </div>

        <div class="kpi-card">

            <div class="kpi-label">

                Debt To Income

            </div>

            <div class="kpi-value">

                {{ Number(dti).toFixed(2) }}%

            </div>

        </div>

    </section>

</template>

<script setup>

const props = defineProps({

    income: {

        type: Number,

        default: 0,

    },

    obligations: {

        type: Number,

        default: 0,

    },

    balance: {

        type: Number,

        default: 0,

    },

    dti: {

        type: Number,

        default: 0,

    },

})

function formatMoney(value) {

    return new Intl.NumberFormat(

        "ru-RU",

        {

            maximumFractionDigits: 0,

        }

    ).format(

        Number(value || 0)

    ) + " сум"

}

</script>

<style scoped>

/* ==========================================================
   GRID
========================================================== */

.dashboard-kpi{

    display:grid;

    grid-template-columns:repeat(4,1fr);

    gap:24px;

}

/* ==========================================================
   CARD
========================================================== */

.kpi-card{

    position:relative;

    overflow:hidden;

    padding:28px;

    border-radius:24px;

    background:#ffffff;

    border:1px solid #e2e8f0;

    transition:.3s;

    box-shadow:0 12px 30px rgba(15,23,42,.05);

}

.kpi-card:hover{

    transform:translateY(-6px);

    box-shadow:0 20px 45px rgba(37,99,235,.12);

    border-color:#3b82f6;

}

.kpi-card::before{

    content:"";

    position:absolute;

    top:0;

    left:0;

    width:100%;

    height:5px;

    background:linear-gradient(
        90deg,
        #2563eb,
        #3b82f6
    );

}

/* ==========================================================
   TEXT
========================================================== */

.kpi-label{

    font-size:14px;

    color:#64748b;

    margin-bottom:18px;

}

.kpi-value{

    font-size:34px;

    font-weight:700;

    color:#0f172a;

    line-height:1.2;

}

/* ==========================================================
   DARK
========================================================== */

.dark .kpi-card{

    background:#0f172a;

    border-color:#1e293b;

    box-shadow:none;

}

.dark .kpi-value{

    color:white;

}

.dark .kpi-label{

    color:#94a3b8;

}

/* ==========================================================
   RESPONSIVE
========================================================== */

@media (max-width:1200px){

    .dashboard-kpi{

        grid-template-columns:repeat(2,1fr);

    }

}

@media (max-width:700px){

    .dashboard-kpi{

        grid-template-columns:1fr;

    }

    .kpi-card{

        padding:22px;

    }

    .kpi-value{

        font-size:28px;

    }

}

</style>