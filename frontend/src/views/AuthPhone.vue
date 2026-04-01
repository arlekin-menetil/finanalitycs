<script setup>
import { ref } from "vue"

const step = ref(1)

const phone = ref("")
const code = ref("")
const loading = ref(false)
const error = ref(null)

const cleanPhone = (p) => p.replace(/\D/g, "")

// 📩 SEND CODE
const sendCode = async () => {
  error.value = null

  if (!phone.value) {
    error.value = "Введите номер"
    return
  }

  loading.value = true

  try {
    const res = await fetch("http://127.0.0.1:8000/api/auth/send-code/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        phone: cleanPhone(phone.value)
      })
    })

    const data = await res.json()
    if (!res.ok) throw data

    step.value = 2
  } catch (e) {
    error.value = e.error || "Ошибка отправки"
  } finally {
    loading.value = false
  }
}

// 🔢 VERIFY CODE
const verifyCode = async () => {
  error.value = null

  if (!code.value) {
    error.value = "Введите код"
    return
  }

  loading.value = true

  try {
    const res = await fetch("http://127.0.0.1:8000/api/auth/verify-code/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        phone: cleanPhone(phone.value),
        code: code.value
      })
    })

    const data = await res.json()
    if (!res.ok) throw data

    localStorage.setItem("access", data.access)
    localStorage.setItem("refresh", data.refresh)

    window.location.href = "/"
  } catch (e) {
    error.value = e.error || "Неверный код"
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="wrapper">

    <div class="card">

      <h1>🔐 Вход в систему</h1>

      <!-- STEP 1 -->
      <div v-if="step === 1" class="form">

        <input
          v-model="phone"
          placeholder="+998901234567"
          @keyup.enter="sendCode"
        />

        <button
          @click="sendCode"
          :disabled="loading"
        >
          {{ loading ? "Отправка..." : "Получить код" }}
        </button>

      </div>

      <!-- STEP 2 -->
      <div v-else class="form">

        <input
          v-model="code"
          placeholder="Введите код"
          maxlength="6"
          @keyup.enter="verifyCode"
        />

        <button
          @click="verifyCode"
          :disabled="loading"
        >
          {{ loading ? "Проверка..." : "Войти" }}
        </button>

        <button class="link" @click="step = 1">
          ← изменить номер
        </button>

      </div>

      <p v-if="error" class="error">
        {{ error }}
      </p>

    </div>

  </div>
</template>

<style scoped>
.wrapper {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f3f4f6;
  font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}

.card {
  background: white;
  padding: 32px;
  border-radius: 18px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 15px 40px rgba(0,0,0,0.1);
  text-align: center;
}

h1 {
  margin-bottom: 20px;
  font-size: 22px;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

input {
  padding: 14px;
  border-radius: 12px;
  border: 1px solid #ddd;
  font-size: 14px;
  transition: 0.2s;
}

input:focus {
  outline: none;
  border-color: black;
  box-shadow: 0 0 0 2px rgba(0,0,0,0.05);
}

button {
  padding: 14px;
  border-radius: 12px;
  border: none;
  background: black;
  color: white;
  cursor: pointer;
  transition: 0.2s;
  font-weight: 500;
}

button:hover:not(:disabled) {
  background: #222;
}

button:disabled {
  background: #aaa;
  cursor: not-allowed;
}

.link {
  background: none;
  color: #666;
  font-size: 13px;
  margin-top: 5px;
}

.error {
  color: red;
  margin-top: 15px;
  font-size: 14px;
}
</style>