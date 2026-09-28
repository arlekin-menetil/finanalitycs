<script setup>
import {
  ref,
  watch,
  nextTick,
} from "vue"

import { useI18n } from "vue-i18n"
import api from "@/api/axios"
import { useRouter } from "vue-router"

const { t } = useI18n()
const router = useRouter()

// ==========================================
// PROPS
// ==========================================

const props = defineProps({
  profile: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits([
  "saved",
])

// ==========================================
// STATE
// ==========================================

const loading = ref(false)

const saving = ref(false)

const form = ref({
  full_name: "",
  birth_date: "",
  passport: "",
  job_type: "employee",
  income: 0,
  expenses: 0,
})

// ==========================================
// JOB TYPES
// ==========================================

const jobs = [
  {
    value: "employee",
    label: "employee",
  },
  {
    value: "business",
    label: "business",
  },
  {
    value: "self_employed",
    label: "selfEmployed",
  },
  {
    value: "freelancer",
    label: "freelancer",
  },
  {
    value: "student",
    label: "student",
  },
  {
    value: "unemployed",
    label: "unemployed",
  },
  {
    value: "pensioner",
    label: "pensioner",
  },
]

// ==========================================
// SYNC PROFILE
// ==========================================

watch(
  () => props.profile,

  async (profile) => {
    if (!profile)
      return

    await nextTick()

    form.value = {
      full_name:
        profile.full_name || "",

      birth_date:
        profile.birth_date || "",

      passport:
        profile.passport || "",

      job_type:
        profile.job_type || "employee",

      income:
        Number(profile.income || 0),

      expenses:
        Number(profile.expenses || 0),
    }
  },

  {
    immediate: true,
    deep: true,
  },
)

// ==========================================
// SAVE PROFILE
// ==========================================

async function saveProfile() {
  saving.value = true

  try {
    await api.post(
      "/profile/setup/",
      form.value,
    )

    emit("saved")

    await router.push(
      "/app/profile",
    )
  }

  catch (e) {
    console.error(e)

    alert(
      e.response?.data?.detail ||
      t("profileEdit.errors.saveFailed"),
    )
  }

  finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="card">
    <div class="card-header">
      <div>
        <h2>
          👤 {{ t("profileEdit.title") }}
        </h2>

        <p>
          {{ t("profileEdit.description") }}
        </p>
      </div>
    </div>

    <div
      v-if="loading"
      class="loading"
    >
      {{ t("profileEdit.loading") }}
    </div>

    <form
      v-else
      class="form"
      @submit.prevent="saveProfile"
    >
      <div class="field">
        <label>
          {{ t("profileEdit.fields.fullName") }}
        </label>

        <input
          v-model="form.full_name"
          type="text"
          :placeholder="t('profileEdit.placeholders.fullName')"
        >
      </div>

      <div class="field">
        <label>
          {{ t("profileEdit.fields.passport") }}
        </label>

        <input
          v-model="form.passport"
          type="text"
          placeholder="AA1234567"
        >
      </div>

      <div class="field">
        <label>
          {{ t("profileEdit.fields.birthDate") }}
        </label>

        <input
          v-model="form.birth_date"
          type="date"
        >
      </div>

      <div class="field">
        <label>
          {{ t("profileEdit.fields.jobType") }}
        </label>

        <select
          v-model="form.job_type"
        >
          <option
            v-for="job in jobs"
            :key="job.value"
            :value="job.value"
          >
            {{ t(`profileEdit.jobTypes.${job.label}`) }}
          </option>
        </select>
      </div>

      <div class="field">
        <label>
          {{ t("profileEdit.fields.income") }}
        </label>

        <input
          v-model.number="form.income"
          type="number"
          min="0"
          placeholder="0"
        >
      </div>

      <div class="field">
        <label>
          {{ t("profileEdit.fields.expenses") }}
        </label>

        <input
          v-model.number="form.expenses"
          type="number"
          min="0"
          placeholder="0"
        >
      </div>

      <div class="actions">
        <button
          class="save-btn"
          type="submit"
          :disabled="loading || saving"
        >
          💾
          {{
            saving
              ? t("profileEdit.buttons.saving")
              : t("profileEdit.buttons.save")
          }}
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.card {
  background: #fff;
  border-radius: 22px;
  padding: 32px;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
  margin-bottom: 30px;
}

.card-header {
  margin-bottom: 30px;
}

.card-header h2 {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #0f172a;
}

.card-header p {
  margin-top: 8px;
  font-size: 15px;
  color: #64748b;
}

.loading {
  padding: 40px;
  text-align: center;
  font-size: 18px;
  color: #2563eb;
  font-weight: 600;
}

.form {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 22px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.field label {
  font-size: 14px;
  font-weight: 600;
  color: #334155;
}

.field input,
.field select {
  width: 100%;
  padding: 14px 16px;
  border: 1px solid #dbe2ea;
  border-radius: 12px;
  font-size: 15px;
  background: #fff;
  transition: 0.25s;
  outline: none;
}

.field input:focus,
.field select:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.12);
}

.actions {
  grid-column: 1 / -1;
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

.save-btn {
  background: #2563eb;
  color: #fff;
  border: none;
  padding: 14px 30px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: 0.25s;
}

.save-btn:hover {
  background: #1d4ed8;
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(37, 99, 235, 0.22);
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

@media (max-width: 900px) {
  .form {
    grid-template-columns: 1fr;
  }

  .actions {
    justify-content: stretch;
  }

  .save-btn {
    width: 100%;
  }
}
</style>