<script setup>
import {
  ref,
  computed,
  onMounted,
} from "vue"

import { useI18n } from "vue-i18n"
import api from "@/api/axios"
import { useRouter } from "vue-router"

import PersonalInfoCard from "@/components/profile/PersonalInfoCard.vue"
import FinancialInfoCard from "@/components/profile/FinancialInfoCard.vue"
import ScoreCard from "@/components/profile/ScoreCard.vue"
import CreditReportUpload from "@/components/profile/CreditReportUpload.vue"
import GovernmentServicesCard from "@/components/profile/GovernmentServicesCard.vue"
import AiAnalysisCard from "@/components/profile/AiAnalysisCard.vue"
import EmploymentVerificationCard from "@/components/profile/EmploymentVerificationCard.vue"
import RecommendationsCard from "@/components/profile/RecommendationsCard.vue"

const { t } = useI18n()

const router = useRouter()

// =====================================================
// STATE
// =====================================================

const loading = ref(true)

const error = ref(null)

const dashboard = ref(null)

const creditReport = ref(null)

const creditContracts = ref([])

// =====================================================
// PROFILE DATA
// =====================================================

const profileData = computed(() => {
  const profile = dashboard.value?.profile || {}

  return {
    // ======================================
    // USER
    // ======================================

    user:
      dashboard.value?.user || {},

    profile,

    // ======================================
    // BANKS
    // ======================================

    recommendations:
      dashboard.value?.recommendations || [],

    // ======================================
    // CREDIT
    // ======================================

    creditReport:
      creditReport.value,

    contracts:
      creditContracts.value,

    // ======================================
    // FINANCIAL (ТОЛЬКО PROFILE)
    // ======================================

    income:
      Number(profile.income || 0),

    expenses:
      Number(profile.expenses || 0),

    netBalance:
      Number(profile.net_balance || 0),

    dti:
      Number(profile.dti || 0),

    // ======================================
    // CREDIT REPORT
    // ======================================

    totalDebt:
      Number(
        creditReport.value?.total_debt || 0,
      ),

    overdueDebt:
      Number(
        creditReport.value?.overdue_debt || 0,
      ),

    contractsCount:
      Number(
        creditReport.value?.contracts_count ||
        creditReport.value?.contracts_total ||
        creditContracts.value.length ||
        0,
      ),

    // ======================================
    // SCORE
    // ======================================

    score:
      Number(
        creditReport.value?.credit_score ||
        dashboard.value?.score?.credit_score ||
        0,
      ),

    risk:
      creditReport.value?.risk_class ||
      dashboard.value?.score?.risk_category ||
      "",
  }
})

// =====================================================
// LOAD DASHBOARD
// =====================================================

const loadDashboard = async () => {
  loading.value = true
  error.value = null

  try {
    const [
      dashboardResponse,
      reportResponse,
      contractsResponse,
    ] = await Promise.allSettled([
      api.get("/profile/dashboard/"),
      api.get("/credit-analysis/report/"),
      api.get("/credit-analysis/contracts/"),
    ])

    // ======================================
    // DASHBOARD
    // ======================================

    if (dashboardResponse.status === "fulfilled") {
      dashboard.value =
        dashboardResponse.value.data
    } else {
      dashboard.value = null
    }

    // ======================================
    // CREDIT REPORT
    // ======================================

    if (reportResponse.status === "fulfilled") {
      creditReport.value =
        reportResponse.value.data
    } else {
      creditReport.value = null
    }

    // ======================================
    // CONTRACTS
    // ======================================

    if (contractsResponse.status === "fulfilled") {
      creditContracts.value =
        contractsResponse.value.data
    } else {
      creditContracts.value = []
    }

    // ======================================
    // DEBUG
    // ======================================

    console.group("📊 PROFILE DASHBOARD")

    console.log(
      "Dashboard",
      dashboard.value,
    )

    console.log(
      "Profile",
      dashboard.value?.profile,
    )

    console.log(
      "Income",
      dashboard.value?.profile?.income,
    )

    console.log(
      "Expenses",
      dashboard.value?.profile?.expenses,
    )

    console.log(
      "Net Balance",
      dashboard.value?.profile?.net_balance,
    )

    console.log(
      "DTI",
      dashboard.value?.profile?.dti,
    )

    console.groupEnd()

    console.group("📄 CREDIT REPORT")

    console.log(
      creditReport.value,
    )

    console.groupEnd()

    console.group("📑 CONTRACTS")

    console.log(
      creditContracts.value,
    )

    console.groupEnd()

    console.group("📦 PROFILE DATA")

    console.log(
      profileData.value,
    )

    console.groupEnd()
  }

  catch (e) {
    console.error(e)

    error.value =
      e.response?.data?.detail ||
      t("profileView.errors.loadFailed")
  }

  finally {
    loading.value = false
  }
}

// =====================================================
// EDIT PROFILE
// =====================================================

const editProfile = async () => {
  await router.push(
    "/app/profile/edit",
  )
}

// =====================================================
// INIT
// =====================================================

onMounted(() => {
  console.count("Profile mounted")

  loadDashboard()
})
</script>

<template>
  <div class="profile-page">
    <!-- ===================================== -->
    <!-- LOADING -->
    <!-- ===================================== -->

    <div
      v-if="loading"
      class="loading"
    >
      {{ t("profileView.loading") }}
    </div>

    <!-- ===================================== -->
    <!-- ERROR -->
    <!-- ===================================== -->

    <div
      v-else-if="error"
      class="error"
    >
      {{ error }}
    </div>

    <!-- ===================================== -->
    <!-- PROFILE -->
    <!-- ===================================== -->

    <template v-else>
      <h1 class="title">
        👤 {{ t("profileView.title") }}
      </h1>

      <!-- ===================================== -->
      <!-- PERSONAL -->
      <!-- ===================================== -->

      <PersonalInfoCard
        :profile="profileData.profile"
        :user="profileData.user"
        @edit="editProfile"
      />

      <!-- ===================================== -->
      <!-- EMPLOYMENT -->
      <!-- ===================================== -->

      <EmploymentVerificationCard
        :profile="profileData.profile"
        @uploaded="loadDashboard"
      />

      <!-- ===================================== -->
      <!-- FINANCIAL GRID -->
      <!-- ===================================== -->

      <div class="grid">
        <FinancialInfoCard
          :profile="profileData"
        />

        <ScoreCard
          :score="profileData"
        />

        <AiAnalysisCard
          :profile="profileData"
          :score="profileData"
          :recommendations="profileData.recommendations"
        />
      </div>

      <!-- ===================================== -->
      <!-- CREDIT HISTORY -->
      <!-- ===================================== -->

      <CreditReportUpload
        :credit-report="profileData.creditReport"
        :contracts="profileData.contracts"
        @uploaded="loadDashboard"
      />

      <!-- ===================================== -->
      <!-- RECOMMENDATIONS -->
      <!-- ===================================== -->

      <RecommendationsCard
        :recommendations="profileData.recommendations"
        :credit-report="profileData.creditReport"
      />

      <!-- ===================================== -->
      <!-- GOVERNMENT SERVICES -->
      <!-- ===================================== -->

      <GovernmentServicesCard />
    </template>
  </div>
</template>

<style scoped>
.profile-page {
  max-width: 1400px;
  margin: auto;
  padding: 30px;
}

.title {
  font-size: 34px;
  font-weight: 700;
  margin-bottom: 30px;
}

.loading {
  padding: 70px;
  text-align: center;
  font-size: 20px;
}

.error {
  padding: 70px;
  text-align: center;
  color: #ef4444;
  font-size: 20px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 22px;
  margin-bottom: 25px;
}

@media (max-width: 1200px) {
  .grid {
    grid-template-columns: 1fr;
  }
}
</style>