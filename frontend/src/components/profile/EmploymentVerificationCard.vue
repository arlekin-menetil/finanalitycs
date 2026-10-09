<script setup>

import {
  computed,
  ref,
} from "vue"

import {
  useI18n,
} from "vue-i18n"

import api from "@/api/axios"


const {
  t,
} = useI18n()


const props = defineProps({

  profile: {
    type: Object,
    required: true,
  },

})


const emit = defineEmits([
  "uploaded",
])


const loading = ref(false)

const dragOver = ref(false)


// =====================================
// DOCUMENT
// =====================================

const hasDocument = computed(() => {

  return !!props.profile?.employment_document

})


const verified = computed(() => {

  return !!props.profile?.employment_verified

})


// =====================================
// EXPERIENCE
// =====================================

const experience = computed(() => {

  const total = Number(
    props.profile?.work_experience_months || 0,
  )

  if (!total) {
    return t("employmentVerification.values.empty")
  }

  const years = Math.floor(total / 12)

  const months = total % 12

  const parts = []

  if (years) {

    parts.push(
      `${years} ${t("employmentVerification.values.years")}`,
    )

  }

  if (months) {

    parts.push(
      `${months} ${t("employmentVerification.values.months")}`,
    )

  }

  return parts.join(" ")

})


// =====================================
// MY.GOV
// =====================================

const myGovCareerUrl = new URL(
  "/ru/login?redirect=/ru/user/career&tab=0",
  "https://" + "my.gov.uz",
).toString()


// =====================================
// UPLOAD
// =====================================

async function upload(file) {

  if (!file) {
    return
  }


  if (file.type !== "application/pdf") {

    alert(
      t("employmentVerification.errors.pdfOnly"),
    )

    return
  }


  const formData = new FormData()

  formData.append(
    "file",
    file,
  )


  loading.value = true


  try {

    await api.post(
      "/profile/upload-employment/",
      formData,
      {
        headers: {
          "Content-Type":
            "multipart/form-data",
        },
      },
    )

    emit("uploaded")

  }


  catch (e) {

    console.error(e)

    alert(
      e.response?.data?.detail ||
      t(
        "employmentVerification.errors.upload",
      ),
    )

  }


  finally {

    loading.value = false

  }

}


// =====================================
// FILE
// =====================================

function onFile(e) {

  upload(
    e.target.files[0],
  )

}


// =====================================
// DROP
// =====================================

function onDrop(e) {

  e.preventDefault()

  dragOver.value = false

  upload(
    e.dataTransfer.files[0],
  )

}


// =====================================
// DRAG OVER
// =====================================

function onDragOver(e) {

  e.preventDefault()

  dragOver.value = true

}


// =====================================
// DRAG LEAVE
// =====================================

function onDragLeave() {

  dragOver.value = false

}

</script>


<template>

  <div class="employment-card">


    <!-- ===================================== -->
    <!-- HEADER -->
    <!-- ===================================== -->

    <div class="header">

      <div>

        <h2>
          💼 {{ t("employmentVerification.title") }}
        </h2>

        <p>
          {{ t("employmentVerification.description") }}
        </p>

      </div>


      <div
        class="badge"
        :class="{ success: verified }"
      >

        {{
          verified
            ? t("employmentVerification.status.verified")
            : t("employmentVerification.status.notVerified")
        }}

      </div>

    </div>


    <!-- ===================================== -->
    <!-- NO DOCUMENT -->
    <!-- ===================================== -->

<template v-if="!hasDocument">

  <div
    class="upload-zone"
    :class="{ active: dragOver }"
    @dragover.prevent="onDragOver"
    @dragleave="onDragLeave"
    @drop.prevent="onDrop"
  >

    <div class="upload-icon">
      📄
    </div>

    <h3>
      {{ t("employmentVerification.upload.title") }}
    </h3>

    <p>
      {{ t("employmentVerification.upload.description") }}
    </p>

    <div class="upload-actions">

      <!-- ПОЛУЧИТЬ СПРАВКУ -->

      <a
        class="get-document-btn"
        :href="myGovCareerUrl"
        target="_blank"
        rel="noopener noreferrer"
      >
        📄 {{ t("employmentVerification.actions.getDocument") }}
      </a>


      <!-- ЗАГРУЗИТЬ PDF -->

      <label class="upload-btn">

        📁 {{ t("employmentVerification.upload.choose") }}

        <input
          hidden
          type="file"
          accept=".pdf"
          @change="onFile"
        />

      </label>

    </div>


    <div
      v-if="loading"
      class="loading"
    >
      {{ t("employmentVerification.upload.checking") }}
    </div>

  </div>

</template>


    <!-- ===================================== -->
    <!-- DOCUMENT -->
    <!-- ===================================== -->

    <template v-else>

      <div class="employment-content">


        <!-- COMPANY -->

        <div class="main-info">

          <div class="company-avatar">
            🏢
          </div>


          <div class="company-data">

            <h3>
              {{
                profile.company_name ||
                t(
                  "employmentVerification.values.companyUnknown",
                )
              }}
            </h3>

            <p>
              {{
                profile.position ||
                t(
                  "employmentVerification.values.positionUnknown",
                )
              }}
            </p>

          </div>

        </div>


        <!-- DETAILS -->

        <div class="details">


          <!-- START DATE -->

          <div class="detail">

            <span>
              📅 {{ t("employmentVerification.details.startDate") }}
            </span>

            <strong>
              {{ profile.employment_start || "—" }}
            </strong>

          </div>


          <!-- EXPERIENCE -->

          <div class="detail">

            <span>
              ⏳ {{ t("employmentVerification.details.experience") }}
            </span>

            <strong>
              {{ experience }}
            </strong>

          </div>


          <!-- STATUS -->

          <div class="detail">

            <span>
              👨‍💼 {{ t("employmentVerification.details.status") }}
            </span>

            <strong>
              {{
                profile.is_current_employee
                  ? t(
                      "employmentVerification.values.working",
                    )
                  : t(
                      "employmentVerification.values.notWorking",
                    )
              }}
            </strong>

          </div>


          <!-- DEPARTMENT -->

          <div
            v-if="
              profile.department &&
              profile.department !== `Bo'linma mavjud emas`
            "
            class="detail"
          >

            <span>
              🏛 {{ t("employmentVerification.details.department") }}
            </span>

            <strong>
              {{ profile.department }}
            </strong>

          </div>

        </div>


        <!-- MORE -->

        <details class="more">

          <summary>
            {{ t("employmentVerification.more") }}
          </summary>


          <div class="more-grid">


            <!-- COMPANY INN -->

            <div>

              <span>
                {{ t("employmentVerification.additional.companyInn") }}
              </span>

              <strong>
                {{ profile.company_inn || "—" }}
              </strong>

            </div>


            <!-- PINFL -->

            <div>

              <span>
                {{ t("employmentVerification.additional.pinfl") }}
              </span>

              <strong>
                {{ profile.employment_pinfl || "—" }}
              </strong>

            </div>


          </div>

        </details>


        <!-- ACTIONS -->

        <div class="actions">


          <!-- GET DOCUMENT -->

          <a
            class="get-document-btn"
            :href="myGovCareerUrl"
            target="_blank"
            rel="noopener noreferrer"
          >

            📄 {{ t("employmentVerification.actions.getDocument") }}

          </a>


          <!-- REPLACE DOCUMENT -->

          <label class="replace-btn">

            🔄 {{ t("employmentVerification.actions.replace") }}

            <input
              hidden
              type="file"
              accept=".pdf"
              @change="onFile"
            />

          </label>


        </div>

      </div>

    </template>

  </div>

</template>


<style scoped>

.employment-card{

    background:#fff;

    border-radius:24px;

    padding:32px;

    margin-bottom:30px;

    box-shadow:0 12px 30px rgba(15,23,42,.08);

}


/* =====================================
   HEADER
===================================== */

.header{

    display:flex;

    justify-content:space-between;

    align-items:center;

    gap:20px;

    margin-bottom:30px;

}

.header h2{

    margin:0;

    font-size:28px;

    font-weight:700;

    color:#0f172a;

}

.header p{

    margin-top:6px;

    color:#64748b;

    font-size:14px;

}

.badge{

    padding:10px 18px;

    border-radius:999px;

    background:#f1f5f9;

    color:#475569;

    font-size:13px;

    font-weight:700;

}

.badge.success{

    background:#dcfce7;

    color:#15803d;

}


/* =====================================
   UPLOAD
===================================== */

.upload-zone{

    border:2px dashed #cbd5e1;

    border-radius:20px;

    padding:60px 30px;

    text-align:center;

    transition:.25s;

    background:#fafcff;

}

.upload-zone.active{

    border-color:#2563eb;

    background:#eff6ff;

}

.upload-icon{

    font-size:62px;

    margin-bottom:20px;

}

.upload-zone h3{

    margin:0;

    font-size:24px;

    font-weight:700;

    color:#0f172a;

}

.upload-zone p{

    margin:12px 0 28px;

    color:#64748b;

}

.upload-btn{

    display:inline-flex;

    align-items:center;

    justify-content:center;

    padding:14px 28px;

    background:#2563eb;

    color:#fff;

    border-radius:12px;

    cursor:pointer;

    font-weight:600;

    transition:.25s;

}

.upload-btn:hover{

    background:#1d4ed8;

    transform:translateY(-2px);

}

.loading{

    margin-top:24px;

    color:#2563eb;

    font-weight:600;

}


/* =====================================
   CONTENT
===================================== */

.employment-content{

    display:flex;

    flex-direction:column;

    gap:28px;

}


/* =====================================
   COMPANY
===================================== */

.main-info{

    display:flex;

    align-items:center;

    gap:20px;

    padding:24px;

    border:1px solid #e2e8f0;

    border-radius:18px;

    background:#f8fafc;

}

.company-avatar{

    width:72px;

    height:72px;

    border-radius:18px;

    background:linear-gradient(135deg,#2563eb,#38bdf8);

    display:flex;

    align-items:center;

    justify-content:center;

    font-size:34px;

    color:#fff;

    flex-shrink:0;

}

.company-data h3{

    margin:0;

    font-size:24px;

    font-weight:700;

    color:#0f172a;

}

.company-data p{

    margin-top:8px;

    color:#64748b;

    font-size:16px;

}


/* =====================================
   DETAILS
===================================== */

.details{

    display:grid;

    grid-template-columns:repeat(
        auto-fit,
        minmax(220px,1fr)
    );

    gap:18px;

}

.detail{

    background:#f8fafc;

    border:1px solid #e2e8f0;

    border-radius:16px;

    padding:18px;

    transition:.25s;

}

.detail:hover{

    transform:translateY(-2px);

    box-shadow:
        0 10px 20px
        rgba(15,23,42,.06);

}

.detail span{

    display:block;

    margin-bottom:8px;

    font-size:13px;

    color:#64748b;

}

.detail strong{

    font-size:17px;

    font-weight:700;

    color:#0f172a;

    word-break:break-word;

}


/* =====================================
   DETAILS PANEL
===================================== */

.more{

    border:1px solid #e2e8f0;

    border-radius:16px;

    overflow:hidden;

}

.more summary{

    cursor:pointer;

    padding:18px 22px;

    background:#f8fafc;

    font-weight:700;

    color:#0f172a;

    user-select:none;

}

.more-grid{

    display:grid;

    grid-template-columns:repeat(
        auto-fit,
        minmax(240px,1fr)
    );

    gap:18px;

    padding:22px;

}

.more-grid div{

    display:flex;

    flex-direction:column;

    gap:8px;

}

.more-grid span{

    font-size:13px;

    color:#64748b;

}

.more-grid strong{

    font-size:16px;

    font-weight:700;

    color:#0f172a;

    word-break:break-word;

}


/* =====================================
   BUTTONS
===================================== */

.actions{

    display:flex;

    justify-content:flex-end;

    align-items:center;

    gap:12px;

    flex-wrap:wrap;

}

.get-document-btn{

    display:inline-flex;

    align-items:center;

    justify-content:center;

    padding:14px 26px;

    background:#eff6ff;

    color:#2563eb;

    border:1px solid #bfdbfe;

    border-radius:12px;

    cursor:pointer;

    font-weight:600;

    text-decoration:none;

    transition:.25s;

}

.get-document-btn:hover{

    background:#dbeafe;

    border-color:#93c5fd;

    transform:translateY(-2px);

    box-shadow:
        0 10px 20px
        rgba(37,99,235,.12);

}

.replace-btn{

    display:inline-flex;

    align-items:center;

    justify-content:center;

    padding:14px 26px;

    background:#2563eb;

    color:#fff;

    border-radius:12px;

    cursor:pointer;

    font-weight:600;

    transition:.25s;

}

.replace-btn:hover{

    background:#1d4ed8;

    transform:translateY(-2px);

    box-shadow:
        0 12px 24px
        rgba(37,99,235,.25);

}


/* =====================================
   MOBILE
===================================== */

@media (max-width:900px){

    .header{

        flex-direction:column;

        align-items:flex-start;

    }

    .main-info{

        flex-direction:column;

        align-items:flex-start;

    }

    .company-avatar{

        width:64px;

        height:64px;

        font-size:30px;

    }

    .company-data h3{

        font-size:22px;

    }

    .details{

        grid-template-columns:1fr;

    }

    .more-grid{

        grid-template-columns:1fr;

    }

    .actions{

        justify-content:stretch;

    }

    .get-document-btn,
    .replace-btn{

        width:100%;

    }

}

</style>