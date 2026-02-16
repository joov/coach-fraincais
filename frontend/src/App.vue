<template>
  <div class="min-h-screen">
    <nav class="bg-primary text-white shadow-lg">
      <div class="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
        <router-link to="/" class="text-xl font-bold">Coach Français</router-link>
        <div class="flex gap-4 text-sm">
          <router-link to="/" class="hover:underline">Accueil</router-link>
          <router-link to="/plan" class="hover:underline">Plan</router-link>
          <router-link to="/practice" class="hover:underline">Pratiquer</router-link>
          <router-link to="/progress" class="hover:underline">Progrès</router-link>
          <router-link to="/settings" class="hover:underline">Paramètres</router-link>
        </div>
      </div>
    </nav>
    <main class="max-w-5xl mx-auto px-4 py-8">
      <router-view />
    </main>
  </div>
</template>
