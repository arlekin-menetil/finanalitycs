<script setup>

import {
  onMounted,
  ref,
  nextTick,
  onBeforeUnmount,
} from "vue"

import { useRoute } from "vue-router"
import { useI18n } from "vue-i18n"

import api from "@/api/axios"


// ==========================================
// 🔥 YANDEX MAPS
// ==========================================
const ymapsRef = ref(null)

const map = ref(null)

const placemarks = ref([])

let mapDestroyed = false


// ==========================================
// 🔥 ROUTE / I18N
// ==========================================
const { t } = useI18n()

const route = useRoute()


// ==========================================
// 🔥 STATE
// ==========================================
const bankName = ref("")

const branches = ref([])

const activeBranch = ref(null)

const loading = ref(true)

const error = ref(false)


// ==========================================
// 🔥 WAIT YANDEX
// ==========================================
function waitForYandex(){

  return new Promise((resolve) => {

    const check = () => {

      if (
        window.ymaps
        && window.ymaps.Map
      ) {

        resolve()

      } else {

        setTimeout(check, 200)
      }
    }

    check()
  })
}


// ==========================================
// 🔥 TRANSLATE
// ==========================================
function translateBranchName(name){

  if (!name) {
    return t("branches.branch")
  }

  return name.replace(
    "Branch",
    t("branches.branch")
  )
}


// ==========================================
// 🔥 SAFE DESTROY
// ==========================================
function destroyMap(){

  try {

    if (map.value) {

      map.value.geoObjects.removeAll()

      map.value.destroy()

      map.value = null
    }

  } catch(err){

    console.warn(
      "Map destroy error:",
      err
    )
  }
}


// ==========================================
// 🔥 LOAD
// ==========================================
async function loadBranches(){

  loading.value = true

  error.value = false

  try {

    const bankId =
      route.params.id

    const res = await api.get(
      `/banks/${bankId}/branches/`
    )

    const data =
      res.data || {}

    bankName.value =
      data.bank
      || "Банк"

    // ==========================================
    // 🔥 NORMALIZE + FILTER
    // ==========================================
    branches.value = (
      data.branches
      || []
    )
    .map((branch, index) => ({

      id:
        Number(branch.id || index),

      name:
        String(
          branch.name
          || "Филиал"
        ),

      address:
        String(
          branch.address
          || ""
        ),

      city:
        branch.city
        || null,

      phone:
        branch.phone
        || null,

      working_hours:
        branch.working_hours
        || null,

      lat:
        Number(
          branch.lat
          || branch.latitude
        ),

      lng:
        Number(
          branch.lng
          || branch.longitude
        ),
    }))

    .filter(branch => (

      typeof branch.lat === "number"
      && typeof branch.lng === "number"

      && !isNaN(branch.lat)
      && !isNaN(branch.lng)

      && isFinite(branch.lat)
      && isFinite(branch.lng)

      && branch.lat !== 0
      && branch.lng !== 0

    ))

    await nextTick()

    await waitForYandex()

    if (mapDestroyed) {
      return
    }

    window.ymaps.ready(async () => {

      if (mapDestroyed) {
        return
      }

      await initMap()
    })

  } catch(e){

    console.error(
      "Branches load error:",
      e
    )

    error.value = true

  } finally {

    loading.value = false
  }
}


// ==========================================
// 🔥 INIT MAP
// ==========================================
async function initMap(){

  if (!ymapsRef.value) {
    return
  }

  // ==========================================
  // 🔥 DESTROY OLD
  // ==========================================
  destroyMap()

  // ==========================================
  // 🔥 CREATE MAP
  // ==========================================
  map.value = new window.ymaps.Map(
    ymapsRef.value,
    {
      center: [
        41.3111,
        69.2797
      ],

      zoom: 11,

      controls: [
        "zoomControl"
      ]
    },
    {
      suppressMapOpenBlock: true
    }
  )

  placemarks.value = []

  // ==========================================
  // 🔥 NO BRANCHES
  // ==========================================
  if (!branches.value.length) {

    console.warn(
      "No valid branches with coordinates"
    )

    return
  }

  // ==========================================
  // 🔥 REMOVE VUE PROXY
  // ==========================================
  const plainBranches =
    JSON.parse(
      JSON.stringify(branches.value)
    )

  // ==========================================
  // 🔥 MARKERS
  // ==========================================
  for (const branch of plainBranches) {

    if (mapDestroyed) {
      return
    }

    try {

      // ==========================================
      // 🔥 SAFE COORDS
      // ==========================================
      const coords = [

        Number(branch.lat),

        Number(branch.lng)
      ]

      // ==========================================
      // 🔥 VALIDATE
      // ==========================================
      if (

        !Array.isArray(coords)
        || coords.length < 2

        || isNaN(coords[0])
        || isNaN(coords[1])

      ) {

        console.warn(
          "Invalid coords:",
          branch
        )

        continue
      }

      // ==========================================
      // 🔥 SIMPLE PLACEMARK
      // ==========================================
      const placemark =
        new window.ymaps.Placemark(
          coords,
          {}
        )

      placemark.branchId =
        branch.id

      // ==========================================
      // 🔥 SAVE
      // ==========================================
      placemarks.value = [
        ...placemarks.value,
        placemark
      ]

      // ==========================================
      // 🔥 ADD TO MAP
      // ==========================================
      map.value.geoObjects.add(
        placemark
      )

    } catch(err){

      console.error(
        "Placemark error:",
        branch,
        err
      )
    }
  }

  // ==========================================
  // 🔥 AUTO CENTER
  // ==========================================
  if (placemarks.value.length) {

    try {

      const first =
        placemarks.value[0]

      const coords =
        first
          ?.geometry
          ?.getCoordinates?.()

      if (
        coords
        && Array.isArray(coords)
      ) {

        map.value.setCenter(
          coords
        )
      }

    } catch(err){

      console.warn(
        "Center error:",
        err
      )
    }
  }
}


// ==========================================
// 🔥 FOCUS
// ==========================================
function focusBranch(branch){

  activeBranch.value =
    branch.id

  if (
    !map.value
    || !branch.lat
    || !branch.lng
  ) {
    return
  }

  try {

    map.value.setCenter([
      Number(branch.lat),
      Number(branch.lng)
    ])

  } catch(err){

    console.warn(
      "Focus error:",
      err
    )
  }
}


// ==========================================
// 🔥 INIT
// ==========================================
onMounted(() => {

  mapDestroyed = false

  loadBranches()
})


// ==========================================
// 🔥 CLEANUP
// ==========================================
onBeforeUnmount(() => {

  mapDestroyed = true

  destroyMap()
})

</script>


<template>

<div class="branches-page">

  <!-- ==========================================
  🔥 TITLE
  =========================================== -->
  <h1 class="title">

    🏦

    {{ bankName }}

    —

    {{ t("branches.title") }}

  </h1>


  <!-- ==========================================
  🔥 STATES
  =========================================== -->
  <div
    v-if="loading"
    class="state"
  >
    Загрузка филиалов...
  </div>

  <div
    v-else-if="error"
    class="state error"
  >
    Ошибка загрузки филиалов
  </div>


  <!-- ==========================================
  🔥 CONTENT
  =========================================== -->
  <div
    v-else
    class="layout"
  >

    <!-- ==========================================
    🔥 LIST
    =========================================== -->
    <div class="list">

      <div
        v-for="branch in branches"
        :key="branch.id"
        class="branch-card"
        :class="{
          active:
            activeBranch === branch.id
        }"
        @click="focusBranch(branch)"
      >

        <h3>
          {{
            translateBranchName(
              branch.name
            )
          }}
        </h3>

        <p class="address">
          📍
          {{
            branch.address
            || "-"
          }}
        </p>

        <p
          v-if="branch.working_hours"
          class="hours"
        >
          🕒
          {{ branch.working_hours }}
        </p>

        <p
          v-if="branch.phone"
          class="phone"
        >
          📞
          {{ branch.phone }}
        </p>

      </div>

    </div>


    <!-- ==========================================
    🔥 MAP
    =========================================== -->
    <div
      ref="ymapsRef"
      class="map"
    ></div>

  </div>

</div>

</template>


<style scoped>

.branches-page{

  max-width:1400px;

  margin:auto;

  padding:30px;
}


.title{

  font-size:30px;

  font-weight:800;

  margin-bottom:24px;

  color:#111827;
}


.layout{

  display:grid;

  grid-template-columns:
    340px
    1fr;

  gap:20px;
}


/* ==========================================
🔥 MAP
========================================== */

.map{

  width:100%;

  height:620px;

  border-radius:20px;

  overflow:hidden;

  border:1px solid #e5e7eb;

  background:#fff;

  box-shadow:
    0 10px 30px rgba(0,0,0,0.06);
}


/* ==========================================
🔥 LIST
========================================== */

.list{

  overflow-y:auto;

  max-height:620px;

  padding-right:6px;
}


/* ==========================================
🔥 CARD
========================================== */

.branch-card{

  background:#f9fafb;

  padding:18px;

  border-radius:18px;

  margin-bottom:14px;

  cursor:pointer;

  transition:all .2s ease;

  border:1px solid #e5e7eb;
}


.branch-card:hover{

  background:#ffffff;

  transform:translateY(-2px);

  border-color:#bfdbfe;

  box-shadow:
    0 8px 20px rgba(37,99,235,0.08);
}


/* ==========================================
🔥 ACTIVE
========================================== */

.branch-card.active{

  background:#eff6ff;

  border-color:#3b82f6;
}


/* ==========================================
🔥 TEXT
========================================== */

.branch-card h3{

  font-size:16px;

  font-weight:700;

  margin-bottom:10px;

  color:#111827;
}


.address{

  font-size:14px;

  line-height:1.6;

  color:#374151;

  margin-bottom:8px;
}


.hours{

  font-size:13px;

  color:#6b7280;

  margin-bottom:6px;
}


.phone{

  font-size:13px;

  color:#2563eb;
}


/* ==========================================
🔥 STATES
========================================== */

.state{

  text-align:center;

  padding:60px;

  font-size:15px;
}


.error{

  color:#ef4444;
}


/* ==========================================
🔥 MOBILE
========================================== */

@media (max-width:960px){

  .layout{

    grid-template-columns:1fr;
  }

  .list{

    max-height:360px;
  }

  .map{

    height:500px;
  }
}


@media (max-width:768px){

  .branches-page{

    padding:20px;
  }

  .title{

    font-size:24px;
  }

  .map{

    height:420px;
  }
}

</style>