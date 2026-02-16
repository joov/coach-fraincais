import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import PlanView from '../views/PlanView.vue'
import PracticeView from '../views/PracticeView.vue'
import LessonView from '../views/LessonView.vue'
import ProgressView from '../views/ProgressView.vue'
import SettingsView from '../views/SettingsView.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/plan', component: PlanView },
  { path: '/practice', component: PracticeView },
  { path: '/practice/:lessonId', component: LessonView, props: true },
  { path: '/progress', component: ProgressView },
  { path: '/settings', component: SettingsView },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
