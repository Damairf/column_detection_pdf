<template>
  <AppLayout>
    <div class="flex flex-col min-h-full">

      <!-- Kembali + Ubah + Hapus -->
      <div class="flex items-center justify-between mb-5">
        <!-- Kiri -->
        <button
          @click="router.replace('/spk')"
          class="cursor-pointer px-4 py-2 bg-gray-900 text-white text-sm font-semibold rounded-lg hover:bg-gray-700 transition shadow-sm"
        >
          Kembali
        </button>

        <!-- Kanan -->
        <div class="flex items-center gap-2">
          <button
            @click="openEditModal"
            class="cursor-pointer px-4 py-2 border border-gray-300 bg-white text-gray-700 text-sm font-semibold rounded-lg hover:bg-gray-50 transition shadow-sm"
          >
            Ubah
          </button>
          <button
            @click="openDeleteModal"
            class="cursor-pointer px-4 py-2 bg-red-600 text-white text-sm font-semibold rounded-lg hover:bg-red-700 transition shadow-sm"
          >
            Hapus
          </button>
        </div>
      </div>

      <!-- Card Info SPK -->
      <div class="bg-white rounded-xl border border-gray-200 shadow-sm p-7 mb-5">
        <div class="grid grid-cols-3 gap-5">

          <!-- Nomor SPK -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Nomor SPK</label>
            <div class="px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 select-none">
              {{ spk?.id || '—' }}
            </div>
          </div>

          <!-- Nama SPK -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Nama SPK</label>
            <div class="px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 select-none">
              {{ spk?.nama_spk || '—' }}
            </div>
          </div>

          <!-- Tanggal Retail -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Tanggal Retail</label>
            <div class="px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 select-none">
              {{ formatTanggal(spk?.tgl_retail) }}
            </div>
          </div>

        </div>
      </div>

      <!-- Search + Urut -->
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
          <div
            v-if="showUrutDropdown"
            class="absolute right-0 top-full mt-1.5 w-48 bg-white border border-gray-200 rounded-lg shadow-lg z-50 overflow-hidden"
          >
            <button
              v-for="opt in sortOptions"
              :key="opt.value"
              @click="selectSort(opt.value)"
              class="w-full text-left px-4 py-2.5 text-sm transition"
              :class="sortKey === opt.value ? 'bg-gray-900 text-white font-medium' : 'text-gray-700 hover:bg-gray-100'"
            >
              {{ opt.label }}
            </button>
          </div>
        </div>

      </div>

      <!-- Tabel Dokumen -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div class="px-5 py-4 border-b border-gray-100 font-semibold text-gray-700">Daftar Dokumen SPK</div>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b border-gray-200 bg-gray-50">
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700 w-28">ID</th>
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700">Nama Dokumen</th>
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700">Pengunggah</th>
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700">Cabang</th>
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700">Nama Template</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loadingDokumen">
                <td colspan="5" class="px-5 py-10 text-center text-gray-400 text-sm">
                  <div class="flex items-center justify-center gap-2">
                    <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                    </svg>
                    Memuat data...
                  </div>
                </td>
              </tr>
              <tr
                v-else
                v-for="dok in paginatedData"
                :key="dok.id"
                class="border-b border-gray-100 hover:bg-gray-50 transition-colors"
              >
                <td class="px-5 py-3 text-center text-gray-700 font-mono text-xs">{{ formatId(dok.id) }}</td>
                <td class="px-5 py-3 text-center text-gray-700">{{ dok.nama_dokumen }}</td>
                <td class="px-5 py-3 text-center text-gray-700">{{ dok.pengunggah || '—' }}</td>
                <td class="px-5 py-3 text-center text-gray-700">{{ dok.cabang || '—' }}</td>
                <td class="px-5 py-3 text-center text-gray-700">{{ dok.nama_template || '—' }}</td>
              </tr>
              <tr v-if="!loadingDokumen && paginatedData.length === 0">
                <td colspan="5" class="px-5 py-10 text-center text-gray-400 text-sm">
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
            type="number"
            :value="currentPage"
            @change="onPageInputChange"
            @keydown.enter="onPageInputChange"
            min="1"
            :max="totalPages"
            class="w-12 h-9 text-center border border-gray-300 rounded-lg text-sm font-medium text-gray-700
                  focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent
                  [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
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

    <!-- Modal Ubah SPK -->
    <div
      v-if="showEditModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
      @click.self="closeEditModal"
    >
      <div class="bg-white rounded-2xl w-full max-w-lg p-6 shadow-xl relative">
        <h2 class="text-xl font-bold text-gray-800 mb-6">Ubah SPK</h2>
        <form @submit.prevent="handleUpdate">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Nomor SPK</label>
              <input
                :value="spk?.id"
                disabled
                type="text"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg text-sm bg-gray-100 cursor-not-allowed"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Nama SPK</label>
              <input
                v-model="form.nama_spk"
                required
                type="text"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent bg-gray-50"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Tanggal Retail</label>
              <input
                v-model="form.tgl_retail"
                required
                type="date"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent bg-gray-50"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Pilih Template</label>
              <div class="max-h-40 overflow-y-auto border border-gray-300 rounded-lg p-2 bg-gray-50">
                <label
                  v-for="t in listTemplate"
                  :key="t.id"
                  class="flex items-center gap-2 mb-2 cursor-pointer"
                >
                  <input
                    type="radio"
                    :value="t.id"
                    v-model="form.template_id"
                    name="template"
                    class="w-4 h-4 text-gray-900 border-gray-300 focus:ring-gray-900"
                  />
                  <span class="text-sm text-gray-700">{{ t.nama_template }}</span>
                </label>
                <div v-if="listTemplate.length === 0" class="text-sm text-gray-400 text-center py-2">
                  Tidak ada template tersedia.
                </div>
              </div>
            </div>
          </div>
          <div v-if="formError" class="mt-4 text-red-500 text-sm">{{ formError }}</div>
          <div class="mt-8 flex justify-end gap-3">
            <button
              type="button"
              @click="closeEditModal"
              class="cursor-pointer px-5 py-2 text-sm font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition"
            >
              Batal
            </button>
            <button
              type="submit"
              :disabled="saving"
              class="cursor-pointer px-5 py-2 text-sm font-medium text-white bg-gray-900 rounded-lg hover:bg-gray-800 transition disabled:opacity-50"
            >
              {{ saving ? 'Menyimpan...' : 'Simpan' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Hapus -->
    <div v-if="showDeleteModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div class="bg-white rounded-2xl w-full max-w-md p-6 text-center shadow-lg">

        <!-- Icon -->
        <div class="flex justify-center mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6M9 7h6m-1-3H10a1 1 0 00-1 1v1h6V5a1 1 0 00-1-1z" />
          </svg>
        </div>

        <!-- Teks -->
        <h2 class="text-lg font-semibold text-gray-800 mb-2">
          Apakah anda yakin ingin menghapusnya?
        </h2>
        <p class="text-sm text-gray-500 mb-6">
          Data yang sudah dihapus tidak dapat dipulihkan kembali
        </p>

        <!-- Tombol -->
        <div class="flex justify-center gap-3">
          <button
            @click="showDeleteModal = false"
            :disabled="deleting"
            class="px-5 py-2 bg-gray-800 text-white rounded-lg text-sm font-semibold hover:bg-gray-700 disabled:opacity-50"
          >
            Batal
          </button>
          <button
            @click="handleDelete"
            :disabled="deleting"
            class="flex items-center justify-center gap-2 px-5 py-2 bg-red-600 text-white rounded-lg text-sm font-semibold hover:bg-red-700 disabled:opacity-50"
          >
            <svg v-if="deleting" class="animate-spin h-4 w-4" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10" stroke="white" stroke-width="3" fill="none"/>
            </svg>
            {{ deleting ? 'Menghapus...' : 'Hapus' }}
          </button>
        </div>

      </div>
    </div>

  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import AppLayout from '../components/AppLayout.vue'

const route  = useRoute()
const router = useRouter()
const spkId  = route.params.id

const spk          = ref(null)
const dokumenList  = ref([])
const listTemplate = ref([])

const loadingSPK     = ref(false)
const loadingDokumen = ref(false)

const showEditModal   = ref(false)
const showDeleteModal = ref(false)
const form     = ref({ nama_spk: '', tgl_retail: '', template_id: null })
const saving   = ref(false)
const deleting = ref(false)
const formError = ref('')

// ── Search, Sort, Pagination ──────────────────────────────────────────
const searchQuery      = ref('')
const currentPage      = ref(1)
const itemsPerPage     = 10
const sortKey          = ref('id-desc')
const showUrutDropdown = ref(false)

const sortOptions = [
  { label: 'A - Z (Menurun)',   value: 'az-desc'  },
  { label: 'A - Z (Menaik)',    value: 'az-asc'   },
  { label: 'ID (Menurun)',      value: 'id-desc'  },
  { label: 'ID (Menaik)',       value: 'id-asc'   },
]

const filteredData = computed(() => {
  const q = searchQuery.value.toLowerCase().trim()
  if (!q) return dokumenList.value
  return dokumenList.value.filter(dok =>
    formatId(dok.id).toLowerCase().includes(q)      ||
    dok.nama_dokumen?.toLowerCase().includes(q)      ||
    dok.pengunggah?.toLowerCase().includes(q)        ||
    dok.cabang?.toLowerCase().includes(q)            ||
    dok.nama_template?.toLowerCase().includes(q)
  )
})

const sortedData = computed(() => {
  const data = [...filteredData.value]
  switch (sortKey.value) {
    case 'az-asc':  return data.sort((a, b) => a.nama_dokumen.localeCompare(b.nama_dokumen))
    case 'az-desc': return data.sort((a, b) => b.nama_dokumen.localeCompare(a.nama_dokumen))
    case 'id-asc':  return data.sort((a, b) => a.id - b.id)
    case 'id-desc': return data.sort((a, b) => b.id - a.id)
    default:        return data
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
  hideTimeout = setTimeout(() => { showUrutDropdown.value = false }, 150)
}
function selectSort(value) {
  sortKey.value = sortKey.value === value ? '' : value
  showUrutDropdown.value = false
  currentPage.value = 1
}

function goToPage(page) {
  currentPage.value = Math.max(1, Math.min(page, totalPages.value))
}
function onPageInputChange(e) {
  const val = parseInt(e.target.value)
  if (!isNaN(val)) goToPage(val)
  e.target.value = currentPage.value
}

// ── Helpers ───────────────────────────────────────────────────────────
function formatId(id) {
  return id ? `D-${String(id).padStart(6, '0')}` : '—'
}
function formatTanggal(isoString) {
  if (!isoString) return '—'
  const d = new Date(isoString)
  return `${String(d.getDate()).padStart(2,'0')}/${String(d.getMonth()+1).padStart(2,'0')}/${d.getFullYear()}`
}

// ── Fetch ─────────────────────────────────────────────────────────────
async function fetchData() {
  loadingSPK.value     = true
  loadingDokumen.value = true
  const token = localStorage.getItem('token')

  try {
    const resSPK = await axios.get(`/api/spk/${spkId}`, { headers: { Authorization: `Bearer ${token}` } })
    spk.value = resSPK.data
  } catch (err) {
    console.error('Gagal memuat SPK')
  } finally {
    loadingSPK.value = false
  }

  try {
    const resDok = await axios.get(`/api/beranda/dokumen?id_spk=${spkId}`, { headers: { Authorization: `Bearer ${token}` } })
    dokumenList.value = resDok.data
  } catch (err) {
    console.error('Gagal memuat dokumen')
  } finally {
    loadingDokumen.value = false
  }

  try {
    const resTemp = await axios.get('/api/template/list', { headers: { Authorization: `Bearer ${token}` } })
    listTemplate.value = resTemp.data
  } catch (err) {}
}

// ── Edit & Delete ─────────────────────────────────────────────────────
function openEditModal() {
  if (spk.value) {
    form.value = {
      nama_spk:    spk.value.nama_spk,
      tgl_retail:  spk.value.tgl_retail,
      template_id: spk.value.id_template ?? null
    }
  }
  formError.value     = ''
  showEditModal.value = true
}

function closeEditModal() { showEditModal.value = false }

async function handleUpdate() {
  saving.value     = true
  formError.value  = ''
  try {
    const token = localStorage.getItem('token')
    await axios.put(`/api/spk/${spkId}`, form.value, { headers: { Authorization: `Bearer ${token}` } })
    closeEditModal()
    fetchData()
  } catch (err) {
    formError.value = err.response?.data?.detail || 'Gagal mengubah SPK'
  } finally {
    saving.value = false
  }
}

function openDeleteModal() { showDeleteModal.value = true }

async function handleDelete() {
  deleting.value = true
  try {
    const token = localStorage.getItem('token')
    await axios.delete(`/api/spk/${spkId}`, { headers: { Authorization: `Bearer ${token}` } })
    showDeleteModal.value = false
    router.push('/spk')
  } catch (err) {
    alert('Gagal menghapus SPK')
  } finally {
    deleting.value = false
  }
}

// ── Lifecycle ─────────────────────────────────────────────────────────
watch(searchQuery, () => { currentPage.value = 1 })

onMounted(() => fetchData())

onBeforeUnmount(() => {
  if (hideTimeout) clearTimeout(hideTimeout)
})
</script>
