import { createRouter, createWebHistory } from "vue-router"
import { useAuthStore } from "@/stores/auth"

// 🔐 SMS авторизация
import AuthPhone from "@/views/AuthPhone.vue"

// 🌍 LANDING
import LandingView from "@/views/LandingView.vue"

// 💣 Layout
import MainLayout from "@/layouts/MainLayout.vue"

// Lazy views
const DashboardView = () => import("@/views/DashboardView.vue")
const ScoringView = () => import("@/views/ScoringView.vue")
const RecommendationsView = () => import("@/views/RecommendationsView.vue")
const AnalyticsView = () => import("@/views/AnalyticsView.vue")
const MonitoringView = () => import("@/views/MonitoringView.vue")
const ProfileSetupView = () => import("@/views/ProfileSetupView.vue")
const LoanView = () => import("@/views/LoanView.vue")
const BankBranchesView = () => import("@/views/BankBranchesView.vue")

const routes = [

  // 🌍 LANDING (главная)
  {
    path: "/",
    component: LandingView,
    meta: { title: "FinAnalytics" }
  },

  // 🔐 LOGIN
  {
    path: "/login",
    component: AuthPhone,
    meta: { title: "Login" }
  },

  // 💣 ПРИЛОЖЕНИЕ
  {
    path: "/app",
    component: MainLayout,
    meta: { requiresAuth: true },

    children: [

      {
        path: "",
        component: DashboardView,
        meta: { title: "Dashboard" }
      },

      {
        path: "scoring",
        component: ScoringView
      },

      {
        path: "recommendations",
        component: RecommendationsView
      },

      {
        path: "analytics",
        component: AnalyticsView
      },

      {
        path: "monitoring",
        component: MonitoringView
      },

      {
        path: "profile-setup",
        component: ProfileSetupView
      },

      {
        path: "loan/:id",
        component: LoanView
      },

      {
        path: "bank/:id/branches",
        component: BankBranchesView
      }

    ]
  }

]

const router = createRouter({
  history: createWebHistory(),
  routes,
})


// ==========================================
// 💣 GLOBAL GUARD
// ==========================================
router.beforeEach((to) => {

  const auth = useAuthStore()

  // 🔐 если требует авторизацию
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return "/login"
  }

  // 🔥 если уже залогинен → не пускаем на login
  if (to.path === "/login" && auth.isAuthenticated) {
    return "/app"
  }

  // 💣 если нет профиля → отправляем на setup
  if (
    auth.isAuthenticated &&
    !auth.isProfileCompleted &&
    !to.path.startsWith("/app/profile-setup")
  ) {
    return "/app/profile-setup"
  }

  // 🔥 если профиль есть → не пускаем обратно
  if (
    to.path === "/app/profile-setup" &&
    auth.isProfileCompleted
  ) {
    return "/app"
  }

})

export default router