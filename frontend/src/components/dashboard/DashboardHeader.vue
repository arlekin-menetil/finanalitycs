<template>

    <section class="dashboard-header">

        <!-- Background -->
        <div class="dashboard-background"></div>


        <!-- Content -->
        <div class="dashboard-content">

            <!-- LEFT -->
            <div class="dashboard-left">

                <!-- Badge -->
                <div class="dashboard-badge">

                    <span class="badge-icon">
                        ✦
                    </span>

                    <span>
                        BankAnalytics AI
                    </span>

                </div>


                <!-- Welcome -->
                <div class="welcome-block">

                    <span class="welcome-label">
                        {{ t("dashboard.financialCabinet") }}
                    </span>


                    <h1 class="dashboard-title">

                        {{ t("dashboard.welcome") }},

                        <span class="user-name">
                            {{ displayName }}
                        </span>

                        <span class="wave">
                            👋
                        </span>

                    </h1>


                    <p class="dashboard-description">
                        {{ t("dashboard.description") }}
                    </p>

                </div>


                <!-- Features -->
                <div class="dashboard-features">

                    <!-- Profile -->
                    <div class="feature">

                        <span
                            class="dot"
                            :class="{
                                inactive: !profileCompleted
                            }"
                        ></span>


                        <span class="feature-label">
                            {{ t("dashboard.profile") }}
                        </span>


                        <strong>
                            {{
                                profileCompleted
                                    ? t("dashboard.profileCompleted")
                                    : t("dashboard.profileNotCompleted")
                            }}
                        </strong>

                    </div>


                    <!-- Employment -->
                    <div class="feature">

                        <span
                            class="dot"
                            :class="{
                                inactive: !employmentVerified
                            }"
                        ></span>


                        <span class="feature-label">
                            {{ t("dashboard.employment") }}
                        </span>


                        <strong>
                            {{
                                employmentVerified
                                    ? t("dashboard.employmentVerified")
                                    : t("dashboard.employmentNotVerified")
                            }}
                        </strong>

                    </div>

                </div>

            </div>


            <!-- RIGHT -->
            <div class="dashboard-right">

                <!-- AI UPDATE CARD -->
                <div class="update-card">

                    <div class="update-card-glow"></div>


                    <div class="update-icon">
                        ✦
                    </div>


                    <div class="update-title">
                        {{ t("dashboard.lastAiAnalysis") }}
                    </div>


                    <div class="update-value">
                        {{ formattedDate }}
                    </div>


                    <div class="update-subtitle">

                        <span class="version-dot"></span>

                        {{ t("dashboard.profileVersion") }}
                        {{ profileVersion }}

                    </div>


                    <div class="update-status">

                        <span class="status-icon">
                            ✓
                        </span>

                        {{ t("dashboard.analysisCompleted") }}

                    </div>

                </div>

            </div>

        </div>

    </section>

</template>


<script setup>

import { computed } from "vue"
import { useI18n } from "vue-i18n"


// ==========================================================
// I18N
// ==========================================================

const { t, locale } = useI18n()


// ==========================================================
// PROPS
// ==========================================================

const props = defineProps({

    userName: {
        type: String,
        default: "",
    },

    profileCompleted: {
        type: Boolean,
        default: false,
    },

    employmentVerified: {
        type: Boolean,
        default: false,
    },

    lastAiUpdate: {
        type: String,
        default: "",
    },

    profileVersion: {
        type: Number,
        default: 1,
    },

})


// ==========================================================
// USER NAME
// ==========================================================

const displayName = computed(() => {

    const name = String(
        props.userName || ""
    ).trim()


    if (!name) {
        return t("common.user")
    }


    /*
     * Если backend отдаёт полное ФИО,
     * стараемся сделать заголовок аккуратнее.
     */

    const parts = name
        .split(/\s+/)
        .filter(Boolean)


    if (parts.length >= 2) {
        return parts
            .slice(0, 2)
            .join(" ")
    }


    return name

})


// ==========================================================
// DATE
// ==========================================================

const formattedDate = computed(() => {

    if (!props.lastAiUpdate) {
        return "-"
    }


    const date = new Date(
        props.lastAiUpdate
    )


    if (Number.isNaN(date.getTime())) {
        return "-"
    }


    /*
     * Формат даты зависит от выбранного языка.
     *
     * RU -> 25.09.2026
     * EN -> 09/25/2026
     * UZ -> 25/09/2026
     */

    const localeMap = {
        ru: "ru-RU",
        en: "en-US",
        uz: "uz-UZ",
    }


    return date.toLocaleDateString(
        localeMap[locale.value] || "ru-RU",
        {
            day: "2-digit",
            month: "2-digit",
            year: "numeric",
        }
    )

})

</script>


<style scoped>

/* ==========================================================
   DASHBOARD HEADER
========================================================== */

.dashboard-header {
    position: relative;
    overflow: hidden;

    border-radius: 30px;
    padding: 42px;

    background:
        linear-gradient(
            135deg,
            #1d4ed8 0%,
            #2563eb 35%,
            #3b82f6 70%,
            #60a5fa 100%
        );

    color: #fff;

    box-shadow:
        0 30px 70px rgba(37, 99, 235, 0.28);

    animation:
        headerFade 0.5s ease;
}


/* ==========================================================
   BACKGROUND
========================================================== */

.dashboard-background {
    position: absolute;
    inset: 0;

    overflow: hidden;

    pointer-events: none;
}


.dashboard-background::before {
    content: "";

    position: absolute;

    width: 620px;
    height: 620px;

    right: -260px;
    top: -260px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(255, 255, 255, 0.22),
            transparent 72%
        );
}


.dashboard-background::after {
    content: "";

    position: absolute;

    width: 360px;
    height: 360px;

    left: -160px;
    bottom: -160px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(255, 255, 255, 0.10),
            transparent 72%
        );
}


/* ==========================================================
   CONTENT
========================================================== */

.dashboard-content {
    position: relative;
    z-index: 5;

    display: flex;
    justify-content: space-between;
    align-items: center;

    gap: 60px;
}


/* ==========================================================
   LEFT
========================================================== */

.dashboard-left {
    flex: 1;
    max-width: 780px;
}


/* ==========================================================
   BADGE
========================================================== */

.dashboard-badge {
    display: inline-flex;
    align-items: center;

    gap: 10px;

    padding: 10px 17px;

    border-radius: 999px;

    background: rgba(255, 255, 255, 0.14);

    backdrop-filter: blur(18px);

    border: 1px solid rgba(255, 255, 255, 0.15);

    font-size: 12px;
    font-weight: 800;

    text-transform: uppercase;
    letter-spacing: 0.13em;

    transition:
        transform 0.28s ease,
        background 0.28s ease;
}


.dashboard-badge:hover {
    transform: translateY(-2px);

    background: rgba(255, 255, 255, 0.20);
}


.badge-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;

    width: 22px;
    height: 22px;

    border-radius: 50%;

    background: rgba(255, 255, 255, 0.18);

    font-size: 13px;
}


/* ==========================================================
   WELCOME
========================================================== */

.welcome-block {
    margin-top: 26px;
}


.welcome-label {
    display: block;

    margin-bottom: 10px;

    color: rgba(255, 255, 255, 0.68);

    font-size: 13px;
    font-weight: 600;

    letter-spacing: 0.04em;
}


/* ==========================================================
   TITLE
========================================================== */

.dashboard-title {
    margin: 0;

    font-size: 48px;
    font-weight: 800;

    line-height: 1.08;
    letter-spacing: -0.025em;
}


.user-name {
    display: inline;

    background:
        linear-gradient(
            90deg,
            #ffffff,
            #dbeafe
        );

    -webkit-background-clip: text;
    background-clip: text;

    -webkit-text-fill-color: transparent;
}


.wave {
    display: inline-block;

    margin-left: 8px;

    transform-origin: 70% 70%;

    animation:
        wave 2.5s ease-in-out infinite;
}


/* ==========================================================
   DESCRIPTION
========================================================== */

.dashboard-description {
    margin: 18px 0 0;

    max-width: 680px;

    font-size: 16px;
    line-height: 1.75;

    color: rgba(255, 255, 255, 0.88);
}


/* ==========================================================
   FEATURES
========================================================== */

.dashboard-features {
    margin-top: 30px;

    display: flex;
    flex-wrap: wrap;

    gap: 12px 26px;
}


.feature {
    display: flex;
    align-items: center;

    gap: 9px;

    min-height: 30px;

    font-size: 14px;

    color: rgba(255, 255, 255, 0.92);

    transition:
        transform 0.28s ease;
}


.feature:hover {
    transform: translateX(4px);
}


.feature-label {
    color: rgba(255, 255, 255, 0.80);
}


.feature strong {
    color: #fff;

    font-weight: 700;
}


/* ==========================================================
   STATUS DOT
========================================================== */

.dot {
    flex-shrink: 0;

    width: 9px;
    height: 9px;

    border-radius: 50%;

    background: #4ade80;

    box-shadow:
        0 0 14px rgba(74, 222, 128, 0.85);
}


.dot.inactive {
    background: #fbbf24;

    box-shadow:
        0 0 14px rgba(251, 191, 36, 0.65);
}


/* ==========================================================
   RIGHT
========================================================== */

.dashboard-right {
    width: 340px;
    flex-shrink: 0;
}


/* ==========================================================
   UPDATE CARD
========================================================== */

.update-card {
    position: relative;
    overflow: hidden;

    padding: 28px;

    min-height: 220px;

    border-radius: 26px;

    background: rgba(255, 255, 255, 0.14);

    backdrop-filter: blur(22px);

    border: 1px solid rgba(255, 255, 255, 0.18);

    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.10);

    transition:
        transform 0.30s ease,
        box-shadow 0.30s ease,
        background 0.30s ease;
}


.update-card:hover {
    transform: translateY(-6px);

    background: rgba(255, 255, 255, 0.19);

    box-shadow:
        0 22px 45px rgba(0, 0, 0, 0.18);
}


/* ==========================================================
   CARD GLOW
========================================================== */

.update-card::before {
    content: "";

    position: absolute;

    width: 190px;
    height: 190px;

    right: -80px;
    top: -80px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(255, 255, 255, 0.18),
            transparent 70%
        );
}


.update-card::after {
    content: "";

    position: absolute;

    width: 120px;
    height: 120px;

    left: -65px;
    bottom: -65px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(255, 255, 255, 0.10),
            transparent 70%
        );
}


/* ==========================================================
   UPDATE ICON
========================================================== */

.update-icon {
    position: relative;
    z-index: 2;

    display: flex;
    align-items: center;
    justify-content: center;

    width: 42px;
    height: 42px;

    border-radius: 14px;

    background: rgba(255, 255, 255, 0.15);

    border: 1px solid rgba(255, 255, 255, 0.14);

    font-size: 18px;

    box-shadow:
        0 8px 20px rgba(0, 0, 0, 0.08);
}


/* ==========================================================
   UPDATE TITLE
========================================================== */

.update-title {
    position: relative;
    z-index: 2;

    margin-top: 20px;

    font-size: 11px;
    font-weight: 700;

    letter-spacing: 0.12em;

    text-transform: uppercase;

    color: rgba(255, 255, 255, 0.70);
}


/* ==========================================================
   UPDATE VALUE
========================================================== */

.update-value {
    position: relative;
    z-index: 2;

    margin-top: 9px;

    font-size: 38px;
    font-weight: 800;

    line-height: 1;

    letter-spacing: -0.02em;
}


/* ==========================================================
   UPDATE SUBTITLE
========================================================== */

.update-subtitle {
    position: relative;
    z-index: 2;

    display: flex;
    align-items: center;

    gap: 8px;

    margin-top: 14px;

    color: rgba(255, 255, 255, 0.76);

    font-size: 13px;
}


.version-dot {
    width: 6px;
    height: 6px;

    border-radius: 50%;

    background: #93c5fd;
}


/* ==========================================================
   STATUS
========================================================== */

.update-status {
    position: relative;
    z-index: 2;

    display: inline-flex;
    align-items: center;

    gap: 7px;

    margin-top: 18px;

    padding: 7px 11px;

    border-radius: 999px;

    background: rgba(74, 222, 128, 0.13);

    border: 1px solid rgba(74, 222, 128, 0.18);

    color: #dcfce7;

    font-size: 12px;
    font-weight: 600;
}


.status-icon {
    display: inline-flex;

    align-items: center;
    justify-content: center;

    width: 17px;
    height: 17px;

    border-radius: 50%;

    background: rgba(74, 222, 128, 0.22);

    font-size: 10px;
}


/* ==========================================================
   ANIMATION
========================================================== */

@keyframes headerFade {

    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }

}


@keyframes wave {

    0%,
    60%,
    100% {
        transform: rotate(0deg);
    }

    10%,
    30% {
        transform: rotate(14deg);
    }

    20% {
        transform: rotate(-8deg);
    }

    40% {
        transform: rotate(8deg);
    }

    50% {
        transform: rotate(-4deg);
    }

}


/* ==========================================================
   RESPONSIVE
========================================================== */

@media (max-width: 1200px) {

    .dashboard-content {
        flex-direction: column;

        align-items: flex-start;

        gap: 36px;
    }


    .dashboard-left {
        max-width: 100%;
    }


    .dashboard-right {
        width: 100%;
    }


    .update-card {
        width: 100%;
    }

}


@media (max-width: 900px) {

    .dashboard-header {
        padding: 30px;
    }


    .dashboard-title {
        font-size: 36px;
    }


    .dashboard-description {
        font-size: 15px;
    }


    .dashboard-features {
        gap: 12px 20px;
    }


    .update-card {
        padding: 24px;
    }


    .update-value {
        font-size: 34px;
    }

}


@media (max-width: 600px) {

    .dashboard-header {
        padding: 22px;

        border-radius: 22px;
    }


    .dashboard-badge {
        width: 100%;

        justify-content: center;
    }


    .dashboard-title {
        font-size: 29px;

        line-height: 1.15;
    }


    .dashboard-description {
        font-size: 14px;

        line-height: 1.7;
    }


    .dashboard-features {
        flex-direction: column;

        gap: 10px;
    }


    .feature {
        font-size: 13px;
    }


    .update-card {
        min-height: auto;

        padding: 22px;
    }


    .update-value {
        font-size: 30px;
    }

}


/* ==========================================================
   DARK MODE
========================================================== */

.dark .dashboard-header {
    box-shadow:
        0 30px 70px rgba(0, 0, 0, 0.45);
}


.dark .dashboard-badge {
    background: rgba(15, 23, 42, 0.35);

    border-color:
        rgba(255, 255, 255, 0.10);
}


.dark .update-card {
    background: rgba(15, 23, 42, 0.35);

    border-color:
        rgba(255, 255, 255, 0.08);
}


.dark .update-card:hover {
    background: rgba(15, 23, 42, 0.48);
}

</style>