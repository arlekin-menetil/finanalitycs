import { defineStore } from "pinia"
import api from "@/api/axios"

export const useRecommendationsStore = defineStore("recommendations", {

  state: () => ({
    recommendations: [],
    snapshotId: null,
    rankingVersion: null,

    marketRating: [],
    totalBanks: 0,

    loading: {
      recommendations: false,
      rating: false
    },

    error: null
  }),

  // ==========================================
  // 🧠 GETTERS
  // ==========================================
  getters: {

    topRecommendations: (state) => {
      return [...state.recommendations]
        .sort((a, b) => b.score - a.score)
        .slice(0, 3)
    },

    hasData: (state) => state.recommendations.length > 0
  },

  actions: {

    // ==========================================
    // 💣 PERSONAL RECOMMENDATIONS
    // ==========================================
    async loadRecommendations(limit = 5, force = false) {

      if (this.recommendations.length && !force) return

      try {
        this.loading.recommendations = true
        this.error = null

        const res = await api.get("/banks/recommendations/", {
          params: { limit }
        })

        if (Array.isArray(res.data)) {
          this.recommendations = res.data
        } else {
          this.recommendations = res.data.recommendations || []
          this.snapshotId = res.data.snapshot_id || null
          this.rankingVersion = res.data.ranking_version || null
        }

      } catch (e) {
        console.error("Recommendations error:", e)
        this.error = e.response?.data || "Failed to load recommendations"
      } finally {
        this.loading.recommendations = false
      }
    },

    // ==========================================
    // 🧠 CLICK TRACKING (FIXED)
    // ==========================================
    async click(productId, rankingScore = 0) {
      try {

        const payload = {
          product_id: productId
        }

        // 💣 если есть аналитика — добавляем
        if (this.snapshotId) {
          payload.snapshot_id = this.snapshotId
          payload.ranking_version = this.rankingVersion
          payload.ranking_score = rankingScore
        }

        const res = await api.post("/banks/click/", payload)

        return res.data?.interaction_id

      } catch (e) {
        console.error("Click tracking failed:", e)
      }
    },

    // ==========================================
    // 💣 APPLY TRACKING
    // ==========================================
    async apply(productId) {
      try {
        await api.post("/banks/apply/", {
          product_id: productId
        })
      } catch (e) {
        console.error("Apply tracking failed:", e)
      }
    },

    // ==========================================
    // 💣 DECISION TRACKING
    // ==========================================
    async decision(productId, approved) {
      try {
        await api.post("/banks/decision/", {
          product_id: productId,
          approved
        })
      } catch (e) {
        console.error("Decision tracking failed:", e)
      }
    },

    // ==========================================
    // 🏆 MARKET RATING
    // ==========================================
    async loadMarketRating(force = false) {

      if (this.marketRating.length && !force) return

      try {
        this.loading.rating = true
        this.error = null

        const res = await api.get("/banks/rating/")

        this.marketRating = res.data.rating || res.data || []
        this.totalBanks = res.data.total_banks || this.marketRating.length

      } catch (e) {
        console.error("Market rating error:", e)
        this.error = e.response?.data || "Failed to load market rating"
      } finally {
        this.loading.rating = false
      }
    }

  }

})