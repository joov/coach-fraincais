<template>
  <div class="space-y-8">
    <!-- Greeting -->
    <div class="text-center">
      <h1 class="text-3xl font-bold text-gray-800">
        Bonjour{{ userName ? ` ${userName}` : '' }} !
      </h1>
      <p class="mt-2 text-lg text-gray-500">Que voulez-vous faire aujourd'hui ?</p>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center text-gray-400">Chargement...</div>

    <!-- Error -->
    <div v-if="error" class="rounded-lg bg-red-50 p-4 text-red-700 text-sm">{{ error }}</div>

    <!-- Cards -->
    <div class="grid gap-6 sm:grid-cols-3">
      <router-link
        to="/plan"
        class="group block rounded-2xl border border-gray-200 bg-white p-8 text-center shadow-sm transition hover:shadow-lg hover:border-primary"
      >
        <div class="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-blue-100 text-primary text-2xl group-hover:bg-primary group-hover:text-white transition">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 012-2h2a2 2 0 012 2M9 5h6" />
          </svg>
        </div>
        <h2 class="text-lg font-semibold text-gray-800 group-hover:text-primary transition">Plan d'entraînement</h2>
        <p class="mt-1 text-sm text-gray-500">Configurez votre programme personnalisé</p>
      </router-link>

      <router-link
        to="/practice"
        class="group block rounded-2xl border border-gray-200 bg-white p-8 text-center shadow-sm transition hover:shadow-lg hover:border-primary"
      >
        <div class="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-blue-100 text-primary text-2xl group-hover:bg-primary group-hover:text-white transition">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.536 8.464a5 5 0 010 7.072M12 6.253v11.494M8.464 8.464a5 5 0 000 7.072M19.07 4.93a9 9 0 010 12.728M4.93 4.93a9 9 0 000 12.728" />
          </svg>
        </div>
        <h2 class="text-lg font-semibold text-gray-800 group-hover:text-primary transition">Pratiquer</h2>
        <p class="mt-1 text-sm text-gray-500">Suivez vos leçons de français</p>
      </router-link>

      <router-link
        to="/progress"
        class="group block rounded-2xl border border-gray-200 bg-white p-8 text-center shadow-sm transition hover:shadow-lg hover:border-primary"
      >
        <div class="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-blue-100 text-primary text-2xl group-hover:bg-primary group-hover:text-white transition">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6m6 0h6m-6 0V9a2 2 0 012-2h2a2 2 0 012 2v10m6 0v-4a2 2 0 00-2-2h-2a2 2 0 00-2 2v4" />
          </svg>
        </div>
        <h2 class="text-lg font-semibold text-gray-800 group-hover:text-primary transition">Progrès</h2>
        <p class="mt-1 text-sm text-gray-500">Suivez votre progression</p>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '../composables/useApi'
import { useUserStore } from '../stores/user'

const { get } = useApi()
const userStore = useUserStore()

const userName = ref('')
const loading = ref(false)
const error = ref(null)

onMounted(async () => {
  loading.value = true
  try {
    const settings = await get('/settings')
    userName.value = settings.name || ''
    userStore.name = settings.name || ''
    userStore.currentLevel = settings.current_level || ''
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
})
</script>
