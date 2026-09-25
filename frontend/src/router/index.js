import { createRouter, createWebHistory } from "vue-router"
import { useAuthStore } from "@/stores/auth"

// ==========================
// AUTH
// ==========================
import AuthPhone from "@/views/AuthPhone.vue"

// ==========================
// LANDING
// ==========================
import LandingView from "@/views/LandingView.vue"

// ==========================
// LAYOUT
// ==========================
import MainLayout from "@/layouts/MainLayout.vue"

// ==========================
// Lazy Views
// ==========================
const DashboardView = () => import("@/views/DashboardView.vue")
const ScoringView = () => import("@/views/ScoringView.vue")
const RecommendationsView = () => import("@/views/RecommendationsView.vue")
const AnalyticsView = () => import("@/views/AnalyticsView.vue")
const MonitoringView = () => import("@/views/MonitoringView.vue")

// 👤
const ProfileView = () => import("@/views/ProfileView.vue")
const ProfileSetupView = () => import("@/views/ProfileSetupView.vue")

// 💰
const LoanView = () => import("@/views/LoanView.vue")
const LoanDetailView = () => import("@/views/ProductDetailView.vue")

// 🏦
const DepositsView = () => import("@/views/DepositsView.vue")
const DepositDetailView = () => import("@/views/DepositDetailView.vue")

// 💳
const CardsView = () => import("@/views/CardsView.vue")
const CardDetailView = () => import("@/views/CardDetailView.vue")

// 🏛
const BankBranchesView = () => import("@/views/BankBranchesView.vue")

// =====================================
// ROUTES
// =====================================

const routes = [

  {
    path: "/",
    name: "Landing",
    component: LandingView,
  },

  {
    path: "/login",
    name: "Login",
    component: AuthPhone,
  },

  {
    path: "/app",

    component: MainLayout,

    meta: {
      requiresAuth: true,
    },

    children: [

      {
        path: "",
        redirect: "/app/profile",
      },

      {
        path: "dashboard",
        name: "Dashboard",
        component: DashboardView,
        meta: {
          title: "Dashboard",
        },
      },

      {
        path: "profile",
        name: "Profile",
        component: ProfileView,
        meta: {
          title: "Profile",
        },
      },

      {
        path: "profile/edit",
        name: "ProfileEdit",
        component: ProfileSetupView,
        meta: {
          title: "Profile Edit",
        },
      },

      {
        path: "scoring",
        name: "Scoring",
        component: ScoringView,
        meta: {
          title: "Scoring",
        },
      },

      {
        path: "recommendations",
        name: "Recommendations",
        component: RecommendationsView,
        meta: {
          title: "Recommendations",
        },
      },

      {
        path: "analytics",
        name: "Analytics",
        component: AnalyticsView,
        meta: {
          title: "Analytics",
        },
      },

      {
        path: "monitoring",
        name: "Monitoring",
        component: MonitoringView,
        meta: {
          title: "Monitoring",
        },
      },

      // =======================
      // LOANS
      // =======================

      {
        path: "loans",
        name: "Loans",
        component: LoanView,
        meta: {
          title: "Loans",
        },
      },

      {
        path: "loan/:id",
        name: "LoanDetail",
        component: LoanDetailView,
        meta: {
          title: "Loan Detail",
        },
      },

      // =======================
      // DEPOSITS
      // =======================

      {
        path: "deposits",
        name: "Deposits",
        component: DepositsView,
        meta: {
          title: "Deposits",
        },
      },

      {
        path: "deposit/:id",
        name: "DepositDetail",
        component: DepositDetailView,
        meta: {
          title: "Deposit Detail",
        },
      },

      // =======================
      // CARDS
      // =======================

      {
        path: "cards",
        name: "Cards",
        component: CardsView,
        meta: {
          title: "Cards",
        },
      },

      {
        path: "card/:id",
        name: "CardDetail",
        component: CardDetailView,
        meta: {
          title: "Card Detail",
        },
      },

      // =======================
      // BANK
      // =======================

      {
        path: "bank/:id/branches",
        name: "BankBranches",
        component: BankBranchesView,
        meta: {
          title: "Bank Branches",
        },
      },

    ],

  },

  {
    path: "/:pathMatch(.*)*",
    redirect: "/",
  },

]

// =====================================
// ROUTER
// =====================================

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// =====================================
// AUTH GUARD
// =====================================

router.beforeEach((to) => {

  const auth = useAuthStore()

  // =====================================
  // WAIT INIT
  // =====================================

  if (!auth.initialized) {

    return true

  }

  // =====================================
  // NOT AUTHORIZED
  // =====================================

  if (

    to.meta.requiresAuth &&

    !auth.isAuthenticated

  ) {

    return "/login"

  }

  // =====================================
  // ALREADY LOGIN
  // =====================================

  if (

    to.path === "/login" &&

    auth.isAuthenticated

  ) {

    return auth.isProfileCompleted

      ? "/app/dashboard"

      : "/app/profile"

  }

  // =====================================
  // PROFILE LOCK
  // =====================================

  if (

    auth.isAuthenticated &&

    !auth.isProfileCompleted

  ) {

    const allowedRoutes = new Set([

      "/app/profile",

      "/app/profile/edit",

    ])

    if (

      !allowedRoutes.has(to.path)

    ) {

      return "/app/profile"

    }

  }

  // =====================================
  // ACCESS GRANTED
  // =====================================

  return true

})

// =====================================
// TITLE
// =====================================

router.afterEach((to) => {

  document.title =

    to.meta?.title

      ? `${to.meta.title} | Bank Analytics`

      : "Bank Analytics"

})

export default router