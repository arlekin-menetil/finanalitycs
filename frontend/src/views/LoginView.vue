<script setup>

import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

const phone = ref("")
const password = ref("")

const auth = useAuthStore()
const router = useRouter()


// ==========================================
// 🔐 LOGIN
// ==========================================
const handleLogin = async () => {
  console.log("🔥 LOGIN CLICKED")

  try {
    auth.error = null

    // 💣 логин
    await auth.login(phone.value, password.value)

    console.log("✅ LOGIN SUCCESS")

    // 💣 fetchUser УЖЕ вызывается внутри auth.login
    // 👉 поэтому второй вызов убираем (важно)
    // await auth.fetchUser()

    if (auth.isProfileCompleted) {
      router.push("/")
    } else {
      router.push("/profile-setup")
    }

  } catch (e) {
    console.error("❌ Login error:", e)
  }
}


// ==========================================
// 🧠 ERROR FORMAT
// ==========================================
const formatError = (error) => {

  if (!error) return ""

  if (typeof error === "string") return error

  if (error.error) return error.error

  if (error.detail) return error.detail

  if (error.non_field_errors) return error.non_field_errors[0]

  return "Login failed"

}

</script>


<template>

<div class="login-page">

  <div class="login-card">

    <!-- HEADER -->
    <div class="header">
      <h1>Financial Intelligence</h1>
      <p>Персональные рекомендации по кредитам и банкам</p>
    </div>

    <!-- FORM -->
    <form @submit.prevent="handleLogin">

      <input
        v-model="phone"
        type="text"
        placeholder="+998 90 123 45 67"
        required
      />

      <input
        v-model="password"
        type="password"
        placeholder="Пароль"
        required
      />

      <button type="submit" :disabled="auth.loading">

        <span v-if="auth.loading">
          Загрузка...
        </span>

        <span v-else>
          Войти
        </span>

      </button>

    </form>

    <!-- ERROR -->
    <p v-if="auth.error" class="error">
      {{ formatError(auth.error) }}
    </p>

    <!-- FOOTER -->
    <div class="footer">
      <p>
        Вход означает согласие с условиями сервиса
      </p>
    </div>

  </div>

</div>

</template>


<style scoped>

/* PAGE */

.login-page{
height:100vh;
display:flex;
justify-content:center;
align-items:center;
background:linear-gradient(135deg,#f4f6f9,#e5e7eb);
}

/* CARD */

.login-card{
width:100%;
max-width:420px;
padding:40px;
background:white;
border-radius:16px;
box-shadow:0 20px 40px rgba(0,0,0,0.08);
}

/* HEADER */

.header{
margin-bottom:24px;
text-align:center;
}

.header h1{
font-size:24px;
font-weight:700;
}

.header p{
color:#6b7280;
font-size:14px;
margin-top:6px;
}

/* INPUT */

input{
width:100%;
padding:12px;
margin-bottom:16px;
border-radius:10px;
border:1px solid #e5e7eb;
font-size:14px;
transition:0.2s;
}

input:focus{
outline:none;
border-color:#2563eb;
box-shadow:0 0 0 2px rgba(37,99,235,0.15);
}

/* BUTTON */

button{
width:100%;
padding:12px;
background:#111827;
color:white;
border:none;
border-radius:10px;
cursor:pointer;
font-size:14px;
transition:0.2s;
}

button:hover:not(:disabled){
background:#1f2937;
}

button:disabled{
opacity:0.6;
cursor:not-allowed;
}

/* ERROR */

.error{
margin-top:12px;
color:#dc2626;
font-size:14px;
text-align:center;
}

/* FOOTER */

.footer{
margin-top:20px;
font-size:12px;
color:#9ca3af;
text-align:center;
}

</style>