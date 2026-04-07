<template>
  <AppLayout>
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
      <div class="flex items-center justify-between mb-5">
        <button @click="router.replace('/template')"
          class="cursor-pointer px-4 py-2 bg-gray-900 text-white text-sm font-semibold rounded-lg hover:bg-gray-700 transition shadow-sm">
          Kembali
        </button>
        <button @click="router.push(`/template/detail/${templateId}/ubah`)"
          class="cursor-pointer px-4 py-2 border border-gray-300 bg-white text-gray-700 text-sm font-semibold rounded-lg hover:bg-gray-50 transition shadow-sm">
          Ubah
        </button>
      </div>

      <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        <div class="flex gap-0 border-b border-gray-200">
          <div class="w-96 flex-shrink-0 p-7 border-r border-gray-200">
            <div class="mb-5">
              <label class="block text-sm font-semibold text-gray-700 mb-2">Nama Template</label>
              <div class="px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 select-none">{{ template.nama_template || '—' }}</div>
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
          <div class="flex-1 bg-gray-100 flex flex-col" style="min-height: 420px;">
            <iframe v-if="pdfUrl" :src="pdfUrl" class="w-full flex-1 border-0" style="min-height: 420px;"></iframe>
            <div v-else class="flex-1 flex items-center justify-center">
              <p class="text-sm text-gray-400">Preview Dokumen</p>
            </div>
          </div>
        </div>
        <div class="p-7">
          <h3 class="text-sm font-semibold text-gray-700 mb-4">Kolom Template</h3>
          <div v-if="template.kolom && template.kolom.length > 0" class="space-y-2">
            <div v-for="kolom in template.kolom" :key="kolom.id"
              class="px-5 py-3.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 text-center font-medium">
              {{ kolom.nama_kolom }}
            </div>
          </div>
          <div v-else class="px-5 py-8 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-400 text-center">
            Belum ada kolom template.
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

const router = useRouter()
const route  = useRoute()
const templateId = computed(() => route.params.id)
const template  = ref({})
const loading   = ref(false)
const errorMsg  = ref('')
const BASE_URL  = import.meta.env.VITE_API_BASE_URL || ''

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
    const res   = await axios.get(`/api/template/${templateId.value}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    template.value = res.data
  } catch (err) {
    errorMsg.value = err.response?.status === 404 ? 'Template tidak ditemukan.' : 'Gagal memuat data.'
  } finally {
    loading.value = false
  }
}
onMounted(() => fetchDetail())
</script>