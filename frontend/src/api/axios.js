import axios from "axios"

// ==========================================
// API CONFIG
// ==========================================

const API_URL =
  import.meta.env.VITE_API_URL || "/api"

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
})

// ==========================================
// REQUEST INTERCEPTOR
// ==========================================

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access")

    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// ==========================================
// TOKEN REFRESH
// ==========================================

let isRefreshing = false
let failedQueue = []

function processQueue(error, token = null) {
  failedQueue.forEach(
    ({ resolve, reject }) => {
      if (error) {
        reject(error)
      } else {
        resolve(token)
      }
    },
  )

  failedQueue = []
}

// ==========================================
// RESPONSE INTERCEPTOR
// ==========================================

api.interceptors.response.use(
  (response) => {
    return response
  },

  async (error) => {
    const originalRequest = error.config

    // ========================================
    // NETWORK ERROR
    // ========================================

    if (!error.response) {
      console.error(
        "Network error:",
        error.message,
      )

      return Promise.reject(error)
    }

    const status = error.response.status

    // ========================================
    // NOT 401
    // ========================================

    if (status !== 401) {
      console.error(
        `${status} ${originalRequest?.url}`,
        error,
      )

      return Promise.reject(error)
    }

    // ========================================
    // PREVENT INFINITE RETRY
    // ========================================

    if (originalRequest?._retry) {
      forceLogout()

      return Promise.reject(error)
    }

    // ========================================
    // LOGIN REQUEST
    // ========================================

    if (
      originalRequest?.url?.includes(
        "/auth/login",
      )
    ) {
      return Promise.reject(error)
    }

    // ========================================
    // REFRESH TOKEN
    // ========================================

    const refresh =
      localStorage.getItem("refresh")

    if (!refresh) {
      forceLogout()

      return Promise.reject(error)
    }

    // ========================================
    // WAIT FOR EXISTING REFRESH
    // ========================================

    if (isRefreshing) {
      return new Promise(
        (resolve, reject) => {
          failedQueue.push({
            resolve,
            reject,
          })
        },
      )
        .then((token) => {
          originalRequest.headers.Authorization =
            `Bearer ${token}`

          return api(originalRequest)
        })
        .catch((err) => {
          return Promise.reject(err)
        })
    }

    // ========================================
    // START TOKEN REFRESH
    // ========================================

    originalRequest._retry = true
    isRefreshing = true

    try {
      const refreshResponse =
        await axios.post(
          `${API_URL}/token/refresh/`,
          {
            refresh,
          },
        )

      const newAccess =
        refreshResponse.data.access

      // Save new access token
      localStorage.setItem(
        "access",
        newAccess,
      )

      // Update default Authorization
      api.defaults.headers.common.Authorization =
        `Bearer ${newAccess}`

      // Update original request
      originalRequest.headers.Authorization =
        `Bearer ${newAccess}`

      // Resolve queued requests
      processQueue(
        null,
        newAccess,
      )

      // Retry original request
      return api(originalRequest)
    } catch (refreshError) {
      processQueue(refreshError)

      forceLogout()

      return Promise.reject(
        refreshError,
      )
    } finally {
      isRefreshing = false
    }
  },
)

// ==========================================
// FORCE LOGOUT
// ==========================================

function forceLogout() {
  localStorage.removeItem("access")
  localStorage.removeItem("refresh")

  delete api.defaults.headers.common.Authorization

  window.location.href = "/login"
}

// ==========================================
// EXPORT
// ==========================================

export default api