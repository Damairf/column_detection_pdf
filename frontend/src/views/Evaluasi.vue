<template>
  <AppLayout>
    <div class="flex flex-col min-h-full">
      <div class="flex flex-col gap-2 mb-4">

        <!-- Cari (kiri) + Ekspor + Urut (kanan) -->
        <div class="flex items-center justify-between">
          <div class="relative mb-1.5">
            <span class="absolute inset-y-0 left-3 flex items-center text-gray-400 pointer-events-none">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35m0 0A7.5 7.5 0 1010.5 18a7.5 7.5 0 006.15-3.35z" />
              </svg>
            </span>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Cari...."
              class="pl-9 pr-4 py-2 w-64 border border-gray-300 rounded-lg text-sm text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent bg-white shadow-sm"
            />
          </div>

          <div class="flex items-center gap-2">
            <!-- Ekspor -->
            <button
              @click="handleEkspor"
              :disabled="isExporting"
              class="cursor-pointer flex items-center gap-1.5 px-4 py-2 border border-gray-300 bg-white text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-50 transition shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <svg v-if="isExporting" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              {{ isExporting ? 'Mengekspor...' : 'Ekspor' }}
            </button>

            <!-- Urut -->
            <div class="relative" @mouseenter="handleMouseEnter" @mouseleave="handleMouseLeave">
              <button class="flex items-center gap-1.5 px-4 py-2 bg-gray-900 text-white text-sm font-medium rounded-lg hover:bg-gray-800 transition shadow-sm">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V4m0 0L3 8m4-4l4 4M17 8v12m0 0l4-4m-4 4l-4-4" />
                </svg>
                Urut
              </button>
              <div v-if="showUrutDropdown" class="absolute right-0 top-full mt-1.5 w-48 bg-white border border-gray-200 rounded-lg shadow-lg z-50 overflow-hidden">
                <button
                  v-for="opt in sortOptions" :key="opt.value"
                  @click="selectSort(opt.value)"
                  class="cursor-pointer w-full text-left px-4 py-2.5 text-sm transition"
                  :class="sortKey === opt.value ? 'bg-gray-900 text-white font-medium' : 'text-gray-700 hover:bg-gray-100'"
                >
                  {{ opt.label }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Pilih Cabang + Tag -->
        <div class="flex flex-wrap items-center gap-2 w-full">
          <!-- Dropdown Pilih Cabang -->
          <div class="relative" ref="cabangDropdownRef">
            <button
              @click="toggleCabangDropdown"
              class="cursor-pointer flex items-center gap-1.5 px-4 py-2 bg-gray-900 text-white text-sm font-medium rounded-lg hover:bg-gray-800 transition shadow-sm whitespace-nowrap"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
              Pilih Cabang
            </button>

            <!-- Dropdown List -->
            <div
              v-if="showCabangDropdown"
              class="absolute left-0 top-full mt-1.5 w-56 bg-white border border-gray-200 rounded-lg shadow-lg z-50 flex flex-col overflow-hidden"
              style="max-height: 260px;"
            >
              <!-- Pilih Semua -->
              <div class="sticky top-0 bg-white border-b border-gray-100 z-10 shrink-0">
                <label class="flex items-center gap-2.5 px-4 py-2.5 cursor-pointer hover:bg-gray-50 transition select-none">
                  <input
                    type="checkbox"
                    :checked="semuaTerpilih"
                    :indeterminate.prop="sebagiannTerpilih"
                    @change="togglePilihSemua"
                    class="w-4 h-4 accent-gray-900 cursor-pointer"
                  />
                  <span class="text-sm font-semibold text-gray-700">Pilih Semua</span>
                </label>
              </div>
              <!-- List Cabang -->
              <div class="overflow-y-auto flex-1">
                <label
                  v-for="c in listCabang"
                  :key="c.id"
                  class="flex items-center gap-2.5 px-4 py-2.5 cursor-pointer hover:bg-gray-50 transition select-none"
                >
                  <input
                    type="checkbox"
                    :value="c.id"
                    v-model="selectedCabangIds"
                    class="w-4 h-4 accent-gray-900 cursor-pointer"
                  />
                  <span class="text-sm text-gray-700">{{ c.nama_cabang }}</span>
                </label>
                <div v-if="listCabang.length === 0" class="px-4 py-3 text-sm text-gray-400 text-center">
                  Memuat cabang...
                </div>
              </div>
            </div>
          </div>

          <!-- Tag Cabang Terpilih -->
          <template v-for="c in cabangTerpilih" :key="c.id">
            <span class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border border-gray-300 text-gray-700 text-sm font-medium rounded-lg shadow-sm">
              {{ c.nama_cabang }}
              <button
                @click="hapusCabang(c.id)"
                class="cursor-pointer text-gray-400 hover:text-gray-600 transition leading-none"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </span>
          </template>
        </div>

      </div>

      <!-- Tabel -->
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
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700">Kriteria</th>
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700">Benar</th>
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700">Skor</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading">
                <td colspan="9" class="px-5 py-10 text-center text-gray-400 text-sm">
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
                <td colspan="9" class="px-5 py-10 text-center text-red-400 text-sm">{{ errorMsg }}</td>
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
                <td class="px-5 py-3 text-center text-gray-700 font-medium">{{ row.kriteria }}</td>
                <td class="px-5 py-3 text-center text-gray-700 font-medium">{{ row.jml_benar }}/{{ row.kriteria }}</td>
                <td class="px-5 py-3 text-center font-medium text-blue-500">{{ row.skor }}%</td>
              </tr>

              <tr v-if="!loading && !errorMsg && paginatedData.length === 0">
                <td colspan="9" class="px-5 py-10 text-center text-gray-400 text-sm">
                  Tidak ada data ditemukan.
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div class="flex items-center justify-center gap-2 py-5 border-t border-gray-100">
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

          <input
            type="number" :value="currentPage"
            @change="onPageInputChange" @keydown.enter="onPageInputChange"
            min="1" :max="totalPages"
            class="w-12 h-9 text-center border border-gray-300 rounded-lg text-sm font-medium text-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
          />

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
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import axios from 'axios'
import AppLayout from '../components/AppLayout.vue'

const items      = ref([])
const listCabang = ref([])
const loading    = ref(false)
const errorMsg   = ref('')

const searchQuery      = ref('')
const currentPage      = ref(1)
const itemsPerPage     = 10
const showUrutDropdown = ref(false)
const sortKey          = ref('id-desc')
const isExporting      = ref(false)

const showCabangDropdown = ref(false)
const selectedCabangIds  = ref([])
const cabangDropdownRef  = ref(null)

const cabangTerpilih = computed(() =>
  listCabang.value.filter(c => selectedCabangIds.value.includes(c.id))
)

const semuaTerpilih = computed(() =>
  listCabang.value.length > 0 &&
  selectedCabangIds.value.length === listCabang.value.length
)

const sebagiannTerpilih = computed(() =>
  selectedCabangIds.value.length > 0 && !semuaTerpilih.value
)

function toggleCabangDropdown() {
  showCabangDropdown.value = !showCabangDropdown.value
}

function togglePilihSemua() {
  if (semuaTerpilih.value) {
    selectedCabangIds.value = []
  } else {
    selectedCabangIds.value = listCabang.value.map(c => c.id)
  }
}

function hapusCabang(id) {
  selectedCabangIds.value = selectedCabangIds.value.filter(cid => cid !== id)
}

function handleClickOutside(e) {
  if (cabangDropdownRef.value && !cabangDropdownRef.value.contains(e.target)) {
    showCabangDropdown.value = false
  }
}

const sortOptions = [
  { label: 'A - Z (Menurun)',   value: 'az-desc'  },
  { label: 'A - Z (Menaik)',    value: 'az-asc'   },
  { label: 'ID (Menurun)',      value: 'id-desc'  },
  { label: 'ID (Menaik)',       value: 'id-asc'   },
  { label: 'Tanggal (Menurun)', value: 'tgl-desc' },
  { label: 'Tanggal (Menaik)',  value: 'tgl-asc'  },
]

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

function formatId(id) {
  return id ? `D-${String(id).padStart(6, '0')}` : '-'
}
function formatTanggal(isoString) {
  if (!isoString) return '-'
  const d = new Date(isoString)
  return `${String(d.getDate()).padStart(2, '0')}/${String(d.getMonth() + 1).padStart(2, '0')}/${d.getFullYear()}`
}

async function fetchEvaluasi() {
  loading.value = true
  errorMsg.value = ''
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get('/api/evaluasi/', { headers: { Authorization: `Bearer ${token}` } })
    items.value = res.data
  } catch (err) {
    if (err.response && err.response.status === 403) {
      errorMsg.value = 'Akses ditolak.'
    } else {
      errorMsg.value = 'Gagal memuat data evaluasi.'
    }
    console.error(err)
  } finally {
    loading.value = false
  }
}

async function fetchCabang() {
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get('/api/pengguna/cabang', { headers: { Authorization: `Bearer ${token}` } })
    listCabang.value = res.data
  } catch (err) {
    console.error('Gagal memuat data cabang:', err)
  }
}

async function handleEkspor() {
  if (selectedCabangIds.value.length === 0) {
    alert('Pilih cabang terlebih dahulu.')
    return
  }
  isExporting.value = true
  try {
    const token = localStorage.getItem('token')

    const params = new URLSearchParams()
    selectedCabangIds.value.forEach(id => params.append('cabang_ids', id))

    const res = await axios.get(`/api/evaluasi/ekspor?${params.toString()}`, {
      headers: { Authorization: `Bearer ${token}` },
      responseType: 'blob'
    })

    const url  = window.URL.createObjectURL(new Blob([res.data]))
    const link = document.createElement('a')
    link.href  = url

    const now  = new Date()
    const dd   = String(now.getDate()).padStart(2, '0')
    const mm   = String(now.getMonth() + 1).padStart(2, '0')
    const yyyy = now.getFullYear()
    let filename = `Evaluasi_Dokumen_${dd}-${mm}-${yyyy}.xlsx`

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
  } catch (err) {
    console.error('Gagal mengekspor data:', err)
    alert('Gagal mengekspor data. Coba lagi.')
  } finally {
    isExporting.value = false
  }
}

onMounted(() => {
  fetchEvaluasi()
  fetchCabang()
  document.addEventListener('mousedown', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('mousedown', handleClickOutside)
})

watch(searchQuery,      () => { currentPage.value = 1 })
watch(selectedCabangIds, () => { currentPage.value = 1 })

const filteredData = computed(() => {
  let data = items.value

  if (selectedCabangIds.value.length === 0) {
    return []
  }

  const namaCabangTerpilih = new Set(
    listCabang.value
      .filter(c => selectedCabangIds.value.includes(c.id))
      .map(c => c.nama_cabang)
  )
  data = data.filter(row => namaCabangTerpilih.has(row.cabang))

  const q = searchQuery.value.toLowerCase().trim()
  if (q) {
    data = data.filter(row =>
      formatId(row.id).toLowerCase().includes(q) ||
      (row.nama_dokumen  || '').toLowerCase().includes(q) ||
      (row.pengunggah    || '').toLowerCase().includes(q) ||
      (row.cabang        || '').toLowerCase().includes(q) ||
      (row.nama_template || '').toLowerCase().includes(q) ||
      formatTanggal(row.created_at).includes(q)
    )
  }

  return data
})

const sortedData = computed(() => {
  const data = [...filteredData.value]
  switch (sortKey.value) {
    case 'az-asc':   return data.sort((a, b) => (a.nama_dokumen || '').localeCompare(b.nama_dokumen || ''))
    case 'az-desc':  return data.sort((a, b) => (b.nama_dokumen || '').localeCompare(a.nama_dokumen || ''))
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

function goToPage(page) {
  currentPage.value = Math.max(1, Math.min(page, totalPages.value))
}
function onPageInputChange(e) {
  const val = parseInt(e.target.value)
  if (!isNaN(val)) goToPage(val)
  e.target.value = currentPage.value
}
</script>