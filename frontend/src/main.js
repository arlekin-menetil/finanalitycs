import { createApp } from "vue"
import { createPinia } from "pinia"

import App from "./App.vue"
import router from "./router"
import i18n from "./i18n"

// 🗺 Leaflet styles
import "leaflet/dist/leaflet.css"

// 💣 STORE
import { useAuthStore } from "@/stores/auth"

async function bootstrap() {

  const app = createApp(App)
  const pinia = createPinia()

  app.use(pinia)

  // 🔥 ИНИЦИАЛИЗАЦИЯ AUTH ДО ROUTER
  const auth = useAuthStore()

  try {
    await auth.init()
  } catch (e) {
    console.error("Auth init error:", e)
  }

  // 🔥 теперь подключаем router
  app.use(router)

  // 🔥 i18n
  app.use(i18n)

  // 🚀 mount
  app.mount("#app")
}

bootstrap()