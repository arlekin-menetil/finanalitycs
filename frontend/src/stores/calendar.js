import { defineStore } from "pinia"
import api from "@/api/axios"

export const useCalendarStore = defineStore("calendar", {

  state: () => ({
    events: [],
    loading: false,
    error: null
  }),

  actions: {

    async loadEvents() {
      try {

        this.loading = true
        this.error = null

        const res = await api.get("/calendar/")
        this.events = res.data

      } catch (e) {

        console.error("Calendar load error:", e)
        this.error = e

      } finally {
        this.loading = false
      }
    }

  }

})