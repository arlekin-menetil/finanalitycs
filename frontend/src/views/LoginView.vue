<script setup>

import {
  ref
} from "vue"

import {
  useRouter
} from "vue-router"

import {
  useAuthStore
} from "@/stores/auth"


const phone = ref("")
const password = ref("")

const auth = useAuthStore()
const router = useRouter()


// ==========================================
// 🔐 LOGIN
// ==========================================

const handleLogin = async () => {

  console.log(
    "🔥 LOGIN CLICKED"
  )

  try {

    auth.error = null

    await auth.login(
      phone.value,
      password.value
    )

    console.log(
      "✅ LOGIN SUCCESS"
    )

    if (
      auth.isProfileCompleted
    ) {

      router.push("/")

    } else {

      router.push(
        "/profile-setup"
      )

    }

  } catch (e) {

    console.error(
      "❌ Login error:",
      e
    )

  }

}


// ==========================================
// ◀️ BACK
// ==========================================

const goBack = () => {

  if (
    window.history.length > 1
  ) {

    router.back()

  } else {

    router.push("/")

  }

}


// ==========================================
// 🧠 ERROR FORMAT
// ==========================================

const formatError = (
  error
) => {

  if (!error) {
    return ""
  }

  if (
    typeof error === "string"
  ) {
    return error
  }

  if (error.error) {
    return error.error
  }

  if (error.detail) {
    return error.detail
  }

  if (
    error.non_field_errors
  ) {

    return error.non_field_errors[0]

  }

  return "Login failed"

}

</script>


<template>

  <div class="login-page">

    <!-- BACK -->

    <button
      type="button"
      class="back-btn"
      @click="goBack"
    >

      <span class="back-btn__arrow">
        ←
      </span>

      <span>
        Назад
      </span>

    </button>


    <!-- BACKGROUND DECORATION -->

    <div class="background-decoration background-decoration--one"></div>

    <div class="background-decoration background-decoration--two"></div>


    <!-- LOGIN CARD -->

    <div class="login-card">


      <!-- LOGO -->

      <div class="brand">

        <img
          src="/logo.png"
          alt="FinAnalytics"
          class="brand__logo"
        />

      </div>


      <!-- HEADER -->

      <div class="login-header">

        <h1>
          Вход в FinAnalytics
        </h1>

        <p>
          Персональные рекомендации
          по кредитам и банковским продуктам
        </p>

      </div>


      <!-- FORM -->

      <form
        class="login-form"
        @submit.prevent="handleLogin"
      >


        <!-- PHONE -->

        <div class="field">

          <label
            for="phone"
          >
            Номер телефона
          </label>

          <div class="input-wrapper">

            <span class="input-icon">
              📱
            </span>

            <input
              id="phone"
              v-model="phone"
              type="text"
              inputmode="tel"
              autocomplete="tel"
              placeholder="+998 90 123 45 67"
              required
            />

          </div>

        </div>


        <!-- PASSWORD -->

        <div class="field">

          <label
            for="password"
          >
            Пароль
          </label>

          <div class="input-wrapper">

            <span class="input-icon">
              🔒
            </span>

            <input
              id="password"
              v-model="password"
              type="password"
              autocomplete="current-password"
              placeholder="Введите пароль"
              required
            />

          </div>

        </div>


        <!-- ERROR -->

        <div
          v-if="auth.error"
          class="error"
        >

          <span class="error__icon">
            !
          </span>

          <span>
            {{
              formatError(
                auth.error
              )
            }}
          </span>

        </div>


        <!-- LOGIN BUTTON -->

        <button
          type="submit"
          class="login-btn"
          :disabled="auth.loading"
        >

          <span
            v-if="auth.loading"
            class="login-btn__loader"
          ></span>

          <span v-if="auth.loading">
            Вход...
          </span>

          <span v-else>
            Войти
          </span>

        </button>

      </form>


      <!-- FOOTER -->

      <div class="login-footer">

        <span class="login-footer__line"></span>

        <p>
          Вход означает согласие
          с условиями сервиса
        </p>

        <span class="login-footer__line"></span>

      </div>

    </div>

  </div>

</template>


<style scoped>

/* ==========================================
   PAGE
========================================== */

.login-page {

  position:
    relative;

  min-height:
    100vh;

  width:
    100%;

  padding:
    30px 20px;

  box-sizing:
    border-box;

  display:
    flex;

  align-items:
    center;

  justify-content:
    center;

  overflow:
    hidden;

  background:
    linear-gradient(
      135deg,
      #f8fafc 0%,
      #eef4ff 50%,
      #f8fafc 100%
    );

}


/* ==========================================
   BACKGROUND
========================================== */

.background-decoration {

  position:
    absolute;

  border-radius:
    50%;

  pointer-events:
    none;

  filter:
    blur(2px);

}


.background-decoration--one {

  width:
    420px;

  height:
    420px;

  top:
    -180px;

  right:
    -120px;

  background:
    rgba(
      37,
      99,
      235,
      0.08
    );

}


.background-decoration--two {

  width:
    360px;

  height:
    360px;

  bottom:
    -180px;

  left:
    -120px;

  background:
    rgba(
      56,
      189,
      248,
      0.08
    );

}


/* ==========================================
   BACK BUTTON
========================================== */

.back-btn {

  position:
    absolute;

  top:
    25px;

  left:
    30px;

  z-index:
    10;

  display:
    flex;

  align-items:
    center;

  gap:
    7px;

  padding:
    9px 14px;

  border:
    1px solid
    #e2e8f0;

  border-radius:
    10px;

  background:
    rgba(
      255,
      255,
      255,
      0.85
    );

  color:
    #475569;

  font-size:
    13px;

  font-weight:
    600;

  cursor:
    pointer;

  backdrop-filter:
    blur(10px);

  box-shadow:
    0 4px 12px
    rgba(
      15,
      23,
      42,
      0.05
    );

  transition:
    all 0.2s ease;

}


.back-btn:hover {

  color:
    #2563eb;

  border-color:
    #bfdbfe;

  background:
    #ffffff;

  transform:
    translateX(
      -2px
    );

}


.back-btn__arrow {

  font-size:
    17px;

  line-height:
    1;

}


/* ==========================================
   CARD
========================================== */

.login-card {

  position:
    relative;

  z-index:
    2;

  width:
    100%;

  max-width:
    430px;

  padding:
    34px;

  box-sizing:
    border-box;

  background:
    rgba(
      255,
      255,
      255,
      0.96
    );

  border:
    1px solid
    rgba(
      226,
      232,
      240,
      0.9
    );

  border-radius:
    22px;

  box-shadow:
    0 25px 60px
    rgba(
      15,
      23,
      42,
      0.09
    );

  backdrop-filter:
    blur(15px);

}


/* ==========================================
   BRAND
========================================== */

.brand {

  display:
    flex;

  justify-content:
    center;

  margin-bottom:
    22px;

}


.brand__logo {

  display:
    block;

  width:
    190px;

  max-height:
    60px;

  object-fit:
    contain;

}


/* ==========================================
   HEADER
========================================== */

.login-header {

  text-align:
    center;

  margin-bottom:
    28px;

}


.login-header h1 {

  margin:
    0;

  color:
    #0f172a;

  font-size:
    25px;

  line-height:
    1.25;

  font-weight:
    700;

  letter-spacing:
    -0.02em;

}


.login-header p {

  margin:
    9px auto 0;

  max-width:
    340px;

  color:
    #64748b;

  font-size:
    13px;

  line-height:
    1.55;

}


/* ==========================================
   FORM
========================================== */

.login-form {

  display:
    flex;

  flex-direction:
    column;

  gap:
    18px;

}


/* ==========================================
   FIELD
========================================== */

.field {

  display:
    flex;

  flex-direction:
    column;

  gap:
    7px;

}


.field label {

  color:
    #334155;

  font-size:
    12px;

  font-weight:
    600;

}


/* ==========================================
   INPUT WRAPPER
========================================== */

.input-wrapper {

  position:
    relative;

  display:
    flex;

  align-items:
    center;

}


.input-icon {

  position:
    absolute;

  left:
    13px;

  z-index:
    1;

  font-size:
    15px;

  opacity:
    0.65;

  pointer-events:
    none;

}


/* ==========================================
   INPUT
========================================== */

.input-wrapper input {

  width:
    100%;

  height:
    48px;

  padding:
    0 14px 0 42px;

  box-sizing:
    border-box;

  border:
    1px solid
    #e2e8f0;

  border-radius:
    12px;

  outline:
    none;

  background:
    #f8fafc;

  color:
    #0f172a;

  font-size:
    14px;

  transition:
    border-color 0.2s ease,
    background 0.2s ease,
    box-shadow 0.2s ease;

}


.input-wrapper input::placeholder {

  color:
    #94a3b8;

}


.input-wrapper input:hover {

  border-color:
    #cbd5e1;

}


.input-wrapper input:focus {

  background:
    #ffffff;

  border-color:
    #2563eb;

  box-shadow:
    0 0 0 3px
    rgba(
      37,
      99,
      235,
      0.10
    );

}


/* ==========================================
   ERROR
========================================== */

.error {

  display:
    flex;

  align-items:
    center;

  gap:
    9px;

  padding:
    11px 12px;

  border:
    1px solid
    #fecaca;

  border-radius:
    10px;

  background:
    #fef2f2;

  color:
    #dc2626;

  font-size:
    12px;

  line-height:
    1.4;

}


.error__icon {

  width:
    20px;

  height:
    20px;

  flex-shrink:
    0;

  display:
    flex;

  align-items:
    center;

  justify-content:
    center;

  border-radius:
    50%;

  background:
    #dc2626;

  color:
    #ffffff;

  font-size:
    12px;

  font-weight:
    700;

}


/* ==========================================
   LOGIN BUTTON
========================================== */

.login-btn {

  width:
    100%;

  height:
    48px;

  border:
    none;

  border-radius:
    12px;

  background:
    linear-gradient(
      135deg,
      #2563eb,
      #38bdf8
    );

  color:
    #ffffff;

  display:
    flex;

  align-items:
    center;

  justify-content:
    center;

  gap:
    9px;

  font-size:
    14px;

  font-weight:
    700;

  cursor:
    pointer;

  box-shadow:
    0 8px 20px
    rgba(
      37,
      99,
      235,
      0.20
    );

  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    opacity 0.2s ease;

}


.login-btn:hover:not(:disabled) {

  transform:
    translateY(
      -1px
    );

  box-shadow:
    0 12px 25px
    rgba(
      37,
      99,
      235,
      0.28
    );

}


.login-btn:active:not(:disabled) {

  transform:
    translateY(0);

}


.login-btn:disabled {

  opacity:
    0.65;

  cursor:
    not-allowed;

  box-shadow:
    none;

}


/* ==========================================
   LOADER
========================================== */

.login-btn__loader {

  width:
    15px;

  height:
    15px;

  border:
    2px solid
    rgba(
      255,
      255,
      255,
      0.4
    );

  border-top-color:
    #ffffff;

  border-radius:
    50%;

  animation:
    login-spin
    0.7s
    linear
    infinite;

}


@keyframes login-spin {

  to {

    transform:
      rotate(
        360deg
      );

  }

}


/* ==========================================
   FOOTER
========================================== */

.login-footer {

  display:
    flex;

  align-items:
    center;

  gap:
    10px;

  margin-top:
    23px;

}


.login-footer__line {

  flex:
    1;

  height:
    1px;

  background:
    #e2e8f0;

}


.login-footer p {

  margin:
    0;

  color:
    #94a3b8;

  font-size:
    10px;

  line-height:
    1.4;

  text-align:
    center;

  white-space:
    nowrap;

}


/* ==========================================
   MOBILE
========================================== */

@media (max-width: 600px) {

  .login-page {

    padding:
      70px 16px 25px;

  }


  .back-btn {

    top:
      18px;

    left:
      16px;

  }


  .login-card {

    padding:
      28px 22px;

    border-radius:
      18px;

  }


  .brand__logo {

    width:
      165px;

  }


  .login-header h1 {

    font-size:
      22px;

  }


  .login-header p {

    font-size:
      12px;

  }


  .login-footer p {

    white-space:
      normal;

  }

}


/* ==========================================
   SMALL MOBILE
========================================== */

@media (max-width: 380px) {

  .login-card {

    padding:
      24px 18px;

  }


  .brand__logo {

    width:
      145px;

  }


  .back-btn span:last-child {

    display:
      none;

  }

}

</style>