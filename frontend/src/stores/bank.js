import { defineStore } from "pinia"
import api from "@/api/axios"

export const useBanksStore = defineStore("banks", {

  state: () => ({
    banks: [],
    total: 0,

    products: [],
    recommendations: [],

    branches: [],
    mapBranches: [],

    loading: {
      banks: false,
      products: false,
      recommendations: false,
      branches: false,
      map: false,
    },

    error: null
  }),

  // ==========================================
  // 🧠 GETTERS
  // ==========================================
  getters: {

    hasRecommendations: (state) => state.recommendations.length > 0,

    topRecommendations: (state) => {
      return [...state.recommendations]
        .sort((a, b) => b.score - a.score)
        .slice(0, 3)
    },

  },

  actions: {

    // ==========================================
    // 🏦 BANKS
    // ==========================================
    async loadBanks(search = "") {
      if (this.banks.length && !search) return // 💣 cache

      try {
        this.loading.banks = true

        const res = await api.get("/banks/", {
          params: { search }
        })

        this.banks = res.data.banks || res.data || []
        this.total = res.data.total || this.banks.length

      } catch (e) {
        this.error = e.response?.data || "Banks error"
      } finally {
        this.loading.banks = false
      }
    },

    // ==========================================
    // 💣 PRODUCTS
    // ==========================================
    async loadProducts() {
      if (this.products.length) return

      try {
        this.loading.products = true

        const res = await api.get("/banks/products/")
        this.products = res.data

      } catch (e) {
        this.error = e.response?.data || "Products error"
      } finally {
        this.loading.products = false
      }
    },

    // ==========================================
    // 💣 RECOMMENDATIONS
    // ==========================================
    async loadRecommendations(force = false) {
      if (this.recommendations.length && !force) return

      try {
        this.loading.recommendations = true

        const res = await api.get("/banks/recommendations/")
        this.recommendations = res.data

      } catch (e) {
        this.error = e.response?.data || "Recommendations error"
      } finally {
        this.loading.recommendations = false
      }
    },

    // ==========================================
    // 🏢 BRANCHES
    // ==========================================
    async loadBranches(bankId) {
      try {
        this.loading.branches = true

        const res = await api.get(`/banks/${bankId}/branches/`)
        this.branches = res.data

      } catch (e) {
        this.error = e.response?.data || "Branches error"
      } finally {
        this.loading.branches = false
      }
    },

    // ==========================================
    // 🗺 MAP
    // ==========================================
    async loadMapBranches() {
      if (this.mapBranches.length) return

      try {
        this.loading.map = true

        const res = await api.get("/banks/branches/map/")
        this.mapBranches = res.data

      } catch (e) {
        console.error("Map error:", e)
      } finally {
        this.loading.map = false
      }
    },

    // ==========================================
    // 💰 USER ACTIONS
    // ==========================================
    async click(productId) {
      try {
        await api.post("/banks/click/", {
          product_id: productId
        })
      } catch (e) {
        console.error("Click error:", e)
      }
    },

    async apply(productId) {
      try {
        await api.post("/banks/apply/", {
          product_id: productId
        })
      } catch (e) {
        console.error("Apply error:", e)
      }
    },

  }

})