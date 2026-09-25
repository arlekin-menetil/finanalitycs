import { defineStore } from "pinia"
import api from "@/api/axios"
import { useAuthStore } from "@/stores/auth"

export const useScoringStore = defineStore("scoring", {

  // ==========================================
  // 💣 STATE
  // ==========================================
  state: () => ({

    data: null,

    history: [],

    loading: {

      calculate: false,
    },

    error: null,

    lastUpdated: null,
  }),

  // ==========================================
  // 💣 GETTERS
  // ==========================================
  getters: {

    // ==========================================
    // 💣 SCORE
    // ==========================================
    creditScore: (state) => {

      return Number(

        state.data?.credit_score ||

        state.data?.score ||

        0
      )
    },

    // ==========================================
    // 💣 RISK CATEGORY
    // ==========================================
    riskCategory: (state) => {

      return (

        state.data?.risk_category ||

        state.data?.riskLevel ||

        null
      )
    },

    // ==========================================
    // 💣 APPROVAL
    // ==========================================
    approvalProbability: (state) => {

      const raw = (

        state.data?.approval_probability ??

        state.data?.approvalProbability ??

        0
      )

      // backend already returns 0-1
      if (raw <= 1) {

        return Number(raw)
      }

      // fallback 0-100
      return Number(raw) / 100
    },

    // ==========================================
    // 💣 DERIVED RISK LEVEL
    // ==========================================
    riskLevel: (state) => {

      const score = Number(

        state.data?.credit_score ||

        state.data?.score ||

        0
      )

      if (score >= 750) {

        return "low"
      }

      if (score >= 650) {

        return "medium"
      }

      return "high"
    },

    // ==========================================
    // 💣 SCORE HINT
    // ==========================================
    scoreHint: (state) => {

      const score = Number(

        state.data?.credit_score ||

        state.data?.score ||

        0
      )

      if (score >= 800) {

        return "Отличный рейтинг"
      }

      if (score >= 700) {

        return "Хороший рейтинг"
      }

      if (score >= 600) {

        return "Средний рейтинг"
      }

      return "Низкий рейтинг"
    },

    // ==========================================
    // 💣 HAS SCORE
    // ==========================================
    hasScore: (state) => {

      return !!state.data
    },
  },

  // ==========================================
  // 💣 ACTIONS
  // ==========================================
  actions: {

    // ==========================================
    // 💣 NORMALIZE RESPONSE
    // ==========================================
    normalizeResponse(payload) {

      if (!payload) {

        return null
      }

      return {

        credit_score:

          Number(

            payload.credit_score ||

            payload.score ||

            0
          ),

        risk_category:

          payload.risk_category ||

          payload.riskLevel ||

          "medium",

        approval_probability:

          payload.approval_probability ??

          payload.approvalProbability ??

          0,

        monthly_payment:

          payload.monthly_payment ||

          0,

        max_loan_amount:

          payload.max_loan_amount ||

          0,

        recommendations:

          payload.recommendations ||

          [],
      }
    },

    // ==========================================
    // 💣 CALCULATE
    // ==========================================
    async calculate(force = false) {

      const auth = useAuthStore()

      // ==========================================
      // 💣 PROFILE CHECK
      // ==========================================
      if (!auth.isProfileCompleted) {

        this.error =
          "Заполните профиль перед скорингом"

        return
      }

      // ==========================================
      // 💣 CACHE
      // ==========================================
      const now = Date.now()

      const ONE_DAY =
        24 * 60 * 60 * 1000

      if (

        !force &&

        this.lastUpdated &&

        now - this.lastUpdated < ONE_DAY
      ) {

        return this.data
      }

      try {

        this.loading.calculate = true

        this.error = null

        // ==========================================
        // 💣 API
        // ==========================================
        const res = await api.post(
          "/scoring/calculate/"
        )

        // ==========================================
        // 💣 NORMALIZE
        // ==========================================
        this.data = this.normalizeResponse(
          res.data
        )

        this.lastUpdated = Date.now()

        return this.data

      } catch (e) {

        console.error(
          "Scoring error:",
          e
        )

        this.error = (

          e?.response?.data?.detail ||

          e?.response?.data ||

          e.message ||

          "Failed to calculate score"
        )

      } finally {

        this.loading.calculate = false
      }
    },

    // ==========================================
    // 💣 LOAD HISTORY
    // ==========================================
    async loadHistory() {

      try {

        const res = await api.get(
          "/scoring/history/"
        )

        this.history = Array.isArray(
          res.data
        )

          ? res.data

          : []

      } catch (e) {

        console.error(
          "History error:",
          e
        )
      }
    },

    // ==========================================
    // 💣 REFRESH
    // ==========================================
    async refresh() {

      return await this.calculate(true)
    },

    // ==========================================
    // 💣 RESET
    // ==========================================
    reset() {

      this.data = null

      this.history = []

      this.error = null

      this.lastUpdated = null
    },
  },
})