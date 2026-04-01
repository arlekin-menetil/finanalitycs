<template>
  <div class="dashboard-layout">

    <!-- SIDEBAR -->
    <aside class="sidebar">
      <div class="brand">
        <div class="brand-title">Financial</div>
        <div class="brand-sub">Intelligence</div>
      </div>

      <nav>
        <router-link to="/" class="nav-item" active-class="active">
          Dashboard
        </router-link>

        <router-link to="/scoring" class="nav-item" active-class="active">
          Scoring
        </router-link>

        <router-link to="/recommendations" class="nav-item" active-class="active">
          Recommendations
        </router-link>

        <router-link to="/analytics" class="nav-item" active-class="active">
          Analytics
        </router-link>

        <router-link to="/monitoring" class="nav-item" active-class="active">
          Monitoring
        </router-link>
      </nav>
    </aside>

    <!-- MAIN -->
    <div class="main">

      <!-- TOPBAR -->
      <header class="topbar">

        <div class="title">
          {{ currentTitle }}
        </div>

        <div class="topbar-right">

          <!-- 💣 PROFILE STATUS -->
          <div
            v-if="!auth.isProfileCompleted"
            class="profile-warning"
            @click="goToProfile"
          >
            ⚠ Заполните профиль
          </div>

          <!-- 🌐 LANG -->
          <select v-model="locale" class="lang-select" @change="changeLang">
            <option value="ru">RU</option>
            <option value="en">EN</option>
            <option value="uz">UZ</option>
          </select>

          <!-- 👤 USER -->
          <div class="user-box">
            <span>{{ auth.user?.phone }}</span>
            <button @click="logout">Logout</button>
          </div>

        </div>

      </header>

      <!-- CONTENT -->
      <div class="content">
        <router-view />
      </div>

    </div>
  </div>
</template>

<script setup>
import { useI18n } from "vue-i18n"
import { useRoute, useRouter } from "vue-router"
import { computed } from "vue"
import { useAuthStore } from "@/stores/auth"

const { locale } = useI18n()
const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

// 🧠 заголовок
const currentTitle = computed(() => {
  return route.meta?.title || "Dashboard"
})

// 🌐 смена языка
const changeLang = () => {
  localStorage.setItem("lang", locale.value)
}

// 🚪 logout
const logout = () => {
  auth.logout()
  router.push("/login")
}

// 👉 профиль
const goToProfile = () => {
  router.push("/profile-setup")
}
</script>

<style scoped>
.dashboard-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
  font-family: Inter, system-ui;
  background: #f4f6f9;
}

/* SIDEBAR */
.sidebar {
  width: 260px;
  background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
  color: white;
  padding: 32px 22px;
  display: flex;
  flex-direction: column;
}

.brand {
  margin-bottom: 50px;
}

.brand-title {
  font-size: 20px;
  font-weight: 700;
}

.brand-sub {
  font-size: 13px;
  opacity: 0.6;
}

/* NAV */
.nav-item {
  display: block;
  padding: 12px 16px;
  border-radius: 10px;
  margin-bottom: 10px;
  color: white;
  opacity: 0.8;
  text-decoration: none;
}

.nav-item:hover {
  background: #1e293b;
  opacity: 1;
}

.nav-item.active {
  background: #2563eb;
  opacity: 1;
}

/* MAIN */
.main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* TOPBAR */
.topbar {
  background: white;
  padding: 18px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: 14px;
}

/* 💣 профиль warning */
.profile-warning {
  background: #fef3c7;
  color: #92400e;
  padding: 6px 12px;
  border-radius: 10px;
  font-size: 13px;
  cursor: pointer;
}

/* USER */
.user-box {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-box button {
  background: #111827;
  color: white;
  border: none;
  padding: 6px 10px;
  border-radius: 8px;
  cursor: pointer;
}

/* CONTENT */
.content {
  flex: 1;
  overflow-y: auto;
  padding: 35px;
}

/* LANG */
.lang-select {
  padding: 6px 10px;
  border-radius: 8px;
}
</style>