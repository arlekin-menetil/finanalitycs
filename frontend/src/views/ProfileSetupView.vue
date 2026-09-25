<script setup>

import {
    ref,
    onMounted,
} from "vue"

import api from "@/api/axios"

import ProfileEditForm from "@/components/profile/ProfileEditForm.vue"
import EmploymentVerificationCard from "@/components/profile/EmploymentVerificationCard.vue"

const profile = ref(null)

const loading = ref(true)

async function loadProfile(){

    loading.value = true

    try{

        const { data } = await api.get("/profile/")

        profile.value = data

    }

    catch(e){

        console.error(e)

    }

    finally{

        loading.value = false

    }

}

onMounted(loadProfile)

</script>

<template>

<div class="profile-setup-page">

    <div class="page-header">

        <h1>

            👤 Редактирование профиля

        </h1>

        <p>

            Здесь можно изменить персональные данные и сведения о работе.

        </p>

    </div>

    <div
        v-if="loading"
        class="loading"
    >

        Загрузка профиля...

    </div>

    <template v-else>

        <ProfileEditForm

            :profile="profile"

            @saved="loadProfile"

        />

        <EmploymentVerificationCard

            v-if="profile"

            :profile="profile"

            @uploaded="loadProfile"

        />

    </template>

</div>

</template>

<style scoped>

.profile-setup-page{

max-width:1200px;

margin:auto;

padding:30px;

}

.page-header{

margin-bottom:30px;

}

.page-header h1{

margin:0;

font-size:34px;

font-weight:700;

color:#0f172a;

}

.page-header p{

margin-top:8px;

color:#64748b;

font-size:15px;

}

.loading{

padding:80px;

text-align:center;

font-size:20px;

font-weight:600;

color:#2563eb;

}

</style>