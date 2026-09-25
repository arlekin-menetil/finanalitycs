<script setup>

import { ref } from "vue"
import api from "@/api/axios"

const emit = defineEmits([
    "uploaded",
])

const props = defineProps({

    creditReport: {

        type: Object,

        default: null,

    },

    contracts: {

        type: Array,

        default: () => [],

    },

})

// ==========================================
// STATE
// ==========================================

const file = ref(null)

const uploading = ref(false)

const message = ref("")

const error = ref("")

// ==========================================
// FORMAT NUMBER
// ==========================================

function formatNumber(value){

    return Number(value || 0).toLocaleString(

        "ru-RU",

        {

            minimumFractionDigits: 2,

            maximumFractionDigits: 2,

        },

    )

}

// ==========================================
// FILE SELECT
// ==========================================

function selectFile(event){

    file.value = event.target.files[0] || null

    message.value = ""

    error.value = ""

}

// ==========================================
// UPLOAD REPORT
// ==========================================

async function upload(){

    if (!file.value){

        error.value = "Выберите HTML или PDF файл."

        return

    }

    uploading.value = true

    message.value = ""

    error.value = ""

    const formData = new FormData()

    formData.append(

        "file",

        file.value,

    )

    try{

        await api.post(

            "/credit-analysis/upload/",

            formData,

            {

                headers: {

                    "Content-Type": "multipart/form-data",

                },

            },

        )

        message.value =

            "Кредитный отчет успешно обработан."

        file.value = null

        emit("uploaded")

    }

    catch(e){

        console.error(e)

        error.value =

            e.response?.data?.detail ||

            e.response?.data?.error ||

            "Не удалось загрузить кредитный отчет."

    }

    finally{

        uploading.value = false

    }

}

</script>

<template>

<div class="card">

    <!-- ===================================== -->
    <!-- HEADER -->
    <!-- ===================================== -->

    <div class="header">

        <div>

            <h2>

                📄 Кредитная история

            </h2>

            <p>

                Загрузите отчет Infokredit для обновления кредитной истории.

            </p>

        </div>

    </div>

    <!-- ===================================== -->
    <!-- UPLOAD -->
    <!-- ===================================== -->

    <div class="upload-box">

        <input

            type="file"

            accept=".html,.htm,.pdf"

            @change="selectFile"

        >

        <div

            v-if="file"

            class="filename"

        >

            📄 {{ file.name }}

        </div>

        <button

            @click="upload"

            :disabled="uploading"

        >

            {{

                uploading

                    ? "Загрузка..."

                    : creditReport

                        ? "🔄 Обновить отчет"

                        : "📤 Загрузить отчет"

            }}

        </button>

    </div>

    <p

        v-if="message"

        class="success-text"

    >

        {{ message }}

    </p>

    <p

        v-if="error"

        class="error-text"

    >

        {{ error }}

    </p>

    <!-- ===================================== -->
    <!-- CONTRACTS -->
    <!-- ===================================== -->

    <div

        v-if="creditReport"

        class="report"

    >

        <div class="report-header">

            <h3>

                🏦 Активные кредитные договоры

            </h3>

            <span class="count">

                {{ contracts.length }}

            </span>

        </div>

        <table

            v-if="contracts.length"

            class="contracts"

        >

            <thead>

                <tr>

                    <th>Банк</th>

                    <th>Договор</th>

                    <th>Валюта</th>

                    <th>Общий долг</th>

                    <th>Просрочка</th>

                    <th>Ежемесячный платеж</th>

                </tr>

            </thead>

            <tbody>

                <tr

                    v-for="contract in contracts"

                    :key="contract.id"

                >

                    <td>

                        {{ contract.bank_name }}

                    </td>

                    <td>

                        {{ contract.contract_number }}

                    </td>

                    <td>

                        {{ contract.currency }}

                    </td>

                    <td class="amount">

                        {{ formatNumber(contract.current_debt) }}

                    </td>

                    <td class="amount overdue">

                        {{ formatNumber(contract.overdue_debt) }}

                    </td>

                    <td class="amount">

                        {{ formatNumber(contract.monthly_payment) }}

                    </td>

                </tr>

            </tbody>

        </table>

        <div

            v-else

            class="empty"

        >

            <div class="empty-icon">

                📄

            </div>

            <h4>

                Кредитные договоры отсутствуют

            </h4>

            <p>

                После загрузки отчета здесь появится список активных кредитных договоров.

            </p>

        </div>

    </div>

</div>

</template>

<style scoped>

.card{

background:#fff;

padding:30px;

border-radius:24px;

box-shadow:0 12px 32px rgba(15,23,42,.08);

margin-top:25px;

}

/* ==========================================
   HEADER
========================================== */

.header{

display:flex;

justify-content:space-between;

align-items:flex-start;

margin-bottom:28px;

gap:20px;

}

.header h2{

margin:0;

font-size:28px;

font-weight:700;

color:#0f172a;

}

.header p{

margin-top:8px;

font-size:15px;

color:#64748b;

line-height:1.5;

}

/* ==========================================
   UPLOAD
========================================== */

.upload-box{

display:flex;

flex-direction:column;

gap:16px;

margin-bottom:20px;

}

.upload-box input{

padding:14px;

border:1px solid #dbe2ea;

border-radius:12px;

background:#fff;

cursor:pointer;

transition:.2s;

}

.upload-box input:hover{

border-color:#93c5fd;

}

.filename{

padding:14px 18px;

background:#f8fafc;

border:1px solid #e2e8f0;

border-radius:12px;

font-size:14px;

color:#334155;

word-break:break-word;

}

button{

padding:14px 22px;

border:none;

border-radius:12px;

background:#2563eb;

color:#fff;

font-weight:600;

font-size:15px;

cursor:pointer;

transition:.25s;

}

button:hover:not(:disabled){

background:#1d4ed8;

transform:translateY(-2px);

box-shadow:0 10px 20px rgba(37,99,235,.25);

}

button:disabled{

opacity:.6;

cursor:not-allowed;

transform:none;

box-shadow:none;

}

/* ==========================================
   ALERTS
========================================== */

.success-text{

margin-top:18px;

font-weight:600;

color:#16a34a;

}

.error-text{

margin-top:18px;

font-weight:600;

color:#dc2626;

}

/* ==========================================
   REPORT
========================================== */

.report{

margin-top:35px;

}

.report-header{

display:flex;

justify-content:space-between;

align-items:center;

margin-bottom:20px;

gap:20px;

}

.report-header h3{

margin:0;

font-size:22px;

font-weight:700;

color:#0f172a;

}

.count{

display:flex;

align-items:center;

justify-content:center;

width:44px;

height:44px;

border-radius:999px;

background:#dbeafe;

color:#2563eb;

font-size:15px;

font-weight:700;

}

/* ==========================================
   TABLE
========================================== */

.contracts{

width:100%;

border-collapse:collapse;

overflow:hidden;

border-radius:16px;

border:1px solid #e2e8f0;

background:#fff;

}

.contracts thead{

background:#eff6ff;

}

.contracts th{

padding:18px;

text-align:left;

font-size:14px;

font-weight:700;

color:#1e3a8a;

white-space:nowrap;

}

.contracts td{

padding:18px;

font-size:14px;

color:#334155;

border-top:1px solid #e2e8f0;

vertical-align:middle;

}

.contracts tbody tr{

transition:.25s;

}

.contracts tbody tr:hover{

background:#f8fafc;

}

/* ==========================================
   MONEY
========================================== */

.amount{

text-align:right;

font-weight:700;

font-variant-numeric:tabular-nums;

white-space:nowrap;

letter-spacing:.3px;

}

.overdue{

color:#dc2626;

}

.currency{

text-align:center;

font-weight:600;

}

/* ==========================================
   EMPTY
========================================== */

.empty{

padding:60px 30px;

background:#f8fafc;

border:1px dashed #cbd5e1;

border-radius:18px;

text-align:center;

}

.empty-icon{

font-size:54px;

margin-bottom:16px;

}

.empty h4{

margin:0;

font-size:20px;

font-weight:700;

color:#0f172a;

}

.empty p{

margin-top:12px;

font-size:15px;

color:#64748b;

line-height:1.6;

}

/* ==========================================
   MOBILE
========================================== */

@media(max-width:900px){

.header{

flex-direction:column;

align-items:flex-start;

}

.report-header{

flex-direction:column;

align-items:flex-start;

}

.contracts{

display:block;

overflow-x:auto;

white-space:nowrap;

}

.contracts th,

.contracts td{

padding:16px;

}

}

</style>