<template>
  <div class="space-y-8">
    <h1 class="text-2xl font-bold text-gray-800">Plan d'entraînement</h1>

    <!-- Plan creation form -->
    <form
      @submit.prevent="createPlan"
      class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm space-y-5"
    >
      <h2 class="text-lg font-semibold text-gray-700">Créer un nouveau plan</h2>

      <!-- Target level -->
      <div>
        <label for="target_level" class="block text-sm font-medium text-gray-600 mb-1">Niveau cible</label>
        <select
          id="target_level"
          v-model="form.target_level"
          class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:ring-1 focus:ring-primary outline-none"
        >
          <option value="" disabled>Choisir un niveau</option>
          <option v-for="lvl in levels" :key="lvl" :value="lvl">{{ lvl }}</option>
        </select>
      </div>

      <!-- Grammar focus -->
      <div>
        <label for="grammar_focus" class="block text-sm font-medium text-gray-600 mb-1">Points de grammaire (séparés par des virgules)</label>
        <input
          id="grammar_focus"
          v-model="form.grammar_focus"
          type="text"
          placeholder="passé composé, subjonctif, conditionnel"
          class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:ring-1 focus:ring-primary outline-none"
        />
      </div>

      <!-- Topic focus -->
      <div>
        <label for="topic_focus" class="block text-sm font-medium text-gray-600 mb-1">Thèmes (séparés par des virgules)</label>
        <input
          id="topic_focus"
          v-model="form.topic_focus"
          type="text"
          placeholder="voyages, cuisine, travail"
          class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:ring-1 focus:ring-primary outline-none"
        />
      </div>

      <!-- Minutes per day -->
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label for="minutes_per_day" class="block text-sm font-medium text-gray-600 mb-1">Minutes par jour</label>
          <input
            id="minutes_per_day"
            v-model.number="form.minutes_per_day"
            type="number"
            min="5"
            max="120"
            class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:ring-1 focus:ring-primary outline-none"
          />
        </div>

        <!-- Days per week -->
        <div>
          <label for="days_per_week" class="block text-sm font-medium text-gray-600 mb-1">Jours par semaine</label>
          <input
            id="days_per_week"
            v-model.number="form.days_per_week"
            type="number"
            min="1"
            max="7"
            class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:ring-1 focus:ring-primary outline-none"
          />
        </div>
      </div>

      <!-- Submit -->
      <button
        type="submit"
        :disabled="submitting"
        class="w-full rounded-lg bg-primary px-4 py-2.5 text-sm font-medium text-white transition hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {{ submitting ? 'Création en cours...' : 'Créer le plan' }}
      </button>

      <div v-if="formError" class="rounded-lg bg-red-50 p-3 text-red-700 text-sm">{{ formError }}</div>
      <div v-if="formSuccess" class="rounded-lg bg-green-50 p-3 text-green-700 text-sm">Plan créé avec succès !</div>
    </form>

    <!-- Existing plan display -->
    <div v-if="loadingPlan" class="text-center text-gray-400">Chargement du plan...</div>
    <div v-if="planError" class="rounded-lg bg-red-50 p-4 text-red-700 text-sm">{{ planError }}</div>

    <div v-if="planData" class="space-y-6">
      <h2 class="text-xl font-bold text-gray-800">Votre plan actuel</h2>
      <div class="text-sm text-gray-500 space-x-4">
        <span>Niveau cible : <span class="font-medium text-gray-700">{{ planData.target_level }}</span></span>
        <span v-if="planWeeks.length">{{ planData.plan?.total_lessons || planWeeks.reduce((s, w) => s + (w.lessons?.length || 0), 0) }} leçons</span>
      </div>

      <!-- Weeks -->
      <div v-for="(week, wIdx) in planWeeks" :key="wIdx" class="rounded-2xl border border-gray-200 bg-white shadow-sm overflow-hidden">
        <div class="bg-gray-50 px-5 py-3 border-b border-gray-200">
          <h3 class="font-semibold text-gray-700">Semaine {{ week.week_number || wIdx + 1 }}</h3>
        </div>
        <ul class="divide-y divide-gray-100">
          <li
            v-for="(lesson, lIdx) in week.lessons"
            :key="lIdx"
            class="px-5 py-3 flex items-center justify-between"
          >
            <div>
              <span class="text-sm font-medium text-gray-800">
                {{ lesson.lesson_number ? `${lesson.lesson_number}. ` : '' }}{{ lesson.title || `Leçon ${lIdx + 1}` }}
              </span>
              <span v-if="lesson.is_priority" class="ml-2 text-xs text-amber-500 font-medium">Priorité</span>
              <span v-if="lesson.extra_practice" class="ml-2 text-xs text-purple-500">+</span>
            </div>
            <router-link
              v-if="lesson.lesson_number"
              :to="`/practice/${lesson.lesson_number}`"
              class="text-xs text-primary hover:underline"
            >
              Pratiquer
            </router-link>
          </li>
        </ul>
      </div>

      <!-- Notes -->
      <div v-if="planData.plan?.notes" class="rounded-xl bg-blue-50 border border-blue-200 p-4 text-sm text-blue-800">
        {{ planData.plan.notes }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useApi } from '../composables/useApi'
import { usePlanStore } from '../stores/plan'

const { get, post } = useApi()
const planStore = usePlanStore()

const levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']

const form = reactive({
  target_level: '',
  grammar_focus: '',
  topic_focus: '',
  minutes_per_day: 20,
  days_per_week: 5,
})

const submitting = ref(false)
const formError = ref(null)
const formSuccess = ref(false)

const planData = ref(null)
const loadingPlan = ref(false)
const planError = ref(null)

// The API returns { id, target_level, ..., plan: { weeks: [...], ... } }
const planWeeks = computed(() => {
  if (!planData.value) return []
  const p = planData.value.plan
  if (!p) return []
  // plan_data might have weeks directly or nested
  return p.weeks || []
})

async function fetchPlan() {
  loadingPlan.value = true
  planError.value = null
  try {
    const data = await get('/plan')
    // GET /api/plan returns { plan: null } when no plan exists
    if (data && data.plan !== null && data.id) {
      planData.value = data
      planStore.plan = data
    }
  } catch (err) {
    if (!err.message?.includes('404')) {
      planError.value = err.message
    }
  } finally {
    loadingPlan.value = false
  }
}

async function createPlan() {
  submitting.value = true
  formError.value = null
  formSuccess.value = false
  try {
    const payload = {
      target_level: form.target_level,
      grammar_focus: form.grammar_focus.split(',').map((s) => s.trim()).filter(Boolean),
      topic_focus: form.topic_focus.split(',').map((s) => s.trim()).filter(Boolean),
      minutes_per_day: form.minutes_per_day,
      days_per_week: form.days_per_week,
    }
    const data = await post('/plan', payload)
    planData.value = data
    planStore.plan = data
    formSuccess.value = true
  } catch (err) {
    formError.value = err.message
  } finally {
    submitting.value = false
  }
}

onMounted(fetchPlan)
</script>
