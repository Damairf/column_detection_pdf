<template>
  <AppLayout>
    <div class="flex flex-col min-h-full">

      <!-- Modal Upload Gambar -->
      <div
        v-if="showUploadModal"
        @click.self="closeUploadModal"
        class="fixed inset-0 z-50 flex items-center justify-center"
        style="background: rgba(0,0,0,0.40);"
      >
        <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-lg mx-6 p-8">

          <!-- Drop Zone -->
          <div
            class="border-2 border-dashed rounded-xl flex flex-col items-center justify-center py-14 px-6 mb-5 transition-colors"
            :class="[
              isDragging
                ? 'border-gray-500 bg-gray-100 cursor-copy'
                : 'border-gray-300 bg-gray-50 hover:border-gray-400 hover:bg-gray-100 cursor-pointer'
            ]"
            @dragover.prevent="isDragging = true"
            @dragleave.prevent="isDragging = false"
            @drop.prevent="handleDrop"
            @click="triggerFileInput"
          >
            <div class="w-14 h-14 rounded-full bg-gray-200 flex items-center justify-center mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            <p class="text-sm font-medium text-gray-500">Tarik dan lepas gambar di sini</p>
            <p class="text-xs text-gray-400 mt-1">Format: PNG, JPG, JPEG</p>
          </div>

          <input
            ref="fileInputRef"
            type="file"
            accept=".png,.jpg,.jpeg,image/png,image/jpeg"
            class="hidden"
            @change="handleFileInput"
          />

          <!-- Error -->
          <p v-if="uploadError" class="text-red-500 text-sm text-center mb-4">{{ uploadError }}</p>

          <!-- Tombol -->
          <div class="flex justify-center gap-3">
            <button
              @click.stop="triggerFileInput"
              :disabled="isUploading"
              class="flex items-center gap-2 px-5 py-2 border border-gray-300 rounded-lg text-sm text-gray-600 bg-white hover:bg-gray-50 transition shadow-sm"
              :class="isUploading ? 'opacity-60 cursor-not-allowed' : 'cursor-pointer'"
            >
              <span v-if="isUploading" class="flex items-center gap-2">
                <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                </svg>
                Mengunggah...
              </span>
              <span v-else class="flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                </svg>
                Unggah File
              </span>
            </button>
          </div>
        </div>
      </div>

      <!-- Konten Utama -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">

        <!-- Preview Gambar -->
        <div class="mb-4 rounded-xl overflow-hidden border border-gray-200 bg-gray-100" style="height: 80vh;">
          <!-- Loading -->
          <div v-if="isLoadingPreview" class="w-full h-full flex items-center justify-center">
            <svg class="animate-spin h-8 w-8 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
          </div>
          <!-- Gambar Preview -->
          <img
            v-else
            :src="previewUrl"
            :key="previewKey"
            alt="Preview Background Login"
            class="w-full h-full object-cover"
            @error="handleImgError"
          />
        </div>

        <!-- Tombol Ubah Gambar Background -->
        <button
          @click="openUploadModal"
          :disabled="isSaving"
          class="w-full py-3 border border-gray-300 rounded-lg text-sm text-gray-600 bg-white hover:bg-gray-50 transition mb-4"
          :class="isSaving ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'"
        >
          Ubah gambar background
        </button>

        <!-- Tombol Reset & Simpan -->
        <div class="flex justify-end gap-3">
          <button
            @click="handleReset"
            :disabled="isSaving"
            class="cursor-pointer px-6 py-2.5 bg-red-600 text-white text-sm font-semibold rounded-lg
                   hover:bg-red-700 transition shadow-sm"
          >
            Reset
          </button>
          <button
            @click="handleSimpan"
            :disabled="isSaving"
            class="cursor-pointer px-6 py-2.5 bg-gray-900 text-white text-sm font-semibold rounded-lg
                   hover:bg-gray-700 transition shadow-sm"
          >
            <span v-if="isSaving" class="flex items-center gap-2">
              <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
              Menyimpan...
            </span>
            <span v-else>Simpan</span>
          </button>
        </div>

      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { onBeforeRouteLeave } from 'vue-router'
import axios from 'axios'
import AppLayout from '../components/AppLayout.vue'

const showUploadModal  = ref(false)
const isDragging       = ref(false)
const isUploading      = ref(false)
const isSaving         = ref(false)
const isLoadingPreview = ref(true)
const fileInputRef     = ref(null)

const uploadError      = ref('')
const saveSuccess      = ref('')
const saveError        = ref('')

const activeBg         = ref('bg-nasmoco.avif')

const hasTempFile      = ref(false)

const hasUnsavedChange = ref(false)

const previewKey       = ref(0)

const previewUrl = computed(() => {
  const base      = import.meta.env.VITE_API_BASE_URL || ''
  const timestamp = Date.now()
  const filename  = hasTempFile.value ? 'temp-custom.avif' : activeBg.value
  return `${base}/api/kustomisasi/background-file/${filename}?t=${timestamp}`
})

function getAuthHeader() {
  const token = localStorage.getItem('token')
  return { Authorization: `Bearer ${token}` }
}

onMounted(async () => {
  await fetchActiveBg()
})

onBeforeRouteLeave(async (_to, _from, next) => {
  if (hasTempFile.value) {
    try {
      await axios.post(
        '/api/kustomisasi/cancel',
        {},
        { headers: getAuthHeader() }
      )
    } catch (e) {
      console.warn('Gagal menghapus file temp saat navigasi:', e)
    }
    hasTempFile.value      = false
    hasUnsavedChange.value = false
  }
  next()
})

async function fetchActiveBg() {
  isLoadingPreview.value = true
  try {
    const res  = await axios.get('/api/kustomisasi/bg-active', { headers: getAuthHeader() })
    activeBg.value = res.data.background
  } catch (e) {
    console.error('Gagal mengambil background aktif:', e)
    activeBg.value = 'bg-nasmoco.avif'
  } finally {
    previewKey.value++
    isLoadingPreview.value = false
  }
}

function openUploadModal() {
  uploadError.value    = ''
  showUploadModal.value = true
}

function closeUploadModal() {
  if (isUploading.value) return
  showUploadModal.value = false
  isDragging.value      = false
  uploadError.value     = ''
}

function triggerFileInput() {
  fileInputRef.value?.click()
}
async function handleFileInput(event) {
  const file = event.target.files?.[0]
  if (file) await processFile(file)
  if (fileInputRef.value) fileInputRef.value.value = ''
}

async function handleDrop(event) {
  isDragging.value = false
  const file = event.dataTransfer.files?.[0]
  if (file) await processFile(file)
}

async function processFile(file) {
  uploadError.value = ''

  const allowedTypes = ['image/png', 'image/jpeg']
  if (!allowedTypes.includes(file.type)) {
    uploadError.value = 'Format tidak didukung. Gunakan PNG, JPG, atau JPEG.'
    return
  }

  if (file.size > 10 * 1024 * 1024) {
    uploadError.value = 'Ukuran file terlalu besar. Maksimal 10 MB.'
    return
  }

  isUploading.value  = true
  saveSuccess.value  = ''
  saveError.value    = ''

  try {
    const formData = new FormData()
    formData.append('file', file)

    await axios.post('/api/kustomisasi/upload', formData, {
      headers: {
        ...getAuthHeader(),
        'Content-Type': 'multipart/form-data',
      },
    })

    hasTempFile.value      = true
    hasUnsavedChange.value = true
    showUploadModal.value  = false
    previewKey.value++
  } catch (e) {
    uploadError.value = e.response?.data?.detail || 'Gagal mengunggah gambar. Coba lagi.'
  } finally {
    isUploading.value = false
  }
}

async function handleSimpan() {
  isSaving.value    = true
  saveSuccess.value = ''
  saveError.value   = ''
  try {
    const res = await axios.post(
      '/api/kustomisasi/save',
      { action: 'save' },
      { headers: getAuthHeader() }
    )
    activeBg.value         = res.data.background
    hasTempFile.value      = false
    hasUnsavedChange.value = false
    saveSuccess.value      = res.data.message
    previewKey.value++
  } catch (e) {
    saveError.value = e.response?.data?.detail
  } finally {
    isSaving.value = false
  }
}

async function handleReset() {
  isSaving.value    = true
  saveSuccess.value = ''
  saveError.value   = ''
  try {
    const res = await axios.post(
      '/api/kustomisasi/save',
      { action: 'reset' },
      { headers: getAuthHeader() }
    )
    activeBg.value         = res.data.background
    hasTempFile.value      = false
    hasUnsavedChange.value = false
    saveSuccess.value      = res.data.message
    previewKey.value++
  } catch (e) {
    saveError.value = e.response?.data?.detail || 'Gagal mereset background. Coba lagi.'
  } finally {
    isSaving.value = false
  }
}

function handleImgError(e) {
  const base = import.meta.env.VITE_API_BASE_URL || ''
  const defaultUrl = `${base}/api/kustomisasi/background-file/bg-nasmoco.avif?t=${Date.now()}`
  if (e.target.src !== defaultUrl) {
    e.target.src = defaultUrl
  }
}
</script>