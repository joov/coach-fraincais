import { defineStore } from 'pinia'
import { useApi } from '../composables/useApi.js'

export const useLessonStore = defineStore('lesson', {
  state: () => ({
    lesson: null,
    loading: false,
    currentStep: 'dialogue_informal',
  }),

  actions: {
    async fetchLesson(id) {
      const { get } = useApi()
      this.loading = true
      try {
        this.lesson = await get(`/lessons/${id}`)
        this.currentStep = 'dialogue_informal'
      } finally {
        this.loading = false
      }
    },

    async completeLesson(id) {
      const { post } = useApi()
      await post(`/lessons/${id}/complete`)
    },

    setStep(step) {
      this.currentStep = step
    },
  },
})
