<template>
  <div class="space-y-6">
    <!-- Loading / Error -->
    <div v-if="loading" class="text-center text-gray-400 py-12">Chargement de la leçon...</div>
    <div v-if="error" class="rounded-lg bg-red-50 p-4 text-red-700 text-sm">{{ error }}</div>

    <template v-if="lesson && !loading">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div>
          <router-link to="/practice" class="text-sm text-gray-400 hover:text-primary transition">&larr; Retour aux leçons</router-link>
          <h1 class="text-2xl font-bold text-gray-800 mt-1">{{ lesson.title || `Leçon ${lessonId}` }}</h1>
        </div>
      </div>

      <!-- Stepper -->
      <nav class="flex items-center gap-1 overflow-x-auto">
        <button
          v-for="(stepDef, idx) in stepDefinitions"
          :key="idx"
          @click="currentStep = idx"
          class="shrink-0 rounded-lg px-4 py-2 text-sm font-medium transition"
          :class="currentStep === idx
            ? 'bg-primary text-white shadow-sm'
            : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
        >
          {{ stepDef.label }}
        </button>
      </nav>

      <!-- Step Content -->
      <div class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm min-h-[300px]">

        <!-- Step 1a: Dialogue informel -->
        <template v-if="currentStep === 0">
          <h2 class="text-lg font-semibold text-gray-700 mb-2">Dialogue informel <span class="text-sm font-normal text-gray-400">(tu)</span></h2>
          <p v-if="dialogueInformalContext" class="text-sm text-gray-500 mb-4 italic">{{ dialogueInformalContext }}</p>
          <div v-if="!dialogueInformal.length" class="text-gray-400 text-sm">Aucun dialogue disponible.</div>
          <div class="space-y-3">
            <div
              v-for="(line, idx) in dialogueInformal"
              :key="idx"
              class="flex items-start gap-3 rounded-lg p-3"
              :class="idx % 2 === 0 ? 'bg-blue-50' : 'bg-gray-50'"
            >
              <span class="shrink-0 inline-flex h-7 w-auto min-w-[1.75rem] items-center justify-center rounded-full px-2 text-xs font-bold"
                :class="idx % 2 === 0 ? 'bg-primary text-white' : 'bg-gray-300 text-gray-700'"
              >
                {{ line.speaker }}
              </span>
              <div class="flex-1 min-w-0">
                <p class="text-sm text-gray-800">{{ line.text }}</p>
                <p v-if="line.translation" class="text-xs text-gray-400 mt-1">{{ line.translation }}</p>
              </div>
              <div class="flex items-center gap-1 shrink-0">
                <button
                  @click="speak(line.text, { speaker: line.speaker })"
                  :disabled="isSpeaking"
                  class="rounded-lg p-1.5 text-gray-400 hover:text-primary hover:bg-blue-50 transition disabled:opacity-40"
                  title="Ecouter"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.536 8.464a5 5 0 010 7.072M17.95 6.05a8 8 0 010 11.9M6.5 8.788V15.212a.3.3 0 00.476.244l5.024-3.213a.3.3 0 000-.486L6.976 8.544A.3.3 0 006.5 8.788z" />
                  </svg>
                </button>
                <button
                  @click="toggleRecord(line.text, 'informal')"
                  class="rounded-lg p-1.5 transition"
                  :class="isRecording && recordingTarget === line.text ? 'text-red-500 bg-red-50 animate-pulse' : 'text-gray-400 hover:text-red-500 hover:bg-red-50'"
                  :title="isRecording && recordingTarget === line.text ? 'Arrêter' : 'Enregistrer'"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19 11a7 7 0 01-14 0M12 19v2m-3 0h6M12 3a4 4 0 00-4 4v4a4 4 0 008 0V7a4 4 0 00-4-4z" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
          <!-- Spinner while waiting -->
          <div v-if="transcribing" class="mt-4 flex items-center gap-3 rounded-lg bg-blue-50 p-4 text-sm text-blue-700">
            <svg class="h-5 w-5 animate-spin text-primary" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            Analyse en cours...
          </div>

          <!-- Transcription result with word highlighting -->
          <template v-if="transcribeResult && !transcribing">
            <div class="mt-4 space-y-3">
              <!-- Error -->
              <div v-if="transcribeResult._error" class="rounded-lg bg-red-50 p-4 text-sm text-red-700">
                Erreur : {{ transcribeResult._error }}
              </div>

              <template v-else>
                <!-- Score bar -->
                <div class="rounded-lg border border-gray-200 bg-white p-4">
                  <div class="flex items-center justify-between mb-2">
                    <span class="text-sm font-medium text-gray-700">Score</span>
                    <span class="text-lg font-bold" :class="scoreColor(transcribeResult.comparison?.score)">
                      {{ transcribeResult.comparison?.score ?? 0 }}%
                    </span>
                  </div>
                  <div class="h-2.5 w-full rounded-full bg-gray-200 overflow-hidden">
                    <div
                      class="h-full rounded-full transition-all duration-500"
                      :class="scoreBarColor(transcribeResult.comparison?.score)"
                      :style="{ width: (transcribeResult.comparison?.score ?? 0) + '%' }"
                    ></div>
                  </div>
                </div>

                <!-- Word comparison -->
                <div class="rounded-lg border border-gray-200 bg-white p-4">
                  <p class="text-xs font-medium text-gray-400 uppercase mb-2">Comparaison mot à mot</p>
                  <p class="text-sm leading-relaxed">
                    <span v-for="(w, wIdx) in (transcribeResult.comparison?.words || [])" :key="wIdx">
                      <span
                        class="inline-block px-1 py-0.5 rounded mx-0.5 text-sm font-medium"
                        :class="w.match ? 'bg-green-100 text-green-800' : w.partial ? 'bg-yellow-100 text-yellow-800' : 'bg-red-100 text-red-800 line-through'"
                        :title="w.match ? 'Correct' : w.spoken ? `Vous avez dit : ${w.spoken}` : 'Mot manquant'"
                      >{{ w.word }}</span>
                    </span>
                  </p>
                </div>

                <!-- What you said -->
                <div class="rounded-lg bg-gray-50 p-4 text-sm text-gray-600">
                  <p><strong>Texte cible :</strong> {{ transcribeResult._targetText }}</p>
                  <p class="mt-1"><strong>Votre texte :</strong> {{ transcribeResult.transcription || '(vide)' }}</p>
                </div>

                <!-- LLM feedback if available -->
                <div v-if="transcribeResult.evaluation?.feedback" class="rounded-lg bg-blue-50 p-4 text-sm text-blue-800">
                  <p>{{ transcribeResult.evaluation.feedback }}</p>
                </div>
              </template>
            </div>
          </template>
        </template>

        <!-- Step 1b: Dialogue formel -->
        <template v-if="currentStep === 1">
          <h2 class="text-lg font-semibold text-gray-700 mb-2">Dialogue formel <span class="text-sm font-normal text-gray-400">(vous)</span></h2>
          <p v-if="dialogueFormalContext" class="text-sm text-gray-500 mb-4 italic">{{ dialogueFormalContext }}</p>
          <div v-if="!dialogueFormal.length" class="text-gray-400 text-sm">Aucun dialogue disponible.</div>
          <div class="space-y-3">
            <div
              v-for="(line, idx) in dialogueFormal"
              :key="idx"
              class="flex items-start gap-3 rounded-lg p-3"
              :class="idx % 2 === 0 ? 'bg-blue-50' : 'bg-gray-50'"
            >
              <span class="shrink-0 inline-flex h-7 w-auto min-w-[1.75rem] items-center justify-center rounded-full px-2 text-xs font-bold"
                :class="idx % 2 === 0 ? 'bg-primary text-white' : 'bg-gray-300 text-gray-700'"
              >
                {{ line.speaker }}
              </span>
              <div class="flex-1 min-w-0">
                <p class="text-sm text-gray-800">{{ line.text }}</p>
                <p v-if="line.translation" class="text-xs text-gray-400 mt-1">{{ line.translation }}</p>
              </div>
              <div class="flex items-center gap-1 shrink-0">
                <button
                  @click="speak(line.text, { speaker: line.speaker })"
                  :disabled="isSpeaking"
                  class="rounded-lg p-1.5 text-gray-400 hover:text-primary hover:bg-blue-50 transition disabled:opacity-40"
                  title="Ecouter"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.536 8.464a5 5 0 010 7.072M17.95 6.05a8 8 0 010 11.9M6.5 8.788V15.212a.3.3 0 00.476.244l5.024-3.213a.3.3 0 000-.486L6.976 8.544A.3.3 0 006.5 8.788z" />
                  </svg>
                </button>
                <button
                  @click="toggleRecord(line.text, 'formal')"
                  class="rounded-lg p-1.5 transition"
                  :class="isRecording && recordingTarget === line.text ? 'text-red-500 bg-red-50 animate-pulse' : 'text-gray-400 hover:text-red-500 hover:bg-red-50'"
                  :title="isRecording && recordingTarget === line.text ? 'Arrêter' : 'Enregistrer'"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19 11a7 7 0 01-14 0M12 19v2m-3 0h6M12 3a4 4 0 00-4 4v4a4 4 0 008 0V7a4 4 0 00-4-4z" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
          <!-- Spinner while waiting -->
          <div v-if="transcribing" class="mt-4 flex items-center gap-3 rounded-lg bg-blue-50 p-4 text-sm text-blue-700">
            <svg class="h-5 w-5 animate-spin text-primary" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            Analyse en cours...
          </div>

          <!-- Transcription result with word highlighting -->
          <template v-if="transcribeResult && !transcribing">
            <div class="mt-4 space-y-3">
              <div v-if="transcribeResult._error" class="rounded-lg bg-red-50 p-4 text-sm text-red-700">
                Erreur : {{ transcribeResult._error }}
              </div>

              <template v-else>
                <div class="rounded-lg border border-gray-200 bg-white p-4">
                  <div class="flex items-center justify-between mb-2">
                    <span class="text-sm font-medium text-gray-700">Score</span>
                    <span class="text-lg font-bold" :class="scoreColor(transcribeResult.comparison?.score)">
                      {{ transcribeResult.comparison?.score ?? 0 }}%
                    </span>
                  </div>
                  <div class="h-2.5 w-full rounded-full bg-gray-200 overflow-hidden">
                    <div
                      class="h-full rounded-full transition-all duration-500"
                      :class="scoreBarColor(transcribeResult.comparison?.score)"
                      :style="{ width: (transcribeResult.comparison?.score ?? 0) + '%' }"
                    ></div>
                  </div>
                </div>

                <div class="rounded-lg border border-gray-200 bg-white p-4">
                  <p class="text-xs font-medium text-gray-400 uppercase mb-2">Comparaison mot à mot</p>
                  <p class="text-sm leading-relaxed">
                    <span v-for="(w, wIdx) in (transcribeResult.comparison?.words || [])" :key="wIdx">
                      <span
                        class="inline-block px-1 py-0.5 rounded mx-0.5 text-sm font-medium"
                        :class="w.match ? 'bg-green-100 text-green-800' : w.partial ? 'bg-yellow-100 text-yellow-800' : 'bg-red-100 text-red-800 line-through'"
                        :title="w.match ? 'Correct' : w.spoken ? `Vous avez dit : ${w.spoken}` : 'Mot manquant'"
                      >{{ w.word }}</span>
                    </span>
                  </p>
                </div>

                <div class="rounded-lg bg-gray-50 p-4 text-sm text-gray-600">
                  <p><strong>Texte cible :</strong> {{ transcribeResult._targetText }}</p>
                  <p class="mt-1"><strong>Votre texte :</strong> {{ transcribeResult.transcription || '(vide)' }}</p>
                </div>

                <div v-if="transcribeResult.evaluation?.feedback" class="rounded-lg bg-blue-50 p-4 text-sm text-blue-800">
                  <p>{{ transcribeResult.evaluation.feedback }}</p>
                </div>
              </template>
            </div>
          </template>
        </template>

        <!-- Step 2: Exercises -->
        <template v-if="currentStep === 2">
          <h2 class="text-lg font-semibold text-gray-700 mb-4">Exercices</h2>
          <div v-if="!exercises.length" class="text-gray-400 text-sm">Aucun exercice disponible.</div>

          <div class="space-y-6">
            <div v-for="(ex, idx) in exercises" :key="idx" class="rounded-lg border border-gray-100 p-4 space-y-3">
              <p class="text-sm font-medium text-gray-700">{{ idx + 1 }}. {{ ex.instruction || ex.question || ex.prompt }}</p>
              <p v-if="ex.question && ex.instruction" class="text-sm text-gray-800 mt-1">{{ ex.question }}</p>
              <span v-if="ex.register" class="inline-block mt-1 rounded-full px-2 py-0.5 text-xs font-medium"
                :class="ex.register === 'formal' ? 'bg-purple-100 text-purple-700' : ex.register === 'informal' ? 'bg-cyan-100 text-cyan-700' : 'bg-gray-100 text-gray-500'"
              >{{ ex.register === 'formal' ? 'formel (vous)' : ex.register === 'informal' ? 'informel (tu)' : ex.register }}</span>

              <!-- fill_blank -->
              <template v-if="ex.type === 'fill_blank'">
                <div class="text-sm text-gray-600">
                  <span v-for="(part, pIdx) in parseBlanks(ex.template)" :key="pIdx">
                    <span v-if="part.type === 'text'">{{ part.value }}</span>
                    <input
                      v-else
                      v-model="exerciseAnswers[idx][part.index]"
                      class="inline-block w-28 border-b-2 border-gray-300 focus:border-primary outline-none px-1 mx-1 text-center bg-transparent"
                      :placeholder="`___`"
                    />
                  </span>
                </div>
              </template>

              <!-- multiple_choice -->
              <template v-if="ex.type === 'multiple_choice'">
                <div class="space-y-2">
                  <label
                    v-for="(option, oIdx) in ex.options"
                    :key="oIdx"
                    class="flex items-center gap-3 rounded-lg border px-4 py-2.5 cursor-pointer transition text-sm"
                    :class="exerciseAnswers[idx] === option ? 'border-primary bg-blue-50 text-primary' : 'border-gray-200 hover:border-gray-300'"
                  >
                    <input
                      type="radio"
                      :name="`exercise-${idx}`"
                      :value="option"
                      v-model="exerciseAnswers[idx]"
                      class="text-primary focus:ring-primary"
                    />
                    {{ option }}
                  </label>
                </div>
              </template>

              <!-- reorder -->
              <template v-if="ex.type === 'reorder'">
                <p class="text-xs text-gray-400 mb-3">Numérotez les répliques dans le bon ordre (1, 2, 3...) :</p>
                <div class="space-y-2">
                  <div
                    v-for="(line, lIdx) in (ex.lines || [])"
                    :key="lIdx"
                    class="flex items-center gap-3 rounded-lg border border-gray-200 bg-white px-4 py-3"
                  >
                    <input
                      v-model.number="exerciseAnswers[idx][lIdx]"
                      type="number"
                      min="1"
                      :max="(ex.lines || []).length"
                      class="w-12 rounded border border-gray-300 px-2 py-1 text-sm text-center focus:border-primary focus:ring-1 focus:ring-primary outline-none"
                      :placeholder="String(lIdx + 1)"
                    />
                    <span class="text-sm text-gray-700">{{ line }}</span>
                  </div>
                </div>
              </template>

              <!-- match -->
              <template v-if="ex.type === 'match'">
                <div class="space-y-3">
                  <div
                    v-for="(pair, mIdx) in (ex.pairs || [])"
                    :key="mIdx"
                    class="flex items-center gap-3 rounded-lg border border-gray-200 bg-white px-4 py-3"
                  >
                    <span class="text-sm text-gray-800 flex-1 font-medium">{{ pair.informal }}</span>
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-300 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                    </svg>
                    <select
                      v-model="exerciseAnswers[idx][mIdx]"
                      class="flex-1 rounded-lg border border-gray-300 px-3 py-1.5 text-sm focus:border-primary focus:ring-1 focus:ring-primary outline-none"
                    >
                      <option value="" disabled>Choisir l'équivalent formel...</option>
                      <option
                        v-for="(opt, oIdx) in shuffledFormalOptions(ex.pairs)"
                        :key="oIdx"
                        :value="opt"
                      >{{ opt }}</option>
                    </select>
                  </div>
                </div>
              </template>

              <!-- transform -->
              <template v-if="ex.type === 'transform'">
                <div class="space-y-3">
                  <div
                    v-for="(item, tIdx) in (ex.items || [])"
                    :key="tIdx"
                    class="rounded-lg border border-gray-200 bg-white px-4 py-3 space-y-2"
                  >
                    <div class="flex items-center gap-2">
                      <span class="inline-block rounded-full px-2 py-0.5 text-xs font-medium"
                        :class="item.source_register === 'formal' ? 'bg-purple-100 text-purple-700' : 'bg-cyan-100 text-cyan-700'"
                      >{{ item.source_register === 'formal' ? 'formel' : 'informel' }}</span>
                      <span class="text-sm text-gray-800 font-medium">{{ item.source }}</span>
                    </div>
                    <div class="flex items-center gap-2">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-300 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                      </svg>
                      <span class="inline-block rounded-full px-2 py-0.5 text-xs font-medium"
                        :class="item.target_register === 'formal' ? 'bg-purple-100 text-purple-700' : 'bg-cyan-100 text-cyan-700'"
                      >{{ item.target_register === 'formal' ? 'formel' : 'informel' }}</span>
                    </div>
                    <input
                      v-model="exerciseAnswers[idx][tIdx]"
                      type="text"
                      :placeholder="`Transformez en ${item.target_register === 'formal' ? 'formel (vous)' : 'informel (tu)'}...`"
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:ring-1 focus:ring-primary outline-none"
                    />
                  </div>
                </div>
              </template>

              <!-- free_answer -->
              <template v-if="ex.type === 'free_answer'">
                <div class="space-y-3">
                  <div
                    v-for="(q, qIdx) in (ex.questions || [])"
                    :key="qIdx"
                    class="rounded-lg border border-gray-200 bg-white px-4 py-3 space-y-2"
                  >
                    <p class="text-sm text-gray-800 font-medium">{{ q.question }}</p>
                    <p v-if="q.hint" class="text-xs text-gray-400 italic">Indice : {{ q.hint }}</p>
                    <input
                      v-model="exerciseAnswers[idx][qIdx]"
                      type="text"
                      placeholder="Votre réponse..."
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:ring-1 focus:ring-primary outline-none"
                    />
                  </div>
                </div>
              </template>
            </div>
          </div>

          <!-- Submit exercises -->
          <div v-if="exercises.length" class="pt-4">
            <button
              @click="submitExercises"
              :disabled="submittingExercises"
              class="rounded-lg bg-primary px-6 py-2.5 text-sm font-medium text-white transition hover:bg-blue-700 disabled:opacity-50"
            >
              {{ submittingExercises ? 'Envoi...' : 'Vérifier les réponses' }}
            </button>
          </div>

          <!-- Exercise result -->
          <div v-if="exerciseResult" class="mt-4 rounded-lg p-4 text-sm" :class="exerciseResult.all_correct ? 'bg-green-50 text-green-700' : 'bg-yellow-50 text-yellow-700'">
            <p class="font-medium">{{ exerciseResult.all_correct ? 'Parfait ! Toutes les réponses sont correctes.' : `Score : ${exerciseResult.score}%` }}</p>
            <ul v-if="exerciseResult.feedback" class="mt-2 space-y-1">
              <li v-for="(fb, fbIdx) in exerciseResult.feedback" :key="fbIdx">
                <span :class="fb.correct ? 'text-green-600' : 'text-red-600'">{{ fb.correct ? '&#10003;' : '&#10007;' }}</span>
                {{ fb.message || '' }}
              </li>
            </ul>
          </div>
        </template>

        <!-- Step 3: Grammar box -->
        <template v-if="currentStep === 3">
          <h2 class="text-lg font-semibold text-gray-700 mb-4">Grammaire</h2>
          <div v-if="!lesson.grammar_box" class="text-gray-400 text-sm">Aucune fiche de grammaire disponible.</div>
          <div v-else class="prose prose-sm max-w-none text-gray-700" v-html="renderGrammar(lesson.grammar_box)"></div>
        </template>
      </div>

      <!-- Navigation -->
      <div class="flex items-center justify-between">
        <button
          @click="currentStep = Math.max(0, currentStep - 1)"
          :disabled="currentStep === 0"
          class="rounded-lg border border-gray-300 px-5 py-2 text-sm font-medium text-gray-600 transition hover:bg-gray-50 disabled:opacity-30 disabled:cursor-not-allowed"
        >
          &larr; Précédent
        </button>

        <span class="text-sm text-gray-400">{{ currentStep + 1 }} / {{ stepDefinitions.length }}</span>

        <button
          v-if="currentStep < stepDefinitions.length - 1"
          @click="currentStep = Math.min(stepDefinitions.length - 1, currentStep + 1)"
          class="rounded-lg bg-primary px-5 py-2 text-sm font-medium text-white transition hover:bg-blue-700"
        >
          Suivant &rarr;
        </button>
        <button
          v-else
          @click="markComplete"
          :disabled="completing"
          class="rounded-lg bg-green-600 px-5 py-2 text-sm font-medium text-white transition hover:bg-green-700 disabled:opacity-50"
        >
          {{ completing ? 'En cours...' : 'Terminer la leçon' }}
        </button>
      </div>

      <div v-if="completeMsg" class="rounded-lg bg-green-50 p-4 text-green-700 text-sm text-center">{{ completeMsg }}</div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useApi } from '../composables/useApi'
import { useTTS } from '../composables/useTTS'
import { useRecorder } from '../composables/useRecorder'
import { useLessonStore } from '../stores/lesson'

const props = defineProps({
  lessonId: { type: String, required: true },
})

const { get, post, postForm } = useApi()
const { speak, stop, isSpeaking } = useTTS()
const { startRecording, stopRecording, isRecording, audioBlob } = useRecorder()
const lessonStore = useLessonStore()

const lesson = ref(null)
const loading = ref(false)
const error = ref(null)
const currentStep = ref(0)

const stepDefinitions = [
  { label: '1a. Dialogue informel' },
  { label: '1b. Dialogue formel' },
  { label: '2. Exercices' },
  { label: '3. Grammaire' },
]

// Dialogue data — API returns lesson.dialogues.informal.lines / lesson.dialogues.formal.lines
const dialogueInformal = computed(() => lesson.value?.dialogues?.informal?.lines || [])
const dialogueFormal = computed(() => lesson.value?.dialogues?.formal?.lines || [])
const dialogueInformalContext = computed(() => lesson.value?.dialogues?.informal?.context || '')
const dialogueFormalContext = computed(() => lesson.value?.dialogues?.formal?.context || '')

// Exercises
const exercises = computed(() => lesson.value?.exercises || [])
const exerciseAnswers = ref([])
const submittingExercises = ref(false)
const exerciseResult = ref(null)

// Recording state
const recordingTarget = ref(null)
const recordingRegister = ref(null)
const transcribeResult = ref(null)
const transcribing = ref(false)

// Completion
const completing = ref(false)
const completeMsg = ref(null)

// Initialize exercise answers when lesson loads
watch(exercises, (exs) => {
  exerciseAnswers.value = exs.map((ex) => {
    if (ex.type === 'fill_blank') {
      const blanks = (ex.template || '').match(/_{2,}|\[\.\.\.\]/g) || []
      return Array(blanks.length).fill('')
    }
    if (ex.type === 'reorder') {
      return Array((ex.lines || []).length).fill(null)
    }
    if (ex.type === 'match') {
      return Array((ex.pairs || []).length).fill('')
    }
    if (ex.type === 'transform') {
      return Array((ex.items || []).length).fill('')
    }
    if (ex.type === 'free_answer') {
      return Array((ex.questions || []).length).fill('')
    }
    return ''
  })
}, { immediate: true })

// Shuffle formal options for match exercises so they're not in the same order as informal
const _shuffleCache = new Map()
function shuffledFormalOptions(pairs) {
  if (!pairs) return []
  const key = pairs.map(p => p.formal).join('|')
  if (_shuffleCache.has(key)) return _shuffleCache.get(key)
  const options = pairs.map(p => p.formal)
  // Simple Fisher-Yates shuffle
  for (let i = options.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [options[i], options[j]] = [options[j], options[i]]
  }
  _shuffleCache.set(key, options)
  return options
}

function parseBlanks(template) {
  if (!template) return [{ type: 'text', value: '' }]
  const parts = []
  let blankIdx = 0
  const segments = template.split(/(_{2,}|\[\.\.\.\])/)
  for (const seg of segments) {
    if (/^_{2,}$/.test(seg) || seg === '[...]') {
      parts.push({ type: 'blank', index: blankIdx++ })
    } else if (seg) {
      parts.push({ type: 'text', value: seg })
    }
  }
  return parts
}

async function toggleRecord(targetText, register) {
  if (isRecording.value && recordingTarget.value === targetText) {
    // Stop and submit
    const blob = await stopRecording()
    recordingTarget.value = null
    transcribeResult.value = null
    transcribing.value = true

    const fd = new FormData()
    fd.append('file', blob, 'recording.webm')
    fd.append('target_text', targetText)
    fd.append('lesson_id', props.lessonId)
    fd.append('register', register)

    try {
      const result = await postForm('/speech/transcribe', fd)
      transcribeResult.value = { ...result, _targetText: targetText }
    } catch (err) {
      transcribeResult.value = {
        transcription: '',
        comparison: { score: 0, words: [] },
        _targetText: targetText,
        _error: err.message,
      }
    } finally {
      transcribing.value = false
    }
  } else {
    // Stop any other recording first
    if (isRecording.value) {
      await stopRecording()
    }
    transcribeResult.value = null
    transcribing.value = false
    recordingTarget.value = targetText
    recordingRegister.value = register
    await startRecording()
  }
}

async function submitExercises() {
  submittingExercises.value = true
  exerciseResult.value = null
  try {
    const answers = exercises.value.map((ex, idx) => ({
      exercise_index: idx,
      type: ex.type,
      answer: exerciseAnswers.value[idx],
    }))
    exerciseResult.value = await post(`/exercises/${props.lessonId}/answer`, { answers })
  } catch (err) {
    exerciseResult.value = { all_correct: false, score: 0, feedback: [{ correct: false, message: err.message }] }
  } finally {
    submittingExercises.value = false
  }
}

async function markComplete() {
  completing.value = true
  completeMsg.value = null
  try {
    await post(`/lessons/${props.lessonId}/complete`, {})
    completeMsg.value = 'Leçon terminée ! Bravo !'
  } catch (err) {
    completeMsg.value = `Erreur : ${err.message}`
  } finally {
    completing.value = false
  }
}

function renderGrammar(box) {
  if (!box) return ''
  if (typeof box === 'string') {
    return box.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>')
  }

  let html = ''

  if (box.title) {
    html += `<h3 class="text-base font-bold text-gray-800 mb-3">${esc(box.title)}</h3>`
  }

  if (box.rules && box.rules.length) {
    html += '<ul class="list-disc pl-5 mb-4 space-y-1">'
    for (const rule of box.rules) {
      html += `<li class="text-sm text-gray-700">${esc(rule)}</li>`
    }
    html += '</ul>'
  }

  if (box.formal_informal_comparison && box.formal_informal_comparison.length) {
    html += '<h4 class="text-sm font-semibold text-gray-600 mb-2">Informel vs. Formel</h4>'
    html += '<table class="w-full text-sm mb-4 border border-gray-200 rounded-lg overflow-hidden">'
    html += '<thead><tr class="bg-gray-50"><th class="px-3 py-2 text-left text-gray-500 font-medium">Informel (tu)</th><th class="px-3 py-2 text-left text-gray-500 font-medium">Formel (vous)</th></tr></thead><tbody>'
    for (const pair of box.formal_informal_comparison) {
      html += `<tr class="border-t border-gray-100"><td class="px-3 py-2">${esc(pair.informal)}</td><td class="px-3 py-2">${esc(pair.formal)}</td></tr>`
    }
    html += '</tbody></table>'
  }

  if (box.pronunciation_hints && box.pronunciation_hints.length) {
    html += '<h4 class="text-sm font-semibold text-gray-600 mb-2">Prononciation</h4>'
    html += '<ul class="list-disc pl-5 space-y-1">'
    for (const hint of box.pronunciation_hints) {
      html += `<li class="text-sm text-gray-700">${esc(hint)}</li>`
    }
    html += '</ul>'
  }

  return html || `<pre class="text-xs text-gray-500">${JSON.stringify(box, null, 2)}</pre>`
}

function esc(s) {
  if (!s) return ''
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
}

function scoreColor(score) {
  if (score == null) return 'text-gray-400'
  if (score >= 80) return 'text-green-600'
  if (score >= 50) return 'text-yellow-600'
  return 'text-red-600'
}

function scoreBarColor(score) {
  if (score == null) return 'bg-gray-300'
  if (score >= 80) return 'bg-green-500'
  if (score >= 50) return 'bg-yellow-500'
  return 'bg-red-500'
}

onMounted(async () => {
  loading.value = true
  try {
    const data = await get(`/lessons/${props.lessonId}`)
    lesson.value = data
    lessonStore.lesson = data
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
})
</script>
