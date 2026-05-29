<template>
  <AppLayout>
    <div class="flex flex-col min-h-full">

    <!-- Cari + Download + Urut + Tambah -->
    <div class="flex items-center justify-between mb-4">

      <div class="relative">
        <span class="absolute inset-y-0 left-3 flex items-center text-gray-400 pointer-events-none">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M21 21l-4.35-4.35m0 0A7.5 7.5 0 1010.5 18a7.5 7.5 0 006.15-3.35z" />
          </svg>
        </span>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Cari...."
          class="pl-9 pr-4 py-2 w-64 border border-gray-300 rounded-lg text-sm text-gray-700 placeholder-gray-400
                 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent bg-white shadow-sm"
        />
      </div>

      <div class="flex items-center gap-2">

        <!-- Download -->
        <button
          @click="showDownloadModal = true"
          class="cursor-pointer flex items-center gap-1.5 px-4 py-2 border border-gray-300 bg-white text-gray-700
                 text-sm font-medium rounded-lg hover:bg-gray-50 transition shadow-sm"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          Download
        </button>

        <!-- Urut -->
        <div class="relative" @mouseenter="handleMouseEnter" @mouseleave="handleMouseLeave">
          <button class="flex items-center gap-1.5 px-4 py-2 bg-gray-900 text-white text-sm font-medium rounded-lg
                         hover:bg-gray-800 transition shadow-sm">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M7 16V4m0 0L3 8m4-4l4 4M17 8v12m0 0l4-4m-4 4l-4-4" />
            </svg>
            Urut
          </button>
          <div v-if="showUrutDropdown"
            class="absolute right-0 top-full mt-1.5 w-48 bg-white border border-gray-200 rounded-lg shadow-lg z-50 overflow-hidden">
            <button
              v-for="opt in sortOptions" :key="opt.value"
              @click="selectSort(opt.value)"
              class="w-full text-left px-4 py-2.5 text-sm transition"
              :class="sortKey === opt.value ? 'bg-gray-900 text-white font-medium' : 'text-gray-700 hover:bg-gray-100'"
            >
              {{ opt.label }}
            </button>
          </div>
        </div>

        <!-- Tambah -->
        <button
          @click="router.push('/beranda/tambah')"
          class="cursor-pointer flex items-center gap-1.5 px-4 py-2 border border-gray-300 bg-white text-gray-700
                 text-sm font-medium rounded-lg hover:bg-gray-50 transition shadow-sm"
        >
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
              <th class="px-5 py-3.5 text-center font-semibold text-gray-700">Nama Dokumen</th>
              <th class="px-5 py-3.5 text-center font-semibold text-gray-700">Pengunggah</th>
              <th class="px-5 py-3.5 text-center font-semibold text-gray-700">Cabang</th>
              <th class="px-5 py-3.5 text-center font-semibold text-gray-700">Nama Template</th>
              <th class="px-5 py-3.5 text-center font-semibold text-gray-700 w-32">Tanggal</th>
              <th v-if="user.role === 'admin'" class="px-5 py-3.5 text-center font-semibold text-gray-700 w-28">Status</th>
              <th class="px-5 py-3.5 text-center font-semibold text-gray-700 w-24">Detail</th>
            </tr>
          </thead>
          <tbody>

            <tr v-if="loading">
              <td :colspan="user.role === 'admin' ? 8 : 7" class="px-5 py-10 text-center text-gray-400 text-sm">
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
              <td :colspan="user.role === 'admin' ? 8 : 7" class="px-5 py-10 text-center text-red-400 text-sm">{{ errorMsg }}</td>
            </tr>

            <tr
              v-else
              v-for="row in paginatedData"
              :key="row.id"
              class="border-b border-gray-100 hover:bg-gray-50 transition-colors"
            >
              <td class="px-5 py-3 text-center text-gray-700 font-mono text-xs">{{ formatId(row.id) }}</td>
              <td class="px-5 py-3 text-center text-gray-700">{{ row.nama_dokumen }}</td>
              <td class="px-5 py-3 text-center text-gray-700">{{ row.pengunggah || '—' }}</td>
              <td class="px-5 py-3 text-center text-gray-700">{{ row.cabang || '—' }}</td>
              <td class="px-5 py-3 text-center text-gray-700">{{ row.nama_template || '—' }}</td>
              <td class="px-5 py-3 text-center text-gray-500">{{ formatTanggal(row.created_at) }}</td>
              <td v-if="user.role === 'admin'" class="px-5 py-3 text-center">
                <span
                  class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold"
                  :class="badgeClass(row.status)"
                >
                  <!-- Spinner Memuat -->
                  <svg v-if="row.status === 'Memuat'" class="animate-spin h-3 w-3"
                    xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-30" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
                  </svg>
                  {{ labelStatus(row.status) }}
                </span>
              </td>
              <td class="px-5 py-3 text-center">
                <button
                  @click="lihatDetail(row.id)"
                  class="text-blue-500 hover:text-blue-700 font-medium hover:underline transition"
                >
                  Detail
                </button>
              </td>
            </tr>

            <tr v-if="!loading && !errorMsg && paginatedData.length === 0">
              <td :colspan="user.role === 'admin' ? 8 : 7" class="px-5 py-10 text-center text-gray-400 text-sm">
                Tidak ada data ditemukan.
              </td>
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

    <!-- Modal Download Data Dokumen -->
    <div
      v-if="showDownloadModal"
      @click.self="closeDownloadModal"
      class="fixed inset-0 z-50 flex items-center justify-center"
      style="background: rgba(0,0,0,0.35);"
    >
      <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-md mx-6 p-8">
        <h2 class="text-xl font-bold text-gray-800 mb-4">Download Data Dokumen</h2>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Tanggal Mulai</label>
            <input v-model="downloadStartDate" type="date" class="w-full px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent" :class="{'border-red-500 focus:ring-red-400': errorStartDate}" />
            <p v-if="errorStartDate" class="text-red-500 text-xs mt-1">Tanggal mulai harus terisi</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Tanggal Selesai</label>
            <input v-model="downloadEndDate" :min="downloadStartDate" type="date" class="w-full px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent" :class="{'border-red-500 focus:ring-red-400': errorEndDate}" />
            <p v-if="errorEndDate" class="text-red-500 text-xs mt-1">Tanggal selesai harus terisi</p>
          </div>
        </div>
        <div class="mt-6 flex justify-end gap-2">
          <button @click="closeDownloadModal" :disabled="isDownloading" class="px-4 py-2 text-sm font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed">Batal</button>
          <button @click="handleDownload" :disabled="isDownloading" class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-gray-900 rounded-lg hover:bg-gray-800 transition cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed">
            <svg v-if="isDownloading" class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg>
            {{ isDownloading ? 'Menyimpan...' : 'Simpan' }}
          </button>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
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

const showDownloadModal = ref(false)
const downloadStartDate = ref('')
const downloadEndDate   = ref('')
const errorStartDate    = ref(false)
const errorEndDate      = ref(false)
const isDownloading     = ref(false)

const sortOptions = [
  { label: 'A - Z (Menurun)',   value: 'az-desc'  },
  { label: 'A - Z (Menaik)',    value: 'az-asc'   },
  { label: 'ID (Menurun)',      value: 'id-desc'  },
  { label: 'ID (Menaik)',       value: 'id-asc'   },
  { label: 'Tanggal (Menurun)', value: 'tgl-desc' },
  { label: 'Tanggal (Menaik)',  value: 'tgl-asc'  },
]

// Fetch data
async function fetchData(silent = false) {
  if (!silent) loading.value = true
  errorMsg.value = ''
  try {
    const token = localStorage.getItem('token')
    const res   = await axios.get('/api/beranda/dokumen', {
      headers: { Authorization: `Bearer ${token}` }
    })
    allData.value = res.data
  } catch (err) {
    if (!silent) {
      errorMsg.value = err.response?.status === 401
        ? 'Sesi habis. Silakan login ulang.'
        : 'Gagal memuat data. Coba muat ulang halaman.'
    }
  } finally {
    if (!silent) loading.value = false
  }
}

let pollingTimer = null

function startPollingIfNeeded() {
  const hasMemuat = allData.value.some(r => r.status === 'Memuat')
  if (hasMemuat && !pollingTimer) {
    pollingTimer = setInterval(async () => {
      await fetchData(true)
      const stillMemuat = allData.value.some(r => r.status === 'Memuat')
      if (!stillMemuat) {
        clearInterval(pollingTimer)
        pollingTimer = null
      }
    }, 5000)
  }
}

// Format helpers
function formatId(id) { return 'D-' + String(id).padStart(6, '0') }
function formatTanggal(iso) {
  if (!iso) return '-'
  const d = new Date(iso)
  return `${String(d.getDate()).padStart(2,'0')}/${String(d.getMonth()+1).padStart(2,'0')}/${d.getFullYear()}`
}

// Status dari backend: "Benar" | "Salah" | "Memuat" | "Error"
function badgeClass(status) {
  switch (status) {
    case 'Benar':   return 'bg-green-100 text-green-700'
    case 'Salah':   return 'bg-red-100 text-red-600'
    case 'Memuat': return 'bg-gray-100 text-gray-500'
    case 'Error':   return 'bg-orange-100 text-orange-600'
    default:        return 'bg-gray-100 text-gray-500'
  }
}

function labelStatus(status) {
  switch (status) {
    case 'Benar':   return 'Benar'
    case 'Salah':   return 'Salah'
    case 'Memuat': return 'Memuat'
    case 'Error':   return 'Error'
    default:        return status || '—'
  }
}

const filteredData = computed(() => {
  const q = searchQuery.value.toLowerCase().trim()
  if (!q) return allData.value
  return allData.value.filter(row =>
    formatId(row.id).toLowerCase().includes(q) ||
    row.nama_dokumen?.toLowerCase().includes(q) ||
    row.pengunggah?.toLowerCase().includes(q) ||
    row.nama_template?.toLowerCase().includes(q) ||
    formatTanggal(row.created_at).includes(q) ||
    row.status?.toLowerCase().includes(q)
  )
})

const sortedData = computed(() => {
  const data = [...filteredData.value]
  switch (sortKey.value) {
    case 'az-asc':   return data.sort((a, b) => a.nama_dokumen.localeCompare(b.nama_dokumen))
    case 'az-desc':  return data.sort((a, b) => b.nama_dokumen.localeCompare(a.nama_dokumen))
    case 'id-asc':   return data.sort((a, b) => a.id - b.id)
    case 'id-desc':  return data.sort((a, b) => b.id - a.id)
    case 'tgl-asc':  return data.sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
    case 'tgl-desc': return data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    default:         return data
  }
})

const totalPages    = computed(() => Math.ceil(sortedData.value.length / itemsPerPage) || 1)
const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return sortedData.value.slice(start, start + itemsPerPage)
})

// Sort
let hideTimeout = null
function handleMouseEnter() {
  if (hideTimeout) { clearTimeout(hideTimeout); hideTimeout = null }
  showUrutDropdown.value = true
}
function handleMouseLeave() {
  hideTimeout = setTimeout(() => { showUrutDropdown.value = false }, 150)
}
function selectSort(value) {
  sortKey.value = sortKey.value === value ? '' : value
  showUrutDropdown.value = false
  currentPage.value = 1
}

// Pagination
function goToPage(page) { currentPage.value = Math.max(1, Math.min(page, totalPages.value)) }
function onPageInputChange(e) {
  const val = parseInt(e.target.value)
  if (!isNaN(val)) goToPage(val)
  e.target.value = currentPage.value
}

function lihatDetail(id) { router.push(`/beranda/detail/${id}`) }

async function handleDownload() {
  errorStartDate.value = !downloadStartDate.value
  errorEndDate.value   = !downloadEndDate.value

  if (errorStartDate.value || errorEndDate.value) return

  isDownloading.value = true
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get('/api/beranda/download-dokumen', {
      headers: { Authorization: `Bearer ${token}` },
      params: { start_date: downloadStartDate.value, end_date: downloadEndDate.value },
      responseType: 'blob'
    })

    const url = window.URL.createObjectURL(new Blob([res.data]))
    const link = document.createElement('a')
    link.href = url
    
    const formatTanggal = (iso) => {
      if (!iso) return ''
      const parts = iso.split('-')
      if (parts.length === 3) return `${parts[2]}-${parts[1]}-${parts[0]}`
      return iso
    }
    const tglMulai = formatTanggal(downloadStartDate.value)
    const tglSelesai = formatTanggal(downloadEndDate.value)
    
    let filename = `Dokumen_${tglMulai}_${tglSelesai}.xlsx`
    const disposition = res.headers['content-disposition']
    if (disposition && disposition.includes('filename=')) {
      const match = disposition.match(/filename="?([^"]+)"?/)
      if (match && match[1]) filename = match[1]
    }

    link.setAttribute('download', filename)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)

    closeDownloadModal()
  } catch (err) {
    console.error('Gagal mendownload data:', err)
    alert('Gagal mendownload data. Pastikan tanggal benar dan data tersedia.')
  } finally {
    isDownloading.value = false
  }
}

function closeDownloadModal() {
  showDownloadModal.value = false
  errorStartDate.value = false
  errorEndDate.value = false
  downloadStartDate.value = ''
  downloadEndDate.value = ''
}

watch(downloadStartDate, (newVal) => {
  if (downloadEndDate.value && newVal > downloadEndDate.value) {
    downloadEndDate.value = newVal
  }
})

watch(searchQuery, () => { currentPage.value = 1 })

watch(allData, () => startPollingIfNeeded(), { deep: false })

onMounted(async () => {
  await fetchData()
  startPollingIfNeeded()
})

onBeforeUnmount(() => {
  if (pollingTimer) { clearInterval(pollingTimer); pollingTimer = null }
})
</script>