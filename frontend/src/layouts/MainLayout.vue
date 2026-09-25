<script setup>
import {
  computed,
  onMounted,
} from "vue"

import {
  useRoute,
  useRouter,
} from "vue-router"

import {
  useI18n,
} from "vue-i18n"

import {
  useAuthStore,
} from "@/stores/auth"

const auth = useAuthStore()

const router = useRouter()
const route = useRoute()

const { locale, t } = useI18n()

// ==========================================
// TITLE
// ==========================================

const currentTitle = computed(() => {
  return route.meta?.title || "Dashboard"
})

// ==========================================
// USER NAME
// ==========================================

const displayName = computed(() => {
  if (auth.profile?.full_name) {
    const parts = auth.profile.full_name.split(" ")
    return parts[0]
  }

  if (auth.user?.phone) {
    return auth.user.phone
  }

  return "User"
})

// ==========================================
// USER INITIAL
// ==========================================

const userInitial = computed(() => {
  const name = displayName.value

  if (!name) {
    return "U"
  }

  return name.charAt(0).toUpperCase()
})

// ==========================================
// NAVIGATION
// ==========================================

const navigation = computed(() => [
  {
    label: "Dashboard",
    title: "Dashboard",
    to: "/app/dashboard",
    icon: "dashboard",
  },
  {
    label: "Scoring",
    title: "Scoring",
    to: "/app/scoring",
    icon: "scoring",
  },
  {
    label: "Recommendations",
    title: "Recommendations",
    to: "/app/recommendations",
    icon: "recommendations",
  },
  {
    label: "Analytics",
    title: "Analytics",
    to: "/app/analytics",
    icon: "analytics",
  },
  {
    label: "Monitoring",
    title: "Monitoring",
    to: "/app/monitoring",
    icon: "monitoring",
  },
  {
    label: "Deposits",
    title: "Deposits",
    to: "/app/deposits",
    icon: "deposits",
  },
  {
    label: "Cards",
    title: "Cards",
    to: "/app/cards",
    icon: "cards",
  },
])

// ==========================================
// INIT
// ==========================================

onMounted(async () => {
  const lang = localStorage.getItem("lang")

  if (lang) {
    locale.value = lang
  }

  try {
    if (!auth.user) {
      await auth.loadUser()
    }

    if (!auth.profile) {
      await auth.fetchProfile()
    }
  } catch (e) {
    console.error("Ошибка загрузки пользователя:", e)
  }
})

// ==========================================
// LANGUAGE
// ==========================================

const changeLang = () => {
  localStorage.setItem(
    "lang",
    locale.value
  )
}

// ==========================================
// LOGOUT
// ==========================================

const logout = () => {
  auth.logout()

  router.push("/login")
}

// ==========================================
// PROFILE
// ==========================================

const goToProfile = () => {
  router.push("/app/profile")
}

// ==========================================
// HOME
// ==========================================

const goHome = () => {
  router.push("/app/dashboard")
}
</script>

<template>
  <div class="dashboard-layout">

    <!-- ======================================
         SIDEBAR
    ======================================= -->

    <aside class="sidebar">

      <!-- LOGO -->

      <div
        class="brand"
        @click="goHome"
      >

        <div class="brand-logo">

          <img
            src="/logo.png"
            alt="FinAnalytics"
          />

        </div>

        <div class="brand-info">

          <div class="brand-title">
            FinAnalytics
          </div>

          <div class="brand-subtitle">
            Financial Intelligence
          </div>

        </div>

      </div>


      <!-- NAVIGATION -->

      <nav class="navigation">

        <div class="navigation-label">
          PLATFORM
        </div>

        <router-link
          v-for="item in navigation"
          :key="item.to"
          :to="item.to"
          class="nav-item"
        >

          <!-- DASHBOARD -->

          <span
            v-if="item.icon === 'dashboard'"
            class="nav-icon"
          >
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <rect
                x="3"
                y="3"
                width="7"
                height="7"
                rx="1"
              />
              <rect
                x="14"
                y="3"
                width="7"
                height="7"
                rx="1"
              />
              <rect
                x="3"
                y="14"
                width="7"
                height="7"
                rx="1"
              />
              <rect
                x="14"
                y="14"
                width="7"
                height="7"
                rx="1"
              />
            </svg>
          </span>


          <!-- SCORING -->

          <span
            v-else-if="item.icon === 'scoring'"
            class="nav-icon"
          >
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <circle
                cx="12"
                cy="12"
                r="9"
              />
              <path d="M12 7v5l3 2" />
              <path d="M8 4.5l-1.5-1" />
              <path d="M16 4.5l1.5-1" />
            </svg>
          </span>


          <!-- RECOMMENDATIONS -->

          <span
            v-else-if="item.icon === 'recommendations'"
            class="nav-icon"
          >
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path
                d="M12 3l2.8 5.7L21 9.6l-4.5 4.4 1.1 6.2L12 17.3 6.4 20.2l1.1-6.2L3 9.6l6.2-.9L12 3z"
              />
            </svg>
          </span>


          <!-- ANALYTICS -->

          <span
            v-else-if="item.icon === 'analytics'"
            class="nav-icon"
          >
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M4 19V5" />
              <path d="M4 19h16" />
              <path d="M8 16v-5" />
              <path d="M12 16V8" />
              <path d="M16 16v-9" />
              <path d="M20 16v-4" />
            </svg>
          </span>


          <!-- MONITORING -->

          <span
            v-else-if="item.icon === 'monitoring'"
            class="nav-icon"
          >
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <polyline points="3 12 7 12 10 4 14 20 17 12 21 12" />
            </svg>
          </span>


          <!-- DEPOSITS -->

          <span
            v-else-if="item.icon === 'deposits'"
            class="nav-icon"
          >
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <rect
                x="3"
                y="5"
                width="18"
                height="14"
                rx="2"
              />
              <path d="M7 9h10" />
              <path d="M7 13h5" />
              <circle
                cx="17"
                cy="14"
                r="1"
              />
            </svg>
          </span>


          <!-- CARDS -->

          <span
            v-else
            class="nav-icon"
          >
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <rect
                x="2.5"
                y="5"
                width="19"
                height="14"
                rx="2"
              />
              <path d="M2.5 10h19" />
              <path d="M6 15h4" />
            </svg>
          </span>


          <span class="nav-text">
            {{ item.label }}
          </span>

        </router-link>

      </nav>


      <!-- SIDEBAR BOTTOM -->

      <div class="sidebar-bottom">

        <div class="sidebar-status">

          <span class="status-dot"></span>

          <span>
            System online
          </span>

        </div>

        <div class="sidebar-version">
          FinAnalytics v1.0
        </div>

      </div>

    </aside>


    <!-- ======================================
         MAIN
    ======================================= -->

    <div class="main">

      <!-- ====================================
           TOPBAR
      ===================================== -->

      <header class="topbar">

        <div class="topbar-left">

          <div class="breadcrumb">

            <span class="breadcrumb-muted">
              FinAnalytics
            </span>

            <span class="breadcrumb-separator">
              /
            </span>

            <span class="breadcrumb-current">
              {{ currentTitle }}
            </span>

          </div>

        </div>


        <div class="topbar-right">

          <!-- PROFILE WARNING -->

          <button
            v-if="!auth.isProfileCompleted"
            class="profile-warning"
            type="button"
            @click="goToProfile"
          >

            <span class="warning-icon">
              !
            </span>

            <span>
              Заполните профиль
            </span>

          </button>


          <!-- LANGUAGE -->

          <div class="language-wrapper">

            <svg
              class="language-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <circle
                cx="12"
                cy="12"
                r="9"
              />

              <path d="M3 12h18" />

              <path
                d="M12 3c2.5 2.5 3.8 5.5 3.8 9S14.5 18.5 12 21"
              />

              <path
                d="M12 3C9.5 5.5 8.2 8.5 8.2 12S9.5 18.5 12 21"
              />
            </svg>

            <select
              v-model="locale"
              class="lang-select"
              @change="changeLang"
            >
              <option value="ru">
                RU
              </option>

              <option value="en">
                EN
              </option>

              <option value="uz">
                UZ
              </option>
            </select>

          </div>


          <!-- PROFILE -->

          <button
            class="profile-button"
            type="button"
            @click="goToProfile"
          >

            <span class="avatar">
              {{ userInitial }}
            </span>

            <span class="profile-info">

              <span class="profile-name">
                {{ displayName }}
              </span>

              <span class="profile-label">
                Personal account
              </span>

            </span>

            <span class="profile-arrow">
              ›
            </span>

          </button>


          <!-- LOGOUT -->

          <button
            class="logout-button"
            type="button"
            title="Logout"
            @click="logout"
          >

            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M10 17l5-5-5-5" />
              <path d="M15 12H3" />
              <path d="M21 19V5a2 2 0 0 0-2-2h-6" />
            </svg>

          </button>

        </div>

      </header>


      <!-- ====================================
           CONTENT
      ===================================== -->

      <main class="content">

        <router-view />

      </main>

    </div>

  </div>
</template>

<style scoped>

/* ==========================================
   GLOBAL LAYOUT
========================================== */

.dashboard-layout {
  display: flex;

  width: 100%;
  height: 100vh;

  overflow: hidden;

  background: #f5f7fb;

  color: #0f172a;

  font-family:
    Inter,
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    sans-serif;
}


/* ==========================================
   SIDEBAR
========================================== */

.sidebar {
  width: 258px;

  flex-shrink: 0;

  display: flex;
  flex-direction: column;

  padding: 25px 16px 18px;

  box-sizing: border-box;

  background:
    linear-gradient(
      180deg,
      #0b1220 0%,
      #0f172a 55%,
      #111827 100%
    );

  color: #ffffff;

  border-right: 1px solid rgba(255, 255, 255, 0.04);

  box-shadow:
    8px 0 30px rgba(15, 23, 42, 0.08);

  z-index: 20;
}


/* ==========================================
   BRAND
========================================== */

.brand {
  display: flex;
  align-items: center;

  gap: 12px;

  padding: 4px 9px;

  margin-bottom: 38px;

  cursor: pointer;

  user-select: none;
}

.brand-logo {
  width: 43px;
  height: 43px;

  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  overflow: hidden;

  border-radius: 13px;

  background: #ffffff;

  box-shadow:
    0 7px 18px rgba(37, 99, 235, 0.18);
}

.brand-logo img {
  width: 100%;
  height: 100%;

  object-fit: contain;
}

.brand-info {
  min-width: 0;
}

.brand-title {
  color: #ffffff;

  font-size: 17px;
  font-weight: 800;

  line-height: 1.1;

  letter-spacing: -0.35px;
}

.brand-subtitle {
  margin-top: 4px;

  color: #94a3b8;

  font-size: 9px;
  font-weight: 600;

  text-transform: uppercase;

  letter-spacing: 0.65px;

  white-space: nowrap;
}


/* ==========================================
   NAVIGATION
========================================== */

.navigation {
  display: flex;
  flex-direction: column;

  gap: 5px;
}

.navigation-label {
  padding: 0 12px;

  margin-bottom: 8px;

  color: #64748b;

  font-size: 9px;
  font-weight: 800;

  letter-spacing: 1.2px;
}


/* ==========================================
   NAV ITEM
========================================== */

.nav-item {
  position: relative;

  display: flex;
  align-items: center;

  min-height: 47px;

  padding: 0 13px;

  box-sizing: border-box;

  border-radius: 12px;

  color: #94a3b8;

  text-decoration: none;

  transition:
    background 0.2s ease,
    color 0.2s ease,
    transform 0.2s ease;
}

.nav-item:hover {
  color: #ffffff;

  background:
    rgba(255, 255, 255, 0.055);

  transform: translateX(2px);
}

.nav-item.router-link-active {
  color: #ffffff;

  background:
    linear-gradient(
      135deg,
      rgba(37, 99, 235, 0.95),
      rgba(37, 99, 235, 0.72)
    );

  box-shadow:
    0 8px 20px rgba(37, 99, 235, 0.20);
}

.nav-item.router-link-active::before {
  content: "";

  position: absolute;

  left: -16px;

  width: 3px;
  height: 24px;

  border-radius: 0 4px 4px 0;

  background: #38bdf8;
}

.nav-icon {
  width: 21px;
  height: 21px;

  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  margin-right: 12px;
}

.nav-icon svg {
  width: 19px;
  height: 19px;
}

.nav-text {
  font-size: 13px;
  font-weight: 600;

  letter-spacing: -0.05px;
}


/* ==========================================
   SIDEBAR BOTTOM
========================================== */

.sidebar-bottom {
  margin-top: auto;

  padding: 15px 10px 4px;

  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.sidebar-status {
  display: flex;
  align-items: center;
  gap: 7px;

  color: #94a3b8;

  font-size: 10px;
  font-weight: 600;
}

.status-dot {
  width: 7px;
  height: 7px;

  border-radius: 50%;

  background: #22c55e;

  box-shadow:
    0 0 0 4px rgba(34, 197, 94, 0.08);
}

.sidebar-version {
  margin-top: 8px;

  color: #475569;

  font-size: 9px;
}


/* ==========================================
   MAIN
========================================== */

.main {
  min-width: 0;

  flex: 1;

  display: flex;
  flex-direction: column;

  overflow: hidden;
}


/* ==========================================
   TOPBAR
========================================== */

.topbar {
  min-height: 76px;

  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: space-between;

  gap: 20px;

  padding: 0 28px;

  box-sizing: border-box;

  background:
    rgba(255, 255, 255, 0.96);

  border-bottom: 1px solid #e8edf4;

  box-shadow:
    0 2px 15px rgba(15, 23, 42, 0.035);

  z-index: 10;
}


/* ==========================================
   BREADCRUMB
========================================== */

.breadcrumb {
  display: flex;
  align-items: center;

  gap: 9px;

  font-size: 13px;
}

.breadcrumb-muted {
  color: #94a3b8;

  font-weight: 500;
}

.breadcrumb-separator {
  color: #cbd5e1;
}

.breadcrumb-current {
  color: #0f172a;

  font-weight: 750;
}


/* ==========================================
   TOPBAR RIGHT
========================================== */

.topbar-right {
  display: flex;
  align-items: center;

  gap: 10px;

  min-width: 0;
}


/* ==========================================
   PROFILE WARNING
========================================== */

.profile-warning {
  display: flex;
  align-items: center;

  gap: 7px;

  height: 36px;

  padding: 0 12px;

  border: 1px solid #fde68a;

  border-radius: 10px;

  color: #92400e;

  background: #fffbeb;

  font-size: 11px;
  font-weight: 700;

  cursor: pointer;

  transition:
    background 0.2s ease,
    border-color 0.2s ease;
}

.profile-warning:hover {
  background: #fef3c7;

  border-color: #fcd34d;
}

.warning-icon {
  width: 17px;
  height: 17px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 50%;

  color: #ffffff;

  background: #f59e0b;

  font-size: 10px;
  font-weight: 800;
}


/* ==========================================
   LANGUAGE
========================================== */

.language-wrapper {
  height: 38px;

  display: flex;
  align-items: center;

  gap: 5px;

  padding: 0 9px;

  border: 1px solid #e2e8f0;

  border-radius: 10px;

  background: #ffffff;
}

.language-icon {
  width: 16px;
  height: 16px;

  color: #64748b;
}

.lang-select {
  border: none;
  outline: none;

  padding: 0 2px;

  color: #334155;

  background: transparent;

  font-size: 11px;
  font-weight: 750;

  cursor: pointer;
}


/* ==========================================
   PROFILE BUTTON
========================================== */

.profile-button {
  display: flex;
  align-items: center;

  gap: 9px;

  min-width: 0;

  padding: 5px 8px 5px 5px;

  border: 1px solid transparent;

  border-radius: 12px;

  background: transparent;

  cursor: pointer;

  transition:
    background 0.2s ease,
    border-color 0.2s ease;
}

.profile-button:hover {
  background: #f8fafc;

  border-color: #e2e8f0;
}

.avatar {
  width: 36px;
  height: 36px;

  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 11px;

  color: #ffffff;

  background:
    linear-gradient(
      135deg,
      #2563eb,
      #06b6d4
    );

  font-size: 13px;
  font-weight: 800;

  box-shadow:
    0 5px 14px rgba(37, 99, 235, 0.18);
}

.profile-info {
  min-width: 0;

  display: flex;
  flex-direction: column;

  align-items: flex-start;
}

.profile-name {
  max-width: 120px;

  overflow: hidden;

  color: #1e293b;

  font-size: 11px;
  font-weight: 750;

  text-overflow: ellipsis;
  white-space: nowrap;
}

.profile-label {
  margin-top: 2px;

  color: #94a3b8;

  font-size: 9px;
}

.profile-arrow {
  color: #94a3b8;

  font-size: 19px;
}


/* ==========================================
   LOGOUT
========================================== */

.logout-button {
  width: 38px;
  height: 38px;

  display: flex;
  align-items: center;
  justify-content: center;

  border: 1px solid #e2e8f0;

  border-radius: 10px;

  color: #64748b;

  background: #ffffff;

  cursor: pointer;

  transition:
    color 0.2s ease,
    background 0.2s ease,
    border-color 0.2s ease;
}

.logout-button svg {
  width: 18px;
  height: 18px;
}

.logout-button:hover {
  color: #dc2626;

  background: #fef2f2;

  border-color: #fecaca;
}


/* ==========================================
   CONTENT
========================================== */

.content {
  flex: 1;

  min-width: 0;
  min-height: 0;

  overflow-y: auto;
  overflow-x: hidden;

  padding: 30px;

  box-sizing: border-box;

  background:
    linear-gradient(
      180deg,
      #f8fafc 0%,
      #f5f7fb 100%
    );
}


/* ==========================================
   SCROLLBAR
========================================== */

.content::-webkit-scrollbar {
  width: 7px;
}

.content::-webkit-scrollbar-track {
  background: transparent;
}

.content::-webkit-scrollbar-thumb {
  border-radius: 10px;

  background: #cbd5e1;
}

.content::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}


/* ==========================================
   TABLET
========================================== */

@media (max-width: 1100px) {

  .sidebar {
    width: 225px;
  }

  .topbar {
    padding: 0 20px;
  }

  .content {
    padding: 24px;
  }

  .profile-label,
  .profile-arrow {
    display: none;
  }

}


/* ==========================================
   MOBILE
========================================== */

@media (max-width: 800px) {

  .dashboard-layout {
    height: auto;
    min-height: 100vh;

    overflow: visible;
  }

  .sidebar {
    width: 100%;

    height: auto;

    padding: 14px 14px 12px;

    border-right: none;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);

    box-shadow:
      0 6px 20px rgba(15, 23, 42, 0.12);
  }

  .brand {
    margin-bottom: 14px;
  }

  .brand-logo {
    width: 38px;
    height: 38px;
  }

  .brand-title {
    font-size: 16px;
  }

  .brand-subtitle {
    font-size: 8px;
  }

  .navigation {
    display: grid;

    grid-template-columns:
      repeat(4, minmax(0, 1fr));

    gap: 5px;

    overflow-x: auto;

    padding-bottom: 2px;
  }

  .navigation-label {
    display: none;
  }

  .nav-item {
    min-height: 48px;

    padding: 6px 5px;

    flex-direction: column;

    justify-content: center;

    gap: 3px;

    border-radius: 10px;
  }

  .nav-item:hover {
    transform: none;
  }

  .nav-item.router-link-active::before {
    display: none;
  }

  .nav-icon {
    width: 20px;
    height: 20px;

    margin: 0;
  }

  .nav-icon svg {
    width: 18px;
    height: 18px;
  }

  .nav-text {
    font-size: 9px;

    text-align: center;

    white-space: nowrap;
  }

  .sidebar-bottom {
    display: none;
  }

  .main {
    width: 100%;

    min-height: calc(100vh - 110px);

    overflow: visible;
  }

  .topbar {
    min-height: 64px;

    padding: 0 14px;
  }

  .breadcrumb-muted,
  .breadcrumb-separator {
    display: none;
  }

  .breadcrumb-current {
    font-size: 16px;
  }

  .topbar-right {
    gap: 6px;
  }

  .profile-warning {
    width: 34px;
    height: 34px;

    justify-content: center;

    padding: 0;
  }

  .profile-warning > span:last-child {
    display: none;
  }

  .language-wrapper {
    height: 34px;

    padding: 0 6px;
  }

  .language-icon {
    display: none;
  }

  .lang-select {
    font-size: 10px;
  }

  .profile-button {
    padding: 2px;
  }

  .profile-info,
  .profile-arrow {
    display: none;
  }

  .avatar {
    width: 34px;
    height: 34px;
  }

  .logout-button {
    width: 34px;
    height: 34px;
  }

  .content {
    padding: 18px 14px 25px;
  }
}


/* ==========================================
   SMALL MOBILE
========================================== */

@media (max-width: 480px) {

  .navigation {
    grid-template-columns:
      repeat(4, 1fr);
  }

  .nav-item {
    min-width: 72px;
  }

  .nav-text {
    font-size: 8px;
  }

  .topbar {
    gap: 8px;
  }

  .breadcrumb-current {
    font-size: 14px;
  }

  .content {
    padding: 15px 10px 25px;
  }
}

</style>