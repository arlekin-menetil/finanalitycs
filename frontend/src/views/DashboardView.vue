<script setup>
import DashboardHeader from "@/components/dashboard/DashboardHeader.vue"
import DashboardKPI from "@/components/dashboard/DashboardKPI.vue"
import CreditScoreCard from "@/components/dashboard/CreditScoreCard.vue"
import RecommendationList from "@/components/dashboard/RecommendationList.vue"

import { useDashboard } from "@/composables/useDashboard"

const {
    loading,
    error,
    profile,
    scoring,
    creditReport,
    recommendations,
} = useDashboard()
</script>

<template>
    <div class="dashboard-page">

        <!-- ===================================== -->
        <!-- LOADING -->
        <!-- ===================================== -->

        <div
            v-if="loading"
            class="dashboard-loading"
        >
            <div class="loading-spinner"></div>

            <span>Загрузка Dashboard...</span>
        </div>

        <!-- ===================================== -->
        <!-- ERROR -->
        <!-- ===================================== -->

        <div
            v-else-if="error"
            class="dashboard-error"
        >
            <div class="error-icon">
                !
            </div>

            <div>
                <div class="error-title">
                    Не удалось загрузить Dashboard
                </div>

                <div class="error-text">
                    Проверьте подключение к серверу и попробуйте обновить страницу.
                </div>
            </div>
        </div>

        <!-- ===================================== -->
        <!-- DASHBOARD -->
        <!-- ===================================== -->

        <template v-else>

            <!-- ================================= -->
            <!-- HEADER -->
            <!-- ================================= -->

            <DashboardHeader
                :user-name="profile?.full_name"
                :profile-completed="profile?.profile_completed"
                :employment-verified="profile?.employment_verified"
                :last-ai-update="scoring?.created_at"
                :profile-version="scoring?.profile_version"
            />

            <!-- ================================= -->
            <!-- CREDIT SCORE -->
            <!-- ================================= -->

            <CreditScoreCard
                :score="scoring"
                :credit-report="creditReport"
                :profile="profile"
            />

            <!-- ================================= -->
            <!-- RECOMMENDATIONS -->
            <!-- ================================= -->

        </template>

    </div>
</template>

<style scoped>

.dashboard-page {
    width: 100%;
    max-width: 1400px;
    margin: 0 auto;

    padding: 32px;

    display: flex;
    flex-direction: column;

    gap: 32px;

    box-sizing: border-box;
}

/* ========================================= */
/* LOADING */
/* ========================================= */

.dashboard-loading {
    min-height: 420px;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    gap: 16px;

    color: #64748b;

    font-size: 16px;
    font-weight: 600;
}

.loading-spinner {
    width: 38px;
    height: 38px;

    border-radius: 50%;

    border: 4px solid #e2e8f0;
    border-top-color: #2563eb;

    animation: dashboard-spin 0.8s linear infinite;
}

@keyframes dashboard-spin {
    to {
        transform: rotate(360deg);
    }
}

/* ========================================= */
/* ERROR */
/* ========================================= */

.dashboard-error {
    display: flex;
    align-items: center;

    gap: 16px;

    padding: 22px 24px;

    border-radius: 20px;

    background: #fef2f2;

    border: 1px solid #fecaca;

    color: #991b1b;
}

.error-icon {
    width: 42px;
    height: 42px;

    flex-shrink: 0;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 12px;

    background: #fee2e2;

    color: #dc2626;

    font-size: 20px;
    font-weight: 800;
}

.error-title {
    font-size: 15px;
    font-weight: 700;

    margin-bottom: 4px;
}

.error-text {
    font-size: 14px;

    color: #b91c1c;

    line-height: 1.5;
}

/* ========================================= */
/* RESPONSIVE */
/* ========================================= */

@media (max-width: 1024px) {

    .dashboard-page {
        padding: 28px;
        gap: 28px;
    }

}

@media (max-width: 768px) {

    .dashboard-page {
        padding: 20px;
        gap: 24px;
    }

    .dashboard-loading {
        min-height: 320px;
    }

    .dashboard-error {
        padding: 18px;
    }

}

@media (max-width: 480px) {

    .dashboard-page {
        padding: 16px;
        gap: 20px;
    }

    .dashboard-error {
        align-items: flex-start;
    }

    .error-icon {
        width: 36px;
        height: 36px;

        border-radius: 10px;

        font-size: 17px;
    }

    .error-title {
        font-size: 14px;
    }

    .error-text {
        font-size: 13px;
    }

}

</style>