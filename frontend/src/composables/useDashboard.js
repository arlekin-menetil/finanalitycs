import { ref, computed, onMounted } from "vue"

import api from "@/api/axios"

// ==========================================
// STATE
// ==========================================

const loading = ref(false)

const error = ref(null)

const profile = ref(null)

// AI Score
const scoring = ref(null)

// Official Credit Report
const creditReport = ref(null)

const recommendations = ref([])

const safeProducts = ref([])

const premiumProducts = ref([])

// ==========================================
// LOAD DASHBOARD
// ==========================================

async function loadDashboard() {

    loading.value = true

    error.value = null

    try {

        const { data } = await api.get(
            "/scoring/dashboard/"
        )

        profile.value = data.profile || null

        scoring.value = data.scoring || null

        creditReport.value = data.credit_report || null

        recommendations.value =
            data.recommendations || []

        safeProducts.value =
            data.safe_products || []

        premiumProducts.value =
            data.premium_products || []

    }

    catch (err) {

        console.error(err)

        error.value = err

    }

    finally {

        loading.value = false

    }

}

// ==========================================
// COMPUTED
// ==========================================

const hasRecommendations = computed(() =>

    recommendations.value.length > 0

)

const recommendationCount = computed(() =>

    recommendations.value.length

)

const hasCreditReport = computed(() =>

    creditReport.value !== null

)

const hasScoring = computed(() =>

    scoring.value !== null

)

// ==========================================
// EXPORT
// ==========================================

export function useDashboard() {

    onMounted(() => {

        loadDashboard()

    })

    return {

        loading,

        error,

        profile,

        // AI
        scoring,

        // Official
        creditReport,

        recommendations,

        safeProducts,

        premiumProducts,

        hasRecommendations,

        recommendationCount,

        hasCreditReport,

        hasScoring,

        reload: loadDashboard,

    }

}