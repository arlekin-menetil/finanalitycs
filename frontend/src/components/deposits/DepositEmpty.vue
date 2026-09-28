<script setup>

import { computed } from "vue"
import { useI18n } from "vue-i18n"

const { t } = useI18n()

const props = defineProps({

  title: {
    type: String,
    default: "",
  },

  description: {
    type: String,
    default: "",
  },

})

const titleText = computed(() => {

  return (
    props.title ||
    t("deposits.empty.title")
  )

})

const descriptionText = computed(() => {

  return (
    props.description ||
    t("deposits.empty.description")
  )

})

</script>

<template>

  <div class="empty-state">

    <div class="icon">
      🏦
    </div>

    <h2>
      {{ titleText }}
    </h2>

    <p>
      {{ descriptionText }}
    </p>

  </div>

</template>

<style scoped>

.empty-state {

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  text-align: center;

  padding: 80px 24px;

  border-radius: 24px;

  background: white;

  border: 1px solid #e2e8f0;

}

.icon {

  width: 96px;
  height: 96px;

  display: flex;
  align-items: center;
  justify-content: center;

  font-size: 48px;

  border-radius: 50%;

  background: #eff6ff;

  margin-bottom: 24px;

}

h2 {

  margin: 0 0 12px;

  font-size: 24px;
  font-weight: 700;

  color: #0f172a;

}

p {

  margin: 0;

  max-width: 480px;

  color: #64748b;

  line-height: 1.6;

}

@media (max-width: 768px) {

  .empty-state {

    padding: 60px 20px;

  }

  .icon {

    width: 80px;
    height: 80px;

    font-size: 40px;

  }

  h2 {

    font-size: 20px;

  }

}

</style>