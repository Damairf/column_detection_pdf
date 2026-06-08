<template>
  <AppLayout>
    <div class="flex flex-col min-h-full">
      <div class="flex flex-col gap-2 mb-4">

        <!-- Cari (kiri) + Ekspor + Urut + Pilih Data (kanan) -->
        <div class="flex items-center justify-between">
          <div class="relative mb-1.5">
            <span class="absolute inset-y-0 left-3 flex items-center text-gray-400 pointer-events-none">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35m0 0A7.5 7.5 0 1010.5 18a7.5 7.5 0 006.15-3.35z" />
              </svg>
            </span>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Cari...."
              class="pl-9 pr-4 py-2 w-64 border border-gray-300 rounded-lg text-sm text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent bg-white shadow-sm"
            />
          </div>

          <div class="flex items-center gap-2">
            <!-- Ekspor -->
            <button
              @click="handleEkspor"
              :disabled="isExporting"
              class="cursor-pointer flex items-center gap-1.5 px-4 py-2 border border-gray-300 bg-white text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-50 transition shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <svg v-if="isExporting" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              {{ isExporting ? 'Mengekspor...' : 'Ekspor' }}
            </button>

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

            <!-- Pilih Data -->
            <button
              @click="openPilihDataModal"
              class="flex items-center gap-1.5 px-4 py-2 border border-gray-300 bg-white text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-50 transition shadow-sm cursor-pointer"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2a1 1 0 01-.293.707L13 13.414V19a1 1 0 01-.553.894l-4 2A1 1 0 017 21v-7.586L3.293 6.707A1 1 0 013 6V4z" />
              </svg>
              Pilih Data
            </button>
          </div>
        </div>

        <!-- Tag filter aktif -->
        <div v-if="appliedSPK || appliedCabangIds.length > 0" class="flex flex-wrap items-center gap-2">
          <span v-if="appliedSPK" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-gray-900 text-white text-sm font-medium rounded-lg shadow-sm">
            SPK: {{ appliedSPK.nama_spk }}
          </span>
          <span
            v-for="c in appliedCabangList"
            :key="c.id"
            class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border border-gray-300 text-gray-700 text-sm font-medium rounded-lg shadow-sm"
          >
            {{ c.nama_cabang }}
          </span>
        </div>

      </div>

      <!-- Tabel -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b border-gray-200">
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700 w-28">ID</th>
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700">Nama Dokumen</th>
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700">Pengunggah</th>
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700">Cabang</th>
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700">Nomor SPK</th>
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700">Nama SPK</th>
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700 w-32">Tanggal</th>
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700">Kriteria</th>
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700">Benar</th>
                <th class="px-5 py-3.5 text-center font-semibold text-gray-700">Skor</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading">
                <td colspan="10" class="px-5 py-10 text-center text-gray-400 text-sm">
                  <div class="flex items-center justify-center gap-2">
                    <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                    </svg>
                    Memuat data...
                  </div>
                </td>
              </tr>

              <tr v-else-if="errorMsg">
                <td colspan="10" class="px-5 py-10 text-center text-red-400 text-sm">{{ errorMsg }}</td>
              </tr>

              <tr
                v-else
                v-for="row in paginatedData"
                :key="row.id"
                class="border-b border-gray-100 hover:bg-gray-50 transition-colors"
              >
                <td class="px-5 py-3 text-center text-gray-700 font-mono text-sm">{{ formatId(row.id) }}</td>
                <td class="px-5 py-3 text-center text-gray-700">{{ row.nama_dokumen }}</td>
                <td class="px-5 py-3 text-center text-gray-700">{{ row.pengunggah || '—' }}</td>
                <td class="px-5 py-3 text-center text-gray-700">{{ row.cabang || '—' }}</td>
                <td class="px-5 py-3 text-center text-gray-700">{{ row.nomor_spk || '—' }}</td>
                <td class="px-5 py-3 text-center text-gray-700">{{ row.nama_spk || '—' }}</td>
                <td class="px-5 py-3 text-center text-gray-500">{{ formatTanggal(row.tgl_retail) }}</td>
                <td class="px-5 py-3 text-center text-gray-700 font-medium">{{ row.kriteria }}</td>
                <td class="px-5 py-3 text-center text-gray-700 font-medium">{{ row.jml_benar }}/{{ row.kriteria }}</td>
                <td class="px-5 py-3 text-center font-medium text-blue-500">{{ row.skor }}%</td>
              </tr>

              <tr v-if="!loading && !errorMsg && paginatedData.length === 0">
                <td colspan="10" class="px-5 py-10 text-center text-gray-400 text-sm">
                  {{ appliedCabangIds.length === 0 && !appliedSPK
                    ? 'Pilih data terlebih dahulu.'
                    : 'Tidak ada data ditemukan.' }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div class="flex items-center justify-center gap-2 py-5 border-t border-gray-100">
          <button
            @click="goToPage(1)" :disabled="currentPage === 1"
            class="w-9 h-9 flex items-center justify-center rounded-lg font-bold transition"
            :class="currentPage === 1 ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-gray-900 text-white hover:bg-gray-700 cursor-pointer'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M11 19l-7-7 7-7M19 19l-7-7 7-7" />
            </svg>
          </button>
          <button
            @click="goToPage(currentPage - 1)" :disabled="currentPage === 1"
            class="w-9 h-9 flex items-center justify-center rounded-lg font-bold transition"
            :class="currentPage === 1 ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-gray-900 text-white hover:bg-gray-700 cursor-pointer'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <input
            type="number" :value="currentPage"
            @change="onPageInputChange" @keydown.enter="onPageInputChange"
            min="1" :max="totalPages"
            class="w-12 h-9 text-center border border-gray-300 rounded-lg text-sm font-medium text-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
          />
          <button
            @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages || totalPages === 0"
            class="w-9 h-9 flex items-center justify-center rounded-lg font-bold transition"
            :class="currentPage === totalPages || totalPages === 0 ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-gray-900 text-white hover:bg-gray-700 cursor-pointer'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7" />
            </svg>
          </button>
          <button
            @click="goToPage(totalPages)" :disabled="currentPage === totalPages || totalPages === 0"
            class="w-9 h-9 flex items-center justify-center rounded-lg font-bold transition"
            :class="currentPage === totalPages || totalPages === 0 ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-gray-900 text-white hover:bg-gray-700 cursor-pointer'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 5l7 7-7 7M5 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Footer Warning -->
      <div class="mt-auto pt-6 text-xs text-gray-400 text-center border-t border-gray-100">
        Sistem ini bisa melakukan kesalahan. Silahkan periksa kembali hasilnya
      </div>
    </div>

    <!-- Modal Pilih Data -->
    <div
      v-if="showPilihDataModal"
      @click.self="closePilihDataModal"
      class="fixed inset-0 z-50 flex items-center justify-center"
      style="background: rgba(0,0,0,0.35);"
    >
      <div class="relative bg-white rounded-2xl shadow-2xl w-full mx-6 p-7" style="max-width: 1000px;">
        <h2 class="text-xl font-bold text-gray-800 mb-6">Pilih Data</h2>

        <div class="grid gap-6" style="grid-template-columns: 3fr 7fr;">

          <!-- Kolom Cabang -->
          <div class="flex flex-col">
            <div class="flex items-center gap-2 mb-3">
              <h3 class="text-sm font-semibold text-gray-700">Pilih Cabang</h3>
              <span v-if="errorCabangModal" class="text-xs text-red-500 font-medium">Cabang harus dipilih</span>
            </div>

            <!-- Search cabang -->
            <div class="relative mb-3">
              <span class="absolute inset-y-0 left-3 flex items-center text-gray-400 pointer-events-none">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35m0 0A7.5 7.5 0 1010.5 18a7.5 7.5 0 006.15-3.35z" />
                </svg>
              </span>
              <input
                v-model="searchCabangModal"
                type="text"
                placeholder="Cari cabang...."
                class="pl-9 pr-4 py-2 w-full border border-gray-300 rounded-lg text-sm text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent bg-white shadow-sm"
              />
            </div>

            <!-- Tabel Cabang -->
            <div class="border border-gray-200 rounded-xl overflow-hidden shadow-sm">
              <table class="w-full text-sm">
                <thead>
                  <tr class="border-b border-gray-200 bg-gray-50">
                    <th class="px-4 py-3 text-center font-semibold text-gray-700 w-12">
                      <input
                        type="checkbox"
                        :checked="modalSemuaCabangTerpilih"
                        :indeterminate.prop="modalSebagianCabangTerpilih"
                        @change="toggleModalPilihSemuaCabang"
                        class="w-4 h-4 accent-gray-900 cursor-pointer"
                      />
                    </th>
                    <th class="px-4 py-3 text-center font-semibold text-gray-700">Nama Cabang</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="loadingCabang">
                    <td colspan="2" class="px-4 py-6 text-center text-gray-400 text-sm">Memuat cabang...</td>
                  </tr>
                  <tr v-else-if="filteredCabangModal.length === 0">
                    <td colspan="2" class="px-4 py-6 text-center text-gray-400 text-sm">Tidak ditemukan.</td>
                  </tr>
                  <tr
                    v-else
                    v-for="c in paginatedCabangModal"
                    :key="c.id"
                    class="border-b border-gray-100 hover:bg-gray-50 transition-colors cursor-pointer"
                    @click="toggleCabangModal(c.id)"
                  >
                    <td class="px-4 py-3 text-center">
                      <input
                        type="checkbox"
                        :value="c.id"
                        :checked="modalCabangIds.includes(c.id)"
                        @click.stop
                        @change="toggleCabangModal(c.id)"
                        class="w-4 h-4 accent-gray-900 cursor-pointer"
                      />
                    </td>
                    <td class="px-4 py-3 text-center text-gray-700">{{ c.nama_cabang }}</td>
                  </tr>
                </tbody>
              </table>

              <!-- Pagination Cabang -->
              <div class="flex items-center justify-center gap-2 py-3 border-t border-gray-100">
                <button
                  @click="cabangModalPage = Math.max(1, cabangModalPage - 1)"
                  :disabled="cabangModalPage === 1"
                  class="w-7 h-7 flex items-center justify-center rounded-lg transition text-xs font-bold"
                  :class="cabangModalPage === 1 ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-gray-900 text-white hover:bg-gray-700 cursor-pointer'"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7" />
                  </svg>
                </button>
                <span class="text-xs text-gray-500">{{ cabangModalPage }} / {{ totalCabangModalPages }}</span>
                <button
                  @click="cabangModalPage = Math.min(totalCabangModalPages, cabangModalPage + 1)"
                  :disabled="cabangModalPage === totalCabangModalPages || totalCabangModalPages === 0"
                  class="w-7 h-7 flex items-center justify-center rounded-lg transition text-xs font-bold"
                  :class="cabangModalPage === totalCabangModalPages || totalCabangModalPages === 0 ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-gray-900 text-white hover:bg-gray-700 cursor-pointer'"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Kolom SPK -->
          <div class="flex flex-col">
            <div class="flex items-center gap-2 mb-3">
              <h3 class="text-sm font-semibold text-gray-700">Pilih SPK</h3>
              <span v-if="errorSPKModal" class="text-xs text-red-500 font-medium">SPK harus dipilih</span>
            </div>

            <!-- Search SPK -->
            <div class="relative mb-3">
              <span class="absolute inset-y-0 left-3 flex items-center text-gray-400 pointer-events-none">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35m0 0A7.5 7.5 0 1010.5 18a7.5 7.5 0 006.15-3.35z" />
                </svg>
              </span>
              <input
                v-model="searchSPKModal"
                type="text"
                placeholder="Cari SPK...."
                class="pl-9 pr-4 py-2 w-full border border-gray-300 rounded-lg text-sm text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent bg-white shadow-sm"
              />
            </div>

            <!-- Tabel SPK -->
            <div class="border border-gray-200 rounded-xl overflow-hidden shadow-sm">
              <table class="w-full text-sm">
                <thead>
                  <tr class="border-b border-gray-200 bg-gray-50">
                    <th class="px-4 py-3 text-center font-semibold text-gray-700 w-10"></th>
                    <th class="px-4 py-3 text-center font-semibold text-gray-700 w-32">Nomor SPK</th>
                    <th class="px-4 py-3 text-center font-semibold text-gray-700">Nama SPK</th>
                    <th class="px-4 py-3 text-center font-semibold text-gray-700 w-32">Tanggal Retail</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="loadingSPK">
                    <td colspan="4" class="px-4 py-6 text-center text-gray-400 text-sm">Memuat SPK...</td>
                  </tr>
                  <tr v-else-if="filteredSPKModal.length === 0">
                    <td colspan="4" class="px-4 py-6 text-center text-gray-400 text-sm">Tidak ditemukan.</td>
                  </tr>
                  <tr
                    v-else
                    v-for="s in paginatedSPKModal"
                    :key="s.id"
                    @click="modalSelectedSPK = modalSelectedSPK?.id === s.id ? null : s"
                    class="border-b border-gray-100 hover:bg-gray-50 transition-colors cursor-pointer"
                  >
                    <td class="px-4 py-3 text-center">
                      <input
                        type="radio"
                        :checked="modalSelectedSPK?.id === s.id"
                        @click.stop="modalSelectedSPK = modalSelectedSPK?.id === s.id ? null : s"
                        class="w-4 h-4 accent-gray-900 cursor-pointer"
                      />
                    </td>
                    <td class="px-4 py-3 text-center font-medium text-gray-700">{{ s.id }}</td>
                    <td class="px-4 py-3 text-center text-gray-700">{{ s.nama_spk }}</td>
                    <td class="px-4 py-3 text-center text-gray-500">{{ formatTanggal(s.tgl_retail) }}</td>
                  </tr>
                </tbody>
              </table>

              <!-- Pagination SPK -->
              <div class="flex items-center justify-center gap-2 py-3 border-t border-gray-100">
                <button
                  @click="spkModalPage = Math.max(1, spkModalPage - 1)"
                  :disabled="spkModalPage === 1"
                  class="w-7 h-7 flex items-center justify-center rounded-lg transition text-xs font-bold"
                  :class="spkModalPage === 1 ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-gray-900 text-white hover:bg-gray-700 cursor-pointer'"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7" />
                  </svg>
                </button>
                <span class="text-xs text-gray-500">{{ spkModalPage }} / {{ totalSPKModalPages }}</span>
                <button
                  @click="spkModalPage = Math.min(totalSPKModalPages, spkModalPage + 1)"
                  :disabled="spkModalPage === totalSPKModalPages || totalSPKModalPages === 0"
                  class="w-7 h-7 flex items-center justify-center rounded-lg transition text-xs font-bold"
                  :class="spkModalPage === totalSPKModalPages || totalSPKModalPages === 0 ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-gray-900 text-white hover:bg-gray-700 cursor-pointer'"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

        </div>

        <!-- Tombol Batal, Reset & Simpan -->
        <div class="mt-7 flex justify-end gap-3">
          <button
            @click="closePilihDataModal"
            class="px-5 py-2 text-sm font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition cursor-pointer"
          >
            Batal
          </button>
          <button
            @click="resetPilihData"
            class="px-5 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700 transition cursor-pointer"
          >
            Reset
          </button>
          <button
            @click="simpanPilihData"
            class="px-5 py-2 text-sm font-medium text-white bg-gray-900 rounded-lg hover:bg-gray-800 transition cursor-pointer"
          >
            Simpan
          </button>
        </div>

      </div>
    </div>

  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import axios from 'axios'
import AppLayout from '../components/AppLayout.vue'

const items    = ref([])
const loading  = ref(false)
const errorMsg = ref('')
const errorCabangModal = ref(false)
const errorSPKModal    = ref(false)

const appliedCabangIds = ref([])
const appliedSPK       = ref(null)

const appliedCabangList = computed(() =>
  listCabang.value.filter(c => appliedCabangIds.value.includes(c.id))
)

const searchQuery      = ref('')
const currentPage      = ref(1)
const itemsPerPage     = 10
const showUrutDropdown = ref(false)
const sortKey          = ref('id-desc')
const isExporting      = ref(false)

const sortOptions = [
  { label: 'A - Z (Menurun)',   value: 'az-desc'  },
  { label: 'A - Z (Menaik)',    value: 'az-asc'   },
  { label: 'ID (Menurun)',      value: 'id-desc'  },
  { label: 'ID (Menaik)',       value: 'id-asc'   },
  { label: 'Tanggal (Menurun)', value: 'tgl-desc' },
  { label: 'Tanggal (Menaik)',  value: 'tgl-asc'  },
]

let hideTimeout = null
function handleMouseEnter() {
  if (hideTimeout) { clearTimeout(hideTimeout); hideTimeout = null }
  showUrutDropdown.value = true
}
function handleMouseLeave() {
  hideTimeout = setTimeout(() => { showUrutDropdown.value = false }, 150)
}
function selectSort(value) {
  sortKey.value = sortKey.value === value ? '' : value
  showUrutDropdown.value = false
  currentPage.value = 1
}

const showPilihDataModal = ref(false)
const modalCabangIds   = ref([])
const modalSelectedSPK = ref(null)
const searchCabangModal = ref('')
const searchSPKModal    = ref('')

const cabangModalPage = ref(1)
const spkModalPage    = ref(1)
const modalItemsPerPage = 5

function openPilihDataModal() {
  modalCabangIds.value    = [...appliedCabangIds.value]
  modalSelectedSPK.value  = appliedSPK.value ? { ...appliedSPK.value } : null
  searchCabangModal.value = ''
  searchSPKModal.value    = ''
  cabangModalPage.value   = 1
  spkModalPage.value      = 1
  errorCabangModal.value  = false
  errorSPKModal.value     = false
  fetchCabang()
  fetchSPK()
  showPilihDataModal.value = true
}

function closePilihDataModal() {
  showPilihDataModal.value = false
}

function simpanPilihData() {
  const adaCabang = modalCabangIds.value.length > 0
  const adaSPK    = !!modalSelectedSPK.value

  if (!adaCabang && !adaSPK) {
    appliedCabangIds.value   = []
    appliedSPK.value         = null
    showPilihDataModal.value = false
    currentPage.value        = 1
    fetchEvaluasi()
    return
  }

  errorCabangModal.value = !adaCabang
  errorSPKModal.value    = !adaSPK

  if (!adaCabang || !adaSPK) return
  errorCabangModal.value   = false
  errorSPKModal.value      = false
  appliedCabangIds.value   = [...modalCabangIds.value]
  appliedSPK.value         = { ...modalSelectedSPK.value }
  showPilihDataModal.value = false
  currentPage.value        = 1
  fetchEvaluasi()
}

const listCabang    = ref([])
const listSPK       = ref([])
const loadingCabang = ref(false)
const loadingSPK    = ref(false)

async function fetchCabang() {
  if (listCabang.value.length > 0) return
  loadingCabang.value = true
  try {
    const token = localStorage.getItem('token')
    const res   = await axios.get('/api/pengguna/cabang', { headers: { Authorization: `Bearer ${token}` } })
    listCabang.value = res.data
  } catch (err) {
    console.error('Gagal memuat cabang:', err)
  } finally {
    loadingCabang.value = false
  }
}

async function fetchSPK() {
  if (listSPK.value.length > 0) return
  loadingSPK.value = true
  try {
    const token = localStorage.getItem('token')
    const res   = await axios.get('/api/spk/', { headers: { Authorization: `Bearer ${token}` } })
    listSPK.value = res.data
  } catch (err) {
    console.error('Gagal memuat SPK:', err)
  } finally {
    loadingSPK.value = false
  }
}

const filteredCabangModal = computed(() => {
  const q = searchCabangModal.value.toLowerCase().trim()
  if (!q) return listCabang.value
  return listCabang.value.filter(c => c.nama_cabang.toLowerCase().includes(q))
})

const totalCabangModalPages = computed(() =>
  Math.ceil(filteredCabangModal.value.length / modalItemsPerPage) || 1
)
const paginatedCabangModal = computed(() => {
  const start = (cabangModalPage.value - 1) * modalItemsPerPage
  return filteredCabangModal.value.slice(start, start + modalItemsPerPage)
})

const modalSemuaCabangTerpilih = computed(() =>
  filteredCabangModal.value.length > 0 &&
  filteredCabangModal.value.every(c => modalCabangIds.value.includes(c.id))
)
const modalSebagianCabangTerpilih = computed(() =>
  filteredCabangModal.value.some(c => modalCabangIds.value.includes(c.id)) &&
  !modalSemuaCabangTerpilih.value
)

function toggleCabangModal(id) {
  const idx = modalCabangIds.value.indexOf(id)
  if (idx === -1) modalCabangIds.value.push(id)
  else modalCabangIds.value.splice(idx, 1)
}

function toggleModalPilihSemuaCabang() {
  if (modalSemuaCabangTerpilih.value) {
    const filteredIds = filteredCabangModal.value.map(c => c.id)
    modalCabangIds.value = modalCabangIds.value.filter(id => !filteredIds.includes(id))
  } else {
    const filteredIds = filteredCabangModal.value.map(c => c.id)
    const merged = new Set([...modalCabangIds.value, ...filteredIds])
    modalCabangIds.value = [...merged]
  }
}

watch(searchCabangModal, () => { cabangModalPage.value = 1 })

const filteredSPKModal = computed(() => {
  const q = searchSPKModal.value.toLowerCase().trim()
  if (!q) return listSPK.value
  return listSPK.value.filter(s =>
    s.id.toLowerCase().includes(q) ||
    s.nama_spk.toLowerCase().includes(q)
  )
})

const totalSPKModalPages = computed(() =>
  Math.ceil(filteredSPKModal.value.length / modalItemsPerPage) || 1
)
const paginatedSPKModal = computed(() => {
  const start = (spkModalPage.value - 1) * modalItemsPerPage
  return filteredSPKModal.value.slice(start, start + modalItemsPerPage)
})

watch(searchSPKModal, () => { spkModalPage.value = 1 })

async function fetchEvaluasi() {
  if (appliedCabangIds.value.length === 0 && !appliedSPK.value) {
    items.value = []
    return
  }

  loading.value  = true
  errorMsg.value = ''
  try {
    const token    = localStorage.getItem('token')
    const spkParam = appliedSPK.value ? `?id_spk=${appliedSPK.value.id}` : ''
    const res      = await axios.get(`/api/evaluasi/${spkParam}`, { headers: { Authorization: `Bearer ${token}` } })
    items.value    = res.data
  } catch (err) {
    errorMsg.value = err.response?.status === 403
      ? 'Akses ditolak.'
      : 'Gagal memuat data evaluasi.'
  } finally {
    loading.value = false
  }
}

const filteredData = computed(() => {
  let data = items.value

  if (appliedCabangIds.value.length > 0) {
    const namaCabangSet = new Set(
      listCabang.value
        .filter(c => appliedCabangIds.value.includes(c.id))
        .map(c => c.nama_cabang)
    )
    data = data.filter(row => namaCabangSet.has(row.cabang))
  }

  const q = searchQuery.value.toLowerCase().trim()
  if (q) {
    data = data.filter(row =>
      formatId(row.id).toLowerCase().includes(q)        ||
      (row.nama_dokumen || '').toLowerCase().includes(q) ||
      (row.pengunggah   || '').toLowerCase().includes(q) ||
      (row.cabang       || '').toLowerCase().includes(q) ||
      (row.nomor_spk    || '').toLowerCase().includes(q) ||
      (row.nama_spk     || '').toLowerCase().includes(q) ||
      formatTanggal(row.tgl_retail).includes(q)
    )
  }

  return data
})

const sortedData = computed(() => {
  const data = [...filteredData.value]
  switch (sortKey.value) {
    case 'az-asc':   return data.sort((a, b) => (a.nama_dokumen || '').localeCompare(b.nama_dokumen || ''))
    case 'az-desc':  return data.sort((a, b) => (b.nama_dokumen || '').localeCompare(a.nama_dokumen || ''))
    case 'id-asc':   return data.sort((a, b) => a.id - b.id)
    case 'id-desc':  return data.sort((a, b) => b.id - a.id)
    case 'tgl-asc':  return data.sort((a, b) => new Date(a.tgl_retail) - new Date(b.tgl_retail))
    case 'tgl-desc': return data.sort((a, b) => new Date(b.tgl_retail) - new Date(a.tgl_retail))
    default:         return data
  }
})

const totalPages    = computed(() => Math.ceil(sortedData.value.length / itemsPerPage) || 1)
const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return sortedData.value.slice(start, start + itemsPerPage)
})

function goToPage(page) {
  currentPage.value = Math.max(1, Math.min(page, totalPages.value))
}
function onPageInputChange(e) {
  const val = parseInt(e.target.value)
  if (!isNaN(val)) goToPage(val)
  e.target.value = currentPage.value
}

function resetPilihData() {
  modalCabangIds.value   = []
  modalSelectedSPK.value = null
  errorCabangModal.value = false
  errorSPKModal.value    = false
}

async function handleEkspor() {
  if (appliedCabangIds.value.length === 0) {
    alert('Pilih data terlebih dahulu.')
    return
  }
  isExporting.value = true
  try {
    const token  = localStorage.getItem('token')
    const params = new URLSearchParams()
    appliedCabangIds.value.forEach(id => params.append('cabang_ids', id))
    if (appliedSPK.value) params.append('id_spk', appliedSPK.value.id)

    const res = await axios.get(`/api/evaluasi/ekspor?${params.toString()}`, {
      headers: { Authorization: `Bearer ${token}` },
      responseType: 'blob'
    })

    const url  = window.URL.createObjectURL(new Blob([res.data]))
    const link = document.createElement('a')
    link.href  = url

    const now  = new Date()
    const dd   = String(now.getDate()).padStart(2, '0')
    const mm   = String(now.getMonth() + 1).padStart(2, '0')
    const yyyy = now.getFullYear()
    let filename = `Evaluasi_Dokumen_${dd}-${mm}-${yyyy}.xlsx`

    const disposition = res.headers['content-disposition']
    if (disposition?.includes('filename=')) {
      const match = disposition.match(/filename="?([^"]+)"?/)
      if (match?.[1]) filename = match[1]
    }

    link.setAttribute('download', filename)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } catch (err) {
    console.error('Gagal mengekspor data:', err)
    alert('Gagal mengekspor data. Coba lagi.')
  } finally {
    isExporting.value = false
  }
}

function formatId(id) {
  return id ? `D-${String(id).padStart(6, '0')}` : '—'
}
function formatTanggal(isoString) {
  if (!isoString) return '—'
  const d = new Date(isoString)
  return `${String(d.getDate()).padStart(2,'0')}/${String(d.getMonth()+1).padStart(2,'0')}/${d.getFullYear()}`
}

watch(searchQuery, () => { currentPage.value = 1 })

onMounted(() => {
  fetchCabang()
  fetchSPK()
})

onBeforeUnmount(() => {
  if (hideTimeout) clearTimeout(hideTimeout)
})
</script>