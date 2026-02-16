import { defineStore } from 'pinia'
import { useApi } from '../composables/useApi.js'

export const useUserStore = defineStore('user', {
  state: () => ({
    name: '',
    currentLevel: '',
    targetLevel: '',
  }),

  actions: {
    async fetchSettings() {
      const { get } = useApi()
      const data = await get('/settings')
      this.name = data.name ?? ''
      this.currentLevel = data.current_level ?? ''
      this.targetLevel = data.target_level ?? ''
    },

    async updateSettings(data) {
      const { put } = useApi()
      const updated = await put('/settings', data)
      this.name = updated.name ?? this.name
      this.currentLevel = updated.current_level ?? this.currentLevel
      this.targetLevel = updated.target_level ?? this.targetLevel
    },
  },
})
