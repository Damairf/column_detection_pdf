<template>
  <AppLayout>
    <div class="flex flex-col min-h-full">

    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="flex items-center gap-3 text-gray-400 text-sm">
        <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
        </svg>
        Memuat data...
      </div>
    </div>

    <div v-else-if="errorMsg" class="flex items-center justify-center py-20">
      <p class="text-red-400 text-sm">{{ errorMsg }}</p>
    </div>

    <div v-else>

      <!-- Toolbar -->
      <div class="flex items-center gap-2 mb-5">
        <button @click="handleBatal"
          class="cursor-pointer px-4 py-2 bg-gray-900 text-white text-sm font-semibold rounded-lg hover:bg-gray-700 transition shadow-sm">
          Batal
        </button>
        <button @click="handleKonfirmasi" :disabled="isSimpan"
          class="cursor-pointer px-4 py-2 border border-gray-300 bg-white text-gray-700 text-sm font-semibold rounded-lg hover:bg-gray-50 transition shadow-sm"
          :class="isSimpan ? 'opacity-60 cursor-not-allowed' : ''">
          <span v-if="isSimpan" class="flex items-center gap-2">
            <svg class="animate-spin h-3.5 w-3.5 text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            Menyimpan...
          </span>
          <span v-else>Konfirmasi</span>
        </button>
      </div>

      <div v-if="serverError" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
        {{ serverError }}
      </div>

      <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">

        <!-- Info + Preview -->
        <div class="flex gap-0 border-b border-gray-200">
          <div class="w-96 flex-shrink-0 p-7 border-r border-gray-200">
            <div class="mb-5">
              <label class="block text-sm font-semibold text-gray-700 mb-2">Nama Template</label>
              <input v-model="namaTemplate" type="text" placeholder="Masukkan nama template..."
                class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent bg-white"
                :class="{ 'border-red-400 ring-1 ring-red-400': errorNama }" />
              <p v-if="errorNama" class="text-red-500 text-xs mt-1">{{ errorNama }}</p>
            </div>
            <div class="mb-5">
              <label class="block text-sm font-semibold text-gray-700 mb-2">Pembuat</label>
              <div class="px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 select-none">
                {{ template.username || '—' }}
              </div>
            </div>
            <div class="mb-5">
              <label class="block text-sm font-semibold text-gray-700 mb-2">Halaman</label>
              <div class="px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 select-none">{{ template.jml_halaman ?? '—' }}</div>
            </div>
            <div class="mb-5">
              <label class="block text-sm font-semibold text-gray-700 mb-2">Kolom</label>
              <div class="px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 select-none">{{ template.kolom?.length ?? '—' }}</div>
            </div>
            <div class="mb-5">
              <label class="block text-sm font-semibold text-gray-700 mb-2">Tanggal</label>
              <div class="px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 select-none">{{ formatTanggal(template.created_at) }}</div>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">File Unggahan</label>
              <div class="flex items-center gap-2 px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 select-none">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <span class="truncate">{{ namaFile }}</span>
              </div>
            </div>
          </div>

          <!-- Preview PDF -->
          <div class="flex-1 bg-gray-100 flex flex-col" style="min-height: 420px;">
            <iframe v-if="pdfUrl" :src="pdfUrl" class="w-full flex-1 border-0" style="min-height: 420px;"></iframe>
            <div v-else class="flex-1 flex items-center justify-center">
              <p class="text-sm text-gray-400">Preview Dokumen</p>
            </div>
          </div>
        </div>

        <!-- Kolom Template -->
        <div class="p-7">
          <h3 class="text-sm font-semibold text-gray-700 mb-4">Kolom Template</h3>

          <div v-if="template.kolom && template.kolom.length > 0" class="space-y-2 mb-3">
            <div v-for="kolom in template.kolom" :key="kolom.id"
              class="flex items-center justify-between px-4 py-3.5 bg-gray-50 border border-gray-200 rounded-lg">

              <!-- Hapus langsung -->
              <button @click="hapusKolom(kolom.id)"
                class="cursor-pointer p-1 text-gray-400 hover:text-red-500 transition flex-shrink-0" title="Hapus kolom">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>

              <span class="flex-1 text-center text-sm text-gray-700 font-medium">{{ kolom.nama_kolom }}</span>

              <!-- Edit kolom -->
              <button @click="handleEditKolom(kolom)"
                class="cursor-pointer p-1 text-gray-400 hover:text-gray-700 transition flex-shrink-0" title="Edit kolom">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </button>
            </div>
          </div>

          <div v-else class="mb-3 px-5 py-8 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-400 text-center">
            Belum ada kolom template.
          </div>

          <!-- Tombol Tambah Kolom Baru -->
          <button @click="handleTambahKolom"
            class="w-full py-3 border border-gray-200 rounded-lg text-sm text-gray-400 bg-white cursor-pointer hover:bg-gray-50 hover:text-gray-600 transition">
            + Tambah kolom template baru
          </button>
        </div>

      </div>
    </div>
    <div v-if="showDeleteModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
    <div class="bg-white rounded-2xl w-full max-w-md p-6 text-center shadow-lg">

      <!-- Icon -->
      <div class="flex justify-center mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6M9 7h6m-1-3H10a1 1 0 00-1 1v1h6V5a1 1 0 00-1-1z" />
        </svg>
      </div>

      <!-- Text -->
      <h2 class="text-lg font-semibold text-gray-800 mb-2">
        Apakah anda yakin ingin menghapus kolom ini?
      </h2>
      <p class="text-sm text-gray-500 mb-6">
        Data yang sudah dihapus tidak dapat dipulihkan kembali
      </p>

      <!-- Button -->
      <div class="flex justify-center gap-3">
        <button
          @click="showDeleteModal = false"
          class="px-5 py-2 bg-gray-800 text-white rounded-lg text-sm font-semibold hover:bg-gray-700">
          Batal
        </button>

        <button
          @click="confirmDeleteKolom"
          class="px-5 py-2 bg-red-600 text-white rounded-lg text-sm font-semibold hover:bg-red-700">
          Hapus
        </button>
      </div>
    </div>
  </div>
  </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import AppLayout from '../components/AppLayout.vue'
import { useToast } from '../composables/useToast'

const router = useRouter()
const route  = useRoute()

const templateId = computed(() => route.params.id)

const template     = ref({})
const namaTemplate = ref('')
const loading      = ref(false)
const errorMsg     = ref('')
const isSimpan     = ref(false)
const errorNama    = ref('')
const serverError  = ref('')
const isLoaded     = ref(false)

const deletedKolomIds = ref([])
const newKolomList = ref([])
const editedKolomList = ref([])
const snapshotKolom = ref([])
const showDeleteModal = ref(false)
const selectedKolomId = ref(null)

const { addToast } = useToast()

const BASE_URL = import.meta.env.VITE_API_BASE_URL || ''
const SS_KEY   = 'template_detail_ubah'

const pdfUrl = computed(() => {
  const path = template.value.path_template_pdf
  if (!path) return ''
  return `${BASE_URL}/${path.replace(/^\/+/, '').replace(/\\/g, '/')}`
})

const namaFile = computed(() => {
  const path = template.value.path_template_pdf
  if (!path) return '—'
  return path.replace(/\\/g, '/').split('/').pop()
})

function formatTanggal(iso) {
  if (!iso) return '—'
  const d = new Date(iso)
  return `${String(d.getDate()).padStart(2,'0')}/${String(d.getMonth()+1).padStart(2,'0')}/${d.getFullYear()}`
}

async function fetchDetail() {
  loading.value = true
  errorMsg.value = ''

  try {
    const token = localStorage.getItem('token')

    const res = await axios.get(`/api/template/${templateId.value}`, {
      headers: { Authorization: `Bearer ${token}` }
    })

    template.value     = res.data
    namaTemplate.value = res.data.nama_template || ''

    snapshotKolom.value = JSON.parse(
      JSON.stringify(res.data.kolom || [])
    )

  } catch (err) {
    errorMsg.value =
      err.response?.status === 404
        ? 'Template tidak ditemukan.'
        : 'Gagal memuat data.'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await fetchDetail()

  const raw = sessionStorage.getItem(SS_KEY)

  if (raw) {
    try {
      const data = JSON.parse(raw)

      if (data.namaTemplate) {
        namaTemplate.value = data.namaTemplate
      }

      if (data.deletedKolomIds) {
        deletedKolomIds.value = data.deletedKolomIds
      }

      if (data.editedKolomList) {
        editedKolomList.value = data.editedKolomList
      }

      snapshotKolom.value = snapshotKolom.value.filter(
        k => !deletedKolomIds.value.includes(k.id)
      ).map(k => {
        const edited = editedKolomList.value.find(e => e.id === k.id)
        return edited ? edited : k
      })

      template.value.kolom = template.value.kolom.filter(
        k => !deletedKolomIds.value.includes(k.id)
      ).map(k => {
        const edited = editedKolomList.value.find(e => e.id === k.id)
        return edited ? edited : k
      })

      if (data.kolomBaruList && data.kolomBaruList.length > 0) {
        data.kolomBaruList.forEach(k => {
          const exists = newKolomList.value.some(item => item.id === k.kolom_id)
          if (!exists) {
            newKolomList.value.push({
              id: k.kolom_id,
              nama_kolom: k.nama_kolom,
              halaman: k.halaman,
              x1: k.x1,
              y1: k.y1,
              x2: k.x2,
              y2: k.y2,
              type: k.warna,
            })
          }
        })
      }

      template.value.kolom = [
        ...snapshotKolom.value,
        ...newKolomList.value
      ]

    } catch {}
  }
  isLoaded.value = true
})

// Batal
function handleBatal() {
  template.value.kolom = JSON.parse(JSON.stringify(snapshotKolom.value))

  deletedKolomIds.value = []
  newKolomList.value = []
  editedKolomList.value = []

  sessionStorage.removeItem(SS_KEY)
  router.replace(`/template/detail/${templateId.value}`)
}

watch(namaTemplate, (val) => {
  if (!isLoaded.value) return
  let data = {}
  const raw = sessionStorage.getItem(SS_KEY)
  if (raw) {
    try {
      data = JSON.parse(raw)
    } catch {}
  }
  data.namaTemplate = val
  sessionStorage.setItem(SS_KEY, JSON.stringify(data))
})

// Konfirmasi
async function handleKonfirmasi() {
  errorNama.value  = ''
  serverError.value = ''

  if (!namaTemplate.value.trim()) {
    errorNama.value = 'Nama template wajib diisi.'
    return
  }

  isSimpan.value = true
  try {
    const token = localStorage.getItem('token')
    await axios.put(`/api/template/ubah/${templateId.value}`, {
      nama_template: namaTemplate.value.trim()
    }, { headers: { Authorization: `Bearer ${token}` } })

    if (deletedKolomIds.value.length > 0) {
      await axios.delete('/api/template/batal-kolom', {
        headers: { Authorization: `Bearer ${token}` },
        data: { kolom_ids: deletedKolomIds.value }
      })
    }

    if (editedKolomList.value.length > 0) {
      for (const k of editedKolomList.value) {
        if (k.id && k.id.toString().startsWith('temp-')) continue;

        await axios.put(`/api/template/update-kolom/${k.id}`, {
          nama_kolom: k.nama_kolom,
          halaman: k.halaman,
          x1: k.x1, y1: k.y1, x2: k.x2, y2: k.y2,
          resolusi_width: k.resolusi_width,
          resolusi_height: k.resolusi_height,
          warna: k.warna || k.type
        }, {
          headers: { Authorization: `Bearer ${token}` }
        })
      }
    }

    if (newKolomList.value.length > 0) {
      await axios.post('/api/template/tambah-kolom', {
        template_id: templateId.value,
        kolom: newKolomList.value
      }, {
        headers: { Authorization: `Bearer ${token}` }
      })
    }

    sessionStorage.removeItem(SS_KEY)
    addToast('Template berhasil diubah.', 'success')
    router.replace(`/template/detail/${templateId.value}`)
  } catch (err) {
    serverError.value = err.response?.data?.detail || 'Gagal menyimpan perubahan.'
  } finally {
    isSimpan.value = false
  }
}

// Hapus kolom langsung dari DB
function hapusKolom(kolomId) {
  selectedKolomId.value = kolomId
  showDeleteModal.value = true
}

async function confirmDeleteKolom() {
  try {
    const id = selectedKolomId.value

    if (id && !id.toString().startsWith('temp-')) {
      if (!deletedKolomIds.value.includes(id)) {
        deletedKolomIds.value.push(id)
      }
    }

    template.value.kolom = template.value.kolom.filter(k => k.id !== id)

    newKolomList.value = newKolomList.value.filter(k => k.id !== id)

    const raw = sessionStorage.getItem(SS_KEY)
    const data = raw ? JSON.parse(raw) : {}

    if (data.kolomBaruList) {
      data.kolomBaruList = data.kolomBaruList.filter(k => k.kolom_id !== id)
    }

    data.deletedKolomIds = deletedKolomIds.value

    sessionStorage.setItem(SS_KEY, JSON.stringify(data))

    showDeleteModal.value = false
    selectedKolomId.value = null

  } catch (err) {
    alert(err.response?.data?.detail || 'Gagal menghapus kolom.')
  }
}

// Edit kolom
function handleEditKolom(kolom) {
  const existing     = sessionStorage.getItem(SS_KEY)
  const existingData = existing ? JSON.parse(existing) : {}
  sessionStorage.setItem(SS_KEY, JSON.stringify({
    ...existingData,
    templateId:   templateId.value,
    templateData: template.value,
    editKolom:    kolom,
  }))
  router.push(`/kolom/edit?mode=detail&id=${templateId.value}`)
}

// Tambah kolom baru
function handleTambahKolom() {
  const existing     = sessionStorage.getItem(SS_KEY)
  const existingData = existing ? JSON.parse(existing) : {}
  sessionStorage.setItem(SS_KEY, JSON.stringify({
    ...existingData,
    templateId:   templateId.value,
    templateData: template.value
  }))
  router.push(`/kolom/baru?mode=detail&id=${templateId.value}`)
}
</script>