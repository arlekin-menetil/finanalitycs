<script setup>
import { onMounted } from "vue"
import L from "leaflet"
import "leaflet/dist/leaflet.css"
import api from "@/api/axios"

let map

onMounted(async () => {

  // =========================
  // 🗺 карта
  // =========================
  map = L.map("bankMap").setView([41.3111, 69.2797], 12)

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap"
  }).addTo(map)

  // =========================
  // 💣 загрузка филиалов
  // =========================
  try {

    const res = await api.get("/banks/branches/map/")
    const branches = res.data

    branches.forEach(branch => {

      if (!branch.latitude || !branch.longitude) return

      const marker = L.marker([
        branch.latitude,
        branch.longitude
      ]).addTo(map)

      // =========================
      // 💬 popup
      // =========================
      marker.bindPopup(`
        <div style="font-size:14px">
          <b>${branch.bank_name}</b><br/>
          ${branch.address || "Адрес не указан"}<br/>
        </div>
      `)

    })

  } catch (e) {
    console.error("Ошибка загрузки карты", e)
  }

})
</script>


<template>
  <div class="map-wrapper">
    <div id="bankMap"></div>
  </div>
</template>


<style scoped>
.map-wrapper {
  width: 100%;
  height: 600px;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid #e5e5e5;
}

#bankMap {
  width: 100%;
  height: 100%;
}
</style>