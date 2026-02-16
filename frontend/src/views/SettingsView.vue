<template>
  <div class="space-y-8">
    <h1 class="text-2xl font-bold text-gray-800">Paramètres</h1>

    <!-- User settings -->
    <section class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm space-y-5">
      <h2 class="text-lg font-semibold text-gray-700">Utilisateur</h2>

      <div>
        <label for="user-name" class="block text-sm font-medium text-gray-600 mb-1">Nom</label>
        <input
          id="user-name"
          v-model="userForm.name"
          type="text"
          placeholder="Votre nom"
          class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:ring-1 focus:ring-primary outline-none"
        />
      </div>

      <div>
        <label for="user-level" class="block text-sm font-medium text-gray-600 mb-1">Niveau actuel</label>
        <select
          id="user-level"
          v-model="userForm.current_level"
          class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:ring-1 focus:ring-primary outline-none"
        >
          <option value="" disabled>Choisir un niveau</option>
          <option v-for="lvl in levels" :key="lvl" :value="lvl">{{ lvl }}</option>
        </select>
      </div>

      <div class="flex items-center gap-3">
        <button
          @click="saveUserSettings"
          :disabled="savingUser"
          class="rounded-lg bg-primary px-5 py-2 text-sm font-medium text-white transition hover:bg-blue-700 disabled:opacity-50"
        >
          {{ savingUser ? 'Enregistrement...' : 'Enregistrer' }}
        </button>
        <span v-if="userMsg" class="text-sm" :class="userMsgType === 'success' ? 'text-green-600' : 'text-red-600'">
          {{ userMsg }}
        </span>
      </div>
    </section>

    <!-- LLM settings -->
    <section class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm space-y-5">
      <h2 class="text-lg font-semibold text-gray-700">Modèle LLM</h2>

      <div>
        <label for="llm-model" class="block text-sm font-medium text-gray-600 mb-1">Nom du modèle</label>
        <input
          id="llm-model"
          v-model="llmForm.model"
          type="text"
          placeholder="gpt-4o-mini"
          class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:ring-1 focus:ring-primary outline-none"
        />
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label for="llm-temperature" class="block text-sm font-medium text-gray-600 mb-1">Température</label>
          <input
            id="llm-temperature"
            v-model.number="llmForm.temperature"
            type="number"
            min="0"
            max="2"
            step="0.1"
            class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:ring-1 focus:ring-primary outline-none"
          />
        </div>
        <div>
          <label for="llm-max-tokens" class="block text-sm font-medium text-gray-600 mb-1">Max tokens</label>
          <input
            id="llm-max-tokens"
            v-model.number="llmForm.max_tokens"
            type="number"
            min="1"
            max="128000"
            step="100"
            class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:ring-1 focus:ring-primary outline-none"
          />
        </div>
      </div>

      <div class="flex items-center gap-3 flex-wrap">
        <button
          @click="saveLlmSettings"
          :disabled="savingLlm"
          class="rounded-lg bg-primary px-5 py-2 text-sm font-medium text-white transition hover:bg-blue-700 disabled:opacity-50"
        >
          {{ savingLlm ? 'Enregistrement...' : 'Enregistrer' }}
        </button>
        <button
          @click="testLlm"
          :disabled="testingLlm"
          class="rounded-lg border border-gray-300 px-5 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-50 disabled:opacity-50"
        >
          {{ testingLlm ? 'Test en cours...' : 'Tester la connexion' }}
        </button>
        <span v-if="llmMsg" class="text-sm" :class="llmMsgType === 'success' ? 'text-green-600' : 'text-red-600'">
          {{ llmMsg }}
        </span>
      </div>

      <!-- Test result -->
      <div v-if="testResult" class="rounded-lg p-4 text-sm" :class="testResult.success ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'">
        <p class="font-medium">{{ testResult.success ? 'Connexion réussie' : 'Echec de la connexion' }}</p>
        <p v-if="testResult.message" class="mt-1">{{ testResult.message }}</p>
        <p v-if="testResult.response" class="mt-1 text-xs font-mono bg-white/50 rounded p-2">{{ testResult.response }}</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useApi } from '../composables/useApi'
import { useUserStore } from '../stores/user'

const { get, put, post } = useApi()
const userStore = useUserStore()

const levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']

// User form
const userForm = reactive({ name: '', current_level: '' })
const savingUser = ref(false)
const userMsg = ref(null)
const userMsgType = ref('success')

// LLM form
const llmForm = reactive({ model: '', temperature: 0.7, max_tokens: 4096 })
const savingLlm = ref(false)
const llmMsg = ref(null)
const llmMsgType = ref('success')
const testingLlm = ref(false)
const testResult = ref(null)

async function saveUserSettings() {
  savingUser.value = true
  userMsg.value = null
  try {
    await put('/settings', {
      name: userForm.name,
      current_level: userForm.current_level,
    })
    userStore.name = userForm.name
    userStore.currentLevel = userForm.current_level
    userMsg.value = 'Paramètres enregistrés'
    userMsgType.value = 'success'
  } catch (err) {
    userMsg.value = err.message
    userMsgType.value = 'error'
  } finally {
    savingUser.value = false
  }
}

async function saveLlmSettings() {
  savingLlm.value = true
  llmMsg.value = null
  try {
    await put('/settings/llm', {
      model: llmForm.model,
      temperature: llmForm.temperature,
      max_tokens: llmForm.max_tokens,
    })
    llmMsg.value = 'Paramètres LLM enregistrés'
    llmMsgType.value = 'success'
  } catch (err) {
    llmMsg.value = err.message
    llmMsgType.value = 'error'
  } finally {
    savingLlm.value = false
  }
}

async function testLlm() {
  testingLlm.value = true
  testResult.value = null
  llmMsg.value = null
  try {
    testResult.value = await post('/settings/llm/test', {})
  } catch (err) {
    testResult.value = { success: false, message: err.message }
  } finally {
    testingLlm.value = false
  }
}

onMounted(async () => {
  try {
    const [settings, llmSettings] = await Promise.all([
      get('/settings').catch(() => null),
      get('/settings/llm').catch(() => null),
    ])
    if (settings) {
      userForm.name = settings.name || ''
      userForm.current_level = settings.current_level || ''
      userStore.name = settings.name || ''
      userStore.currentLevel = settings.current_level || ''
    }
    if (llmSettings) {
      llmForm.model = llmSettings.model || ''
      llmForm.temperature = llmSettings.temperature ?? 0.7
      llmForm.max_tokens = llmSettings.max_tokens ?? 4096
    }
  } catch {
    // Silently ignore load errors — form will be empty
  }
})
</script>
