<template>
  <AppLayout>

    <!-- Modal Upload PDF -->
    <div
      v-if="showUploadModal"
      @click.self="closeUploadModal"
      class="fixed inset-0 z-50 flex items-center justify-center"
      style="background: rgba(0,0,0,0.35);"
    >
      <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-lg mx-6 p-8">

        <div
          class="border-2 border-dashed rounded-xl flex flex-col items-center justify-center py-14 px-6 mb-6 transition-colors cursor-pointer"
          :class="isDragging ? 'border-gray-500 bg-gray-100' : 'border-gray-300 bg-gray-50 hover:border-gray-400 hover:bg-gray-100'"
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
          <p class="text-sm text-gray-500">tarik dan unggah file PDF anda</p>
        </div>

        <input ref="fileInputRef" type="file" accept=".pdf" multiple class="hidden" @change="handleFileInput" />

        <p v-if="uploadError" class="text-red-500 text-sm text-center mb-4">{{ uploadError }}</p>

        <div class="flex justify-center">
          <button
            @click.stop="triggerFileInput"
            :disabled="isUploading"
            class="flex items-center gap-2 px-5 py-2 border border-gray-300 rounded-lg text-sm text-gray-600 bg-white hover:bg-gray-50 transition shadow-sm"
            :class="isUploading ? 'opacity-60 cursor-not-allowed' : 'cursor-pointer'"
          >
            <span v-if="isUploading" class="flex items-center gap-2">
              <svg class="animate-spin h-4 w-4 text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
              Mengunggah...
            </span>
            <span v-else class="flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
              </svg>
              Unggah file
            </span>
          </button>
        </div>
      </div>
    </div>

    <!-- Konten Utama -->
    <div class="mb-5">
      <button
        @click="handleKembali"
        :disabled="isBatal"
        class="flex items-center gap-2 px-4 py-2 bg-gray-900 text-white text-sm font-semibold rounded-lg hover:bg-gray-700 transition shadow-sm"
        :class="isBatal ? 'opacity-60 cursor-not-allowed' : 'cursor-pointer'"
      >
        <svg v-if="isBatal" class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
        </svg>
        {{ isBatal ? 'Membatalkan...' : 'Kembali' }}
      </button>
    </div>

    <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-8">

      <!-- Nama Template -->
      <div class="mb-6">
        <label class="block text-sm font-semibold text-gray-700 mb-2">Nama Template</label>
        <div class="relative">
          <input
            v-model="searchTemplate"
            @focus="showDropdown = true"
            placeholder="Cari template..."
            class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-gray-400"
            :class="errorTemplate ? 'border-red-400' : ''"
          />
          <div class="pointer-events-none absolute inset-y-0 right-3 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </div>
          <div
            v-if="showDropdown"
            class="absolute z-10 w-full bg-white border border-gray-200 rounded-lg mt-1 shadow max-h-48 overflow-y-auto"
          >
            <div
              v-for="t in filteredTemplate"
              :key="t.id"
              @click="pilihTemplate(t)"
              class="px-4 py-2 text-sm cursor-pointer hover:bg-gray-100"
            >
              {{ t.nama_template }}
            </div>
            <div v-if="filteredTemplate.length === 0" class="px-4 py-2 text-sm text-gray-400">
              Tidak ditemukan nama template
            </div>
          </div>
        </div>
        <p v-if="errorTemplate" class="text-red-500 text-xs mt-1">{{ errorTemplate }}</p>
      </div>

      <!-- Daftar dokumen yang sudah diunggah -->
      <div v-if="dokumenList.length > 0" class="mb-4">
        <div class="grid grid-cols-[10rem_1fr] gap-x-4 mb-2 px-1">
          <span class="text-sm font-semibold text-gray-700">Tanggal</span>
          <span class="text-sm font-semibold text-gray-700">File Unggahan</span>
        </div>
        <div :class="dokumenList.length > 5 ? 'max-h-72 overflow-y-auto' : ''" class="space-y-2 pr-1">
          <div
            v-for="(dok, idx) in dokumenList"
            :key="idx"
            class="grid grid-cols-[10rem_1fr_auto] gap-x-3 items-center"
          >
            <div class="px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 select-none">
              {{ formatTanggal(dok.tanggal) }}
            </div>
            <div class="flex items-center gap-2 px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <span class="truncate">{{ dok.namaFile }}</span>
            </div>
            <button
              @click="hapusDokumen(idx)"
              class="cursor-pointer p-2 text-gray-400 hover:text-red-500 transition flex-shrink-0"
              title="Hapus dokumen"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Tambah Dokumen Baru -->
      <button
        @click="openUploadModal"
        class="w-full py-3 border border-gray-200 rounded-lg text-sm text-gray-400
               bg-white cursor-pointer hover:bg-gray-50 hover:text-gray-600 transition mb-6"
      >
        + Tambah dokumen baru
      </button>

      <!-- Error server -->
      <div v-if="serverError" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm text-center">
        {{ serverError }}
      </div>

      <!-- Tombol Simpan -->
      <button
        @click="handleSimpan"
        :disabled="isSimpan"
        class="w-full py-3.5 font-bold text-sm rounded-lg transition shadow-sm"
        :class="isSimpan ? 'bg-gray-400 text-white cursor-not-allowed' : 'bg-gray-900 text-white hover:bg-gray-700 cursor-pointer'"
      >
        <span v-if="isSimpan" class="flex items-center justify-center gap-2">
          <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
          Menyimpan & memproses...
        </span>
        <span v-else>Simpan</span>
      </button>

    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import AppLayout from '../components/AppLayout.vue'

const router = useRouter()

const showUploadModal = ref(false)
const isDragging      = ref(false)
const isUploading     = ref(false)
const uploadError     = ref('')
const fileInputRef    = ref(null)

const searchTemplate  = ref('')
const showDropdown    = ref(false)
const templateDipilih = ref('')
const templateList    = ref([])

const dokumenList     = ref([])
const isBatal         = ref(false)
const isSimpan        = ref(false)
const errorTemplate   = ref('')
const serverError     = ref('')

// Fetch template list
async function fetchTemplateList() {
  try {
    const token = localStorage.getItem('token')
    const res   = await axios.get('/api/template/list', {
      headers: { Authorization: `Bearer ${token}` }
    })
    templateList.value = res.data
  } catch (err) {
    console.warn('Gagal ambil daftar template:', err?.message)
  }
}

const filteredTemplate = computed(() =>
  templateList.value
    .filter(t => t.nama_template.toLowerCase().includes(searchTemplate.value.toLowerCase()))
    .slice(0, 6)
)

function pilihTemplate(t) {
  templateDipilih.value = t.id
  searchTemplate.value  = t.nama_template
  showDropdown.value    = false
}

function handleClickOutside(e) {
  if (!e.target.closest('.relative')) {
    const match = templateList.value.some(
      t => t.nama_template.toLowerCase() === searchTemplate.value.toLowerCase()
    )
    if (!match) {
      searchTemplate.value  = ''
      templateDipilih.value = ''
    }
    showDropdown.value = false
  }
}

// Format tanggal
function formatTanggal(iso) {
  if (!iso) return '-'
  const d = new Date(iso)
  return `${String(d.getDate()).padStart(2,'0')}/${String(d.getMonth()+1).padStart(2,'0')}/${d.getFullYear()}`
}

// Upload PDF
function openUploadModal()  { uploadError.value = ''; showUploadModal.value = true }
function closeUploadModal() { uploadError.value = ''; showUploadModal.value = false }
function triggerFileInput() { fileInputRef.value?.click() }

function handleFileInput(e) {
  const files = Array.from(e.target.files)
  if (dokumenList.value.length + files.length > 10) {
    uploadError.value = 'Batas maksimal unggah 10 dokumen.'
    e.target.value = ''
    return
  }
  files.forEach(f => prosesFile(f))
  e.target.value = ''
}

function handleDrop(e) {
  isDragging.value = false
  const files = Array.from(e.dataTransfer.files)
  if (dokumenList.value.length + files.length > 10) {
    uploadError.value = 'Batas maksimal unggah 10 dokumen.'
    return
  }
  files.forEach(f => prosesFile(f))
}

async function prosesFile(file) {
  uploadError.value = ''
  if (file.type !== 'application/pdf' && !file.name.endsWith('.pdf')) {
    uploadError.value = 'File harus berformat PDF.'
    return
  }
  isUploading.value = true
  try {
    const token    = localStorage.getItem('token')
    const formData = new FormData()
    formData.append('file', file)

    const res = await axios.post('/api/beranda/upload-dokumen', formData, {
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'multipart/form-data' }
    })

    dokumenList.value.push({
      namaFile:    file.name,
      pdfPath:     res.data.pdf_path,
      imageFolder: res.data.image_folder,
      tanggal:     new Date().toISOString(),
    })

    showUploadModal.value = false

  } catch (err) {
    uploadError.value = err.response?.data?.detail || 'Gagal mengunggah file. Coba lagi.'
  } finally {
    isUploading.value = false
  }
}

// Hapus dokumen
async function hapusDokumen(idx) {
  const dok = dokumenList.value[idx]
  if (dok.pdfPath) {
    try {
      const token = localStorage.getItem('token')
      await axios.delete('/api/beranda/batal-upload-dokumen', {
        headers: { Authorization: `Bearer ${token}` },
        data: { pdf_path: dok.pdfPath }
      })
    } catch (err) {
      console.warn('Gagal hapus file dokumen:', err?.message)
    }
  }
  dokumenList.value.splice(idx, 1)
}

async function hapusSemuaDokumen() {
  for (const dok of dokumenList.value) {
    if (dok.pdfPath) {
      try {
        const token = localStorage.getItem('token')
        await axios.delete('/api/beranda/batal-upload-dokumen', {
          headers: { Authorization: `Bearer ${token}` },
          data: { pdf_path: dok.pdfPath }
        })
      } catch {}
    }
  }
}

// Kembali
async function handleKembali() {
  isBatal.value = true
  await hapusSemuaDokumen()
  router.replace('/beranda')
}

// Simpan → trigger deteksi di backend
async function handleSimpan() {
  errorTemplate.value = ''
  serverError.value   = ''

  if (!templateDipilih.value) {
    errorTemplate.value = 'Pilih template terlebih dahulu.'
    return
  }
  if (dokumenList.value.length === 0) {
    serverError.value = 'Tambahkan minimal satu dokumen.'
    return
  }

  isSimpan.value = true
  try {
    const token = localStorage.getItem('token')

    await axios.post('/api/beranda/simpan-dokumen', {
      id_template:  parseInt(templateDipilih.value),
      dokumen_list: dokumenList.value.map(d => ({
        nama_dokumen: d.namaFile,
        pdf_path:     d.pdfPath,
      }))
    }, { headers: { Authorization: `Bearer ${token}` } })

    // Redirect ke beranda — status akan Memuat, lalu berubah saat deteksi selesai
    router.replace('/beranda')

  } catch (err) {
    serverError.value = err.response?.data?.detail || 'Gagal menyimpan dokumen. Coba lagi.'
  } finally {
    isSimpan.value = false
  }
}

onMounted(() => {
  fetchTemplateList()
  document.addEventListener('click', handleClickOutside)
})

</script>