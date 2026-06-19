<template>
  <AppLayout>
    <div class="flex flex-col min-h-full">
      <div class="flex items-center justify-between mb-4">
        <div class="relative">
          <span class="absolute inset-y-0 left-3 flex items-center text-gray-400 pointer-events-none">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35m0 0A7.5 7.5 0 1010.5 18a7.5 7.5 0 006.15-3.35z" />
            </svg>
          </span>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Cari SPK...."
            class="pl-9 pr-4 py-2 w-64 border border-gray-300 rounded-lg text-sm text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent bg-white shadow-sm"
          />
        </div>

        <div class="flex items-center gap-2">
          <!-- Urut -->
          <div class="relative" @mouseenter="handleMouseEnter" @mouseleave="handleMouseLeave">
            <button class="flex items-center gap-1.5 px-4 py-2 bg-gray-900 text-white text-sm font-medium rounded-lg hover:bg-gray-800 transition shadow-sm">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V4m0 0L3 8m4-4l4 4M17 8v12m0 0l4-4m-4 4l-4-4" />
              </svg>
              Urut
            </button>
            <div v-if="showUrutDropdown" class="absolute right-0 top-full mt-1.5 w-48 bg-white border border-gray-200 rounded-lg shadow-lg z-50 overflow-hidden">
              <button
                v-for="opt in sortOptions" :key="opt.value"
                @click="selectSort(opt.value)"
                class="cursor-pointer w-full text-left px-4 py-2.5 text-sm transition"
                :class="sortKey === opt.value ? 'bg-gray-900 text-white font-medium' : 'text-gray-700 hover:bg-gray-100'"
              >
                {{ opt.label }}
              </button>
            </div>
          </div>

          <button v-if="currentUser.role === 'admin'"
            @click="showAktivasiModal = true"
            class="cursor-pointer flex items-center gap-1.5 px-4 py-2 border border-gray-300 bg-white text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-50 transition shadow-sm"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Aktivasi SPK
          </button>
          
          <button v-if="currentUser.role === 'admin'"
            @click="showUploadModal = true"
            class="cursor-pointer flex items-center gap-1.5 px-4 py-2 border border-gray-300 bg-white text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-50 transition shadow-sm"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
            </svg>
            Upload SPK
          </button>

          <button v-if="currentUser.role === 'admin'" @click="openAddModal" class="cursor-pointer flex items-center gap-1.5 px-4 py-2 border border-gray-300 bg-white text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-50 transition shadow-sm">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Tambah SPK
          </button>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b border-gray-200 bg-white">
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700">Nomor SPK</th>
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700">Nama SPK</th>
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700">Tanggal Retail</th>
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700">Cabang</th>
                <th v-if="currentUser.role === 'admin'" class="px-5 py-3.5 text-center font-semibold text-gray-700">ID Template</th>
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700 w-32">Status</th>
                <th v-if="currentUser.role === 'admin'" class="px-5 py-3.5 text-center font-semibold text-gray-700 w-24">Detail</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading">
                <td colspan="5" class="px-5 py-10 text-center text-gray-400 text-sm">Memuat data...</td>
              </tr>
              <tr v-else-if="paginatedData.length === 0">
                <td colspan="5" class="px-5 py-10 text-center text-gray-400 text-sm">Tidak ada data ditemukan.</td>
              </tr>
              <tr v-else v-for="spk in paginatedData" :key="spk.id" class="border-b border-gray-100 hover:bg-gray-50 transition-colors">
                <td class="px-5 py-3 text-center text-gray-700 font-medium">{{ spk.id }}</td>
                <td class="px-5 py-3 text-center text-gray-700">{{ spk.nama_spk }}</td>
                <td class="px-5 py-3 text-center text-gray-500">{{ formatTanggal(spk.tgl_retail) }}</td>
                <td class="px-5 py-3 text-center text-gray-700">{{ getNamaCabang(spk.id_cabang) }}</td>
                <td v-if="currentUser.role === 'admin'" class="px-5 py-3 text-center text-gray-500">{{ spk.id_template ?? '—' }}</td>
                  <td class="px-5 py-3 text-center">
                    <select
                      v-if="currentUser.role === 'admin'"
                      :value="spk.status ?? 'Aktif'"
                      @change="ubahStatus(spk, $event.target.value)"
                      class="px-2 py-1 text-sm font-medium rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-400 cursor-pointer transition"
                      :class="(spk.status ?? 'Aktif') === 'Aktif'"
                    >
                      <option value="Aktif">Aktif</option>
                      <option value="Nonaktif">Nonaktif</option>
                    </select>
                    <span
                      v-else
                      class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold"
                      :class="getSpkStatus(spk.id) === 'Sudah' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-600'"
                    >
                      {{ getSpkStatus(spk.id) }}
                    </span>
                  </td>
                <td v-if="currentUser.role === 'admin'" class="px-5 py-3 text-center flex items-center justify-center gap-3">
                  <button @click="lihatDetail(spk.id)" class="text-blue-500 hover:text-blue-700 font-medium hover:underline transition">
                    Detail
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div class="flex items-center justify-center gap-2 py-5 border-t border-gray-100">
          <button @click="goToPage(1)" :disabled="currentPage === 1" class="w-9 h-9 flex items-center justify-center rounded-lg font-bold transition" :class="currentPage === 1 ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-gray-900 text-white hover:bg-gray-700 cursor-pointer'"><svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M11 19l-7-7 7-7M19 19l-7-7 7-7" /></svg></button>
          <button @click="goToPage(currentPage - 1)" :disabled="currentPage === 1" class="w-9 h-9 flex items-center justify-center rounded-lg font-bold transition" :class="currentPage === 1 ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-gray-900 text-white hover:bg-gray-700 cursor-pointer'"><svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7" /></svg></button>
          <input type="number" :value="currentPage" @change="onPageInputChange" @keydown.enter="onPageInputChange" min="1" :max="totalPages" class="w-12 h-9 text-center border border-gray-300 rounded-lg text-sm font-medium text-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none" />
          <button @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages || totalPages === 0" class="w-9 h-9 flex items-center justify-center rounded-lg font-bold transition" :class="currentPage === totalPages || totalPages === 0 ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-gray-900 text-white hover:bg-gray-700 cursor-pointer'"><svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7" /></svg></button>
          <button @click="goToPage(totalPages)" :disabled="currentPage === totalPages || totalPages === 0" class="w-9 h-9 flex items-center justify-center rounded-lg font-bold transition" :class="currentPage === totalPages || totalPages === 0 ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-gray-900 text-white hover:bg-gray-700 cursor-pointer'"><svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 5l7 7-7 7M5 5l7 7-7 7" /></svg></button>
        </div>
      </div>
      <!-- Footer Warning -->
      <!-- <div class="mt-auto pt-6 text-xs text-gray-400 text-center border-t border-gray-100">
        Sistem ini bisa melakukan kesalahan. Silahkan periksa kembali hasilnya
      </div> -->
    </div>
    
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40" @click.self="closeModal">
      <div class="bg-white rounded-2xl w-full max-w-lg p-6 shadow-xl relative">
        <h2 class="text-xl font-bold text-gray-800 mb-6">Tambah SPK</h2>
        <form @submit.prevent="handleSimpan">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Nomor SPK</label>
              <input v-model="form.id" required type="text" class="w-full px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent bg-gray-50" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Nama SPK</label>
              <input v-model="form.nama_spk" required type="text" class="w-full px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent bg-gray-50" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Tanggal Retail</label>
              <input v-model="form.tgl_retail" required type="date" class="w-full px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent bg-gray-50" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Cabang</label>
              <select v-model="form.id_cabang" required class="w-full px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent bg-gray-50">
                <option :value="null" disabled>Pilih Cabang</option>
                <option v-for="c in listCabang" :key="c.id" :value="c.id">{{ c.nama_cabang }}</option>
              </select>
            </div>  
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Pilih Template</label>
              <div class="relative mb-2">
                <span class="absolute inset-y-0 left-3 flex items-center text-gray-400 pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35m0 0A7.5 7.5 0 1010.5 18a7.5 7.5 0 006.15-3.35z" />
                  </svg>
                </span>
                <input
                  v-model="templateSearch"
                  type="text"
                  placeholder="Cari template, tekan Enter untuk mencari..."
                  class="w-full pl-9 pr-4 py-2 border border-gray-300 rounded-lg text-sm text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent bg-gray-50"
                  @keydown.enter.prevent="submitTemplateSearch"
                />
              </div>

              <div
                v-if="!templateSearchSubmitted"
                class="border border-gray-300 rounded-lg p-3 bg-gray-50 text-sm text-gray-400 text-center"
              >
                Belum ada template dipilih.
              </div>

              <div
                v-else
                class="overflow-y-auto border border-gray-300 rounded-lg p-2 bg-gray-50"
                style="max-height: calc(5 * 2.25rem);"
              >
                <label
                  v-for="t in filteredTemplates"
                  :key="t.id"
                  class="flex items-center gap-2 cursor-pointer rounded px-1 hover:bg-gray-100"
                  style="height: 2.25rem;"
                >
                  <input
                    type="radio"
                    :value="t.id"
                    v-model="form.template_id"
                    name="template"
                    class="w-4 h-4 text-gray-900 border-gray-300 focus:ring-gray-900"
                  />
                  <span class="text-sm text-gray-700 truncate">{{ t.nama_template }}</span>
                </label>
                <div v-if="filteredTemplates.length === 0" class="text-sm text-gray-400 text-center py-2">
                  Tidak ada template ditemukan.
                </div>
              </div>
            </div>
          </div>
          <div v-if="formError" class="mt-4 text-red-500 text-sm">{{ formError }}</div>
          <div class="mt-8 flex justify-end gap-3">
            <button type="button" @click="closeModal" class="cursor-pointer px-5 py-2 text-sm font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition">Batal</button>
            <button type="submit" :disabled="saving" class="cursor-pointer px-5 py-2 text-sm font-medium text-white bg-gray-900 rounded-lg hover:bg-gray-800 transition disabled:opacity-50">
              {{ saving ? 'Menyimpan...' : 'Simpan' }}
            </button>
          </div>
        </form>
      </div>
    </div>
    <!-- Modal Upload SPK -->
    <div
      v-if="showUploadModal"
      class="fixed inset-0 z-50 flex flex-col items-center justify-center gap-3"
      style="background: rgba(0,0,0,0.35);"
      @click.self="closeUploadModal"
    >
      <!-- Notifikasi Error Upload -->
      <div
        v-if="uploadError"
        class="w-full max-w-lg mx-6 bg-white rounded px-4 py-3"
        style="border-left: 3px solid #9b3a2a;"
      >
        <span class="text-sm text-gray-700">{{ uploadError }}</span>
      </div>

      <!-- Notifikasi Duplikat Upload -->
      <div
        v-if="uploadDuplikat.length > 0"
        class="w-full max-w-lg mx-6 bg-white rounded px-4 py-3"
        style="border-left: 3px solid #8a6d1e;"
      >
        <span class="text-sm text-gray-700"><strong>{{ uploadDuplikat.length }} SPK</strong> sudah pernah ditambahkan sebelumnya</span>
      </div>

      <!-- Notifikasi Sukses Upload -->
      <div
        v-if="uploadSuccess"
        class="w-full max-w-lg mx-6 bg-white rounded px-4 py-3"
        style="border-left: 3px solid #3d6b28;"
      >
        <span class="text-sm text-gray-700">{{ uploadSuccess }}</span>
      </div>

      <!-- Progress Upload -->
      <div
        v-if="isUploading"
        class="w-full max-w-lg mx-6 bg-white rounded px-4 py-3"
      >
        <div class="flex justify-between mb-2">
          <span class="text-xs text-gray-500">Mengunggah {{ uploadProgress.current }} / {{ uploadProgress.total }} SPK...</span>
          <span class="text-xs text-gray-500">{{ uploadProgress.percent }}%</span>
        </div>
        <div class="w-full bg-gray-200 h-1">
          <div class="bg-gray-600 h-1 transition-all duration-300" :style="{ width: uploadProgress.percent + '%' }"></div>
        </div>
      </div>

      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg mx-6 p-8">
        <div
          class="border-2 border-dashed rounded-xl flex flex-col items-center justify-center py-14 px-6 mb-6 transition-colors cursor-pointer"
          :class="isDragging
            ? 'border-gray-500 bg-gray-100'
            : 'border-gray-300 bg-gray-50 hover:border-gray-400 hover:bg-gray-100'"
          @dragover.prevent="isDragging = true"
          @dragleave.prevent="isDragging = false"
          @drop.prevent="handleDrop"
          @click="triggerFileInput"
        >
          <div class="w-14 h-14 rounded-full bg-gray-200 flex items-center justify-center mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          </div>
          <p class="text-sm text-gray-500">Tarik dan unggah file XLSX anda</p>
          <p class="text-xs text-gray-400 mt-1">Format: Nomor SPK, Nama SPK, Tanggal Retail, ID Cabang, ID Template</p>
        </div>

        <input ref="fileInputRef" type="file" accept=".xlsx" class="hidden" @change="handleFileInput" />

        <div class="flex justify-center gap-3">
          <button
            @click.stop="triggerFileInput"
            :disabled="isUploading"
            class="flex items-center gap-2 px-5 py-2 border border-gray-300 rounded-lg text-sm text-gray-600 bg-white hover:bg-gray-50 transition shadow-sm"
            :class="isUploading ? 'opacity-60 cursor-not-allowed' : 'cursor-pointer'"
          >
            <span v-if="isUploading" class="flex items-center gap-2">
              <svg class="animate-spin h-4 w-4 text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
              Mengunggah...
            </span>
            <span v-else class="flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
              </svg>
              Unggah file
            </span>
          </button>
        </div>
      </div>
    </div>
    <!-- Modal Aktivasi SPK -->
    <div
      v-if="showAktivasiModal"
      class="fixed inset-0 z-50 flex flex-col items-center justify-center gap-3"
      style="background: rgba(0,0,0,0.35);"
      @click.self="closeAktivasiModal"
    >
      <!-- Notifikasi Error Aktivasi -->
      <div
        v-if="aktivasiError"
        class="w-full max-w-lg mx-6 bg-white rounded px-4 py-3"
        style="border-left: 3px solid #9b3a2a;"
      >
        <span class="text-sm text-gray-700">{{ aktivasiError }}</span>
      </div>

      <!-- Notifikasi Tidak Ditemukan Aktivasi -->
      <div
        v-if="aktivasiTidakDitemukan.length > 0"
        class="w-full max-w-lg mx-6 bg-white rounded px-4 py-3"
        style="border-left: 3px solid #8a6d1e;"
      >
        <span class="text-sm text-gray-700"><strong>{{ aktivasiTidakDitemukan.length }} SPK</strong> tidak ditemukan di dalam sistem</span>
      </div>

      <!-- Notifikasi Sukses Aktivasi -->
      <div
        v-if="aktivasiSuccess"
        class="w-full max-w-lg mx-6 bg-white rounded px-4 py-3"
        style="border-left: 3px solid #3d6b28;"
      >
        <span class="text-sm text-gray-700">{{ aktivasiSuccess }}</span>
      </div>

      <!-- Progress Aktivasi -->
      <div
        v-if="isAktivasi"
        class="w-full max-w-lg mx-6 bg-white rounded px-4 py-3"
      >
        <div class="flex justify-between mb-2">
          <span class="text-xs text-gray-500">Mengunggah {{ aktivasiProgress.current }} / {{ aktivasiProgress.total }} SPK...</span>
          <span class="text-xs text-gray-500">{{ aktivasiProgress.percent }}%</span>
        </div>
        <div class="w-full bg-gray-200 h-1">
          <div class="bg-gray-600 h-1 transition-all duration-300" :style="{ width: aktivasiProgress.percent + '%' }"></div>
        </div>
      </div>

      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg mx-6 p-8">
        <div
          class="border-2 border-dashed rounded-xl flex flex-col items-center justify-center py-14 px-6 mb-6 transition-colors cursor-pointer"
          :class="isAktivasiDragging
            ? 'border-gray-500 bg-gray-100'
            : 'border-gray-300 bg-gray-50 hover:border-gray-400 hover:bg-gray-100'"
          @dragover.prevent="isAktivasiDragging = true"
          @dragleave.prevent="isAktivasiDragging = false"
          @drop.prevent="handleAktivasiDrop"
          @click="triggerAktivasiFileInput"
        >
          <div class="w-14 h-14 rounded-full bg-gray-200 flex items-center justify-center mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          </div>
          <p class="text-sm text-gray-500">Tarik dan unggah file XLSX anda</p>
          <p class="text-xs text-gray-400 mt-1">Format: Nomor SPK, Nama SPK, Tanggal Retail, Status</p>
          <p class="text-xs text-gray-400 mt-0.5">(Status: 1 = Aktif dan 0 = Nonaktif)</p>
        </div>

        <input ref="aktivasiFileInputRef" type="file" accept=".xlsx" class="hidden" @change="handleAktivasiFileInput" />

        <div class="flex justify-center gap-3">
          <button
            @click.stop="triggerAktivasiFileInput"
            :disabled="isAktivasi"
            class="flex items-center gap-2 px-5 py-2 border border-gray-300 rounded-lg text-sm text-gray-600 bg-white hover:bg-gray-50 transition shadow-sm"
            :class="isAktivasi ? 'opacity-60 cursor-not-allowed' : 'cursor-pointer'"
          >
            <span v-if="isAktivasi" class="flex items-center gap-2">
              <svg class="animate-spin h-4 w-4 text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
              Memproses...
            </span>
            <span v-else class="flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
              </svg>
              Unggah file
            </span>
          </button>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import AppLayout from '../components/AppLayout.vue'
import * as XLSX from 'xlsx'

const router = useRouter()

const spks = ref([])
const listTemplate = ref([])
const listCabang = ref([])
const loading = ref(false)
const errorMsg = ref('')

const showUploadModal = ref(false)
const isDragging      = ref(false)
const isUploading     = ref(false)
const uploadError   = ref('')
const uploadSuccess = ref('')
const uploadDuplikat = ref([])
const fileInputRef    = ref(null)
const uploadProgress  = ref({ current: 0, total: 0, percent: 0 })

const showAktivasiModal      = ref(false)
const isAktivasiDragging     = ref(false)
const isAktivasi             = ref(false)
const aktivasiError          = ref('')
const aktivasiSuccess        = ref('')
const aktivasiTidakDitemukan = ref([])
const aktivasiFileInputRef   = ref(null)
const aktivasiProgress       = ref({ current: 0, total: 0, percent: 0 })

const searchQuery = ref('')
const currentPage = ref(1)
const totalPages = ref(1)
const itemsPerPage = 10
const showUrutDropdown = ref(false)
const sortKey = ref('tgl-desc')
const uploadedSpkIds = ref(new Set())

function getSpkStatus(spkId) {
  return uploadedSpkIds.value.has(spkId) ? 'Sudah' : 'Belum'
}

const sortOptions = [
  { label: 'A - Z (Menurun)',   value: 'az-desc'  },
  { label: 'A - Z (Menaik)',    value: 'az-asc'   },
  { label: 'Tanggal (Menurun)', value: 'tgl-desc' },
  { label: 'Tanggal (Menaik)',  value: 'tgl-asc'  },
]

const showModal = ref(false)
const saving = ref(false)
const templateSearch = ref('')
const templateSearchSubmitted = ref(false)

function submitTemplateSearch() {
  templateSearchSubmitted.value = true
}

const filteredTemplates = computed(() => {
  const q = templateSearch.value.toLowerCase().trim()
  if (!q) return listTemplate.value
  return listTemplate.value.filter(t => t.nama_template.toLowerCase().includes(q))
})
const formError = ref('')

const currentUser = computed(() => {
  try { return JSON.parse(localStorage.getItem('user')) || {} } 
  catch { return {} }
})

const form = ref({ id: '', nama_spk: '', tgl_retail: '', template_id: null, id_cabang: null })

function lihatDetail(id) { router.push(`/spk/detail/${id}`) }

async function ubahStatus(spk, nilaiBaru) {
  const statusLama = spk.status
  spk.status = nilaiBaru
  try {
    const token = localStorage.getItem('token')
    await axios.patch(`/api/spk/${spk.id}/status`, { status: nilaiBaru }, {
      headers: { Authorization: `Bearer ${token}` }
    })
  } catch (err) {
    spk.status = statusLama
    alert('Gagal mengubah status SPK.')
  }
}

async function fetchSPK() {
  loading.value = true
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get('/api/spk/', { 
      headers: { Authorization: `Bearer ${token}` },
      params: {
        page: currentPage.value,
        limit: itemsPerPage,
        search: searchQuery.value
      }
    })
    spks.value = res.data.data
    totalPages.value = Math.ceil(res.data.total / itemsPerPage) || 1
  } catch (err) {
    errorMsg.value = 'Gagal memuat data SPK.'
  } finally {
    loading.value = false
  }
}

async function fetchTemplates() {
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get('/api/template/list', { headers: { Authorization: `Bearer ${token}` } })
    listTemplate.value = res.data
  } catch (err) {}
}

async function fetchCabang() {
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get('/api/pengguna/cabang', { headers: { Authorization: `Bearer ${token}` } })
    listCabang.value = res.data.sort((a, b) => a.nama_cabang.localeCompare(b.nama_cabang))
  } catch (err) {}
}

function getNamaCabang(id_cabang) {
  const c = listCabang.value.find(c => c.id === id_cabang)
  if (c) return c.nama_cabang
  if (currentUser.value.id_cabang === id_cabang && currentUser.value.cabang) {
    return currentUser.value.cabang
  }
  return '—'
}

async function fetchDokumen() {
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get('/api/beranda/dokumen', { headers: { Authorization: `Bearer ${token}` } })
    const ids = res.data.map(d => d.id_spk).filter(Boolean)
    uploadedSpkIds.value = new Set(ids)
  } catch (err) {}
}

onMounted(() => {
  fetchSPK()
  fetchDokumen()
  fetchTemplates()
  fetchCabang()
})

let searchTimeout = null
watch(searchQuery, () => {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    currentPage.value = 1
    fetchSPK()
  }, 400)
})

watch(currentPage, () => fetchSPK())

function formatTanggal(isoString) {
  if (!isoString) return '-'
  const d = new Date(isoString)
  return `${String(d.getDate()).padStart(2,'0')}/${String(d.getMonth()+1).padStart(2,'0')}/${d.getFullYear()}`
}

const sortedData = computed(() => {
  const data = [...spks.value]
  return data.sort((a, b) => {
    switch (sortKey.value) {
      case 'az-asc':   return a.nama_spk.localeCompare(b.nama_spk)
      case 'az-desc':  return b.nama_spk.localeCompare(a.nama_spk)
      case 'tgl-asc':  return new Date(a.tgl_retail) - new Date(b.tgl_retail)
      case 'tgl-desc': return new Date(b.tgl_retail) - new Date(a.tgl_retail)
      default: return 0
    }
  })
})

const paginatedData = computed(() => sortedData.value)

let hideTimeout = null
function handleMouseEnter() { if (hideTimeout) clearTimeout(hideTimeout); showUrutDropdown.value = true }
function handleMouseLeave() { hideTimeout = setTimeout(() => { showUrutDropdown.value = false }, 200) }
function selectSort(value) { sortKey.value = value; showUrutDropdown.value = false; currentPage.value = 1 }

function goToPage(page) { currentPage.value = Math.max(1, Math.min(page, totalPages.value)) }
function onPageInputChange(e) {
  const val = parseInt(e.target.value)
  if (!isNaN(val)) goToPage(val)
  e.target.value = currentPage.value
}

function closeUploadModal() {
  if (isUploading.value) return
  showUploadModal.value = false
  uploadError.value     = ''
  uploadSuccess.value   = ''
  uploadDuplikat.value  = []
  isDragging.value      = false
  uploadProgress.value  = { current: 0, total: 0, percent: 0 }
}

function triggerFileInput() {
  fileInputRef.value?.click()
}

function handleFileInput(e) {
  const file = e.target.files[0]
  if (file) prosesFileXLSX(file)
  e.target.value = ''
}

function handleDrop(e) {
  isDragging.value = false
  const file = e.dataTransfer.files[0]
  if (file) prosesFileXLSX(file)
}

async function prosesFileXLSX(file) {
  uploadError.value   = ''
  uploadSuccess.value = ''
  uploadDuplikat.value = []

  if (!file.name.toLowerCase().endsWith('.xlsx')) {
    uploadError.value = 'File harus berformat XLSX.'
    return
  }

  isUploading.value = true

  const reader = new FileReader()
  reader.onload = async (e) => {
    try {
      const data     = new Uint8Array(e.target.result)
      const workbook = XLSX.read(data, { type: 'array' })
      const sheet    = workbook.Sheets[workbook.SheetNames[0]]
      const rows     = XLSX.utils.sheet_to_json(sheet, { header: 1 })

      const dataRows = rows.slice(1).filter(row =>
        row.length >= 4 && row[0] && row[1] && row[2]
      )

      if (dataRows.length === 0) {
        uploadError.value = 'File kosong atau format tidak sesuai.'
        isUploading.value = false
        return
      }

      const token = localStorage.getItem('token')
      let berhasil = 0
      let gagal    = 0
      const duplikat    = []
      const pesanGagal = []

      uploadProgress.value = { current: 0, total: dataRows.length, percent: 0 }

      for (let i = 0; i < dataRows.length; i++) {
        const row = dataRows[i]

        let tglRetail = ''
        const rawTgl  = row[2]
        if (typeof rawTgl === 'number') {
          const jsDate = new Date(Math.round((rawTgl - 25569) * 86400 * 1000))
          const dd = String(jsDate.getUTCDate()).padStart(2, '0')
          const mm = String(jsDate.getUTCMonth() + 1).padStart(2, '0')
          const yyyy = jsDate.getUTCFullYear()
          tglRetail = `${yyyy}-${mm}-${dd}`
        } else if (typeof rawTgl === 'string') {
          const parts = rawTgl.includes('/')
            ? rawTgl.split('/').reverse().join('-')
            : rawTgl
          tglRetail = parts
        }

        const payload = {
          id:          String(row[0]).trim(),
          nama_spk:    String(row[1]).trim(),
          tgl_retail:  tglRetail,
          id_cabang:   row[3] ? parseInt(row[3]) : null,
          template_id: row[4] ? parseInt(row[4]) : null
        }

        try {
          await axios.post('/api/spk/', payload, {
            headers: { Authorization: `Bearer ${token}` }
          })
          berhasil++
        } catch (err) {
          const detail = err.response?.data?.detail || ''
          if (err.response?.status === 400 && detail.toLowerCase().includes('sudah ada')) {
            duplikat.push(payload.id)
          } else {
            gagal++
            pesanGagal.push(`Baris ${i + 2} (${payload.id}): ${detail}`)
          }
        }

        uploadProgress.value = {
          current: i + 1,
          total:   dataRows.length,
          percent: Math.round(((i + 1) / dataRows.length) * 100)
        }
      }

      if (berhasil > 0) {
        uploadSuccess.value = `${berhasil} SPK berhasil ditambahkan.`
      }
      if (duplikat.length > 0) {
        uploadDuplikat.value = duplikat
      }
      if (gagal > 0) {
        uploadError.value = `${gagal} SPK gagal ditambahkan: ${pesanGagal.join(' | ')}`
      }

      fetchSPK()

    } catch (err) {
      uploadError.value = 'Gagal memproses file XLSX. Pastikan format sesuai.'
    } finally {
      isUploading.value = false
    }
  }

  reader.onerror = () => {
    uploadError.value = 'Gagal membaca file.'
    isUploading.value = false
  }

  reader.readAsArrayBuffer(file)
}

function openAddModal() {
  form.value = { id: '', nama_spk: '', tgl_retail: '', template_id: null, id_cabang: null }
  formError.value = ''
  templateSearch.value = ''
  templateSearchSubmitted.value = false
  showModal.value = true
}

function closeModal() {
  showModal.value = false
}

function closeAktivasiModal() {
  if (isAktivasi.value) return
  showAktivasiModal.value      = false
  aktivasiError.value          = ''
  aktivasiSuccess.value        = ''
  aktivasiTidakDitemukan.value = []
  isAktivasiDragging.value     = false
  aktivasiProgress.value       = { current: 0, total: 0, percent: 0 }
}

function triggerAktivasiFileInput() {
  aktivasiFileInputRef.value?.click()
}

function handleAktivasiFileInput(e) {
  const file = e.target.files[0]
  if (file) prosesAktivasiXLSX(file)
  e.target.value = ''
}

function handleAktivasiDrop(e) {
  isAktivasiDragging.value = false
  const file = e.dataTransfer.files[0]
  if (file) prosesAktivasiXLSX(file)
}

async function prosesAktivasiXLSX(file) {
  aktivasiError.value          = ''
  aktivasiSuccess.value        = ''
  aktivasiTidakDitemukan.value = []

  if (!file.name.toLowerCase().endsWith('.xlsx')) {
    aktivasiError.value = 'File harus berformat XLSX.'
    return
  }

  isAktivasi.value = true

  const reader = new FileReader()
  reader.onload = async (e) => {
    try {
      const data     = new Uint8Array(e.target.result)
      const workbook = XLSX.read(data, { type: 'array' })
      const sheet    = workbook.Sheets[workbook.SheetNames[0]]
      const rows     = XLSX.utils.sheet_to_json(sheet, { header: 1 })

      const dataRows = rows.slice(1).filter(row =>
        row.length >= 4 && row[0] && row[3] !== undefined && row[3] !== ''
      )

      if (dataRows.length === 0) {
        aktivasiError.value = 'File kosong atau format tidak sesuai.'
        isAktivasi.value    = false
        return
      }

      const token          = localStorage.getItem('token')
      let berhasil         = 0
      let gagal            = 0
      const tidakDitemukan = []
      const pesanGagal     = []

      aktivasiProgress.value = { current: 0, total: dataRows.length, percent: 0 }

      for (let i = 0; i < dataRows.length; i++) {
        const row      = dataRows[i]
        const nomorSPK = String(row[0]).trim()

        const statusBaru = String(row[3]).trim() === '1' ? 'Aktif' : 'Nonaktif'

        try {
          await axios.patch(`/api/spk/${nomorSPK}/status`, { status: statusBaru }, {
            headers: { Authorization: `Bearer ${token}` }
          })
          berhasil++
        } catch (err) {
          if (err.response?.status === 404) {
            tidakDitemukan.push(nomorSPK)
          } else {
            gagal++
            const detail = err.response?.data?.detail || 'Error tidak diketahui'
            pesanGagal.push(`Baris ${i + 2} (${nomorSPK}): ${detail}`)
          }
        }

        aktivasiProgress.value = {
          current: i + 1,
          total:   dataRows.length,
          percent: Math.round(((i + 1) / dataRows.length) * 100)
        }
      }

      if (berhasil > 0) {
        aktivasiSuccess.value = `${berhasil} SPK berhasil diperbarui statusnya.`
      }
      if (tidakDitemukan.length > 0) {
        aktivasiTidakDitemukan.value = tidakDitemukan
      }
      if (gagal > 0) {
        aktivasiError.value = `${gagal} SPK gagal diproses: ${pesanGagal.join(' | ')}`
      }

      fetchSPK()

    } catch (err) {
      aktivasiError.value = 'Gagal memproses file XLSX. Pastikan format sesuai.'
    } finally {
      isAktivasi.value = false
    }
  }

  reader.onerror = () => {
    aktivasiError.value = 'Gagal membaca file.'
    isAktivasi.value    = false
  }

  reader.readAsArrayBuffer(file)
}

async function handleSimpan() {
  if (!form.value.id || !form.value.nama_spk || !form.value.tgl_retail) return
  saving.value = true
  formError.value = ''
  try {
    const token = localStorage.getItem('token')
    await axios.post('/api/spk/', form.value, { headers: { Authorization: `Bearer ${token}` } })
    closeModal()
    fetchSPK()
  } catch (err) {
    formError.value = err.response?.data?.detail || 'Gagal menyimpan SPK'
  } finally {
    saving.value = false
  }
}
</script>
