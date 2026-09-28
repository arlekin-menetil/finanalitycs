<template>
  <router-view />
</template>

<script setup>
// Инициализация приложения выполняется в main.js
// Здесь ничего вызывать не нужно.
</script>

<style>
/* RESET */
html,
body {
  margin: 0;
  padding: 0;
  background: #f4f6f9;
  font-family: Inter, system-ui, -apple-system, sans-serif;
}

/* ROOT */
#app {
  min-height: 100vh;
}

/* GLOBAL */
* {
  box-sizing: border-box;
}

/* SCROLL */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}
</style>