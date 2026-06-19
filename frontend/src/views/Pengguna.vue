<template>
  <AppLayout>
    <div class="flex flex-col min-h-full">
      <!-- Cari + Urut + Tambah -->
      <div class="flex items-center justify-between mb-4">
        <div class="relative">
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

          <!-- Tambah -->
          <button
            @click="openAddModal"
            class="cursor-pointer flex items-center gap-1.5 px-4 py-2 border border-gray-300 bg-white text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-50 transition shadow-sm"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Tambah
          </button>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b border-gray-200 bg-white">
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700">Nama</th>
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700">Username</th>
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700">Divisi</th>
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700">Cabang</th>
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700 w-32">Tanggal</th>
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700 w-28">Role</th>
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700 w-24">Aksi</th>
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
                <td colspan="7" class="px-5 py-10 text-center text-red-500 text-sm">{{ errorMsg }}</td>
              </tr>
              <tr v-else-if="paginatedData.length === 0">
                <td colspan="7" class="px-5 py-10 text-center text-gray-400 text-sm">Tidak ada data ditemukan.</td>
              </tr>
              <tr v-else v-for="u in paginatedData" :key="u.id" class="border-b border-gray-100 hover:bg-gray-50 transition-colors">
                <td class="px-5 py-3 text-center text-gray-700 font-medium">{{ u.nama }}</td>
                <td class="px-5 py-3 text-center text-gray-700">{{ u.username }}</td>
                <td class="px-5 py-3 text-center text-gray-700">{{ u.divisi }}</td>
                <td class="px-5 py-3 text-center text-gray-700">{{ u.cabang || '-' }}</td>
                <td class="px-5 py-3 text-center text-gray-500">{{ formatTanggal(u.created_at) }}</td>
                <td class="px-5 py-3 text-center">
                  <span
                    class="px-3 py-1 rounded-full text-xs font-semibold capitalize"
                    :class="u.role === 'admin' ? 'bg-blue-100 text-blue-700' : 'bg-green-100 text-green-700'"
                  >
                    {{ u.role }}
                  </span>
                </td>
                <td class="px-5 py-3 text-center flex items-center justify-center gap-3">
                  <button @click="openEditModal(u)" class="cursor-pointer text-gray-500 hover:text-gray-600 transition" title="Edit">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button v-if="u.username !== 'admin' && u.id !== currentUser.id" @click="openDeleteModal(u)" class="cursor-pointer text-red-500 hover:text-red-600 transition" title="Hapus">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6M9 7h6m-1-3H10a1 1 0 00-1 1v1h6V5a1 1 0 00-1-1z" />
                    </svg>
                  </button>
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
      <!-- <div class="mt-auto pt-6 text-xs text-gray-400 text-center border-t border-gray-100">
        Sistem ini bisa melakukan kesalahan. Silahkan periksa kembali hasilnya
      </div> -->
    </div>

    <!-- Modal Form -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40" @click.self="closeModal">
      <div class="bg-white rounded-2xl w-full max-w-md p-6 shadow-xl relative">
        <h2 class="text-xl font-bold text-gray-800 mb-6">{{ isEdit ? 'Edit Pengguna' : 'Tambah Pengguna' }}</h2>
        <form @submit.prevent="handleSimpan">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Nama Lengkap</label>
              <input v-model="form.nama" required type="text" class="w-full px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent bg-gray-50" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Username</label>
              <input v-model="form.username" required type="text" class="w-full px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent bg-gray-50" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Divisi</label>
              <input v-model="form.divisi" required type="text" class="w-full px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent bg-gray-50" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Role</label>
              <select v-model="form.role" :disabled="isEdit && form.id === currentUser.id" class="w-full px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
                <option value="user">User</option>
                <option value="admin">Admin</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Cabang</label>
              <select v-model="form.id_cabang" required class="w-full px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent bg-gray-50">
                <option :value="null" disabled>Pilih Cabang</option>
                <option v-for="c in listCabang" :key="c.id" :value="c.id">{{ c.nama_cabang }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Password <span v-if="isEdit" class="text-gray-400 font-normal">(kosongkan jika tidak diubah)</span></label>
              <input v-model="form.password" :required="!isEdit" type="password" class="w-full px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent bg-gray-50" />
            </div>
          </div>
          <div v-if="formError" class="mt-4 text-red-500 text-sm">{{ formError }}</div>
          <div class="mt-8 flex justify-end gap-3">
            <button type="button" @click="closeModal" class="cursor-pointer px-5 py-2 text-sm font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition">Batal</button>
            <button type="submit" :disabled="saving" class="cursor-pointer flex items-center gap-2 px-5 py-2 text-sm font-medium text-white bg-gray-900 rounded-lg hover:bg-gray-800 transition disabled:opacity-50">
              <span v-if="saving" class="flex items-center gap-2">
                <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                </svg>
                Menyimpan...
              </span>
              <span v-else>Simpan</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Konfirmasi Hapus -->
    <div v-if="showDeleteModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div class="bg-white rounded-2xl w-full max-w-md p-6 text-center shadow-lg">
        <div class="flex justify-center mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6M9 7h6m-1-3H10a1 1 0 00-1 1v1h6V5a1 1 0 00-1-1z" />
          </svg>
        </div>
        <h2 class="text-lg font-semibold text-gray-800 mb-2">
          Apakah anda yakin ingin menghapusnya?
        </h2>
        <p class="text-sm text-gray-500 mb-6">
          Data pengguna yang sudah dihapus tidak dapat dipulihkan kembali
        </p>
        <div class="flex justify-center gap-3">
          <button
            @click="showDeleteModal = false"
            :disabled="deleting"
            class="cursor-pointer px-5 py-2 bg-gray-800 text-white rounded-lg text-sm font-semibold hover:bg-gray-700 transition disabled:opacity-50"
          >
            Batal
          </button>
          <button
            @click="confirmDelete"
            :disabled="deleting"
            class="cursor-pointer flex items-center justify-center gap-2 px-5 py-2 bg-red-600 text-white rounded-lg text-sm font-semibold hover:bg-red-700 transition disabled:opacity-50"
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
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import AppLayout from '../components/AppLayout.vue'

const users = ref([])
const listCabang = ref([])
const loading = ref(false)
const errorMsg = ref('')

const searchQuery = ref('')
const currentPage = ref(1)
const totalPages = ref(1)
const itemsPerPage = 10
const showUrutDropdown = ref(false)
const sortKey = ref('tgl-desc')

const sortOptions = [
  { label: 'A - Z (Menurun)',   value: 'az-desc'  },
  { label: 'A - Z (Menaik)',    value: 'az-asc'   },
  { label: 'Tanggal (Menurun)', value: 'tgl-desc' },
  { label: 'Tanggal (Menaik)',  value: 'tgl-asc'  },
]

const showModal = ref(false)
const isEdit = ref(false)
const saving = ref(false)
const formError = ref('')

const showDeleteModal = ref(false)
const deleting = ref(false)
const selectedUser = ref(null)

const currentUser = computed(() => {
  try {
    return JSON.parse(localStorage.getItem('user')) || {}
  } catch {
    return {}
  }
})

const form = ref({ id: null, nama: '', username: '', divisi: '', role: 'user', id_cabang: null, password: '' })

async function fetchUsers() {
  loading.value = true
  errorMsg.value = ''
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get('/api/pengguna/', { 
      headers: { Authorization: `Bearer ${token}` },
      params: {
        page: currentPage.value,
        limit: itemsPerPage,
        search: searchQuery.value
      }
    })
    users.value = res.data.data
    totalPages.value = Math.ceil(res.data.total / itemsPerPage) || 1
  } catch (err) {
    errorMsg.value = 'Gagal memuat data pengguna.'
  } finally {
    loading.value = false
  }
}

async function fetchCabang() {
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get('/api/pengguna/cabang', { headers: { Authorization: `Bearer ${token}` } })
    listCabang.value = res.data.slice().sort((a, b) =>
      a.nama_cabang.localeCompare(b.nama_cabang)
    )
  } catch (err) {
    console.error('Gagal memuat data cabang:', err)
  }
}

onMounted(() => {
  fetchUsers()
  fetchCabang()
})

let searchTimeout = null
watch(searchQuery, () => {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    currentPage.value = 1
    fetchUsers()
  }, 400)
})

watch(currentPage, () => fetchUsers())

function formatTanggal(isoString) {
  if (!isoString) return '-'
  const d = new Date(isoString)
  return `${String(d.getDate()).padStart(2,'0')}/${String(d.getMonth()+1).padStart(2,'0')}/${d.getFullYear()}`
}

const sortedData = computed(() => {
  const data = [...users.value]
  return data.sort((a, b) => {
    const aIsMe = a.id === currentUser.value.id
    const bIsMe = b.id === currentUser.value.id
    if (aIsMe && !bIsMe) return -1
    if (bIsMe && !aIsMe) return  1

    if (a.role === 'admin' && b.role !== 'admin') return -1
    if (b.role === 'admin' && a.role !== 'admin') return 1

    switch (sortKey.value) {
      case 'az-asc':   return a.nama.localeCompare(b.nama)
      case 'az-desc':  return b.nama.localeCompare(a.nama)
      case 'tgl-asc':  return new Date(a.created_at) - new Date(b.created_at)
      case 'tgl-desc': return new Date(b.created_at) - new Date(a.created_at)
      default: return 0
    }
  })
})

const paginatedData = computed(() => sortedData.value)

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

function openAddModal() {
  isEdit.value = false
  form.value = { id: null, nama: '', username: '', divisi: '', role: 'user', id_cabang: null, password: '' }
  formError.value = ''
  showModal.value = true
}

function openEditModal(u) {
  isEdit.value = true
  form.value = { id: u.id, nama: u.nama, username: u.username, divisi: u.divisi, role: u.role, id_cabang: u.id_cabang || null, password: '' }
  formError.value = ''
  showModal.value = true
}

function closeModal() {
  showModal.value = false
}

async function handleSimpan() {
  formError.value = ''
  saving.value = true
  try {
    const token = localStorage.getItem('token')
    const payload = {
      nama: form.value.nama,
      username: form.value.username,
      divisi: form.value.divisi,
      role: form.value.role,
      id_cabang: form.value.id_cabang
    }
    if (form.value.password) payload.password = form.value.password

    if (isEdit.value) {
      await axios.put(`/api/pengguna/${form.value.id}`, payload, { headers: { Authorization: `Bearer ${token}` } })
    } else {
      await axios.post('/api/pengguna/', payload, { headers: { Authorization: `Bearer ${token}` } })
    }
    closeModal()
    fetchUsers()
  } catch (err) {
    formError.value = err.response?.data?.detail || 'Gagal menyimpan data.'
  } finally {
    saving.value = false
  }
}

function openDeleteModal(u) {
  selectedUser.value = u
  showDeleteModal.value = true
}

async function confirmDelete() {
  if (!selectedUser.value) return
  deleting.value = true
  try {
    const token = localStorage.getItem('token')
    await axios.delete(`/api/pengguna/${selectedUser.value.id}`, { headers: { Authorization: `Bearer ${token}` } })
    showDeleteModal.value = false
    fetchUsers()
  } catch (err) {
    alert('Gagal menghapus pengguna.')
  } finally {
    deleting.value = false
  }
}
</script>
