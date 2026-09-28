<script setup>

import { computed } from "vue"
import { useI18n } from "vue-i18n"
import { useRouter } from "vue-router"

const { t, locale } = useI18n()
const router = useRouter()

// ==========================================
// PROFILE
// ==========================================

const goToProfile = () => {
  router.push("/app/profile")
}

// ==========================================
// LANGUAGE
// ==========================================

const changeLang = (lang) => {

  locale.value = lang

  localStorage.setItem(
    "lang",
    lang
  )

}

// ==========================================
// LANDING
// ==========================================

const isLanding = computed(() => {

  return (
    router.currentRoute.value.path === "/"
  )

})

// ==========================================
// SCROLL
// ==========================================

const scrollToSection = (id) => {

  if (!isLanding.value) {

    router.push("/")

    setTimeout(() => {

      const element =
        document.getElementById(id)

      if (element) {

        element.scrollIntoView({

          behavior: "smooth",
          block: "start"

        })

      }

    }, 300)

    return

  }

  const element =
    document.getElementById(id)

  if (!element) {
    return
  }

  element.scrollIntoView({

    behavior: "smooth",
    block: "start"

  })

}

// ==========================================
// NAVIGATION TEXT
// ==========================================

const navText = (
  key,
  fallback
) => {

  const value = t(key)

  return value === key
    ? fallback
    : value

}

</script>


<template>

<header class="header">

  <!-- ==========================================
       LOGO
  =========================================== -->

  <div
    class="logo"
    @click="router.push('/')"
  >

    <img
      src="/logo.png"
      alt="FinAnalytics"
      class="logo__image"
    />

  </div>

  <!-- ==========================================
       NAVIGATION
  =========================================== -->

  <nav
    v-if="isLanding"
    class="navigation"
  >

    <button
      class="navigation__item"
      type="button"
      @click="scrollToSection('integrations')"
    >
      {{ t("landingNav.integrations") }}
    </button>

    <button
      class="navigation__item"
      type="button"
      @click="scrollToSection('monitoring')"
    >
      {{ t("landingNav.monitoring") }}
    </button>

    <button
      class="navigation__item"
      type="button"
      @click="scrollToSection('mobile-apps')"
    >
      {{ t("landingNav.mobile") }}
    </button>

    <button
      class="navigation__item"
      type="button"
      @click="scrollToSection('currency')"
    >
      {{ t("landingNav.currency") }}
    </button>

  </nav>

  <!-- ==========================================
       RIGHT SIDE
  =========================================== -->

  <div class="header-right">

    <!-- LANGUAGE -->

    <div class="langs">

      <button
        class="lang"
        :class="{ active: locale === 'ru' }"
        type="button"
        @click="changeLang('ru')"
      >
        🇷🇺
      </button>

      <button
        class="lang"
        :class="{ active: locale === 'en' }"
        type="button"
        @click="changeLang('en')"
      >
        🇬🇧
      </button>

      <button
        class="lang"
        :class="{ active: locale === 'uz' }"
        type="button"
        @click="changeLang('uz')"
      >
        🇺🇿
      </button>

    </div>

    <!-- PROFILE -->

    <button
      class="profile-btn"
      type="button"
      @click="goToProfile"
    >

      <span class="profile-btn__icon">
        👤
      </span>

      {{ t("common.profile") }}

    </button>

  </div>

</header>

</template>

<style scoped>

/* ==========================================
   HEADER
========================================== */

.header {

  position:
    relative;

  z-index:
    100;

  width:
    100%;

  min-height:
    72px;

  padding:
    10px 40px;

  background:
    rgba(
      255,
      255,
      255,
      0.97
    );

  border-bottom:
    1px solid
    #e2e8f0;

  border-radius:
    0 0 16px 16px;

  box-sizing:
    border-box;

  display:
    flex;

  align-items:
    center;

  justify-content:
    space-between;

  gap:
    25px;

}


/* ==========================================
   LOGO
========================================== */

.logo {

  flex-shrink:
    0;

  width:
    190px;

  cursor:
    pointer;

  display:
    flex;

  align-items:
    center;

  transition:
    opacity 0.2s ease,
    transform 0.2s ease;

}


.logo:hover {

  opacity:
    0.88;

  transform:
    translateY(
      -1px
    );

}


.logo__image {

  display:
    block;

  width:
    100%;

  max-width:
    190px;

  height:
    auto;

  max-height:
    52px;

  object-fit:
    contain;

  object-position:
    left center;

}


/* ==========================================
   NAVIGATION
========================================== */

.navigation {

  display:
    flex;

  align-items:
    center;

  justify-content:
    center;

  gap:
    4px;

  flex:
    1;

}


.navigation__item {

  border:
    none;

  background:
    transparent;

  padding:
    9px 12px;

  border-radius:
    9px;

  color:
    #475569;

  font-size:
    12px;

  font-weight:
    600;

  cursor:
    pointer;

  white-space:
    nowrap;

  transition:
    background 0.2s ease,
    color 0.2s ease;

}


.navigation__item:hover {

  background:
    #f1f5f9;

  color:
    #2563eb;

}


/* ==========================================
   RIGHT
========================================== */

.header-right {

  display:
    flex;

  align-items:
    center;

  gap:
    12px;

  flex-shrink:
    0;

}


/* ==========================================
   LANGUAGES
========================================== */

.langs {

  display:
    flex;

  align-items:
    center;

  gap:
    2px;

  padding:
    3px;

  background:
    #f1f5f9;

  border:
    1px solid
    #e2e8f0;

  border-radius:
    10px;

}


.lang {

  width:
    30px;

  height:
    28px;

  padding:
    0;

  border:
    none;

  border-radius:
    7px;

  background:
    transparent;

  cursor:
    pointer;

  display:
    flex;

  align-items:
    center;

  justify-content:
    center;

  font-size:
    15px;

  transition:
    background 0.2s ease,
    transform 0.2s ease;

}


.lang:hover {

  background:
    #ffffff;

  transform:
    scale(1.05);

}


.lang.active {

  background:
    #ffffff;

  box-shadow:
    0 1px 4px
    rgba(
      15,
      23,
      42,
      0.08
    );

}


/* ==========================================
   PROFILE
========================================== */

.profile-btn {

  display:
    flex;

  align-items:
    center;

  gap:
    6px;

  background:
    linear-gradient(
      135deg,
      #2563eb,
      #38bdf8
    );

  color:
    #ffffff;

  border:
    none;

  padding:
    9px 16px;

  border-radius:
    18px;

  font-size:
    12px;

  font-weight:
    600;

  cursor:
    pointer;

  white-space:
    nowrap;

  transition:
    transform 0.25s ease,
    box-shadow 0.25s ease;

}


.profile-btn:hover {

  transform:
    translateY(
      -1px
    );

  box-shadow:
    0 8px 20px
    rgba(
      37,
      99,
      235,
      0.25
    );

}


/* ==========================================
   TABLET
========================================== */

@media (max-width: 1050px) {

  .header {

    padding:
      10px 24px;

  }


  .logo {

    width:
      160px;

  }


  .logo__image {

    max-width:
      160px;

  }


  .navigation__item {

    padding:
      8px 8px;

    font-size:
      11px;

  }

}


/* ==========================================
   MOBILE
========================================== */

@media (max-width: 768px) {

  .header {

    min-height:
      64px;

    padding:
      8px 14px;

    gap:
      10px;

  }


  .logo {

    width:
      135px;

  }


  .logo__image {

    max-width:
      135px;

    max-height:
      42px;

  }


  /*
   * Навигацию скрываем на мобильном,
   * чтобы Header оставался компактным.
   */

  .navigation {

    display:
      none;

  }


  .header-right {

    gap:
      6px;

  }


  .langs {

    padding:
      2px;

  }


  .lang {

    width:
      27px;

    height:
      26px;

    font-size:
      13px;

  }


  .profile-btn {

    padding:
      8px 11px;

    font-size:
      11px;

  }

}


/* ==========================================
   SMALL MOBILE
========================================== */

@media (max-width: 430px) {

  .logo {

    width:
      110px;

  }


  .logo__image {

    max-width:
      110px;

    max-height:
      36px;

  }


  .profile-btn {

    padding:
      8px 10px;

  }


  .profile-btn__icon {

    display:
      none;

  }

}

</style>