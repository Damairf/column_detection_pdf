<template>
  <div class="flex h-screen bg-gray-100 overflow-hidden">

    <!-- ── Navbar Kiri (Sidebar) ─────────────────────────────────── -->
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
          <p class="text-xs text-gray-500 truncate">{{ user.divisi || '-' }}</p>
        </div>
      </div>

      <!-- Menu Navigasi -->
      <nav class="flex-1 px-3 py-4 flex flex-col gap-1">

        <!-- Beranda -->
        <router-link
          to="/beranda"
          class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150"
          :class="isActive('/beranda')
            ? 'bg-gray-900 text-white shadow'
            : 'text-gray-600 hover:bg-gray-100'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
          Beranda
        </router-link>

        <!-- Template -->
        <router-link
          to="/template"
          class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150"
          :class="isActive('/template')
            ? 'bg-gray-900 text-white shadow'
            : 'text-gray-600 hover:bg-gray-100'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Template
        </router-link>

      </nav>
    </aside>

    <!-- ── Area Kanan ────────────────────────────────────────────── -->
    <div class="flex flex-col flex-1 overflow-hidden">

      <!-- Navbar Atas -->
      <header class="h-14 bg-white border-b border-gray-200 flex items-center justify-between px-5 flex-shrink-0 shadow-sm">

        <div class="flex items-center gap-2">
          <!-- Undo -->
          <button
            @click="handleUndo"
            class="p-1.5 rounded-md transition"
            :class="canUndo
              ? 'text-gray-500 hover:bg-gray-300 hover:text-gray-800 cursor-pointer'
              : 'text-gray-300 cursor-not-allowed'"
            :title="canUndo ? 'Kembali' : 'Tidak bisa kembali lebih jauh'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
          </button>

          <!-- Redo -->
          <button
            @click="handleRedo"
            class="p-1.5 rounded-md transition"
            :class="canRedo
              ? 'text-gray-500 hover:bg-gray-300 hover:text-gray-800 cursor-pointer'
              : 'text-gray-300 cursor-not-allowed'"
            :title="canRedo ? 'Maju' : 'Tidak bisa maju lebih jauh'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
            </svg>
          </button>

          <!-- Reload -->
          <button
            @click="reloadPage"
            class="p-1.5 rounded-md text-gray-500 hover:bg-gray-300 hover:text-gray-800 transition cursor-pointer"
            :class="{ 'animate-spin': isReloading }"
            title="Muat Ulang"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </button>

          <span class="text-gray-300 mx-1">|</span>

          <!-- Breadcrumb -->
          <div class="flex items-center gap-1.5 text-sm text-gray-600">
            <span class="text-gray-400">/</span>
            <span class="font-semibold text-gray-800">{{ pageTitle }}</span>
          </div>
        </div>

        <!-- Logo -->
        <div class="flex items-center">
          <img src="/src/assets/logo-nasmoco.png" alt="Nasmoco" class="h-8 object-contain" />
        </div>
      </header>

      <!-- Konten -->
      <main class="flex-1 overflow-auto p-6">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route  = useRoute()
const isReloading = ref(false)
const avatarImg   = ref(null)

// ── Semua halaman dalam area auth ─────────────────────────────────────
const authPages = [
  '/beranda',
  '/template',
  '/template/tambah',
  '/template/tambah/kolom-baru',
  '/profile',
  '/profile/ubah',
]

const authHistory = ref([route.path])
const redoHistory = ref([])
const isUndoing   = ref(false)
const isRedoing   = ref(false)

watch(() => route.path, (newPath) => {
  if (isUndoing.value) { isUndoing.value = false; return }
  if (isRedoing.value) { isRedoing.value = false; return }
  if (authPages.includes(newPath)) {
    redoHistory.value = []
    if (authHistory.value[authHistory.value.length - 1] !== newPath) {
      authHistory.value.push(newPath)
    }
  }
})

const canUndo = computed(() => authHistory.value.length > 1)
const canRedo = computed(() => redoHistory.value.length > 0)

function handleUndo() {
  if (!canUndo.value) return
  isUndoing.value = true
  const cur = authHistory.value[authHistory.value.length - 1]
  redoHistory.value.push(cur)
  authHistory.value.pop()
  router.replace(authHistory.value[authHistory.value.length - 1])
}

function handleRedo() {
  if (!canRedo.value) return
  isRedoing.value = true
  const next = redoHistory.value.pop()
  authHistory.value.push(next)
  router.replace(next)
}

const user = computed(() => {
  try { return JSON.parse(localStorage.getItem('user')) || {} }
  catch { return {} }
})

// ── Breadcrumb ────────────────────────────────────────────────────────
const pageTitle = computed(() => {
  const titles = {
    '/beranda':                      'Beranda',
    '/template':                     'Template',
    '/template/tambah':              'Template / Tambah',
    '/template/tambah/kolom-baru':   'Template / Tambah / Kolom Baru',
    '/profile':                      'Profile',
    '/profile/ubah':                 'Profile / Ubah',
  }
  return titles[route.path] || route.path.replace(/^\//, '')
})

// ── isActive: aktif jika exact match atau sub-route ───────────────────
function isActive(basePath) {
  return route.path === basePath || route.path.startsWith(basePath + '/')
}

function reloadPage() {
  isReloading.value = true
  setTimeout(() => { window.location.reload() }, 300)
}

function handleAvatarError() {
  if (avatarImg.value) avatarImg.value.style.display = 'none'
}
</script>