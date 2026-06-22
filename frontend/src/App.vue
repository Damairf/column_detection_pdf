<script setup>
import ToastContainer from './components/ToastContainer.vue'
import { useToast } from './composables/useToast'

const { toasts, removeToast } = useToast()
</script>

<template>
  <ToastContainer :toasts="toasts" @remove="removeToast" />
  <router-view />
</template>

<style scoped></style>