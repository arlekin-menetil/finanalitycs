import { createRouter, createWebHistory } from "vue-router"
import { useAuthStore } from "@/stores/auth"

// =========================
// 🔐 Views
// =========================
import LoginView from "@/views/LoginView.vue"

const DashboardView = () => import("@/views/DashboardView.vue")
const ScoringView = () => import("@/views/ScoringView.vue")
const RecommendationsView = () => import("@/views/RecommendationsView.vue")
const AnalyticsView = () => import("@/views/AnalyticsView.vue")
const MonitoringView = () => import("@/views/MonitoringView.vue")
const ProfileSetupView = () => import("@/views/ProfileSetupView.vue")

const LoanView = () => import("@/views/LoanView.vue")
const BankBranchesView = () => import("@/views/BankBranchesView.vue")

// =========================
// 🚀 ROUTES
// =========================
const routes = [
  {
    path: "/login",
    component: LoginView,
    meta: { title: "Login" },
  },

  {
    path: "/profile-setup",
    component: ProfileSetupView,
    meta: {
      requiresAuth: true,
      title: "Profile Setup",
    },
  },

  {
    path: "/",
    component: DashboardView,
    meta: {
      requiresAuth: true,
      title: "Dashboard",
    },
  },

  {
    path: "/scoring",
    component: ScoringView,
    meta: {
      requiresAuth: true,
      title: "Scoring",
    },
  },

  {
    path: "/recommendations",
    component: RecommendationsView,
    meta: {
      requiresAuth: true,
      title: "Recommendations",
    },
  },

  {
    path: "/analytics",
    component: AnalyticsView,
    meta: {
      requiresAuth: true,
      title: "Analytics",
    },
  },

  {
    path: "/monitoring",
    component: MonitoringView,
    meta: {
      requiresAuth: true,
      title: "Monitoring",
    },
  },

  {
    path: "/loan/:id",
    component: LoanView,
    meta: {
      requiresAuth: true,
      title: "Loan",
    },
  },

  {
    path: "/bank/:id/branches",
    component: BankBranchesView,
    meta: {
      requiresAuth: true,
      title: "Bank branches",
    },
  },

  // 💣 fallback (очень важно)
  {
    path: "/:pathMatch(.*)*",
    redirect: "/",
  },
]

// =========================
// ⚙️ ROUTER
// =========================
const router = createRouter({
  history: createWebHistory(),
  routes,
})


// ==========================================
// 💣 GLOBAL GUARD (ПРОДУКТОВАЯ ЛОГИКА)
// ==========================================
router.beforeEach((to) => {
  const auth = useAuthStore()

  const isAuth = auth.isAuthenticated
  const isProfileDone = auth.isProfileCompleted

  // 🔐 1. НЕ АВТОРИЗОВАН → LOGIN
  if (to.meta.requiresAuth && !isAuth) {
    return "/login"
  }

  // 🔥 2. УЖЕ ЗАЛОГИНЕН → НЕ ПУСКАЕМ В LOGIN
  if (to.path === "/login" && isAuth) {
    return isProfileDone ? "/" : "/profile-setup"
  }

  // 💣 3. НЕТ ПРОФИЛЯ → ВСЕГДА В PROFILE SETUP
  if (isAuth && !isProfileDone && to.path !== "/profile-setup") {
    return "/profile-setup"
  }

  // 🔥 4. ПРОФИЛЬ ЕСТЬ → НЕ ПУСКАЕМ ОБРАТНО
  if (to.path === "/profile-setup" && isProfileDone) {
    return "/"
  }

  return true
})

export default router