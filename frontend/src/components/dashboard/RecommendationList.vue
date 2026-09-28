<template>

    <section class="recommendations">

        <!-- ================================= -->
        <!-- HEADER -->
        <!-- ================================= -->

        <div class="recommendations-header">

            <div>

                <h2 class="recommendations-title">

                    {{ t("recommendations.title") }}

                </h2>

                <p class="recommendations-description">

                    {{ t("recommendations.subtitle") }}

                </p>

            </div>


            <div class="recommendations-counter">

                {{ recommendations.length }}

                <span>

                    {{ t("recommendations.offers") }}

                </span>

            </div>

        </div>


        <!-- ================================= -->
        <!-- PRODUCTS -->
        <!-- ================================= -->

        <div
            v-if="recommendations.length"
            class="recommendations-grid"
        >

            <RecommendationCard

                v-for="recommendation in recommendations"

                :key="recommendation.product_id"

                :recommendation="recommendation"

            />

        </div>


        <!-- ================================= -->
        <!-- EMPTY -->
        <!-- ================================= -->

        <div
            v-else
            class="recommendations-empty"
        >

            <div class="empty-icon">

                🏦

            </div>


            <h3>

                {{ t("recommendations.empty") }}

            </h3>


            <p>

                {{ t("recommendations.emptyDescription") }}

            </p>

        </div>

    </section>

</template>


<script setup>

import { useI18n } from "vue-i18n"

import RecommendationCard from "./RecommendationCard.vue"


const { t } = useI18n()


defineProps({

    recommendations: {

        type: Array,

        default: () => [],

    },

})

</script>


<style scoped>

/* ==========================================================
   SECTION
========================================================== */

.recommendations{

    display:flex;

    flex-direction:column;

    gap:30px;

}


/* ==========================================================
   HEADER
========================================================== */

.recommendations-header{

    display:flex;

    justify-content:space-between;

    align-items:center;

    gap:24px;

    flex-wrap:wrap;

}


.recommendations-title{

    margin:0;

    font-size:34px;

    font-weight:700;

    color:#0f172a;

}


.recommendations-description{

    margin-top:10px;

    max-width:700px;

    line-height:1.8;

    color:#64748b;

    font-size:15px;

}


/* ==========================================================
   COUNTER
========================================================== */

.recommendations-counter{

    display:flex;

    flex-direction:column;

    align-items:center;

    justify-content:center;

    min-width:140px;

    padding:18px;

    border-radius:22px;

    background:#ffffff;

    border:1px solid #e2e8f0;

    box-shadow:0 12px 28px rgba(15,23,42,.05);

    font-size:38px;

    font-weight:700;

    color:#2563eb;

}


.recommendations-counter span{

    margin-top:4px;

    font-size:13px;

    font-weight:500;

    color:#64748b;

}


/* ==========================================================
   GRID
========================================================== */

.recommendations-grid{

    display:grid;

    grid-template-columns:repeat(2,1fr);

    gap:24px;

}


/* ==========================================================
   EMPTY
========================================================== */

.recommendations-empty{

    padding:60px;

    border-radius:28px;

    border:2px dashed #cbd5e1;

    background:#ffffff;

    text-align:center;

}


.empty-icon{

    font-size:64px;

    margin-bottom:22px;

}


.recommendations-empty h3{

    margin:0;

    font-size:28px;

    font-weight:700;

    color:#0f172a;

}


.recommendations-empty p{

    margin:18px auto 0;

    max-width:620px;

    line-height:1.8;

    color:#64748b;

}


/* ==========================================================
   DARK
========================================================== */

.dark .recommendations-title{

    color:white;

}


.dark .recommendations-description{

    color:#94a3b8;

}


.dark .recommendations-counter{

    background:#0f172a;

    border-color:#1e293b;

    box-shadow:none;

}


.dark .recommendations-counter span{

    color:#94a3b8;

}


.dark .recommendations-empty{

    background:#0f172a;

    border-color:#334155;

}


.dark .recommendations-empty h3{

    color:white;

}


.dark .recommendations-empty p{

    color:#94a3b8;

}


/* ==========================================================
   RESPONSIVE
========================================================== */

@media (max-width:1200px){

    .recommendations-grid{

        grid-template-columns:1fr;

    }

}


@media (max-width:768px){

    .recommendations-header{

        flex-direction:column;

        align-items:flex-start;

    }


    .recommendations-counter{

        width:100%;

    }

}


@media (max-width:600px){

    .recommendations-title{

        font-size:28px;

    }


    .recommendations-empty{

        padding:36px 24px;

    }


    .empty-icon{

        font-size:52px;

    }

}

</style>