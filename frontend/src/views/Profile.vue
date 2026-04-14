<template>
  <AppLayout>
    <div class="max-w-lg mx-auto mt-6">
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">

        <!-- Header card abu -->
        <div class="h-24 bg-gradient-to-r from-gray-700 to-gray-900"></div>

        <!-- Foto & Info -->
        <div class="px-8 pb-8">

          <!-- Avatar -->
          <div class="flex justify-center -mt-12 mb-4">
            <div class="w-24 h-24 rounded-full border-4 border-white shadow-md overflow-hidden bg-gray-200">
              <img
                src="/src/assets/avatar-default.jpg"
                alt="Foto Profil"
                class="w-full h-full object-cover"
              />
            </div>
          </div>

          <!-- Nama & Divisi -->
          <div class="text-center mb-6">
            <h2 class="text-xl font-bold text-gray-800">{{ form.nama || '-' }}</h2>
            <p class="text-sm text-gray-500">{{ form.divisi || '-' }}</p>
          </div>

          <!-- Mode Lihat -->
          <div v-if="!isEditing">
            <div class="space-y-3 mb-6">
              <div class="flex items-center gap-3 p-3 bg-gray-50 rounded-xl">
                <div class="w-8 h-8 rounded-lg bg-gray-200 flex items-center justify-center flex-shrink-0">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <div>
                  <p class="text-xs text-gray-400 leading-none mb-0.5">Nama</p>
                  <p class="text-sm font-semibold text-gray-700">{{ form.nama || '-' }}</p>
                </div>
              </div>

              <div class="flex items-center gap-3 p-3 bg-gray-50 rounded-xl">
                <div class="w-8 h-8 rounded-lg bg-gray-200 flex items-center justify-center flex-shrink-0">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                  </svg>
                </div>
                <div>
                  <p class="text-xs text-gray-400 leading-none mb-0.5">Divisi</p>
                  <p class="text-sm font-semibold text-gray-700">{{ form.divisi || '-' }}</p>
                </div>
              </div>

              <div class="flex items-center gap-3 p-3 bg-gray-50 rounded-xl">
                <div class="w-8 h-8 rounded-lg bg-gray-200 flex items-center justify-center flex-shrink-0">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </div>
                <div>
                  <p class="text-xs text-gray-400 leading-none mb-0.5">Username</p>
                  <p class="text-sm font-semibold text-gray-700">{{ form.username || '-' }}</p>
                </div>
              </div>
            </div>

            <!-- Tombol Ubah Profile & Keluar -->
            <div class="flex flex-col gap-2">
              <button
                @click="startEdit"
                class="cursor-pointer w-full py-2.5 rounded-xl font-semibold text-sm text-white transition-all duration-200 hover:brightness-110 active:scale-95 shadow-sm"
                style="background: #1f2937;"
              >
                Ubah Profile
              </button>
              <button
                @click="handleKeluar"
                class="cursor-pointer w-full py-2.5 rounded-xl font-semibold text-sm text-white bg-red-600 hover:bg-red-800 transition-all duration-200 active:scale-95"
              >
                Keluar
              </button>
            </div>
          </div>

          <!-- Mode Edit -->
          <div v-else>
            <form @submit.prevent="handleSimpan" novalidate>

              <!-- Nama -->
              <div class="mb-3">
                <label class="block text-xs font-semibold text-gray-500 mb-1 uppercase tracking-wide">Nama</label>
                <input
                  v-model="form.nama"
                  type="text"
                  placeholder="Masukkan nama..."
                  class="w-full px-3 py-2.5 rounded-xl border border-gray-200 text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-400 transition bg-gray-50"
                  :class="{ 'ring-2 ring-red-400 border-red-300': errors.nama }"
                />
                <p v-if="errors.nama" class="text-red-500 text-xs mt-1">{{ errors.nama }}</p>
              </div>

              <!-- Divisi -->
              <div class="mb-3">
                <label class="block text-xs font-semibold text-gray-500 mb-1 uppercase tracking-wide">Divisi</label>
                <input
                  v-model="form.divisi"
                  type="text"
                  placeholder="Masukkan divisi..."
                  class="w-full px-3 py-2.5 rounded-xl border border-gray-200 text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-400 transition bg-gray-50"
                  :class="{ 'ring-2 ring-red-400 border-red-300': errors.divisi }"
                />
                <p v-if="errors.divisi" class="text-red-500 text-xs mt-1">{{ errors.divisi }}</p>
              </div>

              <!-- Username -->
              <div class="mb-3">
                <label class="block text-xs font-semibold text-gray-500 mb-1 uppercase tracking-wide">Username</label>
                <input
                  v-model="form.username"
                  type="text"
                  placeholder="Masukkan username..."
                  class="w-full px-3 py-2.5 rounded-xl border border-gray-200 text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-400 transition bg-gray-50"
                  :class="{ 'ring-2 ring-red-400 border-red-300': errors.username }"
                />
                <p v-if="errors.username" class="text-red-500 text-xs mt-1">{{ errors.username }}</p>
              </div>

              <!-- Password Baru -->
              <div class="mb-5">
                <label class="block text-xs font-semibold text-gray-500 mb-1 uppercase tracking-wide">
                  Password Baru
                  <span class="text-gray-400 font-normal normal-case">(kosongkan jika tidak diubah)</span>
                </label>
                <div class="relative">
                  <input
                    v-model="form.password"
                    :type="showPassword ? 'text' : 'password'"
                    placeholder="Masukkan password baru..."
                    class="w-full px-3 py-2.5 rounded-xl border border-gray-200 text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-400 transition bg-gray-50 pr-10"
                    :class="{ 'ring-2 ring-red-400 border-red-300': errors.password }"
                  />
                  <button
                    type="button"
                    @click="showPassword = !showPassword"
                    class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition"
                  >
                    <svg v-if="!showPassword" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 4.411m0 0L21 21" />
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0zM2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  </button>
                </div>
                <p v-if="errors.password" class="text-red-500 text-xs mt-1">{{ errors.password }}</p>
              </div>

              <!-- Pesan error server -->
              <div v-if="serverError" class="mb-3 p-3 bg-red-50 border border-red-200 rounded-xl text-red-600 text-sm text-center">
                {{ serverError }}
              </div>

              <!-- Pesan sukses -->
              <div v-if="successMsg" class="mb-3 p-3 bg-green-50 border border-green-200 rounded-xl text-green-600 text-sm text-center">
                {{ successMsg }}
              </div>

              <!-- Tombol Simpan & Batal -->
              <div class="flex gap-2">
                <button
                  type="button"
                  @click="cancelEdit"
                  class="cursor-pointer flex-1 py-2.5 rounded-xl font-semibold text-sm text-gray-600 bg-gray-100 hover:bg-gray-200 transition-all duration-200 active:scale-95"
                >
                  Batal
                </button>
                <button
                  type="submit"
                  :disabled="loading"
                  class="cursor-pointer flex-1 py-2.5 rounded-xl font-semibold text-sm text-white transition-all duration-200 hover:brightness-110 active:scale-95 shadow-sm"
                  style="background: #1f2937;"
                  :class="loading ? 'opacity-70 cursor-not-allowed' : ''"
                >
                  <span v-if="loading" class="flex items-center justify-center gap-2">
                    <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                    </svg>
                    Menyimpan...
                  </span>
                  <span v-else>Simpan</span>
                </button>
              </div>
            </form>
          </div>

        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import AppLayout from '../components/AppLayout.vue'

const router = useRouter()
const route = useRoute()
const isEditing = ref(false)
const loading = ref(false)
const showPassword = ref(false)
const serverError = ref('')
const successMsg = ref('')

const form = reactive({
  nama: '',
  divisi: '',
  username: '',
  password: ''
})

const originalData = reactive({
  nama: '',
  divisi: '',
  username: ''
})

const errors = reactive({
  nama: '',
  divisi: '',
  username: '',
  password: ''
})

watch(() => route.path, (path) => {
  if (path === '/profile/ubah') {
    isEditing.value = true
  } else if (path === '/profile') {
    isEditing.value = false
  }
}, { immediate: true })

onMounted(() => {
  const stored = localStorage.getItem('user')
  if (stored) {
    const user = JSON.parse(stored)
    form.nama = user.nama || ''
    form.divisi = user.divisi || ''
    form.username = user.username || ''
    originalData.nama = user.nama || ''
    originalData.divisi = user.divisi || ''
    originalData.username = user.username || ''
  }
})

function startEdit() {
  serverError.value = ''
  successMsg.value = ''
  form.password = ''
  router.push('/profile/ubah')
}

function cancelEdit() {
  form.nama = originalData.nama
  form.divisi = originalData.divisi
  form.username = originalData.username
  form.password = ''
  errors.nama = ''
  errors.divisi = ''
  errors.username = ''
  errors.password = ''
  serverError.value = ''
  successMsg.value = ''
  router.replace('/profile')
}

function validate() {
  let valid = true
  errors.nama = ''
  errors.divisi = ''
  errors.username = ''
  errors.password = ''

  if (!form.nama.trim()) { errors.nama = 'Nama wajib diisi.'; valid = false }
  if (!form.divisi.trim()) { errors.divisi = 'Divisi wajib diisi.'; valid = false }
  if (!form.username.trim()) { errors.username = 'Username wajib diisi.'; valid = false }
  if (form.password && form.password.length < 6) {
    errors.password = 'Password minimal 6 karakter.'
    valid = false
  }

  return valid
}

async function handleSimpan() {
  serverError.value = ''
  successMsg.value = ''
  if (!validate()) return

  loading.value = true
  try {
    const token = localStorage.getItem('token')
    const user = JSON.parse(localStorage.getItem('user'))

    const payload = {
      nama: form.nama,
      divisi: form.divisi,
      username: form.username
    }
    if (form.password) payload.password = form.password

    const response = await axios.put(`/api/profile/${user.id}`, payload, {
      headers: { Authorization: `Bearer ${token}` }
    })

    const updatedUser = { ...user, ...response.data }
    localStorage.setItem('user', JSON.stringify(updatedUser))

    originalData.nama = form.nama
    originalData.divisi = form.divisi
    originalData.username = form.username

    successMsg.value = 'Profile berhasil diperbarui!'
    form.password = ''

    setTimeout(() => {
      successMsg.value = ''
      router.replace('/profile')
    }, 1500)

  } catch (err) {
    if (err.response?.data?.detail) {
      serverError.value = err.response.data.detail
    } else {
      serverError.value = 'Terjadi kesalahan. Coba lagi.'
    }
  } finally {
    loading.value = false
  }
}

function handleKeluar() {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.replace('/masuk')
}
</script>