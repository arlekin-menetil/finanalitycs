import axios from "axios"

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api", // 💣 ВАЖНО
})


// ==========================================
// 🧠 REQUEST INTERCEPTOR
// ==========================================
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access")

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})


// ==========================================
// 💣 REFRESH LOGIC
// ==========================================
let isRefreshing = false
let failedQueue = []

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })

  failedQueue = []
}


// ==========================================
// 🧠 RESPONSE INTERCEPTOR
// ==========================================
api.interceptors.response.use(
  (response) => response,
  async (error) => {

    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {

      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        })
        .then(token => {
          originalRequest.headers.Authorization = 'Bearer ' + token
          return api(originalRequest)
        })
        .catch(err => Promise.reject(err))
      }

      originalRequest._retry = true
      isRefreshing = true

      const refreshToken = localStorage.getItem("refresh")

      if (!refreshToken) {
        logout()
        return Promise.reject(error)
      }

      try {
        const res = await axios.post(
          "http://127.0.0.1:8000/api/token/refresh/", // 💣 тоже фикс
          { refresh: refreshToken }
        )

        const newAccess = res.data.access

        localStorage.setItem("access", newAccess)

        api.defaults.headers.Authorization = `Bearer ${newAccess}`
        originalRequest.headers.Authorization = `Bearer ${newAccess}`

        processQueue(null, newAccess)

        return api(originalRequest)

      } catch (err) {
        processQueue(err, null)
        logout()
        return Promise.reject(err)

      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error)
  }
)


// ==========================================
// 💣 LOGOUT
// ==========================================
function logout() {
  localStorage.removeItem("access")
  localStorage.removeItem("refresh")

  window.location.href = "/login"
}

export default api