<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-gray-800">Leçons</h1>

    <div v-if="loading" class="text-center text-gray-400 py-12">Chargement des leçons...</div>
    <div v-if="error" class="rounded-lg bg-red-50 p-4 text-red-700 text-sm">{{ error }}</div>

    <div v-if="!loading && !error && Object.keys(grouped).length === 0" class="text-center py-12">
      <p class="text-gray-400">Aucune leçon disponible.</p>
      <router-link to="/plan" class="mt-3 inline-block text-sm text-primary hover:underline">
        Créer un plan d'entraînement
      </router-link>
    </div>

    <!-- Grouped by block_name -->
    <div v-for="(lessons, block) in grouped" :key="block" class="space-y-3">
      <h2 class="text-lg font-semibold text-gray-700">{{ block }}</h2>
      <div class="space-y-2">
        <router-link
          v-for="lesson in lessons"
          :key="lesson.id || lesson.number"
          :to="`/practice/${lesson.id || lesson.number}`"
          class="flex items-center justify-between rounded-xl border border-gray-200 bg-white px-5 py-4 shadow-sm transition hover:shadow-md hover:border-primary"
        >
          <div class="min-w-0">
            <div class="text-sm font-medium text-gray-800 truncate">
              <span class="text-gray-400 mr-1">{{ lesson.number }}.</span>
              {{ lesson.title || `Leçon ${lesson.number}` }}
            </div>
            <div v-if="lesson.grammar_focus" class="text-xs text-gray-400 mt-0.5">{{ lesson.grammar_focus }}</div>
          </div>
          <div class="flex items-center gap-2 shrink-0 ml-4">
            <span
              v-if="lesson.is_priority"
              class="inline-flex items-center rounded-full bg-amber-100 px-2 py-0.5 text-xs font-medium text-amber-700"
            >
              Priorité
            </span>
            <span
              v-if="lesson.has_content"
              class="inline-flex items-center rounded-full bg-blue-100 px-2 py-0.5 text-xs font-medium text-primary"
            >
              Contenu
            </span>
            <span
              v-if="lesson.status === 'completed'"
              class="inline-flex items-center rounded-full bg-green-100 px-2 py-0.5 text-xs font-medium text-green-700"
            >
              Terminé
            </span>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
            </svg>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useApi } from '../composables/useApi'

const { get } = useApi()

const lessons = ref([])
const loading = ref(false)
const error = ref(null)

const grouped = computed(() => {
  const groups = {}
  for (const lesson of lessons.value) {
    const block = lesson.block_name || `Bloc ${lesson.block}` || 'Sans bloc'
    if (!groups[block]) groups[block] = []
    groups[block].push(lesson)
  }
  return groups
})

onMounted(async () => {
  loading.value = true
  try {
    const data = await get('/plan/lessons')
    lessons.value = Array.isArray(data) ? data : []
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
})
</script>
