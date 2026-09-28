import { createApp } from "vue"
import { createPinia } from "pinia"

import App from "./App.vue"
import router from "./router"
import i18n from "./i18n"

import "leaflet/dist/leaflet.css"

import { useAuthStore } from "@/stores/auth"

function bootstrap() {
  const app = createApp(App)
  const pinia = createPinia()

  app.use(pinia)
  app.use(router)
  app.use(i18n)

  const auth = useAuthStore()

  app.mount("#app")

  auth.init().catch((e) => {
    console.error("Auth init error:", e)
  })
}

bootstrap()