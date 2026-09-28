<script setup>

import {
  ref,
  nextTick
} from "vue"

import { useI18n } from "vue-i18n"

import { useAuthStore } from "@/stores/auth"
import { useRouter } from "vue-router"
import api from "@/api/axios"

const { t } = useI18n()

const auth = useAuthStore()
const router = useRouter()

const step = ref(1)

const phone = ref("")
const code = ref("")

const loading = ref(false)
const error = ref(null)

const codeInput = ref(null)

// ==========================================
// 📱 CLEAN PHONE
// ==========================================

const cleanPhone = (value = "") => {

  return value.replace(/\D/g, "")

}

// ==========================================
// 🔙 BACK
// ==========================================

const goBack = () => {

  // Если мы на втором шаге —
  // возвращаемся к вводу номера

  if (step.value === 2) {

    step.value = 1

    code.value = ""

    error.value = null

    return

  }

  // Если мы на первом шаге —
  // всегда возвращаемся на лендинг

  router.replace("/")

}

// ==========================================
// 📩 SEND CODE
// ==========================================

const sendCode = async () => {

  error.value = null

  const cleaned =
    cleanPhone(phone.value)

  // Проверка номера

  if (!cleaned) {

    error.value =
      t("auth.enterPhone")

    return

  }

  if (cleaned.length !== 12) {

    error.value =
      t("auth.invalidPhone")

    return

  }

  loading.value = true

  try {

    await api.post(
      "/auth/send-code/",
      {
        phone: cleaned
      }
    )

    // Переходим ко второму шагу

    step.value = 2

    // Очищаем старую ошибку

    error.value = null

    // Ждём появления input в DOM

    await nextTick()

    // Автоматически ставим курсор

    codeInput.value?.focus()

  }

  catch (e) {

    console.error(
      "Send code error:",
      e
    )

    error.value =

      e?.response?.data?.error ||

      e?.response?.data?.detail ||

      t("auth.sendCodeError")

  }

  finally {

    loading.value = false

  }

}

// ==========================================
// 🔐 VERIFY CODE
// ==========================================

const verifyCode = async () => {

  error.value = null

  const enteredCode =
    code.value.trim()

  // Проверка кода

  if (!enteredCode) {

    error.value =
      t("auth.enterCode")

    return

  }

  loading.value = true

  try {

    const { data } =
      await api.post(

        "/auth/verify-code/",

        {

          phone:
            cleanPhone(
              phone.value
            ),

          code:
            enteredCode

        }

      )

    // ======================================
    // 🔑 СОХРАНЯЕМ JWT
    // ======================================

    auth.setTokens(data)

    // ======================================
    // 👤 ЗАГРУЖАЕМ ПОЛЬЗОВАТЕЛЯ
    // ======================================

    await auth.loadUser()

    // ======================================
    // 🚀 РЕДИРЕКТ
    // ======================================

    if (auth.isProfileCompleted) {

      router.replace(
        "/app/dashboard"
      )

    }

    else {

      router.replace(
        "/app/profile-setup"
      )

    }

  }

  catch (e) {

    console.error(
      "Verify error:",
      e
    )

    error.value =

      e?.response?.data?.error ||

      e?.response?.data?.detail ||

      t("auth.invalidCode")

  }

  finally {

    loading.value = false

  }

}

</script>

<template>
  <div class="login-page">

    <!-- Декоративный фон -->
    <div class="background-shape background-shape--one"></div>
    <div class="background-shape background-shape--two"></div>
    <div class="background-grid"></div>

    <!-- Кнопка назад -->
    <button
      class="back-button"
      type="button"
      @click="goBack"
    >
      <span class="back-button__icon">←</span>
      <span>{{ t("login.back") }}</span>
    </button>

    <main class="login-container">

      <div class="login-card">

        <!-- Логотип -->
        <div class="brand">
          <div class="brand__logo">
            <img
              src="/logo.png"
              alt="FinAnalytics"
            />
          </div>

          <div class="brand__name">
            FinAnalytics
          </div>
        </div>

        <!-- Заголовок -->
        <div class="login-header">

          <div class="login-icon">
            <svg
              v-if="step === 1"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M22 16.92v3a2 2 0 0 1-2.18 2A19.79 19.79 0 0 1 3.08 5.18 2 2 0 0 1 5.06 3h3a2 2 0 0 1 2 1.72c.12.9.33 1.78.62 2.63a2 2 0 0 1-.45 2.11L9 10.73a16 16 0 0 0 4.27 4.27l1.27-1.27a2 2 0 0 1 2.11-.45c.85.29 1.73.5 2.63.62A2 2 0 0 1 21 15.9z" />
            </svg>

            <svg
              v-else
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <rect
                x="3"
                y="11"
                width="18"
                height="10"
                rx="2"
              />
              <path d="M7 11V7a5 5 0 0 1 10 0v4" />
            </svg>
          </div>

          <h1>
            {{
  step === 1
    ? t("login.title")
    : t("login.confirmTitle")
}}
          </h1>

          <p v-if="step === 1">
            {{ t("login.subtitle") }}
          </p>

          <p v-else>
            {{ t("login.confirmSubtitle") }}
          </p>
        </div>

        <!-- Индикатор шагов -->
        <div class="steps">

          <div
            class="step"
            :class="{ 'step--active': step === 1, 'step--done': step === 2 }"
          >
            <div class="step__number">
              <span v-if="step === 2">✓</span>
              <span v-else>1</span>
            </div>

            {{ t("login.phoneStep") }}
          </div>

          <div class="steps__line"></div>

          <div
            class="step"
            :class="{ 'step--active': step === 2 }"
          >
            <div class="step__number">
              2
            </div>

            {{ t("login.codeStep") }}
          </div>

        </div>

        <!-- =============================== -->
        <!-- STEP 1 -->
        <!-- =============================== -->

        <form
          v-if="step === 1"
          class="login-form"
          @submit.prevent="sendCode"
        >

          <div class="field">

            <label for="phone">
              {{ t("login.phone") }}
            </label>

            <div class="input-wrapper">

              <span class="input-icon">

                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.8"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="M22 16.92v3a2 2 0 0 1-2.18 2A19.79 19.79 0 0 1 3.08 5.18 2 2 0 0 1 5.06 3h3a2 2 0 0 1 2 1.72c.12.9.33 1.78.62 2.63a2 2 0 0 1-.45 2.11L9 10.73a16 16 0 0 0 4.27 4.27l1.27-1.27a2 2 0 0 1 2.11-.45c.85.29 1.73.5 2.63.62A2 2 0 0 1 21 15.9z" />
                </svg>

              </span>

              <input
                id="phone"
                v-model="phone"
                type="tel"
                inputmode="numeric"
                autocomplete="tel"
                :placeholder="t('login.phonePlaceholder')"
                :disabled="loading"
                @keyup.enter="sendCode"
              />

            </div>

            <span class="field-hint">
              {{ t("login.phoneHint") }}
            </span>

          </div>

          <button
            class="submit-button"
            type="submit"
            :disabled="loading"
          >

            <span v-if="loading" class="loader"></span>

            <span>
              {{
  loading
    ? t("login.sending")
    : t("login.sendCode")
}}
            </span>

            <span
              v-if="!loading"
              class="submit-arrow"
            >
              →
            </span>

          </button>

        </form>

        <!-- =============================== -->
        <!-- STEP 2 -->
        <!-- =============================== -->

        <form
          v-else
          class="login-form"
          @submit.prevent="verifyCode"
        >

          <div class="phone-preview">

            <div class="phone-preview__icon">
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="1.8"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path d="M22 16.92v3a2 2 0 0 1-2.18 2A19.79 19.79 0 0 1 3.08 5.18 2 2 0 0 1 5.06 3h3a2 2 0 0 1 2 1.72c.12.9.33 1.78.62 2.63a2 2 0 0 1-.45 2.11L9 10.73a16 16 0 0 0 4.27 4.27l1.27-1.27a2 2 0 0 1 2.11-.45c.85.29 1.73.5 2.63.62A2 2 0 0 1 21 15.9z" />
              </svg>
            </div>

            <div>
              <span>{{ t("login.codeSent") }}</span>
              <strong>+{{ cleanPhone(phone) }}</strong>
            </div>

          </div>

          <div class="field">

            <label for="code">
              {{ t("login.code") }}
            </label>

            <div class="input-wrapper input-wrapper--code">

              <span class="input-icon">

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
                    y="11"
                    width="18"
                    height="10"
                    rx="2"
                  />
                  <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                </svg>

              </span>

              <input
                ref="codeInput"
                id="code"
                v-model="code"
                type="text"
                inputmode="numeric"
                autocomplete="one-time-code"
                :placeholder="t('login.codePlaceholder')"
                maxlength="6"
                :disabled="loading"
                @keyup.enter="verifyCode"
              />

            </div>

          </div>

          <button
            class="submit-button"
            type="submit"
            :disabled="loading"
          >

            <span v-if="loading" class="loader"></span>

            <span>
              {{
  loading
    ? t("login.checking")
    : t("login.login")
}}
            </span>

            <span
              v-if="!loading"
              class="submit-arrow"
            >
              →
            </span>

          </button>

          <button
            class="change-phone"
            type="button"
            @click="step = 1; error = null"
          >
            ← {{ t("login.changePhone") }}
          </button>

        </form>

        <!-- Ошибка -->

        <transition name="error">
          <div
            v-if="error"
            class="error-box"
          >

            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <circle
                cx="12"
                cy="12"
                r="10"
              />

              <line
                x1="12"
                y1="8"
                x2="12"
                y2="12"
              />

              <line
                x1="12"
                y1="16"
                x2="12.01"
                y2="16"
              />
            </svg>

            <span>{{ error }}</span>

          </div>
        </transition>

        <!-- Нижняя часть -->

        <div class="login-footer">

          <div class="security">

            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.7"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <rect
                x="3"
                y="11"
                width="18"
                height="10"
                rx="2"
              />
              <path d="M7 11V7a5 5 0 0 1 10 0v4" />
            </svg>

            <span>
              {{ t("login.secure") }}
            </span>

          </div>

          <p>
            {{ t("login.agreement") }}
          </p>

        </div>

      </div>

      <!-- Подпись -->

      <div class="copyright">
        © {{ new Date().getFullYear() }} FinAnalytics
      </div>

    </main>

  </div>
</template>

<style scoped>
/* ==========================================
   PAGE
========================================== */

.login-page {
  position: relative;
  min-height: 100vh;
  width: 100%;
  overflow: hidden;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 40px 20px;

  box-sizing: border-box;

  background:
    radial-gradient(
      circle at 15% 20%,
      rgba(59, 130, 246, 0.14),
      transparent 32%
    ),
    radial-gradient(
      circle at 85% 80%,
      rgba(6, 182, 212, 0.12),
      transparent 32%
    ),
    linear-gradient(
      135deg,
      #f8fbff 0%,
      #eef5ff 50%,
      #f7fbff 100%
    );

  font-family:
    Inter,
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    sans-serif;
}

/* ==========================================
   BACKGROUND
========================================== */

.background-grid {
  position: absolute;
  inset: 0;

  opacity: 0.35;

  background-image:
    linear-gradient(
      rgba(148, 163, 184, 0.07) 1px,
      transparent 1px
    ),
    linear-gradient(
      90deg,
      rgba(148, 163, 184, 0.07) 1px,
      transparent 1px
    );

  background-size: 45px 45px;

  pointer-events: none;
}

.background-shape {
  position: absolute;
  border-radius: 999px;
  filter: blur(2px);
  pointer-events: none;
}

.background-shape--one {
  width: 420px;
  height: 420px;

  top: -220px;
  left: -180px;

  background:
    radial-gradient(
      circle,
      rgba(37, 99, 235, 0.14),
      transparent 68%
    );
}

.background-shape--two {
  width: 500px;
  height: 500px;

  right: -260px;
  bottom: -260px;

  background:
    radial-gradient(
      circle,
      rgba(6, 182, 212, 0.13),
      transparent 68%
    );
}

/* ==========================================
   BACK BUTTON
========================================== */

.back-button {
  position: absolute;

  top: 28px;
  left: 30px;

  z-index: 10;

  display: inline-flex;
  align-items: center;
  gap: 9px;

  padding: 10px 15px;

  border: 1px solid rgba(148, 163, 184, 0.22);
  border-radius: 12px;

  background: rgba(255, 255, 255, 0.75);

  color: #475569;

  font-size: 14px;
  font-weight: 600;

  cursor: pointer;

  box-shadow:
    0 5px 20px rgba(15, 23, 42, 0.05);

  backdrop-filter: blur(10px);

  transition:
    transform 0.2s ease,
    background 0.2s ease,
    color 0.2s ease,
    box-shadow 0.2s ease;
}

.back-button:hover {
  transform: translateY(-1px);

  background: #ffffff;

  color: #2563eb;

  box-shadow:
    0 8px 24px rgba(15, 23, 42, 0.08);
}

.back-button__icon {
  font-size: 20px;
  line-height: 1;
}

/* ==========================================
   CONTAINER
========================================== */

.login-container {
  position: relative;
  z-index: 2;

  width: 100%;
  max-width: 460px;

  display: flex;
  flex-direction: column;
  align-items: center;
}

/* ==========================================
   CARD
========================================== */

.login-card {
  width: 100%;
  box-sizing: border-box;

  padding: 34px;

  background: rgba(255, 255, 255, 0.96);

  border: 1px solid rgba(226, 232, 240, 0.85);

  border-radius: 26px;

  box-shadow:
    0 30px 70px rgba(15, 23, 42, 0.10),
    0 8px 25px rgba(37, 99, 235, 0.05);

  backdrop-filter: blur(18px);
}

/* ==========================================
   BRAND
========================================== */

.brand {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 11px;

  margin-bottom: 25px;
}

.brand__logo {
  width: 44px;
  height: 44px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 13px;

  overflow: hidden;

  background: #ffffff;

  box-shadow:
    0 6px 18px rgba(37, 99, 235, 0.12);
}

.brand__logo img {
  width: 100%;
  height: 100%;

  object-fit: contain;
}

.brand__name {
  font-size: 19px;
  font-weight: 800;

  letter-spacing: -0.4px;

  color: #0f172a;
}

/* ==========================================
   HEADER
========================================== */

.login-header {
  text-align: center;
}

.login-icon {
  width: 58px;
  height: 58px;

  margin: 0 auto 17px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 17px;

  color: #2563eb;

  background:
    linear-gradient(
      135deg,
      rgba(37, 99, 235, 0.12),
      rgba(6, 182, 212, 0.10)
    );

  border: 1px solid rgba(37, 99, 235, 0.08);
}

.login-icon svg {
  width: 27px;
  height: 27px;
}

.login-header h1 {
  margin: 0;

  color: #0f172a;

  font-size: 26px;
  line-height: 1.2;

  font-weight: 800;

  letter-spacing: -0.6px;
}

.login-header p {
  max-width: 330px;

  margin: 10px auto 0;

  color: #64748b;

  font-size: 14px;
  line-height: 1.6;
}

/* ==========================================
   STEPS
========================================== */

.steps {
  display: flex;
  align-items: center;

  margin: 27px 0 28px;
}

.step {
  display: flex;
  align-items: center;
  gap: 8px;

  color: #94a3b8;

  font-size: 12px;
  font-weight: 700;

  white-space: nowrap;
}

.step__number {
  width: 28px;
  height: 28px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 50%;

  color: #94a3b8;

  background: #f1f5f9;

  border: 1px solid #e2e8f0;

  font-size: 12px;
  font-weight: 800;

  transition: 0.25s ease;
}

.step--active {
  color: #2563eb;
}

.step--active .step__number {
  color: #ffffff;

  background:
    linear-gradient(
      135deg,
      #2563eb,
      #06b6d4
    );

  border-color: transparent;

  box-shadow:
    0 5px 14px rgba(37, 99, 235, 0.22);
}

.step--done .step__number {
  color: #ffffff;

  background: #10b981;

  border-color: #10b981;
}

.steps__line {
  flex: 1;

  height: 1px;

  margin: 0 12px;

  background: #e2e8f0;
}

/* ==========================================
   FORM
========================================== */

.login-form {
  display: flex;
  flex-direction: column;

  gap: 20px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.field label {
  color: #334155;

  font-size: 13px;
  font-weight: 700;

  text-align: left;
}

.field-hint {
  color: #94a3b8;

  font-size: 11px;
  line-height: 1.4;

  text-align: left;
}

/* ==========================================
   INPUT
========================================== */

.input-wrapper {
  position: relative;

  display: flex;
  align-items: center;

  width: 100%;
}

.input-icon {
  position: absolute;

  left: 16px;

  display: flex;
  align-items: center;
  justify-content: center;

  color: #94a3b8;

  pointer-events: none;

  transition: color 0.2s ease;
}

.input-icon svg {
  width: 20px;
  height: 20px;
}

.input-wrapper input {
  width: 100%;
  height: 54px;

  box-sizing: border-box;

  padding: 0 16px 0 48px;

  border: 1px solid #e2e8f0;

  border-radius: 14px;

  outline: none;

  background: #f8fafc;

  color: #0f172a;

  font-size: 15px;
  font-weight: 500;

  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease,
    background 0.2s ease;
}

.input-wrapper input::placeholder {
  color: #a8b2c1;
}

.input-wrapper input:hover:not(:disabled) {
  border-color: #cbd5e1;

  background: #ffffff;
}

.input-wrapper input:focus {
  border-color: #3b82f6;

  background: #ffffff;

  box-shadow:
    0 0 0 4px rgba(59, 130, 246, 0.10);
}

.input-wrapper:focus-within .input-icon {
  color: #2563eb;
}

.input-wrapper input:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

/* Код */

.input-wrapper--code input {
  text-align: center;

  padding-left: 48px;

  letter-spacing: 7px;

  font-size: 20px;
  font-weight: 800;
}

.input-wrapper--code input::placeholder {
  letter-spacing: 0;
  font-size: 14px;
  font-weight: 400;
}

/* ==========================================
   PHONE PREVIEW
========================================== */

.phone-preview {
  display: flex;
  align-items: center;
  gap: 12px;

  padding: 13px 15px;

  border: 1px solid #dbeafe;

  border-radius: 14px;

  background:
    linear-gradient(
      135deg,
      #f8fbff,
      #f0f9ff
    );
}

.phone-preview__icon {
  width: 38px;
  height: 38px;

  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 11px;

  color: #2563eb;

  background: #ffffff;
}

.phone-preview__icon svg {
  width: 19px;
  height: 19px;
}

.phone-preview span {
  display: block;

  margin-bottom: 2px;

  color: #94a3b8;

  font-size: 11px;
}

.phone-preview strong {
  color: #334155;

  font-size: 13px;

  font-weight: 700;
}

/* ==========================================
   SUBMIT BUTTON
========================================== */

.submit-button {
  width: 100%;
  height: 54px;

  display: flex;
  align-items: center;
  justify-content: center;
  gap: 9px;

  border: none;
  border-radius: 14px;

  color: #ffffff;

  background:
    linear-gradient(
      135deg,
      #2563eb 0%,
      #3b82f6 50%,
      #06b6d4 100%
    );

  box-shadow:
    0 10px 24px rgba(37, 99, 235, 0.22);

  font-size: 14px;
  font-weight: 700;

  cursor: pointer;

  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    opacity 0.2s ease;
}

.submit-button:hover:not(:disabled) {
  transform: translateY(-1px);

  box-shadow:
    0 14px 30px rgba(37, 99, 235, 0.28);
}

.submit-button:active:not(:disabled) {
  transform: translateY(0);
}

.submit-button:disabled {
  opacity: 0.65;

  cursor: not-allowed;

  box-shadow: none;
}

.submit-arrow {
  font-size: 19px;

  line-height: 1;
}

/* ==========================================
   LOADER
========================================== */

.loader {
  width: 17px;
  height: 17px;

  border: 2px solid rgba(255, 255, 255, 0.35);
  border-top-color: #ffffff;

  border-radius: 50%;

  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* ==========================================
   CHANGE PHONE
========================================== */

.change-phone {
  padding: 3px 0;

  border: none;

  color: #64748b;

  background: transparent;

  font-size: 13px;
  font-weight: 600;

  cursor: pointer;

  transition: color 0.2s ease;
}

.change-phone:hover {
  color: #2563eb;
}

/* ==========================================
   ERROR
========================================== */

.error-box {
  display: flex;
  align-items: flex-start;
  gap: 10px;

  margin-top: 18px;

  padding: 12px 14px;

  border: 1px solid #fecaca;

  border-radius: 12px;

  color: #b91c1c;

  background: #fef2f2;

  font-size: 12px;
  line-height: 1.5;

  text-align: left;
}

.error-box svg {
  width: 18px;
  height: 18px;

  flex-shrink: 0;

  margin-top: 1px;
}

.error-enter-active,
.error-leave-active {
  transition:
    opacity 0.2s ease,
    transform 0.2s ease;
}

.error-enter-from,
.error-leave-to {
  opacity: 0;
  transform: translateY(-5px);
}

/* ==========================================
   FOOTER
========================================== */

.login-footer {
  margin-top: 25px;

  text-align: center;
}

.security {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 7px;

  margin-bottom: 9px;

  color: #64748b;

  font-size: 11px;
  font-weight: 600;
}

.security svg {
  width: 15px;
  height: 15px;

  color: #10b981;
}

.login-footer p {
  max-width: 300px;

  margin: 0 auto;

  color: #94a3b8;

  font-size: 10px;
  line-height: 1.5;
}

/* ==========================================
   COPYRIGHT
========================================== */

.copyright {
  margin-top: 18px;

  color: #94a3b8;

  font-size: 11px;
  font-weight: 500;
}

/* ==========================================
   MOBILE
========================================== */

@media (max-width: 600px) {
  .login-page {
    align-items: flex-start;

    padding:
      85px
      15px
      30px;
  }

  .back-button {
    top: 18px;
    left: 15px;

    padding: 9px 12px;
  }

  .login-card {
    padding: 26px 20px;

    border-radius: 22px;
  }

  .brand {
    margin-bottom: 22px;
  }

  .login-header h1 {
    font-size: 23px;
  }

  .login-header p {
    font-size: 13px;
  }

  .steps {
    margin-top: 24px;
  }

  .step span:last-child {
    display: none;
  }

  .step__number {
    width: 30px;
    height: 30px;
  }

  .input-wrapper input {
    height: 52px;
  }

  .submit-button {
    height: 52px;
  }

  .background-shape--one {
    width: 280px;
    height: 280px;
  }

  .background-shape--two {
    width: 300px;
    height: 300px;
  }
}

/* ==========================================
   SMALL MOBILE
========================================== */

@media (max-width: 380px) {
  .login-page {
    padding-left: 10px;
    padding-right: 10px;
  }

  .login-card {
    padding: 23px 16px;
  }

  .login-header h1 {
    font-size: 21px;
  }

  .brand__name {
    font-size: 17px;
  }

  .login-icon {
    width: 52px;
    height: 52px;
  }
}
</style>