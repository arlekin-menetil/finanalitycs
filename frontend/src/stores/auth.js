import { defineStore } from "pinia"
import api from "@/api/axios"

export const useAuthStore = defineStore("auth", {
  state: () => ({
    access: localStorage.getItem("access") || null,
    refresh: localStorage.getItem("refresh") || null,

    user: null,
    profile: null,

    loading: false,
    error: null,

    initialized: false,
  }),

  getters: {
    // ==========================================
    // AUTH
    // ==========================================

    isAuthenticated: (state) => !!state.access,

    // ==========================================
    // PROFILE
    // ==========================================

    isProfileCompleted: (state) => {
      return Boolean(
        state.profile?.is_profile_completed,
      )
    },

    // ==========================================
    // PLATFORM ACCESS
    // ==========================================

    canUsePlatform() {
      return (
        this.isAuthenticated &&
        this.isProfileCompleted
      )
    },
  },

  actions: {
    // ==========================================
    // LOGIN
    // ==========================================

    async login(phone, password) {
      try {
        this.loading = true
        this.error = null

        const { data } = await api.post(
          "/auth/login/",
          {
            phone,
            password,
          },
        )

        this.setTokens(data)

        await this.loadUser()

        return true
      } catch (err) {
        this.error =
          err.response?.data ||
          "Login failed"

        throw err
      } finally {
        this.loading = false
      }
    },

    // ==========================================
    // TOKENS
    // ==========================================

    setTokens(data) {
      this.access = data.access
      this.refresh = data.refresh

      localStorage.setItem(
        "access",
        data.access,
      )

      localStorage.setItem(
        "refresh",
        data.refresh,
      )

      api.defaults.headers.common.Authorization =
        `Bearer ${data.access}`
    },

    // ==========================================
    // USER
    // ==========================================

    async loadUser() {
      const { data } = await api.get(
        "/auth/me/",
      )

      this.user = data

      await this.fetchProfile()

      return data
    },

    // ==========================================
    // PROFILE
    // ==========================================

    async fetchProfile() {
      try {
        const { data } = await api.get(
          "/profile/",
        )

        this.profile = data

        return data
      } catch (e) {
        this.profile = null

        return null
      }
    },

    // ==========================================
    // PROFILE SETUP
    // ==========================================

    async setupProfile(payload) {
      this.loading = true

      try {
        const { data } = await api.post(
          "/profile/setup/",
          payload,
        )

        await this.fetchProfile()

        return data
      } finally {
        this.loading = false
      }
    },

    // ==========================================
    // REFRESH PROFILE
    // ==========================================

    async refreshProfile() {
      return await this.fetchProfile()
    },

    // ==========================================
    // LOGOUT
    // ==========================================

    logout() {
      this.access = null
      this.refresh = null
      this.user = null
      this.profile = null

      this.loading = false
      this.error = null

      localStorage.removeItem("access")
      localStorage.removeItem("refresh")

      delete api.defaults.headers.common.Authorization
    },

    // ==========================================
    // INIT
    // ==========================================

    async init() {
      try {
        const access =
          localStorage.getItem("access")

        if (!access) {
          this.initialized = true
          return
        }

        this.access = access

        api.defaults.headers.common.Authorization =
          `Bearer ${access}`

        await this.loadUser()
      } catch (e) {
        console.error(
          "Auth init:",
          e,
        )

        this.logout()
      } finally {
        this.initialized = true
      }
    },
  },
})