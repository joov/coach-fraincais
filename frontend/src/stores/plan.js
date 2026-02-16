import { defineStore } from 'pinia'
import { useApi } from '../composables/useApi.js'

export const usePlanStore = defineStore('plan', {
  state: () => ({
    plan: null,
    loading: false,
  }),

  actions: {
    async fetchPlan() {
      const { get } = useApi()
      this.loading = true
      try {
        this.plan = await get('/plan')
      } finally {
        this.loading = false
      }
    },

    async createPlan(data) {
      const { post } = useApi()
      this.loading = true
      try {
        this.plan = await post('/plan', {
          target_level: data.target_level,
          grammar_focus: data.grammar_focus,
          topic_focus: data.topic_focus,
          minutes_per_day: data.minutes_per_day,
          days_per_week: data.days_per_week,
        })
      } finally {
        this.loading = false
      }
    },
  },
})
