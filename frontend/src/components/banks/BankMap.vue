<script setup>

import {
  onMounted,
  onBeforeUnmount,
  watch,
  nextTick,
} from "vue"

import { useRouter } from "vue-router"

// ==========================================
// 🔥 ROUTER
// ==========================================
const router = useRouter()


// ==========================================
// 🔥 PROPS
// ==========================================
const props = defineProps({

  points: {
    type: Array,
    default: () => []
  },

  height: {
    type: String,
    default: "760px"
  },

  autoFit: {
    type: Boolean,
    default: true
  },

  selectedBranchId: {
    type: [
      Number,
      String,
      null
    ],
    default: null
  }
})


// ==========================================
// 🔥 MAP STATE
// ==========================================
let map = null

let clusterer = null

let placemarks = new Map()

let initialized = false


// ==========================================
// 🔥 DEFAULT CENTER
// ==========================================
const DEFAULT_CENTER = [
  41.3111,
  69.2797
]

const DEFAULT_ZOOM = 11


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
// 🔥 INIT
// ==========================================
onMounted(async () => {

  await nextTick()

  await waitForYandex()

  window.ymaps.ready(() => {

    initMap()

    initialized = true
  })
})


// ==========================================
// 🔥 INIT MAP
// ==========================================
function initMap(){

  if (map) return

  map = new window.ymaps.Map(
    "bankMap",
    {
      center: DEFAULT_CENTER,

      zoom: DEFAULT_ZOOM,

      controls: [
        "zoomControl",
        "fullscreenControl"
      ]
    },
    {
      suppressMapOpenBlock: true
    }
  )

  // ==========================================
  // 🔥 CLUSTERER
  // ==========================================
  clusterer = new window.ymaps.Clusterer({

    preset: "islands#blueClusterIcons",

    groupByCoordinates: false,

    clusterDisableClickZoom: false,

    clusterHideIconOnBalloonOpen: false,

    geoObjectHideIconOnBalloonOpen: false,
  })

  map.geoObjects.add(clusterer)

  renderMarkers()
}


// ==========================================
// 🔥 WATCH POINTS
// ==========================================
watch(

  () => props.points,

  () => {

    if (!initialized) return

    renderMarkers()
  },

  {
    deep: true
  }
)


// ==========================================
// 🔥 WATCH SELECTED
// ==========================================
watch(

  () => props.selectedBranchId,

  (id) => {

    if (!id) return

    focusBranch(id)
  }
)


// ==========================================
// 🔥 RENDER MARKERS
// ==========================================
function renderMarkers(){

  if (!map || !clusterer) return

  clusterer.removeAll()

  placemarks.clear()

  const objects = []

  props.points.forEach((branch, index) => {

    try {

      const lat = Number(
        branch.lat
        || branch.latitude
      )

      const lng = Number(
        branch.lng
        || branch.longitude
      )

      if (
        !lat
        || !lng
        || isNaN(lat)
        || isNaN(lng)
      ) {
        return
      }

      const bankName =
        branch.bank
        || branch.bank_name
        || "Банк"

      const address =
        branch.address
        || "Адрес не указан"

      const city =
        branch.city
        || ""

      const phone =
        branch.phone
        || ""

      const placemark =
        new window.ymaps.Placemark(

          [lat, lng],

          {
            balloonContent: `
              <div class="ymap-popup">

                <div style="font-size:16px;font-weight:700;margin-bottom:8px;">
                  🏦 ${bankName}
                </div>

                ${
                  city
                  ? `
                    <div style="margin-bottom:8px;color:#2563eb;">
                      📍 ${city}
                    </div>
                  `
                  : ""
                }

                <div style="margin-bottom:10px;">
                  ${address}
                </div>

                ${
                  phone
                  ? `
                    <div style="color:#6b7280;">
                      ☎ ${phone}
                    </div>
                  `
                  : ""
                }

              </div>
            `,

            hintContent: bankName,
          },

          {
            preset: "islands#blueIcon",
          }
        )

      const key =
        branch.id
        || branch.branch_id
        || index

      placemarks.set(
        key,
        placemark
      )

      objects.push(placemark)

    } catch(err){

      console.error(
        "Yandex marker error:",
        err
      )
    }
  })

  clusterer.add(objects)

  // ==========================================
  // 🔥 AUTO FIT
  // ==========================================
  if (
    props.autoFit
    && objects.length
  ) {

    map.setBounds(
      clusterer.getBounds(),
      {
        checkZoomRange: true,

        zoomMargin: 40
      }
    )
  }
}


// ==========================================
// 🔥 FOCUS BRANCH
// ==========================================
function focusBranch(id){

  const placemark = placemarks.get(id)

  if (!placemark || !map) return

  const coords =
    placemark.geometry.getCoordinates()

  map.setCenter(
    coords,
    17,
    {
      duration: 300
    }
  )

  placemark.balloon.open()
}


// ==========================================
// 🔥 OPEN LOAN
// ==========================================
window.__openLoan = (id) => {

  router.push(
    `/app/loan/${id}`
  )
}


// ==========================================
// 🔥 CLEANUP
// ==========================================
onBeforeUnmount(() => {

  placemarks.clear()

  if (map) {

    map.destroy()

    map = null
  }
})

</script>


<template>

  <div
    class="map-wrapper"
    :style="{ height }"
  >

    <div id="bankMap"></div>

  </div>

</template>


<style scoped>

.map-wrapper{

  width:100%;

  height:100%;

  min-height:760px;

  border-radius:20px;

  overflow:hidden;

  border:1px solid #e5e7eb;

  background:#fff;

  position:relative;

  box-shadow:
    0 10px 30px rgba(0,0,0,0.06);
}


#bankMap{

  width:100%;

  height:100%;

  min-height:760px;
}


/* ==========================================
🔥 MOBILE
========================================== */

@media (max-width:768px){

  .map-wrapper{

    min-height:500px;

    border-radius:14px;
  }

  #bankMap{

    min-height:500px;
  }
}

</style>