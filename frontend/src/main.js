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

  // 💣 ИНИЦИАЛИЗАЦИЯ AUTH ДО ROUTER
  const auth = useAuthStore()
  await auth.init()

  app.use(router)
  app.use(i18n)

  app.mount("#app")
}

bootstrap()