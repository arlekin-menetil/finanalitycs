<template>

    <article class="recommendation-card">

        <!-- ===================================== -->
        <!-- HEADER -->
        <!-- ===================================== -->

        <div class="card-header">

            <div class="bank-info">

                <div class="bank-logo">

                    <img

                        :src="bankLogo"

                        :alt="bankName"

                        @error="logoError"

                    />

                </div>

                <div>

                    <h3 class="bank-name">

                        {{ bankName }}

                    </h3>

                    <p class="product-name">

                        {{ productName }}

                    </p>

                </div>

            </div>

            <div
                class="match-score"
                :class="matchClass"
            >

                <span>

                    AI Match

                </span>

                <strong>

                    {{ rankingScore }}

                </strong>

            </div>

        </div>

        <!-- ===================================== -->
        <!-- BADGES -->
        <!-- ===================================== -->

        <div class="badges">

            <div

                v-if="featured"

                class="badge featured"

            >

                ⭐ Лучший выбор

            </div>

            <div

                v-if="isOnline"

                class="badge online"

            >

                Онлайн оформление

            </div>

            <div

                v-if="approvalProbability >= 80"

                class="badge success"

            >

                Высокий шанс одобрения

            </div>

        </div>

        <!-- ===================================== -->
        <!-- REASONS -->
        <!-- ===================================== -->

        <div

            v-if="reasons.length"

            class="reasons"

        >

            <h4>

                Почему рекомендуем

            </h4>

            <ul>

                <li

                    v-for="reason in reasons"

                    :key="reason.title"

                >

                    ✔ {{ reason.title }}

                </li>

            </ul>

        </div>

        <!-- ===================================== -->
        <!-- INFORMATION -->
        <!-- ===================================== -->

        <div class="info-grid">

            <div class="info-item">

                <span>

                    Процентная ставка

                </span>

                <strong>

                    {{ interestRate }} %

                </strong>

            </div>

            <div class="info-item">

                <span>

                    Максимальный лимит

                </span>

                <strong>

                    {{ formatMoney(recommendedLimit) }}

                </strong>

            </div>

            <div class="info-item">

                <span>

                    Вероятность одобрения

                </span>

                <strong>

                    {{ approvalProbability }} %

                </strong>

            </div>

            <div class="info-item">

                <span>

                    Способ оформления

                </span>

                <strong>

                    {{ isOnline ? "Онлайн" : "В отделении" }}

                </strong>

            </div>

        </div>

        <!-- ===================================== -->
        <!-- CAMPAIGNS -->
        <!-- ===================================== -->

        <div

            v-if="campaigns.length"

            class="campaigns"

        >

            <div

                v-for="campaign in campaigns"

                :key="campaign.title"

                class="campaign"

            >

                {{ campaign.badge }}

                {{ campaign.title }}

            </div>

        </div>

        <!-- ===================================== -->
        <!-- FOOTER -->
        <!-- ===================================== -->

        <div class="card-footer">

            <button

                class="btn secondary"

                @click="openProduct"

            >

                Подробнее

            </button>

            <button

                class="btn primary"

                @click="openBank"

            >

                Подать заявку

            </button>

        </div>

    </article>

</template>

<script setup>

import { computed } from "vue"

// ==========================================
// PROPS
// ==========================================

const props = defineProps({

    recommendation: {

        type: Object,

        required: true,

    },

})

// ==========================================
// COMPUTED
// ==========================================

const bankName = computed(() =>

    props.recommendation?.bank?.name || props.recommendation?.bank?.short_name || "-"

)

const productName = computed(() =>

    props.recommendation?.product?.name || "-"

)

const interestRate = computed(() =>

    Number(
        props.recommendation?.product?.interest_rate ?? 0
    )

)

const recommendedLimit = computed(() =>

    Number(
        props.recommendation?.recommended_limit ?? 0
    )

)

const approvalProbability = computed(() =>

    Number(
        props.recommendation?.approval_probability ?? 0
    )

)

const rankingScore = computed(() =>

    Number(
        props.recommendation?.ranking_score ?? 0
    )

)

const isOnline = computed(() =>

    props.recommendation?.product?.is_online === true

)

const featured = computed(() =>

    props.recommendation?.featured === true

)

const campaigns = computed(() =>

    props.recommendation?.campaigns || []

)

const reasons = computed(() =>

    props.recommendation?.reasons || []

)

// ==========================================
// BANK LOGO
// ==========================================

const bankLogo = computed(() => {

    const bank = String(bankName.value)
        .toLowerCase()
        .replace(/'/g, "")
        .replace(/"/g, "")
        .replace(/\s+/g, "")
        .replace(/-/g, "")

    const aliases = {

        asiaalliancebank: "asiaalliancebank",

        asiaalliance: "asiaalliance",

        ipakyoli: "ipakyuli",

        ipakyulibank: "ipakyulibank",

        ipakyuli: "ipakyuli",

        orientfinans: "orientfinans",

        xalqbank: "xalqbank",

        xalqbanki: "xalqbanki",

        trustbank: "trustbank",

        trastbank: "trastbank",

        kdbuzbekiston: "kdbuzbekiston",

        kdbbank: "kdbbank",

    }

    const file = aliases[bank] || bank

    return `/banks/${file}.png`

})

function logoError(event) {

    event.target.src = "/banks/default.png"

}

// ==========================================
// LINKS
// ==========================================

function openProduct() {

    const url = props.recommendation?.product?.source_url

        || props.recommendation?.source_url

    if (url) {

        window.open(
            url,
            "_blank"
        )

    }

}

function openBank() {

    const url = props.recommendation?.product?.bank_url

        || props.recommendation?.bank_url

    if (url) {

        window.open(
            url,
            "_blank"
        )

    }

}

// ==========================================
// MATCH COLOR
// ==========================================

const matchClass = computed(() => {

    if (rankingScore.value >= 90)

        return "excellent"

    if (rankingScore.value >= 75)

        return "good"

    if (rankingScore.value >= 60)

        return "medium"

    return "low"

})

// ==========================================
// HELPERS
// ==========================================

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
   CARD
========================================================== */

.recommendation-card{

    position:relative;

    overflow:hidden;

    display:flex;

    flex-direction:column;

    gap:28px;

    padding:30px;

    border-radius:28px;

    background:#ffffff;

    border:1px solid #e2e8f0;

    box-shadow:0 16px 40px rgba(15,23,42,.06);

    transition:
        transform .30s,
        box-shadow .30s,
        border-color .30s;

}

.recommendation-card::before{

    content:"";

    position:absolute;

    left:0;

    top:0;

    width:100%;

    height:5px;

    background:linear-gradient(
        90deg,
        #2563eb,
        #3b82f6,
        #60a5fa
    );

}

.recommendation-card:hover{

    transform:translateY(-8px);

    border-color:#3b82f6;

    box-shadow:0 26px 60px rgba(37,99,235,.18);

}

/* ==========================================================
   HEADER
========================================================== */

.card-header{

    display:flex;

    justify-content:space-between;

    align-items:flex-start;

    gap:22px;

}

.bank-info{

    display:flex;

    align-items:center;

    gap:18px;

}

/* ==========================================================
   LOGO
========================================================== */

.bank-logo{

    width:72px;

    height:72px;

    border-radius:18px;

    overflow:hidden;

    background:#ffffff;

    border:1px solid #e2e8f0;

    display:flex;

    align-items:center;

    justify-content:center;

    flex-shrink:0;

    box-shadow:0 8px 20px rgba(0,0,0,.05);

}

.bank-logo img{

    width:88%;

    height:88%;

    object-fit:contain;

    transition:.25s;

}

.recommendation-card:hover .bank-logo img{

    transform:scale(1.05);

}

/* ==========================================================
   TITLES
========================================================== */

.bank-name{

    margin:0;

    font-size:24px;

    font-weight:700;

    color:#0f172a;

}

.product-name{

    margin-top:6px;

    font-size:15px;

    color:#64748b;

    line-height:1.5;

}

/* ==========================================================
   MATCH
========================================================== */

.match-score{

    min-width:95px;

    display:flex;

    flex-direction:column;

    align-items:center;

    justify-content:center;

    padding:14px;

    border-radius:20px;

    background:#eff6ff;

    border:1px solid #bfdbfe;

}

.match-score span{

    font-size:11px;

    letter-spacing:1px;

    text-transform:uppercase;

    color:#64748b;

}

.match-score strong{

    margin-top:8px;

    font-size:30px;

    font-weight:700;

}

/* ==========================================================
   MATCH COLORS
========================================================== */

.match-score.excellent{

    background:#dcfce7;

    border-color:#86efac;

}

.match-score.excellent strong{

    color:#15803d;

}

.match-score.good{

    background:#dbeafe;

    border-color:#93c5fd;

}

.match-score.good strong{

    color:#2563eb;

}

.match-score.medium{

    background:#fef3c7;

    border-color:#fde68a;

}

.match-score.medium strong{

    color:#d97706;

}

.match-score.low{

    background:#fee2e2;

    border-color:#fecaca;

}

.match-score.low strong{

    color:#dc2626;

}

/* ==========================================================
   BADGES
========================================================== */

.badges{

    display:flex;

    flex-wrap:wrap;

    gap:12px;

}

.badge{

    padding:8px 15px;

    border-radius:999px;

    font-size:12px;

    font-weight:600;

    display:flex;

    align-items:center;

    gap:6px;

}

.featured{

    background:#fef3c7;

    color:#92400e;

}

.online{

    background:#dbeafe;

    color:#1d4ed8;

}

.success{

    background:#dcfce7;

    color:#15803d;

}

/* ==========================================================
   REASONS
========================================================== */

.reasons{

    padding:22px;

    border-radius:22px;

    background:#f8fafc;

    border:1px solid #e2e8f0;

}

.reasons h4{

    margin:0 0 16px;

    font-size:17px;

    font-weight:700;

    color:#0f172a;

}

.reasons ul{

    margin:0;

    padding:0;

    list-style:none;

    display:flex;

    flex-direction:column;

    gap:12px;

}

.reasons li{

    display:flex;

    align-items:flex-start;

    gap:10px;

    color:#475569;

    line-height:1.6;

}

/* ==========================================================
   INFORMATION GRID
========================================================== */

.info-grid{

    display:grid;

    grid-template-columns:repeat(2,1fr);

    gap:18px;

}

.info-item{

    padding:18px;

    border-radius:18px;

    background:#f8fafc;

    border:1px solid #e2e8f0;

    transition:.25s;

}

.info-item:hover{

    background:#eff6ff;

    border-color:#bfdbfe;

}

.info-item span{

    display:block;

    font-size:13px;

    color:#64748b;

}

.info-item strong{

    display:block;

    margin-top:10px;

    font-size:18px;

    font-weight:700;

    color:#0f172a;

}

/* ==========================================================
   CAMPAIGNS
========================================================== */

.campaigns{

    display:flex;

    flex-wrap:wrap;

    gap:10px;

}

.campaign{

    padding:8px 15px;

    border-radius:999px;

    background:#fee2e2;

    color:#b91c1c;

    font-size:13px;

    font-weight:600;

}

/* ==========================================================
   FOOTER
========================================================== */

.card-footer{

    display:flex;

    justify-content:flex-end;

    gap:16px;

    margin-top:auto;

}

.btn{

    min-width:170px;

    padding:13px 22px;

    border:none;

    border-radius:14px;

    cursor:pointer;

    font-size:14px;

    font-weight:600;

    transition:.25s;

}

.btn.primary{

    color:white;

    background:linear-gradient(

        135deg,

        #2563eb,

        #3b82f6

    );

}

.btn.primary:hover{

    transform:translateY(-2px);

    box-shadow:0 12px 24px rgba(37,99,235,.25);

}

.btn.secondary{

    background:#f1f5f9;

    color:#0f172a;

}

.btn.secondary:hover{

    background:#e2e8f0;

}

/* ==========================================================
   DARK MODE
========================================================== */

.dark .recommendation-card{

    background:#0f172a;

    border-color:#1e293b;

}

.dark .bank-logo{

    background:#1e293b;

    border-color:#334155;

}

.dark .bank-name{

    color:#ffffff;

}

.dark .product-name{

    color:#94a3b8;

}

.dark .reasons{

    background:#1e293b;

    border-color:#334155;

}

.dark .reasons h4{

    color:#ffffff;

}

.dark .reasons li{

    color:#cbd5e1;

}

.dark .info-item{

    background:#1e293b;

    border-color:#334155;

}

.dark .info-item:hover{

    background:#263548;

}

.dark .info-item strong{

    color:#ffffff;

}

.dark .btn.secondary{

    background:#1e293b;

    color:white;

}

.dark .btn.secondary:hover{

    background:#334155;

}

/* ==========================================================
   RESPONSIVE
========================================================== */

@media (max-width:900px){

    .card-header{

        flex-direction:column;

        align-items:flex-start;

    }

    .match-score{

        width:100%;

    }

    .info-grid{

        grid-template-columns:1fr;

    }

    .card-footer{

        flex-direction:column;

    }

    .btn{

        width:100%;

    }

}

@media (max-width:600px){

    .recommendation-card{

        padding:22px;

    }

    .bank-logo{

        width:60px;

        height:60px;

    }

    .bank-name{

        font-size:20px;

    }

    .match-score strong{

        font-size:24px;

    }

}
</style>