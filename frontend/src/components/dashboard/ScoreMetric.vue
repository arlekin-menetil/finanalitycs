<template>

    <div class="metric-card">

        <div class="metric-header">

            <span class="metric-title">

                {{ title }}

            </span>

        </div>

        <div class="metric-value">

            {{ value }}

        </div>

    </div>

</template>

<script setup>

defineProps({

    title: {

        type: String,

        default: "",

    },

    value: {

        type: [Number, String],

        default: 0,

    },

})

</script>

<style scoped>

/* ==========================================
   METRIC CARD
========================================== */

.metric-card {

    background: #ffffff;

    border: 1px solid #e2e8f0;

    border-radius: 18px;

    padding: 20px;

    transition: .25s;

    display: flex;

    flex-direction: column;

    gap: 14px;

}

.metric-card:hover {

    transform: translateY(-3px);

    box-shadow: 0 12px 28px rgba(15,23,42,.08);

}

/* ==========================================
   HEADER
========================================== */

.metric-header {

    display: flex;

    justify-content: space-between;

    align-items: center;

}

.metric-title {

    font-size: 13px;

    font-weight: 600;

    text-transform: uppercase;

    letter-spacing: 1px;

    color: #64748b;

}

/* ==========================================
   VALUE
========================================== */

.metric-value {

    font-size: 28px;

    font-weight: 700;

    color: #0f172a;

    line-height: 1.2;

    word-break: break-word;

}

/* ==========================================
   DARK MODE
========================================== */

.dark .metric-card {

    background: #111827;

    border-color: #1f2937;

}

.dark .metric-title {

    color: #94a3b8;

}

.dark .metric-value {

    color: #f8fafc;

}

/* ==========================================
   RESPONSIVE
========================================== */

@media (max-width: 768px) {

    .metric-card {

        padding: 16px;

    }

    .metric-value {

        font-size: 24px;

    }

}

@media (max-width: 480px) {

    .metric-card {

        padding: 14px;

    }

    .metric-title {

        font-size: 12px;

    }

    .metric-value {

        font-size: 20px;

    }

}

</style>