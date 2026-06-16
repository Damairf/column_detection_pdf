<template>
  <AppLayout>
    <div class="flex flex-col min-h-full">

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="flex items-center gap-3 text-gray-400 text-sm">
        <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
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

      <!-- Toolbar: Kembali + Download + Hapus -->
      <div class="flex items-center justify-between mb-5">
        <button
          @click="router.replace('/beranda')"
          class="cursor-pointer px-4 py-2 bg-gray-900 text-white text-sm font-semibold rounded-lg
                 hover:bg-gray-700 transition shadow-sm"
        >
          Kembali
        </button>

        <div class="flex items-center gap-2">
          <!-- Tombol Download -->
          <button
            @click="downloadPDF"
            class="cursor-pointer flex items-center gap-1.5 px-4 py-2 border border-gray-300 bg-white text-gray-700 text-sm font-semibold rounded-lg hover:bg-gray-50 transition shadow-sm"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            Download
          </button>

          <!-- Tombol Hapus — hanya admin -->
          <button
            v-if="user.role === 'admin'"
            @click="showDeleteModal = true"
            class="cursor-pointer px-4 py-2 bg-red-600 text-white text-sm font-semibold rounded-lg
                   hover:bg-red-700 transition shadow-sm"
          >
            Hapus
          </button>
        </div>
      </div>

      <!-- Card Utama -->
      <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">

        <!-- Baris Atas: Info + Preview PDF -->
        <div class="flex gap-0 border-b border-gray-200">

          <!-- Panel Info -->
          <div class="w-96 flex-shrink-0 p-7 border-r border-gray-200">

            <!-- Nama Dokumen -->
            <div class="mb-5">
              <label class="block text-sm font-semibold text-gray-700 mb-2">Nama Dokumen</label>
              <div class="px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 select-none">
                {{ detail.nama_dokumen || '—' }}
              </div>
            </div>

            <!-- Pengunggah -->
            <div class="mb-5">
              <label class="block text-sm font-semibold text-gray-700 mb-2">Pengunggah</label>
              <div class="px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 select-none">
                {{ detail.pengunggah || '—' }}
              </div>
            </div>

            <!-- Nomor SPK -->
            <div class="mb-5">
              <label class="block text-sm font-semibold text-gray-700 mb-2">Nomor SPK</label>
              <div class="px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 select-none">
                {{ detail.id_spk || '—' }}
              </div>
            </div>

            <!-- Nama SPK -->
            <div class="mb-5">
              <label class="block text-sm font-semibold text-gray-700 mb-2">Nama SPK</label>
              <div class="px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 select-none">
                {{ detail.nama_spk || '—' }}
              </div>
            </div>

            <!-- Nama Template -->
            <div class="mb-5">
              <label class="block text-sm font-semibold text-gray-700 mb-2">Nama Template</label>
              <div class="px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 select-none">
                {{ detail.nama_template || '—' }}
              </div>
            </div>

            <!-- Tanggal -->
            <div class="mb-5">
              <label class="block text-sm font-semibold text-gray-700 mb-2">Tanggal</label>
              <div class="px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 select-none">
                {{ formatTanggal(detail.created_at) }}
              </div>
            </div>

            <!-- Status -->
            <div v-if="user.role === 'admin'" class="mb-5">
              <label class="block text-sm font-semibold text-gray-700 mb-2">Status</label>
              <span
                class="inline-flex items-center gap-1.5 px-4 py-2 rounded-full text-sm font-semibold"
                :class="badgeClass(detail.status)"
              >
                <svg v-if="detail.status === 'Memuat'" class="animate-spin h-3.5 w-3.5"
                  xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-30" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
                </svg>
                {{ labelStatus(detail.status) }}
              </span>
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

        <!-- Tabel Hasil Deteksi Kolom -->
        <div v-if="user.role === 'admin'" class="p-7">

          <div v-if="detail.status === 'Memuat'" class="flex items-center gap-2 text-gray-400 text-sm mb-4">
            <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
            </svg>
            Proses deteksi sedang berjalan...
          </div>

          <div v-if="detail.status === 'Error'" class="flex items-center gap-3 px-4 py-3 mb-4 bg-orange-50 border border-orange-200 rounded-lg text-orange-700 text-sm">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 flex-shrink-0 text-orange-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
            </svg>
            Error. Periksa apakah terdapat kesalahan dalam dokumen atau template.
          </div>

          <div class="overflow-hidden rounded-xl border border-gray-200">
            <table class="w-full text-sm">
              <thead>
                <tr class="bg-gray-50 border-b border-gray-200">
                  <th class="px-5 py-3.5 text-center font-semibold text-gray-700 w-16">No</th>
                  <th class="px-5 py-3.5 text-left font-semibold text-gray-700">Nama Kolom</th>
                  <th class="px-5 py-3.5 text-center font-semibold text-gray-700 w-56">Koordinat</th>
                  <th class="px-5 py-3.5 text-center font-semibold text-gray-700 w-32">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(kolom, idx) in hasilDeteksi"
                  :key="kolom.id_kolom"
                  class="border-b border-gray-100 last:border-0 hover:bg-gray-50 transition-colors"
                >
                  <td class="px-5 py-3.5 text-center text-gray-500">{{ idx + 1 }}</td>
                  <td class="px-5 py-3.5 text-left text-gray-700 font-medium">{{ kolom.nama_kolom }}</td>
                  <td class="px-5 py-3.5 text-center text-gray-500 font-mono text-xs">
                    ({{ kolom.x1 }}, {{ kolom.y1 }}, {{ kolom.x2 }}, {{ kolom.y2 }})
                  </td>
                  <td class="px-5 py-3.5 text-center">
                    <span
                      class="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-semibold"
                      :class="badgeKolom(kolom.status)"
                    >
                      <svg v-if="kolom.status === 'Memuat'" class="animate-spin h-3 w-3"
                        xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-30" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
                      </svg>
                      {{ kolom.status || 'Memuat' }}
                    </span>
                  </td>
                </tr>
                <tr v-if="hasilDeteksi.length === 0">
                  <td colspan="4" class="px-5 py-8 text-center text-gray-400 text-sm">
                    {{ detail.status === 'Memuat' ? 'Menunggu hasil deteksi...' : 'Belum ada data deteksi.' }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Konfirmasi Hapus -->
    <div v-if="showDeleteModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div class="bg-white rounded-2xl w-full max-w-md p-6 text-center shadow-lg">
        <div class="flex justify-center mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6M9 7h6m-1-3H10a1 1 0 00-1 1v1h6V5a1 1 0 00-1-1z" />
          </svg>
        </div>
        <h2 class="text-lg font-semibold text-gray-800 mb-2">
          Apakah anda yakin ingin menghapusnya?
        </h2>
        <p class="text-sm text-gray-500 mb-6">
          Data yang sudah dihapus tidak dapat dipulihkan kembali
        </p>
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

    <!-- Footer Warning -->
    <!-- <div class="mt-auto pt-6 text-xs text-gray-400 text-center border-t border-gray-100">
      Sistem ini bisa melakukan kesalahan. Silahkan periksa kembali hasilnya
    </div> -->
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import AppLayout from '../components/AppLayout.vue'

const router = useRouter()
const route  = useRoute()

const user = computed(() => {
  try { return JSON.parse(localStorage.getItem('user')) || {} }
  catch { return {} }
})

const dokumenId = computed(() => route.params.id)
const BASE_URL  = import.meta.env.VITE_API_BASE_URL || ''

const detail       = ref({})
const hasilDeteksi = ref([])
const loading      = ref(false)
const errorMsg     = ref('')
const showDeleteModal = ref(false)
const deleting        = ref(false)

const pdfUrl = computed(() => {
  const path = detail.value.path_pdf
  if (!path) return ''
  return `${BASE_URL}/${path.replace(/^\/+/, '').replace(/\\/g, '/')}`
})

const namaFile = computed(() => {
  const path = detail.value.path_pdf
  if (!path) return '—'
  return path.replace(/\\/g, '/').split('/').pop()
})

function formatTanggal(iso) {
  if (!iso) return '—'
  const d = new Date(iso)
  return `${String(d.getDate()).padStart(2,'0')}/${String(d.getMonth()+1).padStart(2,'0')}/${d.getFullYear()}`
}

function badgeClass(status) {
  switch (status) {
    case 'Benar':  return 'bg-green-100 text-green-700'
    case 'Salah':  return 'bg-red-100 text-red-600'
    case 'Memuat': return 'bg-gray-100 text-gray-500'
    case 'Error':  return 'bg-orange-100 text-orange-600'
    default:       return 'bg-gray-100 text-gray-500'
  }
}
function labelStatus(status) {
  const map = { Benar: 'Benar', Salah: 'Salah', Memuat: 'Memuat', Error: 'Error' }
  return map[status] ?? status ?? '—'
}

function badgeKolom(status) {
  switch (status) {
    case 'TERISI':  return 'bg-blue-100 text-blue-600'
    case 'KOSONG':  return 'bg-gray-200 text-gray-600'
    case 'Memuat':  return 'bg-gray-100 text-gray-400'
    default:        return 'bg-gray-100 text-gray-400'
  }
}

async function fetchDetail(silent = false) {
  if (!silent) loading.value = true
  errorMsg.value = ''
  try {
    const token = localStorage.getItem('token')
    const res   = await axios.get(`/api/beranda/dokumen/${dokumenId.value}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    detail.value       = res.data.dokumen
    hasilDeteksi.value = res.data.hasil_deteksi || []
  } catch (err) {
    if (!silent) {
      errorMsg.value = err.response?.status === 404
        ? 'Dokumen tidak ditemukan.'
        : 'Gagal memuat data.'
    }
  } finally {
    if (!silent) loading.value = false
  }
}

let pollingTimer = null

function startPollingIfNeeded() {
  if (detail.value.status === 'Memuat' && !pollingTimer) {
    pollingTimer = setInterval(async () => {
      await fetchDetail(true)
      if (detail.value.status !== 'Memuat') {
        clearInterval(pollingTimer)
        pollingTimer = null
      }
    }, 5000)
  }
}

async function downloadPDF() {
  if (!pdfUrl.value) { alert('File PDF tidak tersedia.'); return }
  try {
    const res = await axios.get(pdfUrl.value, { responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([res.data], { type: 'application/pdf' }))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', namaFile.value || 'dokumen.pdf')
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } catch {
    const link = document.createElement('a')
    link.href = pdfUrl.value
    link.setAttribute('download', namaFile.value || 'dokumen.pdf')
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }
}

async function handleDelete() {
  deleting.value = true
  try {
    const token = localStorage.getItem('token')
    await axios.delete(`/api/beranda/dokumen/${dokumenId.value}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    showDeleteModal.value = false
    router.replace('/beranda')
  } catch (err) {
    alert(err.response?.data?.detail || 'Gagal menghapus dokumen.')
  } finally {
    deleting.value = false
  }
}

onMounted(async () => {
  await fetchDetail()
  startPollingIfNeeded()
})

onBeforeUnmount(() => {
  if (pollingTimer) { clearInterval(pollingTimer); pollingTimer = null }
})
</script>