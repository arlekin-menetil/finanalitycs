<script setup>
import { ref, computed } from "vue"
import { useI18n } from "vue-i18n"
import api from "@/api/axios"

const { t, locale } = useI18n()

const emit = defineEmits(["uploaded"])

const props = defineProps({
  creditReport: {
    type: Object,
    default: null,
  },

  contracts: {
    type: Array,
    default: () => [],
  },
})

// ==========================================
// STATE
// ==========================================

const file = ref(null)
const uploading = ref(false)
const message = ref("")
const error = ref("")
const isDragging = ref(false)

const fileInput = ref(null)

// ==========================================
// FORMAT NUMBER
// ==========================================

function formatNumber(value) {
  const localeMap = {
    ru: "ru-RU",
    en: "en-US",
    uz: "uz-UZ",
  }

  return Number(value || 0).toLocaleString(
    localeMap[locale.value] || "ru-RU",
    {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    },
  )
}

// ==========================================
// FILE HELPERS
// ==========================================

const fileExtension = computed(() => {
  if (!file.value?.name) {
    return ""
  }

  const parts = file.value.name.split(".")
  return parts.length > 1
    ? parts.pop().toLowerCase()
    : ""
})

const fileType = computed(() => {
  if (fileExtension.value === "pdf") {
    return "PDF"
  }

  if (
    fileExtension.value === "html" ||
    fileExtension.value === "htm"
  ) {
    return "HTML"
  }

  return "FILE"
})

const formattedFileSize = computed(() => {
  if (!file.value?.size) {
    return ""
  }

  const size = file.value.size

  if (size < 1024) {
    return `${size} B`
  }

  if (size < 1024 * 1024) {
    return `${(size / 1024).toFixed(1)} KB`
  }

  if (size < 1024 * 1024 * 1024) {
    return `${(size / (1024 * 1024)).toFixed(1)} MB`
  }

  return `${(size / (1024 * 1024 * 1024)).toFixed(1)} GB`
})

const fileIcon = computed(() => {
  if (fileType.value === "PDF") {
    return "PDF"
  }

  if (fileType.value === "HTML") {
    return "</>"
  }

  return "📄"
})

// ==========================================
// VALIDATION
// ==========================================

function isValidFile(selectedFile) {
  if (!selectedFile) {
    return false
  }

  const name = selectedFile.name?.toLowerCase() || ""

  return (
    name.endsWith(".pdf") ||
    name.endsWith(".html") ||
    name.endsWith(".htm")
  )
}

// ==========================================
// SET FILE
// ==========================================

function setFile(selectedFile) {
  if (!selectedFile) {
    return
  }

  message.value = ""
  error.value = ""

  if (!isValidFile(selectedFile)) {
    error.value = t(
      "creditReportUpload.errors.selectFile",
    )

    file.value = null

    return
  }

  file.value = selectedFile
}

// ==========================================
// FILE SELECT
// ==========================================

function selectFile(event) {
  const selectedFile =
    event.target.files?.[0] || null

  setFile(selectedFile)

  // Позволяет повторно выбрать тот же самый файл
  if (event.target) {
    event.target.value = ""
  }
}

// ==========================================
// OPEN FILE SELECTOR
// ==========================================

function openFileDialog() {
  if (uploading.value) {
    return
  }

  fileInput.value?.click()
}

// ==========================================
// DRAG & DROP
// ==========================================

function handleDragOver(event) {
  if (uploading.value) {
    return
  }

  event.preventDefault()
  isDragging.value = true
}

function handleDragLeave(event) {
  if (uploading.value) {
    return
  }

  event.preventDefault()

  // Не убираем состояние, если курсор
  // перешёл на дочерний элемент drop-zone
  if (
    event.currentTarget === event.target
  ) {
    isDragging.value = false
  }
}

function handleDrop(event) {
  if (uploading.value) {
    return
  }

  event.preventDefault()

  isDragging.value = false

  const droppedFile =
    event.dataTransfer?.files?.[0] || null

  setFile(droppedFile)
}

// ==========================================
// REMOVE FILE
// ==========================================

function removeFile() {
  if (uploading.value) {
    return
  }

  file.value = null
  message.value = ""
  error.value = ""
}

// ==========================================
// UPLOAD REPORT
// ==========================================

async function upload() {
  if (!file.value) {
    error.value = t(
      "creditReportUpload.errors.selectFile",
    )

    return
  }

  uploading.value = true
  message.value = ""
  error.value = ""

  const formData = new FormData()

  formData.append(
    "file",
    file.value,
  )

  try {
    await api.post(
      "/credit-analysis/upload/",
      formData,
      {
        headers: {
          "Content-Type":
            "multipart/form-data",
        },
      },
    )

    message.value = t(
      "creditReportUpload.success",
    )

    file.value = null

    emit("uploaded")
  } catch (e) {
    console.error(e)

    error.value =
      e.response?.data?.detail ||
      e.response?.data?.error ||
      t(
        "creditReportUpload.errors.uploadFailed",
      )
  } finally {
    uploading.value = false
  }
}
</script>

<template>
  <div class="card">

    <!-- ===================================== -->
    <!-- HEADER -->
    <!-- ===================================== -->

    <div class="header">
      <div class="header-content">
        <div class="header-icon">
          <span>📄</span>
        </div>

        <div>
          <h2>
            {{ t("creditReportUpload.title") }}
          </h2>

          <p>
            {{ t("creditReportUpload.description") }}
          </p>
        </div>
      </div>
    </div>

    <!-- ===================================== -->
    <!-- UPLOAD -->
    <!-- ===================================== -->

    <div class="upload-box">

      <!-- HIDDEN FILE INPUT -->

      <input
        ref="fileInput"
        class="hidden-file-input"
        type="file"
        accept=".html,.htm,.pdf"
        @change="selectFile"
      />

      <!-- ================================= -->
      <!-- DROP ZONE -->
      <!-- ================================= -->

      <div
        class="drop-zone"
        :class="{
          dragging: isDragging,
          'has-file': file,
          disabled: uploading,
        }"
        @click="openFileDialog"
        @dragover="handleDragOver"
        @dragleave="handleDragLeave"
        @drop="handleDrop"
      >

        <!-- EMPTY STATE -->

        <template v-if="!file">

          <div class="upload-icon-wrapper">
            <div class="upload-icon">
              <svg
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M12 16V4"
                  stroke="currentColor"
                  stroke-width="1.8"
                  stroke-linecap="round"
                />

                <path
                  d="M7.5 8.5L12 4L16.5 8.5"
                  stroke="currentColor"
                  stroke-width="1.8"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />

                <path
                  d="M5 20H19"
                  stroke="currentColor"
                  stroke-width="1.8"
                  stroke-linecap="round"
                />

                <path
                  d="M5 16.5V19C5 19.5523 5.44772 20 6 20H18C18.5523 20 19 19.5523 19 19V16.5"
                  stroke="currentColor"
                  stroke-width="1.8"
                  stroke-linecap="round"
                />
              </svg>
            </div>
          </div>

          <div class="drop-content">
            <h3>
              {{ t("creditReportUpload.uploadZone.title") }}
            </h3>

            <p class="drop-description">
              {{ t("creditReportUpload.uploadZone.description") }}

              <button
                type="button"
                class="browse-button"
                @click.stop="openFileDialog"
              >
                {{ t("creditReportUpload.uploadZone.choose") }}
              </button>
            </p>

            <div class="supported-files">
              <span class="format-badge pdf-badge">
                PDF
              </span>

              <span class="format-badge html-badge">
                HTML
              </span>

              <span class="format-text">
                {{ t("creditReportUpload.uploadZone.formats") }}
              </span>
            </div>
          </div>

        </template>

        <!-- SELECTED FILE -->

        <template v-else>

          <div class="selected-file">

            <div
              class="file-type-icon"
              :class="{
                pdf: fileType === 'PDF',
                html: fileType === 'HTML',
              }"
            >
              <span>
                {{ fileIcon }}
              </span>
            </div>

            <div class="selected-file-info">

              <div class="selected-file-name">
                {{ file.name }}
              </div>

              <div class="selected-file-meta">
                <span>
                  {{ fileType }}
                </span>

                <span class="meta-dot">
                  •
                </span>

                <span>
                  {{ formattedFileSize }}
                </span>
              </div>

            </div>

            <button
              type="button"
              class="remove-file-button"
              :disabled="uploading"
              :title="
                t(
                  'creditReportUpload.uploadZone.removeFile'
                )
              "
              @click.stop="removeFile"
            >
              <svg
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M6 6L18 18"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                />

                <path
                  d="M18 6L6 18"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                />
              </svg>
            </button>

          </div>

        </template>

      </div>

      <!-- ================================= -->
      <!-- CHANGE FILE -->
      <!-- ================================= -->

      <button
        v-if="file"
        type="button"
        class="change-file-button"
        :disabled="uploading"
        @click="openFileDialog"
      >
        <svg
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M12 20H21"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
          />

          <path
            d="M16.5 3.5C16.8978 3.10218 17.4374 2.87868 18 2.87868C18.5626 2.87868 19.1022 2.87868 19.5 3.5C19.8978 3.89782 20.1213 4.43739 20.1213 5C20.1213 5.56261 19.8978 6.10218 19.5 6.5L8 18L3 19L4 14L15.5 2.5C15.7652 2.23478 16.0804 2.02431 16.4271 1.88148C16.7738 1.73864 17.1451 1.66513 17.52 1.66513C17.8949 1.66513 18.2673 1.73864 18.614 1.88148C18.9607 1.7367 19.276 1.948 19.5412 2.5"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>

        {{ t("creditReportUpload.uploadZone.changeFile") }}
      </button>

      <!-- ================================= -->
      <!-- UPLOAD BUTTON -->
      <!-- ================================= -->

      <button
        class="upload-button"
        type="button"
        :disabled="uploading || !file"
        @click="upload"
      >

        <svg
          v-if="!uploading"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M12 16V4"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
          />

          <path
            d="M7.5 8.5L12 4L16.5 8.5"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
            stroke-linejoin="round"
          />

          <path
            d="M5 20H19"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
          />

          <path
            d="M5 16.5V19C5 19.5523 5.44772 20 6 20H18C18.5523 20 19 19.5523 19 19V16.5"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
          />
        </svg>

        <span
          v-if="uploading"
          class="spinner"
        ></span>

        <span>
          {{
            uploading
              ? t("creditReportUpload.buttons.uploading")
              : creditReport
                ? t("creditReportUpload.buttons.update")
                : t("creditReportUpload.buttons.upload")
          }}
        </span>

      </button>

    </div>

    <!-- ===================================== -->
    <!-- SUCCESS -->
    <!-- ===================================== -->

    <div
      v-if="message"
      class="alert success-alert"
    >
      <div class="alert-icon">
        ✓
      </div>

      <p>
        {{ message }}
      </p>
    </div>

    <!-- ===================================== -->
    <!-- ERROR -->
    <!-- ===================================== -->

    <div
      v-if="error"
      class="alert error-alert"
    >
      <div class="alert-icon">
        !
      </div>

      <p>
        {{ error }}
      </p>
    </div>

    <!-- ===================================== -->
    <!-- CONTRACTS -->
    <!-- ===================================== -->

    <div
      v-if="creditReport"
      class="report"
    >

      <div class="report-header">
        <div class="report-title-wrapper">

          <div class="report-icon">
            🏦
          </div>

          <div>
            <h3>
              {{ t("creditReportUpload.activeContracts") }}
            </h3>

            <span class="report-subtitle">
              {{ t("creditReportUpload.uploadZone.creditObligations") }}
            </span>
          </div>

        </div>

        <span class="count">
          {{ contracts.length }}
        </span>
      </div>

      <!-- ================================= -->
      <!-- TABLE -->
      <!-- ================================= -->

      <div class="table-wrapper">

        <table
          v-if="contracts.length"
          class="contracts"
        >

          <thead>
            <tr>

              <th>
                {{ t("creditReportUpload.table.bank") }}
              </th>

              <th>
                {{ t("creditReportUpload.table.contract") }}
              </th>

              <th>
                {{ t("creditReportUpload.table.currency") }}
              </th>

              <th>
                {{ t("creditReportUpload.table.totalDebt") }}
              </th>

              <th>
                {{ t("creditReportUpload.table.overdue") }}
              </th>

              <th>
                {{ t("creditReportUpload.table.monthlyPayment") }}
              </th>

            </tr>
          </thead>

          <tbody>

            <tr
              v-for="contract in contracts"
              :key="contract.id"
            >

              <td>
                <div class="bank-cell">

                  <span class="bank-dot"></span>

                  <span>
                    {{ contract.bank_name }}
                  </span>

                </div>
              </td>

              <td>
                {{ contract.contract_number }}
              </td>

              <td class="currency">
                {{ contract.currency }}
              </td>

              <td class="amount">
                {{ formatNumber(contract.current_debt) }}
              </td>

              <td class="amount overdue">
                {{ formatNumber(contract.overdue_debt) }}
              </td>

              <td class="amount">
                {{ formatNumber(contract.monthly_payment) }}
              </td>

            </tr>

          </tbody>

        </table>

      </div>

      <!-- ================================= -->
      <!-- EMPTY -->
      <!-- ================================= -->

      <div
        v-if="!contracts.length"
        class="empty"
      >

        <div class="empty-icon">
          📄
        </div>

        <h4>
          {{ t("creditReportUpload.empty.title") }}
        </h4>

        <p>
          {{ t("creditReportUpload.empty.description") }}
        </p>

      </div>

    </div>

  </div>
</template>

<style scoped>
/* ==========================================
   CARD
========================================== */

.card {
  background: #fff;
  padding: 30px;
  border-radius: 24px;
  box-shadow: 0 12px 32px rgba(15, 23, 42, 0.08);
  margin-top: 25px;
}

/* ==========================================
   HEADER
========================================== */

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 28px;
  gap: 20px;
}

.header-content {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.header-icon {
  width: 50px;
  height: 50px;
  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 15px;

  background: linear-gradient(
    135deg,
    #eff6ff,
    #dbeafe
  );

  font-size: 24px;

  box-shadow:
    inset 0 0 0 1px rgba(59, 130, 246, 0.08);
}

.header h2 {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #0f172a;
}

.header p {
  margin-top: 8px;
  font-size: 15px;
  color: #64748b;
  line-height: 1.5;
}

/* ==========================================
   UPLOAD
========================================== */

.upload-box {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-bottom: 20px;
}

.hidden-file-input {
  display: none;
}

/* ==========================================
   DROP ZONE
========================================== */

.drop-zone {
  position: relative;

  min-height: 260px;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 35px;

  border: 2px dashed #cbd5e1;
  border-radius: 22px;

  background:
    linear-gradient(
      180deg,
      #f8fafc 0%,
      #ffffff 100%
    );

  cursor: pointer;

  transition:
    border-color 0.25s ease,
    background 0.25s ease,
    transform 0.25s ease,
    box-shadow 0.25s ease;
}

.drop-zone:hover {
  border-color: #60a5fa;

  background:
    linear-gradient(
      180deg,
      #f8fbff 0%,
      #ffffff 100%
    );

  box-shadow:
    0 10px 30px rgba(37, 99, 235, 0.08);
}

.drop-zone.dragging {
  border-color: #2563eb;

  background:
    linear-gradient(
      135deg,
      #eff6ff,
      #f8fbff
    );

  transform: scale(1.005);

  box-shadow:
    0 16px 40px rgba(37, 99, 235, 0.12);
}

.drop-zone.disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

/* ==========================================
   UPLOAD ICON
========================================== */

.upload-icon-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.upload-icon {
  width: 74px;
  height: 74px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 22px;

  color: #2563eb;

  background:
    linear-gradient(
      135deg,
      #dbeafe,
      #eff6ff
    );

  box-shadow:
    0 12px 30px rgba(37, 99, 235, 0.14);

  transition:
    transform 0.25s ease,
    box-shadow 0.25s ease;
}

.drop-zone:hover .upload-icon {
  transform: translateY(-4px);

  box-shadow:
    0 16px 34px rgba(37, 99, 235, 0.18);
}

.upload-icon svg {
  width: 34px;
  height: 34px;
}

/* ==========================================
   DROP CONTENT
========================================== */

.drop-content {
  text-align: center;
  max-width: 620px;
}

.drop-content h3 {
  margin: 0;

  font-size: 20px;
  font-weight: 700;

  color: #0f172a;
}

.drop-description {
  margin: 10px 0 0;

  font-size: 15px;
  line-height: 1.6;

  color: #64748b;
}

.browse-button {
  display: inline;

  padding: 0;

  border: none;
  background: transparent;

  color: #2563eb;

  font: inherit;
  font-weight: 700;

  cursor: pointer;

  transition: color 0.2s ease;
}

.browse-button:hover {
  color: #1d4ed8;
}

/* ==========================================
   SUPPORTED FILES
========================================== */

.supported-files {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;

  margin-top: 18px;
}

.format-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;

  min-width: 44px;
  height: 28px;

  padding: 0 9px;

  border-radius: 8px;

  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.5px;
}

.pdf-badge {
  color: #b91c1c;
  background: #fee2e2;
}

.html-badge {
  color: #0369a1;
  background: #e0f2fe;
}

.format-text {
  margin-left: 3px;

  font-size: 12px;
  color: #94a3b8;
}

/* ==========================================
   SELECTED FILE
========================================== */

.selected-file {
  width: 100%;

  display: flex;
  align-items: center;

  gap: 16px;

  padding: 18px 20px;

  border-radius: 16px;

  background: #ffffff;

  border: 1px solid #dbeafe;

  box-shadow:
    0 8px 24px rgba(15, 23, 42, 0.06);
}

.file-type-icon {
  width: 54px;
  height: 54px;

  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 15px;

  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.5px;
}

.file-type-icon.pdf {
  color: #b91c1c;
  background: #fee2e2;
}

.file-type-icon.html {
  color: #0369a1;
  background: #e0f2fe;
}

.selected-file-info {
  min-width: 0;
  flex: 1;
}

.selected-file-name {
  overflow: hidden;

  font-size: 15px;
  font-weight: 700;

  color: #0f172a;

  text-overflow: ellipsis;
  white-space: nowrap;
}

.selected-file-meta {
  display: flex;
  align-items: center;

  gap: 7px;

  margin-top: 5px;

  font-size: 12px;
  color: #64748b;
}

.meta-dot {
  color: #cbd5e1;
}

.remove-file-button {
  width: 38px;
  height: 38px;

  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 0;

  border: none;
  border-radius: 10px;

  background: #f8fafc;
  color: #64748b;

  cursor: pointer;

  transition:
    background 0.2s ease,
    color 0.2s ease,
    transform 0.2s ease;
}

.remove-file-button:hover:not(:disabled) {
  background: #fee2e2;
  color: #dc2626;

  transform: scale(1.05);
}

.remove-file-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.remove-file-button svg {
  width: 18px;
  height: 18px;
}

/* ==========================================
   CHANGE FILE
========================================== */

.change-file-button {
  align-self: flex-start;

  display: inline-flex;
  align-items: center;
  gap: 8px;

  padding: 8px 12px;

  border: none;
  border-radius: 9px;

  background: transparent;

  color: #2563eb;

  font-size: 13px;
  font-weight: 600;

  cursor: pointer;

  transition:
    background 0.2s ease,
    color 0.2s ease;
}

.change-file-button:hover:not(:disabled) {
  background: #eff6ff;
  color: #1d4ed8;
}

.change-file-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.change-file-button svg {
  width: 16px;
  height: 16px;
}

/* ==========================================
   UPLOAD BUTTON
========================================== */

.upload-button {
  width: 100%;

  min-height: 54px;

  display: flex;
  align-items: center;
  justify-content: center;

  gap: 10px;

  padding: 14px 22px;

  border: none;
  border-radius: 14px;

  background:
    linear-gradient(
      135deg,
      #2563eb,
      #1d4ed8
    );

  color: #fff;

  font-weight: 700;
  font-size: 15px;

  cursor: pointer;

  box-shadow:
    0 10px 22px rgba(37, 99, 235, 0.22);

  transition:
    transform 0.25s ease,
    box-shadow 0.25s ease,
    opacity 0.25s ease;
}

.upload-button:hover:not(:disabled) {
  transform: translateY(-2px);

  box-shadow:
    0 14px 28px rgba(37, 99, 235, 0.28);
}

.upload-button:active:not(:disabled) {
  transform: translateY(0);
}

.upload-button:disabled {
  opacity: 0.5;

  cursor: not-allowed;

  box-shadow: none;
}

.upload-button svg {
  width: 20px;
  height: 20px;
}

/* ==========================================
   SPINNER
========================================== */

.spinner {
  width: 19px;
  height: 19px;

  border: 2px solid rgba(255, 255, 255, 0.35);
  border-top-color: #fff;

  border-radius: 50%;

  animation: spin 0.75s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* ==========================================
   ALERTS
========================================== */

.alert {
  display: flex;
  align-items: center;

  gap: 12px;

  margin-top: 18px;

  padding: 14px 16px;

  border-radius: 14px;
}

.alert p {
  margin: 0;

  font-size: 14px;
  font-weight: 600;
}

.alert-icon {
  width: 28px;
  height: 28px;

  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 50%;

  font-size: 14px;
  font-weight: 800;
}

.success-alert {
  color: #166534;

  background: #f0fdf4;

  border: 1px solid #bbf7d0;
}

.success-alert .alert-icon {
  color: #fff;
  background: #16a34a;
}

.error-alert {
  color: #991b1b;

  background: #fef2f2;

  border: 1px solid #fecaca;
}

.error-alert .alert-icon {
  color: #fff;
  background: #dc2626;
}

/* ==========================================
   REPORT
========================================== */

.report {
  margin-top: 35px;
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  margin-bottom: 20px;

  gap: 20px;
}

.report-title-wrapper {
  display: flex;
  align-items: center;

  gap: 14px;
}

.report-icon {
  width: 46px;
  height: 46px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 13px;

  background: #eff6ff;

  font-size: 21px;
}

.report-header h3 {
  margin: 0;

  font-size: 22px;
  font-weight: 700;

  color: #0f172a;
}

.report-subtitle {
  display: block;

  margin-top: 4px;

  font-size: 12px;
  color: #94a3b8;
}

.count {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 44px;
  height: 44px;

  border-radius: 999px;

  background: #dbeafe;

  color: #2563eb;

  font-size: 15px;
  font-weight: 700;
}

/* ==========================================
   TABLE
========================================== */

.table-wrapper {
  width: 100%;
  overflow-x: auto;

  border-radius: 16px;
}

.contracts {
  width: 100%;

  border-collapse: collapse;

  overflow: hidden;

  border-radius: 16px;

  border: 1px solid #e2e8f0;

  background: #fff;
}

.contracts thead {
  background: #eff6ff;
}

.contracts th {
  padding: 18px;

  text-align: left;

  font-size: 14px;
  font-weight: 700;

  color: #1e3a8a;

  white-space: nowrap;
}

.contracts td {
  padding: 18px;

  font-size: 14px;

  color: #334155;

  border-top: 1px solid #e2e8f0;

  vertical-align: middle;
}

.contracts tbody tr {
  transition: background 0.25s ease;
}

.contracts tbody tr:hover {
  background: #f8fafc;
}

/* ==========================================
   BANK
========================================== */

.bank-cell {
  display: flex;
  align-items: center;

  gap: 9px;

  font-weight: 600;
}

.bank-dot {
  width: 7px;
  height: 7px;

  flex-shrink: 0;

  border-radius: 50%;

  background: #2563eb;
}

/* ==========================================
   MONEY
========================================== */

.amount {
  text-align: right;

  font-weight: 700;

  font-variant-numeric: tabular-nums;

  white-space: nowrap;

  letter-spacing: 0.3px;
}

.overdue {
  color: #dc2626;
}

.currency {
  text-align: center;

  font-weight: 600;
}

/* ==========================================
   EMPTY
========================================== */

.empty {
  padding: 60px 30px;

  background: #f8fafc;

  border: 1px dashed #cbd5e1;

  border-radius: 18px;

  text-align: center;
}

.empty-icon {
  font-size: 54px;

  margin-bottom: 16px;
}

.empty h4 {
  margin: 0;

  font-size: 20px;

  font-weight: 700;

  color: #0f172a;
}

.empty p {
  margin-top: 12px;

  font-size: 15px;

  color: #64748b;

  line-height: 1.6;
}

/* ==========================================
   MOBILE
========================================== */

@media (max-width: 900px) {
  .card {
    padding: 22px;
  }

  .header {
    flex-direction: column;
    align-items: flex-start;
  }

  .header h2 {
    font-size: 24px;
  }

  .drop-zone {
    min-height: 230px;
    padding: 25px 18px;
  }

  .upload-icon {
    width: 64px;
    height: 64px;
  }

  .upload-icon svg {
    width: 30px;
    height: 30px;
  }

  .supported-files {
    flex-wrap: wrap;
  }

  .selected-file {
    padding: 14px;
    gap: 12px;
  }

  .selected-file-name {
    max-width: 190px;
  }

  .report-header {
    align-items: flex-start;
  }

  .contracts {
    min-width: 850px;
  }
}

@media (max-width: 600px) {
  .card {
    padding: 18px;
    border-radius: 18px;
  }

  .header-content {
    gap: 12px;
  }

  .header-icon {
    width: 44px;
    height: 44px;
    font-size: 21px;
  }

  .header h2 {
    font-size: 21px;
  }

  .header p {
    font-size: 14px;
  }

  .drop-zone {
    min-height: 210px;

    padding: 22px 14px;

    border-radius: 18px;
  }

  .drop-content h3 {
    font-size: 18px;
  }

  .drop-description {
    font-size: 14px;
  }

  .selected-file {
    align-items: flex-start;
  }

  .file-type-icon {
    width: 46px;
    height: 46px;

    border-radius: 12px;
  }

  .selected-file-name {
    max-width: 150px;

    font-size: 14px;
  }

  .selected-file-meta {
    font-size: 11px;
  }

  .remove-file-button {
    width: 34px;
    height: 34px;
  }

  .report-title-wrapper {
    align-items: flex-start;
  }

  .report-header h3 {
    font-size: 18px;
  }

  .report-subtitle {
    display: none;
  }

  .count {
    width: 38px;
    height: 38px;
  }
}
</style>