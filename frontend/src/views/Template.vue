<template>
  <AppLayout>
    <div class="flex flex-col min-h-full">

    <!-- Overlay Upload PDF -->
    <div
      v-if="showUploadModal"
      class="fixed inset-0 z-50 flex items-center justify-center"
      style="background: rgba(0,0,0,0.35);"
      @click.self="showUploadModal = false"
    >
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg mx-6 p-8">

        <!-- Drop Zone -->
        <div
          class="border-2 border-dashed rounded-xl flex flex-col items-center justify-center py-14 px-6 mb-6 transition-colors cursor-pointer"
          :class="isDragging
            ? 'border-gray-500 bg-gray-100'
            : 'border-gray-300 bg-gray-50 hover:border-gray-400 hover:bg-gray-100'"
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

        <input ref="fileInputRef" type="file" accept=".pdf" class="hidden" @change="handleFileInput" />

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

    <!-- Cari + Urut + Tambah -->
    <div class="flex items-center justify-between mb-4">

      <div class="relative">
        <span class="absolute inset-y-0 left-3 flex items-center text-gray-400 pointer-events-none">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35m0 0A7.5 7.5 0 1010.5 18a7.5 7.5 0 006.15-3.35z" />
          </svg>
        </span>
        <input v-model="searchQuery" type="text" placeholder="Cari...."
          class="pl-9 pr-4 py-2 w-64 border border-gray-300 rounded-lg text-sm text-gray-700 placeholder-gray-400
                 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent bg-white shadow-sm" />
      </div>

      <div class="flex items-center gap-2">
        <div class="relative" @mouseenter="handleMouseEnter" @mouseleave="handleMouseLeave">
          <button class="flex items-center gap-1.5 px-4 py-2 bg-gray-900 text-white text-sm font-medium rounded-lg hover:bg-gray-800 transition shadow-sm">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V4m0 0L3 8m4-4l4 4M17 8v12m0 0l4-4m-4 4l-4-4" />
            </svg>
            Urut
          </button>
          <div v-if="showUrutDropdown" class="absolute right-0 top-full mt-1.5 w-48 bg-white border border-gray-200 rounded-lg shadow-lg z-50 overflow-hidden">
            <button v-for="opt in sortOptions" :key="opt.value" @click="selectSort(opt.value)"
              class="w-full text-left px-4 py-2.5 text-sm transition"
              :class="sortKey === opt.value ? 'bg-gray-900 text-white font-medium' : 'text-gray-700 hover:bg-gray-100'">
              {{ opt.label }}
            </button>
          </div>
        </div>

        <button v-if="user.role === 'admin'" @click="showUploadModal = true"
          class="cursor-pointer flex items-center gap-1.5 px-4 py-2 border border-gray-300 bg-white text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-50 transition shadow-sm">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Tambah
        </button>
      </div>
    </div>

    <!-- Kartu Tabel -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-gray-200">
              <th class="px-5 py-3.5 text-center font-semibold text-gray-700 w-28">ID</th>
              <th class="px-5 py-3.5 text-center font-semibold text-gray-700">Nama Template</th>
              <th class="px-5 py-3.5 text-center font-semibold text-gray-700">Pembuat</th>
              <th class="px-5 py-3.5 text-center font-semibold text-gray-700 w-28">Halaman</th>
              <th class="px-5 py-3.5 text-center font-semibold text-gray-700 w-28">Kolom</th>
              <th class="px-5 py-3.5 text-center font-semibold text-gray-700 w-32">Tanggal</th>
              <th class="px-5 py-3.5 text-center font-semibold text-gray-700 w-24">Detail</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="7" class="px-5 py-10 text-center text-gray-400 text-sm">
                <div class="flex items-center justify-center gap-2">
                  <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                  </svg>
                  Memuat data...
                </div>
              </td>
            </tr>
            <tr v-else-if="errorMsg">
              <td colspan="7" class="px-5 py-10 text-center text-red-400 text-sm">{{ errorMsg }}</td>
            </tr>
            <tr v-else v-for="row in paginatedData" :key="row.id" class="border-b border-gray-100 hover:bg-gray-50 transition-colors">
              <td class="px-5 py-3 text-center text-gray-700 font-mono text-xs">{{ formatId(row.id) }}</td>
              <td class="px-5 py-3 text-center text-gray-700">{{ row.nama_template }}</td>
              <td class="px-5 py-3 text-center text-gray-500">{{ row.username || '—' }}</td>
              <td class="px-5 py-3 text-center text-gray-700">{{ row.jml_halaman }}</td>
              <td class="px-5 py-3 text-center text-gray-700">{{ row.jml_kolom }}</td>
              <td class="px-5 py-3 text-center text-gray-500">{{ formatTanggal(row.created_at) }}</td>
              <td class="px-5 py-3 text-center">
                <button @click="lihatDetail(row.id)" class="text-blue-500 hover:text-blue-700 font-medium hover:underline transition">Detail</button>
              </td>
            </tr>
            <tr v-if="!loading && !errorMsg && paginatedData.length === 0">
              <td colspan="7" class="px-5 py-10 text-center text-gray-400 text-sm">Tidak ada data ditemukan.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="flex items-center justify-center gap-2 py-5 border-t border-gray-100">

        <!-- Max Prev -->
        <button
          @click="goToPage(1)"
          :disabled="currentPage === 1"
          class="w-9 h-9 flex items-center justify-center rounded-lg font-bold transition"
          :class="currentPage === 1 ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-gray-900 text-white hover:bg-gray-700 cursor-pointer'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M11 19l-7-7 7-7M19 19l-7-7 7-7" />
          </svg>
        </button>

        <!-- Prev -->
        <button
          @click="goToPage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="w-9 h-9 flex items-center justify-center rounded-lg font-bold transition"
          :class="currentPage === 1 ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-gray-900 text-white hover:bg-gray-700 cursor-pointer'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7" />
          </svg>
        </button>

        <!-- Input halaman -->
        <input
          type="number" :value="currentPage"
          @change="onPageInputChange" @keydown.enter="onPageInputChange"
          min="1" :max="totalPages"
          class="w-12 h-9 text-center border border-gray-300 rounded-lg text-sm font-medium text-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
        />

        <!-- Next -->
        <button
          @click="goToPage(currentPage + 1)"
          :disabled="currentPage === totalPages || totalPages === 0"
          class="w-9 h-9 flex items-center justify-center rounded-lg font-bold transition"
          :class="currentPage === totalPages || totalPages === 0 ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-gray-900 text-white hover:bg-gray-700 cursor-pointer'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7" />
          </svg>
        </button>

        <!-- Max Next -->
        <button
          @click="goToPage(totalPages)"
          :disabled="currentPage === totalPages || totalPages === 0"
          class="w-9 h-9 flex items-center justify-center rounded-lg font-bold transition"
          :class="currentPage === totalPages || totalPages === 0 ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-gray-900 text-white hover:bg-gray-700 cursor-pointer'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 5l7 7-7 7M5 5l7 7-7 7" />
          </svg>
        </button>

      </div>
    </div>
    <!-- Footer Warning -->
    <div class="mt-auto pt-6 text-xs text-gray-400 text-center border-t border-gray-100">
      Sistem ini bisa melakukan kesalahan. Silahkan periksa kembali hasilnya
    </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import AppLayout from '../components/AppLayout.vue'

const router = useRouter()

const user = computed(() => {
  try { return JSON.parse(localStorage.getItem('user')) || {} }
  catch { return {} }
})

const allData          = ref([])
const loading          = ref(false)
const errorMsg         = ref('')
const searchQuery      = ref('')
const currentPage      = ref(1)
const itemsPerPage     = 10
const showUrutDropdown = ref(false)
const sortKey          = ref('id-desc')

const showUploadModal = ref(false)
const isDragging      = ref(false)
const isUploading     = ref(false)
const uploadError     = ref('')
const fileInputRef    = ref(null)

const sortOptions = [
  { label: 'A - Z (Menurun)',   value: 'az-desc'  },
  { label: 'A - Z (Menaik)',    value: 'az-asc'   },
  { label: 'ID (Menurun)',      value: 'id-desc'  },
  { label: 'ID (Menaik)',       value: 'id-asc'   },
  { label: 'Tanggal (Menurun)', value: 'tgl-desc' },
  { label: 'Tanggal (Menaik)',  value: 'tgl-asc'  },
]

async function fetchData() {
  loading.value = true
  errorMsg.value = ''
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('/api/template/list', {
      headers: { Authorization: `Bearer ${token}` }
    })
    allData.value = response.data
  } catch (err) {
    errorMsg.value = err.response?.status === 401
      ? 'Sesi habis. Silakan login ulang.'
      : 'Gagal memuat data. Coba muat ulang halaman.'
  } finally {
    loading.value = false
  }
}

onMounted(() => fetchData())
watch(searchQuery, () => { currentPage.value = 1 })

function formatId(id)   { return 'T-' + String(id).padStart(6, '0') }
function formatTanggal(isoString) {
  if (!isoString) return '-'
  const d = new Date(isoString)
  return `${String(d.getDate()).padStart(2,'0')}/${String(d.getMonth()+1).padStart(2,'0')}/${d.getFullYear()}`
}

const filteredData = computed(() => {
  const q = searchQuery.value.toLowerCase().trim()
  if (!q) return allData.value
  return allData.value.filter(row =>
    formatId(row.id).toLowerCase().includes(q) ||
    row.nama_template?.toLowerCase().includes(q) ||
    row.username?.toLowerCase().includes(q) ||
    String(row.jml_halaman).includes(q) ||
    String(row.jml_kolom).includes(q) ||
    formatTanggal(row.created_at).includes(q)
  )
})

const sortedData = computed(() => {
  const data = [...filteredData.value]
  switch (sortKey.value) {
    case 'az-asc':   return data.sort((a, b) => a.nama_template.localeCompare(b.nama_template))
    case 'az-desc':  return data.sort((a, b) => b.nama_template.localeCompare(a.nama_template))
    case 'id-asc':   return data.sort((a, b) => a.id - b.id)
    case 'id-desc':  return data.sort((a, b) => b.id - a.id)
    case 'tgl-asc':  return data.sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
    case 'tgl-desc': return data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    default: return data
  }
})

const totalPages    = computed(() => Math.ceil(sortedData.value.length / itemsPerPage) || 1)
const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return sortedData.value.slice(start, start + itemsPerPage)
})

let hideTimeout = null
function handleMouseEnter() {
  if (hideTimeout) { clearTimeout(hideTimeout); hideTimeout = null }
  showUrutDropdown.value = true
}
function handleMouseLeave() {
  hideTimeout = setTimeout(() => { showUrutDropdown.value = false }, 200)
}
function selectSort(value) {
  sortKey.value = sortKey.value === value ? '' : value
  showUrutDropdown.value = false
  currentPage.value = 1
}

function goToPage(page) { currentPage.value = Math.max(1, Math.min(page, totalPages.value)) }
function onPageInputChange(e) {
  const val = parseInt(e.target.value)
  if (!isNaN(val)) goToPage(val)
  e.target.value = currentPage.value
}
function lihatDetail(id) { router.push(`/template/detail/${id}`) }

// Upload PDF
function triggerFileInput() { fileInputRef.value?.click() }
function handleFileInput(e) {
  const file = e.target.files[0]
  if (file) prosesFile(file)
  e.target.value = ''
}
function handleDrop(e) {
  isDragging.value = false
  const file = e.dataTransfer.files[0]
  if (file) prosesFile(file)
}

async function prosesFile(file) {
  uploadError.value = ''
  if (file.type !== 'application/pdf' && !file.name.endsWith('.pdf')) {
    uploadError.value = 'File harus berformat PDF.'
    return
  }
  isUploading.value = true
  try {
    const token = localStorage.getItem('token')
    const formData = new FormData()
    formData.append('file', file)

    const response = await axios.post('/api/template/upload-pdf', formData, {
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'multipart/form-data' }
    })
    sessionStorage.setItem('template_tambah_data', JSON.stringify({
      namaFile:        response.data.nama_file,
      pdf_path:        response.data.pdf_path,
      imagePaths:      response.data.image_paths,
      jml_halaman:     response.data.jml_halaman,
      resolusi_width:  response.data.resolusi_width,
      resolusi_height: response.data.resolusi_height,
      kolomList:       [],
      kolomBaru:       null,
    }))

    showUploadModal.value = false
    router.push('/template/tambah')

  } catch (err) {
    uploadError.value = err.response?.data?.detail || 'Gagal mengunggah file. Coba lagi.'
  } finally {
    isUploading.value = false
  }
}
</script>