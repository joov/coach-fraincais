/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts}'],
  theme: {
    extend: {
      colors: {
        primary: '#2563eb',
        accent: '#0ea5e9',
      },
    },
  },
  plugins: [],
}
