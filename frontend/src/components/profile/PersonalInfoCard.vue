<script setup>

import { computed } from "vue"

const props = defineProps({

    profile: {
        type: Object,
        required: true,
    },

    user: {
        type: Object,
        required: true,
    },

})

defineEmits([
    "edit",
])

// ==========================================
// JOB TYPE
// ==========================================

const jobName = computed(() => {

    const jobs = {

        employee: "Сотрудник",

        business: "Предприниматель",

        entrepreneur: "Предприниматель",

        self_employed: "Самозанятый",

        freelancer: "Фрилансер",

        student: "Студент",

        unemployed: "Безработный",

        pensioner: "Пенсионер",

    }

    return jobs[props.profile?.job_type] ||
        props.profile?.job_type ||
        "Не указано"

})

// ==========================================
// BIRTH DATE
// ==========================================

const birthDate = computed(() => {

    if (!props.profile?.birth_date)
        return "—"

    const date = new Date(props.profile.birth_date)

    if (Number.isNaN(date.getTime()))
        return props.profile.birth_date

    return date.toLocaleDateString("ru-RU")

})

// ==========================================
// PASSPORT
// ==========================================

const passport = computed(() => {

    return props.profile?.passport || "—"

})

// ==========================================
// PHONE
// ==========================================

const phone = computed(() => {

    return (
        props.user?.phone ||
        props.user?.phone_number ||
        "—"
    )

})

// ==========================================
// PROFILE STATUS
// ==========================================

const profileStatus = computed(() => {

    return props.profile?.is_profile_completed
        ? "Заполнен"
        : "Не заполнен"

})

// ==========================================
// AVATAR
// ==========================================

const avatarLetter = computed(() => {

    const name = props.profile?.full_name

    if (!name)
        return "U"

    return name.trim().charAt(0).toUpperCase()

})

</script>

<template>

<div class="card">

    <!-- ===================================== -->
    <!-- HEADER -->
    <!-- ===================================== -->

    <div class="header">

        <div class="left">

            <div class="avatar">

                {{ avatarLetter }}

            </div>

            <div>

                <h2>

                    {{ profile.full_name || "Пользователь" }}

                </h2>

                <p>

                    {{ phone }}

                </p>

            </div>

        </div>

        <button
            class="edit"
            @click="$emit('edit')"
        >

            ✏️ Редактировать

        </button>

    </div>

    <!-- ===================================== -->
    <!-- PERSONAL INFO -->
    <!-- ===================================== -->

    <div class="grid">

        <div class="item">

            <span>

                🪪 Паспорт

            </span>

            <strong>

                {{ passport }}

            </strong>

        </div>

        <div class="item">

            <span>

                🎂 Дата рождения

            </span>

            <strong>

                {{ birthDate }}

            </strong>

        </div>

        <div class="item">

            <span>

                👤 Тип занятости

            </span>

            <strong>

                {{ jobName }}

            </strong>

        </div>

        <div class="item">

            <span>

                ✔ Статус профиля

            </span>

            <strong
                :class="{
                    completed: profile.is_profile_completed,
                    incomplete: !profile.is_profile_completed
                }"
            >

                {{ profileStatus }}

            </strong>

        </div>

    </div>

</div>

</template>

<style scoped>

.card{

background:#fff;

border-radius:22px;

padding:32px;

margin-bottom:30px;

box-shadow:0 10px 30px rgba(15,23,42,.08);

}

.header{

display:flex;

justify-content:space-between;

align-items:center;

margin-bottom:30px;

}

.left{

display:flex;

align-items:center;

gap:22px;

}

.avatar{

width:84px;

height:84px;

border-radius:50%;

display:flex;

align-items:center;

justify-content:center;

background:linear-gradient(135deg,#2563eb,#38bdf8);

font-size:34px;

font-weight:700;

color:#fff;

flex-shrink:0;

}

.left h2{

margin:0;

font-size:30px;

font-weight:700;

color:#0f172a;

}

.left p{

margin-top:8px;

font-size:15px;

color:#64748b;

}

.edit{

background:#2563eb;

color:#fff;

border:none;

padding:12px 22px;

border-radius:12px;

cursor:pointer;

font-weight:600;

transition:.25s;

}

.edit:hover{

transform:translateY(-2px);

box-shadow:0 10px 20px rgba(37,99,235,.25);

}

.grid{

display:grid;

grid-template-columns:repeat(4,1fr);

gap:20px;

}

.item{

background:#f8fafc;

border:1px solid #e2e8f0;

padding:20px;

border-radius:16px;

display:flex;

flex-direction:column;

gap:8px;

}

.item span{

font-size:13px;

color:#64748b;

}

.item strong{

font-size:17px;

font-weight:700;

color:#0f172a;

}

@media (max-width:900px){

.header{

flex-direction:column;

align-items:flex-start;

gap:20px;

}

.grid{

grid-template-columns:1fr;

}

}

</style>