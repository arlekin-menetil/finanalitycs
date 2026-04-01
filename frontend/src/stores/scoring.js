import { defineStore } from "pinia"
import api from "@/api/axios"
import { useAuthStore } from "@/stores/auth"

export const useScoringStore = defineStore("scoring", {

  state: () => ({
    data: null,
    history: [],

    loading: {
      calculate: false
    },

    error: null,
    lastUpdated: null // 💣 cache
  }),

  // ==========================================
  // 🧠 GETTERS
  // ==========================================
  getters: {

    creditScore: (state) => state.data?.credit_score || 0,

    riskCategory: (state) => state.data?.risk_category || null,

    approvalProbability: (state) =>
      state.data?.approval_probability || 0,

    riskLevel: (state) => {
      const score = state.data?.credit_score || 0

      if (score >= 750) return "low"
      if (score >= 650) return "medium"
      return "high"
    },

    scoreHint: (state) => {
      const score = state.data?.credit_score || 0

      if (score >= 750) return "Отличный рейтинг"
      if (score >= 650) return "Хороший рейтинг"
      if (score >= 550) return "Средний рейтинг"
      return "Низкий рейтинг"
    },

    hasScore: (state) => !!state.data
  },

  // ==========================================
  // ⚙️ ACTIONS
  // ==========================================
  actions: {

    // ==========================================
    // 💣 CALCULATE SCORING
    // ==========================================
    async calculate(force = false) {

      const auth = useAuthStore()

      // 🚨 защита
      if (!auth.isProfileCompleted) {
        this.error = "Заполните профиль перед скорингом"
        return
      }

      // 💣 cache (30 сек)
      const now = Date.now()
      if (!force && this.lastUpdated && now - this.lastUpdated < 30000) {
        return
      }

      try {
        this.loading.calculate = true
        this.error = null

        const res = await api.post("/scoring/calculate/")

        this.data = res.data
        this.lastUpdated = Date.now()

        // 💣 история (ограничиваем)
        this.history.unshift({
          ...res.data,
          created_at: new Date()
        })

        if (this.history.length > 10) {
          this.history.pop()
        }

      } catch (e) {
        console.error("Scoring error:", e)
        this.error = e.response?.data || "Failed to calculate score"
      } finally {
        this.loading.calculate = false
      }
    },

    // ==========================================
    // 🔄 REFRESH
    // ==========================================
    async refresh() {
      await this.calculate(true)
    },

    // ==========================================
    // 🧹 RESET
    // ==========================================
    reset() {
      this.data = null
      this.error = null
      this.lastUpdated = null
    }

  }

})