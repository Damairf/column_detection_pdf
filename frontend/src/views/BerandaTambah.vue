<template>
  <AppLayout>
    <div class="flex flex-col min-h-full">

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

      <!-- Search SPK -->
      <div class="mb-4">
        <label class="block text-sm font-semibold text-gray-700 mb-2">Nomor SPK</label>
        <div class="flex gap-2">
          <div class="relative flex-1">
            <span class="absolute inset-y-0 left-3 flex items-center text-gray-400 pointer-events-none">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35m0 0A7.5 7.5 0 1010.5 18a7.5 7.5 0 006.15-3.35z" />
              </svg>
            </span>
            <input
              v-model="searchSPK"
              type="text"
              placeholder="Cari nomor atau nama SPK..."
              class="w-full pl-9 pr-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent"
              @keydown.enter="handleCari"
            />
          </div>
          <button
            @click="handleCari"
            class="cursor-pointer px-4 py-2.5 bg-gray-900 text-white text-sm font-semibold rounded-lg hover:bg-gray-700 transition shadow-sm"
          >
            Cari SPK
          </button>
        </div>
        <p v-if="errorSPK" class="text-red-500 text-xs mt-1">{{ errorSPK }}</p>
      </div>

      <!-- Tabel SPK -->
      <div v-if="sudahCari" class="mb-6 border border-gray-200 rounded-xl overflow-hidden">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-gray-200 bg-gray-50">
              <th class="px-4 py-3 text-center font-semibold text-gray-700">Nomor SPK</th>
              <th class="px-4 py-3 text-center font-semibold text-gray-700">Nama SPK</th>
              <th class="px-4 py-3 text-center font-semibold text-gray-700">Tanggal Retail</th>
              <th class="px-4 py-3 text-center font-semibold text-gray-700 w-24">Aksi</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loadingSPK">
              <td colspan="4" class="px-4 py-8 text-center text-gray-400 text-sm">Memuat data...</td>
            </tr>
            <tr v-else-if="paginatedSPK.length === 0">
              <td colspan="4" class="px-4 py-8 text-center text-gray-400 text-sm">SPK tidak ditemukan.</td>
            </tr>
            <tr
              v-else
              v-for="s in paginatedSPK"
              :key="s.id"
              class="border-b border-gray-100 hover:bg-gray-50 transition-colors"
            >
              <td class="px-4 py-3 text-center text-gray-700 font-medium">{{ s.id }}</td>
              <td class="px-4 py-3 text-center text-gray-700">{{ s.nama_spk }}</td>
              <td class="px-4 py-3 text-center text-gray-500">{{ formatTanggal(s.tgl_retail) }}</td>
              <td class="px-4 py-3 text-center">
                <button
                  @click="pilihSPK(s)"
                  class="px-3 py-1.5 rounded-lg text-xs font-semibold transition"
                  :class="spkDipilih === s.id
                    ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
                    : 'bg-gray-900 text-white hover:bg-gray-700 cursor-pointer'"
                >
                  {{ spkDipilih === s.id ? 'Dipilih' : 'Pilih' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Pagination tabel SPK -->
        <div class="flex items-center justify-center gap-2 py-3 border-t border-gray-100">

          <!-- Max Prev -->
          <button
            @click="goToSpkPage(1)"
            :disabled="spkPageRef === 1"
            class="w-9 h-9 flex items-center justify-center rounded-lg font-bold transition"
            :class="spkPageRef === 1 ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-gray-900 text-white hover:bg-gray-700 cursor-pointer'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M11 19l-7-7 7-7M19 19l-7-7 7-7" />
            </svg>
          </button>

          <!-- Prev -->
          <button
            @click="goToSpkPage(spkPageRef - 1)"
            :disabled="spkPageRef === 1"
            class="w-9 h-9 flex items-center justify-center rounded-lg font-bold transition"
            :class="spkPageRef === 1 ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-gray-900 text-white hover:bg-gray-700 cursor-pointer'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7" />
            </svg>
          </button>

          <input
            type="number"
            :value="spkPageRef"
            @change="onSpkPageInputChange"
            @keydown.enter="onSpkPageInputChange"
            min="1"
            :max="totalSpkPages"
            class="w-12 h-9 text-center border border-gray-300 rounded-lg text-sm font-medium text-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
          />

          <!-- Next -->
          <button
            @click="goToSpkPage(spkPageRef + 1)"
            :disabled="spkPageRef === totalSpkPages || totalSpkPages === 0"
            class="w-9 h-9 flex items-center justify-center rounded-lg font-bold transition"
            :class="spkPageRef === totalSpkPages || totalSpkPages === 0 ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-gray-900 text-white hover:bg-gray-700 cursor-pointer'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7" />
            </svg>
          </button>

          <!-- Max Next -->
          <button
            @click="goToSpkPage(totalSpkPages)"
            :disabled="spkPageRef === totalSpkPages || totalSpkPages === 0"
            class="w-9 h-9 flex items-center justify-center rounded-lg font-bold transition"
            :class="spkPageRef === totalSpkPages || totalSpkPages === 0 ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-gray-900 text-white hover:bg-gray-700 cursor-pointer'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 5l7 7-7 7M5 5l7 7-7 7" />
            </svg>
          </button>

        </div>
      </div>

      <!-- Info SPK yang dipilih -->
      <div class="mb-4">
        <div
          v-if="!spkDipilihObj"
          class="px-4 py-2.5 border border-gray-200 bg-gray-50 rounded-lg text-sm text-center text-gray-400"
        >
          Belum ada SPK yang dipilih
        </div>
        <div v-else class="grid grid-cols-3 gap-3">
          <div class="px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 select-none truncate">
            {{ spkDipilihObj.id }}
          </div>
          <div class="px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 select-none truncate">
            {{ spkDipilihObj.nama_spk }}
          </div>
          <div class="px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 select-none">
            {{ formatTanggal(spkDipilihObj.tgl_retail) }}
          </div>
        </div>
      </div>

      <!-- Dokumen yang sudah diunggah -->
      <div v-if="dokumen" class="mb-4">
        <div class="grid grid-cols-[10rem_1fr_auto] gap-x-3 items-center">
          <div class="px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 select-none">
            {{ formatTanggal(dokumen.tanggal) }}
          </div>
          <div class="flex items-center gap-2 px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <span class="truncate">{{ dokumen.namaFile }}</span>
          </div>
          <button
            @click="hapusDokumen"
            class="cursor-pointer p-2 text-gray-400 hover:text-red-500 transition flex-shrink-0"
            title="Hapus dokumen"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Tambah Dokumen -->
      <button
        v-if="!dokumen"
        @click="openUploadModal"
        class="w-full py-3 border border-gray-200 rounded-lg text-sm text-gray-400 bg-white cursor-pointer hover:bg-gray-50 hover:text-gray-600 transition mb-6"
      >
        + Tambah dokumen
      </button>
      <div v-else class="mb-6"></div>

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
const sudahCari      = ref(false)
const queryDicari    = ref('')

const showUploadModal = ref(false)
const isDragging      = ref(false)
const isUploading     = ref(false)
const uploadError     = ref('')
const fileInputRef    = ref(null)

const dokumen     = ref(null)
const isBatal     = ref(false)
const isSimpan    = ref(false)
const serverError = ref('')

const searchSPK   = ref('')
const spkDipilih  = ref('')
const spkList     = ref([])
const loadingSPK  = ref(false)
const errorSPK    = ref('')

const spkPerPage  = 6
const spkPageRef  = ref(1)

watch(searchSPK, () => {
  if (sudahCari.value) {
    sudahCari.value   = false
    queryDicari.value = ''
  }
})

const filteredSPK = computed(() => {
  const q = queryDicari.value.toLowerCase().trim()
  if (!q) return []
  return spkList.value.filter(s =>
    s.id.toLowerCase().includes(q) ||
    s.nama_spk.toLowerCase().includes(q) ||
    formatTanggal(s.tgl_retail).includes(q)
  )
})

const totalSpkPages = computed(() =>
  Math.ceil(filteredSPK.value.length / spkPerPage) || 1
)

const paginatedSPK = computed(() => {
  const start = (spkPageRef.value - 1) * spkPerPage
  return filteredSPK.value.slice(start, start + spkPerPage)
})

const spkDipilihObj = computed(() =>
  spkList.value.find(s => s.id === spkDipilih.value) || null
)

function handleCari() {
  sudahCari.value   = true
  queryDicari.value = searchSPK.value
  spkPageRef.value  = 1
}

function goToSpkPage(page) {
  spkPageRef.value = Math.max(1, Math.min(page, totalSpkPages.value))
}

function onSpkPageInputChange(e) {
  const val = parseInt(e.target.value)
  if (!isNaN(val)) goToSpkPage(val)
  e.target.value = spkPageRef.value
}

watch(filteredSPK, () => {
  spkPageRef.value = 1
})

async function fetchSPKList() {
  loadingSPK.value = true
  try {
    const token = localStorage.getItem('token')
    const res   = await axios.get('/api/beranda/spk-tersedia', {
      headers: { Authorization: `Bearer ${token}` }
    })
    spkList.value = res.data
  } catch (err) {
    console.warn('Gagal ambil daftar SPK:', err?.message)
  } finally {
    loadingSPK.value = false
  }
}

function pilihSPK(s) {
  spkDipilih.value  = s.id
  errorSPK.value    = ''
  sudahCari.value   = false
  queryDicari.value = ''
  searchSPK.value   = ''
  spkPageRef.value  = 1
}

function formatTanggal(iso) {
  if (!iso) return '-'
  const d = new Date(iso)
  return `${String(d.getDate()).padStart(2,'0')}/${String(d.getMonth()+1).padStart(2,'0')}/${d.getFullYear()}`
}

function openUploadModal()  { uploadError.value = ''; showUploadModal.value = true }
function closeUploadModal() { uploadError.value = ''; showUploadModal.value = false }
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
    const token    = localStorage.getItem('token')
    const formData = new FormData()
    formData.append('file', file)

    const res = await axios.post('/api/beranda/upload-dokumen', formData, {
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'multipart/form-data' }
    })

    dokumen.value = {
      namaFile:    file.name,
      pdfPath:     res.data.pdf_path,
      imageFolder: res.data.image_folder,
      tanggal:     new Date().toISOString(),
    }

    showUploadModal.value = false
  } catch (err) {
    uploadError.value = err.response?.data?.detail || 'Gagal mengunggah file. Coba lagi.'
  } finally {
    isUploading.value = false
  }
}

async function hapusDokumen() {
  if (!dokumen.value) return
  if (dokumen.value.pdfPath) {
    try {
      const token = localStorage.getItem('token')
      await axios.delete('/api/beranda/batal-upload-dokumen', {
        headers: { Authorization: `Bearer ${token}` },
        data: { pdf_path: dokumen.value.pdfPath }
      })
    } catch (err) {
      console.warn('Gagal hapus file:', err?.message)
    }
  }
  dokumen.value = null
}

async function handleKembali() {
  isBatal.value = true
  if (dokumen.value?.pdfPath) {
    try {
      const token = localStorage.getItem('token')
      await axios.delete('/api/beranda/batal-upload-dokumen', {
        headers: { Authorization: `Bearer ${token}` },
        data: { pdf_path: dokumen.value.pdfPath }
      })
    } catch {}
  }
  router.replace('/beranda')
}

async function handleSimpan() {
  errorSPK.value    = ''
  serverError.value = ''

  if (!spkDipilih.value) {
    errorSPK.value = 'Pilih SPK terlebih dahulu.'
    return
  }
  if (!dokumen.value) {
    serverError.value = 'Tambahkan dokumen terlebih dahulu.'
    return
  }

  const spkTerpilih = spkList.value.find(s => s.id === spkDipilih.value)
  if (!spkTerpilih?.id_template) {
    serverError.value = 'SPK ini tidak memiliki template.'
    return
  }

  isSimpan.value = true
  try {
    const token = localStorage.getItem('token')
    await axios.post('/api/beranda/simpan-dokumen', {
      id_spk:       spkDipilih.value,
      id_template:  spkTerpilih.id_template,
      dokumen_list: [{
        nama_dokumen: dokumen.value.namaFile,
        pdf_path:     dokumen.value.pdfPath,
      }]
    }, { headers: { Authorization: `Bearer ${token}` } })

    router.replace('/beranda')
  } catch (err) {
    serverError.value = err.response?.data?.detail || 'Gagal menyimpan dokumen. Coba lagi.'
  } finally {
    isSimpan.value = false
  }
}

onMounted(() => fetchSPKList())
</script>