import { ref, computed, watch } from "vue"
import { defineStore } from "pinia"

export const useCounterStore = defineStore("counter", () => {

  // ==========================================
  // 📊 STATE (с сохранением)
  // ==========================================
  const clicks = ref(Number(localStorage.getItem("clicks")) || 0)
  const applications = ref(Number(localStorage.getItem("applications")) || 0)
  const views = ref(Number(localStorage.getItem("views")) || 0)

  // ==========================================
  // 💣 COMPUTED
  // ==========================================

  const totalActions = computed(() => {
    return clicks.value + applications.value + views.value
  })

  const conversionRate = computed(() => {
    if (clicks.value === 0) return 0
    return ((applications.value / clicks.value) * 100).toFixed(1)
  })

  // 💣 CTR (новое)
  const clickThroughRate = computed(() => {
    if (views.value === 0) return 0
    return ((clicks.value / views.value) * 100).toFixed(1)
  })

  // ==========================================
  // 🔥 ACTIONS
  // ==========================================

  function trackClick() {
    clicks.value++
  }

  function trackApplication() {
    applications.value++
  }

  function trackView() {
    views.value++
  }

  function reset() {
    clicks.value = 0
    applications.value = 0
    views.value = 0
  }

  // ==========================================
  // 💾 AUTO SAVE
  // ==========================================
  watch(clicks, (v) => localStorage.setItem("clicks", v))
  watch(applications, (v) => localStorage.setItem("applications", v))
  watch(views, (v) => localStorage.setItem("views", v))

  // ==========================================
  // 🚀 RETURN
  // ==========================================

  return {
    clicks,
    applications,
    views,

    totalActions,
    conversionRate,
    clickThroughRate,

    trackClick,
    trackApplication,
    trackView,
    reset
  }
})