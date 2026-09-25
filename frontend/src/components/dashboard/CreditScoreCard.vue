<template>
    <section class="credit-card">

        <!-- =====================================================
             HEADER
        ====================================================== -->

        <div class="card-header">
            <div>
                <div class="card-title">
                    {{ t("dashboard.creditAnalysis") }}
                </div>

                <h2 class="card-subtitle">
                    {{ t("dashboard.financialScoring") }}
                </h2>

                <p class="card-description">
                    {{ t("dashboard.description") }}
                </p>
            </div>

            <div
                class="risk-badge"
                :class="riskClass"
            >
                <span class="risk-dot"></span>
                {{ riskLabel }}
            </div>
        </div>


        <!-- =====================================================
             SCORE CARDS
        ====================================================== -->

        <div class="scores-grid">

            <!-- Official Score -->

            <div class="score-box official">
                <div class="score-top">
                    <div class="score-icon">
                        ✓
                    </div>

                    <div class="score-label">
                        {{ t("dashboard.officialCreditScore") }}
                    </div>
                </div>

                <div class="score-value">
                    {{ officialScore.credit_score }}
                </div>

                <div class="score-description">
                    {{ t("dashboard.creditBureau") }}
                </div>
            </div>


            <!-- AI Score -->

            <div class="score-box ai">
                <div class="score-top">
                    <div class="score-icon">
                        ✦
                    </div>

                    <div class="score-label">
                        {{ t("dashboard.aiCreditScore") }}
                    </div>
                </div>

                <div class="score-value">
                    {{ safeScore.score }}
                </div>

                <div class="score-description">
                    BankAnalytics AI
                </div>
            </div>

        </div>


        <!-- =====================================================
             AI SCORE SCALE
        ====================================================== -->

        <div class="panel score-scale-panel">

            <div class="panel-heading">
                <div>
                    <div class="panel-kicker">
                        {{ t("dashboard.aiScore") }}
                    </div>

                    <h3>
                        {{ t("dashboard.creditworthiness") }}
                    </h3>
                </div>

                <div class="scale-score">
                    {{ safeScore.score }}
                    <span>/ 900</span>
                </div>
            </div>


            <div class="score-scale">

                <div class="scale-track">

                    <div
                        class="scale-progress"
                        :style="{
                            width: scoreScalePercent + '%'
                        }"
                    ></div>

                    <div
                        class="scale-marker"
                        :style="{
                            left: scoreScalePercent + '%'
                        }"
                    >
                        <span>
                            {{ safeScore.score }}
                        </span>
                    </div>

                </div>


                <div class="scale-labels">
                    <span>300</span>
                    <span>450</span>
                    <span>600</span>
                    <span>750</span>
                    <span>900</span>
                </div>

            </div>


            <div class="scale-footer">

                <span>
                    {{ t("dashboard.scoreCalculated") }}
                </span>

                <strong>
                    {{ riskDescription }}
                </strong>

            </div>

        </div>


        <!-- =====================================================
             APPROVAL
        ====================================================== -->

        <div class="panel approval-panel">

            <div class="panel-heading">

                <div>
                    <div class="panel-kicker">
                        {{ t("dashboard.approvalSection") }}
                    </div>

                    <h3>
                        {{ t("dashboard.approvalProbability") }}
                    </h3>
                </div>

                <div class="approval-value">
                    {{ approvalPercent }}%
                </div>

            </div>


            <div class="approval-progress">

                <div
                    class="approval-progress-value"
                    :style="{
                        width: approvalPercent + '%'
                    }"
                ></div>

            </div>


            <div class="approval-footer">

                <span>
                    {{ t("dashboard.estimatedProbability") }}
                </span>

                <span>
                    {{ approvalLabel }}
                </span>

            </div>

        </div>


        <!-- =====================================================
             RECOMMENDED LIMIT
        ====================================================== -->

        <div class="limit-card">

            <div class="limit-content">

                <div class="limit-icon">
                    {{ t("currency.uzs") }}
                </div>

                <div>

                    <div class="limit-title">
                        {{ t("dashboard.recommendedLimit") }}
                    </div>

                    <div class="limit-value">
                        {{ formatMoney(safeScore.recommended_limit) }}
                    </div>

                    <div class="limit-description">
                        {{ t("dashboard.limitDescription") }}
                    </div>

                </div>

            </div>

        </div>


        <!-- =====================================================
             FINANCIAL SNAPSHOT
        ====================================================== -->

        <div class="panel snapshot-panel">

            <div class="panel-heading">

                <div>
                    <div class="panel-kicker">
                        {{ t("dashboard.financialSnapshot") }}
                    </div>

                    <h3>
                        {{ t("dashboard.financialInformation") }}
                    </h3>
                </div>

            </div>


            <div class="snapshot-grid">

                <!-- Income -->

                <div class="snapshot-item">

                    <div class="snapshot-icon income">
                        ↗
                    </div>

                    <div class="snapshot-info">

                        <span>
                            {{ t("dashboard.metrics.income") }}
                        </span>

                        <strong>
                            {{ formatMoney(financialProfile.monthly_income_total) }}
                        </strong>

                    </div>

                </div>


                <!-- Obligations -->

                <div class="snapshot-item">

                    <div class="snapshot-icon obligations">
                        ↓
                    </div>

                    <div class="snapshot-info">

                        <span>
                            {{ t("dashboard.obligations") }}
                        </span>

                        <strong>
                            {{ formatMoney(financialProfile.monthly_obligations_total) }}
                        </strong>

                    </div>

                </div>


                <!-- Debt -->

                <div class="snapshot-item">

                    <div class="snapshot-icon debt">
                        {{ t("currency.uzs") }}
                    </div>

                    <div class="snapshot-info">

                        <span>
                            {{ t("dashboard.totalDebt") }}
                        </span>

                        <strong>
                            {{ formatMoney(officialScore.total_debt) }}
                        </strong>

                    </div>

                </div>


                <!-- Contracts -->

                <div class="snapshot-item">

                    <div class="snapshot-icon contracts">
                        #
                    </div>

                    <div class="snapshot-info">

                        <span>
                            {{ t("dashboard.contracts") }}
                        </span>

                        <strong>
                            {{ officialScore.contracts_total }}
                        </strong>

                    </div>

                </div>


                <!-- Balance -->

                <div class="snapshot-item">

                    <div class="snapshot-icon balance">
                        =
                    </div>

                    <div class="snapshot-info">

                        <span>
                            {{ t("dashboard.netBalance") }}
                        </span>

                        <strong>
                            {{ formatMoney(financialProfile.net_balance) }}
                        </strong>

                    </div>

                </div>


                <!-- DTI -->

                <div class="snapshot-item">

                    <div class="snapshot-icon dti">
                        %
                    </div>

                    <div class="snapshot-info">

                        <span>
                            DTI
                        </span>

                        <strong>
                            {{ formatPercent(financialProfile.dti_ratio) }}
                        </strong>

                    </div>

                </div>

            </div>

        </div>


        <!-- =====================================================
             AI ANALYSIS
        ====================================================== -->

        <div class="panel ai-analysis-panel">

            <div class="panel-heading">

                <div>
                    <div class="panel-kicker">
                        {{ t("dashboard.aiAnalysis") }}
                    </div>

                    <h3>
                        {{ t("dashboard.aiMetrics") }}
                    </h3>
                </div>

                <div class="ai-badge">
                    ✦ BankAnalytics AI
                </div>

            </div>


            <div class="metrics">

                <Metric
                    :title="t('dashboard.metrics.income')"
                    :value="safeScore.income_score"
                />

                <Metric
                    :title="t('dashboard.metrics.dti')"
                    :value="safeScore.dti_score"
                />

                <Metric
                    :title="t('dashboard.metrics.employment')"
                    :value="safeScore.employment_score"
                />

                <Metric
                    :title="t('dashboard.metrics.history')"
                    :value="safeScore.history_score"
                />

                <Metric
                    :title="t('dashboard.metrics.profile')"
                    :value="safeScore.profile_score"
                />

                <Metric
                    :title="t('dashboard.metrics.netBalance')"
                    :value="formatMoney(financialProfile.net_balance)"
                />

            </div>

        </div>

    </section>
</template>


<script setup>
import { computed } from "vue"
import { useI18n } from "vue-i18n"

import Metric from "./ScoreMetric.vue"


// ==========================================================
// I18N
// ==========================================================

const { t } = useI18n()


// ==========================================================
// PROPS
// ==========================================================

const props = defineProps({
    score: {
        type: Object,
        default: () => ({}),
    },

    creditReport: {
        type: Object,
        default: () => ({}),
    },

    profile: {
        type: Object,
        default: () => ({}),
    },
})


// ==========================================================
// AI SCORE
// ==========================================================

const safeScore = computed(() => ({
    score: Number(
        props.score?.score ?? 0
    ),

    risk_category:
        props.score?.risk_category ?? "UNKNOWN",

    approval_probability: Number(
        props.score?.approval_probability ?? 0
    ),

    recommended_limit: Number(
        props.score?.recommended_limit ?? 0
    ),

    income_score: Number(
        props.score?.income_score ?? 0
    ),

    dti_score: Number(
        props.score?.dti_score ?? 0
    ),

    employment_score: Number(
        props.score?.employment_score ?? 0
    ),

    history_score: Number(
        props.score?.history_score ?? 0
    ),

    profile_score: Number(
        props.score?.profile_score ?? 0
    ),
}))


// ==========================================================
// OFFICIAL CREDIT REPORT
// ==========================================================

const officialScore = computed(() => ({
    credit_score: Number(
        props.creditReport?.credit_score ?? 0
    ),

    risk_class:
        props.creditReport?.risk_class ?? "-",

    contracts_total: Number(
        props.creditReport?.contracts_total ?? 0
    ),

    total_debt: Number(
        props.creditReport?.total_debt ?? 0
    ),

    overdue_debt: Number(
        props.creditReport?.overdue_debt ?? 0
    ),
}))


// ==========================================================
// FINANCIAL PROFILE
// ==========================================================

const financialProfile = computed(() => ({
    monthly_income_total: Number(
        props.profile?.monthly_income_total ?? 0
    ),

    monthly_obligations_total: Number(
        props.profile?.monthly_obligations_total ?? 0
    ),

    net_balance: Number(
        props.profile?.net_balance ?? 0
    ),

    dti_ratio: Number(
        props.profile?.dti_ratio ?? 0
    ),
}))


// ==========================================================
// RISK CLASS
// ==========================================================

const riskClass = computed(() => {

    switch (safeScore.value.risk_category) {

        case "LOW":
            return "risk-low"

        case "MEDIUM":
            return "risk-medium"

        case "HIGH":
            return "risk-high"

        case "REJECT":
            return "risk-high"

        default:
            return "risk-default"
    }

})


// ==========================================================
// RISK LABEL
// ==========================================================

const riskLabel = computed(() => {

    switch (safeScore.value.risk_category) {

        case "LOW":
            return t("dashboard.riskLevels.low")

        case "MEDIUM":
            return t("dashboard.riskLevels.medium")

        case "HIGH":
            return t("dashboard.riskLevels.high")

        case "REJECT":
            return t("dashboard.riskLevels.reject")

        default:
            return t("dashboard.riskLevels.unknown")
    }

})


// ==========================================================
// RISK DESCRIPTION
// ==========================================================

const riskDescription = computed(() => {

    switch (safeScore.value.risk_category) {

        case "LOW":
            return t("dashboard.riskLevels.low")

        case "MEDIUM":
            return t("dashboard.riskLevels.medium")

        case "HIGH":
            return t("dashboard.riskLevels.high")

        case "REJECT":
            return t("dashboard.riskLevels.reject")

        default:
            return t("dashboard.riskLevels.unknown")
    }

})


// ==========================================================
// APPROVAL
// ==========================================================

const approvalPercent = computed(() => {

    const value = Number(
        safeScore.value.approval_probability || 0
    )

    /*
     * Backend may return:
     *
     * 0.32  -> 32%
     * 32    -> 32%
     */

    if (value <= 1) {
        return Math.round(
            Math.min(
                Math.max(value * 100, 0),
                100
            )
        )
    }

    return Math.round(
        Math.min(
            Math.max(value, 0),
            100
        )
    )
})


// ==========================================================
// APPROVAL LABEL
// ==========================================================

const approvalLabel = computed(() => {

    const value = approvalPercent.value

    if (value >= 70) {
        return t("dashboard.highProbability")
    }

    if (value >= 40) {
        return t("dashboard.mediumProbability")
    }

    return t("dashboard.lowProbability")
})


// ==========================================================
// AI SCORE SCALE
// ==========================================================

const scoreScalePercent = computed(() => {

    const min = 300
    const max = 900

    const score = Math.min(
        Math.max(
            Number(safeScore.value.score || min),
            min
        ),
        max
    )

    return ((score - min) / (max - min)) * 100
})


// ==========================================================
// MONEY
// ==========================================================

function formatMoney(value) {

    const number = Number(value || 0)

    return new Intl.NumberFormat(
        "ru-RU",
        {
            maximumFractionDigits: 0,
        }
    ).format(number) + " " + t("currency.uzs")
}


// ==========================================================
// PERCENT
// ==========================================================

function formatPercent(value) {

    const number = Number(value || 0)

    return `${number.toFixed(2)}%`
}
</script>


<style scoped>

/* ==========================================================
   MAIN CARD
========================================================== */

.credit-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 28px;
    padding: 30px;

    box-shadow:
        0 18px 45px rgba(15, 23, 42, 0.06);

    display: flex;
    flex-direction: column;
    gap: 22px;

    transition:
        box-shadow .25s ease,
        transform .25s ease;
}

.credit-card:hover {
    box-shadow:
        0 24px 60px rgba(15, 23, 42, 0.09);
}


/* ==========================================================
   HEADER
========================================================== */

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 24px;
    padding-bottom: 8px;
}

.card-title {
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #64748b;
    margin-bottom: 8px;
}

.card-subtitle {
    margin: 0;
    font-size: 28px;
    line-height: 1.2;
    font-weight: 750;
    color: #0f172a;
}

.card-description {
    margin: 10px 0 0;
    max-width: 650px;
    font-size: 14px;
    line-height: 1.6;
    color: #64748b;
}


/* ==========================================================
   RISK
========================================================== */

.risk-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 16px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 750;
    white-space: nowrap;
}

.risk-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
}

.risk-low {
    background: #dcfce7;
    color: #166534;
}

.risk-low .risk-dot {
    background: #22c55e;
}

.risk-medium {
    background: #fef3c7;
    color: #92400e;
}

.risk-medium .risk-dot {
    background: #f59e0b;
}

.risk-high {
    background: #fee2e2;
    color: #991b1b;
}

.risk-high .risk-dot {
    background: #ef4444;
}

.risk-default {
    background: #f1f5f9;
    color: #334155;
}

.risk-default .risk-dot {
    background: #64748b;
}


/* ==========================================================
   SCORE CARDS
========================================================== */

.scores-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 18px;
}

.score-box {
    position: relative;
    overflow: hidden;

    min-height: 190px;
    padding: 26px;

    border-radius: 22px;
    color: #ffffff;

    box-shadow:
        0 12px 28px rgba(15, 23, 42, 0.12);

    transition:
        transform .25s ease,
        box-shadow .25s ease;
}

.score-box:hover {
    transform: translateY(-3px);

    box-shadow:
        0 18px 36px rgba(15, 23, 42, 0.17);
}

.score-box::after {
    content: "";

    position: absolute;

    width: 180px;
    height: 180px;

    right: -75px;
    top: -80px;

    border-radius: 50%;

    background: rgba(255, 255, 255, .12);
}

.score-box.official {
    background:
        linear-gradient(
            135deg,
            #2563eb 0%,
            #1d4ed8 100%
        );
}

.score-box.ai {
    background:
        linear-gradient(
            135deg,
            #0f766e 0%,
            #0d9488 100%
        );
}

.score-top {
    position: relative;
    z-index: 1;

    display: flex;
    align-items: center;
    gap: 10px;
}

.score-icon {
    width: 32px;
    height: 32px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 10px;
    background: rgba(255, 255, 255, .15);

    font-size: 15px;
    font-weight: 800;
}

.score-label {
    font-size: 12px;
    font-weight: 700;

    text-transform: uppercase;
    letter-spacing: 1px;

    opacity: .9;
}

.score-value {
    position: relative;
    z-index: 1;

    margin-top: 24px;

    font-size: 52px;
    line-height: 1;

    font-weight: 800;
}

.score-description {
    position: relative;
    z-index: 1;

    margin-top: 12px;

    font-size: 13px;

    opacity: .82;
}


/* ==========================================================
   GENERIC PANEL
========================================================== */

.panel {
    padding: 24px;

    border-radius: 22px;

    background: #f8fafc;
    border: 1px solid #e2e8f0;

    display: flex;
    flex-direction: column;
    gap: 22px;
}

.panel-heading {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 20px;
}

.panel-kicker {
    margin-bottom: 5px;

    font-size: 11px;
    font-weight: 800;

    letter-spacing: 1.6px;
    text-transform: uppercase;

    color: #94a3b8;
}

.panel-heading h3 {
    margin: 0;

    font-size: 18px;
    font-weight: 750;

    color: #0f172a;
}


/* ==========================================================
   SCORE SCALE
========================================================== */

.score-scale-panel {
    background:
        linear-gradient(
            180deg,
            #f8fafc 0%,
            #ffffff 100%
        );
}

.scale-score {
    font-size: 22px;
    font-weight: 800;
    color: #0f766e;
}

.scale-score span {
    font-size: 13px;
    font-weight: 600;
    color: #94a3b8;
}

.score-scale {
    padding: 10px 4px 0;
}

.scale-track {
    position: relative;

    height: 12px;

    border-radius: 999px;

    background:
        linear-gradient(
            90deg,
            #ef4444 0%,
            #f59e0b 30%,
            #eab308 50%,
            #22c55e 75%,
            #16a34a 100%
        );
}

.scale-progress {
    position: absolute;

    left: 0;
    top: 0;
    bottom: 0;

    border-radius: 999px;

    background: rgba(255, 255, 255, .12);
}

.scale-marker {
    position: absolute;

    top: 50%;

    width: 20px;
    height: 20px;

    transform:
        translate(-50%, -50%);

    border-radius: 50%;

    background: #ffffff;

    border: 4px solid #0f766e;

    box-shadow:
        0 3px 12px rgba(15, 118, 110, .3);
}

.scale-marker span {
    position: absolute;

    left: 50%;
    bottom: calc(100% + 9px);

    transform: translateX(-50%);

    padding: 5px 8px;

    border-radius: 8px;

    background: #0f172a;
    color: #ffffff;

    font-size: 11px;
    font-weight: 750;

    white-space: nowrap;
}

.scale-labels {
    display: flex;
    justify-content: space-between;

    margin-top: 10px;

    font-size: 11px;
    font-weight: 600;

    color: #94a3b8;
}

.scale-footer {
    display: flex;
    justify-content: space-between;
    gap: 20px;

    font-size: 12px;
    color: #64748b;
}

.scale-footer strong {
    color: #334155;
}


/* ==========================================================
   APPROVAL
========================================================== */

.approval-panel {
    background: #f8fafc;
}

.approval-value {
    font-size: 28px;
    font-weight: 800;
    color: #2563eb;
}

.approval-progress {
    width: 100%;
    height: 12px;

    overflow: hidden;

    border-radius: 999px;

    background: #e2e8f0;
}

.approval-progress-value {
    height: 100%;

    border-radius: inherit;

    background:
        linear-gradient(
            90deg,
            #2563eb,
            #0d9488
        );

    transition: width .5s ease;
}

.approval-footer {
    display: flex;
    justify-content: space-between;

    font-size: 12px;
    color: #94a3b8;
}

.approval-footer span:last-child {
    color: #475569;
    font-weight: 650;
}


/* ==========================================================
   LIMIT
========================================================== */

.limit-card {
    position: relative;

    padding: 26px;

    border-radius: 22px;

    background:
        linear-gradient(
            135deg,
            #eff6ff 0%,
            #ecfeff 100%
        );

    border: 1px solid #bae6fd;

    transition:
        transform .25s ease,
        box-shadow .25s ease;
}

.limit-card:hover {
    transform: translateY(-2px);

    box-shadow:
        0 14px 30px rgba(14, 165, 233, .10);
}

.limit-content {
    display: flex;
    align-items: center;
    gap: 18px;
}

.limit-icon {
    width: 52px;
    height: 52px;

    flex-shrink: 0;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 16px;

    background: #ffffff;

    color: #0f766e;

    font-size: 12px;
    font-weight: 850;

    box-shadow:
        0 6px 16px rgba(15, 23, 42, .07);
}

.limit-title {
    font-size: 12px;
    font-weight: 700;

    text-transform: uppercase;
    letter-spacing: 1px;

    color: #64748b;
}

.limit-value {
    margin-top: 6px;

    font-size: 30px;
    line-height: 1.1;

    font-weight: 800;

    color: #0f172a;
}

.limit-description {
    margin-top: 7px;

    font-size: 12px;

    color: #64748b;
}


/* ==========================================================
   FINANCIAL SNAPSHOT
========================================================== */

.snapshot-grid {
    display: grid;

    grid-template-columns:
        repeat(3, minmax(0, 1fr));

    gap: 14px;
}

.snapshot-item {
    display: flex;
    align-items: center;

    gap: 12px;

    min-height: 78px;

    padding: 15px;

    border-radius: 16px;

    background: #ffffff;

    border: 1px solid #e2e8f0;

    transition:
        transform .2s ease,
        box-shadow .2s ease;
}

.snapshot-item:hover {
    transform: translateY(-2px);

    box-shadow:
        0 8px 20px rgba(15, 23, 42, .06);
}

.snapshot-icon {
    width: 38px;
    height: 38px;

    flex-shrink: 0;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 11px;

    font-size: 12px;
    font-weight: 800;
}

.snapshot-icon.income {
    background: #dcfce7;
    color: #15803d;
}

.snapshot-icon.obligations {
    background: #fef3c7;
    color: #b45309;
}

.snapshot-icon.debt {
    background: #fee2e2;
    color: #b91c1c;
}

.snapshot-icon.contracts {
    background: #ede9fe;
    color: #6d28d9;
}

.snapshot-icon.balance {
    background: #dbeafe;
    color: #1d4ed8;
}

.snapshot-icon.dti {
    background: #ccfbf1;
    color: #0f766e;
}

.snapshot-info {
    min-width: 0;

    display: flex;
    flex-direction: column;
    gap: 4px;
}

.snapshot-info span {
    font-size: 11px;
    color: #94a3b8;
}

.snapshot-info strong {
    font-size: 14px;
    font-weight: 750;

    color: #0f172a;

    white-space: nowrap;
}


/* ==========================================================
   AI ANALYSIS
========================================================== */

.ai-analysis-panel {
    background:
        linear-gradient(
            180deg,
            #f8fafc 0%,
            #ffffff 100%
        );
}

.ai-badge {
    display: inline-flex;
    align-items: center;

    padding: 8px 11px;

    border-radius: 10px;

    background: #ecfeff;
    color: #0f766e;

    font-size: 11px;
    font-weight: 750;
}

.metrics {
    display: grid;

    grid-template-columns:
        repeat(3, minmax(0, 1fr));

    gap: 14px;
}


/* ==========================================================
   DARK MODE
========================================================== */

.dark .credit-card {
    background: #0f172a;
    border-color: #1e293b;
}

.dark .card-subtitle,
.dark .panel-heading h3,
.dark .limit-value,
.dark .snapshot-info strong {
    color: #f8fafc;
}

.dark .card-description,
.dark .card-title,
.dark .panel-kicker,
.dark .snapshot-info span,
.dark .limit-description,
.dark .scale-labels,
.dark .scale-footer,
.dark .approval-footer {
    color: #94a3b8;
}

.dark .panel,
.dark .snapshot-item {
    background: #111827;
    border-color: #1f2937;
}

.dark .scale-footer strong,
.dark .approval-footer span:last-child {
    color: #cbd5e1;
}

.dark .limit-card {
    background: #102a33;
    border-color: #164e63;
}

.dark .limit-icon {
    background: #0f172a;
}


/* ==========================================================
   RESPONSIVE
========================================================== */

@media (max-width: 1100px) {

    .snapshot-grid,
    .metrics {
        grid-template-columns:
            repeat(2, minmax(0, 1fr));
    }
}


@media (max-width: 900px) {

    .scores-grid {
        grid-template-columns: 1fr;
    }

    .snapshot-grid,
    .metrics {
        grid-template-columns:
            repeat(2, minmax(0, 1fr));
    }
}


@media (max-width: 768px) {

    .credit-card {
        padding: 22px;
        border-radius: 22px;
    }

    .card-header {
        flex-direction: column;
    }

    .card-subtitle {
        font-size: 24px;
    }

    .panel {
        padding: 20px;
    }

    .panel-heading {
        flex-direction: column;
    }

    .scale-footer {
        flex-direction: column;
        gap: 8px;
    }

    .snapshot-grid,
    .metrics {
        grid-template-columns: 1fr;
    }

    .limit-value {
        font-size: 26px;
    }
}


@media (max-width: 480px) {

    .credit-card {
        padding: 16px;
    }

    .score-box {
        min-height: 165px;
        padding: 20px;
    }

    .score-value {
        font-size: 42px;
    }

    .risk-badge {
        width: 100%;
        justify-content: center;
    }

    .limit-content {
        align-items: flex-start;
    }

    .limit-icon {
        width: 44px;
        height: 44px;
    }

    .limit-value {
        font-size: 23px;
    }

    .snapshot-item {
        min-height: 70px;
    }
}

</style>