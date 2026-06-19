<template>
  <div class="flex h-screen bg-gray-100 overflow-hidden">

    <!-- Modal Peringatan Idle Timeout -->
    <div
      v-if="showWarningModal"
      class="fixed inset-0 z-[9999] flex items-center justify-center"
      style="background: rgba(0,0,0,0.50);"
    >
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-sm mx-6 p-8 text-center">

        <h3 class="text-lg font-bold text-gray-800 mb-2">Sesi Akan Berakhir</h3>
        <p class="text-sm text-gray-500 mb-1">
          Anda tidak aktif selama beberapa waktu.
        </p>
        <p class="text-sm text-gray-500 mb-6">
          Logout otomatis dalam
          <span class="font-semibold text-red-500 tabular-nums">{{ countdown }}</span>
          detik.
        </p>

        <!-- Progress bar hitung mundur -->
        <div class="w-full bg-gray-200 rounded-full h-1.5 mb-6 overflow-hidden">
          <div
            class="h-1.5 rounded-full transition-all duration-1000 ease-linear"
            :class="countdown > 30 ? 'bg-yellow-400' : countdown > 10 ? 'bg-orange-400' : 'bg-red-500'"
            :style="{ width: `${(countdown / 60) * 100}%` }"
          ></div>
        </div>

        <!-- Tombol aksi -->
        <div class="flex gap-3">
          <button
            @click="logoutNow"
            class="flex-1 py-2.5 border border-gray-300 rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-50 transition cursor-pointer"
          >
            Keluar
          </button>
          <button
            @click="stayLoggedIn"
            class="flex-1 py-2.5 bg-gray-900 text-white rounded-lg text-sm font-semibold hover:bg-gray-700 transition cursor-pointer"
          >
            Tetap Masuk
          </button>
        </div>
      </div>
    </div>

    <!-- Sidebar -->
    <aside class="w-56 bg-white flex flex-col shadow-md flex-shrink-0">

      <!-- Profile -->
      <div
        class="flex items-center gap-3 px-4 py-4 border-b border-gray-100 cursor-pointer hover:bg-gray-50 transition"
        @click="router.push('/profile')"
        title="Lihat Profile"
      >
        <div class="w-10 h-10 rounded-full overflow-hidden flex-shrink-0 bg-gray-200">
          <img
            src="/src/assets/avatar-default.jpg"
            alt="Avatar"
            class="w-full h-full object-cover"
            @error="handleAvatarError"
            ref="avatarImg"
          />
        </div>
        <div class="overflow-hidden">
          <p class="text-sm font-bold text-gray-800 truncate">{{ user.nama || 'Pengguna' }}</p>
          <p class="text-xs text-gray-500 truncate">{{ user.divisi || '-' }}{{ user.cabang ? ` (${user.cabang})` : '' }}</p>
        </div>
      </div>

      <!-- Nav Menu -->
      <nav class="flex-1 px-3 py-4 flex flex-col gap-1">

        <router-link to="/beranda"
          class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150"
          :class="isActive('/beranda') ? 'bg-gray-900 text-white shadow' : 'text-gray-600 hover:bg-gray-100'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
          Beranda
        </router-link>

        <router-link v-if="user.role === 'admin'" to="/template"
          class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150"
          :class="isActive('/template') ? 'bg-gray-900 text-white shadow' : 'text-gray-600 hover:bg-gray-100'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Template
        </router-link>

        <router-link v-if="user.role === 'admin'" to="/evaluasi"
          class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150"
          :class="isActive('/evaluasi') ? 'bg-gray-900 text-white shadow' : 'text-gray-600 hover:bg-gray-100'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
          </svg>
          Evaluasi
        </router-link>

        <router-link to="/spk"
          class="flex items-center justify-between px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150"
          :class="isActive('/spk') ? 'bg-gray-900 text-white shadow' : 'text-gray-600 hover:bg-gray-100'"
        >
          <div class="flex items-center gap-3">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
            </svg>
            SPK
          </div>
          <span
            v-if="user.role === 'user' && unuploadedSpkCount > 0"
            class="flex items-center justify-center bg-red-500 text-white text-xs font-semibold h-5 min-w-[1.25rem] px-1 rounded-full"
          >
            {{ unuploadedSpkCount }}
          </span>
        </router-link>

        <router-link v-if="user.role === 'admin'" to="/pengguna"
          class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150"
          :class="isActive('/pengguna') ? 'bg-gray-900 text-white shadow' : 'text-gray-600 hover:bg-gray-100'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
          Pengguna
        </router-link>

        <router-link v-if="user.role === 'admin'" to="/cabang"
          class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150"
          :class="isActive('/cabang') ? 'bg-gray-900 text-white shadow' : 'text-gray-600 hover:bg-gray-100'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
          Cabang
        </router-link>

        <router-link v-if="user.role === 'admin'" to="/kustomisasi"
          class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150"
          :class="isActive('/kustomisasi') ? 'bg-gray-900 text-white shadow' : 'text-gray-600 hover:bg-gray-100'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
          </svg>
          Kustomisasi
        </router-link>

      </nav>
    </aside>

    <div class="flex flex-col flex-1 overflow-hidden">

      <header class="h-14 bg-white border-b border-gray-200 flex items-center justify-between px-5 flex-shrink-0 shadow-sm">
        <div class="flex items-center gap-2">
          <span class="text-gray-300 mx-1">|</span>
          <div class="flex items-center gap-1.5 text-sm text-gray-600">
            <span class="text-gray-400">/</span>
            <span class="font-semibold text-gray-800">{{ pageTitle }}</span>
          </div>
        </div>
        <div class="flex items-center">
          <img src="/src/assets/logo-nasmoco.png" alt="Nasmoco" class="h-8 object-contain" />
        </div>
      </header>

      <main class="flex-1 overflow-auto p-6">
        <slot />
      </main>
    </div>

  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { useIdleTimeout } from '../composables/useIdleTimeout'

const router    = useRouter()
const route     = useRoute()
const avatarImg = ref(null)

const unuploadedSpkCount = ref(0)

const { showWarningModal, countdown, stayLoggedIn, logoutNow } = useIdleTimeout()

const user = computed(() => {
  try { return JSON.parse(localStorage.getItem('user')) || {} }
  catch { return {} }
})

const pageTitle = computed(() => {
  const p    = route.path
  const mode = route.query.mode || ''
  const q    = mode === 'detail' ? 'Template / Detail / Ubah' : 'Template / Tambah'

  const map = {
    '/beranda':        'Beranda',
    '/beranda/tambah': 'Beranda / Tambah',
    '/template':       'Template',
    '/template/tambah':'Template / Tambah',
    '/profile':        'Profile',
    '/profile/ubah':   'Profile / Ubah',
    '/pengguna':       'Pengguna',
    '/cabang':         'Cabang',
    '/evaluasi':       'Evaluasi',
    '/spk':            'SPK',
    '/kustomisasi':    'Kustomisasi',
  }
  if (map[p]) return map[p]

  if (p === '/kolom/baru') return `${q} / Kolom Baru`
  if (p === '/kolom/edit') return `${q} / Edit Kolom`

  if (/^\/beranda\/detail\/\d+$/.test(p))        return 'Beranda / Detail'
  if (/^\/spk\/detail\/[^/]+$/.test(p))          return 'SPK / Detail'
  if (/^\/template\/detail\/\d+$/.test(p))        return 'Template / Detail'
  if (/^\/template\/detail\/\d+\/ubah$/.test(p))  return 'Template / Detail / Ubah'

  return p.replace(/^\//, '')
})

function isActive(basePath) {
  if (basePath === '/template') {
    return route.path === '/template'
      || route.path.startsWith('/template/')
      || route.path === '/kolom/baru'
      || route.path === '/kolom/edit'
  }
  if (basePath === '/beranda') {
    return route.path === '/beranda' || route.path.startsWith('/beranda/')
  }
  if (basePath === '/spk') {
    return route.path === '/spk' || route.path.startsWith('/spk/')
  }
  return route.path === basePath || route.path.startsWith(basePath + '/')
}

function handleAvatarError() {
  if (avatarImg.value) avatarImg.value.style.display = 'none'
}

onMounted(async () => {
  if (user.value.role === 'user') {
    try {
      const token = localStorage.getItem('token')
      const headers = { Authorization: `Bearer ${token}` }
      const [resSpk, resDoc] = await Promise.all([
        axios.get('/api/spk/',          { headers }),
        axios.get('/api/beranda/dokumen', { headers }),
      ])

      const spks   = resSpk.data.filter(s => s.id_cabang === user.value.id_cabang)
      const docIds = new Set(resDoc.data.map(d => d.id_spk).filter(Boolean))

      let count = 0
      for (const s of spks) {
        if (!docIds.has(s.id)) count++
      }
      unuploadedSpkCount.value = count
    } catch (err) {
      console.error('Gagal memuat badge SPK:', err)
    }
  }
})
</script>