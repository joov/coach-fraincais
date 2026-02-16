<template>
  <div class="space-y-8">
    <h1 class="text-2xl font-bold text-gray-800">Progrès</h1>

    <div v-if="loading" class="text-center text-gray-400 py-12">Chargement...</div>
    <div v-if="error" class="rounded-lg bg-red-50 p-4 text-red-700 text-sm">{{ error }}</div>

    <template v-if="!loading && !error && progress">
      <!-- Summary cards -->
      <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <!-- Accuracy -->
        <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
          <p class="text-xs font-medium text-gray-400 uppercase tracking-wide">Précision globale</p>
          <p class="mt-2 text-3xl font-bold text-primary">{{ progress.accuracy ?? 0 }}%</p>
        </div>

        <!-- Completed lessons -->
        <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
          <p class="text-xs font-medium text-gray-400 uppercase tracking-wide">Leçons terminées</p>
          <p class="mt-2 text-3xl font-bold text-gray-800">{{ progress.completed_lessons ?? 0 }}</p>
        </div>

        <!-- Total exercises -->
        <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
          <p class="text-xs font-medium text-gray-400 uppercase tracking-wide">Exercices complétés</p>
          <p class="mt-2 text-3xl font-bold text-gray-800">{{ progress.total_exercises ?? 0 }}</p>
        </div>

        <!-- Current streak -->
        <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
          <p class="text-xs font-medium text-gray-400 uppercase tracking-wide">Série en cours</p>
          <p class="mt-2 text-3xl font-bold text-accent">{{ progress.streak ?? 0 }} j</p>
        </div>
      </div>

      <!-- Level assessment -->
      <div v-if="level" class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
        <h2 class="text-lg font-semibold text-gray-700 mb-4">Estimation du niveau</h2>
        <div class="flex items-center gap-6">
          <div class="text-center">
            <p class="text-4xl font-bold text-primary">{{ level.estimated_level || '?' }}</p>
            <p class="text-xs text-gray-400 mt-1">Niveau estimé</p>
          </div>
          <div class="flex-1 space-y-3">
            <div v-for="skill in levelSkills" :key="skill.name">
              <div class="flex items-center justify-between text-sm mb-1">
                <span class="text-gray-600">{{ skill.name }}</span>
                <span class="font-medium text-gray-800">{{ skill.score }}%</span>
              </div>
              <div class="h-2 rounded-full bg-gray-100 overflow-hidden">
                <div
                  class="h-full rounded-full transition-all duration-500"
                  :class="skill.score >= 70 ? 'bg-green-500' : skill.score >= 40 ? 'bg-yellow-500' : 'bg-red-400'"
                  :style="{ width: `${skill.score}%` }"
                ></div>
              </div>
            </div>
          </div>
        </div>
        <p v-if="level.summary" class="mt-4 text-sm text-gray-500">{{ level.summary }}</p>
      </div>

      <!-- Error breakdown -->
      <div v-if="progress.error_breakdown && Object.keys(progress.error_breakdown).length" class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
        <h2 class="text-lg font-semibold text-gray-700 mb-4">Répartition des erreurs</h2>
        <div class="space-y-3">
          <div v-for="(count, category) in progress.error_breakdown" :key="category">
            <div class="flex items-center justify-between text-sm mb-1">
              <span class="text-gray-600 capitalize">{{ category }}</span>
              <span class="font-medium text-gray-800">{{ count }}</span>
            </div>
            <div class="h-2 rounded-full bg-gray-100 overflow-hidden">
              <div
                class="h-full rounded-full bg-red-400"
                :style="{ width: `${Math.min(100, (count / maxErrorCount) * 100)}%` }"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <div v-if="!loading && !error && !progress" class="text-center py-12 text-gray-400">
      <p>Aucune donnée de progression disponible.</p>
      <router-link to="/practice" class="mt-3 inline-block text-sm text-primary hover:underline">Commencer une leçon</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useApi } from '../composables/useApi'

const { get } = useApi()

const progress = ref(null)
const level = ref(null)
const loading = ref(false)
const error = ref(null)

const levelSkills = computed(() => {
  if (!level.value?.skills) return []
  return Object.entries(level.value.skills).map(([name, score]) => ({ name, score }))
})

const maxErrorCount = computed(() => {
  if (!progress.value?.error_breakdown) return 1
  return Math.max(1, ...Object.values(progress.value.error_breakdown))
})

onMounted(async () => {
  loading.value = true
  try {
    const [progressData, levelData] = await Promise.all([
      get('/progress'),
      get('/progress/level').catch(() => null),
    ])
    progress.value = progressData
    level.value = levelData
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
})
</script>
