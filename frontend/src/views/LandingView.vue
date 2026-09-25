<script setup>
import AppHeader from "@/components/landing/layout/AppHeader.vue"
import AppFooter from "@/components/landing/layout/AppFooter.vue"

import HeroSection from "@/components/landing/sections/HeroSection.vue"
import StatsSection from "@/components/landing/sections/StatsSection.vue"
import DataSection from "@/components/landing/sections/DataSection.vue"
import BenefitsSection from "@/components/landing/sections/BenefitsSection.vue"
import MobileAppsSection from "@/components/landing/sections/MobileAppsSection.vue"
import ConverterSection from "@/components/landing/sections/ConverterSection.vue"
</script>

<template>

  <div class="landing">

    <!-- HEADER -->

    <AppHeader />


    <!-- HERO -->

    <HeroSection />


    <!-- STATS -->

    <StatsSection />


    <!-- INTEGRATIONS -->

    <div
      id="integrations"
      class="landing__anchor"
    >
      <DataSection />
    </div>


    <!-- MONITORING -->

    <div
      id="monitoring"
      class="landing__anchor"
    >
      <BenefitsSection />
    </div>


    <!-- MOBILE APPS -->

    <div
      id="mobile-apps"
      class="landing__anchor"
    >
      <MobileAppsSection />
    </div>


    <!-- CURRENCY -->

    <div
      id="currency"
      class="landing__anchor"
    >
      <ConverterSection />
    </div>


    <!-- FOOTER -->

    <AppFooter />

  </div>

</template>

<style scoped>

.landing {
  width: 100%;
}


/*
 * Отступ при переходе по якорю.
 *
 * Header находится сверху,
 * поэтому секция не должна
 * упираться прямо в него.
 */

.landing__anchor {
  scroll-margin-top: 90px;
}


/*
 * Плавный переход
 * при клике по #anchor.
 */

:global(html) {
  scroll-behavior: smooth;
}

</style>