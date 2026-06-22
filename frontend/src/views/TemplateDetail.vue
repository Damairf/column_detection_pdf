<template>
  <AppLayout>
    <div class="flex flex-col min-h-full">

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="flex items-center gap-3 text-gray-400 text-sm">
        <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
        </svg>
        Memuat data...
      </div>
    </div>

    <!-- Error -->
    <div v-else-if="errorMsg" class="flex items-center justify-center py-20">
      <p class="text-red-400 text-sm">{{ errorMsg }}</p>
    </div>

    <!-- Konten -->
    <div v-else>

      <!-- Kembali + Ubah + Hapus -->
      <div class="flex items-center justify-between mb-5">
        <!-- Kiri -->
        <button
          @click="router.replace('/template')"
          class="cursor-pointer px-4 py-2 bg-gray-900 text-white text-sm font-semibold rounded-lg hover:bg-gray-700 transition shadow-sm"
        >
          Kembali
        </button>

        <!-- Kanan -->
        <div class="flex items-center gap-2">
          <!-- Tombol Ubah -->
          <button
            v-if="user.role === 'admin'"
            @click="router.push(`/template/detail/${templateId}/ubah`)"
            class="cursor-pointer px-4 py-2 border border-gray-300 bg-white text-gray-700 text-sm font-semibold rounded-lg hover:bg-gray-50 transition shadow-sm"
          >
            Ubah
          </button>

          <!-- Tombol Download -->
          <button
            @click="showDownloadModal = true"
            class="cursor-pointer flex items-center gap-1.5 px-4 py-2 border border-gray-300 bg-white text-gray-700 text-sm font-semibold rounded-lg hover:bg-gray-50 transition shadow-sm"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            Download
          </button>

          <!-- Tombol Hapus -->
          <button
            v-if="user.role === 'admin'"
            @click="showDeleteModal = true"
            class="cursor-pointer px-4 py-2 bg-red-600 text-white text-sm font-semibold rounded-lg hover:bg-red-700 transition shadow-sm"
          >
            Hapus
          </button>
        </div>
      </div>

      <!-- Card utama -->
      <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">

        <!-- Baris atas: Info + Preview PDF -->
        <div class="flex gap-0 border-b border-gray-200">

          <!-- Panel Info -->
          <div class="w-96 flex-shrink-0 p-7 border-r border-gray-200">

            <!-- Nama Template -->
            <div class="mb-5">
              <label class="block text-sm font-semibold text-gray-700 mb-2">Nama Template</label>
              <div class="px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 select-none">
                {{ template.nama_template || '—' }}
              </div>
            </div>

            <!-- Pembuat -->
            <div class="mb-5">
              <label class="block text-sm font-semibold text-gray-700 mb-2">Pembuat</label>
              <div class="px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 select-none">
                {{ template.username || '—' }}
              </div>
            </div>

            <!-- Halaman -->
            <div class="mb-5">
              <label class="block text-sm font-semibold text-gray-700 mb-2">Halaman</label>
              <div class="px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 select-none">
                {{ template.jml_halaman ?? '—' }}
              </div>
            </div>

            <!-- Kolom -->
            <div class="mb-5">
              <label class="block text-sm font-semibold text-gray-700 mb-2">Kolom</label>
              <div class="px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 select-none">
                {{ template.kolom?.length ?? '—' }}
              </div>
            </div>

            <!-- Tanggal -->
            <div class="mb-5">
              <label class="block text-sm font-semibold text-gray-700 mb-2">Tanggal</label>
              <div class="px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 select-none">
                {{ formatTanggal(template.created_at) }}
              </div>
            </div>

            <!-- File Unggahan -->
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

          <!-- Panel Preview PDF -->
          <div class="flex-1 bg-gray-100 flex flex-col" style="min-height: 420px;">
            <iframe
              v-if="pdfUrl"
              :src="pdfUrl"
              class="w-full flex-1 border-0"
              style="min-height: 420px;"
            ></iframe>
            <div v-else class="flex-1 flex items-center justify-center">
              <div class="text-center">
                <div class="w-14 h-14 rounded-full bg-gray-200 flex items-center justify-center mx-auto mb-3">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                  </svg>
                </div>
                <p class="text-sm text-gray-400">Preview Dokumen</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Kolom Template -->
        <div class="p-7">
          <h3 class="text-sm font-semibold text-gray-700 mb-4">Kolom Template</h3>

          <div v-if="template.kolom && template.kolom.length > 0" class="space-y-2">
            <div
              v-for="kolom in template.kolom"
              :key="kolom.id"
              class="px-5 py-3.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 text-center font-medium"
            >
              {{ kolom.nama_kolom }}
            </div>
          </div>

          <div v-else class="px-5 py-8 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-400 text-center">
            Belum ada kolom template.
          </div>
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
          Apakah anda yakin ingin menghapusnya?
        </h2>
        <p class="text-sm text-gray-500 mb-6">
          Data yang sudah dihapus tidak dapat dipulihkan kembali
        </p>

        <!-- Button -->
        <div class="flex justify-center gap-3">
          <button
            @click="showDeleteModal = false"
            :disabled="deleting"
            class="px-5 py-2 bg-gray-800 text-white rounded-lg text-sm font-semibold hover:bg-gray-700 disabled:opacity-50">
            Batal
          </button>

          <button
            @click="handleDelete"
            :disabled="deleting"
            class="flex items-center justify-center gap-2 px-5 py-2 bg-red-600 text-white rounded-lg text-sm font-semibold hover:bg-red-700 disabled:opacity-50">

            <svg v-if="deleting" class="animate-spin h-4 w-4" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10" stroke="white" stroke-width="3" fill="none"/>
            </svg>

            <span>{{ deleting ? 'Menghapus...' : 'Hapus' }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Modal Download -->
    <div v-if="showDownloadModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40" @click.self="showDownloadModal = false">
      <div class="bg-white rounded-2xl w-full max-w-sm p-6 text-center shadow-lg">
        <h2 class="text-xl font-bold text-gray-800 mb-6">Download Template</h2>
        
        <div class="flex flex-col gap-3">
          <button
            @click="downloadPDF"
            class="w-full px-5 py-3 cursor-pointer border border-gray-300 bg-white text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition shadow-sm"
          >
            Dokumen Template
          </button>

          <button
            @click="downloadXLSX"
            class="w-full px-5 py-3 cursor-pointer border border-gray-300 bg-white text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition shadow-sm"
          >
            Kolom Template
          </button>

          <button
            @click="showDownloadModal = false"
            class="w-full px-5 py-3 cursor-pointer bg-gray-900 text-white font-medium rounded-lg hover:bg-gray-700 transition shadow-sm"
          >
            Batal
          </button>
        </div>
      </div>
    </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import AppLayout from '../components/AppLayout.vue'
import * as XLSX from 'xlsx'
import { useToast } from '../composables/useToast'

const router = useRouter()
const route  = useRoute()

const templateId = computed(() => route.params.id)
const { addToast } = useToast()

const template  = ref({})
const loading   = ref(false)
const errorMsg  = ref('')

const deleting = ref(false)
const showDeleteModal = ref(false)
const showDownloadModal = ref(false)

const BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

const user = computed(() => {
  try {
    return JSON.parse(localStorage.getItem('user') || '{}')
  } catch {
    return {}
  }
})

const isOwner = computed(() =>
  template.value.id_user != null &&
  user.value.id != null &&
  Number(template.value.id_user) === Number(user.value.id)
)

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

// Format tanggal
function formatTanggal(iso) {
  if (!iso) return '—'
  const d = new Date(iso)
  return `${String(d.getDate()).padStart(2,'0')}/${String(d.getMonth()+1).padStart(2,'0')}/${d.getFullYear()}`
}

async function handleDelete() {
  deleting.value = true
  try {
    const token = localStorage.getItem('token')

    await axios.delete(`/api/template/${templateId.value}`, {
      headers: { Authorization: `Bearer ${token}` }
    })

    showDeleteModal.value = false
    addToast('Template berhasil dihapus.', 'success')
    router.replace('/template')

  } catch (err) {
    console.error(err)
    alert('Gagal menghapus template')
  } finally {
    deleting.value = false
  }
}

function downloadXLSX() {
  if (!template.value || !template.value.kolom || template.value.kolom.length === 0) {
    alert('Tidak ada kolom template untuk diunduh.')
    return
  }

  const wsData = template.value.kolom.map(k => ({
    nama_kolom: k.nama_kolom,
    halaman:    k.halaman,
    x1:         k.x1,
    y1:         k.y1,
    x2:         k.x2,
    y2:         k.y2,
    type:       k.type
  }))

  const ws = XLSX.utils.json_to_sheet(wsData, { skipHeader: true })
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, 'Kolom')

  XLSX.writeFile(wb, `Kolom_${template.value.nama_template || 'Template'}.xlsx`)

  showDownloadModal.value = false
}

async function downloadPDF() {
  showDownloadModal.value = false
  if (!pdfUrl.value) return
  try {
    const res = await axios.get(pdfUrl.value, { responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([res.data], { type: 'application/pdf' }))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', namaFile.value || 'template.pdf')
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } catch (err) {
    console.error('Gagal mendownload:', err)
    const link = document.createElement('a')
    link.href = pdfUrl.value
    link.setAttribute('download', namaFile.value || 'template.pdf')
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }
}

// Fetch detail template dari API
async function fetchDetail() {
  loading.value  = true
  errorMsg.value = ''
  try {
    const token = localStorage.getItem('token')
    const res   = await axios.get(`/api/template/${templateId.value}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    template.value = res.data
  } catch (err) {
    errorMsg.value = err.response?.status === 404
      ? 'Template tidak ditemukan.'
      : 'Gagal memuat data. Coba muat ulang halaman.'
  } finally {
    loading.value = false
  }
}

onMounted(() => fetchDetail())
</script>