<template>
  <AppLayout>

    <div class="mb-5">
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
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import AppLayout from '../components/AppLayout.vue'

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

const SS_KEY = 'template_tambah_data'

onMounted(() => {
  const raw = sessionStorage.getItem(SS_KEY)
  if (!raw) { router.replace('/template'); return }

  try {
    const data = JSON.parse(raw)
    namaFile.value  = data.namaFile  || ''
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
    isDeleting.value = false // 🔥 INI WAJIB
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

    // ── FIX: baca dengan key snake_case yang sama persis seperti
    //         yang disimpan di Template.vue saat upload berhasil ──
    const resTemplate = await axios.post('/api/template/simpan', {
      nama_template:     namaTemplate.value.trim(),
      pdf_path:          data.pdf_path        || '',  // ← key: pdf_path
      jml_halaman:       data.jml_halaman     || 0,   // ← key: jml_halaman
      resolusi_width:    data.resolusi_width  || 0,   // ← key: resolusi_width
      resolusi_height:   data.resolusi_height || 0,   // ← key: resolusi_height
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
</script>