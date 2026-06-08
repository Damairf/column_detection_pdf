<template>
  <AppLayout>
    <div class="flex flex-col min-h-full">

    <!-- Overlay Upload CSV -->
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
          <p class="text-sm text-gray-500">tarik dan unggah file XLSX anda</p>
        </div>

        <input ref="fileInputRef" type="file" accept=".xlsx" class="hidden" @change="handleFileInput" />

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

    <div class="mb-5 flex items-center justify-between">
      <button
        @click="handleKembali"
        :disabled="isBatal"
        class="flex items-center gap-2 px-4 py-2 bg-gray-900 text-white text-sm font-semibold rounded-lg
               hover:bg-gray-700 transition shadow-sm"
        :class="isBatal ? 'opacity-60 cursor-not-allowed' : 'cursor-pointer'"
      >
        <svg v-if="isBatal" class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
        </svg>
        {{ isBatal ? 'Membatalkan...' : 'Kembali' }}
      </button>

      <button
        @click="showUploadModal = true"
        class="cursor-pointer flex items-center gap-1.5 px-4 py-2 border border-gray-300 bg-white text-gray-700 text-sm font-semibold rounded-lg hover:bg-gray-50 transition shadow-sm"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
        </svg>
        Upload Template
      </button>
    </div>

    <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-8">

      <!-- Nama Template -->
      <div class="mb-6">
        <label class="block text-sm font-semibold text-gray-700 mb-2">Nama Template</label>
        <input
          v-model="namaTemplate"
          type="text"
          placeholder="Masukkan nama template....."
          class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm text-gray-700 placeholder-gray-400
                 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent bg-white"
          :class="{ 'border-red-400 ring-1 ring-red-400': errorNama }"
        />
        <p v-if="errorNama" class="text-red-500 text-xs mt-1">{{ errorNama }}</p>
      </div>

      <!-- Tanggal & File Unggahan -->
      <div class="flex gap-6 mb-6">
        <div class="w-40">
          <label class="block text-sm font-semibold text-gray-700 mb-2">Tanggal</label>
          <div class="px-4 py-2.5 border border-gray-200 rounded-lg text-sm text-gray-700 bg-gray-50 select-none">
            {{ tanggalHariIni }}
          </div>
        </div>
        <div class="flex-1">
          <label class="block text-sm font-semibold text-gray-700 mb-2">File Unggahan</label>
          <div class="flex items-center gap-2 px-4 py-2.5 border border-gray-200 rounded-lg text-sm text-gray-700 bg-gray-50">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <span class="truncate">{{ namaFile }}</span>
          </div>
        </div>
      </div>

      <!-- Kolom Template -->
      <div class="mb-8">
        <label class="block text-sm font-semibold text-gray-700 mb-3">Kolom Template</label>

        <div v-if="kolomList.length > 0" class="space-y-2 mb-2">
          <div
            v-for="(kolom, index) in kolomList"
            :key="kolom.kolom_id ?? index"
            class="flex items-center justify-between px-4 py-3 bg-gray-100 rounded-lg border border-gray-200"
          >
            <button
              @click="hapusKolom(index, kolom.kolom_id)"
              :disabled="isDeleting"
              class="p-1 transition flex-shrink-0"
              :class="isDeleting
                ? 'text-gray-300 cursor-not-allowed'
                : 'text-gray-400 hover:text-red-500 cursor-pointer'"
              title="Hapus kolom"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-4 w-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
            <span class="w-3 h-3 rounded-full flex-shrink-0 ml-1" :style="{ backgroundColor: warnaHex(kolom.warna) }"></span>
            <span class="flex-1 text-center text-sm text-gray-700 font-medium">{{ kolom.nama_kolom }}</span>
            <button @click="handleEditKolom(index)"
              class="cursor-pointer p-1 text-gray-400 hover:text-gray-600 transition flex-shrink-0" title="Edit kolom">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </button>
          </div>
        </div>

        <button
          @click="handleTambahKolom"
          class="w-full py-3 border border-gray-200 rounded-lg text-sm text-gray-400
                 bg-white cursor-pointer hover:bg-gray-50 hover:text-gray-600 transition"
        >
          + Tambah kolom template baru
        </button>
      </div>

      <!-- Error server -->
      <div v-if="serverError" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm text-center">
        {{ serverError }}
      </div>

      <!-- Tombol Simpan -->
      <button
        @click="handleSimpan"
        :disabled="isSimpan"
        class="w-full py-3.5 font-bold text-sm rounded-lg transition shadow-sm"
        :class="isSimpan
          ? 'bg-gray-400 text-white cursor-not-allowed'
          : 'bg-gray-900 text-white hover:bg-gray-700 cursor-pointer'"
      >
        <span v-if="isSimpan" class="flex items-center justify-center gap-2">
          <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
          Menyimpan...
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
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import AppLayout from '../components/AppLayout.vue'
import * as XLSX from 'xlsx'

const router = useRouter()

const namaTemplate   = ref('')
const namaFile       = ref('')
const tanggalHariIni = ref('')
const kolomList      = ref([])
const isBatal        = ref(false)
const isSimpan       = ref(false)
const errorNama      = ref('')
const serverError    = ref('')
const isDeleting = ref(false)
const isLoaded      = ref(false)

const showUploadModal = ref(false)
const isDragging      = ref(false)
const isUploading     = ref(false)
const uploadError     = ref('')
const fileInputRef    = ref(null)

const SS_KEY = 'template_tambah_data'

onMounted(() => {
  const raw = sessionStorage.getItem(SS_KEY)
  if (!raw) { router.replace('/template'); return }

  try {
    const data = JSON.parse(raw)
    namaFile.value  = data.namaFile  || ''
    namaTemplate.value = data.namaTemplate || ''
    kolomList.value = data.kolomList || []

    if (data.kolomBaruList && data.kolomBaruList.length > 0) {
      data.kolomBaruList.forEach(k => {
        const kolomBaru = {
          ...k,
          kolom_id: k.kolom_id || `temp-${Date.now()}`
        }

        const exists = kolomList.value.some(item => item.kolom_id === kolomBaru.kolom_id)

        if (!exists) {
          kolomList.value.push(kolomBaru)
        }
      })

      sessionStorage.setItem(SS_KEY, JSON.stringify(data))
    }
  } catch {
    router.replace('/template')
    return
  }

  const now = new Date()
  tanggalHariIni.value = `${String(now.getDate()).padStart(2,'0')}/${String(now.getMonth()+1).padStart(2,'0')}/${now.getFullYear()}`
  
  isLoaded.value = true
})

async function hapusFileDiServer() {
  if (!namaFile.value) return
  try {
    const token = localStorage.getItem('token')
    await axios.delete('/api/template/batal-upload', {
      headers: { Authorization: `Bearer ${token}` },
      data: { nama_file: namaFile.value }
    })
  } catch (err) {
    console.warn('Gagal hapus file sementara:', err?.message)
  }
}

async function hapusKolomSementaraDiDB() {
  const kolomDenganId = kolomList.value.filter(k => k.kolom_id)
  if (kolomDenganId.length === 0) return
  try {
    const token = localStorage.getItem('token')
    await axios.delete('/api/template/batal-kolom', {
      headers: { Authorization: `Bearer ${token}` },
      data: { kolom_ids: kolomDenganId.map(k => k.kolom_id) }
    })
  } catch (err) {
    console.warn('Gagal hapus kolom sementara:', err?.message)
  }
}

async function handleKembali() {
  isBatal.value = true
  await hapusFileDiServer()
  await hapusKolomSementaraDiDB()
  sessionStorage.removeItem(SS_KEY)
  router.replace('/template')
}

watch(namaTemplate, (val) => {
  if (!isLoaded.value) return
  const raw = sessionStorage.getItem(SS_KEY)
  if (raw) {
    try {
      const data = JSON.parse(raw)
      data.namaTemplate = val
      sessionStorage.setItem(SS_KEY, JSON.stringify(data))
    } catch {}
  }
})

function handleTambahKolom() {
    const raw = sessionStorage.getItem(SS_KEY)
    if (raw) {
      try {
        const data = JSON.parse(raw)

        data.kolomList = kolomList.value

        data.kolomBaruList = data.kolomBaruList || []

        sessionStorage.setItem(SS_KEY, JSON.stringify(data))
      } catch {}
    }
    router.push({ path: '/kolom/baru', query: { mode: 'tambah' } })
  }

async function hapusKolom(index, kolomId) {
  if (isDeleting.value) return

  isDeleting.value = true

  try {
    const id = kolomId

    if (id && !id.toString().startsWith('temp-')) {
      const token = localStorage.getItem('token')
      await axios.delete('/api/template/batal-kolom', {
        headers: { Authorization: `Bearer ${token}` },
        data: { kolom_ids: [id] }
      })
    }

    kolomList.value.splice(index, 1)

    const raw = sessionStorage.getItem(SS_KEY)
    if (raw) {
      const data = JSON.parse(raw)

      data.kolomList = kolomList.value

      if (data.kolomBaruList) {
        data.kolomBaruList = data.kolomBaruList.filter(
          k => k.kolom_id !== id
        )
      }

      sessionStorage.setItem(SS_KEY, JSON.stringify(data))
    }

  } catch (err) {
    console.error(err)
  } finally {
    isDeleting.value = false
  }
}

async function handleSimpan() {
  errorNama.value   = ''
  serverError.value = ''

  if (!namaTemplate.value.trim()) {
    errorNama.value = 'Nama template wajib diisi.'
    return
  }

  isSimpan.value = true

  try {
    const token = localStorage.getItem('token')
    const raw   = sessionStorage.getItem(SS_KEY)
    const data  = raw ? JSON.parse(raw) : {}


    const resTemplate = await axios.post('/api/template/simpan', {
      nama_template:     namaTemplate.value.trim(),
      pdf_path:          data.pdf_path        || '',
      jml_halaman:       data.jml_halaman     || 0,
      resolusi_width:    data.resolusi_width  || 0,
      resolusi_height:   data.resolusi_height || 0,
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })

    const templateId = resTemplate.data.template_id

    const kolomDenganId = kolomList.value.filter(k => k.kolom_id)
    if (kolomDenganId.length > 0) {
      await axios.put('/api/template/update-kolom-template', {
        template_id: templateId,
        kolom_ids:   kolomDenganId.map(k => k.kolom_id)
      }, {
        headers: { Authorization: `Bearer ${token}` }
      })
    }

    sessionStorage.removeItem(SS_KEY)
    router.replace('/template')

  } catch (err) {
    serverError.value = err.response?.data?.detail || 'Gagal menyimpan template. Coba lagi.'
  } finally {
    isSimpan.value = false
  }
}

function handleEditKolom(index) {
  const raw = sessionStorage.getItem(SS_KEY)
  if (raw) {
    try {
      const data = JSON.parse(raw)
      data.kolomList    = kolomList.value
      data.editKolomIdx = index
      sessionStorage.setItem(SS_KEY, JSON.stringify(data))
    } catch {}
  }
  router.push({ path: '/kolom/edit', query: { mode: 'tambah' } })
}

function warnaHex(warna) {
  const map = { green: '#22c55e', red: '#ef4444', blue: '#3b82f6', yellow: '#eab308' }
  return map[warna] ?? '#6b7280'
}

// Upload PDF
function triggerFileInput() { fileInputRef.value?.click() }
function handleFileInput(e) {
  const file = e.target.files[0]
  if (file) prosesFileXLSX(file)
  e.target.value = ''
}

function handleDrop(e) {
  isDragging.value = false
  const file = e.dataTransfer.files[0]
  if (file) prosesFileXLSX(file)
}

async function prosesFileXLSX(file) {
  uploadError.value = ''

  if (!file.name.toLowerCase().endsWith('.xlsx')) {
    uploadError.value = 'File harus berformat XLSX.'
    return
  }

  isUploading.value = true

  const reader = new FileReader()
  reader.onload = async (e) => {
    try {
      const data     = new Uint8Array(e.target.result)
      const workbook = XLSX.read(data, { type: 'array' })
      const sheet    = workbook.Sheets[workbook.SheetNames[0]]
      const rows     = XLSX.utils.sheet_to_json(sheet, { header: 1 })
      const dataRows = rows.filter(row => row.length >= 7 && row[0])

      if (dataRows.length === 0) {
        uploadError.value = 'File kosong atau format tidak sesuai.'
        isUploading.value = false
        return
      }

      const newColumns = []
      const token      = localStorage.getItem('token')
      const rawData    = sessionStorage.getItem(SS_KEY)
      const dataJson   = rawData ? JSON.parse(rawData) : {}
      const resWidth   = dataJson.resolusi_width  || 0
      const resHeight  = dataJson.resolusi_height || 0

      for (const cols of dataRows) {
        const res = await axios.post('/api/template/simpan-kolom-sementara', {
          nama_kolom:      String(cols[0]).trim(),
          halaman:         parseInt(cols[1]) || 1,
          x1:              parseInt(cols[2]) || 0,
          y1:              parseInt(cols[3]) || 0,
          x2:              parseInt(cols[4]) || 0,
          y2:              parseInt(cols[5]) || 0,
          warna:           String(cols[6]).trim() || 'green',
          resolusi_width:  resWidth,
          resolusi_height: resHeight
        }, {
          headers: { Authorization: `Bearer ${token}` }
        })

        newColumns.push({
          kolom_id:   res.data.kolom_id,
          nama_kolom: String(cols[0]).trim(),
          halaman:    parseInt(cols[1]) || 1,
          x1:         parseInt(cols[2]) || 0,
          y1:         parseInt(cols[3]) || 0,
          x2:         parseInt(cols[4]) || 0,
          y2:         parseInt(cols[5]) || 0,
          warna:      String(cols[6]).trim() || 'green'
        })
      }

      kolomList.value      = [...kolomList.value, ...newColumns]
      dataJson.kolomList   = kolomList.value
      sessionStorage.setItem(SS_KEY, JSON.stringify(dataJson))
      showUploadModal.value = false

    } catch (err) {
      uploadError.value = 'Gagal memproses file XLSX.'
    } finally {
      isUploading.value = false
    }
  }

  reader.onerror = () => {
    uploadError.value = 'Gagal membaca file.'
    isUploading.value = false
  }

  reader.readAsArrayBuffer(file)
}
</script>