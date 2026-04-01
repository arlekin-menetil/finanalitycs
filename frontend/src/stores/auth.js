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
    isAuthenticated: (state) => !!state.access,

    isProfileCompleted: (state) => {
      return state.profile?.is_profile_completed || false
    },
  },

  actions: {

    // ==========================================
    // 🔐 LOGIN
    // ==========================================
    async login(phone, password) {
      try {
        this.loading = true
        this.error = null

        const response = await api.post("/auth/login/", {
          phone,
          password,
        })

        this.access = response.data.access
        this.refresh = response.data.refresh

        localStorage.setItem("access", this.access)
        localStorage.setItem("refresh", this.refresh)

        // 💣 ставим токен
        api.defaults.headers.common["Authorization"] = `Bearer ${this.access}`

        await this.fetchUser()

        return true

      } catch (err) {
        this.error = err.response?.data || "Login failed"
        throw err
      } finally {
        this.loading = false
      }
    },


    // ==========================================
    // 👤 USER
    // ==========================================
    async fetchUser() {
      try {
        const res = await api.get("/auth/me/")
        this.user = res.data

        await this.fetchProfile()

      } catch (e) {
        console.error("User fetch error", e)

        // 💣 если токен умер → logout
        if (e.response?.status === 401) {
          this.logout()
        }
      }
    },


    // ==========================================
    // 💣 PROFILE
    // ==========================================
    async fetchProfile() {
      try {
        const res = await api.get("/profile/")
        this.profile = res.data
      } catch (e) {
        console.error("Profile fetch error", e)
        this.profile = null
      }
    },


    // ==========================================
    // 💣 PROFILE SETUP
    // ==========================================
    async setupProfile(data) {
      try {
        this.loading = true

        const res = await api.post("/profile/setup/", data)

        // 💣 обновляем профиль после сохранения
        await this.fetchProfile()

        return res.data

      } catch (e) {
        console.error("Profile setup error", e)
        throw e
      } finally {
        this.loading = false
      }
    },


    // ==========================================
    // 🔄 REFRESH TOKEN (НОВОЕ 💣)
    // ==========================================
    async refreshToken() {
      try {
        const res = await api.post("/token/refresh/", {
          refresh: this.refresh,
        })

        this.access = res.data.access
        localStorage.setItem("access", this.access)

        api.defaults.headers.common["Authorization"] = `Bearer ${this.access}`

        return true

      } catch (e) {
        console.error("Refresh token failed", e)
        this.logout()
        return false
      }
    },


    // ==========================================
    // 🚪 LOGOUT
    // ==========================================
    logout() {
      this.access = null
      this.refresh = null
      this.user = null
      this.profile = null
      this.error = null

      localStorage.removeItem("access")
      localStorage.removeItem("refresh")

      delete api.defaults.headers.common["Authorization"]

      window.location.href = "/login"
    },


    // ==========================================
    // 🔄 INIT
    // ==========================================
    async init() {
      try {
        if (this.access) {
          api.defaults.headers.common["Authorization"] = `Bearer ${this.access}`

          try {
            await this.fetchUser()
          } catch (e) {
            // 💣 если access умер → пробуем refresh
            const ok = await this.refreshToken()

            if (ok) {
              await this.fetchUser()
            }
          }
        }
      } finally {
        this.initialized = true
      }
    },
  },
})