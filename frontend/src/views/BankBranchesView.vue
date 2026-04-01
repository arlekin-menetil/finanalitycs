<script setup>

import { onMounted, ref, nextTick } from "vue"
import { useRoute } from "vue-router"
import { useI18n } from "vue-i18n"
import api from "@/api/axios"

import L from "leaflet"
import "leaflet/dist/leaflet.css"

// 💣 FIX ICONS (ВАЖНО ДЛЯ ПРОДА)
import markerIcon from "leaflet/dist/images/marker-icon.png"
import markerShadow from "leaflet/dist/images/marker-shadow.png"

delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
})

const { t } = useI18n()
const route = useRoute()

const bankName = ref("")
const branches = ref([])
const map = ref(null)
const markers = ref([])
const activeBranch = ref(null)


// ==========================================
// 🧠 TRANSLATE
// ==========================================
function translateBranchName(name){
  if(!name) return ""
  return name.replace("Branch", t("branches.branch"))
}


// ==========================================
// 🚀 LOAD
// ==========================================
async function loadBranches(){

  try{

    const bankId = route.params.id

    const res = await api.get(`/banks/${bankId}/branches/`)
    const data = res.data

    bankName.value = data.bank || "Банк"
    branches.value = data.branches || []

    await nextTick()
    initMap()

  }catch(e){

    console.error("Branches load error:", e)

  }

}


// ==========================================
// 🗺 INIT MAP
// ==========================================
function initMap(){

  if(!branches.value.length) return

  // 💣 RESET
  markers.value = []

  if(map.value){
    map.value.remove()
  }

  map.value = L.map("map")

  L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    { maxZoom:19 }
  ).addTo(map.value)

  const bounds=[]

  branches.value.forEach(branch=>{

    if(!branch.lat || !branch.lng) return

    const marker = L.marker([branch.lat, branch.lng])
      .addTo(map.value)
      .bindPopup(`
        <b>${bankName.value}</b><br>
        ${translateBranchName(branch.name)}<br>
        📍 ${branch.address || "-"}<br>
        🕒 ${branch.working_hours || "09:00 - 18:00"}<br>
        ${branch.phone ? "📞 " + branch.phone : ""}
      `)

    markers.value.push({
      id: branch.id,
      marker
    })

    bounds.push([branch.lat, branch.lng])

  })

  if(bounds.length){
    map.value.fitBounds(bounds, { padding:[40,40] })
  }

}


// ==========================================
// 🎯 FOCUS
// ==========================================
function focusBranch(branch){

  activeBranch.value = branch.id

  if(!map.value || !branch.lat) return

  map.value.setView(
    [branch.lat, branch.lng],
    16,
    { animate:true }
  )

  const found = markers.value.find(m => m.id === branch.id)

  if(found){
    found.marker.openPopup()
  }

}

onMounted(()=>{
  loadBranches()
})

</script>


<template>

<div class="branches-page">

<h1 class="title">
🏦 {{ bankName }} — {{ t("branches.title") }}
</h1>

<div class="layout">

<!-- LIST -->
<div class="list">

<div
v-for="branch in branches"
:key="branch.id"
class="branch-card"
:class="{ active: activeBranch === branch.id }"
@click="focusBranch(branch)"
>

<h3>
{{ translateBranchName(branch.name) }}
</h3>

<p class="address">
📍 {{ branch.address || "-" }}
</p>

<p v-if="branch.working_hours" class="hours">
🕒 {{ branch.working_hours }}
</p>

<p v-if="branch.phone" class="phone">
📞 {{ branch.phone }}
</p>

</div>

</div>

<!-- MAP -->
<div id="map" class="map"></div>

</div>

</div>

</template>


<style scoped>

.branches-page{
max-width:1200px;
margin:auto;
padding:30px;
}

.title{
font-size:28px;
font-weight:700;
margin-bottom:20px;
}

.layout{
display:grid;
grid-template-columns:320px 1fr;
gap:20px;
}

/* MAP */

.map{
height:520px;
width:100%;
border-radius:14px;
overflow:hidden;
}

/* LIST */

.list{
overflow-y:auto;
max-height:520px;
}

/* CARD */

.branch-card{
background:#f3f4f6;
padding:16px;
border-radius:12px;
margin-bottom:12px;
cursor:pointer;
transition:.25s;
border:1px solid #e5e7eb;
}

.branch-card:hover{
background:#ffffff;
transform:translateY(-2px);
box-shadow:0 6px 16px rgba(0,0,0,0.08);
}

/* 💣 ACTIVE */

.branch-card.active{
background:#e0f2fe;
border-color:#3b82f6;
}

/* TEXT */

.address{
font-size:14px;
margin-top:6px;
color:#374151;
}

.hours{
font-size:13px;
margin-top:4px;
color:#6b7280;
}

.phone{
font-size:13px;
margin-top:4px;
color:#2563eb;
}

/* MOBILE */

@media (max-width:900px){

.layout{
grid-template-columns:1fr;
}

.list{
max-height:none;
}

.map{
height:420px;
}

}

</style>