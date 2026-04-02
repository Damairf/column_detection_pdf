<template>
  <div class="relative min-h-screen w-full overflow-hidden flex items-center justify-center">

    <!-- Background image -->
    <div class="absolute inset-0 z-0">
      <img
        src="/src/assets/bg-nasmoco.jpeg"
        alt="Nasmoco Background"
        class="w-full h-full object-cover"
      />
    </div>

    <!-- Card container -->
    <div class="relative z-10 w-full max-w-md mx-6">
      <div
        class="rounded-2xl shadow-2xl px-8 py-8"
        style="background: rgba(100, 110, 120, 0.70); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.15);"
      >

        <!-- Logo -->
        <div class="flex justify-center mb-6">
          <img
            src="/src/assets/logo-nasmoco.png"
            alt="Nasmoco Column Detection"
            class="h-16 object-contain"
          />
        </div>

        <!-- Form -->
        <form @submit.prevent="handleDaftar" novalidate>

          <!-- Nama -->
          <div class="mb-3">
            <label class="block text-white font-semibold mb-0.5 text-sm">Nama</label>
            <input
              v-model="form.nama"
              type="text"
              placeholder="Masukkan Nama anda....."
              class="w-full px-3 py-2 rounded-lg text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-sky-400 transition text-sm border-0"
              style="background: rgba(255,255,255,0.88);"
              :class="{ 'ring-2 ring-red-400': errors.nama }"
            />
            <p v-if="errors.nama" class="text-red-700 text-xs mt-1">{{ errors.nama }}</p>
          </div>

          <!-- Divisi -->
          <div class="mb-3">
            <label class="block text-white font-semibold mb-0.5 text-sm">Divisi</label>
            <input
              v-model="form.divisi"
              type="text"
              placeholder="Masukkan divisi anda....."
              class="w-full px-3 py-2 rounded-lg text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-sky-400 transition text-sm border-0"
              style="background: rgba(255,255,255,0.88);"
              :class="{ 'ring-2 ring-red-400': errors.divisi }"
            />
            <p v-if="errors.divisi" class="text-red-700 text-xs mt-1">{{ errors.divisi }}</p>
          </div>

          <!-- username -->
          <div class="mb-3">
            <label class="block text-white font-semibold mb-0.5 text-sm">Username</label>
            <input
              v-model="form.username"
              type="username"
              placeholder="Masukkan username anda....."
              class="w-full px-3 py-2 rounded-lg text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-sky-400 transition text-sm border-0"
              style="background: rgba(255,255,255,0.88);"
              :class="{ 'ring-2 ring-red-400': errors.username }"
            />
            <p v-if="errors.username" class="text-red-700 text-xs mt-1">{{ errors.username }}</p>
          </div>

          <!-- Password -->
          <div class="mb-6">
            <label class="block text-white font-semibold mb-0.5 text-sm">Password</label>
            <div class="relative">
              <input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Masukkan password anda....."
                class="w-full px-4 py-3 rounded-lg text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-sky-400 transition text-sm pr-11 border-0"
                style="background: rgba(255,255,255,0.88);"
                :class="{ 'ring-2 ring-red-400': errors.password }"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="cursor-pointer absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700 transition"
              >
                <svg v-if="!showPassword" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 4.411m0 0L21 21" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </button>
            </div>
            <p v-if="errors.password" class="text-red-700 text-xs mt-1">{{ errors.password }}</p>
          </div>

          <!-- Error dari server -->
          <div v-if="serverError" class="mb-4 p-3 bg-red-500/30 border border-red-400/50 rounded-lg text-red-200 text-sm text-center">
            {{ serverError }}
          </div>

          <!-- Sukses -->
          <div v-if="successMsg" class="mb-4 p-3 bg-green-500/30 border border-green-400/50 rounded-lg text-green-200 text-sm text-center">
            {{ successMsg }}
          </div>

          <!-- Tombol Daftar -->
          <button
            type="submit"
            :disabled="loading"
            class="cursor-pointer w-full py-2 rounded-lg font-bold text-white text-sm tracking-widest uppercase transition-all duration-200 shadow-md"
            style="background: #29b6f6;"
            :class="loading ? 'opacity-70 cursor-not-allowed' : 'hover:brightness-110 active:scale-95'"
          >
            <span v-if="loading" class="flex items-center justify-center gap-2">
              <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
              Memproses...
            </span>
            <span v-else>Daftar</span>
          </button>

          <!-- Link ke Masuk -->
          <p class="text-center text-sm text-white mt-4 font-medium">
            Sudah punya akun?
            <router-link to="/masuk" class="text-sky-300 hover:text-sky-200 font-semibold ml-1 transition">Masuk</router-link>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const showPassword = ref(false)
const loading = ref(false)
const serverError = ref('')
const successMsg = ref('')

const form = reactive({
  nama: '',
  divisi: '',
  username: '',
  password: ''
})

const errors = reactive({
  nama: '',
  divisi: '',
  username: '',
  password: ''
})

function validate() {
  let valid = true
  errors.nama = ''
  errors.divisi = ''
  errors.username = ''
  errors.password = ''

  if (!form.nama.trim()) {
    errors.nama = 'Nama wajib diisi.'
    valid = false
  }

  if (!form.divisi.trim()) {
    errors.divisi = 'Divisi wajib diisi.'
    valid = false
  }

  if (!form.username) {
    errors.username = 'username wajib diisi.'
    valid = false
  }

  if (!form.password) {
    errors.password = 'Password wajib diisi.'
    valid = false
  } else if (form.password.length < 6) {
    errors.password = 'Password minimal 6 karakter.'
    valid = false
  }

  return valid
}

async function handleDaftar() {
  serverError.value = ''
  successMsg.value = ''
  if (!validate()) return

  loading.value = true
  try {
    await axios.post('/api/auth/daftar', {
      nama: form.nama,
      divisi: form.divisi,
      username: form.username,
      password: form.password
    })

    successMsg.value = 'Pendaftaran berhasil! Mengarahkan ke halaman masuk...'

    setTimeout(() => router.replace('/masuk'), 1500)
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
</script>