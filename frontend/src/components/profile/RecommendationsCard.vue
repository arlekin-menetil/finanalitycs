<script setup>

import { computed } from "vue"

const props = defineProps({

    recommendations: {
        type: Array,
        default: () => [],
    },

    creditReport: {
        type: Object,
        default: () => null,
    },

})

const banks = computed(() => {

    const priority = {
        "Hamkorbank": 1,
        "Aloqabank": 2,
        "SQB": 3,
        "Ipak Yuli Bank": 4,
        "NBU": 5,
    }

    return [...props.recommendations].sort((a, b) => {

        const pa = priority[a.bank] ?? 999
        const pb = priority[b.bank] ?? 999

        if (pa !== pb) {
            return pa - pb
        }

        return Number(b.approval_probability) - Number(a.approval_probability)

    })

})

const medal = (index) => {

    if (index === 0) return "🥇"
    if (index === 1) return "🥈"
    if (index === 2) return "🥉"

    return "🏦"

}

const level = (p) => {

    p = Number(p)

    if (p >= 90) return "Очень высокий"

    if (p >= 80) return "Высокий"

    if (p >= 70) return "Хороший"

    if (p >= 60) return "Средний"

    return "Низкий"

}

const stars = (p) => {

    p = Number(p)

    if (p >= 90) return 5
    if (p >= 80) return 4
    if (p >= 70) return 3
    if (p >= 60) return 2

    return 1

}

</script>

<template>

<div class="card">

    <div class="header">

        <h2>
            🏦 Лучшие предложения
        </h2>

        <span class="badge">
            AI Selection
        </span>

    </div>

    <div
        v-for="(item,index) in banks"
        :key="item.id"
        class="bank"
    >

        <div class="left">

            <div class="top">

                <span class="medal">
                    {{ medal(index) }}
                </span>

                <div>

                    <div class="bank-name">

                        {{ item.bank }}

                    </div>

                    <div class="product">

                        {{ item.product }}

                    </div>

                </div>

            </div>

            <div class="stars">

                <span
                    v-for="n in 5"
                    :key="n"
                >

                    {{ n<=stars(item.approval_probability) ? "★":"☆" }}

                </span>

            </div>

            <div class="features">

                ✔ {{ level(item.approval_probability) }} шанс одобрения

                <br>

                ✔ Ставка {{ item.interest_rate }}%

            </div>

        </div>

        <div class="right">

            <div class="approval">

                {{ item.approval_probability }}%

            </div>

            <small>

                AI Match

            </small>

        </div>

    </div>

</div>

</template>

<style scoped>

.card{

background:#fff;

border-radius:24px;

padding:32px;

box-shadow:0 10px 30px rgba(15,23,42,.08);

margin-top:30px;

}

.header{

display:flex;

justify-content:space-between;

align-items:center;

margin-bottom:30px;

}

h2{

margin:0;

font-size:26px;

font-weight:700;

}

.badge{

background:#dbeafe;

color:#2563eb;

padding:8px 18px;

border-radius:999px;

font-size:13px;

font-weight:700;

}

.bank{

display:flex;

justify-content:space-between;

align-items:center;

padding:24px;

border:1px solid #e2e8f0;

border-radius:20px;

background:#f8fafc;

margin-bottom:18px;

transition:.25s;

}

.bank:hover{

transform:translateY(-4px);

box-shadow:0 15px 30px rgba(37,99,235,.12);

}

.bank:last-child{

margin-bottom:0;

}

.top{

display:flex;

align-items:center;

gap:18px;

}

.medal{

font-size:34px;

}

.bank-name{

font-size:22px;

font-weight:700;

color:#0f172a;

}

.product{

margin-top:6px;

color:#64748b;

}

.stars{

margin-top:14px;

color:#f59e0b;

font-size:18px;

letter-spacing:3px;

}

.features{

margin-top:14px;

font-size:14px;

color:#475569;

line-height:1.8;

}

.right{

text-align:right;

}

.approval{

font-size:38px;

font-weight:800;

color:#2563eb;

}

.right small{

display:block;

margin-top:8px;

color:#64748b;

font-size:14px;

}

@media(max-width:768px){

.bank{

flex-direction:column;

align-items:flex-start;

gap:20px;

}

.right{

text-align:left;

}

.header{

flex-direction:column;

align-items:flex-start;

gap:16px;

}

}

</style>