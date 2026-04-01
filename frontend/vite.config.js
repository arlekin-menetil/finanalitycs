import { fileURLToPath, URL } from "node:url"
import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"
import vueDevTools from "vite-plugin-vue-devtools"

export default defineConfig({

  plugins: [
    vue(),
    vueDevTools(),
  ],

  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },

  server: {

    host: true, // 💣 ВАЖНО для Docker и сети
    port: 5173,
    strictPort: true,

    open: true,

    hmr: {
      overlay: false
    },

    proxy: {

      "/api": {

        target: "http://127.0.0.1:8000", // 💣 стабильнее чем localhost

        changeOrigin: true,
        secure: false,

        ws: false, // 💣 websocket не нужен → иногда ломает

        rewrite: (path) => path, // явно оставляем путь

      }

    }

  },

  build: {

    sourcemap: false,
    chunkSizeWarningLimit: 1000

  }

})