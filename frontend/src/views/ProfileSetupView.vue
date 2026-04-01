<script setup>

import { ref, computed } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"
import { useI18n } from "vue-i18n"

const router = useRouter()
const auth = useAuthStore()
const { t } = useI18n()

const loading = ref(false)
const error = ref(null)

// ==========================================
// 💣 FORM
// ==========================================

const form = ref({
  full_name: "",
  birth_date: "",
  passport: "",
  income: "",
  expenses: "", // 💣 FIX (было obligations)
  job_type: "employee",
  experience: ""
})

// ==========================================
// 🧠 VALIDATION
// ==========================================

const isValid = computed(() => {
  return (
    form.value.full_name &&
    form.value.birth_date &&
    form.value.passport &&
    Number(form.value.income) > 0 &&
    Number(form.value.experience) > 0
  )
})

// ==========================================
// 💣 SUBMIT
// ==========================================

const submit = async () => {

  if (!isValid.value || loading.value) return

  try {

    loading.value = true
    error.value = null

    await auth.setupProfile({
      full_name: form.value.full_name,
      birth_date: form.value.birth_date,
      passport: form.value.passport,
      job_type: form.value.job_type,
      experience: Number(form.value.experience),

      income: Number(form.value.income),
      expenses: Number(form.value.expenses || 0), // 💣 FIX
      credit_score: 600 // 💣 временно (потом заменим)
    })

    // 💣 редирект
    router.push("/scoring")

  } catch (e) {

    console.error(e)
    error.value = "Ошибка сохранения профиля"

  } finally {

    loading.value = false

  }

}

</script>


<template>

<div class="profile-page">

  <div class="card">

    <!-- HEADER -->
    <div class="header">
      <h1>🧠 {{ t("profile.title") || "Создание профиля" }}</h1>

      <p>
        {{ t("profile.subtitle") || "Нужно для расчета скоринга и рекомендаций" }}
      </p>
    </div>

    <!-- FORM -->
    <form class="form" @submit.prevent="submit">

      <!-- NAME -->
      <input
        v-model="form.full_name"
        type="text"
        placeholder="ФИО"
      />

      <!-- BIRTH -->
      <input
        v-model="form.birth_date"
        type="date"
      />

      <!-- PASSPORT -->
      <input
        v-model="form.passport"
        type="text"
        placeholder="AA1234567"
      />

      <!-- INCOME -->
      <input
        v-model="form.income"
        type="number"
        placeholder="Доход (UZS)"
      />

      <!-- EXPENSES -->
      <input
        v-model="form.expenses"
        type="number"
        placeholder="Расходы / обязательства (UZS)"
      />

      <!-- JOB TYPE -->
      <select v-model="form.job_type">
        <option value="employee">Сотрудник</option>
        <option value="self">Самозанятый</option>
        <option value="business">Бизнес</option>
      </select>

      <!-- EXPERIENCE -->
      <input
        v-model="form.experience"
        type="number"
        placeholder="Стаж (месяцы)"
      />

      <!-- ERROR -->
      <div v-if="error" class="error">
        {{ error }}
      </div>

      <!-- ACTION -->
      <button
        type="submit"
        class="submit"
        :disabled="!isValid || loading"
      >
        <span v-if="loading">
          Сохранение...
        </span>

        <span v-else>
          🚀 Продолжить
        </span>
      </button>

    </form>

  </div>

</div>

</template>


<style scoped>

.profile-page{
height:100vh;
display:flex;
justify-content:center;
align-items:center;
background:#f4f6f9;
}

.card{
width:100%;
max-width:500px;
background:white;
padding:40px;
border-radius:20px;
box-shadow:0 20px 50px rgba(0,0,0,0.08);
}

.header{
margin-bottom:20px;
}

.header h1{
font-size:24px;
}

.header p{
color:#6b7280;
font-size:14px;
margin-top:6px;
}

.form{
display:flex;
flex-direction:column;
gap:14px;
margin-bottom:20px;
}

input, select{
padding:12px;
border-radius:10px;
border:1px solid #e5e7eb;
font-size:14px;
}

input:focus{
outline:none;
border-color:#2563eb;
}

.submit{
width:100%;
padding:14px;
background:#2563eb;
color:white;
border:none;
border-radius:12px;
cursor:pointer;
font-weight:600;
}

.submit:disabled{
opacity:0.5;
cursor:not-allowed;
}

.error{
color:#ef4444;
margin-bottom:10px;
}

</style>