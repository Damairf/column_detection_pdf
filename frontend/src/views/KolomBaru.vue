<template>
  <AppLayout>
    <div class="flex flex-col min-h-full">
    <div class="flex gap-5" style="height: calc(100vh - 8rem);">

      <!-- Panel Kiri -->
      <div class="w-72 flex-shrink-0 flex flex-col gap-4">
        <button @click="handleKembali"
          class="cursor-pointer flex items-center gap-2 px-4 py-2 bg-gray-900 text-white text-sm font-semibold rounded-lg hover:bg-gray-700 transition shadow-sm w-fit">
          Kembali
        </button>

        <div class="bg-white rounded-xl border border-gray-200 shadow-sm p-5 flex flex-col gap-4 overflow-y-auto flex-1">
          <div>
            <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5">Nama Kolom</label>
            <input v-model="namaKolom" type="text" placeholder="Contoh: Kolom Pemesanan"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-400 bg-white" />
          </div>

          <div>
            <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5">Halaman</label>
            <div class="flex items-center gap-2">
              <button @click="halamanDipilih > 1 && halamanDipilih--" :disabled="halamanDipilih <= 1"
                class="w-8 h-8 flex items-center justify-center rounded-lg border border-gray-300 text-gray-600 hover:bg-gray-100 transition disabled:opacity-40 disabled:cursor-not-allowed">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7"/></svg>
              </button>
              <select v-model="halamanDipilih" class="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm text-gray-700 bg-white focus:outline-none focus:ring-2 focus:ring-gray-400">
                <option v-for="n in totalHalaman" :key="n" :value="n">Halaman {{ n }}</option>
              </select>
              <button @click="halamanDipilih < totalHalaman && halamanDipilih++" :disabled="halamanDipilih >= totalHalaman"
                class="w-8 h-8 flex items-center justify-center rounded-lg border border-gray-300 text-gray-600 hover:bg-gray-100 transition disabled:opacity-40 disabled:cursor-not-allowed">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7"/></svg>
              </button>
            </div>
            <p class="text-xs text-gray-400 mt-1">Total {{ totalHalaman }} halaman</p>
          </div>

          <div>
            <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5">Koordinat Seleksi</label>
            <div class="grid grid-cols-2 gap-2">
              <div v-for="k in ['x1','y1','x2','y2']" :key="k">
                <label class="text-xs text-gray-400 mb-1 block">{{ k.toUpperCase() }}</label>
                <div class="px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-600 font-mono select-none">{{ koordinat[k] !== null ? koordinat[k] : '—' }}</div>
              </div>
            </div>
            <p class="text-xs text-gray-400 mt-1.5">Buat seleksi pada gambar untuk mengisi koordinat.</p>
          </div>

          <div>
            <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5">Resolusi Image</label>
            <div class="grid grid-cols-2 gap-2">
              <div><label class="text-xs text-gray-400 mb-1 block">Lebar (px)</label>
                <div class="px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-600 font-mono select-none">{{ resolusi.width ?? '—' }}</div></div>
              <div><label class="text-xs text-gray-400 mb-1 block">Tinggi (px)</label>
                <div class="px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-600 font-mono select-none">{{ resolusi.height ?? '—' }}</div></div>
            </div>
          </div>

          <div class="flex-1"></div>

          <button @click="simpanKolom" :disabled="!bisaSimpan || isSimpan"
            class="w-full py-3 text-sm font-bold rounded-lg transition shadow-sm"
            :class="bisaSimpan && !isSimpan ? 'bg-gray-900 text-white hover:bg-gray-700 cursor-pointer' : 'bg-gray-200 text-gray-400 cursor-not-allowed'">
            <span v-if="isSimpan" class="flex items-center justify-center gap-2">
              <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
              Menyimpan...
            </span>
            <span v-else>Simpan Kolom</span>
          </button>
        </div>
      </div>

      <!-- Panel Kanan: Canvas -->
      <div class="flex-1 flex flex-col bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        <div class="flex items-center gap-1 px-4 py-2.5 border-b border-gray-200 bg-gray-50 flex-shrink-0">
          <button @click="activeTool = 'box'" title="  v  " class="w-8 h-8 flex items-center justify-center rounded-md transition" :class="activeTool === 'box' ? 'bg-gray-900 text-white' : 'text-gray-500 hover:bg-gray-200'">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3h14a2 2 0 012 2v14a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2z"/></svg>
          </button>
          <button @click="activeTool = 'hand'" title="  h  " class="w-8 h-8 flex items-center justify-center rounded-md transition" :class="activeTool === 'hand' ? 'bg-gray-900 text-white' : 'text-gray-500 hover:bg-gray-200'">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 11.5V14m0-2.5v-6a1.5 1.5 0 013 0m-3 6a1.5 1.5 0 00-3 0v2a7.5 7.5 0 0015 0v-5a1.5 1.5 0 00-3 0m-6-3V11m0-5.5v-1a1.5 1.5 0 013 0v1m0 0V11m0-5.5a1.5 1.5 0 013 0v3m0 0V11"/></svg>
          </button>
          <button @click="zoomIn" title="  +  " class="w-8 h-8 flex items-center justify-center rounded-md text-gray-500 hover:bg-gray-200 transition">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M17 11A6 6 0 115 11a6 6 0 0112 0zM11 8v6M8 11h6"/></svg>
          </button>
          <button @click="zoomOut" title="  -  " class="w-8 h-8 flex items-center justify-center rounded-md text-gray-500 hover:bg-gray-200 transition">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M17 11A6 6 0 115 11a6 6 0 0112 0zM8 11h6"/></svg>
          </button>
          <div class="w-px h-5 bg-gray-300 mx-1"></div>
          <div class="flex items-center gap-1">
            <button v-for="w in warnaOptions" :key="w.value" @click="warnaAktif = w.value" :title="w.label"
              class="w-6 h-6 rounded-full border-2 transition" :style="{ backgroundColor: w.bg }"
              :class="warnaAktif === w.value ? 'border-gray-900 scale-110' : 'border-transparent hover:border-gray-400'">
            </button>
          </div>
          <div class="flex-1"></div>
          <span class="text-xs text-gray-400 font-mono">{{ Math.round(zoomLevel * 100) }}%</span>
          <button @click="resetZoom" class="text-xs text-gray-500 hover:text-gray-800 px-2 py-1 rounded hover:bg-gray-200 transition ml-1">Reset</button>
        </div>

        <div ref="canvasWrapperRef" tabindex="0" @mouseenter="isCanvasFocused = true" @mouseleave="isCanvasFocused = false"  @focus="isCanvasFocused = true" @blur="isCanvasFocused = false" class="flex-1 overflow-hidden relative bg-gray-100"
          :style="activeTool === 'hand' && isPanning ? 'cursor: grabbing' : activeTool === 'hand' ? 'cursor: grab' : 'cursor: crosshair'"
          @mousedown="onMouseDown" @mousemove="onMouseMove" @mouseup="onMouseUp" @wheel.prevent="onWheel">
          <div class="absolute origin-top-left select-none"
            :style="{ transform: `translate(${panOffset.x}px, ${panOffset.y}px) scale(${zoomLevel})`, transformOrigin: '0 0' }">
            <div v-if="!imageSrc" class="flex items-center justify-center bg-gray-50" style="width:600px;height:800px;">
              <div class="text-center">
                <div class="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center mx-auto mb-3">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                  </svg>
                </div>
                <p class="text-sm text-gray-400">Memuat gambar...</p>
              </div>
            </div>
            <img v-if="imageSrc" ref="imgRef" :src="imageSrc" class="block max-w-none" draggable="false" @load="onImageLoad" @error="onImageError" />
            <div v-if="seleksi && imageSrc" class="absolute pointer-events-none"
              :style="{ left: seleksi.x+'px', top: seleksi.y+'px', width: seleksi.w+'px', height: seleksi.h+'px', border: `2px solid ${warnaHex}`, backgroundColor: warnaHexAlpha }">
              <div class="absolute -top-5 left-0 px-1.5 py-0.5 text-white text-xs font-semibold rounded" :style="{ backgroundColor: warnaHex }">{{ namaKolom || 'Kolom Baru' }}</div>
            </div>
            <div v-if="drawing && dragBox && imageSrc" class="absolute pointer-events-none"
              :style="{ left: dragBox.x+'px', top: dragBox.y+'px', width: dragBox.w+'px', height: dragBox.h+'px', border: `2px dashed ${warnaHex}`, backgroundColor: warnaHexAlpha }">
            </div>
          </div>
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
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import AppLayout from '../components/AppLayout.vue'

const router   = useRouter()
const route    = useRoute()
const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const mode     = computed(() => route.query.mode || 'tambah')
const detailId = computed(() => route.query.id   || '')

const SS_TAMBAH = 'template_tambah_data'
const SS_DETAIL = 'template_detail_ubah'
const ssKey     = computed(() => mode.value === 'detail' ? SS_DETAIL : SS_TAMBAH)

const routeKembali = computed(() =>
  mode.value === 'detail' ? `/template/detail/${detailId.value}/ubah` : '/template/tambah'
)
const isCanvasFocused = ref(false)

const namaKolom      = ref('')
const halamanDipilih = ref(1)
const totalHalaman   = ref(1)
const imagePaths     = ref([])
const pdfPathServer  = ref('')
const koordinat      = ref({ x1: null, y1: null, x2: null, y2: null })
const resolusi       = ref({ width: null, height: null })
const isSimpan       = ref(false)

const canvasWrapperRef = ref(null)
const imgRef           = ref(null)
const imageSrc         = ref('')
const activeTool       = ref('box')
const zoomLevel        = ref(1)
const panOffset        = ref({ x: 0, y: 0 })
const isPanning        = ref(false)
const panStart         = ref({ x: 0, y: 0 })
const panOrigin        = ref({ x: 0, y: 0 })
const drawing          = ref(false)
const drawStart        = ref({ x: 0, y: 0 })
const dragBox          = ref(null)
const seleksi          = ref(null)

const warnaAktif  = ref('green')
const warnaOptions = [
  { value: 'green', label: 'Hijau', bg: '#22c55e' }, { value: 'red', label: 'Merah', bg: '#ef4444' },
  { value: 'blue', label: 'Biru', bg: '#3b82f6' },   { value: 'yellow', label: 'Kuning', bg: '#eab308' },
]
const warnaHex      = computed(() => warnaOptions.find(w => w.value === warnaAktif.value)?.bg ?? '#22c55e')
const warnaHexAlpha = computed(() => warnaHex.value + '33')
const bisaSimpan    = computed(() =>
  namaKolom.value.trim() !== '' && koordinat.value.x1 !== null &&
  koordinat.value.y1 !== null && koordinat.value.x2 !== null && koordinat.value.y2 !== null
)

function handleKeydown(e) {
  if (!isCanvasFocused.value) return
  const key = e.key.toLowerCase()
  if (key === 'v') {
    activeTool.value = 'box'
  } 
  else if (key === 'h') {
    activeTool.value = 'hand'
  } 
  else if (key === '+' || key === '=') {
    zoomIn()
  } 
  else if (key === '-' || key === '_') {
    zoomOut()
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
  const raw = sessionStorage.getItem(ssKey.value)
  if (!raw) { router.replace(routeKembali.value); return }
  try {
    const data = JSON.parse(raw)
    if (mode.value === 'tambah') {
      imagePaths.value      = data.imagePaths     || []
      totalHalaman.value    = data.jmlHalaman     || imagePaths.value.length || 1
      resolusi.value.width  = data.resolusiWidth  ?? null
      resolusi.value.height = data.resolusiHeight ?? null
    } else {
      const td = data.templateData
      if (!td) { router.replace(routeKembali.value); return }
      pdfPathServer.value   = td.path_template_pdf || ''
      totalHalaman.value    = td.jml_halaman       || 1
      resolusi.value.width  = td.resolusi_width    ?? null
      resolusi.value.height = td.resolusi_height   ?? null
    }
    muatGambar(1)
  } catch { router.replace(routeKembali.value) }
})

function cleanFileName(name) {
  return name
    .replace(/\s+/g, '_')
    .replace(/[^\w\-]/g, '')
}

function muatGambar(halaman) {
  if (mode.value === 'tambah') {
    if (imagePaths.value.length > 0) {
      const path = imagePaths.value[halaman - 1]
      imageSrc.value = `${BASE_URL}/${path.replace(/^\/+/, '').replace(/\\/g, '/')}`
    }
  } else {
    if (pdfPathServer.value) {
      const cleanPath = pdfPathServer.value.replace(/\\/g, '/')
      const fileName  = cleanPath.split('/').pop()
      const baseName = cleanFileName(fileName.replace(/\.[^/.]+$/, ''))
      imageSrc.value  = `${BASE_URL}/storage/template/images/${baseName}/${baseName}_page_${halaman}.jpeg`
    }
  }
  console.log('IMAGE SRC FINAL:', imageSrc.value)
  seleksi.value   = null
  koordinat.value = { x1: null, y1: null, x2: null, y2: null }
  resetZoom()
}

watch(halamanDipilih, (val) => muatGambar(val))

function onImageLoad() {
  if (imgRef.value) {
    resolusi.value.width  = imgRef.value.naturalWidth
    resolusi.value.height = imgRef.value.naturalHeight
  }
}
function onImageError() { console.warn('Gagal memuat gambar:', imageSrc.value) }
function zoomIn()    { zoomLevel.value = Math.min(zoomLevel.value + 0.2, 5) }
function zoomOut()   { zoomLevel.value = Math.max(zoomLevel.value - 0.2, 0.2) }
function resetZoom() { zoomLevel.value = 1; panOffset.value = { x: 0, y: 0 } }
function onWheel(e)  { zoomLevel.value = Math.min(Math.max(zoomLevel.value + (e.deltaY > 0 ? -0.1 : 0.1), 0.2), 5) }
function getImageCoords(e) {
  const rect = canvasWrapperRef.value.getBoundingClientRect()
  return { x: (e.clientX - rect.left - panOffset.value.x) / zoomLevel.value, y: (e.clientY - rect.top - panOffset.value.y) / zoomLevel.value }
}
function onMouseDown(e) {
  if (e.button !== 0) return
  if (activeTool.value === 'hand') { isPanning.value = true; panStart.value = { x: e.clientX, y: e.clientY }; panOrigin.value = { ...panOffset.value }; return }
  if (activeTool.value === 'box' && imageSrc.value) { drawing.value = true; const { x, y } = getImageCoords(e); drawStart.value = { x, y }; dragBox.value = { x, y, w: 0, h: 0 } }
}
function onMouseMove(e) {
  if (activeTool.value === 'hand' && isPanning.value) { panOffset.value = { x: panOrigin.value.x + (e.clientX - panStart.value.x), y: panOrigin.value.y + (e.clientY - panStart.value.y) }; return }
  if (activeTool.value === 'box' && drawing.value) { const { x, y } = getImageCoords(e); dragBox.value = { x: Math.min(x, drawStart.value.x), y: Math.min(y, drawStart.value.y), w: Math.abs(x - drawStart.value.x), h: Math.abs(y - drawStart.value.y) } }
}
function onMouseUp(e) {
  if (activeTool.value === 'hand') { isPanning.value = false; return }
  if (activeTool.value === 'box' && drawing.value) {
    drawing.value = false
    const { x, y } = getImageCoords(e)
    const x1 = Math.round(Math.min(x, drawStart.value.x)), y1 = Math.round(Math.min(y, drawStart.value.y))
    const x2 = Math.round(Math.max(x, drawStart.value.x)), y2 = Math.round(Math.max(y, drawStart.value.y))
    if (x2 - x1 < 5 || y2 - y1 < 5) { dragBox.value = null; return }
    koordinat.value = { x1, y1, x2, y2 }; seleksi.value = { x: x1, y: y1, w: x2 - x1, h: y2 - y1 }; dragBox.value = null
  }
}

function handleKembali() { router.replace(routeKembali.value) }

async function simpanKolom() {
  if (!bisaSimpan.value) return
  isSimpan.value = true
  try {
    const token = localStorage.getItem('token')
    let kolomBaru

    if (mode.value === 'tambah') {
      const res = await axios.post('/api/template/simpan-kolom-sementara', {
        nama_kolom: namaKolom.value.trim(), halaman: halamanDipilih.value,
        x1: koordinat.value.x1, y1: koordinat.value.y1, x2: koordinat.value.x2, y2: koordinat.value.y2,
        resolusi_width: resolusi.value.width, resolusi_height: resolusi.value.height, warna: warnaAktif.value,
      }, { headers: { Authorization: `Bearer ${token}` } })
      kolomBaru = { kolom_id: res.data.kolom_id, nama_kolom: namaKolom.value.trim(), halaman: halamanDipilih.value,
        x1: koordinat.value.x1, y1: koordinat.value.y1, x2: koordinat.value.x2, y2: koordinat.value.y2,
        resolusi_width: resolusi.value.width, resolusi_height: resolusi.value.height, warna: warnaAktif.value }
    } else {
        kolomBaru = {
          kolom_id: `temp-${Date.now()}`,
          nama_kolom: namaKolom.value.trim(),
          halaman: halamanDipilih.value,
          x1: koordinat.value.x1,
          y1: koordinat.value.y1,
          x2: koordinat.value.x2,
          y2: koordinat.value.y2,
          warna: warnaAktif.value
        }
    }

    const raw  = sessionStorage.getItem(ssKey.value)
    let data = raw ? JSON.parse(raw) : {}

    if (!data.kolomBaruList) {
      data.kolomBaruList = []
    }
    data.kolomBaruList.push(kolomBaru)
    sessionStorage.setItem(ssKey.value, JSON.stringify(data))
    router.replace(routeKembali.value)
  } catch (err) {
    alert(err.response?.data?.detail || 'Gagal menyimpan kolom. Coba lagi.')
  } finally {
    isSimpan.value = false
  }
}
</script>